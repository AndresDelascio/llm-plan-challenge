"""Collect reproducible critic runs in a fresh output directory."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1] / ".claude/skills/challenge"


def collect_jobs(suite, key):
    selected = [row["id"] for row in key if suite == "full" or row["split"] == "smoke"]
    repeats = 2 if suite == "full" else 1
    return [
        (case, provider, repeat)
        for repeat in range(1, repeats + 1)
        for case in sorted(selected)
        for provider in ("codex", "claude")
    ]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def version(provider):
    executable = shutil.which(provider)
    if not executable:
        raise ValueError(f"{provider} CLI not found on PATH")
    result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=15)
    if result.returncode:
        raise ValueError(f"{provider} CLI version check failed")
    return result.stdout.strip()


def collect(args, jobs):
    models = {"codex": args.codex_model, "claude": args.claude_model}
    paths = {case: HERE / "plans" / f"{case}.md" for case, _, _ in jobs}
    manifest = {
        "suite": args.suite,
        "planned_calls": len(jobs),
        "models_requested": models,
        "effort": args.effort or "runner defaults",
        "cli_versions": {provider: version(provider) for provider in models},
        "runner_sha256": digest(SKILL / "review.py"),
        "rubric_sha256": digest(SKILL / "critic-prompt.md"),
        "answer_key_sha256": digest(HERE / "answer-key.jsonl"),
        "plan_sha256": {case: digest(path) for case, path in paths.items()},
    }
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    failed = 0
    with (args.out / "runs.jsonl").open("x", encoding="utf-8") as log:
        for case, provider, repeat in jobs:
            output = args.out / f"{case}-{provider}-{repeat}.md"
            command = [sys.executable, str(SKILL / "review.py"), provider, str(paths[case]), str(output)]
            if models[provider]:
                command += ["--model", models[provider]]
            if args.effort:
                command += ["--effort", args.effort]
            result = subprocess.run(command, capture_output=True, encoding="utf-8", errors="replace")
            error = result.stderr.strip() if result.returncode else None
            log.write(json.dumps({
                "case": case, "provider": provider, "repeat": repeat, "ok": error is None,
                "critique": output.name if error is None else None, "error": error,
            }) + "\n")
            log.flush()
            if error is not None:
                failed += 1
                print(f"{output.stem}: {error}", file=sys.stderr, flush=True)
                if any(hint in error for hint in ("requires sign-in", "check CLI setup and connectivity", "CLI not found")):
                    break
            else:
                print(f"{output.stem}: saved", flush=True)
    return 1 if failed else 0


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--suite", choices=("smoke", "full"), default="smoke")
    cli.add_argument("--out", type=Path)
    cli.add_argument("--codex-model")
    cli.add_argument("--claude-model")
    cli.add_argument("--effort", choices=("low", "medium", "high"), help="Override both reviewers for a matched-effort comparison")
    cli.add_argument("--dry-run", action="store_true")
    args = cli.parse_args()
    key = [json.loads(line) for line in (HERE / "answer-key.jsonl").read_text(encoding="utf-8").splitlines()]
    jobs = collect_jobs(args.suite, key)
    if args.dry_run:
        print(f"{len(jobs)} planned calls. No reviewer calls made.")
        return 0
    if args.out is None:
        cli.error("--out is required for a live run")
    try:
        return collect(args, jobs)
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        cli.exit(1, f"{error}\n")


if __name__ == "__main__":
    sys.exit(main())
