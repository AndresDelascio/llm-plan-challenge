## Brief
- Goal: I have one measured answer to "does the shot analyzer still work from a camera position it was never developed on?", given as outcome accuracy on new hand-labelled footage and compared against a pass line fixed before recording.
- Constraints: One person, a mechanical engineer, not a trained software engineer. An existing Python/OpenCV desktop app analyzes a recorded video of soccer shots at a goal: it finds each kick, decides the outcome (goal, miss, woodwork) and estimates ball speed. Existing benchmark: 29 videos, 369 shots I labelled by hand, all from one facility and similar camera positions. With the newest outcome engine switched on: 367 kicks found, 338 outcomes right (92%), 1 false kick, median speed difference to my labels 11.8%. The user clicks the ball once per video before analysis. A benchmark script already scores a folder of labelled videos. Recording gear: one phone on a tripod. Project rule: no tuning on footage that is used to report results.
- Non-goals: No changes to the analyzer. No tuning of thresholds. No live or real-time mode. No new camera hardware.

## Plan
1. Before recording, write down the pass line: on the new footage, at least 95% of kicks found, at least 85% of outcomes right, and no more than 1 false kick per 50 shots. Also write down what counts as a different camera position: the other side of the goal, at least 3 m from any earlier tripod spot, and a different height.
2. Tag the current code commit. All runs in this plan use that tag.
3. Record 3 sessions from the new position, about 20 shots each (about 60 shots), at the same resolution and frame rate as the benchmark videos, with a mix of goals, misses and woodwork.
4. Label every shot by hand in the app's manual mode (kick frame, goal-line crossing frame, outcome) before running any automatic analysis on that video, so the automatic result cannot influence my labels.
5. Run the analyzer on the 3 videos twice: engine off and engine on. Score both with the existing benchmark script.
6. Write one report: kicks found, outcomes right, false kicks and speed difference for the new footage next to the 29-video numbers, with pass or fail against step 1.
7. Group every wrong shot by cause (calibration, ball lost, wrong crossing frame, other). No fixes in this plan.
8. Store the new videos and labels as a separate set that is never used for tuning.
9. Done when the report exists with a pass or fail and the list of wrong shots by cause.

## Risks I already know about
- 60 shots is a small sample; one or two shots move the percentage by several points.
- My hand labels can be wrong, especially the crossing frame used for speed.
- Light, background and goal size at the new spot may differ from the benchmark for reasons other than camera position.
- The single ball click is done by me and may be easier or harder at the new position.
