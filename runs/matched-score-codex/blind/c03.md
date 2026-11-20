VERDICT: PROCEED WITH CHANGES

### 1. [major] Video speed calculation is unspecified
- Failure: Step 4 ends with transformed positions. Step 5 needs a video speed measured over the timing gate’s interval for each kick. Pairing by event ID alone can compare speeds from different parts of the same kick.
- Fix: Specify how to identify the gate interval in the video and compute speed from the transformed distance and elapsed presentation time over that interval.

### 2. [major] Calibration is unverified for the replacement camera
- Failure: Step 4 can produce incorrect distances if the swap changes the camera’s pose or optics. The coordinate conversion only accounts for cropping and resizing.
- Fix: Verify the transform against the replacement camera during setup and recalibrate if needed before freezing settings.
