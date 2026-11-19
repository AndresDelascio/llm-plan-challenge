VERDICT: BLOCKED

### 1. Battery lasts about 1.5 days, not 90
- Severity: blocker
- Claim: Step 6 keeps Wi-Fi on at 80 mA, and 2,600 mAh / 80 mA is about 32 hours against the 2,160 hours required.
- Why it matters: The logger dies on day 2 of the balcony run; 90 days needs an average draw near 1.2 mA.
- Fix: Deep-sleep between readings, log with Wi-Fi off, and bring up Wi-Fi and the page only on a button-press wake (occasional time-server sync).

### 2. History lives only in RAM
- Severity: blocker
- Claim: Steps 4–5 hold the whole log in a memory array, which is erased by any reset, brownout or crash, and by the deep sleep that issue 1 requires.
- Why it matters: One glitch on day 60 loses everything, so the "no gap longer than 30 minutes" criterion fails.
- Fix: Append each reading to a file on the ESP32's flash (LittleFS) and serve the CSV from that file.

### 3. Standby draw from sensors and boards breaks the budget even with sleep
- Severity: major
- Claim: Step 2 powers the 4 sensors continuously from 3.3 V (typically about 5 mA each), and a dev board's regulator and USB chip plus the boost board draw several mA while asleep.
- Why it matters: Roughly 20+ mA of standby drains the cell in about 5 days regardless of firmware.
- Fix: Switch sensor power from a GPIO or transistor only during reads, and measure sleep current; if it is above about 0.5 mA, remove the board's power LED/regulator or choose a low-quiescent board. Use ADC1 pins (GPIO 32–39), since ADC2 fails while Wi-Fi is on.

### 4. Parts list exceeds the budget
- Severity: major
- Claim: Step 1 totals C$112 against the C$80 constraint.
- Why it matters: The plan breaks its own constraint before any build starts.
- Fix: Cut C$32, for example a cheaper sensor 4-pack and box, and drop the boost board (run the 3.3 V regulator directly from the cell).

### 5. Bench test never checks battery life, and the array size is wrong
- Severity: major
- Claim: Step 8 runs on USB, so power is untested, and step 5's count is off: 90 days is 8,640 readings per planter (34,560 values), not 2,160.
- Why it matters: The first battery evidence arrives as a failure on the balcony, and storage is sized 4x too small.
- Fix: Run the 48-hour test on the cell, measure average current with a multimeter, extrapolate to 90 days, and size storage for 8,640 rows.
