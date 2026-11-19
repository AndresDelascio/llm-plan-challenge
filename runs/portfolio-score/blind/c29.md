VERDICT: PROCEED WITH CHANGES

### 1. [major] Queue entries never retire
- Failure: The client has no step to remove an acknowledged entry, so later reconnects can resend sessions that already synced.
- Fix: Remove the persisted queue entry after receiving a successful acknowledgement for its UUID, including a duplicate response that confirms the session committed.

### 2. [minor] Retry test lacks outcome assertions
- Failure: The integration test can simulate lost acknowledgements and concurrent retries without detecting duplicate sessions or attendance.
- Fix: Assert that the retries leave exactly one session with one complete set of attendance records, and that each successful retry returns the same committed session.
