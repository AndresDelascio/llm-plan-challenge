# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. Collect public long-form recordings and label highlight time spans before running either editor.
   - Start from 12 recordings and add more until the evaluation set has at least 10.
   - Confirm that no evaluation recording was used in developing either editor or its prompts. Replace any that were.
2. Freeze the baseline, text prompts and overlap rule. Before running either editor on the evaluation set, also fix and record:
   - the number of evaluation recordings;
   - the aggregate, which is the mean paired recall difference (new minus baseline) across positive-label evaluation recordings;
   - the decision rule, for example that the new editor "improves" only if a paired bootstrap confidence interval on the mean difference excludes zero, or a sign test passes a pre-set threshold.

   Report paired recall differences by recording alongside the aggregate and the outcome of the decision rule.
3. Assign entire source recordings to tuning or evaluation before creating windows.
   - Use a seeded random split, stratified by positive or negative label.
   - Record the seed and the resulting assignment before any tuning.
   - Freeze configuration after tuning.
   - Put all windows from an evaluation recording in evaluation.
4. Score each recording as follows.
   - Take each editor's three highest-ranked clips. If an editor returns fewer than three, count the missing clips as non-matches.
   - Match these clips to the labeled moments one-to-one, using maximum bipartite matching under the frozen overlap rule, so that each moment counts at most once.
   - Divide unique matches by the number of labeled moments.
   - Report positive-label recordings and false positives on negative-label recordings separately.
