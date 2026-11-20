# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. Record a reservation ID and its creation timestamp before calling the gateway. Take the timestamp from the database clock. Pass the reservation ID to the gateway as both the idempotency key and the payment reference, so an unknown payment can be queried and refunded and a retry cannot double-charge.
2. Use a sandbox payment gateway. In every case, assert that stock is never inflated and never oversold. Test these cases:
   - two concurrent shoppers against one remaining unit
   - a gateway that never returns a result
   - a decline
   - a decline that arrives after expiry, and a retried decline
   - a payment that succeeds after expiry
3. Reserve with a single conditional storage update that succeeds only when enough stock exists. Record the reservation and stock update in the same transaction.
4. Release and reconcile as follows:
   - **Single release path:** Route every release (decline, expiry or retry) through one conditional open→closed transition in the same transaction as the stock increment. A release that finds the reservation already closed does nothing.
   - **Declines:** Release declined reservations immediately through that path.
   - **Deadline:** Poll unresolved payments by reservation ID against a deadline computed from the creation timestamp on the database clock. Choose the deadline and sweep interval so that deadline plus one sweep interval plus processing time stays under five minutes.
   - **Expiry:** At the deadline, close expired reservations and release their stock through the same path.
   - **Late results:** After expiry, keep reconciling closed reservations by poll or webhook until the gateway reports a final state. If a late payment succeeds, refund it idempotently and block fulfillment for the expired reservation.
