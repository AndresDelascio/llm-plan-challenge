# Historical demand forecasting

## Objective

Each Monday, forecast daily sales for that Monday through Sunday for stores with two years of daily history. Set the forecast cutoff before Monday sales begin, in each store’s local time. Use only information available by that cutoff. Compare forecasts with sales from the corresponding days of the previous week.

## Data and features

1. Build each historical example as of its own Monday cutoff. Use recorded availability timestamps when sales can arrive late or be revised. Include future calendar or promotion features only if their values were known by the cutoff.
2. Replace the centered rolling average with a trailing 14-day average over the days ending Sunday. Use only sales available by the cutoff. Preserve recorded zero sales and distinguish them from missing records. Keep missing target values out of training and scoring, and report coverage.
3. Fit imputation medians and any other learned preprocessing separately on each fold’s training data. Apply those fitted transformations to that fold’s forecast inputs. Define the handling of missing prior-week sales for the baseline before evaluation and use the same rule throughout.

## Backtesting

1. Reserve the final eight Mondays for evaluation. Use earlier Mondays for expanding-window model selection and tuning. Freeze the chosen model configuration, feature definitions, preprocessing rules, and scoring protocol before evaluating the final eight Mondays.
2. For each evaluation Monday, refit using the history available at that cutoff. Include a historical training example only when all seven of its target days are available. Earlier evaluation weeks may enter later training folds once their sales are available. Generate and save both sets of forecasts before using that week’s actuals for scoring.
3. Score both methods on the same store-days. Report MAE by store, pooled MAE across store-days, and the paired difference in absolute error between the model and baseline. Report results by forecast week and day of the week, along with the number of scored and excluded store-days.

## Deployment

Use the same Monday cutoff, feature generation, preprocessing, and refit procedure validated in backtesting. Store the cutoff, data version, and seven daily forecasts per store so each run can be reproduced and scored once actuals are available.
