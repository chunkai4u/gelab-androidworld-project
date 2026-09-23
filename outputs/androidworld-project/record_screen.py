import datetime,os,pathlib,time
from recorder import Recorder
folder=pathlib.Path(__file__).parent/'runs'/('manual-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
r=Recorder(os.environ['ANDROID_HOME']+'/platform-tools/adb',folder).start()
print('Recording emulator only. Press Enter to stop and save.',flush=True)
try: input()
except (KeyboardInterrupt,EOFError): pass
print('Saved:',r.stop(),flush=True)
