VERDICT: BLOCKED

### 1. [blocker] Payment success can race expiry
- Failure: If payment success and expiry run concurrently, fulfillment can proceed after the same units have been released and sold to another shopper.
- Fix: Make payment success and expiry competing conditional transitions from the same open state. Allow fulfillment only if the paid transition wins.

### 2. [blocker] Release depends on the payment worker staying alive
- Failure: If the worker crashes after reserving stock, or the gateway call hangs before polling starts, the reservation can remain open past five minutes.
- Fix: Run a restart-safe expiry job over persisted open reservations, with enough time for scheduling and retries before the five-minute limit.

### 3. [major] Late payment success can go undetected
- Failure: If polling ends when the reservation expires, a later gateway capture may never trigger the refund.
- Fix: Reconcile expired payments through gateway notifications or durable polling until the payment reaches a terminal state, using a persisted payment reference.

### 4. [major] Decline and expiry can both release stock
- Failure: A decline arriving as expiry runs, or a retried decline, can return the same units twice.
- Fix: Route every release through one transaction that restores stock only when it successfully closes an open reservation.
