#!/bin/bash
# Installs the AndroidWorld-pinned Simple Calendar Pro APK and its task permissions.
set -e
source "$(dirname "$0")/env.sh"
apk="$(python - <<'PY'
from android_world.env.setup_device import apps
print(apps.download_app_data('com.simplemobiletools.calendar.pro_238.apk'))
PY
)"
adb -s emulator-5554 install -r "$apk"
adb -s emulator-5554 shell pm grant com.simplemobiletools.calendar.pro android.permission.READ_CALENDAR
adb -s emulator-5554 shell pm grant com.simplemobiletools.calendar.pro android.permission.WRITE_CALENDAR
adb -s emulator-5554 shell pm grant com.simplemobiletools.calendar.pro android.permission.POST_NOTIFICATIONS || true
echo 'Simple Calendar Pro is ready for AndroidWorld calendar tasks.'
