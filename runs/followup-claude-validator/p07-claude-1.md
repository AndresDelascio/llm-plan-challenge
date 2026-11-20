VERDICT: BLOCKED

### 1. [blocker] Absolute difference breaks on counter wrap
- Failure: The 16-bit counter wraps every 6.5536 s (65,536 ticks) and can start at any phase. If it wraps between beams, `abs(t2 − t1)` is wrong: start 60,000 plus 30,000 ticks reads 24,464, giving 35,536 ticks instead of 30,000. This hits up to about 46% of 3 s runs.
- Fix: Compute `(uint16_t)(t2 − t1)`, which is correct for any interval under 65,536 ticks.

### 2. [blocker] Acceptance test cannot detect the wrap bug
- Failure: Start ≤ 32,000 plus interval ≤ 30,000 gives at most 62,000, so no test pair ever wraps and the suite passes with issue 1 present.
- Fix: Draw start ticks from 0–65,535 and add forced wrap cases (e.g. start 65,535, and start 40,000 with interval 30,000).

### 3. [major] Over-long intervals alias into valid results
- Failure: No timeout is defined for "missing beam". A second beam arriving after more than 6.55 s aliases to a plausible value (7 s reads as 0.446 s).
- Fix: Abort the run with a wrap-independent timeout shortly after 3 s, and reject results outside 1,000–30,000 ticks.

### 4. [major] 2 ms accuracy is never verified on hardware
- Failure: The synthetic harness only checks tick-to-ms arithmetic. Interrupt latency, sensor response and clock error are untested.
- Fix: Add a few physical runs against a reference timer or signal generator across 0.1–3 s.

### 5. [minor] Beam order and repeated edges are unhandled
- Failure: Reversed or repeated triggers produce silent wrong intervals.
- Fix: Enforce beam A then beam B, and ignore further edges once a beam is latched.
