# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. Collect 12 public long-form recordings and label highlight time spans before running either editor. Exclude any recording previously used in developing the new editor, and replace it with one that was not.
2. Freeze the baseline, text prompts and overlap rule. Before tuning, also fix and record:
   - the number of evaluation recordings, including how many have labeled moments;
   - the decision criterion: the new editor improves top-3 recall only if the mean paired recall difference (new minus baseline) across positive-label evaluation recordings is above zero and its bootstrap interval excludes zero.

   Any other result is reported as inconclusive or no improvement, and an inconclusive result is a possible outcome. Report paired recall differences by recording.
3. Assign entire source recordings to tuning or evaluation at random, before running either editor and before creating windows. Group the assignment by show or speaker, so that recordings sharing a show or speaker land on the same side. Freeze configuration after tuning and put all windows from an evaluation recording in evaluation.
4. For each recording, match the three proposed clips to the labeled moments one-to-one using the frozen overlap rule. Divide unique matches by the number of labeled moments. Alongside this recall, report the unique match count and the number of labeled moments per recording, as description only; the decision uses the stated recall metric. Report positive-label recordings and false positives on negative-label recordings separately.
