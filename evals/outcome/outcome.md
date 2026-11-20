# Outcome test: rules frozen before the first call

Written 2026-11-20, before any call below. The prompts and limits are constants in [outcome.py](outcome.py). The six tasks and their hidden tests are in [tasks/](tasks/).

The earlier benchmarks count review findings. None of them checks whether the thing that gets built is any better. This test does: a model writes code, hidden tests run it, and the code either passes or it does not. No AI grades anything.

## The question

Does a plan, or a plan reviewed by `/challenge`, make the first build pass more often than plain chat, and does it save enough reprompts to pay for its extra tokens?

## Tasks

Six small Python functions, one from each topic of the plan benchmark (photogate timer, attendance sheet, store forecast, highlight recall, shop inventory, tracker coordinates). Each prompt is short, the way a user would type it, and names the function. Each task has one trap that a careful reading of the prompt reveals (for example, a 16-bit counter that wraps around during a sprint). The hidden tests check the trap and the easy cases. [tests/test_outcome.py](../../tests/test_outcome.py) proves offline that a correct answer passes every hidden test and the naive answer fails.

## Four ways to get the code

The builder is always a fresh Claude (medium effort, tools off). Each way runs every task twice: 12 runs per arm, 48 in total.

| Arm | What happens before the build | Calls before the build |
| --- | --- | ---: |
| `plain` | Nothing. The task prompt goes straight to the builder | 0 |
| `better` | A fresh Claude gets the prompt and "Make this prompt better." The builder gets only the improved prompt | 1 |
| `plan` | A fresh Claude writes a plan in the skill's format. The builder gets the prompt and the plan | 1 |
| `challenge` | The same plan step, then Codex (low effort) reviews the plan with the skill's real rubric, then a fresh Claude revises the plan with the frozen revise prompt. The builder gets the prompt and the revised plan | 3 |

`plan` is a control arm. It separates the effect of writing a plan from the effect of having it reviewed.

If the Codex review fails or breaks the format, the run is marked `NOT CHALLENGED` and builds from the unrevised plan, as the skill does. There is one review round and no recheck.

## Build, test, reprompt

1. The builder replies with one Python code block. The harness takes the last `python` block.
2. The code and the hidden tests run in an empty temporary folder (`python -I -B`, 10 s limit).
3. If a test fails, a fresh builder call gets the same input again, plus its previous code and one line that names the first failing case, the way a user reports a bug ("wrong time for start_tick=60000, stop_tick=4464"). It never sees the expected value or the test code.
4. At most 10 reprompts. A run that still fails is unsolved.

A model call that fails is logged, is not rerun, and leaves the run unsolved.

## Measures

- Runs that pass on the first build, out of 12 per arm.
- Reprompts needed until the code passed.
- Reported tokens per run and per solved task, split into prepare, review, revise, build and reprompt. Codex: input plus output. Claude: input, cache read, cache creation and output.
- Wall time per run.
- Break-even (computed): tokens spent before the build, divided by the measured tokens of one reprompt. That is how many reprompts the preparation has to save to pay for itself.

## Decision rule, fixed in advance

If `challenge` beats `plain` by fewer than 2 of 12 on first-build passes and does not need fewer reprompts in total, the README will say that the workflow is not worth its tokens on small coding tasks.

If `challenge` does not beat `plan` by at least 2 of 12, the README will say that the review step added nothing measurable here beyond writing the plan.

## Limits fixed in advance

- Six tasks, two related repeats each. Only a large effect can show.
- The tasks are single functions with all needed facts in the prompt. A plan cannot ask the user a question here, which is one of the main things a plan does in real work.
- Claude wrote the tasks, the traps and the hidden tests, and Claude is the builder. If the builder passes everything on the first build, the test has hit its ceiling and says nothing about harder work.
- A reprompt here is a fresh call with a precise bug report. Real reprompts in a long chat are longer and vaguer, so the real cost of a reprompt is likely higher than measured here (assumption, not measured).
- Tokens are not dollars. Codex does not report cost.
- The code a model writes is run on this machine: standard library only, temporary folder, 10 s limit, no other sandbox.
