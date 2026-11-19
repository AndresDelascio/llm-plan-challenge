VERDICT: BLOCKED
### 1. [blocker] Counter rollover corrupts elapsed time
- Failure: If the counter wraps between beams, the absolute difference gives the wrong interval. A run from tick 65,000 to tick 464 lasts 100 ms but reports 6,453.6 ms.
- Fix: Compute `(second_tick - first_tick) mod 65,536`, then multiply by 0.1 ms.

### 2. [major] Acceptance tests exclude rollover
- Failure: The largest generated end tick is 62,000, so all 100 cases can pass with the rollover bug still present.
- Fix: Add deterministic replay cases that cross rollover at the 1,000- and 30,000-tick interval limits.
