VERDICT: BLOCKED
### 1. [blocker] Centered trend leaks future sales

- Failure: The centered 14-day average uses sales after forecast issuance, including days the model is meant to predict.
- Fix: Use a trailing 14-day average ending on the latest day with sales available at forecast issuance.

### 2. [blocker] Full-history imputation leaks holdout data

- Failure: Medians fitted on the full file incorporate held-out sales and sales unavailable at earlier forecast dates.
- Fix: Fit imputation medians separately on each fold’s training data and apply them to that fold’s validation data.
