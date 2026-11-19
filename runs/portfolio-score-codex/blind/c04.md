VERDICT: PROCEED WITH CHANGES
### 1. [major] No rule for deciding improvement
- Failure: Reporting paired recall differences leaves the decision undefined when gains vary across recordings or the average gain is small.
- Fix: Before evaluation, specify how to aggregate paired differences and what result will count as improvement.

### 2. [major] Ambiguous overlap assignment can change recall
- Failure: If one clip overlaps moments A and B and another overlaps only A, a greedy assignment can count one hit where two are possible.
- Fix: Use maximum-cardinality one-to-one matching under the frozen overlap rule.

### 3. [major] The evaluation split can leave recall undefined
- Failure: The source-level split can put every positive-label recording in tuning, leaving no evaluation recordings on which to compute recall.
- Fix: Use the existing labels to reserve a prespecified number of positive-label recordings for evaluation before tuning.
