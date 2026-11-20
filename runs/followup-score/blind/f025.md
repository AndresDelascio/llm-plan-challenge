# Photoelectric timing gate prototype

## Brief

Measure between two beams with no more than 2 ms error over 0.1–3 seconds. Beam events use a shared 16-bit hardware counter with one tick per 0.1 ms. The device can be started at any counter phase.

## Implementation

1. Timestamp each beam using hardware input capture on the shared counter, or an atomic 16-bit counter read if capture is unavailable. Latch the first edge on each beam and ignore later edges on that beam until the run resets. Reject any run with a missing beam.
2. A synthetic replay harness produces labeled edge pairs and verifies the conversion from ticks to milliseconds.
3. Calculate the interval as (finish − start) modulo 65,536, times 0.1 ms. This is only valid when the elapsed time is less than one full counter period (6.5536 s), so enforce the range:
   - After the start edge, count counter overflows (or run a timeout).
   - Reject any run whose elapsed time exceeds 3 s, including a finish edge that arrives after that limit.
   - Reject any run whose computed interval is below 0.1 s.
4. Use a fixed replay set and require each valid result to meet the reference error bound. The set covers:
   - crossing counter wrap
   - starting at zero
   - the minimum and maximum supported intervals
   - an interval over 3 s and one longer than a full counter period (e.g. 7 s), both of which must be rejected
   - an interval below 0.1 s, which must be rejected
   - repeated edges on one beam, where only the first edge counts
5. Run one hardware test that feeds both beam inputs from a reference pulse generator at 0.1 s and 3 s, and require each measured interval to be within 2 ms of the reference.
