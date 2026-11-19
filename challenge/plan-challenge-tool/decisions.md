# Decisions: plan-challenge-tool

Run date: 2026-11-19. Critics: Codex CLI 0.170.0 (two runs) and one fresh Claude subagent, all on the same `plan-v1.md`.

**Not blinded.** Claude made these decisions knowing which critic raised each issue. The blind procedure in the skill's `measure` mode did not exist yet; it was added because of issue 3 below.

| # | Critic | Severity | Issue | Decision | Reason |
|---|--------|----------|-------|----------|--------|
| 1 | claude | major | One run per critic cannot separate real differences from run-to-run variation | Accept | Confirmed in this same run: Codex returned 0 issues the first time and 1 the second. `measure` mode now runs each critic twice |
| 2 | claude | major | Critics are not isolated; either can read the other's saved reply | Accept | Codex now runs from an empty folder (`-C`), and the critic prompt says not to use tools |
| 3 | claude | major | Claude judges which issues count while knowing who raised them | Accept | In `measure` mode the issues are shuffled without labels and the user decides |
| 4 | claude | major | No rule for "same issue"; revision could happen before the second critic runs | Accept | All critics read the frozen `plan-v1.md`; same plan step and same failure counts as the same issue |
| 5 | claude | minor | "Critic fails" has no timeout value or format check | Accept | The skill had a 180 s limit and a format check but the plan did not say so. Real gap found: the shell tool's own default limit is 120 s, so the skill now sets it to 240 s |
| 6 | codex (run 2) | major | A second round triggered by one critic would count as issues the other "missed" | Accept | The comparison table uses round 1 only |

Codex run 1 raised no issues (`VERDICT: NO BLOCKING ISSUES`).

**Counts.** Claude: 5 raised, 5 accepted. Codex run 1: 0 raised. Codex run 2: 1 raised, 1 accepted. No issue was raised by both critics. No blocker, so no second round.

**Tokens (measured, as reported by each tool, input and output together).** Codex run 1: 14,991. Codex run 2: 12,974. Claude subagent: 66,057, most of which is the context Claude Code gives every subagent before it reads the plan.
