# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Decision rule (fixed before any evaluation run)

- **Unit of analysis:** the recording, not the window or clip.
- **Primary metric:** per-recording top-3 recall on evaluation recordings that have at least one labeled moment.
- **Criterion:** the new editor "improves" only if the mean paired recall difference (new − baseline) is positive and a paired bootstrap 95% interval over recordings excludes zero.
- **Otherwise:** report the result as inconclusive, not as a win. With this few recordings, only a large effect is detectable.

## Implementation

1. **Collect and label.**
   - Collect 12 public long-form recordings.
   - Write down the highlight definition and the labeling instructions first.
   - Label highlight time spans (start and end) before running either editor on any recording.
   - Record explicitly which recordings have no highlights.
   - Do not change labels once any editor output has been seen.

2. **Split by recording.**
   - Assign whole recordings to tuning (4) or evaluation (8) before creating any windows.
   - Make the assignment random with a recorded seed, or stratify it by recording length and label count.
   - All windows from a recording stay on its side of the split.
   - Evaluation recordings are not used for tuning, prompt writing or choosing the overlap rule.

3. **Tune, then freeze.**
   - Tune the new editor on the tuning recordings only.
   - Before touching the evaluation recordings, freeze and record:
     - the baseline version and configuration;
     - the new editor's configuration;
     - the text prompts;
     - the overlap rule (for example, the exact threshold and how ties are broken);
     - the scoring script.

4. **Run once.**
   - Run both editors on the same evaluation recordings with identical inputs.
   - Take each editor's three highest-ranked clips per recording.
   - If an editor returns fewer than three, score what it returned without padding.
   - Do not rerun or adjust anything after seeing evaluation scores; any rerun is reported as such.

5. **Score.**
   - For each recording and each editor, match the three proposed clips to the labeled moments one-to-one using the frozen overlap rule.
   - Use a maximum matching, so that no clip and no moment is counted twice.
   - Recall is unique matches divided by the number of labeled moments.
   - When a recording has more than three labeled moments, the maximum recall is 3/n. This applies equally to both editors, so note it but do not correct for it.
   - Recordings with no labeled moments have no defined recall. Exclude them from the recall metric and count the clips proposed on them as false positives.

6. **Report.**
   - A per-recording table: number of labeled moments, baseline recall, new recall and paired difference.
   - The mean paired difference with its bootstrap interval, and the count of recordings improved, tied and worsened.
   - False positives on negative-label recordings, reported separately for each editor.
   - The decision under the rule above.
