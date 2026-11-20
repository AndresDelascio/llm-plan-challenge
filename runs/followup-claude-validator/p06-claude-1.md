VERDICT: BLOCKED

### 1. [blocker] Non-atomic stock check and decrement
- Failure: Step 3 reads stock, then writes separately. Two concurrent shoppers both see one unit and both decrement, so the system oversells.
- Fix: Use one conditional atomic write (`SET stock = stock - q WHERE stock >= q`) and fail the order if zero rows are affected.

### 2. [blocker] Timed-out reservations never release
- Failure: Step 4 leaves timeouts pending for manual inspection, which violates the five-minute release requirement. A gateway that never returns holds stock forever.
- Fix: Set a gateway call deadline and add a sweeper that expires pending reservations by the creation timestamp within five minutes.

### 3. [major] Unknown payment state is not reconciled
- Failure: After a timeout the charge may have succeeded. Releasing the stock then leaves a paid customer with no unit.
- Fix: Send the reservation ID as the gateway idempotency key. Query the payment status before release, and void or refund any charge that succeeds late.

### 4. [major] Reservation order is ambiguous
- Failure: Step 1 records a reservation before the gateway call, but the decrement comes in step 3. If the decrement runs after payment, a shopper can be charged for stock that is gone.
- Fix: Do the atomic decrement and the reservation record in one transaction before calling the gateway.

### 5. [minor] Tests lack assertions and cases
- Failure: Step 2 names scenarios but no expected results, and has no decline or release-timing test.
- Fix: Assert exactly one sale and stock never negative. Add tests for decline and timeout that check release within five minutes.
