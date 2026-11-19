# Plan Challenge

A Claude Code command, `/challenge`, that writes a project plan, has an independent critic attack it, and revises the plan with a logged decision for every criticism.

I describe an idea once. Claude writes the plan, a critic that has not seen our conversation criticises it, and Claude accepts or rejects each point in writing. The critic is a fresh Claude by default, or ChatGPT through OpenAI's Codex CLI. Nothing is copied between apps by hand.

I built it to connect two models, then measured whether the second model found more. On three of my own plans it did not, so I changed the default. The numbers are [below](#does-the-second-model-earn-its-place).

## How it works

```
idea ──> Claude writes plan.md ──> critic reads only plan.md ──> critique.md
                                                                     │
        revised plan.md  <── Claude accepts / rejects each issue <───┘
        + decisions.md       (one row per issue, with a reason)
```

- The critic gets a fixed prompt and the plan, never the chat. It costs fewer tokens and the critic is not led by my reasoning.
- The critic replies in a fixed format: a verdict and at most 5 issues, each with a severity and the smallest fix.
- A second round runs only if the critic found a blocker. Two rounds is the hard limit.
- If the critic fails, the plan is marked **NOT CHALLENGED**. A critique is never made up.
- Claude stops after the revised plan. I decide whether to build it.

The whole tool is two text files: [SKILL.md](.claude/skills/challenge/SKILL.md) (the steps Claude follows) and [critic-prompt.md](.claude/skills/challenge/critic-prompt.md) (what the critic is told).

## How to run it (Windows)

You need [Claude Code](https://claude.com/claude-code).

1. From this repo's folder, link the **challenge** folder into `.claude/skills/` in your user folder, so the command works in every project:
   ```powershell
   New-Item -ItemType Junction -Path $HOME\.claude\skills\challenge -Target "$PWD\.claude\skills\challenge"
   ```
   This is a folder link (a junction), which needs no administrator rights. There is only one set of files, so the installed command is always this repo's working folder: a clean `git status` means it matches the last commit. Moving the repo breaks the link. To remove the link without touching the files, run `cmd /c rmdir $HOME\.claude\skills\challenge`.
2. Open Claude Code in any project and type:
   ```
   /challenge an app that tracks my weekly training load
   ```

Choose the critic with the first word: `/challenge claude ...` (default, a fresh Claude), `/challenge codex ...` (ChatGPT, needs the setup below) or `/challenge measure ...` (both critics, the comparison described below).

### Optional: ChatGPT as the critic

Needed only for `codex` and `measure`. You need a ChatGPT account and Node.js 18.18 or later.

1. Install Codex CLI:
   ```powershell
   npm install -g @openai/codex
   ```
2. Sign in with your ChatGPT account (a browser window opens):
   ```powershell
   codex login
   ```

The results land in `challenge/<idea-name>/`: **plan-v1.md**, **plan.md** (revised), the critique files and **decisions.md**.

## Does the second model earn its place?

OpenAI already publishes an official [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) that reviews code. This repo covers the step before code exists, and asks a narrower question: does ChatGPT find problems in a plan that a fresh Claude, given the same text, does not?

### First run: the tool's own plan (2026-11-19)

The first plan put through the tool was the plan for this repo. Raw files: [challenge/plan-challenge-tool/](challenge/plan-challenge-tool/).

| Critic | Issues raised | Accepted | Tokens (measured) |
|---|---|---|---|
| Codex CLI 0.170.0, run 1 | 0 | 0 | 14,991 |
| Codex CLI 0.170.0, run 2 | 1 | 1 | 12,974 |
| Fresh Claude subagent, 1 run | 5 | 5 | 66,057 |

What this run shows, and what it does not:

- **The same critic gives different answers on the same plan.** Codex found nothing the first time and one real issue the second. A single run per critic proves little.
- **No issue was raised by both critics.** Codex's one issue was not among Claude's five.
- **Claude found more here but cost about five times the tokens.** Most of that is the context Claude Code loads into every subagent, not the critique.
- **This run is not a fair comparison.** Claude judged the issues knowing who raised them, Claude ran once and Codex twice, and the "no tools" line was added to the critic prompt after the Codex runs. Tokens are each tool's own reported total for input and output.

The critiques changed the tool. All six accepted issues were about how to measure fairly, and they became the `measure` mode: each critic runs twice on the same frozen plan, Codex runs from an empty folder, issues are shuffled without labels, and I make the accept/reject calls instead of Claude. See [decisions.md](challenge/plan-challenge-tool/decisions.md).

### Second run: a real plan, judged blind (2026-11-19)

The plan was the next step of my trading research bot: run its paper-trading log automatically after every market day. Each critic ran twice on the same frozen plan. The four runs raised 7 distinct issues. I judged them shuffled, without knowing who raised which. Raw files: [challenge/orb-forward-log/](challenge/orb-forward-log/).

| Critic | Issues raised | Accepted by me | Tokens (measured) |
|---|---|---|---|
| Codex CLI 0.170.0, run 1 | 3 | 0 | 8,343 |
| Codex CLI 0.170.0, run 2 | 3 | 0 | 14,093 |
| Fresh Claude subagent, run 1 | 5 | 2 | 67,242 |
| Fresh Claude subagent, run 2 | 5 | 2 | 69,044 |

- **On this plan the second model did not earn its place.** Both issues I accepted came from Claude only. Codex found nothing I accepted that Claude missed.
- **Each critic agreed with itself this time.** Both Codex runs raised the same 3 issues and both Claude runs the same 5. On the first run the two Codex runs disagreed.
- **Agreement between critics did not make an issue right for me.** One issue was raised by all four runs, and I rejected it.
- **Claude cost 5 to 8 times the tokens of Codex.** Tokens are each tool's own reported total.
- **Limits of this result:** one plan and one judge. Claude wrote the plan, merged the duplicate issues and wrote the one-line summaries I judged from.

See [decisions.md](challenge/orb-forward-log/decisions.md) for every issue and who raised it.

### Third and fourth runs: two more real plans, judged blind (2026-11-19)

Same method, two more of my projects: a test of my soccer shot analyzer from a new camera position ([challenge/shot-tracker-new-camera/](challenge/shot-tracker-new-camera/)) and the first real-footage batch through my clip editor ([challenge/content-studio-real-batch/](challenge/content-studio-real-batch/)).

| Plan | Critic | Issues raised | Accepted by me | Tokens (measured) |
|---|---|---|---|---|
| Shot analyzer test | Codex, run 1 | 0 | 0 | 5,995 |
| Shot analyzer test | Codex, run 2 | 0 | 0 | 11,019 |
| Shot analyzer test | Fresh Claude, run 1 | 5 | 5 | 68,754 |
| Shot analyzer test | Fresh Claude, run 2 | 5 | 5 | 69,335 |
| Clip editor batch | Codex, run 1 | 3 | 3 | not captured |
| Clip editor batch | Codex, run 2 | 3 | 3 | not captured |
| Clip editor batch | Fresh Claude, run 1 | 4 | 4 | 66,625 |
| Clip editor batch | Fresh Claude, run 2 | 5 | 5 | 66,861 |

The two missing token counts are my logging mistake: the command kept only the last lines of Codex's output and cut off the token line. They are not estimated.

### Result across the three blind-judged plans

| Plan | Distinct issues | Accepted by me | Accepted, Codex only | Accepted, Claude only | Accepted, both |
|---|---|---|---|---|---|
| Trading log | 7 | 2 | 0 | 2 | 0 |
| Shot analyzer test | 6 | 6 | 0 | 6 | 0 |
| Clip editor batch | 7 | 7 | 0 | 4 | 3 |
| Total | 20 | 15 | 0 | 12 | 3 |

- **On these three plans the second model did not earn its place.** Codex raised nothing I accepted that a fresh Claude had missed. Claude raised 12 accepted issues that Codex missed.
- **Codex is much cheaper.** 5,995 to 14,093 tokens per run on the four runs I captured, against 66,625 to 69,335 for Claude. Most of Claude's total is the context Claude Code loads into every subagent.
- **Claude disagreed with itself more than Codex did.** Of the 15 accepted issues, 4 were found by only one of the two Claude runs. Codex raised the same issues in both runs every time, but once gave two different verdicts for them (proceed with changes, then blocked).
- **Limits of this result:** three plans and one judge. Claude wrote all three plans, merged the duplicate issues and wrote the one-line summaries I judged from, so the judging was blind to the critic but not to Claude's wording. On the last two plans I accepted every issue, so those two say which critic raised more, not which critic was more often right.

See each folder's **decisions.md** for every issue and who raised it.

**What I changed because of it:** the default critic was Codex until 2026-11-19 and is now a fresh Claude. Codex stays available with `/challenge codex`, and `/challenge measure` repeats this comparison on any new plan.

## What this is not

- Not a multi-agent framework and not a link between the desktop chat apps.
- Not a code reviewer. It reviews plans.
- Not automatic implementation. It stops at the revised plan.

## Limits

- Codex CLI on native Windows is listed by OpenAI as experimental. The critic is run with `-s read-only`; I have not independently tested that the sandbox blocks writes on Windows.
- With the default critic, the writer and the critic are the same model family. A blind spot they share is not caught unless you run `codex` or `measure`.
- A single critic run can miss things: of the 15 issues I accepted, 4 were found by only one of the two Claude runs.
- With the `codex` critic the plan text is sent to OpenAI. Keep secrets out of plans.
- Claude both writes the plan and decides which criticisms to accept, so it can favour its own plan. The decision log is there so a person can check.

## How this was built

Human-led design with AI-assisted implementation. I set the goal, the constraints and the stop rules; Claude Code wrote the skill and prompt files; every result in this README comes from a run whose raw files are in the `challenge/` folder.
