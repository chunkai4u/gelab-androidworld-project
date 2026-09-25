# GELab-Zero × AndroidWorld

A course project that builds a GUI agent for Android. A user types a request, GELab-Zero looks at the Android screen, Python performs one small action, and AndroidWorld checks the final result.

## What we built

- **GELab-Zero** chooses the next action from the task and current Android screenshot.
- **Runpod** provides the cloud GPU for the model.
- **Python** connects the model, local Android emulator, and verifier.
- **AndroidWorld** provides Android tasks and checks the real phone state.

## Demonstrations and evidence

| Task | Result | Evidence |
|---|---|---|
| `SystemWifiTurnOn` | Official AndroidWorld `PASS`, score 1.0 | [`examples/live-wifi-pass/`](examples/live-wifi-pass/) |
| `MarkorCreateNoteAndSms` | Official AndroidWorld `PASS`, score 1.0 | [`examples/markor-sms-pass/`](examples/markor-sms-pass/) |
| Calendar request | `CUSTOM_CALENDAR_PASS` after database check | [`examples/calendar-demo-pass/`](examples/calendar-demo-pass/) |

Each evidence folder contains a result file and visual evidence. The Calendar result is a custom verified demo and is not an official AndroidWorld benchmark score.

## Repository structure

- `outputs/androidworld-project/`: local Mac launcher, agent adapter, runner, and recorder.
- `outputs/gelab-runpod/`: Runpod model service and client code.
- `examples/`: selected successful runs for review.
- `SUBMISSION.md`: the short guide for graders.
- `PROMPT_AND_VERIFICATION.md`: Calendar prompt comparison, parser, verifier, and action logs.

## Run locally

The reference setup uses an Intel Mac, Android emulator, AndroidWorld, and a separately configured Runpod model service. It is not a portable one-click installer because the emulator, model weights, and credentials are intentionally excluded.

On the reference Mac, open `outputs/androidworld-project/Chat-With-Android.command` and type a supported request. The Terminal prints each action as `STEP`, and the run saves evidence under the local `runs/` directory.

## Security and scope

This repository does not include cloud credentials, SSH private keys, model weights, emulator images, or personal data. The included results are development demonstrations, not a full repeated benchmark evaluation.
