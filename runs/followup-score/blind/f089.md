# Inventory reservation during order processing

## Requirements

- Reserve from one shared stock count without overselling, even when shoppers check out concurrently.
- Return reserved units within five minutes of a payment decline or timeout, including when the gateway leaves the payment outcome unknown.
- Accept an order only when payment succeeds and its reservation is still active.

## Implementation

1. **Reserve stock atomically.** In one database transaction, decrement available stock with a conditional update that succeeds only if enough units remain, then create a reservation with the order ID, quantity, creation time, and expiration time. If the update affects no rows, return an out-of-stock result. Use a unique checkout idempotency key so retries reuse the same reservation. Commit before calling the gateway.
2. **Bound the reservation lifetime.** Use the reservation ID as the gateway idempotency key. Set a payment request deadline before the reservation expires, and schedule expiration early enough to leave time for cleanup retries within five minutes of reservation creation. Release immediately on an explicit decline or request timeout. Run a durable expiration worker to release overdue reservations if the request handler crashes or never receives a response.
3. **Make finalization and release mutually exclusive.** On confirmed payment, atomically move an active, unexpired reservation to committed and mark its order accepted. On release, atomically move the active reservation to released and restore its units in the same transaction. Guard both transitions on the current state so concurrent handlers, workers, and duplicate callbacks can commit or restore stock only once.
4. **Reconcile uncertain payments.** Persist payment reconciliation work when releasing a reservation with an unknown outcome. Use gateway status lookups and callbacks to resolve that outcome. If payment succeeds after the reservation has expired or been released, keep the order unaccepted and void the authorization or refund the charge. Retry reconciliation and compensation idempotently, and alert on unresolved payments or overdue releases.

## Verification

- With one unit left, run two simultaneous checkouts and verify that exactly one reserves it and stock never goes negative.
- Exercise explicit declines, gateway timeouts, and a checkout handler crash against the sandbox gateway. Verify that stock becomes available within the five-minute limit without manual intervention.
- Race payment success against expiration and replay checkout requests, gateway callbacks, and expiration jobs. Verify that stock is restored at most once, only a valid reservation can produce an accepted order, and any late successful charge is voided or refunded exactly once.
