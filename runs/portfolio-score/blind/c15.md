VERDICT: BLOCKED

### 1. [blocker] Non-atomic stock check and decrement
- Failure: Step 3 reads stock and then writes separately, so two concurrent shoppers both pass the check on the last unit and it is oversold.
- Fix: Use a single conditional decrement (`SET stock = stock - q WHERE stock >= q`) and reject if no row is affected.

### 2. [blocker] Timed-out reservations never released
- Failure: Step 4 leaves timeouts pending for manual inspection, which violates the five-minute release requirement and locks stock indefinitely.
- Fix: Add a sweeper that uses the step 1 timestamp to expire pending reservations within five minutes.

### 3. [major] Unknown payment state unhandled on release
- Failure: A timed-out payment may actually have succeeded, so releasing the stock leaves a charged customer without a unit.
- Fix: Send the reservation ID as the gateway idempotency key, void or query the payment before release, and refund any late success.

### 4. [major] Reservation and decrement ordering undefined
- Failure: The reservation is recorded before the gateway call, but the decrement is a later step, so payment may be captured before stock is secured.
- Fix: Do the reservation record and the atomic decrement in one transaction, before the gateway call.

### 5. [minor] Tests miss release behaviour
- Failure: The tests cover concurrency and a hanging gateway, but nothing asserts release within five minutes or guards against a double release (decline plus expiry) inflating stock.
- Fix: Make release idempotent on reservation status, and add tests for decline, timeout expiry and late success.
