# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. Reserve stock with one atomic conditional decrement that succeeds only if enough stock remains. If it fails, reject the order and do not call the gateway.
2. In the same step, record a reservation ID and its creation timestamp. Call the gateway only after the decrement and the reservation record have succeeded.
3. On an explicit decline, release the reserved units immediately.
4. On a gateway timeout or missing result, automatically expire the reservation and release its units within five minutes of the timeout. Make the release a guarded state transition (pending to released) so it happens exactly once, even if a decline and the expiry race.
5. Never fulfil an expired or released reservation. If a payment success arrives late for one, void or refund that payment instead of fulfilling the order.
6. Use a sandbox payment gateway. Test:
   - two concurrent shoppers against one remaining unit: exactly one succeeds and stock never goes below zero;
   - a gateway that never returns a result: the units are released within five minutes, and only once;
   - a late success after expiry: the order is not fulfilled and the payment is voided or refunded.
