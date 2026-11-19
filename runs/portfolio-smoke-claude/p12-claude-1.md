VERDICT: PROCEED WITH CHANGES

### 1. [major] Over-range intervals alias to valid-looking results
- Failure: The counter wraps every 6.5536 s, and nothing enforces step 3's "less than one period" assumption. A 7 s crossing reports 0.4464 s. A finish beam that never fires has no timeout, so the "missing beam" rejection cannot trigger.
- Fix: Add a timeout armed at the start edge (for example, just over 3 s, or an overflow count). Abort the run on expiry and reject computed intervals outside 0.1–3 s.

### 2. [major] The 2 ms bound is only verified on synthetic data
- Failure: The replay harness checks tick-to-millisecond arithmetic only. It cannot detect counter clock error (2 ms over 3 s is about 667 ppm, which an RC oscillator can exceed), interrupt latency, or sensor response delay. The prototype could pass every test and still miss the brief.
- Fix: Add one hardware test: drive both beam inputs from a reference pulse generator at 0.1 s and 3 s, starting at arbitrary counter phases, and require error of 2 ms or less.

### 3. [minor] Timestamp capture method is unspecified
- Failure: If the ISR reads the counter in software, latency and masked interrupts add variable error. Repeated edges from one beam could also overwrite the timestamp.
- Fix: Use hardware input capture, latch the first edge per beam, and ignore further edges until the run is re-armed.
