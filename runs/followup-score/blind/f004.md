# Photoelectric timing gate prototype

## Brief

Measure between two beams with no more than 2 ms error over 0.1–3 seconds. Beam events use a shared 16-bit hardware counter with one tick per 0.1 ms. The device can be started at any counter phase.

## Implementation

1. Timestamp each beam with hardware capture.
   - The counter value is latched by the beam edge itself (input capture on both the start and finish channels), not read by software inside an interrupt handler. Interrupt latency therefore does not enter the measurement.
   - Reject any run with a missing beam.

2. Set an error budget for the 2 ms bound.
   - The budget covers counter clock accuracy over the full 3 s interval, the ±1 tick (0.1 ms) quantization, and any residual capture or sensor response difference between the two channels.
   - 2 ms at 3 s is about 667 ppm in total, so the clock source must have a tolerance comfortably inside that figure over the operating conditions.

3. Calculate the interval as (finish − start) modulo 65,536, times 0.1 ms.
   - This is valid only while the elapsed time is less than one full counter period (6.5536 s). Step 4 enforces that.

4. Expire the run at the supported deadline.
   - On the start edge, arm a deadline at start + 30,020 ticks (3 s plus the 2 ms tolerance), using a counter compare match or an equivalent mechanism that is guaranteed to fire before the counter wraps.
   - When the deadline fires, close the run as a missing finish beam.
   - Discard any finish edge that arrives after expiry, so a late finish cannot alias to a valid-looking interval (for example, 6.6536 s wrapping to 100 ms).

5. Build a synthetic replay harness.
   - It produces labeled edge pairs and verifies the conversion from ticks to milliseconds and the run-rejection logic.
   - It uses a fixed replay set that includes:
     - crossing counter wrap;
     - starting at zero;
     - the minimum and maximum supported intervals;
     - a finish just before and just after the deadline;
     - a finish more than one full counter period after the start (must be rejected, not reported as a short interval);
     - a missing finish.
   - Each valid result must meet the reference error bound, and each invalid run must be rejected.

6. Verify the physical gate against an independent timing reference.
   - The replay harness checks the arithmetic only, so the hardware is verified separately.
   - Measure the physical gate against a reference such as a calibrated pulse generator triggering both beams, or an oscilloscope or logic analyzer on the beam sensor outputs.
   - Cover the minimum, intermediate and maximum intervals, at arbitrary counter phases including runs that cross a wrap.
   - Require every measurement to be within 2 ms of the reference.
   - Confirm on hardware that a finish later than the deadline is rejected.
