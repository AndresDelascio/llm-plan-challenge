VERDICT: BLOCKED
### 1. [blocker] Concurrent shoppers can oversell
- Failure: Two shoppers can both read one available unit and pass the stock check before either decrement is written.
- Fix: Use one atomic conditional decrement that succeeds only if enough stock remains. Call the gateway only after it succeeds.

### 2. [blocker] Timed-out reservations never release automatically
- Failure: If the gateway never responds, the reservation stays pending past five minutes. A late payment success can also arrive after the stock has been released and resold.
- Fix: Automatically expire and release the reservation within five minutes of timeout, exactly once. Prevent expired reservations from being fulfilled and void or refund any late successful payment.
