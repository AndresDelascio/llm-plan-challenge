# Decisions: Shot Tracker new-camera test (`measure` mode, 2026-11-19)

Judged blind by the user: the 6 merged issues were shown shuffled, with no critic names. Unticked meant rejected. The user gave no written reasons, so there is no Reason column. Critic names were restored afterwards.

Two issues are counted as the same when they name the same plan step and the same failure. Claude did the merging and wrote the one-line summaries the user judged from.

Both Codex runs replied `VERDICT: NO BLOCKING ISSUES` and raised nothing.

| # | Issue | Severity | Codex run 1 | Codex run 2 | Claude run 1 | Claude run 2 | Decision |
|---|-------|----------|:-:|:-:|:-:|:-:|----------|
| 1 | Pass line does not say which run it judges (engine off or on) or what the percentages are out of | major | | | x (#1) | x (#2, #5) | **Accept** |
| 2 | No rule on ball-click retries, reruns or dropped shots | major | | | x (#2) | x (#1) | **Accept** |
| 3 | Outcome mix (goals, misses, woodwork) has no minimum counts | major | | | x (#3) | x (#3) | **Accept** |
| 4 | No "inconclusive" result: 60 shots cannot separate pass from fail near the line | major | | | x (#4) | | **Accept** |
| 5 | Location not pinned to the benchmark goal, so a fail could not be blamed on camera position | minor | | | x (#5) | | **Accept** |
| 6 | All sessions share one tripod setup, so one bad or lucky setup decides the result | major | | | | x (#4) | **Accept** |

Claude run 2 spent two of its five entries (#2 and #5) on merged issue 1, so it covers 4 distinct issues.

## Counts

| Run | Issues raised | Accepted | Tokens (measured, as reported by the tool) |
|---|---|---|---|
| Codex run 1 | 0 | 0 | 5,995 |
| Codex run 2 | 0 | 0 | 11,019 |
| Claude run 1 | 5 | 5 | 68,754 |
| Claude run 2 | 5 | 5 | 69,335 |

- Noise: accepted issues found by only one of the two Codex runs: 0. By only one of the two Claude runs: 3 (issues 4 and 5 by run 1 only, issue 6 by run 2 only).
- Difference: accepted issues found by Codex but neither Claude run: 0. By Claude but neither Codex run: 6 (all of them).
- 6 distinct issues raised, 6 accepted, 0 rejected.
