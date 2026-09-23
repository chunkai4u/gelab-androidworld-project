# GELab-Zero × AndroidWorld course project

**English** | [🌐 繁體中文](README.zh-TW.md)

Status: a working live Wi-Fi prototype was verified on 2026-09-23. This repository is not a completed benchmark submission.

## The project in one story

The course defines an agent as a model, plus the context placed in front of it, plus the tools it can use to act. This repository follows that definition, and its folders follow the week in which each part is taught:

- **Monday, the model → [`model/runpod/`](model/runpod/).** Ours is GELab-Zero-4B-preview, a small vision model that looks at a phone screenshot and answers with one action: a tap, a swipe or a line of text to type. It runs on a rented Runpod GPU, and this folder starts it, reaches it over SSH and restores it. We do not change the model; we only serve it.
- **Tuesday and Wednesday, context and tools → [`harness/androidworld/`](harness/androidworld/).** The course calls everything written around the model the *harness*, and almost all of our own code is here. Each step, the harness takes a fresh screenshot from the emulator, adds the goal and the last few actions, and asks the model what to do. It checks the answer against our guardrails, turns it into a real tap or keystroke, and decides whether to continue or stop, recording a video and a trace as it goes.
- **Thursday, building and evaluating → [`results/`](results/).** AndroidWorld gives every task fresh random values and an official verifier that inspects the phone afterwards, so a run counts only when the verifier says PASS, not when the agent says it is done. Each run becomes one row in [`results/runs.csv`](results/runs.csv); development attempts go to [`results/development/`](results/development/) and the nine formal runs to [`results/formal/`](results/formal/). So far one run has passed: Wi-Fi turned on in five actions, with its video, final screen, trace and result in [`results/development/live-wifi-pass/`](results/development/live-wifi-pass/).
- **Friday, the presentation → [`presentation/`](presentation/).** The rows in `results/runs.csv` are the presentation; this folder holds the slides built from them.
- **Throughout the week, the team → [`docs/`](docs/).** The [handoff backlog](docs/ISSUES.md), the [contribution workflow](docs/CONTRIBUTING.md) and the [live demo guide](docs/LIVE_DEMO.md), each with a Traditional Chinese version.

## Where each harness part lives

The course names five parts of a harness, and two further ideas from the Day 2 lecture on context. This is where each one sits in our code today, and which ones we do not have yet.

| Course concept | In this repository |
|---|---|
| Loop control | The loop and `--max-steps` in `run_task.py`; the step budget in `gelab_agent.py` |
| Context assembly | `GelabAgent.step()`: screenshot, goal and the last eight actions; the model prompt in `model/runpod/prompt.txt` |
| Tool dispatch | `GelabAgent.execute()`; typing through the GELab YADB helper; swipes through ADB |
| Error recovery | `parse_action()` rejects malformed answers; a repeated unchanged screen stops the run; `run_task.py` still scores interrupted runs |
| Guardrails | The app allowlist (`ALLOWED_PACKAGES`), the payment block and the step cap |
| Logging | `recorder.py`, `trajectory.jsonl` and `result.json` for every run |
| Agent status bar (Day 2) | Not implemented |
| Memory (Day 2) | Only the last eight actions are sent back to the model |

The last two rows matter for the multi-app tasks. When an agent has to read a value in one app and type it in another, the course calls the typical failure `lost_value`, and a status bar or a scratch note is where the course says it is fixed.

## What is not finished

The Intel Mac emulator has previously shown Settings/System UI ANRs. Markor has not passed end to end. The SMS composite task has not been tested. The YADB input adapter remains unverified end to end. Three runs per task (nine formal runs) have not started.

The successful Wi-Fi example validates the reference configuration recorded in its result file. Do not use development attempts to calculate a formal success rate.

## Working as a team

Everyone can clone the code and review logs without installing AndroidWorld. Start with one experiment operator and, later, one backup machine. Other members can work on the adapter, model service, failure analysis, and presentation. Use a branch per issue and review changes through pull requests, as described in [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md). Record the code revision, model, task seed, and environment configuration for every reported run.

Only the experiment operator needs the full Android emulator and AndroidWorld setup. This source bundle is not a portable one-click installer. The launchers currently target an Intel Mac and expect dependencies, app snapshots, SDK/AVD, and a Python environment in an untracked `work/` directory at the repository root. `harness/androidworld/` and `model/runpod/` are both two levels deep because their scripts find `work/` that way; keep that depth if you move them.

The YADB helper comes from the official GELab-Zero repository at commit `7b619f6f67d2b1101021fc453cb27bd48a29e4f2`; the local integration expects that source checkout at `work/gelab-zero-source`. AndroidWorld is pinned to `e3fea3ccc69787570e282c99573298f1c3019a34`. The lockfile describes the reference Mac and is not a universal installer.

## Access and large files

No SSH private key, account credential, model weight, emulator image, or virtual environment is included. Runpod connection identifiers are placeholders in this bundle. Each cloud user needs their own authorized SSH key and host configuration; do not share the reference Mac's private key. The checked-in Wi-Fi recording is intentionally small (about 0.6 MB) and is included with its verifier evidence.

This is a private team repository. Track work in [GitHub Issues](https://github.com/chunkai4u/gelab-androidworld-project/issues).
