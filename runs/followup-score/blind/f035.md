# Attendance sync after offline practice

## Brief

Support offline attendance with exactly one server-side session per locally created session. An acknowledgement may be lost, and reconnects can submit retries concurrently.

## Implementation

1. Generate a stable session UUID once, when the session is created on-device, and persist it with the queued session. Send that same UUID on every retry.
2. Persist the queue on-device before showing a session as saved.
3. Enforce a unique session UUID in server storage. Write the session and its attendance atomically in one transaction. On a duplicate UUID, including a unique-constraint violation raised when concurrent requests race, return the existing committed session instead of an error.
4. Send queued attendance batches after reconnect. The server acknowledges only after committing the result. The client removes a session from the queue only after receiving an acknowledgement; otherwise it keeps the session and retries with the same UUID.
5. Simulate a lost acknowledgement and concurrent retry requests during integration testing. In both cases, verify that exactly one session and one set of attendance records exist on the server, and that every retry receives the committed session.
