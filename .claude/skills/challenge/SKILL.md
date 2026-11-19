---
name: challenge
description: Write a project plan, have an independent critic (a fresh Claude, or ChatGPT via Codex CLI) attack it, then revise the plan with a logged accept/reject decision for every issue. Use when the user types /challenge or asks to have a plan challenged, stress-tested or reviewed by another model.
argument-hint: "[codex|claude|measure] <idea, or nothing to use the idea already discussed>"
---

# /challenge

Turn an idea into a plan that has survived one independent critique.

## Settings (change here only)

- Default critic: `codex` (chosen 2026-11-19 for its token cost, about a tenth to a quarter of `claude`; in the measured comparison in the README `claude` raised more of the accepted issues)
- Plan length cap: 700 words
- Max critique rounds: 2
- Codex timeout: 180 s (set the shell tool's own timeout to 240 s; its default of 120 s would cut Codex off first)
- Output folder: `challenge/<slug>/` in the current project, where `<slug>` is 2–4 words naming the idea

## Critic argument

- `claude`: a fresh Claude subagent. Needs no install. Used about 64,000–69,000 tokens per run (measured on nine runs, 2026-11-19) because every subagent starts with Claude Code's own context.
- `codex` (default): ChatGPT through Codex CLI, which must be installed and signed in. About 6,000–15,000 tokens per run (measured on six runs, 2026-11-19). Sends the plan text to OpenAI.
- `measure`: the comparison procedure at the end of this file. Slower and needs the user to judge the issues. Only for measuring whether the second model earns its place.

## Steps

### 1. Write `plan.md`

Start with this brief, then the plan. Stay under the length cap.

```markdown
## Brief
- Goal: <one sentence, what done looks like>
- Constraints: <budget, tools, time, skills, anything fixed>
- Non-goals: <what this deliberately does not do>

## Plan
<numbered steps>

## Risks I already know about
<short list>
```

Never put secrets, API keys or private personal details in the plan. The `codex` critic sends this file to OpenAI.

### 2. Get the critique

The critic sees only `critic-prompt.md` (in this skill's folder) followed by `plan.md`. Never pass the conversation: a critic that has not seen the reasoning is less likely to agree with it, and it costs fewer tokens.

**codex** — use absolute paths. `<empty folder>` is a new empty folder in the system temp directory:

```bash
cat "<skill folder>/critic-prompt.md" "<project>/challenge/<slug>/plan.md" | timeout 180 codex exec - -C "<empty folder>" -s read-only --skip-git-repo-check --ephemeral -o "<project>/challenge/<slug>/critique-codex.md"
```

- `-C <empty folder>`: Codex works in a folder with nothing in it, so it cannot read the project or another critic's reply. `-s read-only`: it cannot edit files. `--ephemeral`: no session history is kept.
- Do not cut the command's output (no `tail` or `head`): the number on the line after `tokens used` is the only record of the run's cost, and `--ephemeral` means it cannot be looked up later.
- If the command fails, times out, or the output file is empty or its first line is not `VERDICT: ...`: do not retry more than once, and do not invent a critique. Mark the plan `NOT CHALLENGED (<reason>)` at the top of `decisions.md`, tell the user, and offer the `claude` critic instead.
- If the error is about login, tell the user to run `codex login` themselves.

**claude** — spawn one general-purpose subagent (not a fork). Its prompt is the full text of `critic-prompt.md` followed by the full text of `plan.md`, and nothing else. Save its reply unchanged to `critique-claude.md`.

### 3. Decide on every issue, in `decisions.md`

One row per issue. Every issue gets a decision; none are skipped.

```markdown
| # | Critic | Severity | Issue | Decision | Reason |
|---|--------|----------|-------|----------|--------|
```

- **Accept** when the issue is real and the fix serves the Goal.
- **Reject** when it contradicts the Brief, adds scope the Goal does not need, or is wrong. Say which, in one line.
- Do not accept an issue just because it was raised, and do not reject one just to keep the plan unchanged.

End the file with one line of counts: issues raised, accepted and rejected.

### 4. Revise `plan.md`

Apply the accepted fixes. Keep the original as `plan-v1.md` so the before and after can be compared.

### 5. Second round, only if needed

Run the critique again on the revised plan only if round 1 contained a `blocker`. Save as `critique-<critic>-2.md` and add the rows to `decisions.md`. Never run a third round; if a blocker is still open, say so and stop.

### 6. Stop and report

Show the user the `decisions.md` table and a three-line summary of what changed in the plan. Then wait. Do not start implementing until the user says to.

## `measure` mode

Answers one question: does the Codex critic find accepted issues that a fresh Claude does not, beyond what two runs of the same critic already differ by?

1. Write `plan.md` as in step 1 and copy it to `plan-v1.md`. Do not revise it until step 6 below.
2. Run each critic twice on `plan-v1.md`, all four in parallel: `critique-codex-run1.md`, `critique-codex-run2.md`, `critique-claude-run1.md`, `critique-claude-run2.md`. Round 1 only; no second round counts.
3. Merge duplicates. Two issues are the same if they name the same plan step and the same failure. Record privately which runs raised each one.
4. Show the user the merged issues in shuffled order with no critic names. The user marks each accept or reject. Claude does not decide in this mode, because it would be judging its own model family.
5. Write `decisions.md` with the labels restored, and these counts: issues raised and accepted per run; accepted issues found by only one of the two Codex runs and only one of the two Claude runs (the noise); accepted issues found by Codex but neither Claude run, and by Claude but neither Codex run (the difference).
6. Revise `plan.md` with the accepted fixes and stop as in step 6 of the normal flow.
