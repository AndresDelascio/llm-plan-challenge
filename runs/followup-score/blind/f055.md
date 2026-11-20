# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. Collect 12 public long-form recordings and label highlight time spans before running either editor.
2. Freeze the baseline, text prompts and overlap rule. Before evaluation, also freeze the decision rule:
   - Aggregate the paired recall differences (new editor minus baseline) as their mean over the positive-label evaluation recordings.
   - Write down the result that will count as improvement, i.e. the minimum mean difference and how variation across recordings is handled (e.g. a paired confidence interval or sign test excluding zero).
   - Report the per-recording paired differences alongside the aggregate and the resulting decision.
3. Assign entire source recordings to tuning or evaluation before creating windows.
   - Using the existing labels, reserve a prespecified number of positive-label recordings for evaluation before any tuning, so recall is always defined on the evaluation set.
   - Freeze configuration after tuning.
   - Put all windows from an evaluation recording in evaluation.
4. For each recording, match the three proposed clips to the labeled moments one-to-one using maximum-cardinality matching under the frozen overlap rule, not greedy assignment, so that ambiguous overlaps cannot undercount hits. Divide unique matches by the number of labeled moments. Report positive-label recordings and false positives on negative-label recordings separately.
