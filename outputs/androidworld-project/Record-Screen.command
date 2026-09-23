#!/bin/bash
set -e
source "$(dirname "$0")/env.sh"
"$PROJECT_DIR/start-emulator.command"
python "$PROJECT_DIR/wait_ready.py"
python "$PROJECT_DIR/record_screen.py"
