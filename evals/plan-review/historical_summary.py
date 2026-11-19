"""Recompute descriptive pilot metrics from the archived decision tables."""

from collections import Counter
import json
from pathlib import Path
from statistics import mean, median


ARCHIVE = Path(__file__).resolve().parents[2] / "challenge"
TRIALS = ("orb-forward-log", "shot-tracker-new-camera", "content-studio-real-batch")


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def accepted_findings(path):
    text = path.read_text(encoding="utf-8")
    rows = [cells(line) for line in text.split("## Counts", 1)[0].splitlines() if line.startswith("|")]
    header = rows[0]
    counts = Counter()
    for row in rows[1:]:
        if not row[0].isdigit() or not row[header.index("Decision")].startswith("**Accept**"):
            continue
        counts["accepted_union"] += 1
        codex = sum(row[header.index(f"Codex run {run}")].startswith("x") for run in (1, 2))
        claude = sum(row[header.index(f"Claude run {run}")].startswith("x") for run in (1, 2))
        for reviewer, occurrences in (("codex", codex), ("claude", claude)):
            counts[reviewer] += bool(occurrences)
            counts[f"{reviewer}_both_repeats"] += occurrences == 2
        overlap = "shared" if codex and claude else "codex_only" if codex else "claude_only"
        counts[overlap] += 1
    return counts


def seeded_tokens(path):
    totals = {"codex": [], "claude": []}
    table = path.read_text(encoding="utf-8").split("## Tokens per run (measured)", 1)[1].split("##", 1)[0]
    for line in table.splitlines():
        if line.startswith(("| A,", "| B,", "| C,")):
            tokens = [int(value.replace(",", "")) for value in cells(line)[1:]]
            totals["codex"].extend(tokens[:2])
            totals["claude"].extend(tokens[2:])
    return {
        reviewer: {"n": len(counts), "total": sum(counts), "mean": mean(counts), "median": median(counts)}
        for reviewer, counts in totals.items()
    }


def summarize():
    real = sum((accepted_findings(ARCHIVE / trial / "decisions.md") for trial in TRIALS), Counter())
    tokens = seeded_tokens(ARCHIVE / "seeded-test/results.md")
    codex, claude = (tokens[name]["mean"] for name in ("codex", "claude"))
    scenarios = []
    for share in (0.05, 0.10, 0.20):
        for mode, consequential_cost in (("claude", claude), ("both", codex + claude)):
            average = (1 - share) * codex + share * consequential_cost
            scenarios.append({
                "consequential_share": share,
                "escalation": mode,
                "mean_reported_tokens": round(average),
                "reduction_vs_all_claude_pct": round(100 * (1 - average / claude), 1),
            })
    return {
        "historical_accepted_findings": dict(real),
        "historical_seeded_tokens": tokens,
        "historical_seeded_token_ratio_claude_to_codex": round(claude / codex, 2),
        "illustrative_routing_scenarios": scenarios,
    }


if __name__ == "__main__":
    print(json.dumps(summarize(), indent=2))
