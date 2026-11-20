# Camera swap validation for a soccer shot tracker

## Acceptance criterion

Each of the seven held-out kicks must have an absolute speed error of at most **5 km/h** against its matched timing-gate reading. A missing or invalid measurement prevents the run from passing. Report mean and maximum absolute error as summaries.

## Setup

1. Verify that the camera delivers 1920×1080 frames and that the calibration is valid for the replacement camera’s mounting, lens settings, and original-frame coordinates.
2. Confirm that preprocessing crops a 1440×1080 region starting at `(240, 0)` and resizes it to 720×540. Convert detector coordinates back to the original frame before applying the calibration transform. The mapping is `(x, y) = (240 + 2u, 2v)` under an origin-aligned convention. If preprocessing uses a pixel-center offset, invert that offset as well. Verify the mapping with known points.
3. Compute elapsed time from decoded presentation timestamps in seconds. Confirm that the timestamps used for speed estimation increase strictly and that the tracker measures speed over a region comparable to the timing gate’s measurement region. Match readings by unique event ID. Use timestamps within each device’s own clock unless the clocks have been synchronized.
4. Record 10 new kicks. Use the first three to verify the coordinate mapping, timestamp handling, gate pairing, and speed calculation. Freeze calibration, preprocessing, tracking settings, and the scoring procedure before examining results for the remaining seven.

## Held-out evaluation

5. For each of the seven held-out kicks, record the event ID, tracker speed, gate speed, and absolute difference in km/h. Flag missing or duplicate IDs, invalid timestamps, and failed tracks. Keep all seven kicks in the report.
6. Pass only if all seven kicks have valid paired measurements and every absolute difference is at most 5 km/h. Use unrounded values for the decision. If settings change after reviewing the results, validate again on a fresh held-out set.
