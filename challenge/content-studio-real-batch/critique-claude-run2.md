VERDICT: PROCEED WITH CHANGES

### 1. Wide action clip may have no passing layout
- Severity: major
- Claim: Step 6 requires the ball to stay visible, but a fixed vertical crop of wide footage shows about a third of the frame width, and a full-width fit shrinks the ball to a few pixels.
- Why it matters: The wide-session clip can fail step 6 on every existing layout, so step 10 is never met.
- Fix: Before cutting, define "visible" and the fallback: pick a moment that stays inside one crop window, or record "no layout passes" as a valid result.

### 2. Only HDR has a fix path
- Severity: major
- Claim: Step 2 lists variable frame rate, rotation, HEVC and audio layout, but only HDR gets a remedy (step 7).
- Why it matters: Variable-frame-rate drift appears late in long recordings, so audio sync or cut points fail at step 6 after the full cut and caption work is spent.
- Fix: After step 2, export a 10-second uncaptioned test from near the end of each source and phone-check it before the real cuts.

### 3. Tone mapping is assumed available and skips the preview
- Severity: major
- Claim: Step 7 assumes the installed FFmpeg has a working tone-mapping chain (typically zscale or libplacebo) and applies it to the export only.
- Why it matters: If the build lacks the filter, the fix needs a different FFmpeg build mid-task. If the preview is not tone mapped, you approve a look the export does not have.
- Fix: In step 2, read the transfer characteristic with ffprobe and check `ffmpeg -filters`; apply the same filter to the preview.

### 4. Time data will not support the decision rule
- Severity: major
- Claim: Step 8 has no bucket for first-run debugging or render waits, and step 9 does not say how three clips combine.
- Why it matters: Debugging time inflates the total and shrinks the finding share, biasing the decision. Tutorial and action clips may also land on opposite sides of 50%.
- Fix: Log debugging and render waits separately and exclude them; state the rule on summed minutes across all three clips.

### 5. Transfers can alter the files
- Severity: minor
- Claim: The plan names no transfer method in either direction.
- Why it matters: Some phones transcode HEVC/HDR on USB import to Windows, so the "original" is not original. A messaging app recompresses and breaks the no-cloud constraint.
- Fix: Set the phone to keep originals, and copy exports by USB.
