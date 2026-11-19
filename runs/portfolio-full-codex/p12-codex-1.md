VERDICT: PROCEED WITH CHANGES
### 1. [major] Replay leaves hardware timing unverified
- Failure: Synthetic edge pairs can pass even if interrupt latency or counter clock error pushes real measurements beyond 2 ms.
- Fix: Add an end-to-end test with independently timed beam breaks at 0.1 s and 3 s under representative interrupt load.

### 2. [major] Missing finish can be paired with a later edge
- Failure: Without an explicit expiry, a run missing its finish can remain open. A finish arriving after a full 6.5536 s counter period can then appear to fall within the supported interval.
- Fix: Expire each pending start just after the 3 s measurement window, allowing for the 2 ms error budget, and discard subsequent finish edges until a new start.
