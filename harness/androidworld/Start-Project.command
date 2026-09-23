#!/bin/bash
source "$(dirname "$0")/env.sh"
printf '\nGELab-Zero × AndroidWorld\n\n1. Turn on Wi-Fi\n2. Create a calendar event\n3. Create a note\n4. Create a note and share via SMS\n5. Log reimbursable expenses from Markor\n6. Record the emulator only (manual)\n\n'
read -r -p 'Choose 1–6: ' choice
case "$choice" in
  1) task=SystemWifiTurnOn; steps=15;;
  2) task=SimpleCalendarAddOneEvent; steps=30;;
  3) task=MarkorCreateNote; steps=25;;
  4) task=MarkorCreateNoteAndSms; steps=35;;
  5) task=ExpenseAddMultipleFromMarkor; steps=45;;
  6) exec "$PROJECT_DIR/Record-Screen.command";;
  *) echo 'No task selected.'; exit 0;;
esac
"$PROJECT_DIR/start-emulator.command"
python "$PROJECT_DIR/wait_ready.py" || exit 1
python "$PROJECT_DIR/run_task.py" --task "$task" --runs 1 --max-steps "$steps"
run_status=$?
if [ "$run_status" -ne 0 ]; then echo "Run stopped with an environment error. Keep this window open and show Codex the error."; fi
printf '\nFinished. Open the runs folder for videos and results.\n'
read -r -p 'Press Enter to close.'
