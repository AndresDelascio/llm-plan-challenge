# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. Collect 12 public long-form recordings and label highlight time spans before running either editor.
2. Randomly assign whole recordings to tuning (6) or evaluation (6). No recording contributes data to both sides.
3. Tune the new editor on the tuning recordings only.
4. Before running anything on the evaluation recordings, freeze the baseline, the new editor's configuration, the text prompts, the overlap rule and the decision rule. The decision rule is that the new editor improves if the mean paired recall difference (new minus baseline) across evaluation recordings is above zero and the lower bound of its 95% bootstrap interval is also above zero.
5. Run both frozen editors once on each whole evaluation recording. For each recording and editor, take the three proposed clips and count the distinct ground-truth moments overlapped by at least one of them. Divide that count by the number of labeled moments in the recording.
6. Report paired recall differences by recording and apply the frozen decision rule.
