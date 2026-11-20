# Photoelectric timing gate prototype

## Brief

Measure the time between two beam breaks with no more than 2 ms error over intervals of 0.1–3 seconds. Beam events are timestamped from a shared 16-bit hardware counter with one tick per 0.1 ms. The device can be started at any counter phase.

## Key constraint

The counter wraps every 65,536 ticks (6.5536 s). Because the device can start at any phase, a valid interval of up to 30,000 ticks can straddle the wrap. The interval calculation and the tests must both handle this.

## Implementation

1. **Capture.** Latch the counter value for each beam at the interrupt edge, using hardware input capture if available and otherwise reading the counter first thing in the ISR. Record which beam fired.
2. **Interval calculation.** Compute `ticks = (uint16)(t_second − t_first)`, i.e. subtraction modulo 65,536, then `interval_ms = ticks × 0.1`.
   - Do not use an absolute difference, which gives wrong results whenever the counter wraps between the beams.
   - If the beams can fire in either order, determine order from interrupt arrival, not by comparing timestamp magnitudes.
3. **Run validation.** Reject a run when:
   - The second beam has not arrived within a timeout of about 3.2 s after the first. Track the timeout independently of the raw 16-bit value (e.g. by counting overflows or using a separate timer). Otherwise an interval longer than 6.5536 s aliases to a short, plausible-looking one.
   - The computed interval falls outside 1,000–30,000 ticks.
   - The same beam fires twice before the other; either ignore the re-trigger or reject the run, and document which.
4. **Synthetic replay harness.** Feed labeled edge pairs (first timestamp, second timestamp, expected interval) through the same calculation and validation code used on the device. Check wrap handling, rejection logic and the conversion from ticks to milliseconds.

## Acceptance

1. **Deterministic boundary cases** (must match exactly):
   - Intervals of exactly 1,000 and 30,000 ticks.
   - Start ticks of 0, 65,535, and values that put the second edge just before, exactly at, and just after the wrap (e.g. start 65,000 + interval 1,000; start 40,000 + interval 30,000).
   - Rejections: missing second beam, interval of 999 ticks, interval of 30,001 ticks, and an interval over 65,536 ticks, which must be rejected by timeout and not reported as a short interval.
2. **Random cases.** Draw 1,000 edge pairs with the start tick uniform over the full 0–65,535 range and intervals of 1,000–30,000 ticks, so roughly a quarter of pairs cross the wrap. Use a fixed, logged seed for reproducibility.
3. **Pass criterion.** In replay, every computed interval equals the labeled interval exactly, since the synthetic data has no physical jitter. This sits well inside the 2 ms (20 tick) budget.
4. **Hardware sanity check.** Drive both beam inputs from a signal generator or a second microcontroller at known intervals (e.g. 0.1 s, 1 s, 3 s), with the device powered up at arbitrary times. Confirm that the measured error stays within 2 ms, including on runs that cross a counter wrap.
