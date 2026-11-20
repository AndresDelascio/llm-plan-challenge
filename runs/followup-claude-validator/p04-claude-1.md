VERDICT: BLOCKED

### 1. [blocker] Crop offset missing from the coordinate mapping
- Failure: Step 4 applies the transform to (2u, 2v), but the crop begins at original x=240. Every point is therefore 240 px too far left in the original frame, so the calibration transform gives wrong positions and speeds on every kick.
- Fix: Apply the transform to (2u+240, 2v).

### 2. [blocker] Pass criterion is weaker than the goal
- Failure: Step 5 passes on mean absolute error ≤ 5 km/h across the seven kicks, but the brief requires ≤ 5 km/h on each held-out kick. One kick could be off by 15 km/h and the swap would still pass on the mean.
- Fix: Pass only if the maximum absolute error across the seven held-out kicks is ≤ 5 km/h.
