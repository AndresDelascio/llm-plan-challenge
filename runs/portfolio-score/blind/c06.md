VERDICT: PROCEED WITH CHANGES

### 1. [major] No decision rule and a very small evaluation set
- Failure: The brief requires a decision, but the plan only reports paired differences by recording. Of the 12 recordings, some go to tuning and some have no labelled moments, so only a handful of pairs remain. Any difference can then be read either way after the fact.
- Fix: Before tuning, fix the evaluation count and the decision criterion (for example, mean paired difference with a bootstrap interval excluding zero). State that an inconclusive result is a possible outcome.

### 2. [major] "Unseen" is not verified
- Failure: The recordings are public and the split method is unspecified. The new editor's earlier development may already have used an evaluation recording, or one from the same show or speaker as a tuning recording. Hand-picking the split can also favour the new editor. Either way, recall is inflated at evaluation.
- Fix: Assign recordings randomly, grouped by show or speaker, before running either editor. Exclude any recording previously used in developing the new editor.

### 3. [minor] Recall ceiling hides differences
- Failure: With three clips and a denominator of all labelled moments, a recording with more than three moments caps recall at 3/N. This compresses the paired differences when the sample is already small.
- Fix: Also report the unique match count per recording, or recall against min(3, N), alongside the stated metric.
