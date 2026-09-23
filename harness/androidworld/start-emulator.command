#!/bin/bash
source "$(dirname "$0")/env.sh"
if adb devices | awk '$1 == "emulator-5554" { found=1 } END { exit !found }'; then
  echo 'AndroidWorld emulator is already running.'
else
  python - <<'PY'
import os,subprocess
with open(os.environ['ANDROID_HOME']+'/../emulator.log','a') as log:
    # Configuration verified by the latest live Wi-Fi PASS on the reference Mac.
    subprocess.Popen([os.environ['ANDROID_HOME']+'/emulator/emulator','-avd','AndroidWorldAvd','-port','5554','-grpc','8554','-no-snapshot','-no-boot-anim','-no-metrics','-gpu','host','-feature','-Vulkan','-memory','4096','-cores','4'],stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
PY
  echo 'Starting AndroidWorld emulator. First boot can take several minutes.'
fi
