# Historical demand forecasting

## Brief

Forecast the following seven days of sales each Monday using only data available that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Implementation

1. Use an expanding-window evaluation with the final eight Mondays held out. Compare and select candidates on expanding-window folds over Mondays before the holdout, fitting each candidate independently using the history earlier than each fold. Score the final eight Mondays once, for the chosen model only, fitting it for each held-out Monday using the earlier history.
2. Use MAE by store, aggregate MAE across stores, and paired baseline comparisons. Build the last-week baseline from the same as-of data as the model, using only finalized values available at the same forecast cutoff. Keep feature definitions frozen at final evaluation.
3. For each Monday, compute a trailing 14-day average that ends before the forecast cutoff, using only finalized values available then.
4. Fit missing-value medians on each fold's training period, then apply them unchanged to that fold's validation data.
