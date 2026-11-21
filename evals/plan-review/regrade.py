"""Second opinion on the AI grader. Samples 30 extra findings (not seeds) that the Claude grader
judged valid or unsupported, has Codex grade the same findings blind, and writes a sheet a person
can grade. Rules are in regrade.md. Run from the repository root."""

import argparse
import csv
import json
from pathlib import Path
import random
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / ".claude/skills/challenge"))
import review  # noqa: E402

# Frozen before the first call. Do not edit after it.
REGRADE = (
    "You grade one finding from a review of the plan below. Use only the plan text. Answer valid when "
    "the finding names a specific failure that follows from the plan text and its brief. Answer "
    "unsupported when it is wrong, contradicts the brief, or needs facts the plan does not give. "
    "Answer unclear when you cannot decide from the text. Reply with one line: the word valid, "
    "unsupported or unclear, then a colon and a one-sentence reason."
)
SEED, PER_REVIEWER = 20261120, 15
SCORE = ROOT / "runs/portfolio-score"
OUT = ROOT / "runs/regrade"
JUDGMENTS = ("valid", "unsupported", "unclear")


def finding(blind_id, issue):
    text = (SCORE / "blind" / f"{blind_id}.md").read_text(encoding="utf-8")
    part = re.split(rf"^### {issue}\.", text, flags=re.M)[1]
    return f"### {issue}." + re.split(r"^### \d+\.", part, flags=re.M)[0].rstrip()


def sample():
    """Pick the findings. The item order is shuffled so it does not reveal the reviewer."""
    mapping = json.loads((SCORE / "mapping.json").read_text(encoding="utf-8"))
    provider = {m["blind_id"]: m["provider"] for m in mapping if m.get("blind_id")}  # failed calls have no blind file
    rows = [json.loads(line) for line in (SCORE / "judgments.jsonl").read_text(encoding="utf-8").splitlines()]
    pick = random.Random(SEED)
    chosen = []
    for name in ("codex", "claude"):
        pool = [r for r in rows if r["judgment"] in ("valid", "unsupported") and provider[r["blind_id"]] == name]
        chosen += pick.sample(pool, PER_REVIEWER)
    pick.shuffle(chosen)
    return [{"item": n, "blind_id": r["blind_id"], "case": r["case"], "issue": r["issue"],
             "reviewer": provider[r["blind_id"]], "claude_grader": r["judgment"]} for n, r in enumerate(chosen, 1)]


def write_sheet(items):
    """Markdown for a person: the plan link and the finding only, no reviewer and no AI judgment."""
    lines = ["# Grade 30 review findings", "",
             "For each finding, open the plan and decide: **valid** (a specific failure that follows from the plan "
             "text and its brief), **unsupported** (wrong, contradicts the brief, or needs facts the plan does not "
             "give) or **unclear**. Do not look at `key.jsonl` or `codex.jsonl` until you are done. "
             "Write your answers in `human.csv`, one row per item.", ""]
    for it in items:
        lines += [f"## Item {it['item']:02d}: plan [{it['case']}](../../evals/plan-review/plans/{it['case']}.md)", "",
                  *("> " + line for line in finding(it["blind_id"], it["issue"]).splitlines()), "", "Judgment:", ""]
    (OUT / "sheet.md").write_text("\n".join(lines), encoding="utf-8")
    with (OUT / "human.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([("item", "judgment")] + [(it["item"], "") for it in items])


def regrade(items):
    with (OUT / "codex.jsonl").open("x", encoding="utf-8") as log:
        for it in items:
            plan = (HERE / "plans" / f"{it['case']}.md").read_text(encoding="utf-8-sig").strip()
            payload = f"=== PLAN ===\n{plan}\n\n=== FINDING ===\n{finding(it['blind_id'], it['issue'])}"
            try:
                answer, usage, _ = review.review("codex", payload, REGRADE)
                word = answer.strip().split(":")[0].strip().lower()
                row = {"item": it["item"], "judgment": word if word in JUDGMENTS else None, "reply": answer.strip()}
            except (review.ReviewError, subprocess.TimeoutExpired) as problem:
                row = {"item": it["item"], "judgment": None, "reply": None, "error": str(problem)}
            log.write(json.dumps(row) + "\n")
            log.flush()
            print(f"item {it['item']:02d}: {row['judgment']}", flush=True)


def agreement(items, other):
    """Agreement of another grader with the Claude grader, split by which model wrote the finding."""
    for name in ("codex", "claude"):
        mine = [it for it in items if it["reviewer"] == name and other.get(it["item"])]
        same = sum(other[it["item"]] == it["claude_grader"] for it in mine)
        print(f"  findings by {name}: {same}/{len(mine)} agree with the Claude grader")


def report():
    items = [json.loads(line) for line in (OUT / "key.jsonl").read_text(encoding="utf-8").splitlines()]
    codex = {r["item"]: r["judgment"] for r in map(json.loads, (OUT / "codex.jsonl").read_text(encoding="utf-8").splitlines())}
    print("Codex regrade:")
    agreement(items, codex)
    with (OUT / "human.csv").open(encoding="utf-8") as f:
        human = {int(r["item"]): r["judgment"].strip().lower() for r in csv.DictReader(f) if r["judgment"].strip()}
    print(f"Person: {len(human)} of {len(items)} graded")
    if human:
        agreement(items, human)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("mode", choices=("prepare", "codex", "report"))
    cli.add_argument("--dry-run", action="store_true")
    args = cli.parse_args()
    if args.mode == "prepare":
        items = sample()
        OUT.mkdir(parents=True, exist_ok=False)
        (OUT / "key.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items), encoding="utf-8")
        write_sheet(items)
        print(f"{len(items)} findings sampled")
    elif args.mode == "codex":
        items = [json.loads(line) for line in (OUT / "key.jsonl").read_text(encoding="utf-8").splitlines()]
        if args.dry_run:
            return print(f"{len(items)} planned calls. No model calls made.")
        regrade(items)
    else:
        report()


if __name__ == "__main__":
    main()
