# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. Record a reservation ID and its creation timestamp before calling the gateway. Send the reservation ID to the gateway as a correlation key.
2. Use a sandbox payment gateway. Test two concurrent shoppers against one remaining unit and a gateway that never returns a result.
3. Reserve with a single conditional storage update that succeeds only when enough stock exists. Record the reservation and stock update in the same transaction.
4. Resolve each reservation through atomic transitions from the open state, and keep reconciling unknown payments after expiry.
   - **Decline:** Release declined reservations immediately.
   - **Competing transitions:** Make payment acceptance and expiration competing atomic transitions from the open state, so only one can win. Allow fulfillment only if payment acceptance wins.
   - **Expiration:** Run a durable worker that expires open reservations independently of gateway calls, using the stored creation timestamp. It atomically marks each expired reservation closed and releases its stock. Set its scan interval to leave time to complete the release within five minutes, even if a gateway call hangs or the requesting process crashes.
   - **Reconciliation:** Continue reconciling expired reservations whose payment outcome is unknown, using the correlation key, until each reaches a terminal state. If a late payment succeeds, refund it idempotently and block fulfillment for the expired reservation.
