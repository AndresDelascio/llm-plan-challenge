VERDICT: BLOCKED

### 1. [blocker] Decline release can double-release stock
- Failure: Only the expiry release is atomic and state-guarded. If a decline result arrives after expiry, or a decline is retried, stock is incremented twice and the system oversells.
- Fix: Route every release through one conditional transition (open→closed) in the same transaction as the stock increment.

### 2. [major] Unknown payments cannot be reliably polled or refunded
- Failure: The reservation ID is recorded but never sent to the gateway. After a timeout there is no key to query or refund against, and a retry could double-charge.
- Fix: Pass the reservation ID as the gateway idempotency key and reference.

### 3. [major] Late successes go undetected after expiry
- Failure: Polling runs only until the deadline. A charge that succeeds afterwards is never seen, so the customer pays, gets no goods and gets no refund.
- Fix: Keep reconciling closed reservations (by poll or webhook) until the gateway reports a final state, or void the attempt at expiry.

### 4. [minor] Five-minute bound is not anchored
- Failure: The deadline start and sweeper cadence are unspecified. Gateway timeout plus sweep interval can exceed five minutes.
- Fix: Set the deadline from the creation timestamp on the database clock, with a sweep interval that leaves margin.

### 5. [minor] Tests miss the risky paths
- Failure: The tests cover only two concurrent shoppers and a gateway that never returns. Decline, decline after expiry and late success are untested.
- Fix: Add those three sandbox cases, asserting that stock is never inflated.
