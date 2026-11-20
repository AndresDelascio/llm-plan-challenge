VERDICT: BLOCKED
### 1. [blocker] Training labels can leak future sales

- Failure: A training forecast can start before a validation Monday while some of its seven target days are still unavailable at that Monday’s cutoff.
- Fix: Include a training example only when all seven target values were available at the fold’s forecast cutoff.

### 2. [major] Last-week baseline lacks a cutoff rule

- Failure: If prior-week sales finalize late, the baseline can use values that were unavailable when the forecast was issued.
- Fix: Use sales from the corresponding weekdays one week earlier as available at the same cutoff. Define a fallback for unavailable values before evaluation.

### 3. [major] Final holdout can influence candidate selection

- Failure: If the best candidate is selected on the final eight Mondays, its reported performance on those same Mondays can be optimistic.
- Fix: Select the candidate and hyperparameters on earlier folds, then evaluate the locked configuration on the final eight Mondays.
