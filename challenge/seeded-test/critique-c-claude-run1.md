VERDICT: BLOCKED

### 1. The 16-team cap and the deadline are only enforced by the page
- Severity: blocker
- Claim: The server saves every submission it receives (step 2), while the cap and the closing time only hide the form (steps 3, 5).
- Why it matters: Two captains submitting near team 16, or anyone with a page left open, will create team 17 or later, or register after Friday 18:00. The Goal says exactly 16.
- Fix: In the POST handler, check the count and the deadline inside the same transaction as the insert, and reject if there are 16 teams or it is past closing.

### 2. The schedule is built before registration closes
- Severity: blocker
- Claim: Step 6 builds the schedule from the "final list" on Thursday 11 June, but registration stays open until Friday 12 June 18:00 (step 5).
- Why it matters: Teams that register on Thursday or Friday are not in the schedule and get no email, so the done criterion in step 10 fails.
- Fix: Close registration before the schedule is built, for example Wednesday 10 June at 18:00.

### 3. SQLite on a free tier may not persist
- Severity: major
- Claim: Many free hosting tiers have ephemeral disks that reset on restart or redeploy, and a daily manual download (step 7) assumes a file browser exists.
- Why it matters: A restart silently wipes the registrations. The page then shows free slots again, and up to a day of captain contacts is lost.
- Fix: Confirm the host has persistent disk before building. Also email yourself each submission as it arrives, so no registration exists only in the database.

### 4. Captain contacts are public at a guessable URL
- Severity: major
- Claim: `/organiser-list` has no login and a predictable name (step 4).
- Why it matters: Anyone in the group chat, or any crawler, can read every captain's name, email and phone number from 25 May onwards.
- Fix: Require a long random token in the URL, read from an environment variable, or use HTTP basic auth with one password.

### 5. Duplicate and junk rows consume slots
- Severity: major
- Claim: Every submission becomes a new row with no validation and no redirect after the POST (step 2).
- Why it matters: A double-click, a browser refresh or a prank entry fills slots. Registration then shows "Tournament full" with fewer than 16 real teams, and step 8's test would not catch it.
- Fix: Add a UNIQUE constraint on team name and on captain email, redirect after a successful POST, and add a delete button per row on the organiser page.
