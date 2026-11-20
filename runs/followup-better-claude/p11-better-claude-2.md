# Clip ranking evaluation

## Brief

Decide whether the new editor improves top-3 recall over a fixed baseline on unseen source recordings. A ground-truth moment counts once, even if several proposed clips overlap it.

## Implementation

1. **Collect and label.** Collect 12 public long-form recordings and label highlight time spans before running either editor.
2. **Split by recording, not by window.** Randomly assign whole recordings to tuning or evaluation (e.g. 4 tuning, 8 evaluation), stratified by highlight count where possible. No evaluation recording, or any window of one, may be used for tuning, because otherwise the evaluation recordings are not unseen.
3. **Freeze before any evaluation run.** Record a version or hash for each of these:
   - the baseline
   - the text prompts
   - the overlap rule: the minimum overlap that counts as a match, and how a clip spanning two moments is handled
   - the scoring script
   - the decision rule from step 6
4. **Tune only on tuning recordings.** Adjust the new editor on the tuning set, then freeze it too. After that, nothing changes.
5. **Score each evaluation recording.** Run both editors once on each full recording and take the three proposed clips from each.
   - Recall is the number of distinct labeled moments overlapped by at least one of the three clips, divided by the number of labeled moments in that recording.
   - A moment hit by several clips counts once.
   - Check the scoring script on a hand-built case where two clips overlap the same moment.
6. **Report and decide.**
   - Report the paired recall difference (new minus baseline) for each evaluation recording, plus the mean difference and a paired bootstrap interval, or a sign-test count of wins, ties and losses.
   - Apply the pre-frozen decision rule, e.g. "improved" only if the mean difference is positive and the interval excludes zero.
   - State that with about 8 evaluation recordings, only large differences are detectable. Otherwise report the result as inconclusive.
