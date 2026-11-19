VERDICT: PROCEED WITH CHANGES
### 1. [major] Late finish can pass as a valid interval
- Failure: If the gate keeps waiting after a missing finish, an edge 6.6536 seconds after the start decodes as 100 ms.
- Fix: Expire the pending run after the maximum supported interval, with a small measurement margin, and clear it before a full counter period elapses.

### 2. [major] Replay leaves the hardware error unverified
- Failure: Synthetic tick pairs can pass even when differential interrupt latency or counter clock error pushes real measurements outside the 2 ms bound.
- Fix: Drive both beam inputs with independently timed edges and verify the 2 ms bound at the supported endpoints under expected interrupt load.
