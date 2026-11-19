VERDICT: PROCEED WITH CHANGES

### 1. Pipeline debugging lands inside the timed clips
- Severity: major
- Claim: Step 2 lists unhandled formats, but the first real export of each happens in step 4, and only HDR has a remedy.
- Why it matters: Variable frame rate (audio drift, shifted in and out points) or rotation metadata (wrong crop) surface at step 5 or 6, after a full cut. The rework then inflates the cutting minutes and retry counts in step 8.
- Fix: After step 2, export an uncaptioned 10-second throwaway clip from each source and run steps 5 and 6 on it. Fix format problems there, then start the timed clips.

### 2. The decision rule's inputs are undefined
- Severity: major
- Claim: "Total time per clip" does not say whether export retries and fix time count, or how three clips combine into one answer.
- Why it matters: The three source types will likely disagree, for example finding dominating only on the action session. Counting retry time shrinks the finding share. The step 9 rule can then go either way on the same data.
- Fix: Define total as finding plus cutting and captioning minutes only, with fix time logged separately. Decide on the pooled sum across the three clips.

### 3. Tone mapping may not be possible without a new dependency
- Severity: major
- Claim: Step 7 assumes the installed FFmpeg build has a usable tone-mapping filter chain, which is unverified.
- Why it matters: If the build lacks zscale, an HDR clip cannot pass step 6 without breaking "no new dependencies". The gap only appears after cutting. A preview without tone mapping also means approval covers a picture that differs from the export.
- Fix: In step 2, run `ffmpeg -filters` and confirm `zscale` and `tonemap` are present. If step 7 triggers, apply the same filter to the draft preview and re-approve.

### 4. Phone transfer method is unspecified
- Severity: major
- Claim: Step 6 does not say how the file reaches the phone, and the method named in the risks is a messaging app.
- Why it matters: A messaging app is a cloud upload of footage whose permission is still unknown, which breaks a stated constraint. Its recompression also makes the colour, sync and ball-visibility checks invalid.
- Fix: State in step 6 that transfer is by USB cable, and confirm the file size on the phone matches the PC.
