## Brief
- Goal: One command produces a table of my 2026 spending by category and month, built from the monthly CSV exports of my two bank accounts.
- Constraints: Python with pandas, run by hand on my own PC, fully offline. Each bank gives one CSV export per month. Bank A writes dates as DD/MM/YYYY and Bank B writes them as MM/DD/YYYY. Both banks list spending as negative amounts. I am the only user.
- Non-goals: No budgeting or forecasting. No connection to a bank API. No charts.

## Plan
1. Put the exports in one folder, `exports/`: one file per month from each of the two banks, 12 files in total. The script refuses to run unless exactly 12 CSV files are present.
2. The script, `summarise.py`, reads every `*.csv` file in `exports/` and joins them into one table with the columns date, description, amount and bank. The bank is taken from the file name.
3. Parse the date column of the joined table with the format `%d/%m/%Y` and add a month column from it.
4. Drop rows where the amount is zero or positive, so only spending is left.
5. Assign a category to each row from a hand-written list of keywords in one config file, `categories.toml` (for example "LOBLAWS" → groceries). A row that matches no keyword gets the category "other".
6. Build the summary: total amount per category per month, with a yearly total column, and write it to `exports/summary.csv`.
7. To keep the folder tidy, the script deletes the monthly export files once the summary has been written.
8. Print the 20 largest rows in "other" so I can add keywords and run it again.
9. Test with a small made-up set of files: a known total per category, a row with no keyword, a positive row that must be dropped.
10. Done when the yearly total in the summary equals the sum of the spending rows in the bank files, checked by hand for both banks.

## Risks I already know about
- Keyword matching will put some rows in the wrong category; the "other" list is how I catch them.
- A bank may change its CSV column names during the year.
- A transfer between my two accounts looks like spending in one of them.
