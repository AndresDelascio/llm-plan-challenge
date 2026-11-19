## Brief
- Goal: I have one measured answer to "does the shot analyzer still work from a camera position it was never developed on?", given as outcome accuracy on new hand-labelled footage and compared against a pass line fixed before recording.
- Constraints: One person, a mechanical engineer, not a trained software engineer. An existing Python/OpenCV desktop app analyzes a recorded video of soccer shots at a goal: it finds each kick, decides the outcome (goal, miss, woodwork) and estimates ball speed. Existing benchmark: 29 videos, 369 shots I labelled by hand, all from one facility and similar camera positions. With the newest outcome engine switched on: 367 kicks found, 338 outcomes right (92%), 1 false kick, median speed difference to my labels 11.8%. The user clicks the ball once per video before analysis. A benchmark script already scores a folder of labelled videos. Recording gear: one phone on a tripod. Project rule: no tuning on footage that is used to report results.
- Non-goals: No changes to the analyzer. No tuning of thresholds. No live or real-time mode. No new camera hardware.

## Plan
1. Before recording, write down the rules below. All numbers in this step are proposals until I confirm them.
   - Pass line, judged on the engine-on run only, with N = all labelled shots as the base for every count: kicks found at least 95% of N rounded up, outcomes right at least 85% of N rounded up, false kicks at most N divided by 50 rounded down. At N = 60 that is at least 57 found, at least 51 right, at most 1 false kick. The engine-off run is reported for information only.
   - Inconclusive band: if outcomes right lands from 3 below the line to 2 above it (48 to 53 at N = 60), the result is "inconclusive" and I record one more session and judge again on all shots. At most 2 extra sessions. After that the result stands as inconclusive.
   - Outcome mix: minimum counts for goals, misses and woodwork, taken from the split of the 369 benchmark shots scaled to 60, and never fewer than 5 of any outcome.
   - What changes and what does not: same goal and same ball as the benchmark. Only the tripod moves: the other side of the goal, at least 3 m from any earlier tripod spot, and a different height.
   - Run rules: one ball click per video, made before any result is seen and reused for both runs. One run per engine setting, and every run is logged. Every recorded shot counts. A shot can only be left out at labelling time, before any automatic run, with the reason written down.
2. Tag the current code commit. All runs in this plan use that tag.
3. Record 3 sessions from the new position, about 20 shots each (about 60 shots), at the same resolution and frame rate as the benchmark videos, meeting the outcome minimums from step 1. Take the tripod down and set it up again between sessions, inside the step 1 definition.
4. Label every shot by hand in the app's manual mode (kick frame, goal-line crossing frame, outcome) before running any automatic analysis on that video, so the automatic result cannot influence my labels.
5. Run the analyzer on the 3 videos twice: engine off and engine on. Score both with the existing benchmark script.
6. Write one report: kicks found, outcomes right, false kicks and speed difference for the new footage next to the 29-video numbers. Give outcomes right per session and per outcome, with the 95% interval beside the overall percentage, and pass, fail or inconclusive against step 1.
7. Group every wrong shot by cause (calibration, ball lost, wrong crossing frame, other). No fixes in this plan.
8. Store the new videos and labels as a separate set that is never used for tuning.
9. Done when the report exists with pass, fail or inconclusive and the list of wrong shots by cause.

## Risks I already know about
- 60 shots is a small sample; one or two shots move the percentage by several points.
- My hand labels can be wrong, especially the crossing frame used for speed.
- Light, background and goal size at the new spot may differ from the benchmark for reasons other than camera position.
- The single ball click is done by me and may be easier or harder at the new position.
