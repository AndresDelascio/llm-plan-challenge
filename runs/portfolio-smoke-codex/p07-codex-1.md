VERDICT: BLOCKED

### 1. [blocker] Counter rollover corrupts elapsed time

- Failure: A run starting at tick 65,000 and ending at tick 464 lasts 100 ms, but the absolute difference reports 6,453.6 ms.
- Fix: Compute `(end_tick - start_tick) mod 65536` using the events in chronological order, then multiply by 0.1 ms.

### 2. [major] Acceptance tests exclude rollover

- Failure: The latest possible end tick is 62,000, so all 100 random cases can pass with the broken calculation.
- Fix: Sample starts across all 65,536 ticks and include a mandatory rollover case with a known expected duration.
