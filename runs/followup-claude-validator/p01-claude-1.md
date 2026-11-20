VERDICT: PROCEED WITH CHANGES

### 1. [major] Idempotency is built after the sync and the test that depend on it
- Failure: Followed in order, step 2 ships retrying sync with no stable UUID or unique constraint, so a lost acknowledgement creates duplicate server sessions. Step 3's lost-acknowledgement and concurrent-retry test then runs before steps 4–5 exist, so it fails, and nothing re-runs it against the finished design. Queue entries persisted in step 1 also have no UUID yet.
- Fix: Reorder to 1, 4, 5, 2, 3. Generate the UUID when the session is first persisted in step 1, and run the step 3 test last.
