# Two-reviewer modes

## `both`

1. Run Codex, then Claude, once each against the untouched `plan-v1.md`. Pass only the plan and rubric to each CLI. Save separate critiques. Never pass the other review as context.
2. Merge overlapping findings for revision but preserve each critic's issue number and disposition in `decisions.md`. If one review fails, mark the result `PARTIALLY CHALLENGED` and identify the missing reviewer. If both fail, mark it `NOT CHALLENGED` and preserve the draft as `plan.md`.
3. Apply supported changes and stop after the two calls. Surface blockers and partial outcomes before reporting completion.

## `measure`

1. Freeze `plan-v1.md`. Run `review.py` twice per critic on that file, with outputs `critique-<critic>-run1.md` and `critique-<critic>-run2.md`. Use independent runs and parallel calls when available. No blocker recheck here.
2. If any run fails, record the missing runs in `decisions.md`, copy the draft to `plan.md` and report the incomplete comparison.
3. Merge issues only when they describe the same failure at the same step. Keep run provenance out of the shuffled issue list shown to the user. Ask for an accept/reject decision on every issue and wait for those decisions before revising or revealing provenance.
4. Write `decisions.md` with user decisions, provenance, per-run issues and accepted counts, accepted issues unique to one run within each critic, and accepted issues unique to each critic across both runs. Link each usage JSON. Apply accepted fixes to `plan.md`, summarize and stop.
