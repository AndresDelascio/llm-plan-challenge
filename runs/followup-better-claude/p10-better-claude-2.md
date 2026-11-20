# Historical demand forecasting

## Brief

Each Monday, forecast the following seven days of sales (Monday to Sunday) per store, using only data available that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Definitions (fix before any modelling)

- **Cutoff:** for each forecast Monday, the cutoff is the start of that Monday. Only values finalized before the cutoff may be used, taken from an as-of snapshot where one exists, since later corrections to history would leak.
- **Baseline:** the forecast for each day is the actual sales for the same weekday in the week ending before the cutoff.
- **Scope:** only stores with two years of daily history are evaluated, matching deployment.

## Implementation

1. **Build features with the cutoff rule.** For each Monday, compute the trailing 14-day average ending before the cutoff, using only values finalized by then. Add one automated check that no feature for a given Monday uses a row dated on or after its cutoff.
2. **Split the history into three parts by time.**
   - Final test: the last eight Mondays, used once.
   - Selection: the eight Mondays before that, used to compare candidates and tune.
   - Training: everything earlier, with an expanding window.
3. **Fit per fold.** For each Monday, fit each candidate independently on the history before its cutoff. Fit missing-value medians on that fold's training period and apply them unchanged to that fold's validation data. Any other fitted preprocessing follows the same rule.
4. **Select on the selection Mondays only.** Choose the candidate and its settings there, then freeze the feature definitions, hyperparameters and model choice.
5. **Run the final evaluation once on the eight test Mondays.** Refit the frozen candidate on an expanding window for each Monday, and score it and the baseline on the same store-days.
6. **Report:**
   - MAE by store.
   - Aggregate MAE across stores, plus a scale-free aggregate (MAE relative to the baseline's MAE per store, then averaged) so large stores do not dominate.
   - MAE by horizon day (1 to 7).
   - Paired comparison against the baseline, paired on store-week: the mean difference with a confidence interval, and the share of stores where the model wins.
7. **Set the decision rule before the test run.** The model replaces the baseline only if the paired difference in aggregate MAE favours it with an interval excluding zero, and it is not materially worse on any horizon day or on a large share of stores. Otherwise, ship the baseline or go back to selection with new data, without reusing the test Mondays.

## Known limitation

Eight test Mondays cover about two months, so the result may not hold across seasons or holidays. State which period was tested, and keep running the same paired comparison after deployment.
