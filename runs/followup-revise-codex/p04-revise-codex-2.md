# Camera swap for a soccer shot tracker

## Brief

Achieve at most 5 km/h absolute error on each held-out kick after a 1920×1080 camera feed is cropped to 1440×1080 and resized to 720×540. The calibration transform accepts original-frame pixel coordinates. Reference speeds come from a separately timestamped timing gate.

## Implementation

1. Record 10 new kicks and use the first 3 solely for setup. Evaluate the other 7 with the settings frozen.
2. The crop begins at original x=240, y=0. The detector operates on resized crop coordinates (u,v).
3. Use decoded presentation timestamps in seconds. Associate each shot with the gate reading by event ID.
4. Apply the transform to (240 + 2u, 2v).
5. Pass the camera swap only if every one of the seven held-out kicks has an absolute error of at most 5 km/h.
