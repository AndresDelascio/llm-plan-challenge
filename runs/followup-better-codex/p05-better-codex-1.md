# Inventory reservation during order processing

## Outcomes

- Concurrent orders cannot reserve more units than the shared stock count allows.
- A confirmed decline releases stock immediately. If payment remains unresolved, stock is released within five minutes of reservation creation, even if the gateway never responds.
- Each reservation releases stock at most once. Only an order with a confirmed payment and a committed reservation can enter fulfillment.

## Implementation

1. **Reserve stock before calling the gateway.** In one database transaction, decrement available stock with a conditional update that succeeds only if enough units remain, then create a pending reservation. Store the quantity, order attempt ID, payment reference, and a database-generated expiration time five minutes after creation. Enforce uniqueness on the order attempt ID so a retried checkout returns the existing reservation without reserving stock again. If stock is insufficient, reject the attempt without calling the gateway.

2. **Submit and reconcile payment using the same reference.** Use the stored reference as the gateway idempotency key for payment submission and retries. Treat a gateway timeout as an unknown outcome. Feed verified webhooks and payment status lookups through the same state transition logic. Recover interrupted submissions by reconciling against the stored reference.

3. **Make payment resolution and expiration atomic.** On confirmed success, commit the reservation and durably enqueue fulfillment in one transaction, provided the reservation is still pending and the database clock is before the deadline. On confirmed decline or expiration, close the pending reservation and restore its stock in one transaction. Only the transaction that changes the pending state may restore stock or enqueue fulfillment. A success processed at or after the deadline follows the expiration path.

4. **Release expired stock independently of the gateway.** Run a recurring worker that finds due reservations through an index on pending status and expiration time. Start expiration processing early enough to allow retries within the five-minute limit. Alert on overdue pending reservations and monitor the time from creation to release.

5. **Refund successful payments on closed reservations.** Continue reconciling closed reservations with unresolved payments until the gateway confirms an outcome. If a successful payment is discovered, durably enqueue a refund keyed by the gateway payment ID. Retry refunds with the same idempotency key until confirmed. Keep fulfillment blocked for the closed reservation throughout.

## Verification

- Run two concurrent checkouts against one remaining unit. Verify that exactly one reserves stock and only that attempt reaches the gateway. Retry the winning checkout and verify that it creates no additional reservation or charge.
- Exercise a confirmed decline and a gateway that never returns a result. Verify immediate release on decline and release within five minutes of creation for the unresolved payment. Verify that another checkout can reserve the released unit.
- Race payment success against expiration, including success processed at the deadline. Verify that a pre-deadline commit produces one fulfillment request and that expiration produces one stock release and a refund if payment succeeds.
- Replay webhook events and restart workers after payment submission, stock release, and refund submission. Verify that recovery creates no duplicate charge, stock release, fulfillment request, or refund.
