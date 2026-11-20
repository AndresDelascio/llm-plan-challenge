# Camera swap for a soccer shot tracker

## Brief

Achieve at most 5 km/h absolute error on each held-out kick after a 1920×1080 camera feed is cropped to 1440×1080 and resized to 720×540. The calibration transform accepts original-frame pixel coordinates. Reference speeds come from a separately timestamped timing gate.

## Implementation

1. **Confirm the geometry before recording.**
   - The crop begins at original x=240, y=0 and is 1440×1080. The resize to 720×540 is a uniform factor of 0.5.
   - The detector operates on resized crop coordinates (u,v).
   - Check that the calibration transform was made for the new camera in its current position, and re-calibrate if not.

2. **Map detections back to original-frame pixels.**
   - Apply the transform to (2u+240, 2v).
   - Sanity check: (0,0) maps to (240,0) and (720,540) maps to (1680,1080).
   - Mark a known landmark in both the original frame and the resized crop, and confirm they agree to within about 1 px.

3. **Compute speed.**
   - Use decoded presentation timestamps in seconds for each frame, not frame index divided by nominal fps.
   - Speed is transformed distance divided by PTS difference, taken over the part of the flight where the gate measures.
   - Convert to the gate's units (m/s × 3.6 = km/h) before comparing.

4. **Match to the reference.**
   - Associate each shot with its gate reading by event ID.
   - Never match by timestamp, because the gate and camera clocks are separate.

5. **Record and evaluate.**
   - Record 10 new kicks.
   - Use the first 3 solely for setup (detector thresholds, measurement window).
   - Freeze all settings, then evaluate the other 7 once.
   - Decide before recording which is which, and do not replace or drop kicks afterwards.
   - A held-out kick with no detection or no gate reading counts as a failure.

6. **Pass criterion.**
   - Pass the camera swap only if all seven held-out kicks have an absolute error of at most 5 km/h.
   - Report the per-kick errors, not just pass or fail.
   - If any kick fails, fix the cause and repeat with a fresh set of 10 kicks; do not re-tune on the seven.
