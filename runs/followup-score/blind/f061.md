# Attendance sync after offline practice

## Goal

Save attendance offline and create exactly one server-side session for each locally created session once it syncs, even if an acknowledgement is lost or retries arrive concurrently.

## Implementation

1. Generate a session UUID once, when the session is created locally. Persist the UUID and attendance data in the on-device sync queue before showing the session as saved. Keep the queue across app restarts.
2. Send queued sessions after reconnect. Reuse each session’s UUID and queued payload on every retry. If attempt logging is needed, use a separate attempt UUID for diagnostics.
3. Enforce a database unique constraint on the session UUID within the owning account. Use an atomic insert-or-get operation under that constraint so concurrent requests converge on the same server session. Commit the session and its attendance records together in one transaction. If a retry uses the same UUID with a different payload, return a conflict without changing the stored session.
4. Acknowledge each session only after its transaction commits. Return the same server session ID for duplicates with matching payloads. Remove a queue entry only after receiving its success acknowledgement. Retry timeouts and transient failures with backoff, and surface permanent failures while retaining the local data.

## Verification

- Save a session offline, restart the app, and reconnect. Verify that the queued session syncs and is removed after acknowledgement.
- Drop the acknowledgement after the server commits, then retry. Verify that the retry returns the original server session ID and that only one session and one set of attendance records exist.
- Send concurrent requests with the same UUID before any request commits. Verify that all successful responses return the same server session ID and that attendance records are written once.
- Force a failure before commit and verify that no partial session or attendance records remain. Retry and verify that the full session is saved.
- Submit a different payload with an existing UUID and verify that the server returns a conflict and preserves the original data. In a batch with mixed outcomes, verify that the client removes only the acknowledged entries.
