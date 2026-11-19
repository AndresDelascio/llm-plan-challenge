## Brief
- Goal: The forward paper log for 12 frozen trading-strategy candidates runs once after every US trading session from 2026-11-17 onward without me starting it, and one status file tells me whether any session is missing or wrong.
- Constraints: One person, not a trained software engineer. A Windows 11 desktop that is not always switched on. Free Twelve Data 1-minute bars for SPY and QQQ, fetched after the close. An existing script, `research/paper_trader.py`, already computes simulated fills for one session and refuses dates before 2026-11-17; no session has been run yet. An existing NYSE calendar module. Python with numpy and DuckDB only (pyarrow is blocked on this PC). No paid services. Registered research rule: the 12 candidates and their parameters are frozen, every forward day is out-of-sample, and nothing is changed because of forward results.
- Non-goals: No broker connection, no orders, no real money. No new strategies and no tuning. No dashboard beyond one generated text file. No cloud hosting.

## Plan
1. Add one entry point, `run_forward.py`. It builds the list of trading sessions from 2026-11-17 to the last completed session using the existing NYSE calendar, and processes every session not yet in the log, oldest first. This is the catch-up for days the PC was off.
2. Windows Task Scheduler starts it on weekdays at 18:00 Toronto time, with "run as soon as possible after a missed start" switched on. The task starts only if a network connection is available and restarts on failure every 10 minutes, up to 3 times, so a run that fires at boot does not fail once and wait for the next boot.
3. For each session it downloads the day's 1-minute bars for SPY and QQQ, checks them (390 regular-session bars on a full day, fewer on calendar half days, no gaps, no duplicate timestamps), saves the raw bars to a file and records the file's hash.
4. It then calls the existing paper trader for that date. Results go to an append-only log: one row per candidate per session, with the data hash, the code commit id and the run time.
5. A session already in the log is never recomputed. A deliberate rerun needs an explicit flag and adds a correction row; it never overwrites.
6. If the download fails or the bars fail the check, nothing is written for that session. The failure goes to a run log and the session is retried on the next run. After 3 failed runs for the same session the status file flags it.
7. Every run regenerates `forward_status.md`: sessions expected, logged and missing; last run time; progress of the 14-session warm-up that some candidates need; and cumulative results under both registered scorings. The file opens with a fixed line: simulated fills, a record only, cannot promote any candidate.
8. Tests on synthetic data: catch-up after a gap, a holiday, a half day, a duplicate run changing nothing, incomplete bars refused, a date before the start refused.
9. Before the schedule is switched on: download and check one real session from before 2026-11-17 (download and check only, nothing is logged). Confirm the bar count and the timestamp convention match what the check in step 3 expects. If they do not, fix the check first.
10. Done when, after 5 consecutive trading sessions, the status file shows 5 expected, 5 logged and 0 missing, and I started none of the runs by hand.

## Risks I already know about
- The data vendor may revise or backfill bars after the close, so bars fetched late can differ from bars fetched the same evening.
- The free data tier has request limits; a long catch-up could hit them.
- Simulated fills are derived from minute bars and are not broker fills.
- Seeing results every day is a temptation to change the frozen candidates.
- The scheduled task runs only while my Windows user is able to run tasks; a long shutdown delays the log.
