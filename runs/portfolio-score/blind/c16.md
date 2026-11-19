VERDICT: BLOCKED
### 1. [blocker] Training labels can cross the forecast cutoff
- Failure: An earlier training example can contain seven-day sales totals or daily targets that were still unavailable on the Monday being evaluated. Ordering examples by forecast date alone allows future sales into model fitting.
- Fix: At each held-out Monday, fit only on examples whose full target window was finalized by that Monday’s cutoff.

### 2. [major] Baseline availability is unspecified
- Failure: If the baseline uses retrospectively finalized sales from the previous week, it can use values that were unavailable at the same cutoff imposed on the candidates.
- Fix: Build the baseline from the prior week’s same-weekday sales as available at the Monday cutoff, with a fixed fallback for missing values.
