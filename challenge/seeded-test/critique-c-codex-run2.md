VERDICT: BLOCKED

### 1. Registration limits are only enforced visually
- Severity: blocker
- Claim: The server enforces neither the 16-team cap nor the closing time.
- Why it matters: Two captains submitting when 15 teams are registered can create 17 rows; an already-open form can also submit after Friday’s cutoff.
- Fix: Reject full or closed registrations on the server, with the capacity check and insertion in one atomic database transaction.

### 2. Captain contacts are publicly accessible
- Severity: major
- Claim: Keeping `/organiser-list` unlisted provides no access control.
- Why it matters: Anyone who guesses or receives that URL can read every captain’s name, email and phone number.
- Fix: Protect the route with a single organiser password; captain accounts are unnecessary.

### 3. Repeated submissions become extra teams
- Severity: major
- Claim: Every repeated request creates another team row.
- Why it matters: A double-click or network retry can duplicate a team, consuming registration slots and putting duplicate entries in the final list.
- Fix: Give each registration attempt an idempotency token enforced by a unique database constraint, so retrying the same submission returns its existing registration.

### 4. The schedule precedes the final list
- Severity: major
- Claim: Thursday’s list is treated as final even though registration remains open until Friday.
- Why it matters: A team registering on Friday is absent from the schedule and Thursday’s mailing, leaving the completion condition unmet and requiring schedule rework.
- Fix: Build and email the schedule after registration closes.