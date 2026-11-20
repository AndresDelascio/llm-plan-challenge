VERDICT: BLOCKED
### 1. [blocker] Calibration receives crop-relative coordinates

- Failure: Applying the transform to `(2u, 2v)` puts every detection 240 original-frame pixels too far left.
- Fix: Apply the transform to `(2u + 240, 2v)`.

### 2. [blocker] Mean error can hide a failed kick

- Failure: The swap can pass with a mean absolute error of 5 km/h or less even when an individual held-out kick exceeds 5 km/h.
- Fix: Pass only if the maximum absolute error across the seven held-out kicks is at most 5 km/h.
