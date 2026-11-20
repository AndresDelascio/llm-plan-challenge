VERDICT: BLOCKED

### 1. [blocker] Centered average uses future sales
- Failure: The centered 14-day average includes sales after the forecast Monday, leaking future sales into evaluation and requiring data unavailable at deployment.
- Fix: Use the 14 most recent daily sales observations available at the Monday forecast cutoff.

### 2. [blocker] Imputation leaks held-out data
- Failure: Medians fitted on the full two-year file use observations from held-out periods, so earlier folds benefit from data unavailable at their forecast cutoffs.
- Fix: Fit medians on each fold’s training data and apply those same medians to its validation data.
