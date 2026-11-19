VERDICT: BLOCKED
### 1. [blocker] Calibration omits the crop offset
- Failure: Passing `(2u, 2v)` gives the calibration transform an x-coordinate 240 pixels left of the detected point in the original frame.
- Fix: Pass `(2u + 240, 2v)` to the transform.
### 2. [blocker] Mean error can hide a failing kick
- Failure: Seven kicks can average at most 5 km/h absolute error even when an individual kick exceeds 5 km/h.
- Fix: Pass only if the maximum absolute error across the seven held-out kicks is at most 5 km/h.
