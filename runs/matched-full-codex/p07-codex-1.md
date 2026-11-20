VERDICT: BLOCKED
### 1. [blocker] Counter rollover corrupts valid intervals
- Failure: A run from tick 65,000 to tick 464 lasts 100 ms, but the absolute difference reports 6,453.6 ms.
- Fix: Subtract the first edge timestamp from the second modulo 65,536, then multiply by 0.1 ms.

### 2. [major] Acceptance tests exclude rollover
- Failure: The largest generated end tick is 62,000, so none of the 100 cases exercises rollover.
- Fix: Sample starts across the full 16-bit range and add a deterministic case that crosses rollover.

### 3. [major] Replay cannot verify end-to-end accuracy
- Failure: Synthetic timestamps bypass beam detection and interrupt timing, so acceptance can pass even if the prototype exceeds 2 ms error.
- Fix: Add hardware acceptance cases using independently timed beam interruptions at both interval limits and check the reported error against 2 ms.
