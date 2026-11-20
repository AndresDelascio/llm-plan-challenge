# Attendance sync after offline practice

## Brief

Support offline attendance with exactly one server-side session per locally created session. An acknowledgement may be lost, and reconnects can submit retries concurrently.

## Implementation

1. Persist a queue on-device before showing a session as saved.
2. Send queued attendance batches after reconnect. The server acknowledges only after committing the result.
3. Simulate a lost acknowledgement and concurrent retry requests during integration testing.
4. Generate one UUID per local session when the session is created and persist it in the queue with the session. Reuse the same UUID on every send, and retain it in the attempt log.
5. On the server, add a unique constraint on the local session UUID in the session table. Atomically insert the session or return the existing session by UUID, with no separate deduplication write.
