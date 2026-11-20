VERDICT: BLOCKED

### 1. [blocker] Counter rollover corrupts elapsed time
- Failure: The absolute difference gives the wrong interval when the counter wraps between beams. A run from tick 65,000 to tick 464 lasts 100 ms but reports 6,453.6 ms.
- Fix: Subtract the earlier event’s timestamp from the later event’s timestamp modulo 65,536, then multiply by 0.1 ms.

### 2. [major] Acceptance tests never cross rollover
- Failure: The largest generated end tick is 62,000, so all 100 tests can pass while the device fails on runs that cross rollover.
- Fix: Add deterministic rollover cases at 100 ms and 3,000 ms and check each reported interval against the 2 ms error limit.
