# Historical demand forecasting

## Brief

Forecast the following seven days of sales each Monday using only data available that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Implementation

1. Use an expanding-window evaluation with the final eight Mondays held out. Fit each candidate independently using the earlier history. At each held-out Monday, fit only on training examples whose full seven-day target window was finalized by that Monday's cutoff.
2. Use MAE by store, aggregate MAE across stores, and paired baseline comparisons. Build the last-week baseline from the prior week's same-weekday sales as available at the Monday cutoff, with a fixed fallback for missing values. Keep feature definitions frozen at final evaluation.
3. For each Monday, compute a trailing 14-day average that ends before the forecast cutoff, using only finalized values available then.
4. Fit missing-value medians on each fold's training period, then apply them unchanged to that fold's validation data.
