VERDICT: BLOCKED
### 1. [blocker] Centered average uses future sales
- Failure: The centered 14-day average includes sales after the forecast Monday, so the feature cannot be computed as evaluated when the forecast is issued.
- Fix: Use a trailing 14-day average ending on the latest day with complete sales at forecast time.

### 2. [blocker] Imputation leaks held-out data
- Failure: Medians fitted on the full two-year file incorporate observations from validation windows, including data unavailable at earlier forecast dates.
- Fix: Fit medians on each fold’s training data and apply them to that fold’s validation data.
