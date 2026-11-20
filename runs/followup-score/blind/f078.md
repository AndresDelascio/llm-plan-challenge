# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. **Reserve atomically, before calling the gateway.**
   - Decrement stock with a single conditional write: `UPDATE stock SET available = available - :qty WHERE sku = :sku AND available >= :qty`. Zero rows affected means the order is rejected as out of stock.
   - Do not use a separate read followed by a write; that lets two shoppers both pass the check.
   - In the same transaction, insert a reservation row with ID, SKU, quantity, state `PENDING`, `created_at`, and `expires_at`.
   - Set `expires_at` to at most 4 minutes after creation, leaving margin inside the five-minute limit.

2. **Call the gateway with the reservation ID as the idempotency key.**
   - Use a client timeout far shorter than the reservation expiry, for example 30 seconds.
   - This ensures a retry or status lookup never creates a second charge.

3. **Resolve each outcome with a guarded state transition.**
   - Every transition is conditional on the current state (`UPDATE ... WHERE id = :id AND state = 'PENDING'`). Stock is returned in the same transaction as the move to `RELEASED`, so a reservation can never be released twice.
   - **Success:** `PENDING → CONFIRMED`. Stock stays decremented.
   - **Explicit decline:** `PENDING → RELEASED`. Stock is returned immediately.
   - **Timeout or unknown:** query the gateway for the payment status by idempotency key.
     - If it was paid, confirm.
     - If it was declined or not found, void or cancel the attempt, then release.
     - If it is still unknown at `expires_at`, send a void and release anyway. The five-minute limit wins.

4. **Run an expiry sweeper every 30 seconds or less.**
   - It picks up every `PENDING` reservation past `expires_at` and applies the timeout path from step 3.
   - This covers app crashes between reserving and calling the gateway, as well as gateways that never answer.
   - It must be safe to run concurrently with request handlers, which the guarded transitions provide.

5. **Handle a late success after release.**
   - If a payment confirmation arrives for a `RELEASED` reservation, try a fresh atomic reservation as in step 1.
   - If stock is available, confirm the order.
   - If not, refund or void automatically and notify the customer.
   - Never confirm against stock that was already returned.

6. **Add observability.**
   - Log every state transition with the reservation ID.
   - Alert on any `PENDING` reservation older than 5 minutes, on late-success refunds, and on `available < 0`.
   - Manual inspection is a backstop for alerts, not the release mechanism.

## Verification (sandbox gateway)

- **Concurrency:** N parallel shoppers against 1 remaining unit. Exactly one reservation succeeds and stock never goes below 0.
- **Decline:** stock is restored immediately.
- **Gateway never returns:** stock is restored within 5 minutes, with a void attempted.
- **Crash after reserve, before gateway call:** the sweeper releases the stock.
- **Timeout, then status lookup shows paid:** the order is confirmed with no double charge.
- **Late success after release:** covered for both cases, stock available (confirmed) and stock gone (refunded).
- **Sweeper races a handler on the same reservation:** stock is returned exactly once.
