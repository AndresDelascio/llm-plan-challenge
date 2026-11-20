VERDICT: BLOCKED
### 1. [blocker] Concurrent shoppers can oversell
- Failure: With one unit left, two shoppers can both pass the stock check before either decrement is written.
- Fix: Use one atomic conditional decrement that succeeds only when stock covers the requested quantity. Create the reservation in the same transaction.

### 2. [blocker] Gateway timeouts leave stock reserved indefinitely
- Failure: A gateway that never responds leaves units reserved past the five-minute deadline.
- Fix: Set a deadline from the reservation timestamp and automatically restore stock by that deadline with an atomic release that can run only once per reservation.

### 3. [blocker] Late payment success can confirm an order after stock is released
- Failure: Once timeout release is added, the gateway can report success after another shopper has reserved the released units.
- Fix: Confirm the order only if it atomically transitions an active reservation to confirmed. Void or refund a payment that succeeds after release.
