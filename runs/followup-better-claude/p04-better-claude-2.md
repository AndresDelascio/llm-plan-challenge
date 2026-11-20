# Camera swap for a soccer shot tracker

## Brief

Achieve at most 5 km/h absolute error on **each** held-out kick after a 1920×1080 camera feed is cropped to 1440×1080 and resized to 720×540. The calibration transform accepts original-frame pixel coordinates. Reference speeds come from a separately timestamped timing gate.

## Implementation

1. **Record and split.** Record 10 new kicks. Use the first 3 solely for setup. Evaluate the other 7 with all settings frozen (crop, coordinate mapping, detector parameters, calibration transform).

2. **Pipeline geometry.** The crop begins at original x=240, y=0 and is 1440×1080. It is resized to 720×540, a uniform scale of 0.5 on both axes. The detector operates on resized crop coordinates (u,v).

3. **Map detections back to original-frame coordinates.** Undo the resize first, then the crop offset:
   - x = 2u + 240
   - y = 2v

   Apply the calibration transform to (2u + 240, 2v), not (2u, 2v). Leaving out the 240 px offset shifts every point horizontally before the transform, which distorts speeds.

   Refinement: if the detector reports pixel-centre coordinates and the resize is centre-aligned, the exact mapping is x = 2u + 240.5, y = 2v + 0.5. Check which convention the resize library uses and apply it consistently.

4. **Check the mapping on the setup kicks.** Before using the 3 setup kicks for anything else:
   - Confirm each decoded frame is 720×540.
   - Pick a known landmark, such as a calibration marker or pitch line intersection.
   - Confirm its detected (u,v) maps to within about 1 px of its position in the original 1920×1080 frame.

5. **Timing.** Use decoded presentation timestamps in seconds for the camera-side speed calculation. Compute speed only from camera timestamp differences. The gate clock is separate, so never mix gate and camera timestamps in one calculation. Associate each shot with its gate reading by event ID.

6. **Compute errors.** For each of the 7 held-out kicks, compute |tracker speed − gate speed| in km/h. Check that units are consistent (m/s × 3.6 = km/h).

7. **Pass criterion.** Pass the camera swap only if every one of the 7 held-out kicks has absolute error ≤ 5 km/h, i.e. the maximum error is ≤ 5 km/h. A mean of ≤ 5 km/h is not enough.
   - Report the per-kick errors, the maximum and the mean.
   - A held-out kick with a missed detection or no matching gate reading counts as a failure. Do not drop it.
   - If the test fails, do not retune on the 7 held-out kicks. Record a new held-out set after any change.
