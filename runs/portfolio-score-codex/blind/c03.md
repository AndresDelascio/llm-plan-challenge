VERDICT: BLOCKED

### 1. [blocker] Retries use different deduplication keys

- Failure: After a lost acknowledgement, the retry sends a new UUID, so the server inserts a second session.
- Fix: Generate one UUID per local session and persist it in the queue. Reuse it on every send.

### 2. [blocker] Deduplication and session creation are separate writes

- Failure: Concurrent retries can both pass the lookup and insert sessions. A crash after the session insert can also leave no deduplication record.
- Fix: Add a unique constraint on the local session UUID in the server’s session table. Atomically insert or return the existing session by UUID.
