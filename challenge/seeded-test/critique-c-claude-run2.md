VERDICT: BLOCKED

### 1. The 16-team cap is only enforced by hiding the form
- Severity: blocker
- Claim: Step 2 has the server save every submission it receives, while the cap in step 3 and the deadline in step 5 only change what the page shows.
- Why it matters: Once the link is in the group chat, two captains with the form already open at 15 teams both submit and you have 17 or more. A stale tab can also submit after Friday 18:00.
- Fix: In the POST handler, check the row count and the closing time in the same transaction as the insert, and reject the submission if full or closed.

### 2. The schedule is built before registration closes
- Severity: blocker
- Claim: Step 6 builds and emails the schedule on Thursday 11 June, but step 5 keeps registration open until Friday 12 June 18:00.
- Why it matters: A team that registers on Thursday evening or Friday is in neither the schedule nor the email, so the "every captain has received the schedule" condition in step 10 fails.
- Fix: Close registration before the schedule is built, for example Wednesday 10 June at 18:00.

### 3. SQLite on a free hosting tier can be wiped
- Severity: major
- Claim: Many free tiers have an ephemeral filesystem that resets on restart or redeploy, and some have no file browser for the step 7 backup.
- Why it matters: The registration list disappears mid-campaign. A daily manual backup still loses up to a day of sign-ups, and the page reopens slots that were already taken.
- Fix: Before step 9, confirm the host has persistent disk by registering a team, restarting the app and checking the row survives; otherwise pick a host that does.

### 4. Captain contact data sits on an unprotected URL
- Severity: major
- Claim: `/organiser-list` exposes names, emails and phone numbers with no login, at a guessable path.
- Why it matters: Anyone who guesses the path, or sees it in shared browser history or a screenshot, gets every captain's phone number and email.
- Fix: Protect the route with one password stored in an environment variable (HTTP basic auth); this needs no captain accounts.

### 5. Duplicate submissions use up slots
- Severity: major
- Claim: Step 2 saves every submission as a new row and reloads the page instead of redirecting, with no uniqueness check.
- Why it matters: With the slow wake-up you already expect, captains double-click or refresh and the same team fills two or three of the 16 slots. Registration then shows "Tournament full" with fewer than 16 real teams.
- Fix: Add a UNIQUE constraint on team name and redirect after a successful POST.
