# GELab-Zero × AndroidWorld

This Mac runs an Android 13 / API 33 Pixel 6 emulator. A Runpod L4 runs the official GELab-Zero-4B-preview model. The agent sends emulator screenshots through the project SSH connection, executes the model's next action, and uses AndroidWorld's task verifier to evaluate the result.

## Work paused — current status

Testing was stopped at the user’s request on 2026-09-23. The local emulator and experiment processes are stopped. The Runpod GPU remains running under the earlier authorization. This is a prototype, not a fully verified three-task deployment.

The latest launcher configuration (3 GB RAM, SwiftShader software graphics, native 540 × 1200 at 210 dpi) is an **untested candidate**. It was prepared immediately before work was paused and has not been boot-tested. The newly integrated official YADB text helper has not completed an end-to-end input test. Do not describe these changes as fixes proven to work.

## Verified on this Mac

On 2026-09-23, the cloud-connected agent completed `SystemWifiTurnOn` in 6 steps. The official AndroidWorld verifier returned `PASS` (score 1.0). The automatic H.264 recording is 71 seconds at 540 × 1200, saved in `runs/20260923-124310-SystemWifiTurnOn-1/recording.mp4`. This is a development smoke test, not the required three-run evaluation. Earlier infrastructure failures are retained separately.

## Start on this Mac

After resolving the pending environment issues below, double-click `Start-Project.command` in Finder and choose a task. The run automatically records the emulator and saves its results under `runs/`. Do not interact with the emulator while the agent is running.

- `Run-WiFi-and-Record.command`: start one Wi-Fi development run directly.
- `Chat-With-Android.command`: open a terminal chat. It recognizes English or Chinese Wi-Fi and calendar-event requests, starts the matching AndroidWorld task, then records the original request in `result.json`. It uses the generated official task details so the result remains verifier-scored.
- `Record-Screen.command`: record only the emulator; press Enter to stop and save. This does not run an agent or produce a benchmark score.
- `start-emulator.command`: open the emulator.

The cloud Pod must be running and its model service ready. The cloud setup lives in the sibling `gelab-runpod` folder. After stopping and restarting this temporary Pod, double-click `Restore-Cloud-Model.command` to restore the model service; allow a few minutes for model download/loading.

## Tasks

| Level | Task | Action budget |
|---|---|---:|
| Warm-up | SystemWifiTurnOn | 15 |
| Real work | SimpleCalendarAddOneEvent | 30 |
| Real work | MarkorCreateNote | 25 |
| Multi-app | MarkorCreateNoteAndSms | 35 |

`SimpleCalendarAddOneEvent` has been added to the launcher and uses the AndroidWorld-pinned Simple Calendar Pro app. Run `Install-Simple-Calendar.command` once on a fresh reference emulator before the first Calendar test. Calendar task metadata is serialized into `result.json`, and its clean app snapshot is included in the local baseline. The app integration is installed and prepared, but it has not yet passed an end-to-end model run.

Each menu selection runs one development attempt. The formal evaluation should run each task three times using a fixed configuration, retaining failures as well as successes. Do not count infrastructure smoke tests as formal evaluation runs.

## Run artifacts

Each run folder includes `recording.mp4`, `result.json`, `trajectory.jsonl`, screenshots of the model's observations, and a final screenshot when available. `result.json` distinguishes the agent's completion claim from the official verifier's result. A successful video alone is not a benchmark score. Review failures and annotate misclick, wrong app, loop, hallucinated state, or false completion as appropriate.

Recording is emulator-only, at 540 × 1200. Longer recordings use Android's segmented recording and are concatenated; small gaps may occur between segments. Audio, the Mac desktop and terminal output are not included.

## Architecture and limits

The custom `GelabAgent.step()` adapter translates GELab's normalized coordinates into AndroidWorld actions. The model receives fresh ADB screenshots and recent action history. Actions use AndroidWorld’s ADB actuation helpers, with a 3-second settling pause and an additional 10 seconds after app launch. The runtime uses AndroidWorld’s supported screenshot-only mode (`A11yMethod.NONE`) because accessibility-tree retrieval timed out on this Mac. UIAutomator was used during app setup. Short ADB operation deadlines are extended to 60 seconds; verifier logic is unchanged. A step cap and app allowlist restrict operation to the selected workflow and exclude browser, store and payment apps. The optional UI-text payment cue check is inactive without a UI tree. These prototype guardrails do not detect every possible payment screen; use only this dedicated emulator and these three tasks.

