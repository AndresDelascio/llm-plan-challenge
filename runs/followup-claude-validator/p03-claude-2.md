VERDICT: BLOCKED

### 1. [blocker] Centered rolling average leaks future sales
- Failure: A 14-day window centered on Monday includes about seven days after it, which are the forecast targets. This violates "only data available that Monday", inflates evaluation scores, and the feature cannot be computed in production.
- Fix: Use a trailing window ending the day before the forecast Monday (e.g. the prior 14 days).

### 2. [blocker] Imputation medians fit on the full file
- Failure: Medians computed over the whole two years include the held-out Mondays and their target weeks, so future information leaks into every fold and the baseline comparison is biased.
- Fix: Fit medians inside each fold on that fold's training window only, then apply them to the validation window.

### 3. [major] Model selection and final evaluation share the same eight Mondays
- Failure: Candidates are compared on the held-out Mondays and the winner is then reported on those same Mondays, so the reported gain over baseline is optimistically biased.
- Fix: Select candidates on earlier expanding-window folds and reserve the final eight Mondays for a single evaluation of the chosen model.

### 4. [minor] Paired comparison and aggregation are underspecified
- Failure: Unweighted aggregate MAE is dominated by high-volume stores, and the eight overlapping-history folds give few, correlated pairs, so a "win" over last-week may be noise.
- Fix: Predefine the pairing unit (store-week), add a scaled metric such as MAE relative to baseline per store, and state the decision threshold up front.
