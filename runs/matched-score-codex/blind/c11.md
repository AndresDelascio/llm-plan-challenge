VERDICT: BLOCKED
### 1. [blocker] Evaluation recordings leak into tuning
- Failure: Splitting windows lets the same source recording appear in tuning and evaluation, so the measured gain does not establish improvement on unseen recordings.
- Fix: Split by source recording before tuning and keep every window from each held-out recording in evaluation.

### 2. [blocker] Recall counts clips instead of moments
- Failure: Several clips overlapping one moment inflate recall and can push it above 100%. A single clip covering multiple moments can also undercount recall.
- Fix: For each editor and held-out recording, count each labeled moment once if any of the top three clips matches it under the frozen overlap rule. Divide by the total labeled moments in that recording.
