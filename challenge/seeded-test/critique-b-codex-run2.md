VERDICT: BLOCKED

### 1. A full year requires 24 files
- Severity: blocker
- Claim: The 12-file requirement rejects the 24 monthly exports needed for two accounts across 2026.
- Why it matters: Supplying the complete year prevents execution; supplying only 12 files omits part of the required data.
- Fix: Require 24 monthly source files.

### 2. Bank B dates use the wrong format
- Severity: blocker
- Claim: Parsing both banks with `%d/%m/%Y` misinterprets Bank B’s dates.
- Why it matters: Bank B dates with days above 12 fail parsing, while ambiguous dates silently put spending in the wrong month.
- Fix: Parse each bank’s dates with its specified format before combining the rows.

### 3. Deleting exports prevents recategorization
- Severity: major
- Claim: Step 7 deletes the inputs needed for the rerun requested in step 8.
- Why it matters: After updating keywords, the user must retrieve the bank exports again; the original inputs are also unavailable to investigate incorrect results.
- Fix: Retain the monthly exports.

### 4. The summary becomes an input
- Severity: major
- Claim: Writing `summary.csv` inside `exports/` makes it match the input file selection.
- Why it matters: On a subsequent run with retained or restored exports, the summary triggers the file-count rejection; if that check is relaxed, it gets read as bank data.
- Fix: Write the summary outside `exports/`, or exclude it from both counting and ingestion.

### 5. Internal transfers inflate spending
- Severity: major
- Claim: The negative-only filter counts outgoing internal transfers as spending and drops their positive receiving entries.
- Why it matters: Whenever money moves between the two accounts, reported spending increases by the transfer amount; the proposed reconciliation also accepts that incorrect total.
- Fix: Identify internal transfers and exclude them from both the summary and the reconciliation’s spending total.