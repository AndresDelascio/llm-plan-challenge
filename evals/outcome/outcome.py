"""Outcome test: does a plan, or a reviewed plan, make the first build pass more often than plain chat?
Rules are in outcome.md. Every model call goes through the skill's own review.review(), so it runs
in an empty temporary folder with tools off. Hidden tests decide pass or fail; no AI grades anything."""

import argparse
import json
import os
from pathlib import Path
import re
import secrets
from statistics import median
import subprocess
import sys
import tempfile
from time import monotonic

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / ".claude/skills/challenge"))
sys.path.insert(0, str(ROOT / "evals/plan-review"))
import review  # noqa: E402
from followup import REVISE  # noqa: E402  (the same frozen revise prompt as the follow-up tests)

# Frozen prompts and limits. Do not edit after the first live call.
BUILD = (
    "Write the Python code the user asks for. Use only the standard library. "
    "Reply with one ```python code block and nothing else."
)
BETTER = "Make this prompt better. Return only the improved prompt."
PLAN = (
    "Write a plan for the task below. Do not write the code. Use exactly these three headings: "
    "'## Brief' (Goal, Constraints, Non-goals), '## Plan' (numbered steps) and "
    "'## Risks I already know about'. Stay under 300 words. Return only the plan."
)
RETRY = (
    "\n\n=== YOUR PREVIOUS CODE ===\n{code}\n\n=== RESULT ===\n"
    "It failed a check: {symptom}. Return the full corrected code."
)
MAX_REPROMPTS = 10
TEST_TIMEOUT_S = 10
ARMS = ("plain", "better", "plan", "challenge")
TASKS = sorted(path.stem for path in (HERE / "tasks").glob("*.txt"))

# Missing-fact suite (rules in missing.md), frozen before its first call. The prompts in
# tasks-missing/ leave out facts that are in *_facts.txt; the hidden tests are the same as above.
# A plan, or a chat reply with no code, that asks the user a question gets the whole facts sheet.
PLAN_ASK = (
    "Write a plan for the task below. Do not write the code. Use exactly these four headings: "
    "'## Brief' (Goal, Constraints, Non-goals), '## Plan' (numbered steps), "
    "'## Risks I already know about' and '## Questions for the user' (facts you need from the user "
    "before building, or None). Stay under 300 words. Return only the plan."
)
BUILD_ASK = (
    "Write the Python code the user asks for. Use only the standard library. If a fact you need is "
    "missing from the request, do not guess: reply only with your questions for the user. "
    "Otherwise reply with one ```python code block and nothing else."
)
ANSWERS = "\n\n=== THE USER'S ANSWERS TO YOUR QUESTIONS ===\n{facts}"
SUITES = {"full": (HERE / "tasks", ARMS, MAX_REPROMPTS),
          "missing": (HERE / "tasks-missing", ("plain", "ask", "plan", "challenge"), 3)}


def asks(text, plan):
    """Did the model ask the user something? A plan asks under its questions heading; a chat reply
    asks when it holds a question and no code."""
    if not text:
        return False
    if not plan:
        return extract_code(text) is None and "?" in text
    part = re.split(r"^#+\s*Questions for the user\s*$", text, flags=re.M | re.I)
    return len(part) > 1 and "?" in re.split(r"^#", part[1], flags=re.M)[0]

# The model's code is saved as solution.py and imported, so a self-test block under
# `if __name__ == "__main__"` in it does not run and its own test functions cannot collide
# with the hidden ones. (The first live run pasted code and tests into one file; see outcome.md.)
# The hidden tests are fed to Python on stdin, so there is no test file for the answer to open,
# and a pass only counts with a random token that is set after the answer has been imported.
# ponytail: same process, so code that walks the caller's stack frames could still find the
# token; run the tests in a container if the builder is ever treated as hostile.
HEADER = '''
import os as _os, sys as _sys
_sys.path.insert(0, _os.getcwd())
from solution import {function}
'''
# Runs the hidden tests in name order and prints the first failing test's one-line symptom
# (its docstring), never the expected value.
FOOTER = '''
for _name, _test in sorted((k, v) for k, v in list(globals().items()) if k.startswith("test_")):
    try:
        _test()
    except BaseException:
        print("FAIL " + _test.__doc__)
        _sys.exit(1)
print("PASS TOKEN")
'''


