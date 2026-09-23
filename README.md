# GELab-Zero × AndroidWorld course project

**English** | [🌐 繁體中文](README.zh-TW.md)

Status: a working live Wi-Fi prototype was verified on 2026-09-23. This repository is not a completed benchmark submission.

## What exists

- A private Runpod model service for GELab-Zero-4B-preview, plus bootstrap and SSH client scripts.
- An AndroidWorld agent adapter, task runners, step budgets, a limited app allowlist, observation/action logs, official verifier integration, and emulator video recording.
- Launchers for SystemWifiTurnOn, MarkorCreateNote, and MarkorCreateNoteAndSms.
- A live Wi-Fi development run: 5 actions, official score 1.0/PASS, 71.16 seconds of video. The video, final screenshot, trace, and result are in [`examples/live-wifi-pass`](examples/live-wifi-pass/).
- A [live demo and verification guide](LIVE_DEMO.md), including a concise code tour and fallback plan.

## What is not finished

The Intel Mac emulator has previously shown Settings/System UI ANRs. Markor has not passed end to end. The SMS composite task has not been tested. The YADB input adapter remains unverified end to end. Three runs per task (nine formal runs) have not started.

The successful Wi-Fi example validates the reference configuration recorded in its result file. Do not use development attempts to calculate a formal success rate.

## Layout

- `outputs/gelab-runpod/`: cloud model service, private client, and rebuild scripts.
- `outputs/androidworld-project/`: Mac launchers, agent, recording, baseline handling, and environment notes.
- `examples/live-wifi-pass/`: latest video, trace, final screenshot, and sanitized official verifier result.
- `ISSUES.md`: the next concrete work items.

The `outputs/` layout is retained because the existing launchers resolve the local `work/` directory relative to it. Do not flatten these folders without adjusting paths.

## Working as a team

Everyone can clone the code and review logs without installing AndroidWorld. Start with one experiment operator and, later, one backup machine. Other members can work on the adapter, model service, failure analysis, and presentation. Use a branch per issue and review changes through pull requests. Record the code revision, model, task seed, and environment configuration for every reported run.

Only the experiment operator needs the full Android emulator and AndroidWorld setup. This source bundle is not a portable one-click installer. The launchers currently target an Intel Mac and expect dependencies, app snapshots, SDK/AVD, and a Python environment in an untracked `work/` directory. See the component README files before attempting to reproduce it.

The YADB helper comes from the official GELab-Zero repository at commit `7b619f6f67d2b1101021fc453cb27bd48a29e4f2`; the local integration expects that source checkout at `work/gelab-zero-source`. AndroidWorld is pinned to `e3fea3ccc69787570e282c99573298f1c3019a34`. The lockfile describes the reference Mac and is not a universal installer.

## Access and large files

No SSH private key, account credential, model weight, emulator image, or virtual environment is included. Runpod connection identifiers are placeholders in this bundle. Each cloud user needs their own authorized SSH key and host configuration; do not share the reference Mac's private key. The checked-in Wi-Fi recording is intentionally small (about 0.6 MB) and is included with its verifier evidence.

This is a private team repository. Track work in [GitHub Issues](https://github.com/chunkai4u/gelab-androidworld-project/issues). Collaborators have not been invited yet.
