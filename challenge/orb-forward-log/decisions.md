# Decisions: ORB forward log (`measure` mode, 2026-11-19)

Judged blind by the user: the 7 merged issues were shown shuffled, with no critic names. Unticked meant rejected. The user gave no written reasons, so there is no Reason column. Critic names were restored afterwards.

Two issues are counted as the same when they name the same plan step and the same failure. Claude did the merging and wrote the one-line summaries the user judged from.

| # | Issue | Severity | Codex run 1 | Codex run 2 | Claude run 1 | Claude run 2 | Decision |
|---|-------|----------|:-:|:-:|:-:|:-:|----------|
| 1 | A half-written session (fewer than 12 rows) counts as logged and is never redone | major | x | x | x | x | Reject |
| 2 | Checked and hashed bars are not tied to what the paper trader reads | major | x | x | | | Reject |
| 3 | Correction rows have no rule for which row counts, so results can double-count | major | x | x | | | Reject |
| 4 | Bar check never tried on real vendor data | major | | | x | x | **Accept** |
| 5 | No rule for a session whose data never passes the check | major | | | x | x | Reject |
| 6 | A stale status file reads as healthy | major | | | x | x | Reject |
| 7 | Missed-start runs fire before the network is up | minor | | | x | x | **Accept** |

Note on issue 5: the user left it unticked but, asked which rule they would want, chose "stop and wait for me". It is counted as rejected and the plan is unchanged on this point. The two Claude runs also proposed opposite fixes for it (stop at the failed session / mark no-data and continue).

## Counts

| Run | Issues raised | Accepted | Tokens (measured, as reported by the tool) |
|---|---|---|---|
| Codex run 1 | 3 | 0 | 8,343 |
| Codex run 2 | 3 | 0 | 14,093 |
| Claude run 1 | 5 | 2 | 67,242 |
| Claude run 2 | 5 | 2 | 69,044 |

- Noise: accepted issues found by only one of the two Codex runs: 0. By only one of the two Claude runs: 0. Each critic raised the same issues in both runs.
- Difference: accepted issues found by Codex but neither Claude run: 0. By Claude but neither Codex run: 2 (issues 4 and 7).
- 7 distinct issues raised, 2 accepted, 5 rejected.
