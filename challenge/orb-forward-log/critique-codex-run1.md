VERDICT: PROCEED WITH CHANGES

### 1. Partial sessions become permanent
- Severity: major
- Claim: Steps 1 and 5 use session presence as completion without requiring all 12 candidate results to be committed together.
- Why it matters: If a run stops after appending some candidate rows, subsequent runs skip that date, and the status can count it as logged despite missing results.
- Fix: Commit all 12 results atomically, require the exact candidate set before marking a session complete, and have status flag incomplete sessions.

### 2. Validated data is not bound to execution
- Severity: major
- Claim: The plan does not establish that the paper trader consumes the saved bars whose hash is recorded.
- Why it matters: If the existing script reads another cache or downloads again, fills can use different bars while the log attributes them to the validated snapshot; vendor revisions make this a concrete failure case.
- Fix: Explicitly route the saved snapshot into the trader and record the hash of the data it actually consumes.

### 3. Corrections have no authoritative version
- Severity: major
- Claim: Correction rows are appended without a rule determining which results feed session counts and cumulative scorings.
- Why it matters: After the first deliberate rerun, multiple results exist for the same candidate and session; summing the append-only log double-counts that session while missing-session counts can still look correct.
- Fix: Link each correction to the revision it supersedes and calculate both scorings from one effective result per candidate and session.