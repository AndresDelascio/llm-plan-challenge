## Brief
- Goal: The forward paper log for 12 frozen trading-strategy candidates runs once after every US trading session from 2026-11-17 onward without me starting it, and one status file tells me whether any session is missing or wrong.
- Constraints: One person, not a trained software engineer. A Windows 11 desktop that is not always switched on. Free Twelve Data 1-minute bars for SPY and QQQ, fetched after the close. An existing script, `research/paper_trader.py`, already computes simulated fills for one session and refuses dates before 2026-11-17; no session has been run yet. An existing NYSE calendar module. Python with numpy and DuckDB only (pyarrow is blocked on this PC). No paid services. Registered research rule: the 12 candidates and their parameters are frozen, every forward day is out-of-sample, and nothing is changed because of forward results.
- Non-goals: No broker connection, no orders, no real money. No new strategies and no tuning. No dashboard beyond one generated text file. No cloud hosting.

## Plan
1. Add one entry point, `run_forward.py`. It lists the trading sessions from 2026-11-17 to the last completed session with the existing NYSE calendar and processes every session not yet logged, oldest first.
2. Windows Task Scheduler starts it on weekdays at 18:00 Toronto time, with "run as soon as possible after a missed start" on. The task starts only if a network connection is available and restarts on failure every 10 minutes, up to 3 times.
3. For each session it downloads the 1-minute bars for SPY and QQQ, checks them (390 bars on a full day, fewer on calendar half days, no gaps or duplicate timestamps), saves the raw bars and records the file's hash.
4. It then calls the existing paper trader, which reads the saved file from step 3, not a fresh download. The append-only log gets one row per candidate per session, with the hash of the file actually read, the code commit id and the run time. A session's 12 rows are written in one DuckDB transaction; a session counts as logged only with exactly 12 rows.
5. A logged session is never recomputed. A deliberate rerun needs an explicit flag and adds 12 correction rows with a version number and the version replaced; nothing is overwritten. Status and both scorings use only each session's latest version.
6. If the download or the check fails, nothing is written for that session, the failure is logged and the run stops before any later session. The session is retried on the next run; after 3 failed runs the status file flags it. Only I can close a session that will never have data, with a flag that writes 12 "no data" rows.
7. Every run regenerates `forward_status.md`, also when the run fails (a `finally` block, absolute paths). Line 1: the time generated and the last session covered. Line 2, fixed: simulated fills, a record only, cannot promote any candidate. Then: sessions expected, logged and missing; sessions without exactly 12 rows or whose saved bars no longer match their hash; 14-session warm-up progress; cumulative results under both registered scorings.
8. Tests on synthetic data: gap catch-up, holiday, half day, duplicate run changes nothing, incomplete bars refused, pre-start date refused, stop at a failed session, interrupted write leaves no rows, correction counted once.
9. Before scheduling: download and check one real session from before 2026-11-17 (nothing is logged). Confirm the bar count and timestamp convention match step 3's check; if not, fix the check first.
10. Done when, after 5 consecutive trading sessions, the status file shows 5 expected, 5 logged and 0 missing, with no run started by hand.

## Risks I already know about
- The data vendor may revise or backfill bars after the close, so bars fetched late can differ from bars fetched the same evening.
- The free data tier has request limits; a long catch-up could hit them.
- Simulated fills are derived from minute bars and are not broker fills.
- Seeing results every day is a temptation to change the frozen candidates.
- The scheduled task runs only while my Windows user is able to run tasks; a long shutdown delays the log.
