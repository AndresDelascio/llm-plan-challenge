# Photoelectric timing gate prototype

## Acceptance criteria

Measure elapsed time from the start beam’s leading edge to the finish beam’s leading edge. For reference intervals from 100 ms through 3,000 ms inclusive, the reported interval must be within 2 ms of the reference at any initial counter phase. A run with a missing beam must produce no interval.

## Implementation

1. Capture both beam edges using the shared 16-bit hardware counter. Use hardware input capture where available so interrupt latency does not shift the timestamp. If the interrupt handler must read the counter, measure the worst-case difference in timestamp latency between the two channels.
2. On arming, clear stale capture flags and wait for the start edge. Ignore finish edges before the start and duplicate start edges after it. Accept the first finish edge after the start. Expire the run if either expected edge is missing. Use an arming timeout while waiting for the start and a finish deadline that leaves margin beyond 3,000 ms for measurement uncertainty but expires before the 6,553.6 ms counter period. Resolve finish-versus-timeout races using the captured edge time so a delayed interrupt cannot discard an on-time finish or accept a late one.
3. Compute `elapsed_ticks = (finish_tick - start_tick) mod 65,536` using explicit unsigned arithmetic. Report `elapsed_ticks × 0.1 ms`, preserving the 0.1 ms resolution. The finish deadline ensures that a late edge cannot appear valid after a full counter revolution.
4. Budget the 2 ms tolerance across tick quantization, counter clock error over 3 seconds, and channel-to-channel delay through the sensors and capture path. Use the resulting budget to set the required clock tolerance and timestamp latency limits.

## Verification

1. Replay labeled edge pairs with independently specified expected tick counts and times. Sweep all 65,536 start phases at 100 ms and 3,000 ms. Add cases around counter wrap, including a finish exactly at zero. Require exact tick counts and correct millisecond conversion.
2. Replay missing edges, a finish before the start, duplicate edges, edges at the finish deadline, and a late finish after a full counter revolution. Verify that each valid run reports exactly once, expired runs report no interval, and rearming cannot pair edges from different runs.
3. Verify the assembled gate against an independent timing reference with known uncertainty. Exercise both optical channels at the interval endpoints and representative intermediate intervals, including runs across counter wrap and under expected interrupt load. Require the absolute error plus reference uncertainty to stay within 2 ms for every run.
