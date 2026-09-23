import os, argparse
parser=argparse.ArgumentParser()
parser.add_argument('--resume-sms',action='store_true')
args=parser.parse_args()
from absl import flags, logging
flags.FLAGS(['setup'])
logging.set_verbosity(logging.WARNING)
from android_world.env import env_launcher
from android_world.env.setup_device import setup, apps
from environment import load_environment

print('Connecting AndroidWorld to the emulator...',flush=True)
env=load_environment(freeze_datetime=False,read_ui_tree=True)
selected=(apps.SimpleSMSMessengerApp,) if args.resume_sms else (apps.AndroidWorldApp, apps.SettingsApp, apps.MarkorApp, apps.SimpleSMSMessengerApp)
for app in selected:
    print('Setting up:',app.app_name,flush=True)
    setup.setup_apps(env, (app,))
env_launcher.setup_env(env,freeze_datetime=True)
s=env.get_state(wait_to_stabilize=True)
print('SETUP_OK',s.pixels.shape,flush=True)
env.close()
