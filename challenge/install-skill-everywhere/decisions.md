# Decisions: install the skill for every project (2026-11-19)

Critic: fresh Claude (the default). In this mode Claude decides, so each row has a reason a person can check.

## Round 1 — verdict: BLOCKED

| # | Critic | Severity | Issue | Decision | Reason |
|---|--------|----------|-------|----------|--------|
| 1 | claude | blocker | A "remember to copy" rule cannot meet "cannot silently differ" | **Accept** | Real: the plan's own first risk was this failure. A folder link (junction) leaves one set of files. |
| 2 | claude | major | The outside check can pass on the wrong files | **Accept** | Real: an existing install folder would make the copy nest. Added a `Test-Path` check before installing and a `VERDICT:` and link-target check after. |
| 3 | claude | major | Destination folder not named; later edits could land in the temporary folder | **Accept** | Real: a README edit made in the temporary folder would be lost. Path named (as a proposal) and later steps tied to a session opened there. |
| 4 | claude | minor | README change is never committed, and there is no `main` | **Accept** | Small and real: first commit on `main`, then a task branch, and "README change committed" is part of done. |

## Round 2 — verdict: PROCEED WITH CHANGES (no blocker left)

| # | Critic | Severity | Issue | Decision | Reason |
|---|--------|----------|-------|----------|--------|
| 5 | claude | major | The copy fallback is the same rule round 1 blocked | **Accept** | Real, and my own mistake: I kept the blocked rule as a fallback. If the link does not load, the plan now stops and the Goal counts as not met. |
| 6 | claude | major | Moving the only copy, not yet in git, out of a folder in use | **Accept** | Real: a move across drives is a copy then a delete, and nothing is in git yet. Changed to copy, check both skill files arrived, then `git init`. |
| 7 | claude | major | The outside check does not show which `critic-prompt.md` was read | **Accept** | The check is cheap, so it is added. The second half of the claim does not apply: **SKILL.md** already points to the prompt "in this skill's folder", not to a project path. |
| 8 | claude | minor | Work ends on an unmerged branch; the link serves the working tree | **Accept** | Real: `main` would keep the old install steps. Added a local merge after I review the diff (no push) and one README line on what "installed" means. |

Tokens (measured, each run's own reported total): round 1 64,296, round 2 65,816.

Counts: 8 issues raised, 8 accepted, 0 rejected.
