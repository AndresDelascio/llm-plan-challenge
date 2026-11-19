VERDICT: BLOCKED
### 1. [blocker] Retries use different deduplication keys
- Failure: After a lost acknowledgement, the retry sends a new UUID, so the server creates a second session.
- Fix: Persist one UUID with each queued session and reuse it on every send.

### 2. [blocker] Session creation and deduplication are separate writes
- Failure: Concurrent retries can both pass the UUID check and insert a session. A crash after insertion but before logging the UUID also allows a duplicate on retry.
- Fix: Store the UUID on the session row under a unique constraint. Insert atomically and acknowledge an existing row with the same UUID as success.
