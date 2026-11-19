| Measure | claude | codex |
| --- | ---: | ---: |
| Model | claude-fable-5-2 | CLI default (not reported) |
| Completed / attempted runs | 21/24 (88%) | 24/24 (100%) |
| Seeded blockers found (completed runs) | 18/18 (100%) | 18/18 (100%) |
| Seeded blockers found (failed runs count as zero) | 18/18 (100%) | 18/18 (100%) |
| All seeded flaws found (completed runs) | 24/24 (100%) | 24/24 (100%) |
| All seeded flaws found (failed runs count as zero) | 24/24 (100%) | 24/24 (100%) |
| Control runs repeating a repaired flaw | 0/9 (0%) | 2/12 (17%) |
| Other findings: valid / unsupported / unclear | 37 / 19 / 0 | 17 / 12 / 0 |
| Median new input tokens per run | 2 | 2,810 |
| Median cache read tokens per run | 755 | 10,368 |
| Median cache write tokens per run | 581 | 0 |
| Median output tokens per run | 1,090 | 177 |
| Median total tokens per run | 2,417 | 14,184 |
| Median wall time per run (s) | 17.9 | 7.1 |
| Reported cost, all runs (USD) | 1.21 over 21 runs | not reported by CLI |

| Policy | Calls (failed) | Blockers found | All seeds found | Blocker misses on consequential plans | Total tokens | Total wall time (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| always codex | 24 (0) | 18/18 (100%) | 24/24 (100%) | 0 | 335,826 | 181 |
| always claude | 24 (3) | 18/18 (100%) | 24/24 (100%) | 0 | 52,122 | 404 |
| both | 48 (3) | 18/18 (100%) | 24/24 (100%) | 0 | 387,948 | 585 |
| routing rule | 24 (1) | 18/18 (100%) | 24/24 (100%) | 0 | 242,855 | 266 |
