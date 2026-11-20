VERDICT: BLOCKED
### 1. [blocker] Tuning and evaluation share source recordings
- Failure: Splitting windows within each recording lets tuning and evaluation use the same sources, so the evaluation cannot measure recall on unseen recordings.
- Fix: Assign whole recordings to tuning or evaluation, and keep all windows from each recording in its assigned split.

### 2. [blocker] Recall counts clips instead of distinct moments
- Failure: When several top-three clips overlap the same labeled moment, each clip adds a true positive. This inflates recall and can push it above 100%.
- Fix: Count each labeled moment once if any of the top three clips overlaps it under the frozen rule, then divide by the total number of labeled moments in that recording.
