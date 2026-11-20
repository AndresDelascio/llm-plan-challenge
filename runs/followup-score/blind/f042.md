# Camera swap for a soccer shot tracker

## Brief

Achieve at most 5 km/h absolute error on each held-out kick after a 1920×1080 camera feed is cropped to 1440×1080 and resized to 720×540. The calibration transform accepts original-frame pixel coordinates. Reference speeds come from a separately timestamped timing gate.

## Implementation

1. **Coordinate mapping.** The crop begins at original x=240, y=0, and the detector operates on resized crop coordinates (u,v). Map each detection to the original frame as (2u+240, 2v) before applying the calibration transform.
2. **Timing.** Compute the time between detections from decoded presentation timestamps in seconds, not from frame counts or nominal frame rate. Convert the resulting speed to km/h (m/s × 3.6).
3. **Gate association.** Match each shot to its gate reading by event ID. Do not compare the two clocks, as they are separately timestamped.
4. **Recording and setup.** Record 10 new kicks. Use the first 3 solely for setup, then freeze all settings.
   - On a setup frame, confirm that a landmark at a known original-frame position maps back to within 1 px.
   - If the landmark shows a consistent half-pixel offset from the resizer's pixel-centre convention, use (2u+240.5, 2v+0.5) instead.
   - Confirm that the first 3 kicks produce a speed and a matching gate reading.
5. **Evaluation.** Run the other 7 kicks once with the frozen settings. Record the tracker speed, gate speed and absolute error for each.
6. **Pass criterion.** Pass the camera swap only if all 7 kicks have an absolute error of at most 5 km/h. A held-out kick with no tracker speed or no gate reading counts as a fail; it is not excluded or replaced.
7. **On failure.** Do not retune on the 7 held-out kicks. Record a fresh set of 10 and repeat from step 4.
