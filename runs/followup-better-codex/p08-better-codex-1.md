# Attendance sync after offline practice

## Goal

Save attendance while offline and create exactly one server-side session for each locally created session, even when an acknowledgement is lost or retries arrive concurrently.

## Implementation

1. Generate a stable session UUID when the session is created locally. Save the session and its pending sync entry in one durable on-device transaction before showing it as saved.
2. Send pending sessions when connectivity returns and resume syncing after an app restart. Reuse the original session UUID and queued payload on every retry. Generate a separate attempt UUID for logging each send.
3. Enforce a database uniqueness constraint on the tenant ID and client session UUID. In one transaction, use an atomic insert-or-conflict operation to create the session and its attendance records. If the session already exists, return its canonical server ID for a matching payload. Return a conflict for a different payload under the same UUID.
4. Acknowledge each session only after its transaction commits. Mark a queue entry synced only after receiving a successful acknowledgement for that session. Keep entries pending after timeouts or transient failures and retry with backoff. Surface permanent failures for resolution.

## Integration tests

- Save offline, restart the app, reconnect, and verify the session syncs with its original UUID and attendance.
- Drop the acknowledgement after commit, then send concurrent retries with the same session UUID and different attempt UUIDs. Verify that all successful responses return the same server ID and that the database contains one session and one set of attendance records.
- Force a failure while writing attendance and verify that the transaction leaves no partial session. Retry and verify that the complete session is committed.
- Submit a different payload under an existing session UUID and verify that the server reports a conflict and preserves the committed attendance.
