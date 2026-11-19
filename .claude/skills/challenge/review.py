"""Run and validate one independent plan critique (Python 3.9+)."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


TIMEOUT = 180
RUBRIC = Path(__file__).with_name("critic-prompt.md")
VERDICTS = {
    "BLOCKED": "blocker",
    "PROCEED WITH CHANGES": "changes",
    "NO BLOCKING ISSUES": "clear",
}


class ReviewError(Exception):
    pass


def validate(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    verdict = lines[0].removeprefix("VERDICT: ") if lines and lines[0].startswith("VERDICT: ") else ""
    if verdict not in VERDICTS or len(text.split()) > 250 or len(text.encode("utf-8")) > 4096:
        raise ReviewError("invalid or oversized critique")
    body = lines[1:]
    if len(body) % 3 or len(body) > 15:
        raise ReviewError("invalid issue count or format")
    severities = []
    for index in range(0, len(body), 3):
        heading, failure, fix = body[index:index + 3]
        number = index // 3 + 1
        match = re.fullmatch(rf"### {number}\. \[(blocker|major|minor)\] \S.*", heading)
        if not match or not re.fullmatch(r"- Failure: \S.*", failure) or not re.fullmatch(r"- Fix: \S.*", fix):
            raise ReviewError(f"invalid format for issue {number}")
        severities.append(match[1])
    expected = "clear"
    if severities:
        expected = "blocker" if "blocker" in severities else "changes"
    if VERDICTS[verdict] != expected:
        raise ReviewError("verdict disagrees with issue severities")
    return text.strip() + "\n"


def parse_codex(stdout):
    answer = None
    usage = None
    for line in stdout.splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        kind = event["type"]
        if kind in {"turn.failed", "error"}:
            raise ReviewError("Codex reported a failed run")
        if kind == "item.completed":
            item = event["item"]
            if item["type"] == "agent_message":
                answer = item["text"]
            elif item["type"] != "reasoning":
                raise ReviewError("Codex used a tool or returned an unexpected item")
        if kind == "turn.completed":
            usage = event.get("usage")
    if not isinstance(answer, str) or usage is None:
        raise ReviewError("Codex returned no completed critique or usage")
    return answer, usage


def parse_claude(stdout):
    response = json.loads(stdout)
    if response["type"] != "result" or response["subtype"] != "success" or response["is_error"]:
        raise ReviewError("Claude reported a failed run")
    if response["num_turns"] != 1 or not isinstance(response.get("result"), str):
        raise ReviewError("Claude returned no single-turn critique")
    return response["result"], response.get("usage")


def review(provider, plan, rubric):
    executable = shutil.which(provider)
    if not executable:
        raise ReviewError(f"{provider} CLI not found on PATH")
    if provider == "codex":
        flags = [
            "exec", "--json", "--ephemeral", "--skip-git-repo-check", "--ignore-user-config",
            "--ignore-rules", "-s", "read-only", "-c", "approval_policy=\"never\"",
            "-c", "model_reasoning_effort=\"low\"", "-c", "features.shell_tool=false",
            "-c", "web_search=\"disabled\"", "-",
        ]
        parser = parse_codex
        stdin = rubric + "\n\n=== PLAN ===\n" + plan
    else:
        flags = [
            "-p", "--safe-mode", "--tools", "", "--strict-mcp-config", "--effort", "low",
            "--max-turns", "1", "--no-session-persistence", "--output-format", "json",
            "--system-prompt", rubric,
        ]
        parser = parse_claude
        stdin = "=== PLAN ===\n" + plan

    env = os.environ.copy()
    if provider == "claude":
        env.pop("CLAUDECODE", None)  # Start a fresh process even when the writer is Claude.
    with tempfile.TemporaryDirectory(prefix="plan-challenge-") as cwd:
        result = subprocess.run(
            [executable, *flags], input=stdin, capture_output=True, encoding="utf-8",
            errors="replace", cwd=cwd, env=env, timeout=TIMEOUT,
        )
    if result.returncode:
        details = (result.stdout + result.stderr).lower()
        if any(hint in details for hint in ("not logged in", "please run /login", "unauthorized", "401 unauthorized")):
            raise ReviewError(f"{provider} requires sign-in")
        raise ReviewError(f"{provider} exited with code {result.returncode}; check CLI setup and connectivity")
    try:
        answer, usage = parser(result.stdout)
    except (ValueError, TypeError, KeyError) as error:
        raise ReviewError(f"{provider} returned unexpected JSON") from error
    return validate(answer), usage


def save_review(provider, plan_path, output):
    usage_path = output.with_suffix(".usage.json")
    if output.exists() or usage_path.exists():
        raise ReviewError("output already exists; choose a new filename")
    if not output.parent.is_dir():
        raise ReviewError("output directory does not exist")
    if plan_path.stat().st_size > 4096:
        raise ReviewError("plan exceeds 4096 bytes")
    plan = plan_path.read_text(encoding="utf-8-sig").strip()
    if not plan or len(plan.split()) > 500:
        raise ReviewError("plan must have 1–500 words")
    critique, usage = review(provider, plan, RUBRIC.read_text(encoding="utf-8").strip())
    with usage_path.open("x", encoding="utf-8") as sidecar:
        json.dump({"provider": provider, "usage": usage}, sidecar, indent=2)
        sidecar.write("\n")
    try:
        with output.open("x", encoding="utf-8") as report:
            report.write(critique)
    except OSError:
        usage_path.unlink()
        raise


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("critic", choices=("codex", "claude"))
    cli.add_argument("plan", type=Path)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    try:
        save_review(args.critic, args.plan, args.output)
    except subprocess.TimeoutExpired:
        cli.exit(1, f"NOT CHALLENGED: {args.critic} timed out after {TIMEOUT}s\n")
    except (ReviewError, OSError, UnicodeError) as error:
        cli.exit(1, f"NOT CHALLENGED: {error}\n")
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
