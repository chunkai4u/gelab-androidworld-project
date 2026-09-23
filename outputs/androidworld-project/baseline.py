"""Keep clean AndroidWorld app snapshots across emulator restarts."""
import os,pathlib,subprocess
from android_world.env import adb_utils
from android_world.utils import app_snapshot

APPS=('settings','simple calendar pro','markor','simple sms messenger')
REMOTE='/data/data/android_world/snapshots'
def _run(*args,**kwargs):
    return subprocess.run([os.environ['ANDROID_SDK_ROOT']+'/platform-tools/adb','-s','emulator-5554',*args],check=True,timeout=180,**kwargs)
def _cache():
    return pathlib.Path(os.environ['ANDROID_SDK_ROOT']).parent/'device-baseline'
def capture(env):
    adb_utils.set_root_if_needed(env.controller)
    for app in APPS:
        print('Saving clean app state:',app,flush=True)
        adb_utils.close_app(app,env.controller)
        app_snapshot.save_snapshot(app,env.controller)
    cache=_cache(); cache.mkdir(exist_ok=True)
    _run('pull',REMOTE,str(cache),stdout=subprocess.DEVNULL)
    print('Clean app states backed up locally.',flush=True)
def restore_if_missing(env):
    adb_utils.set_root_if_needed(env.controller)
    packages=['com.android.settings','com.simplemobiletools.calendar.pro','net.gsantner.markor','com.simplemobiletools.smsmessenger']
    check=' && '.join('[ -d '+REMOTE+'/'+p+' ]' for p in packages)
    status=_run('shell',check+' && echo ready || echo missing',capture_output=True,text=True).stdout.strip()
    if status=='ready': return
    saved=_cache()/'snapshots'
    if not saved.exists(): raise RuntimeError('Clean app snapshots are missing. Ask Codex to complete baseline setup.')
    print('Restoring clean app snapshots...',flush=True)
    _run('shell','mkdir','-p','/data/data/android_world')
    _run('push',str(saved),'/data/data/android_world/',stdout=subprocess.DEVNULL)
