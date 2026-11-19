VERDICT: BLOCKED

### 1. Manual copy rule does not meet the Goal
- Severity: blocker
- Claim: Step 4 relies on remembering to copy, which the plan's own first risk says will fail, while the Goal says the installed copy "cannot silently differ".
- Why it matters: The first forgotten copy after a repo edit leaves `/challenge` running the old version in every project, with nothing to flag it.
- Fix: Replace the copies in steps 2 and 4 with one directory junction: `New-Item -ItemType Junction -Path $HOME\.claude\skills\challenge -Target <permanent repo>\.claude\skills\challenge`. Step 3 then confirms Claude Code loads through it. If it does not, keep the copy and add a `Get-FileHash` comparison to the update rule.

### 2. Step 3 can pass on the wrong files
- Severity: major
- Claim: Step 3 only checks that the skill is listed and four output files exist, not which copy ran or whether `critic-prompt.md` was actually used.
- Why it matters: If `$HOME\.claude\skills\challenge` already exists, step 2 nests the new copy and the old one passes the test. If `SKILL.md` points to the prompt by a repo-relative path, the critic can improvise in another project and still write `critique-claude.md`.
- Fix: Before step 2, confirm the destination does not exist. In step 3, check that the critique follows the `critic-prompt.md` format and that the installed `SKILL.md` matches the repo's.

### 3. Moving the repo out from under the session
- Severity: major
- Claim: Step 1 moves the repo but never names the destination or says later steps run from there.
- Why it matters: If the step 4 README edit is made in the temporary folder, it is lost when the session is deleted, and the permanent repo keeps a README without the update rule.
- Fix: Name the permanent path in step 1, and run steps 2–5 from a session opened in that folder.

### 4. README change is never committed
- Severity: minor
- Claim: The only commit is in step 1, on a task branch, and the "done" test in step 5 does not include committing the step 4 README edit.
- Why it matters: The repo ends with no `main` branch and its key install rule sitting uncommitted, so git does not hold the real source version.
- Fix: Make the first commit on `main`, then branch, and add "README change committed" to step 5.
