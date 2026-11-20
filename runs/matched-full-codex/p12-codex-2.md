VERDICT: BLOCKED
### 1. [blocker] Missing beam can produce a false interval
- Failure: Without a deadline for each run, a later finish edge can pair with an unmatched start. After a full counter period, modulo subtraction can make that stale pair look valid.
- Fix: Expire and clear each unmatched start after 3 seconds. Accept a finish only while that run is active.

### 2. [major] Replay skips physical timing errors
- Failure: Replaying timestamp pairs checks the arithmetic but cannot detect beam sensor delays or differences in interrupt latency that could push the measured interval beyond the 2 ms error limit.
- Fix: Keep the replay tests and add end-to-end tests that break both beams at independently measured intervals, including 0.1 seconds, 3 seconds, and a counter wrap.
