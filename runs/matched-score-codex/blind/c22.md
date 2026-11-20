VERDICT: BLOCKED

### 1. [blocker] Training labels can cross the forecast cutoff
- Failure: A training example can come from an earlier Monday while some of its seven target sales values are still unavailable at the evaluation cutoff. Using those labels leaks future data into the fit.
- Fix: At each Monday cutoff, train only on examples whose full seven-day target was finalized and available by then.

### 2. [major] Point-in-time rules cover only the trailing average
- Failure: Other candidate features can use values finalized or revised after their historical forecast cutoff, giving evaluation inputs that deployment would lack.
- Fix: Construct every feature from the data available at its example’s Monday cutoff, for both training and evaluation.

### 3. [major] The baseline lacks an availability rule
- Failure: A same-weekday-last-week baseline can use sales that were still unfinalized that Monday, invalidating the paired comparison.
- Fix: Define the baseline as the sales value seven days before each target day, with a fixed cutoff-safe fallback for unavailable values.

### 4. [minor] The forecast window has no explicit date boundary
- Failure: Implementations can disagree on whether Monday is the first target day and score different dates.
- Fix: Specify the store-local Monday cutoff and the exact seven target dates, then use them for every candidate and the baseline.
