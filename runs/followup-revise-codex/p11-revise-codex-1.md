# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. Collect 12 public long-form recordings and label highlight time spans before running either editor.
2. Freeze the baseline, text prompts and overlap rule. Report paired recall differences by recording.
3. Before any tuning, randomly assign whole source recordings to tuning or evaluation. Create six windows per recording, and keep all windows from a recording in that recording's split, so no evaluation recording contributes any window to tuning.
4. For each evaluation recording, score the three proposed clips. Count the distinct labeled moments overlapped by any of the top three clips, so each moment counts once however many clips overlap it and a clip overlapping several moments credits each of them. Divide that count by the total number of labeled moments in that recording.
