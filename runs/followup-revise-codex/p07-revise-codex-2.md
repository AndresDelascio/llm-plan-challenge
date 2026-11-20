# Photoelectric timing gate prototype

## Brief

Measure between two beams with no more than 2 ms error over 0.1–3 seconds. Beam events use a shared 16-bit hardware counter with one tick per 0.1 ms. The device can be started at any counter phase.

## Implementation

1. Timestamp each beam at the interrupt edge and reject any run with a missing beam.
2. A synthetic replay harness produces labeled edge pairs and verifies the conversion from ticks to milliseconds.
3. Calculate the interval as `(second_tick - first_tick) mod 65,536`, times 0.1 ms, so that a counter rollover between the beams still gives the correct elapsed time (for example, tick 65,000 to tick 464 is 1,000 ticks, or 100 ms).
4. Use 100 random edge pairs for acceptance, drawing the start tick from 0 through 32,000 and intervals of 1,000 through 30,000 ticks.
5. Add deterministic replay cases for acceptance that cross rollover at the 1,000-tick and 30,000-tick interval limits, since the largest end tick in the random cases is 62,000 and never wraps.
