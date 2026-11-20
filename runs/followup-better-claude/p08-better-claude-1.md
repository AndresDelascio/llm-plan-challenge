# Attendance sync after offline practice

## Brief

Support offline attendance with exactly one server-side session per locally created session. An acknowledgement may be lost, and reconnects can submit retries concurrently.

## Design rule

Each locally created session gets one idempotency key, generated once on the device and reused on every send. The server enforces uniqueness on that key atomically with the session insert.

## Implementation

1. **Generate a stable session key at creation.**
   - When a session is created locally, generate a UUID (`client_session_id`).
   - It never changes for the life of that session and is reused on every retry.
   - Do not generate a new ID per send. A per-attempt ID may be logged for diagnostics, but it must never be used for deduplication.

2. **Persist before showing the session as saved.**
   - Write the session, its attendance records and its `client_session_id` to a durable on-device queue in a single local transaction.
   - Show "saved" only after that write succeeds.
   - Mark the entry `pending`.

3. **Send after reconnect.**
   - Send each queued batch with its `client_session_id`.
   - Allow only one in-flight request per queue entry on the client (a single sync worker or a per-entry lock).
   - Retry with backoff on timeouts and on network or 5xx errors, always with the same key.
   - Treat a non-retryable 4xx as a failure: mark the entry `failed` and surface it, rather than retrying forever or dropping it silently.

4. **Make the server atomically idempotent.**
   - Put a unique constraint on `client_session_id`, scoped per user or team if appropriate, either on the sessions table or on a deduplication table.
   - Insert the session, its attendance rows and the key in one database transaction.
   - Do not do a separate check, then insert, then record the key. That sequence lets concurrent retries both pass the check, and a crash between the writes leaves a session with no key.
   - On a unique-constraint conflict, including when a concurrent request wins the race, do not insert. Look up the existing session and return the same success response as the original, with the same server session ID.
   - Acknowledge only after the transaction commits.

5. **Handle the acknowledgement on the client.**
   - On success, whether the session was newly created or already existed, record the server session ID and mark the queue entry `synced` or remove it.
   - If the acknowledgement is lost, the entry stays `pending`. It is resent with the same key and resolves through the duplicate path in step 4.

6. **Test.**
   - **Lost acknowledgement:** the server commits and the response is dropped. The client retries. Expect exactly one server session and the client entry to end up `synced`.
   - **Concurrent retries:** fire N simultaneous requests with the same key. Expect exactly one session row and the same session ID in every response.
   - **Crash during the server transaction:** expect no partial session and no orphaned key. A retry then succeeds cleanly.
   - **App killed mid-sync:** the queue entry survives a restart and is resent with the same key.
   - **Distinct sessions:** two different local sessions create two server sessions, with no false deduplication.
