# Grade 30 review findings

For each finding, open the plan and decide: **valid** (a specific failure that follows from the plan text and its brief), **unsupported** (wrong, contradicts the brief, or needs facts the plan does not give) or **unclear**. Do not look at `key.jsonl` or `codex.jsonl` until you are done. Write your answers in `human.csv`, one row per item.

## Item 01: plan [p05](../../evals/plan-review/plans/p05.md)

> ### 1. [blocker] Payment success can race expiry
> - Failure: If payment success and expiry run concurrently, fulfillment can proceed after the same units have been released and sold to another shopper.
> - Fix: Make payment success and expiry competing conditional transitions from the same open state. Allow fulfillment only if the paid transition wins.

Judgment:

## Item 02: plan [p02](../../evals/plan-review/plans/p02.md)

> ### 3. [major] The evaluation split can yield undefined recall
> - Failure: If all recordings with labeled moments land in tuning, the evaluation set cannot support a recall comparison.
> - Fix: Use the existing labels to ensure the held-out split includes recordings with labeled moments.

Judgment:

## Item 03: plan [p11](../../evals/plan-review/plans/p11.md)

> ### 4. [major] New editor is not frozen before evaluation
> - Failure: Step 2 freezes the baseline, prompts and overlap rule, but not the new editor's configuration. Tuning comes after the freeze, so the editor can still be adjusted after evaluation results are seen.
> - Fix: Reorder to split, tune, freeze both editors, then run the evaluation once.

Judgment:

## Item 04: plan [p09](../../evals/plan-review/plans/p09.md)

> ### 1. [blocker] No camera speed calculation
> - Failure: Step 4 produces transformed positions, but the plan never defines how to turn them into a speed in km/h for step 5.
> - Fix: Specify which ball observations to use, divide their calibrated distance in metres by their decoded timestamp difference in seconds, and multiply by 3.6.

Judgment:

## Item 05: plan [p03](../../evals/plan-review/plans/p03.md)

> ### 4. [minor] Aggregate MAE dominated by large stores
> - Failure: Unscaled MAE pooled across stores lets high-volume stores swamp regressions at small ones.
> - Fix: Also report a scaled metric (e.g. MAE divided by baseline MAE per store) and the share of stores that beat the baseline.

Judgment:

## Item 06: plan [p12](../../evals/plan-review/plans/p12.md)

> ### 1. [major] Replay leaves hardware timing unverified
> - Failure: Synthetic edge pairs can pass even if interrupt latency or counter clock error pushes real measurements beyond 2 ms.
> - Fix: Add an end-to-end test with independently timed beam breaks at 0.1 s and 3 s under representative interrupt load.

Judgment:

## Item 07: plan [p02](../../evals/plan-review/plans/p02.md)

> ### 2. [major] "Unseen" is not verified
> - Failure: The recordings are public and the split method is unspecified. The new editor's earlier development may already have used an evaluation recording, or one from the same show or speaker as a tuning recording. Hand-picking the split can also favour the new editor. Either way, recall is inflated at evaluation.
> - Fix: Assign recordings randomly, grouped by show or speaker, before running either editor. Exclude any recording previously used in developing the new editor.

Judgment:

## Item 08: plan [p11](../../evals/plan-review/plans/p11.md)

> ### 3. [major] Scoring unit does not match the split unit
> - Failure: Step 3 splits by window, but Step 4 scores three clips per whole recording, so scoring would include tuning windows. Highlights that straddle window boundaries are also undefined.
> - Fix: With the recording-level split, score whole evaluation recordings only and drop windows from the scoring.

Judgment:

## Item 09: plan [p03](../../evals/plan-review/plans/p03.md)

> ### 5. [minor] Eight weeks is a thin, single-season test
> - Failure: Eight consecutive Mondays cover one season, and their paired differences are autocorrelated, so the baseline comparison is weak.
> - Fix: Pair comparisons at the store-week level, and add earlier folds spread across the second year as backtest origins.

Judgment:

## Item 10: plan [p12](../../evals/plan-review/plans/p12.md)

