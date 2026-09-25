# Prompt handling and verification

This document explains why the Calendar demonstration changed from a failed development run to a verified successful run.

## The comparison

| Run | User prompt | System task goal | Result |
|---|---|---|---|
| Earlier development run | `add a calendar event, today 5pm, a date with amy, that will last for an hour` | An AndroidWorld-generated task for **Call with Bob**, 2023-10-18 at 00:00, 45 minutes | `FAIL` after 20 steps |
| Improved run | `Create exactly one event in Simple Calendar Pro. Date: 10/1 Start time: 18:00 End time: 19:00 Title: Appointment with Hafid. Do not use All-day.` | A free-form goal with the requested date, start time, end time, title, and UI constraints | `CUSTOM_CALENDAR_PASS` after 16 steps |

This is a development comparison, not a controlled prompt-only experiment. The request handler was improved between the two runs. The purpose is to show why a GUI agent needs both clear input fields and code that preserves those fields.

## Evidence

- Failed earlier run: [`examples/calendar-vague-prompt-failed/`](examples/calendar-vague-prompt-failed/)
- Improved successful run: [`examples/calendar-demo-pass/`](examples/calendar-demo-pass/)

Each GitHub folder contains:

- `action-trace.txt`: readable step-by-step trace.
- `trajectory.jsonl`: original structured action records.
- `result.json`: task goal, result, and metadata.

The improved run also includes `recording.mp4` on GitHub. The final submission ZIP additionally includes the recording for the earlier failed run.

## Parameter parser

The parser is implemented in [`outputs/androidworld-project/chat_with_android.py`](outputs/androidworld-project/chat_with_android.py).

`freeform_goal()` extracts explicit Calendar fields such as `Date`, `Start time`, `End time`, and `Title`. It then creates a precise task goal for GELab-Zero. The model receives this goal together with the current Android screenshot and chooses one action at a time.

```python
explicit_date = re.search(r"\bdate\s*:\s*(\d{1,2})\s*/\s*(\d{1,2})", lowered)
explicit_start = re.search(r"\bstart\s*time\s*:\s*(\d{1,2})\s*:\s*(\d{2})", lowered)
explicit_end = re.search(r"\bend\s*time\s*:\s*(\d{1,2})\s*:\s*(\d{2})", lowered)
explicit_title = re.search(r"\btitle\s*:\s*([^\n.]+?)", text, re.I)
```

## Database verifier

The Calendar verifier is implemented in [`outputs/androidworld-project/run_task.py`](outputs/androidworld-project/run_task.py).

It reads the real Simple Calendar Pro database from the emulator and compares the saved title, date, start time, and end time against the expected values.

```python
if expected['title'] and row.title != expected['title']: continue
if expected['date'] and (start_at.month, start_at.day) != expected_date: continue
if expected['start'] and (start_at.hour, start_at.minute) != expected_start: continue
if expected['end'] and (end_at.hour, end_at.minute) != expected_end: continue
return True
```

`CUSTOM_CALENDAR_PASS` means this custom database verifier found a matching event. It is clearly labelled as a custom result and is not presented as an official AndroidWorld benchmark score.

## Suggested explanation

> The early workflow did not preserve the user's required details. We improved the system so Python extracts the important fields, GELab-Zero operates the screen using an exact goal, and a database verifier checks the saved event. The model's own completion message is not treated as proof.
