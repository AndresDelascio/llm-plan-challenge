# Historical demand forecasting

## Brief

Forecast the following seven days of sales each Monday using only data available that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Implementation

1. Use an expanding-window evaluation with the final eight Mondays held out. Fit each candidate independently using the earlier history.
2. Use MAE by store, aggregate MAE across stores, and paired baseline comparisons. Keep feature definitions frozen at final evaluation.
3. For each Monday, compute a trailing average of the latest 14 completed days of sales available at that Monday's forecast cutoff and add it as a trend feature.
4. Fit the missing-value medians on each fold's training data only, then apply those medians unchanged to that fold's validation window.
