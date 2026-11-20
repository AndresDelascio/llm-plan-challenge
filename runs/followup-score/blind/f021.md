# Photoelectric timing gate prototype

## Brief

Measure between two beams with no more than 2 ms error over 0.1–3 seconds. Beam events use a shared 16-bit hardware counter with one tick per 0.1 ms. The device can be started at any counter phase.

## Implementation

1. Timestamp each beam at the interrupt edge and reject any run with a missing beam.
   - Detect a missing second beam with a timeout armed on the first beam at 30,020 ticks (3 s plus the 2 ms tolerance). This is well inside the 6.5536 s counter period, so an over-range interval cannot alias into the valid range.
   - Reject the run if the timeout fires before the second beam arrives.
2. A synthetic replay harness produces labeled edge pairs and verifies the conversion from ticks to milliseconds.
3. Calculate the interval as the wrap-safe modular difference `(uint16_t)(end - start)` times 0.1 ms.
   - This is unambiguous because the maximum interval of 30,000 ticks is below the 65,536-tick counter period.
   - Reject any result outside 980–30,020 ticks (0.1–3 s widened by the 2 ms tolerance, so valid runs at the range limits are not discarded).
4. Use 100 random edge pairs for acceptance in the replay harness, drawing the start tick from 0 through 65,535 and intervals of 1,000 through 30,000 ticks.
   - Pass criterion: each pair's computed interval is within 20 ticks (2 ms) of its labeled interval.
   - Add forced wrap-straddling cases, such as start 60,000 with interval 30,000 and start 65,535 with interval 1,000.
   - Add explicit boundary cases at exactly 1,000 and 30,000 ticks, each with and without a wrap.
   - Add rejection cases: no second beam, an interval above 30,020 ticks (including one above 65,536 ticks, such as 7 s), and an interval below 980 ticks.
5. Verify the 2 ms error on hardware, since the synthetic replay checks only the arithmetic.
   - Drive both beam inputs from a reference pulse generator at 0.1 s, 1 s and 3 s.
   - Repeat the runs at varied counter phases, including ones that straddle a wrap.
   - Assert that every measured interval is within 2 ms of the reference.
