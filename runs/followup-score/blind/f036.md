# Historical demand forecasting

## Brief

Each Monday, forecast the next seven days of sales using only data available that Monday. The service will be deployed to stores with two years of daily history and compared against a last-week baseline.

## Definitions to fix before any modeling

- **Cutoff:** for a forecast origin on Monday *T*, the latest usable data is Sunday *T−1*. This assumes Monday's own sales are not known at forecast time, and that the forecast week is Monday *T* through Sunday *T+6*. Confirm both with the service owner.
- **Baseline:** the forecast for each day is the actual sales from the same weekday in the prior week (*T−7* to *T−1*).
- **Leakage rule:** every feature, imputation statistic, scaler and hyperparameter used for origin *T* must be computed only from data dated *T−1* or earlier.

## Implementation

1. **Split the data by forecast origin.**
   - Final test: the last eight Mondays, each with a full seven-day horizon of actuals. These are used once, at the end.
   - Selection: the eight Mondays before those, used for all model comparison, feature choices and tuning.
   - Both sets use an expanding window: for each origin, fit each candidate independently on all history before that origin's cutoff.

2. **Build features with strictly trailing windows.**
   - The trend feature is the 14-day average over *T−14* to *T−1*, not a window centered on *T*.
   - Any lag or rolling feature must be available for all seven horizon days as seen from the origin, so day *T+3* cannot use a lag-1 value.

3. **Fit preprocessing inside each fold.**
   - Compute missing-value medians (and any other fitted preprocessing) on that fold's training window only, then apply them to that fold's training and validation rows.
   - Never fit them on the full two-year file.
   - For deployment, refit on all data available at the forecast Monday.

4. **Add a leakage test.**
   - For a sample of origins, truncate the raw data at *T−1*, rebuild features, and assert they match the features from the full pipeline.

5. **Report metrics for every candidate and the baseline.**
   - MAE by store.
   - Aggregate MAE across stores.
   - A scale-free view, such as MAE relative to baseline MAE per store, so large stores do not dominate the aggregate.
   - MAE by horizon day (1–7).

6. **Run paired baseline comparisons.**
   - Compute the difference in absolute error between model and baseline on identical store × origin × horizon cells.
   - Report the mean difference, the share of stores where the model wins, and a confidence interval from bootstrapping over stores and origins as blocks, not individual rows.
   - Eight origins is a small sample, so state the uncertainty explicitly.

7. **Freeze, then run the final evaluation.**
   - Before touching the final eight Mondays, lock the feature definitions, model choice, hyperparameters and decision rule (for example, "ship if the aggregate MAE interval excludes zero and no more than X% of stores get worse").
   - Run the final test once and report the results as is; do not iterate after seeing them.

## Known limitations to document

- Two years of history gives at most one prior observation of each yearly seasonal period.
- The eight-week test covers only one part of the year, so holiday and seasonal performance is untested.
- New stores or stores with gaps need a defined fallback, such as the baseline.