def extract_code(reply):
    blocks = re.findall(r"```(?:python|py)?[ \t]*\n(.*?)```", reply, re.S)
    return blocks[-1] if blocks else None


def grade(task, code):
    """Return None when every hidden test passes, else a one-line symptom."""
    if code is None:
        return "there was no python code block in the reply"
    tests = (HERE / "tasks" / f"{task}_tests.py").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="outcome-") as cwd:
        function = (HERE / "tasks" / f"{task}.txt").read_text(encoding="utf-8").split("(")[0].split()[-1]
        (Path(cwd) / "solution.py").write_text(code, encoding="utf-8")
        token = secrets.token_hex(8)
        script = HEADER.format(function=function) + tests + FOOTER.replace("TOKEN", token)
        # The model's code gets no environment variables (no API keys); Windows needs SYSTEMROOT.
        env = {k: os.environ[k] for k in ("SYSTEMROOT",) if k in os.environ}
        try:  # -I: isolated mode, the model's code cannot pick up modules from the user's folders
            done = review.run_limited([sys.executable, "-I", "-B", "-"], input=script, cwd=cwd, env=env,
                                      timeout=TEST_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            return f"the code did not finish in {TEST_TIMEOUT_S} seconds"
    last = (done.stdout.strip().splitlines() or [""])[-1]
    if last == "PASS " + token:
        return None
    return last[5:] if last.startswith("FAIL ") else "the code crashed when it was loaded"


def call(steps, phase, provider, instruction, payload):
    """One model call. Logs it in steps and returns the reply, or None when the call failed."""
    started, answer, usage, extra, error = monotonic(), None, None, {}, None
    try:
        answer, usage, extra = review.review(provider, payload, instruction)
        if not answer.strip():
            raise review.ReviewError("empty reply")
    except (review.ReviewError, subprocess.TimeoutExpired) as problem:
        answer, error = None, str(problem)  # a failed call is logged and never rerun
    steps.append({"phase": phase, "provider": provider, "wall_ms": round(1000 * (monotonic() - started)),
                  "usage": usage, **extra, "error": error, "reply": answer})
    return answer


def one_run(arm, task, suite="full"):
    folder, _, max_reprompts = SUITES[suite]
    prompt = (folder / f"{task}.txt").read_text(encoding="utf-8").strip()
    facts = suite == "missing" and (folder / f"{task}_facts.txt").read_text(encoding="utf-8").strip()
    steps, note, payload, answered, built = [], None, prompt, False, None
    if arm == "better":
        payload = call(steps, "prepare", "claude", BETTER, prompt)
    elif arm == "ask":
        reply = call(steps, "ask", "claude", BUILD_ASK, prompt)
        if asks(reply, plan=False):
            answered = True
            payload = prompt + "\n\n=== YOUR QUESTIONS ===\n" + reply.strip() + ANSWERS.format(facts=facts)
        elif reply is None:
            payload = None
        else:
            built = reply  # it wrote code without asking: that reply is its first build
            steps[-1]["phase"] = "build"
    elif arm in ("plan", "challenge"):
        plan = call(steps, "prepare", "claude", PLAN_ASK if facts else PLAN, prompt)
        if plan and arm == "challenge":
            critique = call(steps, "review", "codex", review.RUBRIC.read_text(encoding="utf-8"), plan)
            try:
                critique = review.validate(critique or "")
                plan = call(steps, "revise", "claude", REVISE, plan + "\n\n=== REVIEW ===\n" + critique)
            except review.ReviewError as problem:
                note = f"NOT CHALLENGED ({problem}); built from the unrevised plan"
        payload = plan and prompt + "\n\n=== PLAN ===\n" + plan
        if facts and asks(plan, plan=True):
            answered, payload = True, payload + ANSWERS.format(facts=facts)
    solved_at, code, symptom = None, None, None
    for attempt in range(max_reprompts + 1) if payload else ():
        ask = payload if attempt == 0 else payload + RETRY.format(code=code or "(none)", symptom=symptom)
        if attempt == 0 and built:
            reply = built
        else:
            reply = call(steps, "reprompt" if attempt else "build", "claude", BUILD, ask)
        if reply is None:
            break
        code = extract_code(reply)
        symptom = grade(task, code)
        steps[-1]["symptom"] = symptom
        if symptom is None:
            solved_at = attempt  # 0 means the first build passed
            break
    return {"arm": arm, "task": task, "suite": suite, "asked_and_answered": answered,
            "solved_at": solved_at, "note": note, "steps": steps}


def run(arm, out, suite="full"):
    out.mkdir(parents=True, exist_ok=False)
    for repeat in (1, 2):
        for task in TASKS:
            result = one_run(arm, task, suite)
            (out / f"{task}-{repeat}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            print(f"{arm} {task}-{repeat}: solved_at={result['solved_at']}", flush=True)


def tokens(step):
    """Reported tokens of one call. Cached input is counted, as in the other benchmarks."""
    used = step["usage"]
    if not used:
        return 0
    if step["provider"] == "codex":
        return used["input_tokens"] + used["output_tokens"]
    return (used["input_tokens"] + used.get("cache_read_input_tokens", 0)
            + used.get("cache_creation_input_tokens", 0) + used["output_tokens"])


def summary(folder):
    runs = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(folder.glob("t*.json"))]
    solved = [r["solved_at"] for r in runs if r["solved_at"] is not None]
    by_phase = {}
    for r in runs:
        for step in r["steps"]:
            by_phase[step["phase"]] = by_phase.get(step["phase"], 0) + tokens(step)
    total = sum(by_phase.values())
    return {
        "runs": len(runs), "first_try_as_run": solved.count(0),
        # Regraded offline with the fixed grader from the saved first reply. No model call.
        "first_try_regraded": sum(
            grade(r["task"], extract_code(s["reply"])) is None
            for r in runs for s in r["steps"] if s["phase"] == "build" and s["reply"]), "solved": len(solved), "reprompts": sum(solved),
        "unsolved_reprompts": sum(sum(s["phase"] == "reprompt" for s in r["steps"]) for r in runs if r["solved_at"] is None),
        "failed_calls": sum(bool(s["error"]) for r in runs for s in r["steps"]),
        "not_challenged": sum(bool(r["note"]) for r in runs),
        "asked_and_answered": sum(bool(r.get("asked_and_answered")) for r in runs),
        "tokens_total": total, "tokens_by_phase": by_phase,
        "tokens_per_solved": round(total / len(solved)) if solved else None,
        "median_tokens": median(sum(tokens(s) for s in r["steps"]) for r in runs),
        "median_wall_s": round(median(sum(s["wall_ms"] for s in r["steps"]) for r in runs) / 1000, 1),
        "cost_usd_claude": round(sum(s.get("reported_cost_usd") or 0 for r in runs for s in r["steps"]), 2),
    }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("mode", choices=("run", "report"))
    cli.add_argument("--arm", choices=ARMS + ("ask",))
    cli.add_argument("--suite", choices=tuple(SUITES), default="full")
    cli.add_argument("--out", type=Path, help="run: new folder for this arm. report: folder that holds outcome-<arm>/")
    cli.add_argument("--dry-run", action="store_true")
    args = cli.parse_args()
    if args.mode == "report":
        prefix = "outcome-" if args.suite == "full" else "outcome-missing-"
        for arm in SUITES[args.suite][1]:
            print(arm, json.dumps(summary((args.out or ROOT / "runs") / f"{prefix}{arm}")))
    elif args.arm not in SUITES[args.suite][1]:
        cli.error(f"arm {args.arm} is not part of suite {args.suite}")
    elif args.dry_run:
        print(f"{2 * len(TASKS)} runs of arm {args.arm}, suite {args.suite}. No model calls made.")
    else:
        run(args.arm, args.out, args.suite)


if __name__ == "__main__":
    main()
