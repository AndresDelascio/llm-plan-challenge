# Camera swap for a soccer shot tracker

## Brief

Achieve at most 5 km/h absolute error on each held-out kick after a 1920×1080 camera feed is cropped to 1440×1080 and resized to 720×540. The calibration transform accepts original-frame pixel coordinates. Reference speeds come from a separately timestamped timing gate.

## Implementation

1. Record 10 new kicks and use the first 3 solely for setup. Evaluate the other 7 with all settings frozen, including the coordinate mapping, segment selection, any clock alignment and the speed calculation.
2. The crop begins at original x=240, y=0. The detector operates on resized crop coordinates (u,v).
3. Use decoded presentation timestamps in seconds. Associate each shot with the gate reading by event ID.
4. Map detector coordinates back to original-frame pixels using the resize convention the pipeline actually uses, then apply the transform.
   - If (u,v) are pixel-center indices under half-pixel sampling, the mapping is (2u+240.5, 2v+0.5).
   - If the resize is origin-aligned with no half-pixel offset, the mapping is (2u+240, 2v).
   - During setup, verify the mapping with a known point: mark a feature at a known original-frame pixel, locate it in the resized frame, and confirm the inverse mapping returns the original coordinates.
5. Estimate camera speed over the same portion of the flight that the gate measures.
   - Select the tracked samples that fall within the gate's measurement segment, preferably by position in calibrated coordinates.
   - If the segment is selected by time, first align the camera and gate clocks during setup, for example with a shared sync event or an offset estimated from the 3 setup kicks.
6. Compute the camera speed for each kick.
   - Transform the selected samples to calibrated coordinates.
   - Compute the distance travelled across the segment in calibrated units and divide by the elapsed time between the corresponding presentation timestamps.
   - Convert the result to km/h (m/s × 3.6).
7. Pass the camera swap only if all seven kicks have an absolute error of at most 5 km/h between the camera speed from step 6 and the gate reading matched by event ID.