> ### 2. [major] Missing finish can be paired with a later edge
> - Failure: Without an explicit expiry, a run missing its finish can remain open. A finish arriving after a full 6.5536 s counter period can then appear to fall within the supported interval.
> - Fix: Expire each pending start just after the 3 s measurement window, allowing for the 2 ms error budget, and discard subsequent finish edges until a new start.

Judgment:

## Item 11: plan [p12](../../evals/plan-review/plans/p12.md)

> ### 1. [blocker] Hardware timing error is unverified
> - Failure: Synthetic replay checks the conversion but cannot show that the physical gate meets the 2 ms bound. Clock drift and, if interrupt handlers read the counter, differences in interrupt latency can exceed the error budget.
> - Fix: Specify hardware capture at both edges and verify the physical gate against an independent timing reference. Include counter clock accuracy in the 2 ms budget.

Judgment:

## Item 12: plan [p07](../../evals/plan-review/plans/p07.md)

> ### 5. [minor] `abs()` hides reversed beam order
> - Failure: A run where beam 2 triggers first gives a plausible positive interval.
> - Fix: Reject runs where the edges arrive in the wrong order.

Judgment:

## Item 13: plan [p10](../../evals/plan-review/plans/p10.md)

> ### 1. [major] Training labels can cross the Monday cutoff
> - Failure: A training row can have an earlier forecast date while its seven-day sales target is still incomplete or unfinalized at the validation Monday. Using that row leaks future sales into the fit.
> - Fix: Include a training row only once all seven target values were finalized by that fold’s Monday cutoff.

Judgment:

## Item 14: plan [p10](../../evals/plan-review/plans/p10.md)

> ### 2. [major] Baseline availability is unspecified
> - Failure: If the baseline uses retrospectively finalized sales from the previous week, it can use values that were unavailable at the same cutoff imposed on the candidates.
> - Fix: Build the baseline from the prior week’s same-weekday sales as available at the Monday cutoff, with a fixed fallback for missing values.

Judgment:

## Item 15: plan [p08](../../evals/plan-review/plans/p08.md)

> ### 3. [major] Duplicate retries have no defined response
> - Failure: The plan does not say what the server returns when it detects a duplicate. If it returns an error, the client never clears the queued item and retries indefinitely.
> - Fix: Return the original success acknowledgement for a known key, and have the client dequeue only on that acknowledgement.

Judgment:

## Item 16: plan [p01](../../evals/plan-review/plans/p01.md)

> ### 2. [minor] Retry test lacks outcome assertions
> - Failure: The integration test can simulate lost acknowledgements and concurrent retries without detecting duplicate sessions or attendance.
> - Fix: Assert that the retries leave exactly one session with one complete set of attendance records, and that each successful retry returns the same committed session.

Judgment:

## Item 17: plan [p08](../../evals/plan-review/plans/p08.md)

> ### 4. [major] Duplicate response is undefined
> - Failure: If a deduplicated retry returns an error or an empty reply, the client cannot tell it succeeded and keeps retrying or shows a failure.
> - Fix: Return the original committed result, as a success, for a repeated key.

Judgment:

## Item 18: plan [p10](../../evals/plan-review/plans/p10.md)

> ### 2. [major] The last-week baseline lacks a cutoff rule
> - Failure: A baseline built from retrospectively finalized sales can use values that were unavailable on the forecast Monday, making the paired comparison unfair.
> - Fix: Forecast each day from the same weekday one week earlier using the Monday snapshot, and specify a fallback for unavailable values before evaluating.

Judgment:

## Item 19: plan [p10](../../evals/plan-review/plans/p10.md)

> ### 4. [major] As-of availability may not be reconstructable
> - Failure: Step 3 assumes history records what was finalized on each Monday. If the two-year history holds only current revised values, the backtest silently uses unavailable data.
> - Fix: Confirm finalization timestamps exist; otherwise apply a fixed conservative finalization lag.

Judgment:

## Item 20: plan [p11](../../evals/plan-review/plans/p11.md)

