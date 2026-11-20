# Historical demand forecasting

## Brief

Each Monday, forecast daily sales for the following seven days (Monday to Sunday) per store, using only data available at that Monday's cutoff. The service will be deployed to stores with two years of daily history and must beat a last-week baseline, which is the same weekday's sales from the prior week.

## Definitions (fix before any modelling)

- **Cutoff:** a set time each Monday. A value is "available" only if it was finalized by then. Confirm the reporting lag: if Sunday's sales are not final by Monday's cutoff, neither the model nor the baseline may use them.
- **Baseline:** built under the same availability rule as the model. If a prior-week value is not finalized, fall back to the most recent finalized same weekday.
- **Success criterion:** the chosen model has lower aggregate MAE than the baseline on the final holdout and lower MAE in a majority of stores. State this before looking at the holdout.

## Implementation

1. **Split the history into three parts by time.**
   - Final holdout: the last eight Mondays, used once and only for the final comparison.
   - Selection folds: the eight Mondays before that, used for choosing candidates, features and hyperparameters.
   - Training: for each fold, everything before that fold's cutoff (expanding window).

2. **Select on the selection folds only.** For each selection Monday, fit every candidate independently on the earlier history and forecast the seven days. Choose the model, features and hyperparameters from these results, then freeze them.

3. **Build features as of the cutoff.** For each Monday, compute the trailing 14-day average ending before the cutoff, using only values finalized by then. Apply the same rule to every other feature, so that no feature uses actuals from the forecast week.

4. **Fit all learned preprocessing inside the fold.** Fit missing-value medians, and any scaling or encoding, on each fold's training period. Apply them unchanged to that fold's validation data.

5. **Run the final evaluation once.** With the configuration frozen, run the expanding window over the eight holdout Mondays, refitting parameters and medians at each cutoff. Do not change anything after seeing these results.

6. **Report the following.**
   - MAE by store.
   - Aggregate MAE across stores, both pooled over all store-days and as the unweighted mean of store MAEs, so large stores do not hide small-store failures.
   - MAE by horizon day (1 to 7).
   - Paired model-versus-baseline differences on matching store-weeks, with a confidence interval and the share of stores improved.
   - The caveat that eight weeks covers one part of the year and results may not hold for other seasons or holidays.

7. **Deploy.** Refit the frozen configuration on all available history each Monday, using the same feature and preprocessing code as in evaluation. Log the forecasts and the baseline every week so the comparison continues in production.
