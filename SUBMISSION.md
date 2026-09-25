# Course project submission: GELab-Zero × AndroidWorld

## Repository

https://github.com/chunkai4u/gelab-androidworld-project

## Project in one sentence

We built a GUI agent that reads a user request, looks at an Android screen, takes one small action at a time, and verifies the final phone state.

## Main components

- **GELab-Zero**: the model that chooses the next Android action from a screenshot.
- **Runpod**: the cloud GPU used to run the model.
- **AndroidWorld**: the Android task environment and verifier.
- **Python**: connects the model, emulator, and verifier.

## Evidence included in this ZIP

| Demo | Result | Evidence folder |
|---|---|---|
| `SystemWifiTurnOn` | Official AndroidWorld `PASS`, score 1.0 | `examples/live-wifi-pass/` |
| `MarkorCreateNoteAndSms` | Official AndroidWorld `PASS`, score 1.0 | `examples/markor-sms-pass/` |
| Calendar request | Custom database verification `CUSTOM_CALENDAR_PASS` | `examples/calendar-demo-pass/` |

Each evidence folder contains a compact result file. The Wi-Fi and Calendar folders also include a recording. The Markor-to-SMS example is an official AndroidWorld task that creates a note and shares its full content using the emulator's SMS app.

## How verification works

A model response alone is not counted as success. AndroidWorld checks the real phone state. For example, it checks whether Wi-Fi is enabled, and whether the required note and SMS data are present. The calendar demo checks the saved Calendar database entry for its title, date, start time, and end time.

## Scope and limitation

The Wi-Fi and Markor-to-SMS results are official development passes. The Calendar result is a custom verified demonstration, not an official AndroidWorld benchmark score. This ZIP contains source code and selected evidence. It does not contain cloud credentials, model weights, emulator images, or a portable one-click environment.

## More explanation

Our class documentation is available in Notion:
https://app.notion.com/p/The-group-project-build-a-GUI-agent-3e3e84bdefa98039bd3af98a85dbcfd4
