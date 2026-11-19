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
7. If the critic fails, runs past 180 s, or replies without a readable verdict line, the plan is labelled "NOT CHALLENGED" and the user is told. No critique is ever invented.
8. Claude shows the decision table and stops. The user decides whether to implement.
9. Measurement (`/challenge measure`), on 3 real project ideas:
   - Each critic runs twice on the frozen `plan-v1.md`, before any revision. Codex runs from an empty folder so it cannot read other critiques. The critic prompt forbids tool use.
   - Only round 1 counts. Second-round findings are reported separately.
   - Two issues are the same if they name the same plan step and the same failure.
   - All issues are merged and shuffled with the critic labels removed. The user, not Claude, marks each one accept or reject.
   - The README table reports, per idea: issues raised and accepted per run, how much two runs of the same critic differ, and how much the two critics differ. The second number only means something next to the first.
   - The table and raw files are published, including the result if ChatGPT adds nothing.

## Risks I already know about
- Codex CLI on native Windows is listed as experimental; the read-only sandbox may not be enforced.
- Three ideas is a small sample; the result is an observation, not a statistic.
- The same model (Claude) both writes the plan and judges which criticisms to accept, so it may favour its own plan.
- Plan text is sent to OpenAI when the Codex critic is used.
- Codex CLI flags may change between versions and break the command.
