# Photoelectric timing gate prototype

## Brief

Measure between two beams with no more than 2 ms error over 0.1–3 seconds. Beam events use a shared 16-bit hardware counter with one tick per 0.1 ms. The device can be started at any counter phase.

## Implementation

1. Timestamp each beam at the interrupt edge and reject any run with a missing beam. Expire each pending start just after the 3 s measurement window, allowing for the 2 ms error budget (3.002 s, or 30,020 ticks after the start edge). Once a start has expired, reject the run and discard subsequent finish edges until a new start arrives.
2. A synthetic replay harness produces labeled edge pairs and verifies the conversion from ticks to milliseconds.
3. Calculate the interval as (finish − start) modulo 65,536, times 0.1 ms. The allowed maximum elapsed time is less than one full counter period, and the expiry in step 1 ensures a finish arriving a full 6.5536 s counter period late is never paired with a stale start.
4. Use a fixed replay set that includes crossing counter wrap, starting at zero, and the minimum and maximum supported intervals. Require each result to meet the reference error bound.
5. Run an end-to-end hardware test with independently timed beam breaks at 0.1 s and 3 s under representative interrupt load. Require each measured interval to be within 2 ms of the independent reference, so that interrupt latency and counter clock error are covered as well as the tick conversion.
