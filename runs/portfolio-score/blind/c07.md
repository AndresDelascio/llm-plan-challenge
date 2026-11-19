VERDICT: BLOCKED

### 1. [blocker] Hardware timing error is unverified
- Failure: Synthetic replay checks the conversion but cannot show that the physical gate meets the 2 ms bound. Clock drift and, if interrupt handlers read the counter, differences in interrupt latency can exceed the error budget.
- Fix: Specify hardware capture at both edges and verify the physical gate against an independent timing reference. Include counter clock accuracy in the 2 ms budget.

### 2. [major] Late finish can alias to a valid interval
- Failure: If a run remains armed for a full counter period after the start, a late finish can produce a valid-looking result. For example, 6.6536 seconds wraps to 100 ms.
- Fix: Expire the run at the supported deadline, allowing for the maximum interval’s timing tolerance, and discard finish events after expiry.
