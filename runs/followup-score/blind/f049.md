# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. **Reserve atomically before payment.**
   - In one transaction, decrement stock with a single conditional update that succeeds only when enough stock exists.
   - In the same transaction, insert a reservation row with its ID, quantity, state `pending`, creation timestamp, and an expiry deadline.
   - Set the deadline well inside five minutes (for example 4 minutes) so that sweep interval and processing time still fit within the limit.
   - If the update fails, reject the order without calling the gateway.

2. **Call the gateway with the reservation ID as the idempotency key.**
   - Retries then cannot double-charge.
   - An unknown outcome can later be looked up by that ID.
   - Give the call a client-side timeout much shorter than the reservation deadline.

3. **Close every reservation through one conditional state transition.**
   - Allow only `pending → paid` and `pending → released`, each as a compare-and-set on the current state.
   - Return the stock in the same transaction as the move to `released`.
   - This makes release happen exactly once, and a payment confirmation racing an expiry has a single winner.

4. **Resolve each payment outcome.**
   - **Success:** transition to `paid`. Fulfil only if that transition wins.
   - **Decline:** transition to `released` immediately.
   - **Timeout or unknown:** leave the reservation `pending` and poll the gateway by reservation ID until the deadline.

5. **Sweep expired reservations.**
   - Run a sweeper at a short interval (for example every 30 seconds) that transitions `pending` reservations past their deadline to `released`.
   - Drive it from stored timestamps on the database clock so it survives application restarts.
   - On expiry, try to void or cancel the payment at the gateway.

6. **Handle late success.**
   - If a payment later reports success for a `released` reservation, by poll or webhook, block fulfilment.
   - Refund it using a refund idempotency key derived from the reservation ID.
   - Keep reconciling released reservations with unknown payment state until the gateway reports a final result.

7. **Test against a sandbox gateway.**
   - **Concurrency:** two shoppers race for one remaining unit. Exactly one reserves and stock never goes negative.
   - **Decline:** stock is restored immediately.
   - **No response:** the gateway never returns. Stock is restored within five minutes, exactly once.
   - **Late success:** payment succeeds after expiry. It is refunded exactly once and nothing is fulfilled.
   - **Race at the deadline:** confirmation and expiry arrive together. The result is either paid and fulfilled, or released and refunded, never both.
   - **Restart:** the process restarts while a payment is unresolved. The reservation is still released on time.
