VERDICT: BLOCKED
### 1. [blocker] Calibration drops the crop offset
- Failure: Applying the transform to `(2u, 2v)` places every detection 240 original-frame pixels too far left.
- Fix: Apply the transform to `(2u + 240, 2v)`.

### 2. [blocker] Mean error can hide a failed kick
- Failure: The mean can be at most 5 km/h even when one or more held-out kicks exceed the 5 km/h limit.
- Fix: Pass only if the maximum absolute error across the seven held-out kicks is at most 5 km/h.
