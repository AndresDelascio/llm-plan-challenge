# Historical demand forecasting

## Brief

Each Monday, forecast the next seven days of sales (Monday through Sunday) per store, using only data available before that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Definitions

- **Forecast origin:** a Monday, date `T`. The latest usable observation is Sunday `T-1`. If sales data arrives late, set the cutoff to the last day reliably available on Monday morning and use it everywhere.
- **Target:** daily sales for `T` through `T+6`, seven horizons per store per origin.
- **Baseline:** the forecast for day `T+h` is the actual sales on `T+h-7`, the same weekday in the prior week.
- **Leakage rule:** every feature, imputation statistic and fitted parameter used for origin `T` comes only from data dated before `T`.

## Implementation

1. **Split the data by time into two parts.**
   - **Final test:** the last eight Mondays. Use them once, after all modelling decisions are frozen.
   - **Development:** everything earlier. Within it, use expanding-window validation over the eight or more Mondays before the test period for model, feature and hyperparameter choices.
   - At every origin, fit each candidate only on history before that origin.

2. **Build features from past data only.**
   - **Trend:** use a trailing 14-day average ending at `T-1`, not a window centred on the date, because a centred window includes the days being forecast.
   - **Lags and seasonality:** add same-weekday lags (7, 14, 21 and 28 days back), day of week, and calendar or holiday flags known in advance.
   - **Shared code path:** generate features with one function that takes an as-of date, used for training, validation and production alike.

3. **Fit preprocessing inside each fold.**
   - Compute missing-value medians, and any scaling or encoding, on that fold's training window only.
   - Apply them to that fold's validation or test origin.
   - Never compute them on the full two-year file.
   - In production, refit them on all history before the forecast Monday.

4. **Evaluate against the baseline.**
   - **Metrics:** MAE per store, aggregate MAE across stores, and MAE by horizon (day 1 to day 7).
   - **Scale-free metric:** also report each store's MAE divided by its baseline MAE, so large stores do not dominate the aggregate.
   - **Paired comparison:** compare model and baseline on the same store-origin pairs. Report the mean difference with a confidence interval, for example by bootstrapping over stores, and the share of stores where the model wins.
   - **Small sample:** eight origins is few, so treat small aggregate gains with caution.

5. **Freeze, then test.**
   - Lock feature definitions, model choice and hyperparameters using development results only.
   - Run the final eight-Monday test once and report it as is.
   - If anything is changed after seeing test results, that test is no longer clean and a new holdout period is needed.

6. **Check for leakage and bad data before trusting results.**
   - **Automated test:** recompute an origin's features after truncating the data at `T-1` and confirm they are identical.
   - **Suspicious results:** treat a model that beats the baseline by an implausibly large margin as a likely leak and investigate.
   - **Data issues:** decide how to handle store closures, stockouts and gaps in history, and apply the same handling to the model and the baseline.

## Success criterion

The chosen model beats the last-week baseline on aggregate MAE in the final test, with a paired confidence interval excluding zero, and does not lose materially on any large group of stores. Otherwise, ship the baseline, or a simple seasonal average, and report why.
