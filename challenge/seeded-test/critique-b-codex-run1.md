VERDICT: BLOCKED

### 1. File-count gate rejects a complete year
- Severity: blocker
- Claim: Twelve monthly exports from each of two banks require 24 files, but the script accepts only 12.
- Why it matters: Providing all the files needed for the 2026 summary makes the command refuse to run.
- Fix: Change the required monthly export count to 24.

### 2. Bank B dates use the wrong format
- Severity: blocker
- Claim: Parsing every date as `%d/%m/%Y` contradicts Bank B’s `%m/%d/%Y` format.
- Why it matters: Bank B dates such as `12/31/2026` fail parsing, while `01/02/2026` silently moves January spending into February.
- Fix: Parse dates using each bank’s specified format before joining the tables.

### 3. Transfers inflate spending
- Severity: major
- Claim: Keeping every negative amount includes outgoing transfers between the two accounts.
- Why it matters: Whenever an internal transfer occurs, its debit increases reported spending while its corresponding credit is discarded; the proposed negative-row total check also accepts this error.
- Fix: Identify and exclude internal-transfer debits before aggregation.

### 4. Deleting inputs prevents the planned rerun
- Severity: major
- Claim: Monthly exports are deleted before the keyword refinement and manual verification steps.
- Why it matters: After adding keywords, the next command has no source transactions to reclassify, and the bank files needed for verification are gone.
- Fix: Retain the monthly export files.

### 5. Generated output becomes an input
- Severity: major
- Claim: `exports/summary.csv` matches the same file pattern used to count and read bank exports.
- Why it matters: On a subsequent run with the monthly exports retained or restored, the summary adds an extra CSV and triggers the file-count rejection.
- Fix: Write the summary outside `exports/`.