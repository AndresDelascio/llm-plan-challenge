VERDICT: PROCEED WITH CHANGES

### 1. [major] Release paths can double-credit stock
- Failure: The immediate decline release is not stated as conditional. If a decline handler and the expiry sweep (or a retry) both release the same reservation, the stock count inflates and later orders oversell.
- Fix: Route every release through the same atomic open→closed transition used for expiry, and credit stock only if that transition succeeds.

### 2. [major] Unknown payments cannot be polled
- Failure: When the gateway call times out, no gateway payment ID comes back, so step 4's polling has nothing to query, and a retry may double-charge.
- Fix: Send the reservation ID as the gateway idempotency key and reference, and poll by it.

### 3. [major] Late successes go undetected after the deadline
- Failure: Polling stops at the deadline, so a payment that succeeds afterwards is never seen and never refunded.
- Fix: At expiry, void the payment attempt at the gateway, and keep reconciling until it reaches a terminal state.

### 4. [minor] Five-minute budget is undefined
- Failure: The plan sets no client timeout, deadline value or sweep interval. A hung gateway call plus a slow sweep can exceed five minutes.
- Fix: Set the deadline from the reservation timestamp so that deadline plus sweep interval is under five minutes, with a shorter client timeout.

### 5. [minor] Tests miss the riskiest paths
- Failure: Step 2 does not cover late success after expiry, duplicate release, or success racing expiry.
- Fix: Add those three sandbox cases, asserting the stock count and the refund.
