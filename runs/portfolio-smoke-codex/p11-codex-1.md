VERDICT: BLOCKED
### 1. [blocker] Evaluation leaks source recordings
- Failure: Splitting windows allows the same recording to appear in tuning and evaluation, invalidating the test on unseen recordings.
- Fix: Split by recording before tuning and keep every window from a recording in the same split.

### 2. [blocker] Duplicate clips inflate recall
- Failure: Multiple top-three clips overlapping the same labeled moment each earn credit, so recall can exceed 100%. A clip covering multiple labeled moments also earns only one credit.
- Fix: Count each labeled moment once if any of the top three clips overlaps it, then divide by the number of labeled moments in the recording.
