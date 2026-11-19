# Decisions: Content Studio real-footage batch (`measure` mode, 2026-11-19)

Judged blind by the user: the 7 merged issues were shown shuffled, with no critic names. Unticked meant rejected. The user gave no written reasons, so there is no Reason column. Critic names were restored afterwards.

Two issues are counted as the same when they name the same plan step and the same failure. Claude did the merging and wrote the one-line summaries the user judged from. One critique entry can cover two merged issues, so the "Issues raised" counts below are entries in each critique file, not rows in this table.

| # | Issue | Codex run 1 | Codex run 2 | Claude run 1 | Claude run 2 | Decision |
|---|-------|:-:|:-:|:-:|:-:|----------|
| 1 | "Total time" in the decision rule is not defined (checking, fixing and retry time) | x (#1, major) | x (#1, blocker) | x (#2) | x (#4) | **Accept** |
| 2 | No rule to combine three clips into one decision | x (#3, minor) | x (#3, major) | x (#2) | x (#4) | **Accept** |
| 3 | The HDR fix changes the export after approval, without a new preview and approval | x (#2) | x (#2) | x (#3) | x (#3) | **Accept** |
| 4 | The tone-mapping filter is assumed to exist in the installed FFmpeg | | | x (#3) | x (#3) | **Accept** |
| 5 | Format problems only show after a full cut, so fixing them lands inside the timed clips | | | x (#1) | x (#2) | **Accept** |
| 6 | How the clip gets to the phone is not stated | | | x (#4, major) | x (#5, minor) | **Accept** |
| 7 | The wide-action clip may fail "ball visible" on every layout | | | | x (#1) | **Accept** |

Severity is major unless shown.

Notes:

- The two Codex runs raised the same 3 issues but gave different verdicts. Run 1 said `PROCEED WITH CHANGES`. Run 2 rated issue 1 a blocker and said `BLOCKED`. In the normal flow run 2 would have started a second round and run 1 would not. `measure` mode stops after round 1.
- On issue 1 the critics proposed opposite fixes. Codex: count all hands-on time in the total. Claude: log fix time separately and leave it out. The revised plan counts recurring checking time and leaves out one-off format fixing and unattended render time. That choice was made by Claude when revising and still needs the user's OK.

## Counts

| Run | Issues raised | Accepted | Tokens (measured, as reported by the tool) |
|---|---|---|---|
| Codex run 1 | 3 | 3 | not captured |
| Codex run 2 | 3 | 3 | not captured |
| Claude run 1 | 4 | 4 | 66,625 |
| Claude run 2 | 5 | 5 | 66,861 |

The two Codex token counts were lost: the command that ran Codex kept only the last four lines of its output, which cut off the token line. The runs were not saved by Codex, so the numbers cannot be recovered and are not estimated here.

- Noise: accepted issues found by only one of the two Codex runs: 0. By only one of the two Claude runs: 1 (issue 7, run 2 only).
- Difference: accepted issues found by Codex but neither Claude run: 0. By Claude but neither Codex run: 4 (issues 4, 5, 6 and 7).
- Raised by all four runs: 3 (issues 1, 2 and 3).
- 7 distinct issues raised, 7 accepted, 0 rejected.
