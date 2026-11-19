# Scoring rules

Frozen before any reviewer call of the portfolio runs. The plans, [answer key](answer-key.jsonl) and [stakes labels](stakes.jsonl) are frozen at the same commit. Scoring is done by an AI grader (Claude), not a person. No human has checked the judgments.

## Blinding

`python evals/plan-review/score.py blind <run folder>... --out <scoring folder>` copies each completed critique to `blind/<random id>.md` and writes `blind/index.jsonl` with the blind ID and the plan ID. The grader sees the plan, the answer key row and the blind critique. It does not see the reviewer name, run number, usage file or `mapping.json`.

## One row per finding

The grader writes `judgments.jsonl` with one row per numbered issue in each critique:

```json
{"blind_id": "x1", "case": "p04", "issue": 1, "matched_seeds": ["camera-coordinate-offset"], "judgment": "seed", "rationale": "Names the missing +240 x offset at step 4."}
```

| Judgment | When |
| --- | --- |
| `seed` | The finding names the failure in the key at the named step or its equivalent. A mention of the step without the failure does not count. One finding can match both seeds if it clearly states both. |
| `repaired-claim` | The plan is a control and the finding claims a failure that the control already repaired. Counts as a false alarm. |
| `valid` | Not a seed. A specific failure that follows from the plan text and the brief. |
| `unsupported` | Not a seed. Wrong, contradicts the brief, or needs facts the plan does not give. |
| `unclear` | The grader cannot decide from the text. |
| `duplicate` | Repeats an earlier finding in the same critique. Not counted again. |

A reviewer's severity label is not scored. A seed counts as detected in a run if any finding in that run matches it.

## Measures

`python evals/plan-review/score.py report <scoring folder>` prints these with exact counts.

- Blocker recall and all-seed recall: detected seed opportunities over opportunities in completed runs. A second view counts failed runs as detecting nothing.
- Repaired-claim false alarms: completed control runs with at least one `repaired-claim` finding, over completed control runs.
- Other findings: counts of `valid`, `unsupported` and `unclear`.
- Completion: completed runs over attempted runs.
- Median tokens per completed run, split into new input, cache read, cache write and output, plus median wall time. Codex counts cached tokens inside its input figure and Claude reports them separately, so the report converts both to the same four fields. Dollar cost is shown only where the CLI reports it.

## Routing comparison

Four policies are replayed on the same reviews, matched by plan and repeat number: always Codex, always Claude, both (a seed counts if either review found it; tokens and wall time are added), and the routing rule (Codex for `routine` plans, Claude for `consequential` plans). The routing replay assumes the user accepts the Claude recommendation every time. Stakes labels come from the brief only and are separate from seed severity. The replay leaves out writer tokens and blocker rechecks.

## Limits fixed in advance

- Both splits are development data written with AI help. Results on them are not independent validation.
- Two repeats of one plan are related, not independent samples.
- The grader is Claude, one of the two reviewer families.
