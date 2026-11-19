VERDICT: BLOCKED

### 1. Battery life falls far short
- Severity: blocker
- Claim: Staying awake with Wi-Fi drawing about 80 mA cannot deliver 90 days on the specified cell.
- Why it matters: The simple capacity/current estimate is only 32.5 hours, versus 2,160 hours required; logging stops near the start of the deployment.
- Fix: Sleep between measurements, switch sensor power off between readings, and provide brief scheduled Wi-Fi access. Verify the complete system’s average battery current is below approximately 1.2 mA, with margin.

### 2. Storage is undersized by four
- Severity: blocker
- Claim: The required capacity is 8,640 readings per planter, or 34,560 sensor values total, plus timestamps.
- Why it matters: The planned array fills after 22.5 days; further readings must be discarded, overwrite earlier history, or exceed its bounds.
- Fix: Allocate storage for 8,640 complete timestamped records and verify its byte size against available memory while Wi-Fi and the web server are running.

### 3. Parts exceed the budget
- Severity: blocker
- Claim: The listed purchases total C$112, exceeding the C$80 constraint by C$32.
- Why it matters: The specified build cannot be purchased within the allowed budget, even before any additional charges.
- Fix: Revise the parts selection and quantities to total C$80 or less while retaining the required components and outdoor protection.

### 4. A reset erases the entire history
- Severity: major
- Claim: Keeping the only copy of the readings in RAM makes the accumulated history disappear on a reset or power interruption.
- Why it matters: A brief brownout or watchdog reset late in the deployment destroys earlier readings, preventing the final page and CSV from containing the full 90 days.
- Fix: Append records to the ESP32’s onboard nonvolatile storage and resume from the last complete record after restarting.