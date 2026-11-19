# Plan review evaluation

Twelve synthetic plans form six matched pairs. Each pair has a flawed plan with two seeded issues and a control with both seeds repaired. Cases cover camera calibration, timing gates, clip ranking, offline sync, forecasting, and inventory. Controls can still contain genuine concerns. This suite is authored with AI assistance and currently has no scored model runs.

## Run

1. Freeze the plan files and [answer key](answer-key.jsonl) at a commit before collecting results. Send each critic only the selected plan and shared rubric. Keep filenames, labels, paired versions, and earlier reviews out of its prompt.
2. Run the three smoke pairs once per reviewer for 12 calls. After fixing integration issues, freeze the configuration. Then run all 12 plans twice per reviewer for a 48-call primary evaluation. Use the same frozen text and record model version, CLI, effort, run ID and latency. Both splits are inspectable development data. For a generalization claim, ask another person to supply unseen pairs and keep those outside this repository until scoring is complete.
3. Run from the repository root. `--dry-run` prints the intended call count without invoking either CLI. For live runs, choose a new output directory. Record exact model IDs with `--codex-model` and `--claude-model` for a reproducible model comparison. Add `--effort low` to set the same requested effort label for both providers. A provider's effort label does not imply equivalent compute.

   ```text
   python evals/plan-review/run_benchmark.py --suite smoke --dry-run
   python evals/plan-review/run_benchmark.py --suite smoke --out runs/smoke
   python evals/plan-review/run_benchmark.py --suite full --out runs/full
   ```

4. Shuffle critiques and hide provider, run order and metadata before judging. Score each seeded failure from the key against the actual claim. Give credit for a specific failure at the named step or its equivalent, including when one finding clearly identifies two failures. Deduplicate repeated claims. Judge non-seeded findings separately as valid, unsupported, or unclear and note the rationale. Ask a second person to independently score a subset and report agreement before reconciling.
5. Save raw critiques with usage JSON. For scoring, record plan ID, run ID, finding number, matched seed IDs, valid/unsupported/unclear judgment, evidence and adjudicator. Keep provider and runtime metadata in the run index. Log failures and show denominators and run counts.

## Report

| Measure | Calculation |
| --- | --- |
| Blocker recall | Detected blocker opportunities divided by all blocker opportunities across scored runs |
| Seeded recall | Detected seed opportunities divided by all seed opportunities across scored runs |
| Repaired-claim rate | Control runs in which a reviewer still claims a repaired failure, divided by completed control runs |
| Finding validity | Valid deduplicated findings divided by the number judged, with unclear counts shown separately |
| Reliability | Valid completed runs divided by attempted runs, including error types |
| Efficiency | Median input, cache and output tokens and wall time per completed run, plus cost per valid finding when a trustworthy cost is available |

Report exact counts and per-case misses. Include a sensitivity result that treats failed reviews as detecting zero seeds. Repeated runs of the same plan are related observations. Compare configurations within each provider and show original and revised usage fields separately when their accounting differs. Analyze the matched control alongside each flawed plan before claiming a reviewer caught the specific change.

For a portfolio demo, show one tracking or ML pair, a missed blocker, a false alarm, and the token or latency trade-off from actual logs. The [historical results](../../docs/benchmarks.md) describe a different experiment.

## Test the routing policy

Before collecting new results, label stakes from the brief without seeing reviews. Keep those labels separate from the severity key. Compare all-Codex, all-Claude, all-both and the human-approved routing policy on the same runs and repeat indices. Use an issue union for the both policy, and sum token totals and sequential latency for its two calls. Treat approval outcomes as inputs to the policy. Report blocker misses within consequential plans and measure how often the writer asked the right question on fresh invocations. This replay measures reviewer selection. It excludes writer tokens and blocker rechecks.

The original seeded runs had mean reported totals of 8,249 for Codex CLI and 62,641 for the Claude subagent. Using those means gives the following first-pass budget scenarios versus always using the historical Claude subagent. These are workload projections from the old workflows. The percentages describe reported token counts under assumed traffic mixes.

| Consequential share | Claude on escalation | Both on escalation |
| --- | ---: | ---: |
| 5% | 82.5% fewer tokens | 81.8% fewer tokens |
| 10% | 78.1% fewer tokens | 76.8% fewer tokens |
| 20% | 69.5% fewer tokens | 66.8% fewer tokens |

Recompute the pilot findings, usage summaries and scenario math with `python evals/plan-review/historical_summary.py`.
