# Attendance sync after offline practice

## Brief

Support offline attendance with exactly one server-side session per locally created session. An acknowledgement may be lost, and reconnects can submit retries concurrently.

## Implementation

1. Generate one idempotency key (UUID) for each locally created session at creation time. Persist the session and its key in an on-device queue before showing the session as saved.
2. Send queued attendance batches after reconnect, reusing the same idempotency key on every retry of a session. The server acknowledges only after committing the result.
3. On the server, put a unique constraint on the session's idempotency key. Insert the session and write the deduplication record in a single transaction. On a key conflict, do not insert; return the original committed result as a success.
4. Delete a queued item on the client only after receiving the server acknowledgement for its key. Until then it stays queued and is retried with the same key.
5. In integration testing, simulate a lost acknowledgement and concurrent retry requests. Assert that exactly one server session exists per locally created session, that the retry receives the original result as a success, and that the queued item is removed after acknowledgement.
