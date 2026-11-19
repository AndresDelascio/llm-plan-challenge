# Answer key: planted flaws (written and committed before any critic ran)

Three made-up plans, 4 planted flaws each: 2 serious and 2 small. 12 planted flaws in total.

## Scoring rule (fixed before the runs)

- A planted flaw counts as **found** by a run when one of its issues names the same plan step (or the same Brief line) and the same failure. Naming the right step with a different failure does not count.
- A flaw mentioned only in passing inside another issue's text counts as found if the failure is stated, not if only the step is mentioned.
- Each run is scored on its own. A critic "found" a flaw if either of its two runs found it; the per-run numbers are reported too.
- Issues a critic raises that are not in this key are listed as "not planted". They are not counted as wrong: the plans may have real flaws I did not intend.
- Claude writes the plans, the key and does the scoring. Each score cites the issue number in the critique file so it can be checked.

## Plan A: balcony moisture logger

| Id | Size | Step | Planted flaw |
|---|---|---|---|
| A1 | serious | 6 (and Goal) | Wi-Fi on all the time at about 80 mA empties a 2,600 mAh cell in about 32 hours (computed: 2,600 / 80), not 90 days. |
| A2 | serious | 4 | Readings are kept only in memory, so one reset, crash or flat battery loses the whole history. |
| A3 | small | 5 | Wrong arithmetic: 4 readings an hour for 90 days is 8,640 per planter (4 × 24 × 90) and 34,560 values, not 2,160 and 8,640. |
| A4 | small | 1 (and Constraints) | The parts list adds up to C$112, over the C$80 budget. |

## Plan B: bank CSV summary

| Id | Size | Step | Planted flaw |
|---|---|---|---|
| B1 | serious | 3 (and Constraints) | One date format is used for both banks, but Bank B writes MM/DD/YYYY, so its rows land in the wrong month or fail to parse. |
| B2 | serious | 7 | The script deletes the bank export files after a run, so the source data is gone and step 8's "run it again" cannot work. |
| B3 | small | 1 | One file per month from each of two banks is 24 files, not 12; the "exactly 12" check refuses the correct folder. |
| B4 | small | 6 (with 2) | The summary is written as a CSV into the folder the script reads every CSV from, so a later run reads its own output as bank data (and breaks the file count). |

## Plan C: tournament sign-up page

| Id | Size | Step | Planted flaw |
|---|---|---|---|
| C1 | serious | 2 and 3 | The 16-team limit exists only in the page; the server saves every submission, so more than 16 teams can register. |
| C2 | serious | 4 | Captains' names, emails and phone numbers are on a page with no login, protected only by an unlisted link. |
| C3 | small | 5 and 6 | The schedule is built from the "final list" on Thursday 11 June, a day before registration closes on Friday 12 June. |
| C4 | small | 2 | Nothing stops the same team registering twice (double click, resubmit), which uses up two of the 16 places. |
