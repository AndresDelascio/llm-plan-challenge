VERDICT: BLOCKED

### 1. [blocker] Crop offset dropped in coordinate mapping
- Failure: Step 4 feeds (2u, 2v) to a transform that expects original-frame pixels. The crop starts at x=240, so every point lands 240 px too far left. Under a perspective calibration this distorts field positions and distances, so speeds are wrong on every kick.
- Fix: Apply the transform to (2u + 240, 2v).

### 2. [blocker] Pass criterion does not match the goal
- Failure: Step 5 passes on mean absolute error ≤ 5 km/h across the seven kicks, but the brief requires ≤ 5 km/h on each held-out kick. One kick with a large error can be averaged away and the swap still passes.
- Fix: Pass only if the maximum absolute error across the seven kicks is ≤ 5 km/h.
