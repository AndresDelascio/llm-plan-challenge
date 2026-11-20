VERDICT: BLOCKED

### 1. [blocker] Non-atomic stock check and decrement
- Failure: Step 3 reads stock, then writes separately. Two shoppers both see one unit and both decrement, so the last unit is sold twice.
- Fix: Use a single conditional decrement (`SET stock = stock - q WHERE stock >= q`) and fail the order if zero rows change.

### 2. [blocker] Timed-out reservations never release
- Failure: Step 4 leaves timeouts pending for manual inspection. This breaks the five-minute release requirement and locks stock indefinitely.
- Fix: Add a sweeper that uses the creation timestamp to release pending reservations automatically before five minutes.

### 3. [major] Unknown payment state unresolved
- Failure: After a timeout the charge may still succeed. Releasing the stock then leaves a paid order with no units.
- Fix: Send the reservation ID as an idempotency key, void or query the payment before release, and refund any late capture.

### 4. [major] Reservation not tied to the stock hold
- Failure: Step 1 records the reservation before the gateway call, but the decrement is a separate, unordered step. A crash between them leaves either a reservation with no stock held or stock held with no reservation. A repeated release can also add stock twice.
- Fix: Do the reservation insert and the decrement in one transaction before the gateway call, and make release a guarded state transition (pending→released, once).

### 5. [minor] Tests lack assertions and coverage
- Failure: Step 2 names scenarios without expected outcomes, and omits the decline path and release timing.
- Fix: Assert that exactly one shopper succeeds and that stock is restored within five minutes after a decline or a timeout.
