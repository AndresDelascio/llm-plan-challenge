VERDICT: PROCEED WITH CHANGES

### 1. No rule against re-running after a bad result
- Severity: major
- Claim: Nothing fixes how many attempts the ball click (or any per-video calibration) gets, or whether both runs share the same click.
- Why it matters: After step 5 shows a poor video, re-clicking until it scores well is tuning on reporting footage, and the off/on difference mixes in click variation.
- Fix: Add to step 1: one click/calibration attempt per video, made before any result is seen, reused for both runs, every run logged.

### 2. Pass line does not name the judged configuration
- Severity: major
- Claim: Step 5 produces two results (engine off, engine on), but step 1 has one pass line with no configuration attached.
- Why it matters: If one passes and one fails, the verdict gets chosen after seeing the data, so there is no single answer.
- Fix: State in step 1 that pass/fail is judged on engine on; engine off is reported for information only.

### 3. Outcome mix is left open
- Severity: major
- Claim: "A mix of goals, misses and woodwork" sets no counts, and the pass line is one pooled accuracy.
- Why it matters: At about 60 shots, the share of the analyzer's weakest outcome class can decide pass or fail, and the comparison with 92% is not like-for-like if the mix differs from the 369-shot set.
- Fix: Write minimum counts per outcome in step 1 and report right/wrong per outcome in step 6.

### 4. Three videos from one setup are not 60 independent shots
- Severity: major
- Claim: All sessions share one tripod placement, so a single calibration or framing problem hits every shot.
- Why it matters: The result measures one setup, not the position; one bad (or lucky) setup gives a verdict that would not repeat.
- Fix: Take the tripod down and set it up again between sessions, within the step 1 definition, and report per-session numbers.

### 5. Thresholds are ambiguous at the real shot count
- Severity: minor
- Claim: The outcome denominator (all labelled shots or only found kicks) and "1 false kick per 50" at about 60 shots are undefined.
- Why it matters: 50 right with 57 found is 88% of found kicks but 83% of 60 shots, so the reading chosen afterwards flips the verdict.
- Fix: Write each threshold in step 1 as a formula on the labelled-shot count, with rounding.
