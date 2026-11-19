VERDICT: BLOCKED
### 1. [blocker] Payment success can race expiration
- Failure: A payment handler can approve fulfillment while expiration releases the same units for another order.
- Fix: Make payment acceptance and expiration competing atomic transitions from the open state. Allow fulfillment only if payment acceptance wins.

### 2. [major] A hung gateway call can delay stock release
- Failure: If polling starts only after the gateway call returns, a call that never returns can hold stock past five minutes. Request-local polling also stops if the process crashes.
- Fix: Have a durable worker expire open reservations independently of gateway calls, using the stored creation timestamp and a scan interval that leaves time to complete the release by the deadline.

### 3. [major] Late charges can go undetected
- Failure: If polling ends at expiration, a payment that succeeds afterward may never be detected or refunded.
- Fix: Send the reservation ID as a gateway correlation key and continue reconciling expired payments with unknown outcomes until they reach a terminal state.
