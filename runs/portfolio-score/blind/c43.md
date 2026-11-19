VERDICT: BLOCKED
### 1. [blocker] Centered trend uses future sales
- Failure: The centered 14-day average includes sales after the forecast cutoff, leaking future information into evaluation and making the feature unavailable at forecast time.
- Fix: Average the latest 14 completed days of sales available at each Monday’s forecast cutoff.
### 2. [blocker] Imputation uses held-out data
- Failure: Full-file medians incorporate sales unavailable at earlier forecast cutoffs, including data from the held-out period.
- Fix: Fit medians on each fold’s training data and apply them unchanged to that fold’s validation data.
