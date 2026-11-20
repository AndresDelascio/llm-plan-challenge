VERDICT: PROCEED WITH CHANGES
### 1. [major] Measurement intervals may differ
- Failure: Event IDs pair readings for the same kick, but a decelerating ball can have different average speeds over the tracker’s measurement interval and the gate interval.
- Fix: Compute tracker speed over the gate’s measurement interval using the elapsed video presentation timestamps.
### 2. [major] Calibration may be stale after the swap
- Failure: Restoring original-frame coordinates still gives incorrect field positions if the replacement camera changes the viewpoint or optics.
- Fix: Verify the transform against known field points during setup and recalibrate if needed before freezing settings.
### 3. [minor] Resize convention is unspecified
- Failure: If the resize uses half-pixel sampling and the detector reports pixel-center indices, the stated mapping is half an original pixel off on each axis.
- Fix: Match the inverse mapping to the resize and detector conventions. Under half-pixel sampling with pixel-center indices, use `(2u + 240.5, 2v + 0.5)`.
