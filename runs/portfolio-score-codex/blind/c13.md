VERDICT: BLOCKED
### 1. [blocker] Acceptance test can pass an out-of-tolerance kick
- Failure: A mean absolute error of at most 5 km/h can hide individual kicks with errors above 5 km/h.
- Fix: Pass only if all seven held-out kicks have absolute errors of at most 5 km/h.

### 2. [blocker] Calibration input omits the crop offset
- Failure: Applying the transform to `(2u, 2v)` places every detection 240 original-frame pixels left of its correct position.
- Fix: Apply the transform to `(240 + 2u, 2v)`.
