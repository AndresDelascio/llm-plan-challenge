# Photoelectric timing gate prototype

## Brief

Measure between two beams with no more than 2 ms error over 0.1–3 seconds. Beam events use a shared 16-bit hardware counter with one tick per 0.1 ms. The device can be started at any counter phase.

## Implementation

1. Timestamp each beam at the interrupt edge. The first edge on either beam starts the run. Reject the run as a missing beam if the other beam's edge has not arrived within 3.2 s (32,000 ticks) of the first. Time this window with a compare on the same counter, so that a late edge cannot alias past the 6.5536 s wrap into the valid range.
2. A synthetic replay harness produces labeled edge pairs and verifies the conversion from ticks to milliseconds.
3. Calculate the interval as `(end − start) mod 65536` using unsigned 16-bit subtraction, times 0.1 ms. `start` is the timestamp of whichever beam fired first.
4. Run the synthetic acceptance set in the harness. Every accepted case must be within 2 ms of its labeled interval.
   - **Random pairs:** 100 edge pairs, with the start tick drawn from 0 through 65,535 and intervals of 1,000 through 30,000 ticks.
   - **Fixed wrap cases:** a 0.1 s interval that straddles the wrap (start 65,000, end 464) and a 3 s interval that straddles it (start 60,000, end 24,464).
   - **Timeout cases:** a run with no second edge and a run with the second edge at 7 s. Both must be rejected.
5. Bench-test the 2 ms requirement on hardware. Drive both beam inputs from a reference pulse generator at intervals across 0.1–3 s, including both endpoints. Every reading must be within 2 ms of the reference interval.
