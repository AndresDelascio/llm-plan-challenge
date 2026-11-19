# Verify both clients

Run the offline suite from the repository root. It exercises both CLI adapters with fixture responses, including their command lines, input boundaries, usage logging and failure paths. It requires Python 3.9+ and makes zero model calls.

```text
python -B -m unittest discover -s tests -v
```

Then run these in fresh terminal sessions from a disposable copy. Sign in to the selected critic CLI first. Use the same public, synthetic brief for each test and inspect the files in the new `challenge/` folder.

| Scenario | Claude Code | Codex | Pass condition |
| --- | --- | --- | --- |
| Default | `/challenge Plan a local soccer attendance log with a weekly export.` | `$challenge Plan a local soccer attendance log with a weekly export.` | Codex produces one critique and usage JSON. Every issue has a decision. A second round occurs only for a blocker. |
| Claude critic | `/challenge claude Plan a local soccer attendance log with a weekly export.` | `$challenge claude Plan a local soccer attendance log with a weekly export.` | Claude produces a critique and usage JSON. The run stops after the plan and decision log. |
| Missing CLI or auth | Repeat either command with its critic unavailable. | Same. | Draft is preserved, decisions say `NOT CHALLENGED`, and no critique is fabricated. |
| Existing plan | `/challenge codex challenge/seeded-test/plan-a.md` | `$challenge codex challenge/seeded-test/plan-a.md` | A new run folder contains the source plan's requirements. The source and earlier runs remain intact. |
| Compare | `/challenge measure Plan a local attendance log.` | `$challenge measure Plan a local attendance log.` | Four completed reviews of the same draft, a blind accept/reject step, then a revision. An unavailable critic yields an incomplete result. |

For a cheaper critic-only smoke test, run either command below against the original seeded plan. The output directory must exist and the output files must be new.

```text
python .claude/skills/challenge/review.py codex challenge/seeded-test/plan-a.md smoke-codex.md
python .claude/skills/challenge/review.py claude challenge/seeded-test/plan-a.md smoke-claude.md
```

For a release benchmark, run each critic twice per frozen plan, at the same configured effort and within each provider's same model version across revisions. Include the original seeded plans, a clean control and cases with harder-to-spot flaws. Score seeded-flaw recall, false positives, and accepted novel findings before inspecting provenance. Record the writer and critic versions and compare usage within each provider. Codex reports cached input within input, while Claude exposes separate cache-read and cache-write fields. Preserve those fields and report cost separately wherever the CLI provides it.
