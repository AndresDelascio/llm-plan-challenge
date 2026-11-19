VERDICT: BLOCKED

### 1. [blocker] Centered rolling average uses future sales
- Failure: A 14-day window centered on Monday includes about seven days after it, which are the days being forecast. This breaks the "only data available that Monday" constraint, inflates backtest scores, and cannot be computed in production.
- Fix: Use a trailing 14-day window ending the Sunday before each forecast Monday.

### 2. [blocker] Imputation medians fit on the full file
- Failure: Medians computed over the full two years include the held-out weeks and each fold's future, so every training and validation window is contaminated.
- Fix: Compute medians inside each fold from that fold's training history only, then apply them to its validation window.

### 3. [major] No separate data for choosing a candidate
- Failure: The same eight Mondays are used both to compare candidates and to report the final result. The winner's MAE and its margin over the baseline will be optimistically biased.
- Fix: Select candidates on earlier expanding-window folds and score the frozen winner once on the final eight Mondays.

### 4. [minor] Aggregate MAE is dominated by large stores
- Failure: Unscaled MAE pooled across stores lets high-volume stores hide regressions in small ones.
- Fix: Also report a scaled metric (e.g. MASE against the last-week baseline) and the share of stores that beat the baseline.

### 5. [minor] Holdout covers only one season
- Failure: Eight consecutive Mondays span about two months, so holiday or seasonal performance is untested.
- Fix: State this limit in the results, or spread the selection folds across the second year.
