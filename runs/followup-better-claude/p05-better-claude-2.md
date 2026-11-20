# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown, so a payment may succeed after its reservation has been released.

## Design rules

- **States:** each reservation is `held`, `committed` (paid, stock sold) or `released` (stock returned). It leaves `held` exactly once.
- **Guarded transitions:** every transition is a conditional update that succeeds only if the state is still `held`, in the same transaction as its stock change. When payment confirmation races expiry, exactly one wins.
- **Invariant:** available + held + sold = total stock, at all times.
- **Time budget:** the five minutes run from the decline or the client-side timeout. Fix the timeout at reservation creation and store the release deadline with it. Set the gateway call timeout, hold deadline and sweep interval (for example 30 seconds) so that the worst-case sum is comfortably under five minutes.
- **Clock:** use the database clock for all deadline comparisons, not application server clocks.

## Implementation

1. **Reserve atomically.**
   - In one transaction, run a single conditional update that decrements available stock only if enough exists.
   - In the same transaction, insert the reservation as `held` with its ID, quantity, creation timestamp and deadline.
   - If the update affects no rows, reject the order as out of stock and never call the gateway.

2. **Call the gateway only after the reservation commits.**
   - Send the reservation ID as the gateway idempotency key, so retries and status lookups refer to one payment attempt.
   - Apply an explicit client-side timeout to the call.
   - If the gateway supports authorize-then-capture, authorize here and capture only in the commit step, so an expired reservation can be voided rather than refunded.

3. **Resolve known outcomes immediately.**
   - **Success:** transition `held` to `committed`, then allow fulfillment. Fulfillment must check for `committed`, never for payment success alone.
   - **Decline:** transition `held` to `released` and return the stock in the same transaction.
   - **Lost transition:** if the reservation was already released, treat a success as a late payment (step 5).

4. **Resolve unknown outcomes against the deadline.**
   - On a timeout or ambiguous error, leave the reservation `held` and poll the gateway status by idempotency key.
   - Run a sweeper on the fixed interval that atomically releases every `held` reservation past its deadline, whether or not polling has finished.
   - Make the sweeper idempotent and safe to run concurrently or after a crash; the guarded transition gives this.

5. **Handle late payments.**
   - If a poll result or callback reports success for a `released` reservation, void or refund it using an idempotency key derived from the reservation ID.
   - Block fulfillment and record the refund outcome.
   - Keep polling released reservations with an unknown payment state until the gateway gives a definitive answer, so no charge is left without a refund.
   - Alert if a refund fails or a payment stays unknown beyond a set limit.

6. **Test against a sandbox gateway with injectable faults.**
   - **Concurrency:** two shoppers race for one remaining unit; exactly one reserves and the other is rejected before any gateway call.
   - **Decline:** stock is available again immediately.
   - **Gateway never returns:** stock is released within five minutes of the timeout, measured end to end.
   - **Late success:** the payment is refunded exactly once and nothing is fulfilled.
   - **Confirmation racing expiry:** exactly one outcome applies and the invariant holds.
   - **Duplicates:** repeated callbacks, repeated polls and retried gateway calls cause no double charge, double release or double refund.
   - **Sweeper failure:** kill the sweeper mid-run and restart it; expired holds are still released on time and only once.
   - **Invariant:** check it after every test and under a randomized concurrent load run.

7. **Monitor in production.**
   - Track the age of the oldest `held` reservation, sweeper lag, the count of unknown payments and refund failures.
   - Alert when a hold outlives its deadline by more than one sweep interval.
