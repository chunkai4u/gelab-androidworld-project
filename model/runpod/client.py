"""Private GELab calls over Runpod's SSH gateway; no public model port."""
import argparse, base64, json, os, pathlib, shlex, subprocess, uuid
ROOT=pathlib.Path(__file__).resolve().parents[2]
KEY=pathlib.Path(os.environ.get('GELAB_SSH_KEY',str(ROOT/'work/runpod/gelab_ed25519')))
HOST=os.environ.get('GELAB_SSH_HOST','YOUR_RUNPOD_SSH_USER@ssh.runpod.io')
def remote_python(code):
    encoded=base64.b64encode(code.encode()).decode()
    target='/tmp/gelab-'+uuid.uuid4().hex+'.b64'
    lines=['stty -echo',': > '+target]
    lines += ["printf '%s' "+shlex.quote(encoded[i:i+800])+' >> '+target for i in range(0,len(encoded),800)]
    runner="import base64,pathlib; p=pathlib.Path("+repr(target)+"); s=base64.b64decode(p.read_bytes()); p.unlink(); exec(s)"
    lines += ['python -c '+shlex.quote(runner),'exit']
    result=subprocess.run(['ssh','-tt','-o','BatchMode=yes','-o','ConnectTimeout=20','-o','UserKnownHostsFile='+str(ROOT/'work/runpod/known_hosts'),'-i',str(KEY),HOST],input='\n'.join(lines)+'\n',text=True,capture_output=True,timeout=240)
    for line in result.stdout.splitlines():
        if line.startswith('GELAB_RESULT:'):
            return json.loads(line[len('GELAB_RESULT:'):])
    raise RuntimeError('SSH/model call failed: '+result.stderr[-1000:]+'\n'+result.stdout[-2000:])
def health():
    return remote_python("import json,urllib.request; r=json.load(urllib.request.urlopen('http://127.0.0.1:11435/health')); print('GELAB_RESULT:'+json.dumps(r))")
def step(image_path, task, history=''):
    payload={'task':task,'history':history,'image_base64':base64.b64encode(pathlib.Path(image_path).read_bytes()).decode()}
    data=base64.b64encode(json.dumps(payload).encode()).decode()
    return remote_python("import base64,json,urllib.request; req=urllib.request.Request('http://127.0.0.1:11435/step',data=base64.b64decode("+repr(data)+"),headers={'Content-Type':'application/json'}); r=json.load(urllib.request.urlopen(req,timeout=180)); print('GELAB_RESULT:'+json.dumps(r))")
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--image'); p.add_argument('--task',default='Turn Wi-Fi on.'); a=p.parse_args()
    print(json.dumps(step(a.image,a.task) if a.image else health(),ensure_ascii=False,indent=2))
