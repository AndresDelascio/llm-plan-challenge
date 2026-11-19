## Brief
- Goal: Three real soccer recordings go through my existing local clip workflow and give at least three approved short vertical clips that play correctly on a phone, with my time per clip measured, so I can decide whether automatic moment finding is worth building next.
- Constraints: One person, not a trained software engineer. Windows 11 desktop with an 8 GB NVIDIA GPU. An existing local app (Python and FFmpeg, version 0.1.0): source inventory, manual in and out points, vertical layouts, typed captions, draft preview, approval per revision, export from the original files with source hashes recorded. So far it has only run on generated test video (4 tests pass; export measured at 1080x1920, 30 fps, about -16 LUFS). The real footage is long phone recordings and may be HDR. Free local tools only; no cloud upload and no paid services. Every export is marked not ready for publication until permission is recorded for its source.
- Non-goals: No publishing or posting. No automatic moment finding. No transcription. No new dependencies in this step.

## Plan
1. Copy three recordings into one inbox batch: one spoken coaching tutorial, one wide action session and one mixed session. The app inventories them and records the hashes.
2. Before cutting, inspect each source with ffprobe and list anything the app has not handled before: HDR, variable frame rate, rotation metadata, HEVC, frame rate above 30 fps, audio layout.
3. Add one field per source: who appears and whether I have permission to publish (yes, no, unknown). An export can only be marked ready for publication when its source says yes.
4. Cut one clip per source by hand: in and out points, vertical layout, typed captions, draft preview, approve, export.
5. Check each export on the PC: 1080x1920, 30 fps, full decode without errors, loudness near -16 LUFS, source hashes unchanged.
6. Check each export on a phone: orientation, colours, audio in sync, captions inside the visible area, and the ball still visible during fast action.
7. If HDR sources look washed out, add tone mapping to the export with an FFmpeg filter, export again and repeat steps 5 and 6.
8. For each clip, record minutes spent finding the moment, minutes spent cutting and captioning, and the number of export retries.
9. Decision rule, fixed now: if finding the moment takes more than half of the total time per clip, build a candidate list next. Otherwise improve the cutting and caption steps first.
10. Done when three approved clips pass steps 5 and 6 and the time table from step 8 is written.

## Risks I already know about
- Three clips is a small sample, and I get faster with practice, so the time split may not hold.
- Converting 60 fps footage to 30 fps can blur or drop the ball during fast action.
- Moving a file to the phone through a messaging app may recompress it and hide or add problems.
- Long recordings may be slow to scrub through, which inflates the time spent finding a moment.
