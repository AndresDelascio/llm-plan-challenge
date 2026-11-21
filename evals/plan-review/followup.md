# Follow-up tests: rules frozen before the first call

Written 2026-11-19, after the main benchmark and before any call below. The 12 plans and the [answer key](answer-key.jsonl) are unchanged. The three prompts are constants in [followup.py](followup.py). Grading is by an AI (Claude), blind. No person checks it. No failed call is rerun.

These tests were added because the main benchmark compares two reviewers with each other. It never compares a review with the common habit of asking one model to "make it better", and it counts findings, not fixed plans.

## Test 1: does `/challenge` beat "make it better"?

Each arm ends in a final plan. Twice per plan.

| Arm | What happens | Calls |
| --- | --- | ---: |
| A-Claude | A fresh Claude gets the plan and "Make this plan better." | 24 |
| A-Codex | The same with Codex | 24 |
| B | A fresh Claude gets the plan plus the saved Codex review (low effort) and revises | 24 |
| C | A fresh Claude gets the plan plus the saved Claude review and revises | 21 |

Arms B and C reuse the reviews in `runs/portfolio-full-codex` and `runs/portfolio-full-claude`. Arm C has 21 calls because 3 Claude reviews failed the format check. All 3 were on repaired plans.

The grader sees the original plan, the answer key and the final plan under a random name. It writes one row per final plan:

```json
{"blind_id": "f001", "case": "p04", "seeds": {"camera-coordinate-offset": "fixed", "camera-acceptance-metric": "not-fixed"}, "new_defect": false, "rationale": "One sentence."}
```

- Flawed plan, per planted flaw: `fixed` when the final plan meets the requirement in the key, else `not-fixed`.
- Repaired plan, per flaw of its pair: `kept` when the repair is still there, else `regressed`.
- `new_defect` is true when the final plan breaks a constraint or non-goal of the brief, or adds a specific failure the original did not have.

Measures: planted flaws fixed over 24 per arm, repaired plans with a regression, final plans with a new defect, median words, median tokens and median time. In arms B and C the tokens and time of the saved review are added to the revision. A failed call counts as nothing fixed.

## Test 2: a second model, or the same model twice?

No new reviewer calls. Input: the findings judged `valid` in `runs/portfolio-score/judgments.jsonl`. A blind grader groups them per plan. Two findings are the same when they name the same plan step and the same failure.

Measure, per plan, on plans where all four reviews completed: distinct valid findings in Codex run 1 + Codex run 2, in Claude run 1 + Claude run 2, and in one Codex + one Claude run (mean of the four combinations). Planted flaws are left out because every review found them.

## Test 3: is Claude still less reliable with the current validator?

`run_benchmark.py --suite full --provider claude`, 24 calls. Only the completion rate is reported. These reviews are not graded and do not replace the main results.

## Test 4: does the stakes rule fire correctly?

Each model classifies each of the 12 plans once as `routine` or `consequential` (24 calls), using the wording of the skill. Compared with [stakes.jsonl](stakes.jsonl), which was frozen with the main benchmark. Any other reply counts as wrong.

## Test 5: a reworded stakes rule (frozen 2026-11-20, before any call)

Test 4 missed the store forecast pair (p03, p10) with both models: the money risk is indirect, because stores act on the forecast. The new wording (`STAKES_V2` in [followup.py](followup.py)) names that case. Each model classifies the 12 plans and four new held-out plans once (32 calls). Labels: [stakes.jsonl](stakes.jsonl) and [holdout-stakes.jsonl](holdout-stakes.jsonl), both frozen before the run. Any reply other than one of the two words counts as wrong. Test 4's prompt and results are not changed.

- **Pass:** at least 11 of 12 on the main plans and 4 of 4 on the held-out plans, for each model, with no routine plan called consequential.
- **Why the held-out plans:** the new wording was written after seeing which plans Test 4 missed, so a pass on p03 and p10 alone could be fitting the test. h01 and h02 carry indirect money risk in new settings; h03 and h04 are routine.
- **Ship rule:** the skill's wording changes to match only if both models pass.
- **Limit:** I wrote the held-out plans and their labels, so they are not an independent sample. Four plans is a smoke check, not a measure.

## Limits fixed in advance

- Arm A is a fresh chat with a one-line prompt. A long chat that already holds the reasoning is not tested.
- In B and C the reviser is a fresh Claude, not the chat that wrote the plan.
- The planted flaws were easy for both reviewers, so test 1 can show that a habit misses them. It cannot rank the two reviewers.
- Test 2 depends on which findings an AI grader called valid.
- Twelve plans, two related repeats. Small counts.
