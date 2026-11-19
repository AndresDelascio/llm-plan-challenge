# Historical benchmarks

These measurements used the original Claude Code skill and its Claude subagent. The current runner uses a separate Claude CLI process and lower-effort settings. The old totals describe the original setup.

## Does the second model earn its place?

OpenAI already publishes an official [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) that reviews code. This repo covers the step before code exists, and asks a narrower question: does ChatGPT find problems in a plan that a fresh Claude, given the same text, does not?

### First run: the tool's own plan (2026-11-19)

The first plan put through the tool was the plan for this repo. Raw files: [challenge/plan-challenge-tool/](../challenge/plan-challenge-tool/).

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

The critiques changed the tool. All six accepted issues were about how to measure fairly, and they became the `measure` mode: each critic runs twice on the same frozen plan, Codex runs from an empty folder, issues are shuffled without labels, and I make the accept/reject calls instead of Claude. See [decisions.md](../challenge/plan-challenge-tool/decisions.md).

### Second run: a real plan (2026-11-19)

The plan was the next step of my trading research bot: run its paper-trading log automatically after every market day. Each critic ran twice on the same frozen plan. The four runs raised 7 distinct issues. I judged them shuffled, without knowing who raised which, and ticked 2. I had read the question as "pick one" and meant to accept all 7. I corrected that the same day, after the critic names had been shown, so this plan does not count as judged blind. Raw files: [challenge/orb-forward-log/](../challenge/orb-forward-log/).

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

See [decisions.md](../challenge/orb-forward-log/decisions.md) for every issue and who raised it.

### Third and fourth runs: two more real plans, judged blind (2026-11-19)

Same method, two more of my projects: a test of my soccer shot analyzer from a new camera position ([challenge/shot-tracker-new-camera/](../challenge/shot-tracker-new-camera/)) and the first real-footage batch through my clip editor ([challenge/content-studio-real-batch/](../challenge/content-studio-real-batch/)).

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

### Fifth run: plans with flaws planted on purpose (2026-11-19)

The runs above could not say which critic misses obvious problems, because nobody knew the right answer in advance. So Claude wrote three short made-up plans and planted 4 flaws in each (2 serious, 2 small), 12 in total. The answer key was committed before any critic ran. Each critic then read each plan twice.

| | Codex (ChatGPT) | Claude |
|---|---|---|
| Planted flaws found, per run | 4 of 4 in all 6 runs | 4 of 4 in all 6 runs |
| Tokens per run (measured) | 4,162 to 13,038 | 62,316 to 63,235 |
| Tokens per planted flaw found (computed) | 2,062 | 15,660 |
| Issues raised that were not planted | 1 | 6 |

- **Both critics found every planted flaw in every run.** For flaws that can be found by reading the plan carefully, the cheaper critic is enough.
- **Claude used 7.6 times the tokens** for the same planted flaws (computed, 375,846 against 49,494 over six runs each).
- **The test hit its ceiling**, so it does not show the two are equal. The only difference is in the extra issues nobody planted: Claude raised 6, Codex 1. Those were not judged.
- **Limits:** Claude wrote the plans, planted the flaws and did the scoring, so the flaws may be the kind Claude finds easy to see.

See **challenge/seeded-test/results.md** for the per-flaw table and every token count.

**What I decided from it:** the default critic is Codex. It costs about a tenth to a quarter of the tokens, and that matters for a check I run on every plan. On planted flaws it caught everything Claude caught. The price is coverage of the less obvious problems: on the three real plans it raised 6 of the 20 accepted issues against Claude's 18. When a plan is very important (real money or safety, public under my name, or hard to undo), the command asks me whether to switch to the Claude critic before it runs. I can also force it with `/challenge claude`, and `/challenge measure` repeats the comparison on any new plan.

## How this was built

Human-led design with AI-assisted implementation. I set the goal, the constraints and the stop rules; Claude Code wrote the skill and prompt files; ChatGPT (through Codex CLI) wrote every `critique-codex-*.md` file, and its criticisms changed the plans and the tool's own design; every result in this README comes from a run whose raw files are in the `challenge/` folder.