The adapter uses the official model weights and action prompt, but is a custom integration rather than the complete upstream GELab agent runtime. Report this distinction in the presentation. The selected task subset is installed; the entire AndroidWorld app suite is not installed.

## Team collaboration

One person can operate this reference environment while others review recordings, annotate errors, implement improvements, and prepare slides. A second teammate can reproduce the environment after the first end-to-end run is stable. Everyone does not need a GPU or an AndroidWorld installation.

Share source files through GitHub and keep videos separately. Never commit SSH private keys, API keys, model weights, the virtual environment, the emulator image, or emulator data. The cloud SSH key is local to this Mac and is not included in this folder. A teammate needs their own authorized access if they will call the cloud service from another computer.

## Reference versions

- AndroidWorld source: https://github.com/google-research/android_world
- Commit: `e3fea3ccc69787570e282c99573298f1c3019a34`
- Android API 33, Google APIs x86_64 system image revision 17; Pixel 6 profile.
- Local performance configuration: Candidate: 3 GB RAM, 2 emulator CPU cores, SwiftShader software graphics with Vulkan disabled; native display 540 × 1200 at 210 dpi. This candidate is not yet tested. The successful Wi-Fi run used 4 GB RAM, 2 cores, host graphics, physical 1080 × 2400 with a 540 × 1200 / 210 dpi override. This differs from native Pixel 6 rendering, so keep it fixed across all reported runs.
- Android Emulator 35.4.9, platform tools 37.0.1.
- Python 3.11; exact installed packages in `requirements-lock.txt`.
- GELab-Zero helper source commit: `7b619f6f67d2b1101021fc453cb27bd48a29e4f2`.
- Cloud: PyTorch 2.8.0, Transformers 4.57.6, GELab-Zero-4B-preview.

This folder's launchers use the local `../../work/` installation. On this Mac, `work` is a symbolic link to `~/Library/Caches/CodexAndroidWorld-s84` so the large emulator files stay in a local cache. Copying this folder to another computer is not sufficient to install the emulator; reproduce the dependencies and adjust paths first. The lockfile records this Mac’s packages; install AndroidWorld from the pinned source checkout rather than assuming its PyPI package matches that commit.

For this limited offline task subset, unrelated Google background apps were disabled inside the emulator to reduce repeated service ANRs: `com.google.android.as`, `com.google.android.gms`, `com.google.android.apps.wellbeing`, `com.google.android.projection.gearhead`, `com.google.android.apps.messaging`, `com.google.android.calendar`, `com.google.android.apps.maps`, and `com.google.android.settings.intelligence`. Keep this configuration fixed across runs. It is a modified task-subset environment, not an untouched full-suite benchmark. These packages can be restored with `adb shell pm enable PACKAGE`.

Markor’s manage-all-files permission is granted during environment preparation. Heads-up notifications are disabled in this dedicated emulator; no personal accounts are signed in. Clean app snapshots are also backed up in the local project cache and restored if missing after a restart.

Text entry uses the YADB helper shipped in the official GELab-Zero repository, without automatically pressing Enter. The local clone is stored in `work/gelab-zero-source`; the helper is copied into the dedicated emulator during environment preparation. The earlier Wi-Fi smoke test used 4 GB RAM; subsequent tuning reduced RAM to 2 GB to reduce host memory pressure. Formal runs must all use one fixed configuration.

## Outstanding work

1. Stabilize Android: Settings/System UI have produced recurring ANRs during longer runs.
2. Verify the newly added YADB text adapter and Markor filename/content entry.
3. Run `MarkorCreateNoteAndSms` end to end; its launcher exists but it is untested.
4. Freeze one environment/adapter configuration, then run all three tasks three times and retain all outcomes.

Do not combine the development/debug attempts into a formal success-rate claim.
