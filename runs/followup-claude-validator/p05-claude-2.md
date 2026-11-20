VERDICT: PROCEED WITH CHANGES

### 1. [major] Release is not guarded against running twice
- Failure: An immediate decline release and the expiry sweep (or a duplicate decline callback) can both return the same units. This inflates the stock count and causes overselling.
- Fix: Route every release through one conditional open→closed transition that returns stock only if it wins.

### 2. [major] Payment confirmation can race with expiry
- Failure: Only expiry is atomic. A success arriving during the sweep can be fulfilled after its stock was released and resold.
- Fix: Confirm with the same compare-and-set on reservation state (open→confirmed), so the loser refunds.

### 3. [major] Late successes may never be detected
- Failure: Polling runs "against a deadline". After expiry nothing is stated to keep checking, so an unknown payment that later succeeds is never refunded.
- Fix: Send the reservation ID as the gateway idempotency key, void the payment at expiry, and keep reconciling until the gateway reports a terminal state.

### 4. [major] Five-minute budget is undefined
- Failure: The deadline's length and start point are unspecified. A five-minute deadline plus the sweep interval, or a crashed sweeper, releases stock late.
- Fix: Set deadline plus sweep interval below five minutes from the creation timestamp, use the database clock, and alert on overdue open reservations.

### 5. [minor] Tests miss the risky paths
- Failure: The two scenarios do not cover late success after expiry, duplicate release, or a crash between reservation and gateway call.
- Fix: Add one sandbox test for each.
