VERDICT: PROCEED WITH CHANGES

### 1. [major] Model selection reuses the final holdout
- Failure: Candidates are compared on the same eight held-out Mondays that give the final score. The winner's MAE and its margin over the baseline are therefore optimistically biased.
- Fix: Select candidates and hyperparameters on earlier expanding-window folds, then score the single frozen winner once on the final eight Mondays.

### 2. [major] Baseline not held to the same availability rule
- Failure: The last-week baseline is undefined. If it uses values not finalized by Monday, or revised later, the paired comparison is unfair and unreproducible in deployment.
- Fix: Define the baseline as the same weekday from the prior week, using only values finalized at the cutoff.

### 3. [major] Point-in-time availability assumed, not verified
- Failure: Step 3 depends on knowing which values were finalized on each historical Monday. Without as-of timestamps, revised history leaks silently into features and medians.
- Fix: Confirm that finalization timestamps exist. If they do not, apply a conservative fixed lag to all inputs.

### 4. [minor] Eight weeks give a weak, seasonally narrow comparison
- Failure: Eight paired points per store, from one two-month stretch, cannot distinguish small gains from noise or cover holiday periods.
- Fix: Pool the paired differences across stores with a per-store-clustered test, and state the season covered as a caveat.

### 5. [minor] Aggregate MAE is dominated by large stores
- Failure: Unscaled MAE summed across stores lets high-volume stores hide regressions at small ones.
- Fix: Add a scaled metric, such as MAE relative to the baseline per store, alongside the raw aggregate.
