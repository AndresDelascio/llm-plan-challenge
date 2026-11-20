# Attendance sync after offline practice

## Goal

Create exactly one server-side session with its complete attendance for each locally saved session, even when an acknowledgement is lost or reconnects trigger concurrent retries.

## Implementation

1. Generate a session UUID once. Persist the UUID and complete attendance payload together in the on-device queue before showing the session as saved. Restore pending entries after an app restart.
2. On reconnect, submit pending entries using their stored UUIDs and payloads. Keep each entry queued until the device receives a success acknowledgement for that UUID. Retry unacknowledged entries with the same UUID and payload.
3. Enforce a unique constraint on the session UUID in server storage. Insert the session and all attendance records in one transaction, using the constraint to arbitrate concurrent inserts. Acknowledge success only after the transaction commits.
4. When a request conflicts with an existing UUID, resolve the conflict against the committed session. Return the same success acknowledgement if the payload matches. If the payload differs, return a conflict without modifying the committed session or clearing the queued entry.

## Acceptance tests

- Save a session offline, restart the app, and reconnect. Verify the queue survives the restart and clears after acknowledgement.
- Drop the acknowledgement after a successful commit, then retry. Verify the retry acknowledges the original session and leaves exactly one complete set of attendance records.
- Submit concurrent requests with the same UUID and payload. Verify they resolve to the same committed session and create one set of attendance records.
- Force a failure after the session insert and before the attendance write completes. Verify the transaction rolls back, the queue entry remains pending, and a retry commits the complete session.
- Reuse a committed UUID with a different payload. Verify the server returns a conflict and preserves the original attendance.
