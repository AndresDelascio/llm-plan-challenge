# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. **Collect and label.** Collect 12 public long-form recordings. Label highlight time spans before running either editor, following written labeling guidelines, with the labeler having seen no editor output. Record which recordings have no highlights (negative-label).
2. **Split by recording.** Assign entire source recordings to tuning (4) or evaluation (8) before creating windows, so all windows from a recording land on the same side. Make the assignment random with a recorded seed, and ensure both sides contain positive-label recordings.
3. **Freeze before touching evaluation.** Tune the new editor on the tuning recordings only. Then freeze and write down:
   - the baseline version, the new editor's configuration, and the text prompts;
   - the overlap rule, including its numeric threshold;
   - the decision rule in step 6;
   - random seeds, if either editor is non-deterministic.

   Make no changes after the first evaluation run.
4. **Run both editors.** Run each editor on every evaluation recording with identical inputs. Take each editor's own top three ranked clips. If an editor returns fewer than three, score what it returns without padding.
5. **Score each recording.**
   - **Matching:** match the three proposed clips to the labeled moments one-to-one using the frozen overlap rule. Use a maximum matching rather than a greedy one, so the count does not depend on clip order.
   - **Recall:** on positive-label recordings, divide unique matches by the number of labeled moments. Recall cannot exceed 3 divided by the number of moments, so report the moment count beside each recall.
   - **Negative-label recordings:** recall is undefined here, so report the number of proposed clips (all false positives) per editor and keep them out of the recall figures.
6. **Decide and report.**
   - **Per recording:** report paired recall (new, baseline, difference) for each positive-label evaluation recording.
   - **Summary:** report the mean paired difference with a 95% bootstrap confidence interval, resampling recordings.
   - **Decision:** conclude "improves" only if the interval lies above zero. Otherwise conclude "no improvement demonstrated", and state that roughly eight recordings can detect only large effects.
   - **False positives:** report the negative-label results separately, and flag it if the new editor is worse there.
