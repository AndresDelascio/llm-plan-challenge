# Photoelectric timing gate prototype

## Objective

Measure elapsed time from the start beam to the finish beam with an absolute error of at most 2 ms for intervals from 100 ms through 3,000 ms, inclusive, at any phase of the shared 16-bit counter. Each counter tick represents 0.1 ms.

## Implementation

1. Use hardware input capture to latch the counter value at each beam’s qualifying edge. Track which beam produced each capture and process events in capture order.
2. On arming, clear stale captures and wait for the start beam. Treat a finish edge before a start as an invalid run. After the start, retain its timestamp through any duplicate start edges and use the first qualifying finish edge. If either beam is missing when its wait expires, report an invalid run and rearm with fresh state.
3. Calculate `elapsed_ticks = (finish_tick - start_tick) mod 65536`, using unsigned 16-bit arithmetic or an explicit modulo operation that yields 0 through 65,535. Convert with `elapsed_ms = elapsed_ticks / 10.0`. The counter wraps every 6,553.6 ms, so every supported interval is unambiguous even when it crosses zero.
4. Set the finish timeout slightly beyond 3,000 ms to accommodate measurement uncertainty at the upper endpoint, and keep it below one counter period. Resolve timeout races using the captured edge time so delayed interrupt handling does not discard a timely finish.

## Verification and acceptance

1. Replay labeled edge pairs through the production event-handling and conversion logic. Generate each finish timestamp as `(start_tick + interval_ticks) mod 65536` and compare the reported interval with `interval_ticks / 10.0`, allowing only numerical rounding.
2. For both endpoint intervals, 1,000 and 30,000 ticks, choose starts that place the finish at 65,535, 0, and 1. Then replay 100 seeded random pairs with starts drawn from the full counter range, 0 through 65,535, and intervals drawn from 1,000 through 30,000 ticks. Verify invalid-run handling for missing beams and finish-before-start, timestamp retention on duplicate starts, and successful rearming after a timeout.
3. On the prototype, use a calibrated independent reference to measure the interval between physical beam interruptions. Test both endpoints and representative interior intervals, with repeated runs that cross the counter wrap and runs that stay within one counter cycle. Accept the prototype only if every valid trial is within 2 ms of the reference after accounting for reference uncertainty.
