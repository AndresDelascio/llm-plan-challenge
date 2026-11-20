# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. Collect 12 public long-form recordings and label highlight time spans before running either editor.
2. Freeze the baseline, text prompts and overlap rule. Report paired recall differences by recording.
3. Create six windows per recording. Randomly assign whole recordings to tuning or evaluation, keeping all six windows from a recording in the same partition, so that no evaluation recording is seen during tuning.
4. For each editor and each evaluation recording, score its top three proposed clips. Count the distinct labeled moments overlapped by any of the three clips, so a moment overlapped by several clips counts once. Divide that count by the total number of labeled moments in the recording.
