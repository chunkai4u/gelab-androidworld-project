"""Official AndroidWorld controller with its UIAutomator observation backend."""
import os, pathlib, subprocess
from android_env import loader
from android_env.components import config_classes
from android_world.env import android_world_controller as aw, env_launcher, interface
from android_env.proto import adb_pb2

class CourseController(aw.AndroidWorldController):
    def execute_adb_call(self, request):
        # Short upstream deadlines trigger disruptive ADB restarts on this Mac.
        if 0 < request.timeout_sec < 60:
            request_copy=adb_pb2.AdbRequest(); request_copy.CopyFrom(request)
            request_copy.timeout_sec=60; request=request_copy
        return super().execute_adb_call(request)

def load_environment(freeze_datetime=True, read_ui_tree=False):
    adb=os.environ['ANDROID_HOME']+'/platform-tools/adb'
    # The dedicated emulator uses UIAutomator, not the background forwarding app.
    subprocess.run([adb,'-s','emulator-5554','shell','settings','delete','secure','enabled_accessibility_services'],check=True,timeout=30,stdout=subprocess.DEVNULL)
    subprocess.run([adb,'-s','emulator-5554','shell','appops','set','--uid','net.gsantner.markor','MANAGE_EXTERNAL_STORAGE','allow'],check=True,timeout=30,stdout=subprocess.DEVNULL)
    helper=pathlib.Path(os.environ['ANDROID_SDK_ROOT']).parent/'gelab-zero-source'/'yadb'
    subprocess.run([adb,'-s','emulator-5554','push',str(helper),'/data/local/tmp/yadb'],check=True,timeout=30,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    task=pathlib.Path(os.environ['ANDROID_HOME']).parent/'androidworld-task.textproto'
    task.write_text('id: "default"\nname: "Default task for device control."\ndescription: "Empty task"\nmax_episode_sec: 7200\n')
    launch=config_classes.EmulatorLauncherConfig(emulator_console_port=5554,adb_port=5555,grpc_port=8554)
    if hasattr(launch,'connect_to_existing'): launch.connect_to_existing=True
    config=config_classes.AndroidEnvConfig(task=config_classes.FilesystemTaskConfig(path=str(task)),simulator=config_classes.EmulatorConfig(emulator_launcher=launch,adb_controller=config_classes.AdbControllerConfig(adb_path=adb)))
    raw=loader.load(config)
    method=aw.A11yMethod.UIAUTOMATOR if read_ui_tree else aw.A11yMethod.NONE
    controller=CourseController(raw,a11y_method=method,install_a11y_forwarding_app=False)
    env=interface.AsyncAndroidEnv(controller)
    env_launcher.setup_env(env,freeze_datetime=freeze_datetime)
    env.hide_automation_ui()
    return env
