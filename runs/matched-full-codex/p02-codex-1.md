VERDICT: PROCEED WITH CHANGES
### 1. [major] Improvement decision is unspecified
- Failure: Paired differences can point in different directions, and the plan gives no rule for deciding whether the new editor improved recall.
- Fix: Prespecify the mean paired recall difference across positive evaluation recordings, the uncertainty interval, and the threshold for claiming improvement.

### 2. [major] Window outputs lack a recording-level ranking rule
- Failure: If editors return ranked clips per window, the plan leaves open how to select the three clips scored for the recording. Different merge rules can change recall.
- Fix: Freeze how each editor’s window outputs are mapped to recording timestamps and ranked into one top-three list, including tie handling.

### 3. [major] One-to-one matching can depend on order
- Failure: If one clip overlaps two moments and another clip overlaps only one of them, greedy matching can count one hit when two are possible.
- Fix: Use maximum-cardinality one-to-one matching among eligible clip–moment pairs.

### 4. [major] The holdout can contain no labeled moments
- Failure: A source-level split can put every positive recording in tuning, leaving evaluation recall undefined.
- Fix: Reserve positive recordings for evaluation using the existing labels before tuning begins.
