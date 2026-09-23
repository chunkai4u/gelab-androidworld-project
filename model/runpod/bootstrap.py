"""Restore the model service after restarting the temporary Pod."""
import pathlib, json
from client import remote_python
root=pathlib.Path(__file__).parent
files={name:(root/name).read_text() for name in ['server.py','prompt.txt','setup.sh','smoke_test.py']}
code='import pathlib,subprocess,json\np=pathlib.Path("/workspace/gelab"); p.mkdir(parents=True,exist_ok=True)\n'
code+='files='+repr(files)+'\n'
code+='for n,s in files.items(): (p/n).write_text(s)\n'
code+='log=open(p/"setup.log","a"); job=subprocess.Popen(["bash",str(p/"setup.sh")],stdout=log,stderr=log,start_new_session=True)\n'
code+='print("GELAB_RESULT:"+json.dumps({"setup_started":True,"pid":job.pid,"log":"/workspace/gelab/setup.log"}))\n'
print(json.dumps(remote_python(code),indent=2))
