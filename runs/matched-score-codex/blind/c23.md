VERDICT: BLOCKED
### 1. [blocker] A hung gateway can prevent expiry
- Failure: If polling depends on the gateway call returning, a hung call can hold stock past five minutes. The plan also leaves expiry recovery after a worker restart unspecified.
- Fix: Persist the expiry deadline in the reservation transaction and have a restart-safe worker release overdue reservations independently of the gateway call.

### 2. [blocker] Payment success can race with stock release
- Failure: A success handler can authorize fulfillment while expiry returns the same units to stock, allowing another shopper to buy them. A replayed decline can also release stock twice.
- Fix: Make payment success, decline, and expiry conditional transitions from the same pending state. Return stock in the transaction that wins a release transition, and authorize fulfillment only after the paid transition commits.

### 3. [major] Late payments can go undetected
- Failure: Polling ends at expiry, so a later successful charge can go unnoticed and unrefunded.
- Fix: Keep closed reservations with unknown payment outcomes in durable reconciliation until the gateway reports a terminal result. Retry any required refund with the same idempotency key.
