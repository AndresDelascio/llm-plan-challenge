VERDICT: PROCEED WITH CHANGES

### 1. Bar check never tried on real vendor data
- Severity: major
- Claim: The 390-bar, no-gap rule is tested only on synthetic data, and no real Twelve Data session has ever been fetched.
- Why it matters: If the free feed omits a minute or labels timestamps differently, every session fails from the first run, nothing is logged and step 9 is unreachable.
- Fix: Before scheduling, fetch one real pre-2026-11-17 session (download and check only) and confirm the bar count and timestamp convention.

### 2. A failed session can be overtaken by later ones
- Severity: major
- Claim: The plan does not say whether a session that fails its check blocks later sessions, yet some candidates carry a 14-session warm-up.
- Why it matters: If later sessions are logged over a hole, their never-recomputed rows rest on a history that changes when the hole is filled. If the vendor never supplies good bars, the session retries forever.
- Fix: Stop at the first failed session. Add a void row, written only with an explicit flag, for a permanently unavailable session.

### 3. "Wrong" is never checked, and partial writes count as logged
- Severity: major
- Claim: The status file reports only expected, logged and missing, and nothing makes a session's 12 rows atomic.
- Why it matters: A shutdown mid-write leaves a session with fewer than 12 rows. It then counts as logged, is never recomputed, and the status shows 0 missing.
- Fix: Write each session's 12 rows in one DuckDB transaction. Have the status flag any session without exactly 12 rows or with a raw file that no longer matches its hash.

### 4. A stale status file reads as healthy
- Severity: major
- Claim: The status file is regenerated only by a run that reaches step 7.
- Why it matters: If the task is disabled, Python fails to start or the script crashes early, the old file still shows 0 missing and only the last-run line hints otherwise.
- Fix: Write the status in a `finally` block. Put "calendar complete through <date>, generated <time>" on the top line so staleness is the first thing read.

### 5. Missed-start runs fire at bad moments
- Severity: minor
- Claim: A catch-up run can start at boot before the network is up, or mid-session the next day.
- Why it matters: Those runs fail and count toward the 3-failure flag, and the next retry may be a day away.
- Fix: Set the task's "start only if network available" and "restart on failure" options. Define "completed session" by exchange clock time after the close.
