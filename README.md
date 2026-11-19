# Plan Challenge

Turn an idea or existing plan into a revised plan and decision log. Claude Code and Codex can both run the workflow. The default reviewer is a fresh Codex CLI session. Choose Claude explicitly when you want a different model family from a Codex writer.

## Quick start

1. Clone the repository, or use GitHub **Code → Download ZIP** and extract it. Open a terminal at the repository root. You need Python 3.9+ and the current CLI for the writer and reviewer you choose.
   ```sh
   git clone https://github.com/AndresDelascio/llm-plan-challenge.git
   cd llm-plan-challenge
   ```
2. Sign in to your writer and reviewer. For the default reviewer, install [Codex CLI](https://developers.openai.com/codex/cli) and run `codex login`. For Claude, install [Claude Code](https://code.claude.com/docs/en/quickstart) and follow its sign-in prompt. A Claude-to-Claude run needs only Claude Code and Python.
3. Start `claude` or `codex` from the repository root and enter the appropriate command **in the chat prompt**.

| Choose | Claude Code | Codex |
| --- | --- | --- |
| Default Codex critique | `/challenge Plan a weekly soccer attendance log` | `$challenge Plan a weekly soccer attendance log` |
| Claude critique | `/challenge claude Plan a weekly soccer attendance log` | `$challenge claude Plan a weekly soccer attendance log` |
| Compare both critics | `/challenge measure Plan a weekly soccer attendance log` | `$challenge measure Plan a weekly soccer attendance log` |

Use the idea already discussed by entering just the skill name, or paste a path to an existing Markdown plan in place of the idea. If the skill is missing from the picker, open a new session from the repository root. This repository is currently private, so people need GitHub access to clone it or download the ZIP.

### Use it in another project

Copy the **entire** [`challenge` skill folder](.claude/skills/challenge) into one of these directories. Create the destination parent if needed. The copied folder should contain `SKILL.md` directly. Recopy the folder contents when updating.

| Client | One project | All your projects |
| --- | --- | --- |
| Claude Code | `.claude/skills/challenge/` | `~/.claude/skills/challenge/` |
| Codex | `.agents/skills/challenge/` | `~/.agents/skills/challenge/` |

On Windows, `~` is your user profile folder. Open a fresh session in the destination project and use the same commands.

## What lands in your project

| File in `challenge/<idea>/` | What it contains |
| --- | --- |
| `plan-v1.md` | Original draft |
| `critique-<critic>.md` | Up to five concrete issues |
| `critique-<critic>.usage.json` | CLI-reported usage fields |
| `decisions.md` | One accept/reject decision and reason per issue |
| `plan.md` | Revised plan or preserved draft if the review failed |

The standard run sends a compact plan and rubric to one reviewer in a fresh CLI process. Only a blocker triggers a second review. `measure` runs four reviews of the same draft and asks you to judge the issues before revealing which critic raised them. The workflow stops at planning. Remove secrets and private data from any plan you send to a provider.

## Evidence and next steps

- [Historical benchmarks](docs/benchmarks.md) include the original critiques and token measurements. Those measurements predate the lightweight runner.
- [Verification guide](docs/verification.md) covers offline tests, real-client smoke tests and how to compare the new usage logs.
- Before inviting outside users, run the authenticated smoke tests, benchmark tokens versus review quality, choose a license, and review the archived examples for anything you want to keep private.
