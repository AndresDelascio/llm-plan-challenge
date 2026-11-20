# Historical demand forecasting

## Brief

Forecast the following seven days of sales each Monday using only data available that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Implementation

1. Use an expanding-window evaluation with the final eight Mondays held out as the final test set. Fit each candidate independently using the earlier history, and select among candidates on expanding-window folds that end before the final eight Mondays. Score only the chosen model, once, on the final eight Mondays.
2. Use MAE by store, aggregate MAE across stores, and paired baseline comparisons. Keep feature definitions frozen at final evaluation.
3. For each Monday, compute a trailing 14-day average ending the Sunday before that Monday and add it as a trend feature.
4. Fit the missing-value medians inside each fold on that fold's training window only, then apply those medians to that fold's training and validation data.
