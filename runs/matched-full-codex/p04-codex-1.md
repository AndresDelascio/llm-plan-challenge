VERDICT: BLOCKED
### 1. [blocker] Missing crop offset
- Failure: Step 4 feeds the calibration transform an x-coordinate 240 original-frame pixels too far left for every detection.
- Fix: Apply the transform to `(2u + 240, 2v)`.

### 2. [blocker] Mean error can hide a failing kick
- Failure: Step 5 can pass the swap even when a held-out kick exceeds 5 km/h absolute error.
- Fix: Pass only if the maximum absolute error across the seven held-out kicks is at most 5 km/h.
