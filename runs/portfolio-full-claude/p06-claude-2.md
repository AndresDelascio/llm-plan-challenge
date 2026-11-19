VERDICT: BLOCKED

### 1. [blocker] Non-atomic stock check and decrement
- Failure: Step 3 reads stock, then writes separately. Two concurrent shoppers both see one unit and both decrement, so stock is oversold.
- Fix: Use one conditional write (`SET stock = stock - q WHERE stock >= q`) and reject the order when zero rows are affected.

### 2. [blocker] Timed-out reservations never release
- Failure: Step 4 leaves timeouts pending for manual inspection, which violates the five-minute release requirement and strands stock.
- Fix: Add an expiry job that uses the step 1 timestamp to release pending reservations before five minutes.

### 3. [major] Unknown payment state unresolved on release
- Failure: A timed-out payment may later succeed after its units are released and resold, leaving the customer charged with no stock.
- Fix: Send the reservation ID as the gateway idempotency key, and void or query the payment before release. Refund any late capture.

### 4. [major] Reservation does not hold stock before charging
- Failure: Step 1 records only an ID and timestamp, and the decrement is listed after the gateway call. A shopper can be charged and then fail the stock check.
- Fix: Perform the atomic decrement in the same transaction as the reservation record, before calling the gateway.

### 5. [major] Release is not idempotent
- Failure: A late decline and the expiry job can both release the same reservation, inflating stock and enabling oversell.
- Fix: Release only through a conditional pending→released state transition, and restore stock only when that transition succeeds.
