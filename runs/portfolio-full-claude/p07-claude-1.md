VERDICT: BLOCKED

### 1. [blocker] Absolute difference breaks on counter wrap
- Failure: The 16-bit counter wraps every 6.5536 s and the device can start at any phase, so a wrap between beams is routine. With start 60,000 and a 30,000-tick interval, the end reads 24,464 and step 3 reports 3.55 s instead of 3.0 s.
- Fix: Compute `(end − start) mod 65536` as unsigned 16-bit subtraction, with beam order taken from which beam fired first.

### 2. [major] Acceptance test never exercises a wrap
- Failure: Start ticks of 0–32,000 plus intervals of at most 30,000 peak at 62,000, below 65,536. The suite therefore passes with the step 3 bug in place.
- Fix: Draw the start tick from 0–65,535 and add fixed cases at 0.1 s and 3 s that straddle the wrap.

### 3. [major] No timeout defines a "missing beam"
- Failure: A second beam arriving after more than 6.5536 s aliases into the valid range (7 s reads as about 0.45 s) and is accepted as a real result.
- Fix: Reject the run if the second edge has not arrived within a fixed window just over 3 s, such as 3.2 s.

### 4. [major] The 2 ms requirement is never tested on hardware
- Failure: The synthetic harness checks only the tick-to-millisecond arithmetic. Sensor response time, interrupt latency and clock error go unmeasured.
- Fix: Add a bench test that drives both inputs from a reference pulse generator across 0.1–3 s.

### 5. [minor] `abs()` hides reversed beam order
- Failure: A run where beam 2 triggers first gives a plausible positive interval.
- Fix: Reject runs where the edges arrive in the wrong order.
