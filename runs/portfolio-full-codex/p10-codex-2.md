VERDICT: PROCEED WITH CHANGES
### 1. [major] Training labels can cross the Monday cutoff
- Failure: A training row can have an earlier forecast date while its seven-day sales target is still incomplete or unfinalized at the validation Monday. Using that row leaks future sales into the fit.
- Fix: Include a training row only once all seven target values were finalized by that fold’s Monday cutoff.

### 2. [major] The last-week baseline lacks a cutoff rule
- Failure: A baseline built from retrospectively finalized sales can use values that were unavailable on the forecast Monday, making the paired comparison unfair.
- Fix: Forecast each day from the same weekday one week earlier using the Monday snapshot, and specify a fallback for unavailable values before evaluating.

### 3. [major] Candidate selection can reuse the holdout
- Failure: If the final eight Mondays are used both to pick the candidate and to report its advantage over the baseline, the reported advantage can be optimistic even with frozen features.
- Fix: Select the candidate using earlier expanding-window folds, then evaluate it against the baseline on the final eight Mondays.
