# Photoelectric timing gate prototype

## Objective

Measure the elapsed time between two beam interruptions over 0.1–3.0 seconds, with absolute error no greater than 2 ms at any starting counter phase. Both beams use the same 16-bit hardware counter, which advances every 0.1 ms and wraps every 6.5536 seconds.

## Implementation

1. Capture the counter value at each beam’s active edge using hardware input capture. If the hardware only supports reading the counter in an interrupt handler, verify that the difference in interrupt latency between the two channels stays within the error budget under expected load.
2. When armed, use the first beam edge as the start and the first subsequent edge from the other beam as the stop. Determine order from the edge captures, even if interrupts are serviced out of order. Ignore repeat edges from the starting beam.
3. Calculate `elapsed_ticks = (stop_tick - start_tick) mod 65536` and report `elapsed_ticks × 0.1 ms`. The maximum interval of 30,000 ticks fits within a single counter period, so this calculation works across rollover.
4. After the first edge, expire the run using a hardware timer or monotonic deadline before a full counter period can elapse. Allow enough margin for a valid 3.0-second interval to be captured and processed. Report a timeout if the second beam is missing, and clear pending captures before rearming.

## Verification and acceptance

1. Replay labeled edge pairs with exact expected tick counts. Cover both beam orders, intervals of 1,000 and 30,000 ticks, stops immediately before, at, and after rollover, and starts at tick 65,535. Include duplicate edges, a missing second edge, a late edge after timeout, and a valid run after rearming. Require exact tick counts for valid pairs and no interval for timed-out runs.
2. Add 100 reproducible random cases. Draw start ticks from 0–65,535 and intervals from 1,000–30,000 ticks, both inclusive. Compute the stop tick as `(start_tick + interval_ticks) mod 65536`. Record the random seed and require exact results for every pair.
3. Verify end-to-end accuracy with controlled beam interruptions and an independent, calibrated time reference. Test both beam orders, the 0.1-second and 3.0-second endpoints, intermediate intervals, and runs that cross rollover under expected interrupt load. Accept only if every measured interval differs from the reference by at most 2 ms, accounting for reference uncertainty.
