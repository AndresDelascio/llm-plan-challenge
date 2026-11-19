VERDICT: BLOCKED
### 1. [blocker] Camera speed calculation is unspecified
- Failure: The transform and presentation timestamps produce positions and times, but the plan never defines how to turn them into a speed for each kick.
- Fix: Define how to select the ball samples and compute displacement in meters divided by elapsed presentation time, then multiply by 3.6.

### 2. [major] Camera and gate may measure different parts of the kick
- Failure: An event ID pairs readings from the same kick but does not ensure the camera measures speed over the gate’s measurement interval. Ball speed can change between the two measurements.
- Fix: Use the gate’s physical measurement boundaries to select the camera samples for the speed estimate.

### 3. [major] Calibration is unverified after the swap
- Failure: The crop mapping restores original-frame coordinates, but a change in camera pose or optics can invalidate the transform and bias all seven speeds.
- Fix: Verify the transform against known positions in the new camera’s original frame during setup and recalibrate if needed before freezing settings.
