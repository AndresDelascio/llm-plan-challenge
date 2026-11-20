# Inventory reservation during order processing

## Goals

- Reserve units from one shared stock count without overselling, including when shoppers check out concurrently.
- Release units as soon as a payment decline is recorded. Give each reservation a hard expiry five minutes after creation so a gateway timeout cannot keep stock reserved indefinitely.
- Fulfill only orders whose payment success is recorded before the reservation expires. Refund any successful charge that arrives after the reservation closes.

## Implementation

1. **Reserve stock atomically.** In one transaction, decrement available stock only if it covers the requested quantity, then create a reservation with its order ID, quantity, creation time, and expiry. Use a stable checkout idempotency key so a retry returns the existing reservation without decrementing stock again. Call the gateway only after the transaction commits, using a stable payment idempotency key tied to the reservation.
2. **Apply payment outcomes through one state transition.** Route gateway responses, verified webhooks, and polling results through the same handler. In a transaction, use database time and a conditional state transition to confirm a pending reservation only before expiry, and enqueue fulfillment in that same transaction. For a definitive decline, close the pending reservation and restore its units in one transaction. Treat timeouts as unknown outcomes and reconcile them until expiry.
3. **Make expired units available at the deadline.** Run a durable expiry worker to close overdue pending reservations and restore their units atomically. Also reclaim overdue reservations in the stock allocation transaction under the same stock lock, so a delayed worker cannot make expired units unavailable to shoppers. Guard each transition so concurrent expiry, decline, and payment handlers cannot release stock twice or confirm an expired reservation.
4. **Reconcile payments after closure.** Keep tracking unknown payments after expiry. If a closed reservation has a successful charge, persist a refund job keyed by the charge ID and retry with a stable gateway refund idempotency key until confirmed. Alert on unresolved payments, overdue expiry work, and failed refunds.

## Verification

Use the gateway sandbox and controlled fault injection to verify that:

- Two concurrent shoppers competing for one unit produce exactly one reservation and one payment attempt.
- A definitive decline restores stock once, including when the gateway sends duplicate events.
- A gateway that never responds leaves the units available at the five-minute deadline, even when the expiry worker is paused.
- Payment success racing with expiry produces one valid outcome. A success recorded before expiry allows one fulfillment. A charge discovered after closure produces one refund and no fulfillment.
- Checkout retries, duplicate or out-of-order gateway events, and worker restarts do not double-decrement stock, double-release units, or duplicate charges, refunds, or fulfillment.
