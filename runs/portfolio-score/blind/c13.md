VERDICT: BLOCKED

### 1. [blocker] Tuning and evaluation share recordings
- Failure: Step 3 assigns windows from the same recording to both tuning and evaluation, so the evaluation data is not "unseen source recordings" and the gains are inflated by leakage.
- Fix: Split at the recording level (e.g. 6 tuning, 6 evaluation), so all windows from a recording stay on one side.

### 2. [blocker] Recall double-counts moments
- Failure: Step 4 counts every overlapping clip as a true positive, so three clips on one moment score 3. This violates the brief's count-once rule and recall can exceed 1.
- Fix: Count the distinct ground-truth moments overlapped by any of the three clips, then divide by the number of labeled moments.

### 3. [major] Scoring unit does not match the split unit
- Failure: Step 3 splits by window, but Step 4 scores three clips per whole recording, so scoring would include tuning windows. Highlights that straddle window boundaries are also undefined.
- Fix: With the recording-level split, score whole evaluation recordings only and drop windows from the scoring.

### 4. [major] New editor is not frozen before evaluation
- Failure: Step 2 freezes the baseline, prompts and overlap rule, but not the new editor's configuration. Tuning comes after the freeze, so the editor can still be adjusted after evaluation results are seen.
- Fix: Reorder to split, tune, freeze both editors, then run the evaluation once.

### 5. [major] No decision rule
- Failure: The plan reports paired differences but sets no threshold or test. With few recordings, "improves" becomes a post hoc judgment.
- Fix: Pre-register a criterion, such as mean paired difference above zero with a bootstrap or sign-test bound.
