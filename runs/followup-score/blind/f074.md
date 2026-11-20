# Clip ranking evaluation

## Objective

Measure whether the new editor improves top-3 highlight recall over a fixed baseline on unseen source recordings. Each proposed clip and each labeled moment can contribute to at most one match.

## Dataset and tuning

1. Select 12 public long-form recordings using predefined inclusion criteria. Group duplicate uploads and excerpts from the same original recording so they stay in the same split.
2. Label highlight start and end times using a written rubric before running either editor. Resolve ambiguous labels and freeze the annotations. Explicitly mark recordings with no highlights.
3. Split by source recording before creating windows. Reserve eight recordings for evaluation and four for tuning, keeping positive-label recordings in both splits where possible. Keep evaluation recordings, annotations, and derived windows out of tuning.
4. Freeze the baseline, prompts, overlap criterion and threshold, ranking tie-breaker, and handling of failed runs before tuning. Tune the new editor only on the tuning split, then freeze its configuration before opening evaluation. Give both editors the same source recordings and apply the same scoring rules.

## Scoring

5. For each evaluation recording, take each editor’s three highest-ranked clips, or all clips if it returns fewer. If an editor ranks clips within windows, combine those results into a single recording-level ranking before selecting the top three.
6. Build a bipartite graph between the selected clips and labeled moments. Add an edge for each pair that satisfies the frozen overlap criterion. Use maximum-cardinality one-to-one matching to count hits.
7. On positive-label recordings, compute recall as matched moments divided by labeled moments. On recordings with no labeled moments, report the number of returned clips and the fraction of recordings with at least one returned clip. If the evaluation split contains no such recordings, report that false positives on negative recordings could not be measured.

## Reporting and decision

8. Report both editors’ recall and the paired difference for each positive-label recording. Use the mean paired difference, with equal weight per recording, as the primary result. Report the number of evaluation recordings contributing to each metric and summarize failures under the frozen rules.
9. Before viewing evaluation results, specify the minimum worthwhile recall gain and how uncertainty will inform the decision. Report a recording-level uncertainty interval for the mean paired difference, flag the limits of the small holdout, and call the result inconclusive if it cannot distinguish a worthwhile gain.
