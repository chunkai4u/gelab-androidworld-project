"""Continuous emulator-only recording in <=170-second Android segments."""
import pathlib, subprocess, threading, time

class Recorder:
    def __init__(self, adb, folder):
        self.adb=adb; self.folder=pathlib.Path(folder); self.folder.mkdir(parents=True,exist_ok=True)
        self.stop_event=threading.Event(); self.error=None; self.parts=[]
        self.tag='aw_'+str(time.time_ns())
    def cmd(self,*args,**kw):
        return subprocess.run([self.adb,'-s','emulator-5554',*args],check=kw.pop('check',True),timeout=kw.pop('timeout',60),**kw)
    def start(self):
        self.thread=threading.Thread(target=self._loop,daemon=True); self.thread.start()
        return self
    def _loop(self):
        try:
            i=0
            while not self.stop_event.is_set():
                remote=f'/sdcard/{self.tag}_{i}.mp4'; local=self.folder/f'part-{i:03d}.mp4'
                command=f'screenrecord --size 540x1200 --bit-rate 2000000 --time-limit 170 {remote} & echo $! > /sdcard/{self.tag}.pid; wait'
                with open(self.folder/'recording.log','a') as log:
                    result=self.cmd('shell',command,stdout=log,stderr=log,check=False,timeout=240)
                    if result.returncode: log.write('ADB recorder connection ended; attempting to recover video.\n')
                self.cmd('pull',remote,str(local),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                self.cmd('shell','rm',remote,stdout=subprocess.DEVNULL)
                if local.exists() and local.stat().st_size>1000: self.parts.append(local)
                i+=1
        except Exception as e: self.error=str(e)
    def stop(self):
        self.stop_event.set()
        # Signal only the screenrecord process started by this recorder.
        self.cmd('shell',f'if [ -f /sdcard/{self.tag}.pid ]; then kill -2 $(cat /sdcard/{self.tag}.pid) 2>/dev/null || true; fi',stdout=subprocess.DEVNULL)
        self.thread.join(40)
        if self.thread.is_alive(): raise RuntimeError('Recorder did not finish')
        if self.error and not self.parts: raise RuntimeError(self.error)
        if self.error:
            with (self.folder/'recording.log').open('a') as log: log.write('INCOMPLETE RECORDING: '+self.error+'\n')
        if not self.parts: raise RuntimeError('No video was recorded')
        manifest=self.folder/'parts.txt'
        manifest.write_text(''.join("file '"+p.name+"'\n" for p in self.parts))
        output=self.folder/'recording.mp4'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(manifest),'-c','copy','-movflags','+faststart',str(output)],check=True)
        self.cmd('shell','rm',f'/sdcard/{self.tag}.pid',stdout=subprocess.DEVNULL)
        return output