> ### 3. [major] New editor is never frozen
> - Failure: Step 2 freezes only the baseline, prompts and overlap rule. The new editor can keep being adjusted after evaluation results are seen, which biases the comparison.
> - Fix: Freeze the new editor's configuration after tuning and before any evaluation run.

Judgment:

## Item 21: plan [p12](../../evals/plan-review/plans/p12.md)

> ### 2. [major] Late finish can alias to a valid interval
> - Failure: If a run remains armed for a full counter period after the start, a late finish can produce a valid-looking result. For example, 6.6536 seconds wraps to 100 ms.
> - Fix: Expire the run at the supported deadline, allowing for the maximum interval’s timing tolerance, and discard finish events after expiry.

Judgment:

## Item 22: plan [p06](../../evals/plan-review/plans/p06.md)

> ### 4. [major] Reservation does not hold stock before charging
> - Failure: Step 1 records only an ID and timestamp, and the decrement is listed after the gateway call. A shopper can be charged and then fail the stock check.
> - Fix: Perform the atomic decrement in the same transaction as the reservation record, before calling the gateway.

Judgment:

## Item 23: plan [p05](../../evals/plan-review/plans/p05.md)

> ### 5. [minor] Tests miss the release paths
> - Failure: The two tests do not cover decline, late success after expiry, double release, or the five-minute bound.
> - Fix: Add one sandbox test for each, asserting final stock count and release time.

Judgment:

## Item 24: plan [p02](../../evals/plan-review/plans/p02.md)

> ### 1. [major] One clip can cover multiple moments
> - Failure: One-to-one matching undercounts recall when a top-three clip satisfies the overlap rule for two labeled moments.
> - Fix: Count each labeled moment once if any of the top three clips satisfies the overlap rule for it.

Judgment:

## Item 25: plan [p07](../../evals/plan-review/plans/p07.md)

> ### 3. [major] No timeout defines a "missing beam"
> - Failure: A second beam arriving after more than 6.5536 s aliases into the valid range (7 s reads as about 0.45 s) and is accepted as a real result.
> - Fix: Reject the run if the second edge has not arrived within a fixed window just over 3 s, such as 3.2 s.

Judgment:

## Item 26: plan [p06](../../evals/plan-review/plans/p06.md)

> ### 3. [major] Unknown payment state unhandled on release
> - Failure: A timed-out payment may actually have succeeded, so releasing the stock leaves a charged customer without a unit.
> - Fix: Send the reservation ID as the gateway idempotency key, void or query the payment before release, and refund any late success.

Judgment:

## Item 27: plan [p05](../../evals/plan-review/plans/p05.md)

> ### 3. [major] Late success undetected after expiry
> - Failure: Polling runs only up to the deadline. A payment captured afterwards is never seen, so the shopper is charged with no order and no refund.
> - Fix: On expiry, void the payment at the gateway and keep reconciling until it reaches a terminal state.

Judgment:

## Item 28: plan [p01](../../evals/plan-review/plans/p01.md)

> ### 1. [major] Queue entries never retire
> - Failure: The client has no step to remove an acknowledged entry, so later reconnects can resend sessions that already synced.
> - Fix: Remove the persisted queue entry after receiving a successful acknowledgement for its UUID, including a duplicate response that confirms the session committed.

Judgment:

## Item 29: plan [p05](../../evals/plan-review/plans/p05.md)

> ### 3. [major] Late payment success can go undetected
> - Failure: If polling ends when the reservation expires, a later gateway capture may never trigger the refund.
> - Fix: Reconcile expired payments through gateway notifications or durable polling until the payment reaches a terminal state, using a persisted payment reference.

Judgment:

## Item 30: plan [p05](../../evals/plan-review/plans/p05.md)

> ### 4. [major] Decline and expiry can both release stock
> - Failure: A decline arriving as expiry runs, or a retried decline, can return the same units twice.
> - Fix: Route every release through one transaction that restores stock only when it successfully closes an open reservation.

Judgment:
