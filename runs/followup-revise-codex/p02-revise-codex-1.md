# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. Collect 12 public long-form recordings and label highlight time spans before running either editor.
2. Freeze the baseline, text prompts and overlap rule. Before evaluation, also freeze the decision rule:
   - Aggregate as the mean of per-recording paired recall differences (new editor minus baseline) across positive-label evaluation recordings.
   - Call it an improvement only if that mean is above zero and a paired interval on it (e.g. paired bootstrap over recordings) excludes zero. Otherwise report that improvement was not shown.
   - Report the paired recall differences by recording alongside the aggregate, including how many recordings improved and how many regressed.
3. Assign entire source recordings to tuning or evaluation before creating windows. Use the existing labels to stratify the assignment, so that the evaluation set includes recordings with labeled moments and the recall comparison is defined. Freeze configuration after tuning and put all windows from an evaluation recording in evaluation.
4. For each recording, match the three proposed clips to the labeled moments one-to-one using the frozen overlap rule. Divide unique matches by the number of labeled moments. Report positive-label recordings and false positives on negative-label recordings separately.
