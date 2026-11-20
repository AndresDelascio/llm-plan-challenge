# Clip ranking evaluation

## Objective

Measure whether the new editor improves top-3 recall over a fixed baseline on source recordings held out from tuning. Count each ground-truth highlight at most once per editor.

## Protocol

1. **Split by source recording.** Collect 12 public long-form recordings and label highlight time spans before running either editor. Assign four recordings to tuning and eight to evaluation with a fixed random seed. Keep all windows from each recording in the same split. Group duplicate or alternate versions of the same source before splitting, and ensure every evaluation recording has at least one labeled highlight.
2. **Fix inputs and scoring.** Give both editors the same input for each recording. If processing requires six windows, use identical boundaries for both editors, map their candidates back to source timestamps, and select three clips per recording using each editor’s ranking procedure. Freeze the baseline, prompts, ranking and tie-breaking procedures, and temporal overlap threshold before opening the evaluation set. Use only the tuning recordings to refine the new editor.
3. **Score the held-out recordings once.** For each editor and recording, count the distinct labeled highlights that meet the overlap threshold with at least one of the three selected clips. Divide that count by the total number of labeled highlights in the recording.
4. **Report paired results.** Show both recall scores and the new-minus-baseline difference for each recording. Use the mean paired difference, in percentage points, as the primary result and report a 95% confidence interval that resamples whole recordings. If the interval spans zero, report the result as inconclusive.
