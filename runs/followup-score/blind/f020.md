# Photoelectric timing gate prototype

## Brief

Measure the time between two beam breaks with no more than 2 ms error over intervals of 0.1–3 s. Both beams are timestamped from one shared 16-bit hardware counter at 0.1 ms per tick, which wraps every 6.5536 s. The device can be started at any counter phase.

## Error budget (2 ms total)

- **Quantization:** up to ±0.1 ms (one tick) on the interval.
- **Clock accuracy:** 2 ms over 3 s is about 670 ppm in total, so the counter must run from a crystal or similar source (≤ 100 ppm, i.e. ≤ 0.3 ms at 3 s). An uncalibrated internal RC oscillator (typically 1% or worse, i.e. 30 ms at 3 s) would break the requirement on its own.
- **Capture latency and sensor mismatch:** the remainder, about 1.5 ms, covers any difference in response time between the two beam sensors and any timestamp latency.

## Implementation

1. **Capture.** Timestamp each beam edge from the shared counter, using hardware input capture where available. If timestamps must be read in software inside the ISR, bound the worst-case interrupt latency and include it in the budget.
2. **Run state machine.** Idle → armed → started → finished.
   - Accept only the first start edge, then the first finish edge after it.
   - Ignore repeated edges from the same beam (bounce, or a second object).
   - Reject a finish edge that arrives with no start.
3. **Timeout.** Abort the run as "missing finish beam" if no finish edge arrives within 3 s plus a small margin of the start. Drive this from a compare event on the same counter.
   - This is how a missing beam is detected.
   - It also prevents aliasing: without it, a real 7 s interval would wrap and read as a plausible 0.4464 s.
4. **Interval calculation.** Compute interval ticks as (finish − start) modulo 65,536, using unsigned 16-bit subtraction, and multiply by 0.1 ms. This is correct at any counter phase and across one wrap, because the timeout keeps elapsed time below one counter period.
5. **Range check.** Report a result only if it lies within 0.1–3 s; otherwise flag the run as out of range rather than reporting a number.

## Verification

6. **Synthetic replay harness.** Feed labelled edge sequences (counter values plus beam ID) through the state machine and the interval calculation, and compare against the known reference interval. The fixed replay set covers:
   - Start at counter zero, and start at arbitrary phases.
   - An interval that crosses the counter wrap.
   - The minimum (0.1 s) and maximum (3 s) intervals, plus values one tick inside and outside each limit.
   - A missing finish beam and a missing start beam, both of which must be rejected.
   - A real interval longer than 6.5536 s, which must be rejected by the timeout rather than reported as its aliased value.
   - Duplicate edges on either beam.

   Pass criteria: every valid case is within the error bound (within one tick here, since the replay has no clock or sensor error), and every invalid case is rejected with the correct reason.
7. **Hardware check.** The replay only proves the arithmetic and logic, so also drive both beam inputs from a reference pulse generator or a calibrated timer.
   - Test at 0.1 s, about 1 s and 3 s, with several repeats at random counter phases.
   - Require every reading to be within 2 ms of the reference.
   - Separately measure the response delay of each of the two sensors and confirm the mismatch fits the budget.
