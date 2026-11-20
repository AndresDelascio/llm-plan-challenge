# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. Persist a reservation ID, its creation timestamp, an `open` state and a payment reference before calling the gateway.
2. Use a sandbox payment gateway. Test two concurrent shoppers against one remaining unit and a gateway that never returns a result.
3. Reserve with a single conditional storage update that succeeds only when enough stock exists. Record the reservation and stock update in the same transaction.
4. Resolve each reservation through competing conditional transitions out of the `open` state, so exactly one outcome wins:
   - **Paid:** payment success conditionally moves the reservation from `open` to `paid`. Fulfillment is allowed only if this transition wins.
   - **Released:** every release, whether from a decline or from expiry, goes through one transaction that restores stock only when it successfully closes an `open` reservation. A retried decline, or a decline racing expiry, therefore cannot return the same units twice.
5. Release declined reservations immediately through the release transaction in step 4.
6. Expire unresolved reservations with a restart-safe job that scans persisted `open` reservations, independent of the payment worker and of any in-flight gateway call.
   - The job closes reservations through the release transaction in step 4.
   - Its expiry deadline is set earlier than five minutes after creation, leaving enough margin for scheduling and retries so stock is released within the five-minute limit even after a worker crash or a hung gateway call.
7. Keep reconciling expired reservations whose payment state is unknown until the payment reaches a terminal state.
   - Use gateway notifications or durable polling, keyed by the persisted payment reference.
   - If a late payment succeeds, the paid transition fails because the reservation is no longer `open`. Refund the payment idempotently and block fulfillment for the expired reservation.
