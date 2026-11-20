VERDICT: BLOCKED
### 1. [blocker] A failed upload can stall until the next reconnect
- Failure: If an upload fails before the server commits and the device stays online, the plan gives the queued session no retry trigger. It can remain saved locally with zero server-side sessions.
- Fix: Retry unacknowledged entries with backoff while online, using the same UUID.

### 2. [minor] Acknowledged sessions stay queued
- Failure: The plan never clears acknowledged entries, so later reconnects can resend sessions that already synced.
- Fix: Remove each entry from the durable queue after receiving a successful acknowledgement for its UUID, including a duplicate response that confirms the existing commit.
