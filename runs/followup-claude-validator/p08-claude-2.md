VERDICT: BLOCKED

### 1. [blocker] New UUID per send defeats deduplication
- Failure: Step 4 gives every retry a fresh UUID. After a lost acknowledgement, the resend looks new to the server and creates a second session.
- Fix: Generate one idempotency key per local session at creation, persist it in the queue entry, and reuse it on every send.

### 2. [blocker] Server check, insert and log are not atomic
- Failure: In step 5, concurrent retries can both pass the check and both insert. A crash between the insert and the separate log write also lets the next retry duplicate.
- Fix: Put a unique constraint on the key and write the session and key in one transaction. On conflict, return the original result.

### 3. [major] Batch-level identity breaks if batches change
- Failure: A retry may regroup sessions into a different batch after reconnect. A batch-level key then no longer matches, and already committed sessions are inserted again.
- Fix: Deduplicate per session, not per batch, and return per-session results.

### 4. [major] Dequeue and duplicate-response behaviour unspecified
- Failure: The plan never says when queue entries are removed. If a duplicate is answered with an error, the client retries forever or drops data.
- Fix: Remove an entry only on acknowledgement, and have duplicates return success with the original session ID.

### 5. [minor] Test has no pass criterion
- Failure: Step 3 simulates the faults but asserts nothing, so duplicates could pass unnoticed.
- Fix: Assert exactly one server session per local session after the lost acknowledgement and concurrent retries.
