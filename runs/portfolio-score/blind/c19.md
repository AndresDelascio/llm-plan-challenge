VERDICT: BLOCKED

### 1. [blocker] Crop x-offset dropped before calibration transform
- Failure: The crop starts at original x=240, so a detector point (u,v) maps to original-frame (2u+240, 2v). Step 4 feeds (2u, 2v), so every point is 240 px too far left. Because the transform expects original-frame pixels, a perspective calibration will then give wrong positions and speeds on every kick.
- Fix: Change step 4 to apply the transform to (2u+240, 2v).

### 2. [major] Pass criterion is weaker than the goal
- Failure: The brief requires at most 5 km/h absolute error on each held-out kick, but step 5 passes on the mean across the seven. A set with six kicks at 2 km/h and one at 20 km/h has a mean of about 4.6 and would pass while violating the goal.
- Fix: Change step 5 to pass only if the maximum absolute error across the seven kicks is at most 5 km/h.
