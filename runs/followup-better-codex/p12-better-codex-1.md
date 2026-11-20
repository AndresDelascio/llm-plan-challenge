# Photoelectric timing gate prototype

## Requirements

Measure the time from the first beam break to the second over 0.1–3.0 seconds, with an absolute error of at most 2 ms per valid run. Both beams share a 16-bit hardware counter with a nominal tick period of 0.1 ms. A run may begin at any counter value.

## Implementation

1. Capture the counter value on the beam-break edge for each input. Use hardware input capture where available and read the latched value in the interrupt handler. If firmware reads the counter directly, measure the effect of interrupt latency and jitter on the interval.
2. Track each run as waiting for start, waiting for finish, or complete. Reject a finish before a start, retain the first start timestamp if another start edge arrives, and accept at most one finish per run. Clear pending captures and run state before rearming.
3. Expire a run if either required edge is missing. Use a separate arming timeout for a missing start. Set the finish timeout just beyond 3 seconds, with enough margin to accept a valid edge at the upper endpoint. Enforce it before the counter’s 6.5536-second wrap period elapses, even if no further edges arrive. Resolve finish-versus-timeout ordering using the captured edge time.
4. Compute `elapsed_ticks = (finish - start) mod 65536` using explicit unsigned arithmetic. Convert to milliseconds with `elapsed_ticks / 10.0` and preserve 0.1 ms resolution in the output.

## Verification and acceptance

1. **Replay.** Generate each finish count from a known elapsed tick count and start phase. Check the exact recovered tick count and the millisecond conversion at 1,000 and 30,000 ticks and at representative points between them. Cover a start count of zero, a finish count of zero, and pairs that cross wrap. Verify that missing, reversed, duplicate, and late edges produce the expected result, including a late finish whose wrapped count would otherwise appear valid.
2. **Hardware timing.** Drive both capture inputs with a calibrated pulse source at 100 ms, 3,000 ms, and intermediate intervals. Repeat at different counter phases, including across wrap, and under representative interrupt load. Compare each result against the independent reference to check counter accuracy and capture timing.
3. **Optical timing.** Repeat representative intervals with the actual beams and detectors. Use an independent reference for the physical beam-break times to include detector response and signal conditioning in the error measurement. Pass only if every valid hardware and optical trial has an absolute error of at most 2 ms, accounting for reference uncertainty, and every invalid trial produces no interval.
