"""Wait for this project's emulator to finish booting."""
import os, subprocess, time
adb=os.environ['ANDROID_HOME']+'/platform-tools/adb'
deadline=time.monotonic()+600
print('Waiting for Android to finish starting...',flush=True)
while time.monotonic()<deadline:
    try:
        r=subprocess.run([adb,'-s','emulator-5554','shell','getprop','sys.boot_completed'],capture_output=True,text=True,timeout=10)
        if r.stdout.strip()=='1':
            print('Android is ready.',flush=True)
            break
    except subprocess.TimeoutExpired: pass
    time.sleep(3)
else: raise SystemExit('Android did not finish booting. Check work/emulator.log.')
