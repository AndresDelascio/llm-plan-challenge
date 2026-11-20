# Attendance sync after offline practice

## Goal

Every valid offline-created session that syncs successfully has exactly one server-side session with its full attendance, even when a response is lost or retries arrive concurrently.

## Implementation

1. **Save locally before confirming.** Generate a session UUID once. Persist the UUID and complete attendance payload together in the on-device queue before showing the session as saved. Restore pending entries on app restart.
2. **Retry with the same UUID and payload.** Send pending sessions when connectivity returns and retry transient failures with backoff. Keep each entry until the server confirms that the matching UUID is committed. For batch requests, apply acknowledgements per session so a partial response clears only confirmed entries.
3. **Commit atomically and let storage resolve concurrent requests.** Enforce a database uniqueness constraint on the session UUID within its authorized scope. Insert the session and all attendance records in one transaction. If a concurrent insert wins, resolve the uniqueness conflict and read the authorized, committed session. Return the same successful acknowledgement when its payload matches. Return a conflict for the same UUID with different attendance and preserve the original record.
4. **Acknowledge only after commit.** Include the client UUID and canonical server session ID in each success response. Leave transient failures pending and surface validation errors or payload conflicts so they can be resolved without automatic retries.

## Verification

- Save a session offline, restart the app, and confirm that it syncs with the original UUID and complete attendance.
- Drop the response after commit, then issue concurrent retries for the same UUID. Also test concurrent first submissions. Verify that storage contains one session and one complete set of attendance records, and that successful responses return the same server session ID.
- Fail the transaction after inserting the session but before completing the attendance write. Verify that no partial records remain and that a retry succeeds.
- Resubmit a UUID with different attendance and verify that the server returns a conflict and preserves the committed record. Verify that a partial batch response clears only acknowledged entries.
