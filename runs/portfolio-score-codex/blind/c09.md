VERDICT: BLOCKED
### 1. [blocker] Camera speed calculation is unspecified
- Failure: The plan produces transformed positions and timestamps but never defines how to turn them into a speed in km/h for each kick.
- Fix: Specify how to select the tracked samples, calculate distance over elapsed time in calibrated units, and convert the result to km/h.

### 2. [major] Event IDs do not align measurement intervals
- Failure: A correctly matched kick can exceed the 5 km/h threshold if the camera and gate measure different portions of the ball’s flight.
- Fix: Estimate camera speed over the gate’s measurement segment. If selecting that segment by time, align the two clocks first.

### 3. [minor] Coordinate mapping depends on the resize convention
- Failure: With half-pixel sampling and pixel-center coordinates, the stated inverse mapping is off by 0.5 original pixels on each axis.
- Fix: Use the actual resize convention and verify the inverse mapping with a known point.
