VERDICT: PROCEED WITH CHANGES

### 1. [major] Candidate selection and final evaluation share one holdout
- Failure: Candidates are compared on the final eight Mondays, and no separate final-evaluation set is defined. The winner's reported margin over the baseline is therefore optimistically biased.
- Fix: Select candidates on earlier expanding-window folds. Reserve the final eight Mondays for a single run of the frozen winner against the baseline.

### 2. [major] "Available then" has no stated mechanism
- Failure: Step 3 depends on knowing which values were finalized as of each historical Monday. If the history holds only current, revised values, the backtest silently uses data that was not available on that Monday.
- Fix: Filter on a finalization timestamp or point-in-time snapshot. If neither exists, apply a fixed conservative lag covering the longest finalization delay.

### 3. [major] Eight weeks is thin and covers one season
- Failure: Eight paired points per store, all from one two-month stretch, cannot support a reliable baseline comparison or show holiday and seasonal behaviour.
- Fix: Spread the evaluation origins across the second year of history (the first year still trains), and report uncertainty on the paired differences.

### 4. [minor] Baseline is not held to the same cutoff
- Failure: A last-week baseline built from later-finalized values gets information the model is denied, which skews the paired comparison.
- Fix: Compute the baseline from the same point-in-time data as the model features.

### 5. [minor] Aggregate MAE is undefined
- Failure: Pooled MAE lets high-volume stores dominate, hiding regressions at small ones.
- Fix: Specify the aggregation, and add a scale-normalized metric such as per-store MAE relative to the baseline.
