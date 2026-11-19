VERDICT: BLOCKED
### 1. [blocker] Evaluation recordings leak into tuning
- Failure: Splitting by window allows tuning and evaluation to use the same source recording, so the evaluation cannot establish performance on unseen recordings.
- Fix: Split by source recording before tuning and keep all windows from each recording in the same split.

### 2. [blocker] Clip counts distort top-3 recall
- Failure: Multiple clips overlapping one labeled moment inflate recall, and one clip overlapping several labeled moments can undercount recall.
- Fix: Divide the number of distinct labeled moments overlapped by any of the top three clips by the total number of labeled moments in that recording.
