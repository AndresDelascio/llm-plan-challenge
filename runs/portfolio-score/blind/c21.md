VERDICT: BLOCKED

### 1. [blocker] New UUID per send defeats deduplication
- Failure: Step 4 gives every retry a fresh request UUID, so after a lost acknowledgement the server sees the retry as a new request and creates a duplicate session.
- Fix: Generate one idempotency key per locally created session at creation time, persist it in the queue, and reuse it on every retry.

### 2. [blocker] Check-insert-record is not atomic
- Failure: Step 5 checks, inserts, then saves the UUID separately. Concurrent retries both pass the check and both insert; a crash between insert and log write also allows a duplicate later.
- Fix: Put a unique constraint on the session's idempotency key and do the insert and dedup record in one transaction, returning the existing result on conflict.

### 3. [major] Queue removal rule is unspecified
- Failure: The plan never says when a queued item is deleted. Removing on send loses sessions when the acknowledgement is lost; never removing causes endless resends.
- Fix: Delete a queued item only after receiving the server acknowledgement for its key.

### 4. [major] Duplicate response is undefined
- Failure: If a deduplicated retry returns an error or an empty reply, the client cannot tell it succeeded and keeps retrying or shows a failure.
- Fix: Return the original committed result, as a success, for a repeated key.

### 5. [minor] Test has no stated pass condition and runs before the fix
- Failure: Step 3 simulates faults but asserts nothing, and is ordered before steps 4 and 5.
- Fix: Move it last and assert exactly one server session per local session.
