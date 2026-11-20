VERDICT: BLOCKED
### 1. [blocker] Payment success can race with expiry
- Failure: A success handler can read an open reservation, then authorize fulfillment after expiry releases the units and another shopper reserves them.
- Fix: Require an atomic transition from reserved to paid before authorizing fulfillment. Refund the payment idempotently if expiry wins.
### 2. [blocker] A reservation can release stock twice
- Failure: A retried decline or a decline racing with expiry can increment stock twice, allowing later orders to reserve units that do not exist.
- Fix: Use one transaction for both release paths that restores stock only if it successfully changes the reservation from reserved to closed.
### 3. [blocker] The release deadline can be missed
- Failure: Polling can stop if the order worker crashes or stall if a gateway status call hangs, leaving stock reserved past five minutes.
- Fix: Persist the release deadline and use a restart-safe expiry job that runs independently of gateway calls.
### 4. [major] A late charge can go undetected
- Failure: If the gateway drops the response and polling ends at expiry, a successful charge may never trigger a refund.
- Fix: Keep reconciling expired reservations with unknown payment outcomes until the gateway reports a terminal result.
