#!/bin/bash
set -e
source "$(dirname "$0")/env.sh"
printf 'Start the existing Pod in Runpod first. This restores its model service.\n'
if python "$TASK_DIR/outputs/gelab-runpod/client.py" >/dev/null 2>&1; then
  echo 'Cloud model is already ready.'
else
  python "$TASK_DIR/outputs/gelab-runpod/bootstrap.py"
  python - <<'PY'
import client,time
print('Loading cloud model; this can take several minutes.',flush=True)
deadline=time.monotonic()+600
while time.monotonic()<deadline:
    try:
        if client.health().get('ready'):
            print('Cloud model is ready.',flush=True); break
    except Exception: pass
    time.sleep(10)
else: raise SystemExit('Model setup did not finish. Ask Codex to check the Runpod setup log.')
PY
fi
read -r -p 'Press Enter to close.'
