# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. Reserve stock before calling the gateway. In a single transaction:
   - Decrement stock with one conditional write (`SET stock = stock - q WHERE stock >= q`). Reject the order if zero rows are affected.
   - Record the reservation with its ID, quantity, creation timestamp and state `pending`.
2. Call the gateway only after that transaction commits. Send the reservation ID as the gateway idempotency key.
3. Use a sandbox payment gateway. Test two concurrent shoppers against one remaining unit and a gateway that never returns a result.
4. Release stock only through a conditional `pending` → `released` state transition. Restore the reserved quantity only when that transition succeeds, so a repeated or competing release cannot inflate stock.
5. When the gateway returns an explicit decline, release the reservation through the step 4 transition.
6. Run an expiry job that uses the step 1 timestamp to find reservations still pending and release them before five minutes have passed. For each one:
   - Void the payment or query its state with the reservation ID before releasing.
   - If the query shows the payment was captured, confirm the reservation instead of releasing it.
   - Otherwise release through the step 4 transition.
7. Refund any capture that arrives after a reservation has been released.
