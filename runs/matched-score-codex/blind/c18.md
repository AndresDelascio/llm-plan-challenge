VERDICT: PROCEED WITH CHANGES

### 1. [major] Missing finish can produce a valid-looking interval
- Failure: If the finish beam never fires, the plan gives no deadline for rejecting the run. If an unrelated edge arrives 6.6536 seconds after the start, the modulo calculation reports 100 ms.
- Fix: Expire the run after the 3-second measurement window and require a fresh start before accepting another finish.

### 2. [major] Replay skips physical timing errors
- Failure: Synthetic edge pairs can pass even when counter clock error or differences in beam detection and timestamp latency push the measured interval outside the 2 ms bound.
- Fix: Keep the replay tests and add an end-to-end check using independently timed beam interruptions at 0.1 and 3 seconds, with repeated trials under expected operating conditions.
