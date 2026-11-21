# Changelog

Dates are when the work was committed. Each benchmark froze its rules in a commit before the first model call.

## Unreleased

- **Runner:** a timeout now also stops the CLI's child processes. On Windows the CLIs are `.cmd` shims, and a 2 s timeout used to return after 20 s because Node kept the output pipe open.
- **Outcome grader:** the model's code now runs with no environment variables, so it cannot read API keys.
- **Results:** exact 95% intervals for every pass count ([evals/intervals.py](evals/intervals.py)). 12 of 12 means at least 73.5%, not 100%.
- **Verified:** with the skill's flags, Codex's read-only sandbox refused a write on native Windows, both with shell on and with shell off ([runs/sandbox-check-windows](runs/sandbox-check-windows/)).
- **Stakes rule reworded** to catch indirect money risk (prices, stock, orders or pay set from the output). 16 of 16 with both models, including four held-out plans; rules frozen before the run.
- **Second grader:** Codex regraded 30 extra findings blind and agreed with the Claude grader on 16. Each favoured its own family's findings, so the claim that Claude writes more valid extra findings is now marked as grader-dependent. A blind sheet for a person is in [runs/regrade](runs/regrade/).
- **Plugin:** the repository is now also a Claude Code plugin and marketplace (`.claude-plugin/`), checked with `claude plugin validate`.
- **CI:** tests run on Linux, Windows and macOS with Python 3.9 and 3.13, plus both dry runs.

## 2026-11-20

- **Outcome test:** four ways to build six small functions, 12 runs each, judged by hidden tests. All 48 first builds passed. A grader bug that had failed 19 correct builds was fixed, and the saved replies were regraded. A second fix stops an answer from faking a pass.
- **Follow-up tests of the idea:** "make it better" against a review, a second read against a second model, and the stakes rule (10 of 12 for each model).

## 2026-11-19

- **Matched-pair benchmark:** 12 synthetic plans in six pairs, 48 reviewer calls, graded blind by an AI grader. Codex was faster and always returned a usable review. Claude wrote more extra findings that held up.
- **Codex at medium effort:** rerun to match Claude's effort. It took twice as long and found nothing more.
- **Skill:** risk-based routing (Codex by default, asks before using Claude on consequential plans), format check, `NOT CHALLENGED` on a failed review.
- **Pilot:** three of my real plans, 20 issues raised, all accepted. Seeded test with planted flaws.
- MIT license, README rewritten as a study, how-it-works visuals.
