"""Follow-up tests on the frozen plans: "make it better" baseline, revision after a saved critique,
and a stakes check. Rules are in followup.md. Calls go through the skill's own review.review(),
so they run in an empty temporary folder with tools off, like the reviewers."""

import argparse
import json
from pathlib import Path
import random
import subprocess
import sys
from time import monotonic

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/challenge"))
import review  # noqa: E402

# Frozen prompts. Do not edit after the first live call.
BETTER = "Make this plan better. Return only the improved plan."
REVISE = (
    "You wrote the plan below. An independent reviewer returned the review that follows it. "
    "Decide on each issue: accept it when the plan text supports it and the fix stays within the goal, "
    "constraints and non-goals. Otherwise reject it. Return only the revised plan with the accepted "
    "fixes applied. If you accept nothing, return the plan unchanged."
)
STAKES = (
    "Classify the plan below. Answer consequential when it involves material money, safety, a public "
    "release under the user's name or a hard-to-reverse change. Otherwise answer routine. "
    "Reply with that one word only."
)
STAKES_V2 = (  # Test 5: names indirect money risk, which STAKES missed on the forecast pair
    "Classify the plan below. Answer consequential when a mistake in the plan or in what it produces "
    "could cost material money, now or later (for example, when people set prices, stock, orders or pay "
    "from its output), affect safety, go out publicly under the user's name, or be hard to reverse. "
    "Otherwise answer routine. Reply with that one word only."
)
CASES = [f"p{n:02d}" for n in range(1, 13)]
HOLDOUT = [f"h{n:02d}" for n in range(1, 5)]  # written for Test 5, never seen by a model before it


def plan(case):
    folder = "holdout" if case.startswith("h") else "plans"
    return (HERE / folder / f"{case}.md").read_text(encoding="utf-8-sig").strip()


def jobs(mode, provider=None, critiques=None):
    """Return (output name, provider, instruction, payload) for every planned call."""
    if mode == "better":
        return [(f"{c}-better-{provider}-{r}", provider, BETTER, plan(c)) for r in (1, 2) for c in CASES]
    if mode == "stakes":
        return [(f"{c}-stakes-{p}", p, STAKES, plan(c)) for c in CASES for p in ("codex", "claude")]
    if mode == "stakes2":
        return [(f"{c}-stakes2-{p}", p, STAKES_V2, plan(c)) for c in CASES + HOLDOUT for p in ("codex", "claude")]
    found = []  # revise: one call per saved critique, the writer is always a fresh Claude
    for path in sorted(critiques.glob("p??-*-?.md")):
        case, reviewer, repeat = path.stem.split("-")
        payload = plan(case) + "\n\n=== REVIEW ===\n" + path.read_text(encoding="utf-8").strip()
        found.append((f"{case}-revise-{reviewer}-{repeat}", "claude", REVISE, payload))
    return found


def run(planned, out):
    out.mkdir(parents=True, exist_ok=False)
    with (out / "runs.jsonl").open("x", encoding="utf-8") as log:
        for name, provider, instruction, payload in planned:
            started, error = monotonic(), None
            try:
                answer, usage, extra = review.review(provider, payload, instruction)
                if not answer.strip():
                    raise review.ReviewError("empty reply")
                (out / f"{name}.md").write_text(answer.strip() + "\n", encoding="utf-8")
                meta = {"provider": provider, "requested_effort": review.DEFAULT_EFFORT[provider],
                        "wall_ms": round(1000 * (monotonic() - started)), "usage": usage, **extra}
                (out / f"{name}.usage.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
            except (review.ReviewError, subprocess.TimeoutExpired) as problem:
                error = str(problem)  # a failed call is logged and never rerun
            log.write(json.dumps({"name": name, "ok": error is None, "error": error}) + "\n")
            log.flush()
            print(f"{name}: {error or 'saved'}", flush=True)


def blind(folders, out):
    """Copy final plans under random names so the grader cannot see which arm wrote them."""
    files = [path for folder in folders for path in sorted(folder.glob("p??-*.md"))]
    random.shuffle(files)
    (out / "blind").mkdir(parents=True, exist_ok=False)
    mapping = []
    for number, path in enumerate(files, 1):
        blind_id = f"f{number:03d}"
        (out / "blind" / f"{blind_id}.md").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        mapping.append({"blind_id": blind_id, "case": path.stem[:3], "run_dir": path.parent.name, "file": path.name})
    index = "".join(json.dumps({"blind_id": m["blind_id"], "case": m["case"]}) + "\n" for m in mapping)
    (out / "blind" / "index.jsonl").write_text(index, encoding="utf-8")
    (out / "mapping.json").write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    print(f"{len(files)} final plans blinded")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("mode", choices=("better", "revise", "stakes", "stakes2", "blind"))
    cli.add_argument("folders", nargs="*", type=Path, help="revise: one folder of saved critiques. blind: run folders")
    cli.add_argument("--provider", choices=("codex", "claude"), help="better: which model rewrites the plan")
    cli.add_argument("--out", type=Path)
    cli.add_argument("--dry-run", action="store_true")
    args = cli.parse_args()
    if args.mode == "blind":
        return blind(args.folders, args.out)
    planned = jobs(args.mode, args.provider, args.folders[0] if args.folders else None)
    if args.dry_run:
        return print(f"{len(planned)} planned calls. No model calls made.")
    run(planned, args.out)


if __name__ == "__main__":
    main()
