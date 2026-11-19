VERDICT: BLOCKED

### 1. Always-on Wi-Fi drains the cell in about 1.5 days
- Severity: blocker
- Claim: 2,600 mAh at 80 mA lasts about 32 hours, while 90 days (2,160 h) needs an average draw under roughly 1 mA.
- Why it matters: Logging stops on day 2 of 90, and the USB bench test in step 8 cannot reveal it.
- Fix: Deep-sleep between readings with Wi-Fi off, and serve the page only in a short window (for example a wake button). Measure average current on the cell before deploying.

### 2. History held only in RAM
- Severity: blocker
- Claim: The array is lost on any reset, brownout or deep sleep, and deep sleep is forced by issue 1.
- Why it matters: One reset in 90 days erases everything, so the "no gap longer than 30 minutes" criterion fails. Step 5 also undercounts: it is 8,640 readings per planter and 34,560 values in total, not 2,160 and 8,640.
- Fix: Append each reading to a flash file (LittleFS) and serve the CSV from it. Timestamp from the ESP32's RTC, resynced to the time server whenever Wi-Fi is up.

### 3. Parts list exceeds the budget
- Severity: major
- Claim: The step 1 prices total C$112 against a C$80 constraint.
- Why it matters: The plan breaks its own constraint before any work starts.
- Fix: Cut C$32, for example with cheaper sensors (about C$3–4 each from bulk sellers) and a cheaper enclosure. Otherwise raise the budget explicitly.

### 4. Standby draw of dev board, boost board and sensors
- Severity: major
- Claim: Even in deep sleep, a typical dev board (regulator, USB chip, LED), the boost converter and four always-powered sensors (about 5 mA each) draw tens of mA.
- Why it matters: After fixing issue 1, the run still ends in days to a couple of weeks rather than 90 days.
- Fix: Switch sensor power from a GPIO or transistor only while reading. Drop the boost board and feed a low-quiescent 3.3 V regulator, or pick a low-sleep-current board. Verify sleep current under about 0.3 mA.

### 5. Analog pin choice conflicts with Wi-Fi
- Severity: minor
- Claim: Step 2 does not specify the pins, and the ESP32's ADC2 pins give invalid readings while Wi-Fi is active.
- Why it matters: Sensors on those pins return garbage whenever the page is being served or the time is syncing.
- Fix: Use ADC1 pins only (GPIO 32–39).
