VERDICT: PROCEED WITH CHANGES

### 1. [major] Releases not guarded by reservation state
- Failure: A declined reservation is released immediately, then the expiry sweep can release it again. Stock is incremented twice and the extra unit is oversold. A confirmed payment can likewise be expired by the sweep.
- Fix: Make every transition (confirm, decline, expire) a conditional update from `pending`, and release stock only when that update succeeds.

### 2. [major] No gateway handle for unknown payments
- Failure: When the gateway call times out, no payment ID comes back, so step 4 has nothing to poll or refund against. A retry can also double-charge.
- Fix: Send the reservation ID as the gateway idempotency key and reference, and poll and refund by it.

### 3. [major] Late success undetected after expiry
- Failure: Polling runs only up to the deadline. A payment captured afterwards is never seen, so the shopper is charged with no order and no refund.
- Fix: On expiry, void the payment at the gateway and keep reconciling until it reaches a terminal state.

### 4. [major] Reservation order relative to the gateway call is ambiguous
- Failure: Step 1 records the reservation before the gateway call, but the stock decrement is in step 3. If the decrement runs after payment, shoppers are charged for stock that is gone.
- Fix: Merge steps 1 and 3 into one transaction that commits before the gateway call.

### 5. [minor] Tests miss the release paths
- Failure: The two tests do not cover decline, late success after expiry, double release, or the five-minute bound.
- Fix: Add one sandbox test for each, asserting final stock count and release time.
