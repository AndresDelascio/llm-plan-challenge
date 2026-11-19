"""Blind completed critiques for grading, then report the measures in scoring.md."""

import argparse
import json
from pathlib import Path
import random
from statistics import median
import sys


HERE = Path(__file__).resolve().parent
NOVEL = ("valid", "unsupported", "unclear")


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def blind(run_dirs, out):
    """Copy critiques under random names so the grader cannot see who wrote them."""
    attempts = []
    for folder in run_dirs:
        for row in rows(folder / "runs.jsonl"):
            usage = json.loads((folder / row["critique"]).with_suffix(".usage.json").read_text(encoding="utf-8")) if row["ok"] else None
            attempts.append({**row, "run_dir": folder.name, "usage": usage})
    (out / "blind").mkdir(parents=True)
    done = [row for row in attempts if row["ok"]]
    random.shuffle(done)
    for number, row in enumerate(done, 1):
        row["blind_id"] = f"c{number:02d}"
        text = (next(d for d in run_dirs if d.name == row["run_dir"]) / row["critique"]).read_text(encoding="utf-8")
        (out / "blind" / f"{row['blind_id']}.md").write_text(text, encoding="utf-8")
    index = sorted(({"blind_id": row["blind_id"], "case": row["case"]} for row in done), key=lambda r: r["blind_id"])
    (out / "blind" / "index.jsonl").write_text("".join(json.dumps(r) + "\n" for r in index), encoding="utf-8")
    (out / "mapping.json").write_text(json.dumps(attempts, indent=2) + "\n", encoding="utf-8")
    print(f"{len(done)} critiques blinded, {len(attempts) - len(done)} failed attempts recorded")


def tokens(usage):
    """Convert each CLI's usage fields to new input, cache read, cache write, output."""
    u = usage["usage"]
    if usage["provider"] == "codex":  # Codex counts cached tokens inside input_tokens
        read, write = u.get("cached_input_tokens", 0), u.get("cache_write_input_tokens", 0)
        return u["input_tokens"] - read - write, read, write, u["output_tokens"]
    return u["input_tokens"], u.get("cache_read_input_tokens", 0), u.get("cache_creation_input_tokens", 0), u["output_tokens"]


def frac(hit, total):
    return f"{hit}/{total}" + (f" ({100 * hit / total:.0f}%)" if total else "")


def summarize(attempts, judgments, key, stakes):
    """Return per-reviewer measures and the routing replay as plain dicts."""
    seeds = {row["id"]: row["seeds"] for row in key}
    level = {row["id"]: stakes[row["pair"]] for row in key}
    by_blind = {}
    for j in judgments:
        by_blind.setdefault(j["blind_id"], []).append(j)
    found, reviewers = {}, {}
    for a in attempts:
        mine = by_blind.get(a.get("blind_id"), [])
        found[(a["provider"], a["case"], a["repeat"])] = {s for j in mine for s in j["matched_seeds"]} if a["ok"] else None
        r = reviewers.setdefault(a["provider"], {
            "attempted": 0, "completed": 0, "blockers": [0, 0, 0], "seeds": [0, 0, 0], "controls": [0, 0],
            "novel": dict.fromkeys(NOVEL, 0), "tokens": [], "wall_ms": [], "cost_usd": [], "models": set(),
        })
        r["attempted"] += 1
        for seed in seeds[a["case"]]:  # [detected, opportunities in completed runs, opportunities in all attempts]
            for name in ("seeds",) + (("blockers",) if seed["severity"] == "blocker" else ()):
                r[name][2] += 1
                r[name][1] += a["ok"]
                r[name][0] += a["ok"] and seed["id"] in found[(a["provider"], a["case"], a["repeat"])]
        if not a["ok"]:
            continue
        r["completed"] += 1
        if not seeds[a["case"]]:
            r["controls"][1] += 1
            r["controls"][0] += any(j["judgment"] == "repaired-claim" for j in mine)
        for j in mine:
            if j["judgment"] in NOVEL:
                r["novel"][j["judgment"]] += 1
        r["tokens"].append(tokens(a["usage"]))
        r["wall_ms"].append(a["usage"]["wall_ms"])
        r["models"].update(a["usage"].get("resolved_models") or [a["usage"]["requested_model"] or "CLI default (not reported)"])
        if a["usage"].get("reported_cost_usd") is not None:
            r["cost_usd"].append(a["usage"]["reported_cost_usd"])

    usage = {(a["provider"], a["case"], a["repeat"]): a["usage"] for a in attempts}
    slots = sorted({(case, repeat) for _, case, repeat in found})
    choose = {
        "always codex": lambda case: ("codex",),
        "always claude": lambda case: ("claude",),
        "both": lambda case: ("codex", "claude"),
        "routing rule": lambda case: ("claude",) if level[case] == "consequential" else ("codex",),
    }
    policies = {}
    for name, pick in choose.items():
        p = {"calls": 0, "failed": 0, "blockers": [0, 0], "seeds": [0, 0], "consequential_blocker_misses": 0, "tokens": 0, "wall_ms": 0}
        for case, repeat in slots:
            calls = [(provider, case, repeat) for provider in pick(case)]
            if any(call not in found for call in calls):
                p = None  # a reviewer has no attempt for this slot, so the policy cannot be replayed
                break
            hits = set().union(*(found[call] or set() for call in calls))
            p["calls"] += len(calls)
            p["failed"] += sum(found[call] is None for call in calls)
            for call in calls:
                if usage[call]:
                    p["tokens"] += sum(tokens(usage[call]))
                    p["wall_ms"] += usage[call]["wall_ms"]
            for seed in seeds[case]:
                p["seeds"][1] += 1
                p["seeds"][0] += seed["id"] in hits
                if seed["severity"] == "blocker":
                    p["blockers"][1] += 1
                    p["blockers"][0] += seed["id"] in hits
                    p["consequential_blocker_misses"] += level[case] == "consequential" and seed["id"] not in hits
        policies[name] = p
    return reviewers, policies


