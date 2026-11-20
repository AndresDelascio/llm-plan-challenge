# Historical demand forecasting

## Brief

Forecast the following seven days of sales each Monday using only data available that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Implementation

1. Use an expanding-window evaluation with the final eight Mondays held out. Fit each candidate independently using the earlier history.
2. Use MAE by store, aggregate MAE across stores, and paired baseline comparisons. Keep feature definitions frozen at final evaluation.
3. For each Monday, compute a trailing 14-day average ending on the latest day with sales available at forecast issuance, and add it as a trend feature.
4. Fit the missing-value medians separately on each fold's training data, then apply those medians to that fold's training and validation windows.
