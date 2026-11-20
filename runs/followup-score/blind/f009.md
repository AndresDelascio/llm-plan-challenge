# Attendance sync after offline practice

## Brief

Support offline attendance with exactly one server-side session per locally created session. An acknowledgement may be lost, and reconnects can submit retries concurrently.

## Implementation

1. **Assign a stable idempotency key at creation.** When a session is created locally, generate one UUID for it. This key identifies the session for its whole life and is reused unchanged on every send attempt.

2. **Persist before showing as saved.** Durably write the session, its attendance records and its idempotency key to the on-device queue. Only then show the session as saved.

3. **Send after reconnect and retry until acknowledged.**
   - Send queued batches with each session's idempotency key.
   - Remove an entry from the queue only after a server acknowledgement for that key.
   - On a timeout or network error, keep the entry and retry with backoff, using the same key.
   - Run only one sync at a time on the client so reconnect events do not start overlapping sends. The server must still tolerate concurrent retries.
   - If per-attempt tracing is needed, log a separate attempt ID. It is never used for deduplication.

4. **Make the server insert atomic and idempotent.**
   - Put a unique constraint on the idempotency key, either on the session row itself or in a deduplication table.
   - Insert the session, its attendance records and the key in a single transaction. Do not check first and insert afterwards, and do not write the key separately.
   - If the insert hits the unique constraint, treat it as a duplicate: look up the existing session and return the same success response as the original request, including the server session ID.
   - If a concurrent retry arrives while the first transaction is still in flight, the constraint makes it wait or fail. It then returns the committed result and never creates a second session.
   - Acknowledge only after the transaction commits.

5. **Handle a duplicate acknowledgement on the client.** Treat an "already processed" success exactly like a first success: record the server session ID and remove the entry from the queue.

6. **Run integration tests against the finished flow.**
   - **Lost acknowledgement:** the server commits, the response is dropped and the client retries. Expect exactly one server session and an empty client queue.
   - **Concurrent retries:** send N simultaneous requests with the same key. Expect exactly one session and the same session ID in every response.
   - **Crash after commit:** kill the app between the server commit and the queue removal, then restart. Expect a resend, no duplicate and an empty queue.
   - **Partial failure:** make the transaction fail midway. Expect no session and no key recorded, and a later retry that succeeds.
   - **Distinct sessions:** create two different local sessions. Expect two server sessions.
