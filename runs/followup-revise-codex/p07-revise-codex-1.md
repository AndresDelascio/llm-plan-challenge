# Photoelectric timing gate prototype

## Brief

Measure between two beams with no more than 2 ms error over 0.1–3 seconds. Beam events use a shared 16-bit hardware counter with one tick per 0.1 ms. The device can be started at any counter phase.

## Implementation

1. Timestamp each beam at the interrupt edge and reject any run with a missing beam.
2. A synthetic replay harness produces labeled edge pairs and verifies the conversion from ticks to milliseconds.
3. Calculate the interval as `(finish_tick - start_tick) mod 65536`, times 0.1 ms, so that runs crossing counter rollover are measured correctly.
4. Use 100 random edge pairs for acceptance, drawing the start tick from 0 through 32,000 and intervals of 1,000 through 30,000 ticks.
5. Add a deterministic acceptance pair that crosses rollover: start tick 65,000 and finish tick 464 must report 100.0 ms.
6. Verify the 2 ms error limit end to end, since replay bypasses beam detection and timestamp capture. Trigger real beam interruptions timed by an independent reference at the 0.1 s and 3 s endpoints, and require the reported interval to be within 2 ms of the reference at both.
