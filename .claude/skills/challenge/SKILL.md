---
name: challenge
description: Draft or revise a project plan after a fresh Codex or Claude critique. Use for explicit plan challenges and independent plan stress tests.
---

Parse an optional leading `codex`, `claude`, or `measure` (default `codex`). Use the remaining idea, given plan file, or current discussion. Ask for the idea only if none is available. For consequential plans with no explicit critic, ask before switching to Claude. Remove secrets and private details before sharing a plan with a provider.

1. Create a new `challenge/<slug>/` in the active project. Add a numeric suffix on collision. Write `plan-v1.md` in at most 500 words and 4096 UTF-8 bytes with goal, constraints, non-goals, steps and success checks. Preserve that draft.
2. For `measure`, read [measure.md](measure.md) and follow it. Otherwise run the sibling script by absolute path: `python "<skill>/review.py" <critic> "<run>/plan-v1.md" "<run>/critique-<critic>.md"`. Use `py -3` or `python3` if needed. Allow a shell timeout of at least 200 seconds. The script sends the plan and rubric. On error, copy the draft to `plan.md`, record `NOT CHALLENGED (<reason>)` in `decisions.md`, report the error and stop.
3. In `decisions.md`, log each issue with round, critic, issue number, severity, accept/reject and one reason. Accept supported fixes within the brief. Write `plan.md` with accepted fixes. If no issues, copy the draft and log zero.
4. If round one raised a blocker, review `plan.md` once with the same critic and save `critique-<critic>-2.md`. Append decisions, apply accepted fixes and report any unresolved blocker or failed recheck. Keep the first-round result if the recheck fails.
5. Report the run folder, verdict and main changes in three short lines. Stop before implementation.
