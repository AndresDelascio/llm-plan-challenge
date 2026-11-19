VERDICT: BLOCKED

### 1. [blocker] Tuning and evaluation share recordings
- Failure: Step 3 splits windows within each recording, so every evaluation window comes from a recording also used for tuning. The result cannot show performance on unseen source recordings, and step 4's per-recording scoring would also span tuning windows.
- Fix: Assign whole recordings to tuning or evaluation, and score only the evaluation recordings.

### 2. [blocker] Overlapping clips double-count a moment
- Failure: Step 4 counts each overlapping clip as a true positive, so three clips on one moment score 3. This inflates recall, can push it above 1, and contradicts the brief.
- Fix: Count the distinct labelled moments overlapped by at least one of the three clips, then divide by the number of labelled moments.

### 3. [major] New editor is never frozen
- Failure: Step 2 freezes only the baseline, prompts and overlap rule. The new editor can keep being adjusted after evaluation results are seen, which biases the comparison.
- Fix: Freeze the new editor's configuration after tuning and before any evaluation run.

### 4. [major] No decision rule
- Failure: The plan reports paired differences but never defines what counts as "improves". With at most 12 recordings, noise can be read either way after the fact.
- Fix: Pre-specify the criterion before evaluation, such as a mean paired difference above zero with a paired bootstrap confidence interval that excludes zero.

### 5. [minor] Zero-moment recordings are undefined
- Failure: A recording with no labelled moments causes division by zero in step 4.
- Fix: Require at least one labelled moment per evaluation recording, or state an exclusion rule in advance.
