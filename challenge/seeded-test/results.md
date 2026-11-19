# Seeded-flaw test: results (2026-11-19)

Three made-up plans, each with 4 flaws planted on purpose (2 serious, 2 small), 12 in total. Each critic read each plan twice, so 6 runs per critic. Scoring follows **answer-key.md**, which was committed (`0f651db`) before any critic ran.

## Result

Both critics found all 12 planted flaws in every run. The test shows no difference in detection, only in cost.

| | Codex (ChatGPT) | Claude |
|---|---|---|
| Planted flaws found, per run | 4 of 4 in all 6 runs | 4 of 4 in all 6 runs |
| Serious flaws found | 12 of 12 | 12 of 12 |
| Small flaws found | 12 of 12 | 12 of 12 |
| Tokens per run (measured) | 4,162 to 13,038 | 62,316 to 63,235 |
| Tokens, 6 runs (computed sum) | 49,494 | 375,846 |
| Tokens per run (computed mean) | 8,249 | 62,641 |
| Tokens per planted flaw found (computed, sum / 24) | 2,062 | 15,660 |
| Issues raised that were not planted | 1 | 6 |

Claude used 7.6 times the tokens of Codex for the same planted flaws (computed, 375,846 / 49,494).

## Tokens per run (measured)

| Plan | Codex run 1 | Codex run 2 | Claude run 1 | Claude run 2 |
|---|---|---|---|---|
| A, moisture logger | 6,962 | 6,934 | 62,895 | 63,235 |
| B, bank summary | 11,131 | 13,038 | 62,316 | 62,413 |
| C, sign-up page | 7,267 | 4,162 | 62,487 | 62,500 |

Codex numbers are the `tokens used` line each run printed. Claude numbers are the total each subagent reported, which includes the Claude Code context every subagent starts with.

## Where each planted flaw was found

The number is the issue number in that run's critique file. "in 2" means the flaw was stated inside issue 2 rather than as its own issue, which the key counts as found.

| Flaw | Size | Codex run 1 | Codex run 2 | Claude run 1 | Claude run 2 |
|---|---|---|---|---|---|
| A1 Wi-Fi always on empties the battery in about 32 h | serious | 1 | 1 | 1 | 1 |
| A2 readings only in memory | serious | 4 | 4 | 2 | 2 |
| A3 wrong reading count (8,640, not 2,160) | small | 2 | 2 | in 2 | in 5 |
| A4 parts cost C$112, budget C$80 | small | 3 | 3 | 3 | 4 |
| B1 one date format for both banks | serious | 2 | 2 | 1 | 1 |
| B2 script deletes the export files | serious | 4 | 3 | 3 | 3 |
| B3 24 files needed, 12 required | small | 1 | 1 | 2 | 2 |
| B4 summary written into the input folder | small | 5 | 4 | 4 | 4 |
| C1 16-team cap only in the page | serious | 1 | 1 | 1 | 1 |
| C2 captain contacts on a page with no login | serious | 3 | 2 | 4 | 4 |
| C3 schedule built before registration closes | small | 4 | 4 | 2 | 2 |
| C4 duplicate registrations use up places | small | 2 | 3 | 5 | 5 |

## Issues raised that were not planted

These are listed, not scored. Nobody judged whether they are worth accepting, so they are not evidence of quality either way.

| Plan | Issue | Raised by |
|---|---|---|
| A | Standby current of the board, boost converter and sensors | Claude run 1 (4), Claude run 2 (3) |
| A | ADC2 pins give bad readings while Wi-Fi is on | Claude run 1 (5), Claude run 2 (in 3) |
| A | Bench test runs on USB, so battery life is never tested | Claude run 2 (in 5) |
| B | Transfers between the two accounts counted as spending | Codex run 1 (3), Codex run 2 (5), Claude run 2 (5) |
| B | Refunds dropped, so spending is overstated | Claude run 1 (5) |
| C | SQLite on a free hosting tier can be wiped | Claude run 1 (3), Claude run 2 (3) |

Claude used all 5 issue slots in every run. Codex stopped at 4 issues on plans A and C.

## What this does and does not show

1. For flaws of this kind (a contradiction or bad number that can be found by reading the plan carefully), Codex catches as many as Claude at about an eighth of the tokens.
2. It does not show the two critics are equal. Every flaw was found by every run, so the test hit its ceiling and cannot separate them. Harder flaws would be needed for that.
3. The one visible difference is the unplanted issues: Claude raised 6, Codex 1. That matches the earlier comparison on real plans, where Claude raised 18 of the 20 accepted issues and Codex 6.

## Limits

- Claude wrote the plans, planted the flaws, wrote the key and did the scoring. The key was committed before the runs, but the flaws may be the kind Claude finds easy to see.
- The plans are short and made up. Real plans have flaws nobody planted.
- Two runs per critic per plan is a small sample.
- The six Claude critiques were saved by hand from the subagents' replies, unchanged.
