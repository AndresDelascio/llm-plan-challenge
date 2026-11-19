# Decisions: ORB forward log (`measure` mode, 2026-11-19)

First judged blind by the user: the 7 merged issues were shown shuffled, with no critic names, and 2 were ticked. Critic names were restored afterwards.

**Corrected 2026-11-19:** the user had read the question as "pick one" and meant to accept all 7. Issues 1, 2, 3, 5 and 6 were changed from Reject to Accept. This correction was made after the critic names had been shown, so this plan no longer counts as blind-judged. The user gave no written reasons, so there is no Reason column.

Two issues are counted as the same when they name the same plan step and the same failure. Claude did the merging and wrote the one-line summaries the user judged from.

| # | Issue | Severity | Codex run 1 | Codex run 2 | Claude run 1 | Claude run 2 | Decision |
|---|-------|----------|:-:|:-:|:-:|:-:|----------|
| 1 | A half-written session (fewer than 12 rows) counts as logged and is never redone | major | x | x | x | x | **Accept** (corrected) |
| 2 | Checked and hashed bars are not tied to what the paper trader reads | major | x | x | | | **Accept** (corrected) |
| 3 | Correction rows have no rule for which row counts, so results can double-count | major | x | x | | | **Accept** (corrected) |
| 4 | Bar check never tried on real vendor data | major | | | x | x | **Accept** |
| 5 | No rule for a session whose data never passes the check | major | | | x | x | **Accept** (corrected) |
| 6 | A stale status file reads as healthy | major | | | x | x | **Accept** (corrected) |
| 7 | Missed-start runs fire before the network is up | minor | | | x | x | **Accept** |

Note on issue 5: the two Claude runs proposed opposite fixes (stop at the failed session / mark no-data and continue). Asked which rule they wanted, the user chose "stop and wait for me", and the plan uses that.

## Counts

| Run | Issues raised | Accepted | Tokens (measured, as reported by the tool) |
|---|---|---|---|
| Codex run 1 | 3 | 3 | 8,343 |
| Codex run 2 | 3 | 3 | 14,093 |
| Claude run 1 | 5 | 5 | 67,242 |
| Claude run 2 | 5 | 5 | 69,044 |

- Noise: accepted issues found by only one of the two Codex runs: 0. By only one of the two Claude runs: 0. Each critic raised the same issues in both runs.
- Difference: accepted issues found by Codex but neither Claude run: 2 (issues 2 and 3). By Claude but neither Codex run: 4 (issues 4, 5, 6 and 7).
- Raised by all four runs: 1 (issue 1).
- 7 distinct issues raised, 7 accepted, 0 rejected (first judgement: 2 accepted, 5 rejected).
