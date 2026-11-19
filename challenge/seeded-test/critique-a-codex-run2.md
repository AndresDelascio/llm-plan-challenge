VERDICT: BLOCKED

### 1. Battery life falls far short
- Severity: blocker
- Claim: Continuous operation at the stated 80 mA cannot deliver 90 days from a 2,600 mAh cell.
- Why it matters: At that draw, nominal capacity lasts about 32.5 hours; the required duration is 2,160 hours, before accounting for sensors and conversion losses.
- Fix: Use deep sleep, switched sensor power, and brief scheduled or user-triggered web access. Verify battery-side average current below approximately 1.2 mA, including all components.

### 2. Storage count is four times too small
- Severity: blocker
- Claim: The plan requires 8,640 readings per planter, or 34,560 values total, rather than 2,160 and 8,640.
- Why it matters: An array sized as specified fills after 22.5 days, preventing retention of the complete 90-day history.
- Fix: Allocate storage for 8,640 records containing four readings and a timestamp each, and verify the actual byte requirement fits available memory.

### 3. Parts exceed the budget
- Severity: blocker
- Claim: The listed parts cost C$112 against the C$80 limit.
- Why it matters: Purchasing the complete planned build exceeds the constraint by C$32 before any additional charges.
- Fix: Revise the complete parts list to fit C$80, including the enclosure and wiring, before purchasing.

### 4. A restart erases the history
- Severity: major
- Claim: The only copy of the accumulated readings is in volatile RAM.
- Why it matters: A brownout, crash, or reset during the run destroys all earlier readings, even if logging resumes within 30 minutes.
- Fix: Append readings to onboard nonvolatile storage and recover the existing history after restart.