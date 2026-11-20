# Photoelectric timing gate prototype

## Brief

Measure the time from the start beam to the stop beam with no more than 2 ms error, for intervals of 0.1–3 s. Both beam events are timestamped by one shared 16-bit hardware counter at 0.1 ms per tick. The counter wraps every 65,536 ticks (6.5536 s), and the device may be started at any counter phase, so a measurement can straddle a wrap.

## Error budget (2 ms = 20 ticks total)

- **Quantization:** up to ±1 tick (0.1 ms).
- **Clock accuracy:** 2 ms over 3 s is about 667 ppm. Use a crystal-derived tick source; an uncalibrated internal RC oscillator (typically about 1%, or 30 ms over 3 s) breaks the budget on its own.
- **Capture latency:** use hardware input capture if the counter supports it. If the ISR reads the counter instead, bound the worst-case latency and the latency mismatch between the two channels.
- **Sensor response:** use matched sensors on both beams so that response delays cancel. Measure the residual mismatch.

## Implementation

1. **Capture.** Timestamp each beam at its interrupt edge from the shared counter. Assign fixed roles: beam A is start and beam B is stop. Accept only the first edge per beam per run, so that chatter is ignored.
2. **Interval calculation.** Compute `ticks = (uint16_t)(t_stop - t_start)`, which is unsigned subtraction modulo 65,536, and `interval_ms = ticks * 0.1`. This is correct across a wrap at any start phase, because the maximum valid interval of 30,000 ticks is less than 65,536. Do not use the absolute difference: it gives wrong results whenever the counter wraps between the beams.
3. **Run validation.** Reject a run and report the reason if any of these occurs:
   - A beam is missing.
   - B arrives before A.
   - The stop does not arrive within a timeout of about 3.2 s after the start. Enforce this independently of the modular difference, for example with an overflow or compare interrupt, because intervals longer than 6.5536 s would otherwise alias into valid-looking results.
   - The computed interval falls outside 1,000–30,000 ticks.
4. **Replay harness.** Build a synthetic harness that feeds labeled edge pairs (start tick, true interval) through the production interval and validation code, not only the tick-to-ms conversion. It should check both the accepted values and the rejections.

## Acceptance

1. **Random synthetic tests.** Run at least 1,000 edge pairs, since they are cheap. Draw the start tick uniformly from the full range 0–65,535 and the interval from 1,000–30,000 ticks. The original start range of 0–32,000 never produced a wrap (the maximum stop tick was 62,000), so it could not catch the main failure mode.
2. **Directed synthetic cases.**
   - Start ticks 0, 65,535, and 65,535 minus interval plus or minus 1, so the stop lands on or just past the wrap.
   - Intervals of 1,000 and 30,000 ticks (the boundaries), each with and without a wrap.
   - Rejection cases: missing start, missing stop, reversed order, intervals of 999 and 30,001 ticks, timeout, and an interval longer than 65,536 ticks that must not alias.
3. **Synthetic pass criterion.** Every accepted result must be exact in ticks, and every invalid run must be rejected.
4. **Hardware check.** Drive both beam inputs from a reference pulse generator, or compare against a scope or logic analyzer. Use intervals across 0.1–3 s, for example 0.1, 0.5, 1, 2, and 3 s, with repeated trials at uncontrolled counter phase so that some straddle a wrap. Every measurement must be within 2 ms of the reference.
