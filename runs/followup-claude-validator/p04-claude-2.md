VERDICT: BLOCKED

### 1. [blocker] Crop offset dropped in coordinate mapping
- Failure: Step 4 feeds (2u, 2v) to the transform, but the crop starts at original x=240, so every point lands 240 px left of its true original-frame position. With a perspective calibration, this distorts distances and speeds, and tuning on the three setup kicks may mask the error rather than fix it.
- Fix: Apply the transform to (2u + 240, 2v).

### 2. [blocker] Pass criterion weaker than the goal
- Failure: Step 5 passes on mean absolute error ≤ 5 km/h across seven kicks, while the brief requires ≤ 5 km/h on each held-out kick. A run with errors such as 1, 1, 1, 1, 1, 1, 12 km/h would pass while violating the goal.
- Fix: Pass only if the maximum absolute error across the seven kicks is ≤ 5 km/h.
