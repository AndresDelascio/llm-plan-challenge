# Camera swap for a soccer shot tracker

## Acceptance criterion

Pass if the tracker returns one valid speed for each of the seven held-out kicks and every estimate differs from its timing-gate reference by at most 5 km/h. Compare unrounded values.

## Setup

1. Record 10 consecutive kicks with unique event IDs shared by the video and timing-gate logs. Use kicks 1–3 for setup and keep kicks 4–10 and their reference speeds out of the setup process. Cover the intended speed range and shot paths in the recording.
2. Verify that the calibration maps original-frame pixels from the replacement camera to world coordinates in meters. Recalibrate if the camera position, lens settings, or image geometry invalidate the existing transform. Check the mapping against known points across the measurement area.
3. Crop the 1920×1080 frame at `(x=240, y=0)` to 1440×1080, then resize it to 720×540. Convert each detected ball center `(u, v)` back to original-frame coordinates before applying the calibration. Use `(2u+240, 2v)` if the detector and resize pipeline use edge-based coordinates. If integer coordinates denote pixel centers and the resizer uses half-pixel sampling, use `(2u+240.5, 2v+0.5)`. Verify the applicable convention with known points through the actual preprocessing pipeline.
4. Use decoded presentation timestamps converted to seconds. Estimate when the tracked ball crosses the two timing-gate planes by interpolating between detections that bracket each crossing. Compute speed over the same interval and with the same distance definition as the gate, then convert m/s to km/h by multiplying by 3.6. Match readings by event ID so the two devices can use independent clocks.
5. Use the three setup kicks to verify the coordinate mapping, timestamps, crossing estimates, and event matching. Freeze the calibration, preprocessing, detector and tracking settings, speed calculation, and validity rules before evaluating the held-out kicks.

## Held-out evaluation

6. Run kicks 4–10 through the frozen pipeline. For each kick, report the event ID, tracker speed, gate speed, absolute error, and pass/fail status. A missing or invalid speed or a missing or ambiguous gate match prevents the run from passing.
7. Apply the acceptance criterion to all seven kicks. If any settings change after reviewing the results, collect a fresh set of seven held-out kicks for the next acceptance run.
