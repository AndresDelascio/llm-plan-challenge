VERDICT: BLOCKED

### 1. Registration limits are not enforced by the server
- Severity: blocker
- Claim: The server saves every submission even when capacity or the closing time has been reached.
- Why it matters: Two captains submitting when 15 teams are registered can take the count to 17; an already-open form can also submit after the deadline, preventing the list from being final.
- Fix: Check capacity and the deadline on the server, with the capacity check and insertion inside one SQLite write transaction.

### 2. Retries count as additional teams
- Severity: major
- Claim: Saving every submission as a new row allows a repeated request to register the same team twice.
- Why it matters: A double-click or retry after a slow response can consume multiple places, closing registration before 16 distinct teams have registered.
- Fix: Give each registration submission an idempotency token, enforce its uniqueness in SQLite, and return the existing registration when it is retried.

### 3. Captain contacts are publicly accessible
- Severity: major
- Claim: Keeping `/organiser-list` unlisted provides no access control.
- Why it matters: Anyone who discovers or guesses that address can retrieve every captain’s name, email and phone number.
- Fix: Remove the public organiser route and view the database downloaded through the existing authenticated host file browser locally.

### 4. The schedule uses an unfinished registration list
- Severity: major
- Claim: The schedule is built and emailed on 11 June while registration remains open until 12 June at 18:00.
- Why it matters: Teams registering during that interval are omitted from the schedule and mailing, requiring rework and preventing the stated completion condition from being met.
- Fix: Build and email the schedule after registration closes.