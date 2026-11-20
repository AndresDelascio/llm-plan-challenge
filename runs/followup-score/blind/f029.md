# Attendance sync after offline practice

## Brief

Support offline attendance with exactly one server-side session per locally created session. An acknowledgement may be lost, and reconnects can submit retries concurrently.

## Implementation

1. **Stable identity.** Generate a session UUID on-device once, when the session is created. Never regenerate it.
2. **Durable local queue.** Persist the session, its attendance, and its UUID to an on-device queue before showing the session as saved.
3. **Idempotent server write.**
   - Enforce a unique constraint on session UUID in storage.
   - Write the session and its attendance atomically in one transaction.
   - On a duplicate UUID, write nothing and return the existing committed session with the same success response as the original write.
   - Rely on the constraint, not a check-then-insert, to handle concurrent retries: the losing request waits for or re-reads the winner's committed row and returns it.
4. **Sync on reconnect.**
   - Send queued batches with the same UUID on every attempt.
   - The server acknowledges only after the transaction commits.
   - The client removes a queue entry only after receiving that acknowledgement; otherwise it stays queued and is retried with backoff.
   - Allow one sync run at a time per device to reduce, though not eliminate, concurrent duplicates.
5. **Integration tests.**
   - **Lost acknowledgement:** the server commits, the response is dropped, and the client retries. Expect exactly one session, a success response, and a cleared queue entry.
   - **Concurrent retries:** send N simultaneous requests with the same UUID. Expect exactly one session and one set of attendance rows, with every request returning the same session.
   - **Crash mid-sync:** kill the app after queueing or mid-send. Expect the entry to survive a restart and sync exactly once.
   - **Atomicity:** fail the attendance write. Expect no session row, and a later retry to succeed.
