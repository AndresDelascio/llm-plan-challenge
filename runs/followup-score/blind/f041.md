# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. Collect 12 public long-form recordings and label highlight time spans before running either editor.
2. Randomly assign whole recordings to tuning (4) or evaluation (8). No recording contributes material to both sets, so the evaluation recordings are truly unseen.
3. Tune the new editor on the tuning recordings only. Then freeze the baseline, the new editor, the text prompts, the overlap rule and the decision rule (for example, mean paired recall difference > 0, with the per-recording results shown) before either editor touches the evaluation recordings.
4. Run both editors once on each evaluation recording and take the three proposed clips from each.
5. Score each editor on each recording as the number of distinct labeled moments overlapped by at least one of the three clips, divided by the number of labeled moments. Several clips hitting the same moment count once.
6. Report the paired recall difference (new minus baseline) for each evaluation recording and the mean difference, then apply the frozen decision rule. With only 8 recordings, present the result as indicative, not conclusive.
