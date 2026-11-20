# Historical demand forecasting

## Forecast contract

Every Monday, forecast daily sales for Monday through Sunday for each store with two years of daily history. Set the forecast cutoff to the scheduled run time in each store’s local time zone. Use only records available by that cutoff. Evaluate forecasts against finalized sales and use the previous week’s same-day sales as the baseline.

## Data and features

1. Reconstruct each historical Monday’s inputs from record availability timestamps or archived snapshots. Use the sales values that were finalized and visible at the cutoff, including when records were later revised. Flag any period where historical availability cannot be verified.
2. Compute the trailing 14-calendar-day sales average over the two weeks ending Sunday. Include only values finalized by the Monday cutoff. Keep zero sales distinct from missing records, and record how many days contributed to the average. Treat the average as missing if no days qualify.
3. Use the prior week’s Monday-through-Sunday sales as the baseline, subject to the same cutoff. When a same-day value is unavailable, use the trailing 14-day average. If neither is available, flag the baseline as unavailable and report the resulting coverage.
4. Fit missing-value medians and any other learned preprocessing on each training window. Apply those fitted values unchanged to the corresponding forecasts. Define the fallback for features that are entirely missing in training during development.

## Backtest

1. Reserve the final eight Mondays as the holdout. Use expanding-window backtests on earlier Mondays to select the model, tune hyperparameters, and finalize feature definitions, fallback rules, and scoring.
2. Freeze those choices before opening the holdout. For each holdout Monday, refit the selected model and preprocessing using only training examples whose sales labels were finalized by that cutoff. Reconstruct each training example’s features as of its own forecast cutoff. Earlier holdout weeks may enter later training windows once their labels are available, matching the production schedule.
3. Generate all seven daily predictions at the Monday cutoff. Use the same store-days for paired model and baseline comparisons. Report missing actuals, unavailable baseline values, and failed predictions separately.

## Reporting and release

1. Report MAE by store and forecast day, pooled MAE across scored store-days, and the mean of store-level MAEs so every store receives equal weight in that summary.
2. Report the paired difference in absolute error between the model and baseline for each holdout Monday and overall. Set the minimum improvement and acceptable forecast coverage before reviewing holdout results.
3. Before deployment, verify that the production job uses the same cutoff, features, preprocessing, and fallback rules as the backtest. Log each run’s cutoff, data version, model version, and forecast coverage so its predictions can be reproduced and scored once actuals are finalized.
