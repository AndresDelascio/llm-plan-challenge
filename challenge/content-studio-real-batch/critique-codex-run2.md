VERDICT: BLOCKED

### 1. Total time is not measured
- Severity: blocker
- Claim: Step 8 records finding and editing minutes but omits other hands-on work required for step 9’s total time per clip.
- Why it matters: Previewing, transferring, checking and troubleshooting exports can consume substantial time; excluding it can push finding above the 50% threshold and select the wrong next step.
- Fix: Record all hands-on minutes per clip, including validation and retries, and use their sum as the denominator; exclude unattended processing time.

### 2. HDR repair bypasses revision approval
- Severity: major
- Claim: Step 7 changes rendering after approval without requiring preview and approval of the changed revision.
- Why it matters: When tone mapping is needed, the final export can pass technical checks while differing from the approved preview, leaving its approval unsupported.
- Fix: Apply the correction to preview and export, approve the corrected revision, then repeat the export checks.

### 3. Mixed results have no decision rule
- Severity: major
- Claim: Step 9 specifies a threshold per clip but does not combine three clip results into one next-step decision.
- Why it matters: If one clip exceeds 50% finding time and two do not, the rule directs both building a candidate list and improving editing first.
- Fix: Define one batch-level calculation now, such as total finding minutes divided by total hands-on minutes across all three clips.