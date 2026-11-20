# Historical demand forecasting

## Brief

Forecast the following seven days of sales each Monday using only data available that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Implementation

1. Use an expanding-window evaluation with the final eight Mondays held out. Fit each candidate independently using the earlier history. Include a training row only once all seven of its target values were finalized by that fold's Monday cutoff.
2. Select the candidate using earlier expanding-window folds that precede the final eight Mondays. Then evaluate the selected candidate against the baseline on the final eight Mondays, which are not used for selection.
3. Build the last-week baseline from the Monday snapshot: forecast each day from the same weekday one week earlier, using only values available at that Monday's cutoff. Specify a fallback for unavailable values before evaluating.
4. Use MAE by store, aggregate MAE across stores, and paired baseline comparisons. Keep feature definitions frozen at final evaluation.
5. For each Monday, compute a trailing 14-day average that ends before the forecast cutoff, using only finalized values available then.
6. Fit missing-value medians on each fold's training period, then apply them unchanged to that fold's validation data.
