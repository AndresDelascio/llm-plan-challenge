# Photoelectric timing gate prototype

## Brief

Measure the time between two beam breaks with no more than 2 ms error, for intervals from 0.1 to 3 seconds. Both beams are timestamped from a shared 16-bit hardware counter with one tick per 0.1 ms, so it wraps every 6.5536 s. The device can be started at any counter phase.

## Error budget (2 ms total)

- **Quantization:** up to ±0.1 ms (one tick).
- **Edge capture latency:** must be bounded and roughly equal for both beams. The target is 0.5 ms or less of mismatch.
- **Clock accuracy:** 2 ms over 3 s is about 650 ppm. A crystal or resonator meets this. A typical internal RC oscillator at 1% or more gives up to 30 ms of error at 3 s and does not.

## Implementation

1. **Clock source.** Drive the counter from a source of 500 ppm or better, or calibrate it against one. Record which source is used. Replay testing cannot catch this error.

2. **Edge capture.**
   - Timestamp each beam with hardware input capture where available.
   - Otherwise read the counter first thing in the ISR, atomically on 8-bit MCUs, with the same code path for both beams.
   - Accept only the first start edge, then the first finish edge after it. Ignore repeat edges and any finish edge that arrives before a start.

3. **Interval calculation.** Compute `(finish − start) mod 65,536 × 0.1 ms` using unsigned 16-bit subtraction. This is correct for any start phase, provided the true elapsed time is under one counter period.

4. **Timeout and range rejection.** The modulo result alone cannot tell a 0.2 s interval from a 6.7536 s one.
   - Arm a timeout at the start edge. Use a compare match at start + 30,000 ticks plus a small margin, or an overflow count.
   - If no finish edge arrives before the timeout, abort the run and report "no finish / over range". This covers both a missing beam and intervals long enough to alias.
   - Also reject any computed result outside 0.1–3 s.
   - Never report a number for a rejected run.

5. **Synthetic replay harness.**
   - Generate edge pairs from a true interval and a start phase.
   - Run them through the same calculation and rejection code as the firmware.
   - Take the expected value from the true interval, not from the modulo formula.

6. **Fixed replay set.** Each valid case must be within the error bound. Each invalid case must be rejected, not reported.
   - **Valid:** 0.1 s and 3.0 s, at start phases 0, 65,535, and one that makes the interval cross the wrap.
   - **Valid:** a finish landing exactly on 0, and a mid-range interval with no wrap.
   - **Valid:** a sweep of start phases at a fixed interval.
   - **Rejected:** intervals just under 0.1 s and just over 3.0 s.
   - **Rejected:** aliasing intervals of 6.6 s, 6.7536 s (which looks like 0.2 s), and 10 s.
   - **Rejected:** a missing finish, a missing start, a finish before start, and duplicate edges on either beam.

7. **Hardware check.** Feed both inputs from a signal generator or a second calibrated timer.
   - Use known intervals of 0.1 s, 1 s, and 3 s, repeated at arbitrary phases.
   - Confirm the error stays under 2 ms end to end.
   - Confirm the timeout fires on a withheld finish pulse.
