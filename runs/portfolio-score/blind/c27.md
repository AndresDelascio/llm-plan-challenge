VERDICT: BLOCKED

### 1. [blocker] Concurrent shoppers can oversell

- Failure: Two shoppers can both read one available unit and pass the stock check before either decrement is written.
- Fix: Use a single atomic decrement conditioned on sufficient stock. Call the gateway only if it succeeds.

### 2. [blocker] Timed-out reservations never release automatically

- Failure: If the gateway never returns, the reservation stays pending past the five-minute deadline. A late payment success can also arrive after the units have been released and sold.
- Fix: Automatically expire and release the reservation within five minutes of timeout, exactly once. Prevent fulfillment against an expired reservation and void or refund any late payment success.
