# Historical demand forecasting

## Objective

Each Monday, forecast daily sales for that Monday through Sunday for stores with two years of daily history. Set the Monday forecast cutoff to the production run time in each store’s local time. Use only data that was finalized and available by that cutoff.

## Backtest

1. Reserve the final eight consecutive Monday forecast origins with complete seven-day outcome windows for final evaluation. Use earlier Monday origins for expanding-window development and tuning, with a minimum training history that reflects what will be available at deployment.
2. Build each historical training example using the data available at its own forecast cutoff. At each validation or test origin, train on earlier examples whose full seven-day targets were finalized by that origin’s cutoff. Fit each candidate and its preprocessing independently using that origin’s training data.
3. Select the candidate and freeze feature definitions, hyperparameters, preprocessing rules, and scoring rules before opening the holdout. Refit the selected model at each of the eight holdout Mondays using the same expanding-window procedure planned for production. Earlier holdout outcomes may enter later training once finalized. Use the completed holdout to assess the frozen procedure.

## Features and baseline

4. Compute the trailing 14-day mean over the 14 calendar days ending Sunday. Include only sales values finalized and available at the Monday cutoff. Preserve recorded zero sales, track how many days contributed, and treat an empty window as missing. Use historical availability records or snapshots to reconstruct what was known at each cutoff.
5. Fit feature-imputation medians on each origin’s training data and apply them unchanged to that origin’s forecast inputs. Set a fallback during development for features with no observed training values. Keep missing sales targets out of training and scoring.
6. Define the last-week baseline as sales from the same weekday seven days earlier, using the same cutoff. Before evaluation, specify how the baseline handles unavailable prior-week values, and report how often it uses that fallback.

## Evaluation and rollout

7. Score the candidate and baseline on identical store-day pairs using finalized actuals. Report MAE per store, pooled MAE across store-days, and paired MAE differences overall and by forecast week. Report scoring coverage and summarize performance by forecast day to show where gains or regressions occur.
8. Set the minimum improvement and acceptable store-level regressions before opening the holdout. If the model meets those criteria, run a production dry run to verify cutoff handling, baseline parity, and seven dated predictions per store before deployment.
