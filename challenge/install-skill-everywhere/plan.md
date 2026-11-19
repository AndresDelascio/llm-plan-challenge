## Brief
- Goal: Typing `/challenge` works in every Claude Code project on my Windows PC, and the installed copy cannot silently differ from the version in the repo.
- Constraints: One person, Windows 11, not a trained software engineer. The skill is two text files (`SKILL.md` and `critic-prompt.md`) in the repo folder `.claude/skills/challenge/`. Claude Code loads personal skills from `.claude/skills/` in the user folder. The repo currently sits in a temporary folder that is deleted when the chat session is deleted, and it is not in git yet. No new tools or dependencies. The repo is a portfolio piece, so its README must stay accurate.
- Non-goals: No packaging as a plugin. No automatic run on every plan. No change to what the skill does.

## Plan
1. Copy (not move) the repo to the permanent folder `D:\llm-plan-challenge` (proposed; I confirm the path before starting). Confirm `SKILL.md` and `critic-prompt.md` exist under `D:\llm-plan-challenge\.claude\skills\challenge\`. Then run `git init`, make the first commit on `main`, and create a task branch. Nothing is pushed. Every later step runs from a Claude Code session opened in that folder. The temporary copy is left alone and goes when the session is deleted.
2. Check that the install location is free: `Test-Path $HOME\.claude\skills\challenge` must print `False`. If it prints `True`, stop and look at what is there first.
3. Link instead of copy. Create a folder link (a junction, which needs no administrator rights): `New-Item -ItemType Junction -Path $HOME\.claude\skills\challenge -Target D:\llm-plan-challenge\.claude\skills\challenge`. There is then only one set of files, so the installed version cannot differ from the repo.
4. Check it from outside the repo: open a new Claude Code session in a different project and confirm `challenge` is in the skill list. Type `/challenge <small idea>` and confirm:
   - a `challenge/<slug>/` folder appears in that project with `plan-v1.md`, `plan.md`, `critique-claude.md` and `decisions.md`;
   - the first line of `critique-claude.md` starts with `VERDICT:`;
   - the session read `critic-prompt.md` from `$HOME\.claude\skills\challenge\` (ask it which path it read);
   - `(Get-Item $HOME\.claude\skills\challenge).Target` prints the repo path.
5. If Claude Code does not list the skill through the link: remove the link and stop. The Goal is then not met. A plain copy with a manual update rule is a decision for me to make, not an automatic fallback.
6. Change the install steps in the README to the link method, and add one line: the installed version is the repo's working folder, so a clean `git status` means it matches the last commit. Commit on the task branch.
7. After I review the diff, merge the task branch into `main` locally. Nothing is pushed.
8. Done when step 4 passes and the README change is on `main`.

## Risks I already know about
- Moving or renaming the repo folder breaks the link. `/challenge` then disappears from the skill list, which is visible, not silent.
- Removing the link the wrong way can delete the files it points to. The safe command is `cmd /c rmdir $HOME\.claude\skills\challenge`.
- A project that has its own `.claude/skills/challenge` folder may clash with the personal one.
- The link serves whatever is in the working folder, including a checked-out task branch and uncommitted edits.
