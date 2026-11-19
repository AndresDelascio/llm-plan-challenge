# Plan Challenge

A Claude Code command, `/challenge`, that writes a project plan, has an independent critic attack it, and revises the plan with a logged decision for every criticism.

I describe an idea once. Claude writes the plan, a critic that has not seen our conversation criticises it, and Claude accepts or rejects each point in writing. The critic is ChatGPT through OpenAI's Codex CLI by default, or a fresh Claude. Nothing is copied between apps by hand.

I built it to connect two models, then measured what each critic finds and what it costs. On three of my own plans a fresh Claude raised 18 of the 20 issues I accepted and ChatGPT raised 6, at about a tenth to a quarter of the tokens. I use the cheaper one by default. The numbers are [below](#does-the-second-model-earn-its-place).

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

You need [Claude Code](https://claude.com/claude-code), a ChatGPT account and Node.js 18.18 or later.

1. From this repo's folder, link the **challenge** folder into `.claude/skills/` in your user folder, so the command works in every project:
   ```powershell
   New-Item -ItemType Junction -Path $HOME\.claude\skills\challenge -Target "$PWD\.claude\skills\challenge"
   ```
   This is a folder link (a junction), which needs no administrator rights. There is only one set of files, so the installed command is always this repo's working folder: a clean `git status` means it matches the last commit. Moving the repo breaks the link. To remove the link without touching the files, run `cmd /c rmdir $HOME\.claude\skills\challenge`.
2. Install Codex CLI:
   ```powershell
   npm install -g @openai/codex
   ```
3. Sign in with your ChatGPT account (a browser window opens):
   ```powershell
   codex login
   ```
4. Open Claude Code in any project and type:
   ```
   /challenge an app that tracks my weekly training load
   ```

Choose the critic with the first word: `/challenge codex ...` (default, ChatGPT), `/challenge claude ...` (a fresh Claude; steps 2 and 3 are not needed for it) or `/challenge measure ...` (both critics, the comparison described below).

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

### Second run: a real plan (2026-11-19)

The plan was the next step of my trading research bot: run its paper-trading log automatically after every market day. Each critic ran twice on the same frozen plan. The four runs raised 7 distinct issues. I judged them shuffled, without knowing who raised which, and ticked 2. I had read the question as "pick one" and meant to accept all 7. I corrected that the same day, after the critic names had been shown, so this plan does not count as judged blind. Raw files: [challenge/orb-forward-log/](challenge/orb-forward-log/).

| Critic | Issues raised | Accepted by me | Tokens (measured) |
|---|---|---|---|
| Codex CLI 0.170.0, run 1 | 3 | 3 | 8,343 |
| Codex CLI 0.170.0, run 2 | 3 | 3 | 14,093 |
| Fresh Claude subagent, run 1 | 5 | 5 | 67,242 |
| Fresh Claude subagent, run 2 | 5 | 5 | 69,044 |

- **Each critic found issues the other missed.** Of the 7 accepted issues, 2 came from Codex only, 4 from Claude only and 1 from all four runs.
- **Each critic agreed with itself this time.** Both Codex runs raised the same 3 issues and both Claude runs the same 5. On the first run the two Codex runs disagreed.
- **Claude cost 5 to 8 times the tokens of Codex.** Tokens are each tool's own reported total.
- **Limits of this result:** one plan and one judge, and the judgement was corrected after the names were shown. Claude wrote the plan, merged the duplicate issues and wrote the one-line summaries I judged from.

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

### Result across the three plans I judged

| Plan | Distinct issues | Accepted by me | Accepted, Codex only | Accepted, Claude only | Accepted, both |
|---|---|---|---|---|---|
| Trading log | 7 | 7 | 2 | 4 | 1 |
| Shot analyzer test | 6 | 6 | 0 | 6 | 0 |
| Clip editor batch | 7 | 7 | 0 | 4 | 3 |
| Total | 20 | 20 | 2 | 14 | 4 |

- **A fresh Claude found more.** Of the 20 issues I accepted, Claude raised 18 and Codex 6. Claude raised 14 that Codex missed. Codex raised 2 that Claude missed.
- **Codex is much cheaper.** 5,995 to 14,093 tokens per run on the four runs I captured, against 66,625 to 69,335 for Claude. Most of Claude's total is the context Claude Code loads into every subagent.
- **Claude disagreed with itself more than Codex did.** Of the 20 accepted issues, 4 were found by only one of the two Claude runs. Codex raised the same issues in both runs every time, but once gave two different verdicts for them (proceed with changes, then blocked).
- **Limits of this result:** three plans and one judge. Claude wrote all three plans, merged the duplicate issues and wrote the one-line summaries I judged from, so the judging was blind to the critic but not to Claude's wording, and on the trading log it was corrected after the names were shown. I accepted every issue on all three plans, so the result says which critic raised more, not which critic was more often right.

See each folder's **decisions.md** for every issue and who raised it.

**What I decided from it:** the default critic is Codex. It costs about a tenth to a quarter of the tokens, and that matters for a check I run on every plan. The price is coverage: on these plans it raised 6 of the 20 accepted issues against Claude's 18. For a plan that matters I use `/challenge claude`, and `/challenge measure` repeats this comparison on any new plan.

## What this is not

- Not a multi-agent framework and not a link between the desktop chat apps.
- Not a code reviewer. It reviews plans.
- Not automatic implementation. It stops at the revised plan.

## Limits

- Codex CLI on native Windows is listed by OpenAI as experimental. The critic is run with `-s read-only`; I have not independently tested that the sandbox blocks writes on Windows.
- With the `claude` critic, the writer and the critic are the same model family. A blind spot they share is not caught unless you run `codex` or `measure`.
- A single critic run can miss things. Of the 20 issues I accepted, the default Codex critic missed 14, and 4 were found by only one of the two Claude runs.
- With the default `codex` critic the plan text is sent to OpenAI. Keep secrets out of plans.
- Claude both writes the plan and decides which criticisms to accept, so it can favour its own plan. The decision log is there so a person can check.

## How this was built

Human-led design with AI-assisted implementation. I set the goal, the constraints and the stop rules; Claude Code wrote the skill and prompt files; every result in this README comes from a run whose raw files are in the `challenge/` folder.
