# Saved runs

Every model reply behind the numbers in [docs/portfolio-results.md](../docs/portfolio-results.md). Nothing here was edited after the run. A failed call is kept as `*.rejected.txt` or recorded in `manifest.json`, never rerun.

| Folder | What it holds |
| --- | --- |
| `portfolio-smoke-codex/`, `portfolio-smoke-claude/` | Smoke run on a few plans before the full run |
| `portfolio-full-codex/`, `portfolio-full-claude/` | Main benchmark: 12 plans × 2 reads per reviewer, with usage files |
| `portfolio-score/`, `portfolio-score-codex/` | Blind grading: copies under random names (`blind/`), the name key (`mapping.json`), one row per finding (`judgments.jsonl`) |
| `matched-full-codex/`, `matched-score-codex/` | Codex rerun at medium effort, and its grading |
| `followup-better-*/`, `followup-revise-*/` | "Make it better" against review then revise |
| `followup-claude-validator/` | Claude rerun with the current format check |
| `followup-stakes/` | Stakes rule: each model labels each plan routine or consequential |
| `followup-score/` | Grading for the follow-up tests |
| `outcome-plain/`, `outcome-better/`, `outcome-plan/`, `outcome-challenge/` | Outcome test: one JSON per run with every prompt, reply, token count and test result |
| `outcome-missing-plain/`, `-ask/`, `-plan/`, `-challenge/` | Missing-fact outcome test: same layout as the outcome test, plus whether the run asked and got the facts |
| `regrade/` | Second grader: the 30 sampled findings (`key.jsonl`), Codex's judgments (`codex.jsonl`), and a blind sheet for a person (`sheet.md`, `human.csv`) |
| `sandbox-check-windows/` | Does Codex's read-only sandbox refuse a write on Windows? |

Each `*.usage.json` holds the CLI's reported tokens, time and (for Claude) cost. Tokens are reported by the CLI, not counted by me.
