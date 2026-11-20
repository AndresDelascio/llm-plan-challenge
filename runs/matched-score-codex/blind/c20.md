VERDICT: PROCEED WITH CHANGES
### 1. [major] Retries depend on reconnects
- Failure: If a reconnect batch fails before the server commits and the device stays online, the plan defines no further attempt. A locally saved session can remain missing on the server.
- Fix: Retry timed-out or transiently failed submissions while online, using the same persisted UUID.

### 2. [minor] Acknowledged sessions stay queued
- Failure: The plan never clears acknowledged entries, so later reconnects can resend sessions that already synced.
- Fix: Remove each queue entry after receiving a successful acknowledgement for its UUID, including a response that returns the existing committed session.
