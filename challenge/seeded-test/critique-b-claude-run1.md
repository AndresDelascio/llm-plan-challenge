VERDICT: BLOCKED

### 1. One date format applied to both banks
- Severity: blocker
- Claim: Step 3 parses the joined table with `%d/%m/%Y`, but Bank B writes MM/DD/YYYY.
- Why it matters: Bank B rows with a day above 12 crash the parse. Rows with a day of 12 or below silently swap day and month and land in the wrong month, and step 10's yearly-total check cannot see it.
- Fix: Parse dates per file before joining, choosing the format by bank, and add a Bank B row with a day above 12 and an ambiguous one (e.g. 03/04) to the step 9 test.

### 2. File count is wrong
- Severity: blocker
- Claim: Two banks with one export per month is 24 files, but step 1 requires exactly 12.
- Why it matters: The script refuses to run on the full data set, and it also refuses on any partial year.
- Fix: Require 12 files per bank (24 in total), or check that each bank and month pair appears at most once and report the missing ones.

### 3. Source files deleted after the first run
- Severity: blocker
- Claim: Step 7 deletes the exports, but step 8 needs a re-run and step 10 needs the bank files for the hand check.
- Why it matters: After the first run there is no input left, so the categories cannot be refined or the total verified. A bug in the summary also destroys the only local copy of the data.
- Fix: Drop step 7 and never delete the inputs.

### 4. Summary written into the input folder
- Severity: major
- Claim: `exports/summary.csv` matches the `*.csv` glob in step 2.
- Why it matters: On the second run it trips the file-count check, or is read as a bank export with the wrong columns.
- Fix: Write the summary outside `exports/`, or glob only the bank file-name pattern.

### 5. Refunds dropped, so spending is overstated
- Severity: major
- Claim: Step 4 drops all positive rows, which includes refunds and returns.
- Why it matters: A returned purchase stays counted at full price, so the category totals are too high. Step 10 sums the same negative rows, so it passes anyway.
- Fix: Keep positive rows that match a spending-category keyword and net them against that category, dropping only unmatched positives such as income.