def report(folder):
    attempts = json.loads((folder / "mapping.json").read_text(encoding="utf-8"))
    key = rows(HERE / "answer-key.jsonl")
    stakes = {row["pair"]: row["stakes"] for row in rows(HERE / "stakes.jsonl")}
    reviewers, policies = summarize(attempts, rows(folder / "judgments.jsonl"), key, stakes)
    names = sorted(reviewers)
    print("| Measure | " + " | ".join(names) + " |\n| --- |" + " ---: |" * len(names))

    def line(label, cell):
        print(f"| {label} | " + " | ".join(cell(reviewers[name]) for name in names) + " |")

    def mid(index):
        return lambda r: f"{median(t[index] for t in r['tokens']):,.0f}" if r["tokens"] else "n/a"

    line("Model", lambda r: ", ".join(sorted(r["models"])) or "n/a")
    line("Completed / attempted runs", lambda r: frac(r["completed"], r["attempted"]))
    line("Seeded blockers found (completed runs)", lambda r: frac(r["blockers"][0], r["blockers"][1]))
    line("Seeded blockers found (failed runs count as zero)", lambda r: frac(r["blockers"][0], r["blockers"][2]))
    line("All seeded flaws found (completed runs)", lambda r: frac(r["seeds"][0], r["seeds"][1]))
    line("All seeded flaws found (failed runs count as zero)", lambda r: frac(r["seeds"][0], r["seeds"][2]))
    line("Control runs repeating a repaired flaw", lambda r: frac(*r["controls"]))
    line("Other findings: valid / unsupported / unclear", lambda r: " / ".join(str(r["novel"][n]) for n in NOVEL))
    for index, label in enumerate(("new input", "cache read", "cache write", "output")):
        line(f"Median {label} tokens per run", mid(index))
    line("Median total tokens per run", lambda r: f"{median(map(sum, r['tokens'])):,.0f}" if r["tokens"] else "n/a")
    line("Median wall time per run (s)", lambda r: f"{median(r['wall_ms']) / 1000:.1f}" if r["wall_ms"] else "n/a")
    line("Reported cost, all runs (USD)", lambda r: f"{sum(r['cost_usd']):.2f} over {len(r['cost_usd'])} runs" if r["cost_usd"] else "not reported by CLI")

    print("\n| Policy | Calls (failed) | Blockers found | All seeds found | Blocker misses on consequential plans | Total tokens | Total wall time (s) |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, p in policies.items():
        if p is None:
            print(f"| {name} | not replayable: a reviewer has no runs | | | | | |")
        else:
            print(f"| {name} | {p['calls']} ({p['failed']}) | {frac(*p['blockers'])} | {frac(*p['seeds'])} | "
                  f"{p['consequential_blocker_misses']} | {p['tokens']:,} | {p['wall_ms'] / 1000:.0f} |")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest="command", required=True)
    b = commands.add_parser("blind")
    b.add_argument("run_dirs", nargs="+", type=Path)
    b.add_argument("--out", type=Path, required=True)
    commands.add_parser("report").add_argument("folder", type=Path)
    args = cli.parse_args()
    if args.command == "blind":
        blind(args.run_dirs, args.out)
    else:
        report(args.folder)


if __name__ == "__main__":
    sys.exit(main())
