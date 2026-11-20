VERDICT: BLOCKED

### 1. [blocker] New UUID per send defeats deduplication
- Failure: After a lost acknowledgement, the retry carries a different UUID, so the server sees a new request and inserts a second session.
- Fix: Generate one idempotency key per local session at creation, persist it in the queue, and reuse it on every send.

### 2. [blocker] Non-atomic check, insert, then log
- Failure: Concurrent retries both pass the check before either writes the key, so both insert. A crash between the insert and the log write also allows a later duplicate.
- Fix: Put a unique constraint on the key and write the session and key in one transaction.

### 3. [major] Duplicate response undefined
- Failure: If a deduplicated retry gets an error or no result, the client never learns the session committed, so it retries forever or shows a failure.
- Fix: On key conflict, return the original success result.

### 4. [major] Batch granularity and dequeue rule unspecified
- Failure: If batches are recomposed after reconnect, a batch-level key no longer matches. Removing queue entries before the acknowledgement loses sessions.
- Fix: Key each session individually and delete a queue entry only after its own acknowledgement.

### 5. [minor] Test has no pass criterion and precedes the mechanism
- Failure: Step 3 simulates the faults before steps 4–5 exist and asserts nothing, so duplicates can pass unnoticed.
- Fix: Move the test last and assert exactly one server row per local session.
