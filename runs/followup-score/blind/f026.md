# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. Reserve stock in a single database transaction before calling the gateway.
   - Decrement with one conditional write: `SET stock = stock - q WHERE stock >= q`. If no row is affected, reject the order.
   - In the same transaction, record a reservation with its ID, quantity, status `pending` and creation timestamp.
2. Call the gateway only after that transaction commits. Send the reservation ID as the gateway idempotency key.
3. Settle the reservation on an explicit gateway result.
   - Success: mark the reservation `confirmed`.
   - Explicit decline: release the reservation (see step 5).
4. Run a sweeper that expires timed-out reservations, so their stock is released within five minutes.
   - The sweeper finds `pending` reservations by their creation timestamp. The gateway call timeout and the sweep interval are set so that release always falls inside the five-minute limit.
   - Before releasing, it voids or queries the payment using the reservation ID.
     - Payment succeeded: mark the reservation `confirmed` instead of releasing.
     - Payment voided or not found: release.
     - Payment state still unknown at the deadline: release anyway and flag the reservation for reconciliation.
   - If a payment is later found to have succeeded after its stock was released, refund it.
5. Make release idempotent on reservation status.
   - In one transaction, change the status from `pending` to `released` and add the quantity back to stock.
   - Add the stock back only if the status change affected a row, so a decline plus an expiry cannot inflate stock.
6. Test against a sandbox payment gateway.
   - Two concurrent shoppers against one remaining unit: exactly one succeeds.
   - A gateway that never returns a result: stock is released within five minutes.
   - An explicit decline: stock is released.
   - A late success after timeout: the reservation is confirmed if not yet released, or the payment is refunded if it was.
   - A decline and an expiry on the same reservation: stock is added back only once.
