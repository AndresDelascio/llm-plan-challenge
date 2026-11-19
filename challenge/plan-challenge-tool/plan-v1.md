## Brief
- Goal: A small public repo with one Claude Code command, `/challenge`, that turns a spoken idea into a project plan, has a second AI model attack the plan, and revises it, with no manual copy-pasting between apps. The README must show, with real counts, whether the second model (ChatGPT) finds problems a fresh Claude does not.
- Constraints: One person, Windows 11, not a trained software engineer. Uses existing subscriptions only (Claude Code, ChatGPT via Codex CLI), no paid API keys. Token use per run must stay small. No new frameworks or background services. The repo is a portfolio piece read cold by hiring managers.
- Non-goals: Not a general multi-agent framework. Not a connector between the desktop chat apps. Does not review code, only plans written before code exists. Does not implement the plan automatically.

## Plan
1. The repo holds one Claude Code skill (`SKILL.md`) and one fixed critic prompt (`critic-prompt.md`). No other code.
2. On `/challenge <idea>`, Claude writes `plan.md`: a brief (goal, constraints, non-goals), numbered steps and known risks, capped at 700 words.
3. Claude sends only the critic prompt plus `plan.md` to the critic. The critic never sees the conversation. Two critics are supported: Codex CLI (`codex exec`, read-only sandbox, prompt piped on stdin, reply saved to a file) and a fresh Claude subagent given the identical text.
4. The critic must reply in a fixed format: a verdict, then at most 5 issues, each with severity (blocker, major, minor), claim, why it matters and smallest fix, under 400 words. "No blocking issues" is allowed.
5. Claude writes `decisions.md`: one row per issue with accept or reject and a one-line reason. It then revises `plan.md` and keeps the original as `plan-v1.md`.
6. A second critique round runs only if round 1 contained a blocker. Hard cap of 2 rounds.
7. If the critic fails or times out, the plan is labelled "NOT CHALLENGED" and the user is told. No critique is ever invented.
8. Claude shows the decision table and stops. The user decides whether to implement.
9. Measurement: run 3 real project ideas with both critics on the same plan. For each critic count issues raised, issues accepted, and accepted issues the other critic missed. Publish the table and the raw files in the README, including the result if ChatGPT adds nothing.

## Risks I already know about
- Codex CLI on native Windows is listed as experimental; the read-only sandbox may not be enforced.
- Three ideas is a small sample; the result is an observation, not a statistic.
- The same model (Claude) both writes the plan and judges which criticisms to accept, so it may favour its own plan.
- Plan text is sent to OpenAI when the Codex critic is used.
- Codex CLI flags may change between versions and break the command.
