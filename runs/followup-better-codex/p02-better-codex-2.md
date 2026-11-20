# Clip ranking evaluation

## Objective

Measure whether the new editor improves top-3 recall over a fixed baseline on held-out source recordings. Each proposed clip can match at most one labeled highlight, and each highlight can count at most once.

## Dataset and labels

1. Select 12 public long-form source recordings using predefined eligibility criteria. Group duplicate uploads and excerpts from the same underlying recording so they stay in the same split.
2. Label highlight spans before viewing outputs from either editor. Use a shared rubric, resolve ambiguous boundaries, and record which sources contain no qualifying highlights.
3. Assign whole source groups to tuning or evaluation before creating any windows. Record the split and include both positive- and zero-highlight recordings in evaluation. Keep evaluation labels out of tuning. Generate windows within each split and retain their source timestamps.

## Evaluation protocol

4. Freeze the baseline before tuning. Use the tuning set to finalize the new editor, then record both versions, their prompts and settings, windowing and ranking procedures, and the overlap metric and threshold before running the held-out evaluation.
5. Run both editors on the same evaluation recordings. For each editor and recording, rank proposals across all windows and retain up to three clips. Use a fixed tie-break and return fewer clips when fewer are available.
6. Build eligible clip–highlight pairs using the frozen overlap rule. Find the one-to-one assignment that maximizes the number of matches. For each recording with at least one highlight, compute recall@3 as matched highlights divided by labeled highlights. On zero-highlight recordings, count every returned clip as a false positive and leave recall undefined.

## Reporting and decision

7. Report each positive recording’s label count, matched count and recall@3 for both editors, and the paired difference in percentage points. Use the mean paired difference across positive recordings as the primary result. For zero-highlight recordings, report the number of false-positive clips per recording and the fraction of recordings with any false positive.
8. Before opening the held-out results, set the minimum recall gain and the maximum acceptable increase in false positives. Apply those criteria to the paired results. Report the evaluation sample sizes and how much the mean gain changes when each positive recording is omitted in turn. Treat a result driven by one recording as inconclusive.
