# Camera swap for a soccer shot tracker

## Brief

Achieve at most 5 km/h absolute error on each held-out kick after a 1920×1080 camera feed is cropped to 1440×1080 and resized to 720×540. The calibration transform accepts original-frame pixel coordinates. Reference speeds come from a separately timestamped timing gate.

## Implementation

1. Record 10 new kicks and use the first 3 solely for setup. Evaluate the other 7 with all settings frozen.
2. The crop begins at original x=240, y=0 and is downscaled by exactly 2 in both axes. The detector operates on resized crop coordinates (u,v).
3. Map detections back to original-frame coordinates before calibration: **(x, y) = (2u + 240, 2v)**.
   - The previous draft omitted the +240 crop offset, which would shift every point 240 px horizontally.
   - If the resize uses pixel-centre alignment, use (2u + 240.5, 2v + 0.5) instead. Pick the convention that matches the resize in use and keep it fixed.
4. Check the mapping on the 3 setup kicks: push a few known landmarks (e.g. a goalpost base or pitch marking) through detector coordinates → mapping → transform, and confirm they land at their known positions.
5. Use decoded presentation timestamps, converted to seconds using the stream time base, for the ball's frame-to-frame timing. Do not use frame index ÷ nominal fps.
6. Associate each shot with its gate reading by event ID. The gate clock and video clock are separate, so never compare their timestamps directly; compare only the resulting speeds.
7. Compute absolute error in km/h for each of the 7 held-out kicks.
8. **Pass the camera swap only if every one of the 7 kicks has absolute error ≤ 5 km/h**, i.e. the maximum error is ≤ 5 km/h. A mean of ≤ 5 km/h is not sufficient, because the brief sets a per-kick limit.
9. Report the per-kick errors, the maximum and the mean. If any kick fails, do not retune on the held-out kicks; record a fresh set before re-evaluating.
