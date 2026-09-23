import hashlib, io, json, os, pathlib, re, shlex, subprocess, time
from PIL import Image
from android_world.agents.base_agent import EnvironmentInteractingAgent, AgentInteractionResult
from android_world.env.json_action import JSONAction
from android_world.env import adb_utils, actuation
import client

APP_ALIASES={'settings':'settings','设置':'settings','設定':'settings','markor':'markor','notes':'markor','simple sms messenger':'simple sms messenger','sms':'simple sms messenger','messages':'simple sms messenger','短信':'simple sms messenger'}
ALLOWED_PACKAGES=('com.android.settings','net.gsantner.markor','com.simplemobiletools.smsmessenger','com.google.android.apps.nexuslauncher','com.android.launcher','com.android.systemui','com.android.permissioncontroller','com.google.android.permissioncontroller','com.example.androidworld')
APP_ALIASES.update({'com.android.settings':'settings','net.gsantner.markor':'markor','com.simplemobiletools.smsmessenger':'simple sms messenger','sms messenger':'simple sms messenger'})
def parse_action(text):
    # Match upstream's tab-separated format; note contents may contain newlines.
    body=re.split(r'</\s*(?:THINK|TINK)\s*>',text,flags=re.I)[-1].strip()
    fields={}
    for field in body.split('\t'):
        if ':' in field:
            key,value=field.split(':',1); fields[key.strip()]=value.strip()
    action=fields.get('action','')
    if not re.fullmatch(r'[A-Z]+',action): raise ValueError('Invalid model action: '+text)
    return action,fields
class GelabAgent(EnvironmentInteractingAgent):
    def __init__(self,env,folder,budget=20):
        super().__init__(env,name='GELab-Zero-4B-preview',transition_pause=3)
        self.screen_size=env.logical_screen_size
        self.adb=os.environ["ANDROID_SDK_ROOT"]+"/platform-tools/adb"
        self.folder=pathlib.Path(folder); self.history=[]; self.budget=budget; self.count=0; self.last=None; self.repeats=0
    def execute(self,action):
        actuation.execute_adb_action(action,[],self.screen_size,self.env.controller)
    def step(self,goal):
        if self.count>=self.budget: raise RuntimeError('Step limit reached')
        time.sleep(3)
        pixels=subprocess.check_output([self.adb,"-s","emulator-5554","exec-out","screencap","-p"],timeout=60)
        self.count+=1
        img=Image.open(io.BytesIO(pixels)).convert("RGB"); img.thumbnail((540,1200))
        path=self.folder/f'step-{self.count:03d}.jpg'; img.save(path,quality=85)
        response=client.step(path,goal,'\n'.join(self.history[-8:]))
        text=response['output']; action,fields=parse_action(text)
        fingerprint=hashlib.sha256(img.tobytes()).hexdigest()+text
        self.repeats=self.repeats+1 if fingerprint==self.last else 0; self.last=fingerprint
        if self.repeats>=2: raise RuntimeError('Repeated unchanged action/screen')
        record={'step':self.count,'model_response':response,'parsed_action':action,'fields':fields}
        self.history.append(text)
        with (self.folder/'trajectory.jsonl').open('a') as f: f.write(json.dumps(record,ensure_ascii=False)+'\n')
        if action=='COMPLETE': return AgentInteractionResult(True,record)
        if action in ('INFO','ABORT'): raise RuntimeError(action+': '+fields.get('value',''))
        if action=='WAIT': time.sleep(min(5,max(0,float(fields.get('value',1))))); return AgentInteractionResult(False,record)
        if action=='AWAKE':
            app=APP_ALIASES.get(fields.get('value','').strip().lower())
            if app is None: raise RuntimeError('Blocked app outside course allowlist')
            self.execute(JSONAction(action_type='open_app',app_name=app))
            time.sleep(10)
            return AgentInteractionResult(False,record)
        foreground=self.env.foreground_activity_name.lower()
        if not any(p in foreground for p in ALLOWED_PACKAGES): raise RuntimeError('Blocked foreground app: '+foreground)
        # No browser, store, finance or payment apps are allowed in this project.
        # Also stop before interacting with a visible purchase/payment flow.
        visible=''  # Screenshot-only mode has no UI text tree.
        if re.search(r'\b(pay now|checkout|buy now|purchase|confirm payment)\b|付款|支付|購買',visible,re.I):
            raise RuntimeError('Payment operation blocked')
        width,height=self.screen_size
        def point(key):
            m=re.fullmatch(r'\s*\(?\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\)?\s*',fields.get(key,''))
            if not m: raise ValueError('Invalid coordinates')
            x,y=map(float,m.groups())
            if not (0<=x<=1000 and 0<=y<=1000): raise ValueError('Coordinates out of range')
            return min(width-1,round(x*width/1000)),min(height-1,round(y*height/1000))
        if action in ('CLICK','LONGPRESS'):
            x,y=point('point'); self.execute(JSONAction(action_type='click' if action=='CLICK' else 'long_press',x=x,y=y))
        elif action=='TYPE':
            if 'point' in fields:
                x,y=point('point'); self.execute(JSONAction(action_type='click',x=x,y=y)); time.sleep(.5)
            subprocess.run([self.adb,'-s','emulator-5554','shell','app_process','-Djava.class.path=/data/local/tmp/yadb','/data/local/tmp','com.ysbing.yadb.Main','-keyboard',shlex.quote(fields.get('value',''))],check=True,capture_output=True,timeout=60)
        elif action=='SLIDE':
            x1,y1=point('point1'); x2,y2=point('point2')
            # Preserve the requested endpoints, including top-edge system gestures.
            adb_utils.check_ok(adb_utils.issue_generic_request(['shell','input','swipe',str(x1),str(y1),str(x2),str(y2),'400'],self.env.controller))
        else: raise ValueError('Unsupported action '+action)
        return AgentInteractionResult(False,record)
