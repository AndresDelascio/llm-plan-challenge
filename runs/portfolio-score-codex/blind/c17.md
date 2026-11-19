VERDICT: BLOCKED
### 1. [blocker] Source recordings leak into evaluation
- Failure: Splitting windows lets the same recording appear in tuning and evaluation, so the evaluation does not measure performance on unseen recordings.
- Fix: Split by source recording and keep all six windows from each recording in the same partition.
### 2. [major] Duplicate clips inflate recall
- Failure: If multiple top-three clips overlap the same labeled moment, each clip adds a true positive and recall can exceed 100%.
- Fix: For each editor and evaluation recording, divide the number of distinct labeled moments overlapped by any of its top three clips by the total number of labeled moments.
