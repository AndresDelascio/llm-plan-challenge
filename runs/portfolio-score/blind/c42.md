VERDICT: BLOCKED

### 1. [blocker] Crop offset missing from coordinate mapping
- Failure: The crop starts at original x=240, so a detection at (u,v) corresponds to original pixel (2u+240, 2v). Step 4 feeds (2u,2v) into the calibration transform, so every point is 240 px too far left. Under a perspective transform this distorts distances and therefore speeds on every kick.
- Fix: Apply the transform to (2u+240, 2v).

### 2. [blocker] Pass criterion is weaker than the goal
- Failure: The brief requires at most 5 km/h absolute error on each held-out kick. Step 5 passes on the mean across the seven, so the swap can pass while individual kicks exceed 5 km/h (for example six kicks at 2 km/h and one at 20 km/h).
- Fix: Pass only if the maximum absolute error across the seven held-out kicks is at most 5 km/h.
