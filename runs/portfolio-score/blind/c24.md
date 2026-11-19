VERDICT: BLOCKED

### 1. [blocker] Centered rolling average leaks the future
- Failure: A 14-day window centered on Monday includes about seven days after it, which are the days being forecast. This violates "only data available that Monday" and inflates the model's apparent edge over the baseline.
- Fix: Use a trailing 14-day window ending the Sunday before each forecast Monday.

### 2. [blocker] Imputation medians fit on the full file
- Failure: Medians computed over the full two years include the held-out weeks and data later than each fold's cutoff, so every fold is contaminated.
- Fix: Fit medians inside each fold on that fold's training window only, then apply them to its validation week.

### 3. [major] Holdout used for both selection and final evaluation
- Failure: Candidates are compared on the same eight Mondays that give the final score, so the winner's reported MAE and baseline margin are optimistically biased.
- Fix: Select candidates on earlier expanding-window folds and score only the chosen model, once, on the final eight Mondays.

### 4. [minor] Aggregate MAE dominated by large stores
- Failure: Unscaled MAE pooled across stores lets high-volume stores swamp regressions at small ones.
- Fix: Also report a scaled metric (e.g. MAE divided by baseline MAE per store) and the share of stores that beat the baseline.

### 5. [minor] Eight weeks is a thin, single-season test
- Failure: Eight consecutive Mondays cover one season, and their paired differences are autocorrelated, so the baseline comparison is weak.
- Fix: Pair comparisons at the store-week level, and add earlier folds spread across the second year as backtest origins.
