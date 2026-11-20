# Historical demand forecasting

## Forecast definition

Every Monday before stores open, forecast daily sales for each store from that Monday through Sunday. Use only data available at the forecast cutoff in each store’s local time zone. Apply the same cutoff in backtesting and production, including any delay in receiving or finalizing Sunday sales.

## Implementation

1. **Build features as of each forecast cutoff.** Replace the centered average with a trailing 14-day average over the dates ending Sunday, using only sales already available at the cutoff. Use the same feature-building code for historical training examples and live forecasts. Use calendar features for the seven target dates and sales lags available when the forecast is issued. Generate all seven predictions without using actual sales from the forecast week.
2. **Fit preprocessing within each training window.** For each fold, fit imputation medians and any other learned preprocessing on the training rows only. Apply the fitted transformations to the validation rows. Distinguish recorded zero sales from missing records. Leave missing target values out of scoring and report how many store-days were excluded.
3. **Tune on earlier Mondays and reserve the final eight for evaluation.** Use expanding-window backtests on Mondays before the holdout to choose the model, features, and hyperparameters. Freeze those choices before opening the holdout. For each of the final eight Mondays, refit using only training examples whose full seven-day outcome was available by that Monday’s cutoff. Earlier holdout outcomes may enter later training windows once available, consistent with weekly production refitting.
4. **Run the last-week baseline at the same cutoff.** Predict each day using the same store’s sales for the corresponding weekday one week earlier. If that value is unavailable, use the most recent available observation for that store and weekday. Fix this rule before final evaluation and report any cases where the baseline still cannot produce a prediction.
5. **Score both methods on the same store-days.** Report MAE by store and forecast day, along with overall MAE across all scored store-days. Report the paired difference in absolute error between the model and baseline overall and for each held-out Monday. Include coverage counts so exclusions are visible.
6. **Verify the production path before rollout.** Replay a historical Monday through the production forecast job and confirm that records arriving after the cutoff cannot change its predictions. Check that each eligible store receives seven dated forecasts, then monitor forecast coverage and MAE against the baseline as actuals arrive.
