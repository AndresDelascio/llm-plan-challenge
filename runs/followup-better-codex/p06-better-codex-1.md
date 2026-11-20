# Inventory reservation during order processing

## Required behavior

Sell from one shared stock count without overselling. Return reserved units to available stock within five minutes of a payment decline or timeout, including when the gateway leaves the payment outcome unknown.

## Implementation

1. **Reserve stock atomically.** In one database transaction, decrement available stock only if it covers the requested quantity, then create the reservation with its ID, quantity, creation time, and payment deadline. Reject the order if the decrement affects no row. Use a unique checkout key so retries reuse the existing reservation. Commit before calling the gateway.

2. **Bound the payment attempt.** Use the reservation ID as the gateway idempotency key and set a finite payment deadline. Confirm payment only while the reservation is active and before its deadline. On a decline or timeout, release the reservation and restore its quantity in one transaction. Make confirmation and release conditional on the reservation still being active so concurrent handlers can apply only one transition.

3. **Recover missed releases automatically.** Run a recurring worker that releases expired reservations through the same transaction used by the payment handler. Set the worker cadence and retry budget so overdue units return to stock within five minutes of timeout, even if the checkout process exits. Monitor the age of unreleased reservations and alert before the five-minute limit is breached.

4. **Reconcile late payment results.** Track unknown payment outcomes separately so reconciliation can continue after stock is released. If the gateway later reports success for a released reservation, prevent fulfillment and void the authorization or refund the charge as appropriate. Make reconciliation and payment reversals idempotent.

## Verification

- Start two concurrent checkouts for the last unit. Verify that exactly one reserves it and that available stock never goes below zero.
- Simulate a gateway decline, a gateway that never responds, and a checkout process that exits before releasing stock. Verify that the units become available again within five minutes of the decline or timeout.
- Race payment success against release and replay checkout requests, callbacks, and worker jobs. Verify that stock is decremented or restored only once per reservation and that fulfillment requires a confirmed reservation.
- Report payment success after the released units have been reserved by a second shopper. Verify that the original order cannot be fulfilled, the second reservation remains valid, and the late payment is voided or refunded once.
