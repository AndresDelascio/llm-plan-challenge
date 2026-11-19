VERDICT: BLOCKED

### 1. One date format applied to both banks
- Severity: blocker
- Claim: Step 3 parses the joined table with `%d/%m/%Y`, but Bank B writes MM/DD/YYYY.
- Why it matters: Bank B rows with a day above 12 crash the parse, and the rest silently swap day and month and land in the wrong month. The checks in steps 9 and 10 only compare totals, so they would not catch this.
- Fix: Parse dates per file, with the format chosen by bank, before joining. Add a Bank B row dated after the 12th to the test set, with an expected month.

### 2. File count is wrong
- Severity: blocker
- Claim: Two banks times 12 months is 24 files, but step 1 requires exactly 12.
- Why it matters: With the full year's exports present, the script refuses to run. It also cannot run before all of December's exports exist.
- Fix: Drop the exact-count check. Instead, print which bank and month files were found and warn about any that are missing.

### 3. Script deletes its own inputs
- Severity: blocker
- Claim: Step 7 deletes the exports after the first run, but step 8 needs a re-run and step 10 needs the bank files for the hand check.
- Why it matters: The second run finds no files, so the keyword loop cannot work and the Done check cannot be performed. Source data is gone unless it is downloaded again.
- Fix: Remove step 7.

### 4. Summary is written into the input folder
- Severity: major
- Claim: `exports/summary.csv` matches the `*.csv` glob that step 2 reads.
- Why it matters: On every re-run the summary is ingested as a bank file, which breaks the file count or fails on its different columns.
- Fix: Write the summary outside `exports/`.

### 5. Transfers have no mitigation
- Severity: major
- Claim: The plan lists transfers between the two accounts as a known risk, but no step handles them.
- Why it matters: Every transfer, including any card payment from the other account, is counted as spending. The totals are inflated, and the step 10 check still passes because it sums the same rows.
- Fix: Add a "transfer" keyword category in `categories.toml` and exclude it from the summary.
