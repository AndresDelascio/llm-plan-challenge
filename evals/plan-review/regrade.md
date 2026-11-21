# Second grader: rules frozen before the first call

Written 2026-11-20, before any call below. The code and the prompt are in [regrade.py](regrade.py) (`REGRADE`, `SEED`).

## The question

The matched-pair benchmark was graded by one Claude grader. Claude also wrote half the reviews. Does a second grader from another family agree with those judgments, and does agreement differ between findings Claude wrote and findings Codex wrote? A gap would hint that the Claude grader favoured its own family.

## Sample

- 30 extra findings (not seeds), taken from [runs/portfolio-score/judgments.jsonl](../../runs/portfolio-score/judgments.jsonl): 15 from Codex reviews and 15 from Claude reviews. Only findings the Claude grader called `valid` or `unsupported` are eligible.
- Drawn with `random.Random(20261120)`, then shuffled so the item number does not reveal the reviewer.
- The sample came out at 11 `valid` and 4 `unsupported` for each reviewer.

## Second grader

Codex (low effort, tools off, through the skill's runner). It sees the plan, one finding and the `scoring.md` definitions of `valid`, `unsupported` and `unclear`. It does not see which model wrote the finding or what the Claude grader said. One call per finding: 30 calls. A failed call is logged, not rerun, and counts as no judgment.

## A person

[runs/regrade/sheet.md](../../runs/regrade/sheet.md) lists the same 30 findings with a link to each plan, and nothing else: no reviewer, no AI judgment. Answers go in `human.csv`. `python evals/plan-review/regrade.py report` compares them with both graders once filled in.

## What will be reported, fixed in advance

- Agreement of Codex with the Claude grader, overall and split by reviewer, with exact 95% intervals.
- **Self-preference check:** if agreement on Claude-written findings is higher than on Codex-written findings by 3 or more of 15, the README will say the Claude grader may favour Claude reviews. A smaller gap will be reported as no sign of it at this sample size.
- If overall agreement is below 20 of 30, the README will say the extra-finding counts in the benchmark depend on the grader and should be read as one grader's view.

## Limits fixed in advance

- 15 per reviewer can only show a large gap.
- Codex is also a party: it wrote half the reviews. Agreement between two AI graders is not correctness. The person's grades are the reference, and they are not in yet.
- Seeds are left out: they were matched against a fixed answer key, not judged.
