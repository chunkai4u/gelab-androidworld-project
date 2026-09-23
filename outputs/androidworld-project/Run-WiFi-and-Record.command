#!/bin/bash
set -e
source "$(dirname "$0")/env.sh"
"$PROJECT_DIR/start-emulator.command"
python "$PROJECT_DIR/wait_ready.py"
python "$PROJECT_DIR/run_task.py" --task SystemWifiTurnOn --runs 1 --max-steps 15
printf '\nFinished. Videos and results are in the runs folder. Press Enter to close.\n'
read -r
