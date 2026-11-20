VERDICT: BLOCKED
### 1. [blocker] Retries use a new deduplication key
- Failure: If the server commits a session but its acknowledgement is lost, the retry sends a new UUID and can create a second session.
- Fix: Persist a UUID with each locally created session and reuse it on every retry.

### 2. [blocker] Session creation and deduplication are separate
- Failure: Concurrent requests can both pass the UUID check and insert a session. A crash after the insert can also leave a committed session without a deduplication record.
- Fix: Enforce a unique constraint on the session UUID and insert the session atomically under that constraint. On conflict, acknowledge the existing committed session.
