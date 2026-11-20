# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. Collect 12 public long-form recordings and label highlight time spans before running either editor.
2. Randomly assign whole recordings to tuning or evaluation, so that no recording contributes to both. Only recordings with at least one labeled moment are eligible for the evaluation set; this rule is fixed before any editor is run.
3. Freeze the baseline, text prompts, overlap rule and decision rule before any evaluation run. Tune the new editor on the tuning recordings only, then freeze its configuration before any evaluation run as well. The decision rule is that the new editor improves top-3 recall if the mean paired recall difference across evaluation recordings is above zero and its paired bootstrap confidence interval excludes zero.
4. For each evaluation recording, score the three proposed clips from each editor. Count the distinct labeled moments overlapped by at least one of the three clips, so each moment counts once, then divide by the number of labeled moments in that recording.
5. Report paired recall differences by evaluation recording, and apply the pre-specified decision rule.
