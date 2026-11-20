# Historical demand forecasting

## Brief

Forecast the following seven days of sales each Monday using only data available that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Implementation

1. Use an expanding-window evaluation with the final eight Mondays held out as a final test set that is not used for candidate selection.
   - Select among candidates on earlier expanding-window folds, with forecast Mondays that precede the holdout and are spread across the second year so they cover more than one season.
   - Fit each candidate independently on each fold, using only the history before that fold's forecast Monday.
   - Freeze the winning candidate, then score it once on the final eight Mondays, again fitting only on the history before each Monday.
2. Use MAE by store, aggregate MAE across stores, and paired baseline comparisons. Keep feature definitions frozen at final evaluation. State in the results that the final holdout spans about two consecutive months, so it does not test holiday or other seasonal performance.
3. For each Monday, compute a trailing 14-day average of sales ending the Sunday before that Monday and add it as a trend feature.
4. Fit the missing-value medians inside each fold, using only that fold's training history, then apply those medians to that fold's training and validation windows. Do the same for the final holdout, using only the history before each forecast Monday.
