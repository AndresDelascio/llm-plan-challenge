VERDICT: BLOCKED

### 1. [blocker] Tuning and evaluation share recordings
- Failure: Step 3 splits windows within each recording, so every evaluation window comes from a recording seen in tuning. This breaks the "unseen source recordings" requirement.
- Fix: Assign whole recordings to tuning or evaluation, never windows.

### 2. [blocker] Overlapping clips double-count a moment
- Failure: Step 4 counts every clip that overlaps a ground-truth moment as a true positive. Three clips on one moment score 3, inflating recall (possibly above 1) and contradicting the brief.
- Fix: Count distinct ground-truth moments matched by at least one clip, then divide by labeled moments.

### 3. [major] No decision rule and very few evaluation recordings
- Failure: The plan reports paired differences but never says what counts as "improves". After a recording-level split, only around six pairs remain, so almost any result is ambiguous.
- Fix: Pre-register the decision criterion (e.g. mean paired difference with a bootstrap confidence interval excluding zero) and either add recordings or keep most of the 12 for evaluation.

### 4. [major] New editor is not frozen before evaluation
- Failure: Step 2 freezes the baseline, prompts and overlap rule, but not the new editor. It can be adjusted after evaluation results are seen.
- Fix: Freeze the new editor's configuration after tuning and before any evaluation run.

### 5. [minor] Scoring unit and denominator undefined
- Failure: Step 3 creates windows but step 4 scores per recording. Recordings with zero moments divide by zero, and those with more than three cap recall below 1.
- Fix: State the scoring unit, exclude zero-moment units, and note the ceiling of 3/N.
