# Attendance sync after offline practice

## Brief

Support offline attendance with exactly one server-side session per locally created session. An acknowledgement may be lost, and reconnects can submit retries concurrently.

## Implementation

1. Persist a queue on-device before showing a session as saved.
2. Send queued attendance batches after reconnect. The server acknowledges only after committing the result.
3. Simulate a lost acknowledgement and concurrent retry requests during integration testing. Assert that the retries leave exactly one session with one complete set of attendance records, and that each successful retry returns the same committed session.
4. Generate a stable session UUID once and persist it with the queued session. Send that same UUID on every retry.
5. Enforce a unique session UUID in storage. Write the session and its attendance atomically in one transaction. Return the existing committed session on duplicate UUID.
6. Remove the persisted queue entry after receiving a successful acknowledgement for its UUID, including a duplicate response that confirms the session committed.
