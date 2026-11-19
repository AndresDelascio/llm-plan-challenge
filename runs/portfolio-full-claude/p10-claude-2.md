VERDICT: PROCEED WITH CHANGES

### 1. [major] Selection and final evaluation share the same holdout
- Failure: Candidates are compared on the final eight Mondays, and the "final evaluation" has no separate data. The winner's MAE and its margin over the baseline are optimistically biased.
- Fix: Select candidates on earlier expanding-window folds, and score the final eight Mondays once, for the chosen model only.

### 2. [major] Training targets can cross the fold cutoff
- Failure: "Earlier history" does not exclude training rows whose seven-day target window extends past the validation Monday. Those rows leak future sales into the fit.
- Fix: Train only on rows whose full target window ends before the fold's cutoff, and only on values finalized by then.

### 3. [major] Baseline not held to the availability rule
- Failure: Only the 14-day feature is restricted to finalized values available at cutoff. If the last-week baseline uses later-revised or not-yet-final sales, the paired comparison is invalid.
- Fix: Build the baseline from the same as-of data as the model, at the same cutoff.

### 4. [major] As-of availability may not be reconstructable
- Failure: Step 3 assumes history records what was finalized on each Monday. If the two-year history holds only current revised values, the backtest silently uses unavailable data.
- Fix: Confirm finalization timestamps exist; otherwise apply a fixed conservative finalization lag.

### 5. [minor] Eight weeks and pooled MAE are weak evidence
- Failure: Eight Mondays miss seasonal and holiday periods, and aggregate MAE is dominated by high-volume stores.
- Fix: Add a scale-normalized metric (e.g., per-store MAE relative to baseline) and extend the folds across seasonal periods.
