# Attendance sync after offline practice

## Brief

Support offline attendance with exactly one server-side session per locally created session. An acknowledgement may be lost, and reconnects can submit retries concurrently.

## Implementation

1. Persist a queue on-device before showing a session as saved. Generate one UUID per locally created session at creation time and persist it with the queued session.
2. Send queued attendance batches after reconnect, reusing each session's persisted UUID on every send and retry. The server acknowledges only after committing the result.
3. Simulate a lost acknowledgement and concurrent retry requests during integration testing, and verify exactly one server-side session exists per locally created session.
4. Record each send in the attempt log against the session's UUID; never generate a new UUID for a retry.
5. On the server, store the session UUID on the session row under a unique constraint and insert atomically in a single write. If a row with the same UUID already exists, treat it as success and acknowledge without inserting again.
