# Latest live Wi-Fi PASS

This directory contains a development run performed on 2026-09-23 with the cloud-connected GELab-Zero-4B-preview model. It is a reproducible presentation artifact, not a formal benchmark aggregate.

- `recording.mp4`: emulator-only recording of the run.
- `trajectory.jsonl`: model response and parsed UI action for each step.
- `result.json`: runner metadata plus the AndroidWorld official verifier outcome.
- `final.png`: final emulator observation.

The agent reported `COMPLETE` after five actions. The meaningful outcome is the independent `verifier: "PASS"` and `score: 1.0` in `result.json`.
