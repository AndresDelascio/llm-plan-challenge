# Plan Challenge

**Does a plan get better when a second AI model reviews it before anything is built?** A small measured study, and the tool I use because of it.

AI coding assistants write confident plans, and the model that wrote a plan tends to agree with it. `/challenge` sends the draft to a fresh reviewer (Codex or Claude) that sees only the plan and a rubric. Every issue it raises gets an accept or reject decision in a log, and the plan is revised before any code is written.

This repo holds the skill, the benchmark I built to test it, and every raw reply behind the numbers below.

**Short answer: yes, on my own plans.** One review pass on three real project plans raised 20 issues, and I accepted all 20 before writing any code. A review takes about 7 seconds with Codex.

## Why download it

- **A second opinion in one command.** Type `/challenge <idea>` in Claude Code or `$challenge <idea>` in Codex. You get a revised plan and a log of every issue with the reason it was accepted or rejected.
- **Nothing to install beyond the CLIs.** The skill is one folder with two small Python files that use only the standard library. Copy the folder into a project and it works.
- **It tells you when it failed.** If the reviewer times out or breaks the format, the plan is marked `NOT CHALLENGED` and the raw reply is kept. It never writes a review on the reviewer's behalf.
- **You can check every number.** The 48 benchmark replies, their usage files and the grading rows are in [runs/](runs/), and the commands to rerun the benchmark are under [Reproduce](#reproduce).

## Results at a glance

![Codex and Claude compared on four measures: planted blockers found, usable reviews returned, extra valid findings per review, and median time per review](docs/results.svg)

1. **A fresh reviewer finds real problems.** On three of my own project plans, the two reviewers raised 20 distinct issues and I accepted all 20. Claude raised 18 of them and Codex 6. Only 4 were raised by both. ([pilot](docs/benchmarks.md))
2. **On planted flaws the two reviewers tied.** Both found all 18 planted blockers in every completed review. The test is too easy to separate them on this measure.
3. **They differ in speed, reliability and depth.** Codex took 7.1 s per review and always returned a usable reply. Claude took 17.9 s and 3 of its 24 replies broke the required format. Claude wrote about twice as many extra findings that held up (1.8 per review against 0.7).
4. **The token gap I had measured came from the setup, not the model.** In the pilot, Claude used 7.6 times the tokens of Codex. That was Claude Code loading its own startup context into every subagent. Run as a standalone process, Claude used about one sixth of Codex's tokens (2,417 against 14,184 median).

**What I do with this:** Codex reviews every plan by default because it is fast and reliable. When a mistake would be expensive (money, safety, a public release, something hard to undo), the skill recommends Claude and asks me first.

## How it was tested

![The benchmark in five steps: freeze 12 plans, run both reviewers, hide the reviewer names, grade each finding, count](docs/how-it-works-benchmark.png)

- **12 synthetic plans in six matched pairs.** One plan in each pair has two planted flaws (9 blockers and 3 major issues in total). The other is the same plan with the flaws repaired. The repaired plan checks whether a reviewer drops a claim once the problem is fixed.
- **Frozen before the first call.** Plans, answer key, [scoring rules](evals/plan-review/scoring.md) and stakes labels were committed before any reviewer ran.
- **Each reviewer read each plan twice** (48 calls, 2026-11-19), from an empty temporary folder with tools off. No failed call was rerun.
- **Graded blind.** Reviews were copied under random names, and the grader saw no reviewer names or usage data. The grader is an AI, not a person. Every finding has one row with a reason.

| Measured on the full runs | Codex (low effort) | Claude (medium effort) |
| --- | ---: | ---: |
| Reviews that passed the format check | 24 / 24 | 21 / 24 |
| Planted blockers found | 18 / 18 | 18 / 18 |
| Repaired plans where the old flaw was still claimed | 2 / 12 | 0 / 9 |
| Extra findings judged valid | 17 | 37 |
| Extra findings judged unsupported | 12 | 19 |
| Median wall time per review | 7.1 s | 17.9 s |
| Median reported tokens per review | 14,184 | 2,417 |
| Cost reported by the CLI | not reported | $0.058 median |

- [Full results, failures and limits](docs/portfolio-results.md)
- [Raw reviews, usage files and grading rows](runs/)
- [Earlier pilot on three real plans](docs/benchmarks.md)

## What this does not show

- **It is not independent validation.** The plans are synthetic and were written with AI help. Twelve plans is a small set, and two reads of the same plan are related.
- **No person checked the grading.** The grader is Claude, which is also one of the two reviewers. Two blind grading passes over the Codex findings agreed on 47 of 55.
- **It does not say which reviewer catches more blockers.** Both hit the ceiling. The case for Claude on important plans rests on the extra findings, not on recall.
- **Dollar cost is unknown for Codex.** Its CLI does not report cost, and tokens are not dollars.
- **Effort settings differ** (Codex low, Claude medium), as the skill ships them. I reran Codex at medium to check: it took twice as long (13.9 s), found the same 18 of 18 blockers, and did not add valid findings (12 against 17 at low, within grading noise). Claude's lead in extra findings is not explained by the effort setting. ([follow-up](docs/portfolio-results.md#follow-up-codex-at-medium-effort)) The Codex CLI did not report which model it used.
- **In the pilot I accepted every issue**, so it shows which reviewer raised more, not which was more often right.

## Try it

Clone this repository or extract GitHub's **Download ZIP**. From the repository root, open your preferred CLI. You need Python 3.9+ and a signed-in CLI for each writer or reviewer you use. For the default reviewer, install [Codex CLI](https://developers.openai.com/codex/cli) and run `codex login`. To use Claude as a writer or reviewer, install [Claude Code](https://code.claude.com/docs/en/quickstart) and sign in.

| Goal | Claude Code chat | Codex chat |
| --- | --- | --- |
| Let the skill pick or ask | `/challenge Plan a weekly attendance log` | `$challenge Plan a weekly attendance log` |
| Choose a deeper Claude review | `/challenge claude <idea>` | `$challenge claude <idea>` |
| Get two independent opinions | `/challenge both <idea>` | `$challenge both <idea>` |
| Compare reviewers with repeated runs | `/challenge measure <idea>` | `$challenge measure <idea>` |

You can also enter just the skill name to use the current discussion, or supply a Markdown plan path. Prefix with `codex` to explicitly use Codex, including for consequential plans.

### Use it in another project

Copy the [entire skill folder](.claude/skills/challenge/) into the appropriate location. Keep `SKILL.md` and its supporting files together, then start a fresh session.

| Client | One project | All your projects |
| --- | --- | --- |
| Claude Code | `.claude/skills/challenge/` | `~/.claude/skills/challenge/` |
| Codex | `.agents/skills/challenge/` | `~/.agents/skills/challenge/` |

## How it works

![One run in nine steps: you ask, the writer drafts a plan, a reviewer is picked, a fresh review runs with tools off, the reply is format-checked, every issue gets a decision, the plan is revised, one recheck runs if there was a blocker, and the skill stops and reports](docs/how-it-works-run.png)

The same visual with the benchmark and the folder map, as a two-page PDF: [how-it-works.pdf](docs/how-it-works.pdf).

- **Fixed call budget.** The regular route uses one reviewer call. A blocker can trigger one recheck. `both` makes two independent calls on the same draft, and `measure` makes four.
- **Isolated review.** Each reviewer starts in a temporary directory and receives the frozen plan and rubric. The runner disables shell tools in Codex and tools in Claude, validates the reply format and keeps per-run usage fields. Remove secrets before sending plan text to a provider.
- **Never an invented review.** A reply that fails the format check is recorded as a failure and the plan is marked not challenged. The raw reply is kept.
- **Audit trail.** The output folder keeps `plan-v1.md`, the original critiques, `decisions.md`, and the revised `plan.md`. The skill stops at planning.

For a real example, read the [camera-swap decision log](challenge/shot-tracker-new-camera/decisions.md) from my soccer shot tracker, where the two reviewers disagreed.

## Reproduce

23 offline tests cover both CLI adapters with no model calls. The dry run prints the benchmark plan without calling a reviewer.

```sh
python -B -m unittest discover -s tests -v
python evals/plan-review/run_benchmark.py --suite full --dry-run
```

The live commands and the scoring steps are in the [benchmark folder](evals/plan-review/) and the [client verification guide](docs/verification.md). Each run keeps plan and rubric hashes, CLI versions, usage and failures.

## How this was built

I set the question, the constraints and the stop rules, and I judged the issues on my own plans. Claude Code and ChatGPT (through Codex CLI) did most of the implementation and wrote the synthetic plans. Every number on this page comes from a saved run in this repo.

## License

[MIT](LICENSE)
