VERDICT: PROCEED WITH CHANGES

### 1. [major] Accuracy is never verified on real hardware
- Failure: The synthetic replay harness only checks the tick-to-millisecond arithmetic. Counter clock error, capture latency and sensor response delay are never measured, so the prototype can pass every test and still miss the 2 ms bound. An uncalibrated 1% RC oscillator alone gives 30 ms error at 3 s; the budget is about 667 ppm.
- Fix: Add one bench test that drives both beam inputs from a reference pulse generator at 0.1 s and 3 s and requires no more than 2 ms error. Specify a crystal-grade clock source for the counter.

### 2. [minor] Out-of-range intervals are silently reported as valid
- Failure: The modulo arithmetic is correct for 0.1–3 s (30,000 ticks against a 65,536-tick period). But step 3 only assumes the elapsed time is under one period (6.5536 s) and nothing enforces it. A 7 s gap, such as a late finish beam, reports as about 0.45 s. Results between 3 s and 6.55 s are also accepted.
- Fix: Count counter overflows, or add a timeout after the start edge, and reject any run outside 1,000–30,000 ticks. Add one replay case above 6.5536 s that must be rejected.
