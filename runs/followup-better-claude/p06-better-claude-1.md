# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. **Reserve atomically.** Decrement stock and create the reservation in one transaction, before calling the gateway.
   - Use a single conditional write: `UPDATE stock SET available = available - :qty WHERE sku = :sku AND available >= :qty`.
   - If zero rows are affected, reject the order as out of stock. Do not use a separate read followed by a write.
   - In the same transaction, insert the reservation row: ID, SKU, quantity, state `PENDING`, creation timestamp, and an expiry well under five minutes (e.g. created + 4 min) to leave room for the sweeper.

2. **Call the gateway with a bounded timeout.**
   - Pass the reservation ID as the idempotency key.
   - Set the client timeout well below the reservation expiry (e.g. 30 s).

3. **Handle each gateway outcome with a guarded state transition.** Every transition is conditional on the current state being `PENDING`, so each reservation is confirmed or released exactly once.
   - **Approved:** move `PENDING → CONFIRMED`. The stock stays decremented.
   - **Explicit decline:** move `PENDING → RELEASED` and add the quantity back in the same transaction.
   - **Timeout or unknown:** do not confirm, and do not leave it for manual inspection. Immediately attempt to void the payment using the idempotency key, then release as for a decline.

4. **Run an expiry sweeper as the backstop.** This covers crashes and missed timeouts.
   - Run it at least every 30 s over `PENDING` reservations past expiry.
   - For each one, query the gateway for the payment status by idempotency key:
     - Captured: confirm the reservation.
     - Declined or not found: release it.
     - Still unknown: void the payment, then release it.
   - If the void itself fails, release the stock anyway to meet the five-minute bound, and flag the payment for a void/refund retry queue.

5. **Handle late approvals.** If an approval or webhook arrives for a reservation that is already `RELEASED`:
   - Never ship against released stock.
   - Either re-reserve atomically as in step 1, or, if stock is gone, automatically refund and notify the shopper.

6. **Test against a sandbox gateway.**
   - **Concurrency:** two or more shoppers race for one remaining unit. Exactly one reservation succeeds and stock never goes negative.
   - **Decline:** stock is restored immediately.
   - **Gateway never returns:** stock is released within five minutes and a void is attempted.
   - **Late approval after release:** the payment is refunded or re-reserved, with no oversell.
   - **Crash between reserve and gateway call:** the sweeper releases the reservation.
   - **Duplicate callbacks or retries:** no double release and no double charge.
   - **Invariant after every test:** `available + pending + confirmed = initial stock`.
