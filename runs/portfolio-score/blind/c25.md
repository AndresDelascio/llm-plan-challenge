VERDICT: BLOCKED

### 1. [blocker] New UUID per send defeats deduplication
- Failure: Step 4 generates a fresh request UUID on every send, so a retry after a lost acknowledgement carries an ID the server has never seen. The session is inserted again, violating exactly-once.
- Fix: Generate one idempotency key per locally created session at creation time, persist it in the queue with the session, and reuse it on every retry.

### 2. [blocker] Non-atomic check, insert, then log
- Failure: Step 5 checks, inserts and records the UUID as separate operations. Concurrent retries both pass the check and both insert. A crash between insert and log write also leaves a session with no dedup record.
- Fix: Put a unique constraint on the session's idempotency key and do the insert and dedup record in one transaction; on conflict, return the original result.

### 3. [major] Duplicate retries have no defined response
- Failure: The plan does not say what the server returns when it detects a duplicate. If it returns an error, the client never clears the queued item and retries indefinitely.
- Fix: Return the original success acknowledgement for a known key, and have the client dequeue only on that acknowledgement.

### 4. [minor] Tests lack a stated assertion and come before the logic
- Failure: Step 3 simulates lost acknowledgements and concurrent retries but states no pass condition, and is ordered before the dedup work.
- Fix: Move it last and assert exactly one server session per local session.
