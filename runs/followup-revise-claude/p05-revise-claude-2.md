# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. Record a reservation ID and its creation timestamp before calling the gateway. Send the reservation ID to the gateway as the idempotency key and payment reference, so a retry cannot double-charge and a payment whose call timed out can still be polled, voided and refunded by that ID.
2. Use a sandbox payment gateway. Test each of the following, asserting the final stock count and, where stock is released, the release time:
   - two concurrent shoppers against one remaining unit;
   - a gateway that never returns a result, with stock released within five minutes;
   - a declined payment, with stock released immediately;
   - a decline followed by the expiry sweep, with stock released only once;
   - a late payment success after expiry, which is refunded and not fulfilled.
3. Reserve with a single conditional storage update that succeeds only when enough stock exists. Record the reservation, in state `pending`, and the stock update in the same transaction.
4. Make every state transition (confirm, decline, expire) a conditional update from `pending`, and release stock only when the decline or expire update succeeds.
   - Release declined reservations immediately.
   - Poll unresolved payments by reservation ID against a deadline.
   - Within five minutes, atomically mark expired reservations closed and release their stock.
   - On expiry, void the payment at the gateway and keep reconciling by reservation ID until it reaches a terminal state.
   - If a late payment succeeds, refund it idempotently and block fulfillment for the expired reservation.
