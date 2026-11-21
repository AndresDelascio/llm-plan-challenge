# Missing-fact outcome test: rules frozen before the first call

Written 2026-11-20, before any call below. The prompts and limits are constants in [outcome.py](outcome.py) (`PLAN_ASK`, `BUILD_ASK`, `ANSWERS`, `SUITES`).

The [first outcome test](outcome.md) gave every needed fact in the prompt, and plain chat passed all 12 first builds. That test could not show the main thing a plan does in real work: notice what it does not know and ask. This test removes those facts.

## The question

When the prompt leaves out a fact the code needs, does writing a plan (or a reviewed plan) get the fact from the user more often than plain chat that is allowed to ask?

## Tasks

The same six functions and the same hidden tests as the first outcome test. The prompts in [tasks-missing/](tasks-missing/) leave out the facts that the hidden tests check (the timer's tick rate and width, the time-zone offsets, what to do with short history, how clips are credited, when a reservation expires, the crop geometry). Each `*_facts.txt` holds what was removed, written before any call. Some facts can be guessed (ISO dates with offsets); most cannot (300 seconds, 10,000 ticks per second).

## The simulated user

The user answers only when asked, and always with the whole facts sheet for that task. One question of any kind is enough. This is generous to the arms that ask, and it is fixed so that no AI decides what the user says.

- **A plan asks** when its `## Questions for the user` section contains a `?`.
- **A chat reply asks** when it contains a `?` and no Python code block.

## Four ways to get the code

The builder is always a fresh Claude (medium effort, tools off). Each way runs every task twice: 12 runs per arm, 48 in total.

| Arm | What happens before the build |
| --- | --- |
| `plain` | Nothing. The prompt goes straight to the builder, which is told to reply with code. It cannot ask |
| `ask` | The builder is told to ask if a fact is missing, otherwise to write the code. If it asks, it gets the answers and builds. If it writes code, that reply is its first build |
| `plan` | A fresh Claude writes a plan with a fourth heading, `## Questions for the user`. If it asks, the builder gets the prompt, the plan and the answers |
| `challenge` | The same plan, then Codex reviews it with the skill's rubric, then a fresh Claude revises it with the frozen revise prompt. The questions are read from the revised plan |

The first test's `better` arm is left out: it has no way to ask. `ask` is the fair rival to planning here, since both are told that questions are allowed.

## Build, test, reprompt

As in the first test (`python -I -B`, 10 s limit, hidden tests on stdin, one-line symptom), with **at most 3 reprompts** instead of 10. A reprompt only names the failing case, so a fact that cannot be guessed is unlikely to be found by reprompting, and 10 would mostly burn calls. A failed model call is logged, not rerun, and leaves the run unsolved.

## Measures

- First builds that pass, out of 12 per arm.
- Runs that asked and were answered, out of 12 per arm.
- Runs solved within 3 reprompts, and reprompts used.
- Reported tokens per run and per solved run, and wall time.

## Decision rule, fixed in advance

1. **Floor check.** If `plain` passes 10 or more of 12 first builds, the facts were guessable and the test says nothing about asking.
2. If `plan` or `challenge` beats `ask` by at least 2 of 12 first-build passes, the README will say that a planning step surfaced missing facts that plain chat did not, and the skill gets a questions step.
3. If `ask` is within 1 of the better plan arm, the README will say that letting plain chat ask did as well as planning, and give the token ratio.
4. If `challenge` does not beat `plan` by at least 2 of 12, the README will say that the review step added nothing measurable here beyond writing the plan.

## Limits fixed in advance

- Six tasks, two related repeats each. Only a large effect can show.
- The simulated user is generous: any question unlocks every fact. A real user answers only what was asked.
- The skill itself has no questions step today. The `plan` and `challenge` arms here add one, so a win for them is a case for adding it to the skill, not evidence about the skill as it ships.
- Claude wrote the tasks, the facts sheets and the hidden tests, and Claude is the builder.
- Tokens are not dollars. Codex does not report cost.
- The code a model writes runs on this machine: standard library only, temporary folder, 10 s limit, no environment variables, no other sandbox.
