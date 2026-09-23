#!/bin/bash
# Installs the AndroidWorld-pinned Pro Expense APK and clicks through its first-run screens.
set -e
source "$(dirname "$0")/env.sh"
cd "$PROJECT_DIR"
python - <<'PY'
from absl import flags, logging
flags.FLAGS(['setup'])
logging.set_verbosity(logging.WARNING)
from android_world.env.setup_device import setup, apps
from environment import load_environment
env=load_environment(freeze_datetime=False,read_ui_tree=True)
print('Setting up:',apps.ExpenseApp.app_name,flush=True)
setup.setup_apps(env,(apps.ExpenseApp,))
env.close()
PY
echo 'Pro Expense is ready for ExpenseAddMultipleFromMarkor.'
