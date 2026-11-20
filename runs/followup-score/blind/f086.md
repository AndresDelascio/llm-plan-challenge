# Clip ranking evaluation

## Objective

Determine whether the new editor improves top-3 highlight recall over a fixed baseline on unseen source recordings. Count each labeled highlight at most once per editor.

## Procedure

1. **Build the dataset.** Select 12 public long-form recordings and label highlight start and end times before running either editor. Use a written labeling rubric and ensure each recording has at least one labeled highlight. Keep duplicate and near-duplicate recordings in the same split.

2. **Split by source recording.** Using a fixed random seed, assign four recordings to tuning and eight to evaluation. If either editor needs windowed input, use the same six windows per recording for both editors and keep all windows from a recording in its assigned split. Define window boundaries in advance so the windows cover the full recording.

3. **Freeze the evaluation protocol.** Use only the tuning recordings to refine the new editor. Before running either editor on the evaluation recordings, lock both configurations, prompts, ranking and tie-breaking rules, and the minimum overlap required for a match. If the editors generate candidates per window, convert candidate timestamps to source time and apply the frozen ranking rules to select three clips per recording.

4. **Score unique highlights.** For each editor and held-out recording, count the labeled highlights that meet the overlap rule with at least one of the three selected clips. Divide by the total number of labeled highlights in that recording. Multiple clips that match the same highlight earn one credit in total.

5. **Report the paired results.** Show both recall scores and their difference in percentage points for each held-out recording. Use the mean of the eight paired differences as the primary result and report a 95% confidence interval based on the paired recording-level differences. If the interval includes zero, report the result as inconclusive.
