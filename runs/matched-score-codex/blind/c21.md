VERDICT: BLOCKED
### 1. [blocker] Concurrent shoppers can oversell
- Failure: Two shoppers can both read one remaining unit and pass the stock check before either decrement is written.
- Fix: Use an atomic conditional decrement that succeeds only when enough stock remains. Create the reservation in the same transaction.

### 2. [blocker] Timeouts leave stock reserved indefinitely
- Failure: If the gateway never responds, the reservation stays pending for manual inspection and can miss the five-minute release deadline.
- Fix: Set a gateway timeout and use a durable job to release timed-out reservations within five minutes. Make the release idempotent so retries cannot add stock twice.

### 3. [major] Late payment success can conflict with released stock
- Failure: A timed-out payment can succeed after its reservation expires and another shopper buys the released units.
- Fix: Make payment confirmation conditional on the reservation still being active. If expiry wins, void or refund the late payment and skip fulfillment.
