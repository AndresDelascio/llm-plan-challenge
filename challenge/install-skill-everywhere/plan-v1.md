## Brief
- Goal: Typing `/challenge` works in every Claude Code project on my Windows PC, and the installed copy cannot silently differ from the version in the repo.
- Constraints: One person, Windows 11, not a trained software engineer. The skill is two text files (`SKILL.md` and `critic-prompt.md`) in the repo folder `.claude/skills/challenge/`. Claude Code loads personal skills from `.claude/skills/` in the user folder. The repo currently sits in a temporary folder that is deleted when the chat session is deleted, and it is not in git yet. No new tools or dependencies. The repo is a portfolio piece, so its README must stay accurate.
- Non-goals: No packaging as a plugin. No automatic run on every plan. No change to what the skill does.

## Plan
1. Move the repo to a permanent folder, run `git init`, and make the first commit on a task branch. Nothing is pushed.
2. Copy the skill into the user folder with the command already in the README: `Copy-Item -Recurse .claude\skills\challenge $HOME\.claude\skills\`.
3. Check it from outside the repo: open a new Claude Code session in a different project, confirm `challenge` is in the skill list, type `/challenge <small idea>`, and confirm a `challenge/<slug>/` folder appears in that project with `plan-v1.md`, `plan.md`, `critique-claude.md` and `decisions.md`.
4. Fix the rule for updates: the repo is the source. After any edit to the skill in the repo, copy the two files over the installed ones with `Copy-Item -Force .claude\skills\challenge\* $HOME\.claude\skills\challenge\`. Add this rule and command to the README.
5. Done when step 3 passes and the README has the update rule.

## Risks I already know about
- The installed copy goes stale if I edit the repo and forget to copy again.
- A project that has its own `.claude/skills/challenge` folder may clash with the personal one.
- Running the step 2 command a second time nests a `challenge` folder inside the existing one instead of replacing it.
