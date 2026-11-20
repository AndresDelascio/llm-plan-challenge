# Camera swap validation for a soccer shot tracker

## Acceptance criterion

Pass the camera swap only if all seven held-out kicks produce a valid tracker speed within 5 km/h of the corresponding timing-gate speed. Apply the threshold to unrounded values. A missing or invalid result prevents a pass.

## Setup and coordinate mapping

1. Record 10 new kicks with unique event IDs shared by the camera and timing gate. Use the first three kicks to verify the setup and tune the tracker. Keep the other seven kicks and their reference speeds out of setup.
2. Verify that the camera delivers 1920×1080 frames and that preprocessing crops a 1440×1080 region starting at original-frame coordinates `(240, 0)` before resizing it to 720×540. Confirm that the calibration is valid for the replacement camera’s mounted position and optics by checking known points in the original frame.
3. Convert each detected ball center from resized-crop coordinates `(u, v)` to original-frame coordinates before applying the calibration transform. For edge-based coordinates, use `(240 + 2u, 2v)`. If the detector uses integer-centered pixel coordinates and resizing uses half-pixel sampling, use `(240 + 2(u + 0.5) − 0.5, 2(v + 0.5) − 0.5)`. Verify the convention with known points passed through the actual preprocessing pipeline.
4. Use decoded presentation timestamps in seconds to calculate elapsed time between ball positions. Reject measurement intervals with missing or non-increasing timestamps. Match gate readings by event ID because the two systems have separate clocks. Verify during setup that the tracker measures speed over the same physical segment as the timing gate.
5. Freeze the calibration, coordinate mapping, detector settings, speed calculation, and validity rules before processing the seven held-out kicks.

## Held-out evaluation

6. Run all seven held-out kicks through the frozen pipeline. For each event ID, record the tracker speed, gate speed, and absolute error in km/h, or the reason a valid comparison could not be made.
7. Report all seven results and the maximum absolute error when all comparisons are valid. If any kick exceeds 5 km/h or lacks a valid comparison, record that the swap did not pass. If settings change after reviewing the results, validate the revised setup on a fresh held-out set.
