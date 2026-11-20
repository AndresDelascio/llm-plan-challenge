# Paired benchmark results (2026-11-19)

Live runs of both reviewers on the [12-plan paired benchmark](../evals/plan-review/). The plans, answer key, [scoring rules](../evals/plan-review/scoring.md) and [stakes labels](../evals/plan-review/stakes.jsonl) were frozen in commit `5aaacac` before the first call. All numbers below are measured from the saved usage files or counted from the grader's rows, unless marked otherwise.

## What was run

| Run | Calls | Completed | Evidence |
| --- | ---: | ---: | --- |
| Codex smoke (6 plans, once) | 6 | 6 | [runs/portfolio-smoke-codex](../runs/portfolio-smoke-codex/) |
| Codex full (12 plans, twice) | 24 | 24 | [runs/portfolio-full-codex](../runs/portfolio-full-codex/) |
| Claude smoke (6 plans, once) | 6 | 2 | [runs/portfolio-smoke-claude](../runs/portfolio-smoke-claude/) |
| Claude full (12 plans, twice) | 24 | 21 | [runs/portfolio-full-claude](../runs/portfolio-full-claude/) |
| **Total** | **60** | **53** | |

- Codex CLI 0.170.0, low effort. The CLI did not report which model it used.
- Claude CLI 2.1.319, medium effort, model `claude-fable-5-2` as reported by the CLI.
- Each reviewer got the plan and the rubric only, in an empty temporary folder with tools off.
- No failed call was rerun. One extra Claude call outside the 60 was made to diagnose the smoke failures. It is not scored.

Only the two full runs are scored. The smoke runs were for finding integration problems, and found one (below).

## Reviewer comparison (full runs)

| Measure | Codex | Claude |
| --- | ---: | ---: |
| Completed / attempted runs | 24/24 | 21/24 |
| Seeded blockers found | 18/18 | 18/18 |
| All seeded flaws found | 24/24 | 24/24 |
| Same, counting failed runs as finding nothing | 24/24 | 24/24 |
| Control runs that repeated a repaired flaw | 2/12 | 0/9 |
| Other findings judged valid | 17 | 37 |
| Other findings judged unsupported | 12 | 19 |
| Median total tokens per run | 14,184 | 2,417 |
| Median new input / cache read / cache write / output | 2,810 / 10,368 / 0 / 177 | 2 / 755 / 581 / 1,090 |
| Median wall time per run | 7.1 s | 17.9 s |
| Cost reported by the CLI | not reported | $1.21 over 21 runs (median $0.058) |

The full table as printed by the scorer is in [runs/portfolio-score/report.md](../runs/portfolio-score/report.md). Every finding has one row with a reason in [judgments.jsonl](../runs/portfolio-score/judgments.jsonl).

## Routing policies replayed on the same reviews

| Policy | Calls (failed) | Blockers found | Blocker misses on consequential plans | Total tokens | Total wall time |
| --- | ---: | ---: | ---: | ---: | ---: |
| Always Codex | 24 (0) | 18/18 | 0 | 335,826 | 181 s |
| Always Claude | 24 (3) | 18/18 | 0 | 52,122 | 404 s |
| Both | 48 (3) | 18/18 | 0 | 387,948 | 585 s |
| Routing rule (Claude on the 2 consequential pairs) | 24 (1) | 18/18 | 0 | 242,855 | 266 s |

The replay assumes the user accepts the Claude recommendation every time. It leaves out writer tokens and rechecks.

## What the results support

1. **Both reviewers found every planted flaw in every completed run.** The seeded test is too easy to separate them. It shows the pipeline works. It does not show one reviewer is better at catching blockers.
2. **Codex was faster and never failed the format check.** 7.1 s against 17.9 s median, 24/24 against 21/24 completed.
3. **Claude wrote more findings beyond the seeds.** 37 judged valid in 21 runs (1.8 per run) against 17 in 24 runs (0.7 per run). It also wrote more unsupported ones (0.9 against 0.5 per run). About two in three of Claude's extra findings and three in five of Codex's were judged valid.
4. **Claude never repeated a repaired flaw on a control. Codex did in 2 of 12 control runs**, both on the inventory control (p05). The grader marked both as borderline.
5. **The routing rule did not improve blocker recall here.** All four policies found 18/18. The case for sending consequential plans to Claude rests on finding 3, not on recall.

## Assumptions the data contradicts

- **"Claude costs about 7.6 times the tokens."** That came from the earlier pilot, where Claude ran as a subagent inside Claude Code and carried its startup context. In the standalone runner Claude used about one sixth of Codex's reported tokens (2,417 against 14,184 median). Codex's total is mostly cached input.
- **"Fewer tokens means cheaper."** Tokens are not dollars. Claude reported $0.058 per run. Codex reported no cost, so the dollar comparison is unknown. Most of Claude's tokens are output, which is priced higher than cached input.
- **"Codex is the low-cost default."** Supported for speed and reliability. Not supported for tokens. Unknown for dollars.

## Failures

- **Claude smoke, 4 of 6 rejected.** The validator had a hard 250-word limit and Claude wrote slightly more (270 words on the one reply inspected). The limit in the validator was raised to 400 words before the full run. The rubric text the reviewers see was not changed, so the Codex runs stay comparable. The 4096-byte cap still applies.
- **Claude full, 3 of 24 rejected.** All three added a sentence of plain text after the required format: two "NO BLOCKING ISSUES" replies with an explanation, one review with a closing remark. All three were on control plans, which is why the recall numbers do not change when failed runs count as zero. The raw replies are saved next to the runs as `.rejected.txt`. After the benchmark the validator was changed to drop such a closing remark and keep the review. Replayed offline, it accepts all three saved replies. The benchmark numbers above are not recomputed: these three stay counted as failed and were not graded.

## Limits

- The plans are synthetic and were written with AI help. Both splits are development data. This is not independent validation.
- The grader is an AI (Claude), which is one of the two reviewer families. It graded blind: random file names, no reviewer names, no usage files. No person has checked the judgments.
- Grading is not fully repeatable. The 55 Codex findings were graded twice by separate blind graders. They agreed on 47 (85%). All disagreements were between valid, unsupported and unclear. None changed a seed match or a false alarm. The earlier pass is kept in [runs/portfolio-score-codex](../runs/portfolio-score-codex/).
- Two repeats of the same plan are related, not independent. Twelve plans is a small set.
- Effort settings differ (Codex low, Claude medium), as the skill ships them. An equal-effort run was not done.
- The Codex model is unknown because the CLI did not report it.

## What I would do next

- Write harder plans, where a flaw only shows when two steps are read together, so the blocker test stops hitting its ceiling.
- Have a person grade a sample of the findings and compare with the AI grader.
- Run both reviewers at the same effort setting.
- Rerun Claude with the validator that keeps a review with a closing remark, and report the completion rate again.

## Reproduce

```text
python evals/plan-review/run_benchmark.py --suite full --provider codex --out runs/my-codex
python evals/plan-review/run_benchmark.py --suite full --provider claude --out runs/my-claude
python evals/plan-review/score.py blind runs/my-codex runs/my-claude --out runs/my-score
python evals/plan-review/score.py report runs/my-score
```

The `report` step needs a `judgments.jsonl` written by a grader who follows [scoring.md](../evals/plan-review/scoring.md).
