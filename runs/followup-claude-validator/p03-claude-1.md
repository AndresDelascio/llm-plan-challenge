VERDICT: BLOCKED

### 1. [blocker] Centered rolling average leaks future sales
- Failure: A 14-day window centered on each Monday includes about seven days after it, which is the forecast target period. This breaks the "only data available that Monday" constraint, inflates backtest accuracy, and cannot be computed in production.
- Fix: Use a trailing 14-day window ending the Sunday before each Monday.

### 2. [blocker] Imputation medians fitted on the full file
- Failure: Medians computed over the full two years include the held-out Mondays and each fold's future, so holdout data contaminates every training window.
- Fix: Fit the medians inside each fold on its training window only, then apply them to that fold's validation data.

### 3. [major] Holdout doubles as the selection set
- Failure: Candidates are compared on the same eight Mondays used for final evaluation, so the winner's reported MAE is optimistically biased.
- Fix: Select candidates on earlier expanding-window folds and score the final eight Mondays once, with the chosen model only.

### 4. [major] Baseline is undefined
- Failure: "Last-week" is not specified. If it is built from anything other than the seven days ending Sunday, the paired comparison is either leaky or unfair.
- Fix: Define the baseline as the same weekday's sales from the week ending the Sunday before, generated per fold at the same cutoff.

### 5. [minor] Aggregate MAE is dominated by high-volume stores
- Failure: Unscaled MAE summed across stores hides regressions at small stores, and eight consecutive Mondays cover only one season.
- Fix: Add a scaled metric (MASE against the baseline) per store, and state the seasonal limitation in the results.
