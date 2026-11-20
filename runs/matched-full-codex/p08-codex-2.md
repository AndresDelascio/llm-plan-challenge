VERDICT: BLOCKED

### 1. [blocker] Retries use a different deduplication key

- Failure: If an acknowledgement is lost, the retry sends a new UUID. The server treats it as a new request and creates a second session.
- Fix: Persist a UUID for each local session in the queue and reuse it on every retry.

### 2. [blocker] Deduplication and insertion are separate writes

- Failure: Concurrent retries can both pass the deduplication check and insert a session. A crash after insertion but before logging the UUID also allows a duplicate on retry.
- Fix: Store the stable UUID on the session under a unique constraint. Use an atomic insert-on-conflict operation and acknowledge the existing session when the UUID already exists.
