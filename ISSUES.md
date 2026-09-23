# Handoff backlog

1. **P0 — Stabilize the emulator (environment owner).** Reproduce the recurring System UI/Settings ANRs. The prepared 3 GB SwiftShader / native 540×1200 configuration has not been boot-tested. Confirm app opening and repeated input remain responsive before starting another model experiment.
2. **P0 — Verify the input adapter (agent owner).** Test the upstream YADB helper with filenames, spaces, punctuation, and multiline note text. Earlier AndroidWorld text injection dropped characters; the replacement is implemented but unverified. Preserve the exact requested content and do not automatically submit fields.
3. **P1 — Finish task smoke tests (experiment owner).** Complete MarkorCreateNote and MarkorCreateNoteAndSms through the model loop and the unmodified official task verifiers. Check that recordings are complete. Retain failures with the actual reason.
4. **P1 — Freeze and evaluate (evaluation owner).** Freeze code/environment/model settings, then perform three runs per selected task with recorded seeds. Collect verifier success, actions, elapsed time, complete video/log links, and failure categories. Infrastructure failures must be identified separately; do not silently omit them.
5. **P1 — Explain the result (presentation owner).** Show the three task categories, architecture, actual success rates, and examples of failures/recovery. Disclose that this is a custom GELab integration and a modified AndroidWorld task-subset environment.

Suggested review rule: changes to the model prompt, input adapter, device settings, or verifier plumbing require a new clearly labeled smoke test before the formal configuration is frozen. Do not change official verifiers merely to obtain PASS.
