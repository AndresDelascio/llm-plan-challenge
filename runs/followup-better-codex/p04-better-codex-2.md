# Camera swap for a soccer shot tracker

## Acceptance criterion

Pass only if all seven held-out kicks have a valid tracker estimate and an absolute error of at most 5 km/h against the timing gate. Use unrounded errors for the pass decision.

## Setup and calibration

1. Record 10 new kicks with unique event IDs shared by the video and timing gate logs. Use the first three kicks to check calibration, tracking, and timing. Reserve the remaining seven for evaluation.
2. Crop the 1920×1080 frame to 1440×1080 starting at `(240, 0)`, then resize it to 720×540. Convert each detected ball center `(u, v)` back to original-frame coordinates before applying the calibration transform. The inverse mapping is `(240 + 2u, 2v)` for edge-based coordinates. If the resizer uses half-pixel sampling and the detector reports integer-indexed pixel centers, use `(240 + 2(u + 0.5) - 0.5, 2(v + 0.5) - 0.5)`. Verify the convention with known points and confirm that the calibration is valid for the new camera.
3. Use decoded presentation timestamps in seconds to compute elapsed time between detections. Estimate speed from calibrated positions over the same flight segment measured by the gate. Match readings by event ID. If gate timestamps are needed to locate that segment in the video, establish the clock mapping during setup.
4. Freeze the calibration, coordinate mapping, tracking settings, speed calculation, and rules for missing or invalid measurements before opening the held-out results.

## Held-out evaluation

1. Run the frozen pipeline on all seven held-out kicks. For each event ID, report the tracker speed, gate speed, and absolute error in km/h, or record why the comparison is invalid.
2. Report the maximum absolute error and the number of kicks within 5 km/h. A missing or invalid comparison prevents a pass. If the pipeline changes after reviewing the results, evaluate the revised configuration on a fresh held-out set.
