VERDICT: PROCEED WITH CHANGES
### 1. [major] No rule for declaring improvement
- Failure: Paired differences can point in opposite directions, leaving no defined way to decide whether the new editor improves recall.
- Fix: Before evaluation, specify how to aggregate the paired differences and what result will count as improvement.
### 2. [major] Match order can change recall
- Failure: If one clip overlaps two labeled moments and another overlaps only one of them, greedy matching can count one hit when two are possible.
- Fix: Use maximum-cardinality one-to-one matching over all clip–label pairs that meet the frozen overlap rule.
### 3. [major] Top three across windows is undefined
- Failure: If editors return ranked clips per window, the plan does not say how those lists become three clips for the whole recording.
- Fix: Freeze how each editor’s window outputs are ranked together, then score only its first three clips per recording.
