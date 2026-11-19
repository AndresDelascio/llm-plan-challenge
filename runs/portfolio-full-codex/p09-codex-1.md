VERDICT: BLOCKED
### 1. [blocker] No camera speed calculation
- Failure: Step 4 produces transformed positions, but the plan never defines how to turn them into a speed in km/h for step 5.
- Fix: Specify which ball observations to use, divide their calibrated distance in metres by their decoded timestamp difference in seconds, and multiply by 3.6.

### 2. [major] Calibration validity after the swap
- Failure: Mapping detections back to original-frame pixels corrects the crop and resize. If the replacement camera changes the viewing geometry, the existing transform can still return incorrect distances.
- Fix: Verify the transform against known field points in the replacement camera’s original frame during setup. Recalibrate if needed before freezing settings.

### 3. [major] Speed measurements may cover different intervals
- Failure: Event IDs pair readings to the same kick, but the camera and gate can measure different portions of the ball’s flight. A changing ball speed can then produce a discrepancy even when both measurements are accurate.
- Fix: Compute camera speed over the timing gate’s measurement segment.
