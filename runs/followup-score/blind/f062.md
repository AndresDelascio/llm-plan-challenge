# Attendance sync after offline practice

## Brief

Support offline attendance with exactly one server-side session per locally created session. An acknowledgement may be lost, and reconnects can submit retries concurrently.

## Implementation

1. Generate one idempotency key (UUID) per locally created session at creation time.
2. Persist the session and its idempotency key in an on-device queue before showing the session as saved.
3. Send queued attendance batches after reconnect, reusing each session's persisted idempotency key on every send and retry. Attempts may be recorded in the attempt log against that same key.
4. On the server, enforce a unique constraint on the session's idempotency key. Insert the session and write the deduplication record in a single transaction, and acknowledge only after that transaction commits.
5. On a unique-constraint conflict (a key already seen, including a concurrent retry), do not insert again. Return the original success acknowledgement for that key.
6. On the client, remove a session from the queue only on receiving that success acknowledgement. Otherwise keep it queued and retry with the same key.
7. In integration testing, simulate a lost acknowledgement and concurrent retry requests. Assert that exactly one server-side session exists per locally created session and that the client queue is emptied.
