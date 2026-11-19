## Brief
- Goal: Three real soccer recordings go through my existing local clip workflow and give at least three approved short vertical clips that play correctly on a phone, with my time per clip measured, so I can decide whether automatic moment finding is worth building next.
- Constraints: One person, not a trained software engineer. Windows 11 desktop with an 8 GB NVIDIA GPU. An existing local app (Python and FFmpeg, version 0.1.0): source inventory, manual in and out points, vertical layouts, typed captions, draft preview, approval per revision, export from the original files with source hashes recorded. So far it has only run on generated test video (4 tests pass; export measured at 1080x1920, 30 fps, about -16 LUFS). The real footage is long phone recordings and may be HDR. Free local tools only; no cloud upload and no paid services. Every export is marked not ready for publication until permission is recorded for its source.
- Non-goals: No publishing or posting. No automatic moment finding. No transcription. No new dependencies in this step.

## Plan
1. Set the phone to keep originals when copying to a PC, then copy three recordings by USB cable into one inbox batch: one spoken coaching tutorial, one wide action session and one mixed session. The app inventories them and records the hashes.
2. Before cutting, inspect each source with ffprobe and list anything the app has not handled before: HDR (read the colour transfer field), variable frame rate, rotation metadata, HEVC, frame rate above 30 fps, audio layout. Also run `ffmpeg -filters` and confirm the installed FFmpeg has the `zscale` and `tonemap` filters. If a source is HDR and the filters are missing, stop and ask me: a different FFmpeg build is a new dependency.
3. Add one field per source: who appears and whether I have permission to publish (yes, no, unknown). An export can only be marked ready for publication when its source says yes.
4. Format test, not timed as clip work: export a 10-second clip without captions from near the end of each source and run steps 6 and 7 on it. Fix format problems here, before the real clips. Log this time as setup.
5. Cut one clip per source by hand: in and out points, vertical layout, typed captions, draft preview, approve, export. For the wide action session, pick a moment that stays inside one crop window.
6. Check each export on the PC: 1080x1920, 30 fps, full decode without errors, loudness near -16 LUFS, source hashes unchanged.
7. Check each export on a phone. Copy it by USB cable, never through a messaging app, and confirm the file size in bytes matches the PC. Check orientation, colours, audio in sync, captions inside the visible area, and the ball visible during fast action. "Visible" means I can follow the ball by eye for the whole clip with the phone at arm's length. If no layout passes for the wide action session, write "no layout passes for wide footage" as a result and cut the third clip from the mixed session instead.
8. If HDR sources look washed out, add tone mapping with the FFmpeg filter to both the draft preview and the export. That makes a new revision: preview it, approve it again, export, and repeat steps 6 and 7.
9. For each clip, record hands-on minutes in three groups: finding the moment; cutting and captioning; checking (preview, transfer, PC and phone checks). Record separately, and leave out of the total: minutes spent fixing format or pipeline problems, and unattended render time. Also record the number of export retries.
10. Decision rule, fixed now: add up the three clips. If total finding minutes are more than half of total hands-on minutes (finding + cutting and captioning + checking), build a candidate list next. Otherwise improve the cutting and caption steps first. The per-clip split is reported but does not decide.
11. Done when three approved clips pass steps 6 and 7 and the time table from step 9 is written.

## Risks I already know about
- Three clips is a small sample, and I get faster with practice, so the time split may not hold.
- Converting 60 fps footage to 30 fps can blur or drop the ball during fast action.
- Long recordings may be slow to scrub through, which inflates the time spent finding a moment.
