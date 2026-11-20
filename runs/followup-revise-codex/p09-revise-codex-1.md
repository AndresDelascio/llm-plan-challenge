# Camera swap for a soccer shot tracker

## Brief

Achieve at most 5 km/h absolute error on each held-out kick after a 1920×1080 camera feed is cropped to 1440×1080 and resized to 720×540. The calibration transform accepts original-frame pixel coordinates. Reference speeds come from a separately timestamped timing gate.

## Implementation

1. Record 10 new kicks and use the first 3 solely for setup. Evaluate the other 7 with the settings frozen.
2. During setup, verify the calibration transform against known field points in the replacement camera's original 1920×1080 frame. Recalibrate if needed before freezing settings.
3. The crop begins at original x=240, y=0. The detector operates on resized crop coordinates (u,v).
4. Use decoded presentation timestamps in seconds. Associate each shot with the gate reading by event ID.
5. Apply the transform to (2u+240,2v) to get calibrated ball positions in metres.
6. Compute the camera speed for each kick over the timing gate's measurement segment:
   - Use the ball observations that span that segment.
   - Divide their calibrated distance in metres by their decoded timestamp difference in seconds.
   - Multiply by 3.6 to get km/h.
7. Pass the camera swap only if all seven kicks have an absolute error of at most 5 km/h against the gate reading.
