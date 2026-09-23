import argparse, dataclasses, datetime, json, os, pathlib, random, time, traceback
import numpy as np
from absl import flags, logging
from PIL import Image
from recorder import Recorder

TASKS=['SystemWifiTurnOn','SimpleCalendarAddOneEvent','MarkorCreateNote','MarkorCreateNoteAndSms']
def _json_value(value):
    """Preserve generated AndroidWorld task metadata without breaking runs."""
    if dataclasses.is_dataclass(value): return dataclasses.asdict(value)
    if isinstance(value, (datetime.date, datetime.datetime)): return value.isoformat()
    return str(value)
def _write_result(path, info):
    path.write_text(json.dumps(info,ensure_ascii=False,indent=2,default=_json_value))
def main():
    p=argparse.ArgumentParser(); p.add_argument('--task',choices=TASKS,default=TASKS[0]); p.add_argument('--runs',type=int,default=1); p.add_argument('--max-steps',type=int,default=20); p.add_argument('--seed',type=int,default=42); p.add_argument('--label',default='development'); p.add_argument('--user-command',default=None); p.add_argument('--freeform-goal',default=None); args=p.parse_args()
    if not 1<=args.runs<=3 or not 1<=args.max_steps<=60: p.error('runs must be 1–3 and max-steps 1–60')
    flags.FLAGS(['runner']); logging.set_verbosity(logging.WARNING)
    from android_world import registry
    from environment import load_environment
    from gelab_agent import GelabAgent
    import client
    print('Checking cloud model...',flush=True); print(client.health(),flush=True)
    adb=os.environ['ANDROID_HOME']+'/platform-tools/adb'
    # Each official task initializes the benchmark clock itself.
    print('Connecting to Android...',flush=True)
    env=load_environment(freeze_datetime=False)
    from baseline import restore_if_missing
    restore_if_missing(env)
    catalog=registry.TaskRegistry().get_registry(registry.TaskRegistry.ANDROID_WORLD_FAMILY)
    root=pathlib.Path(__file__).parent/'runs'; root.mkdir(exist_ok=True)
    try:
        for run in range(1,args.runs+1):
            random.seed(args.seed+run-1); np.random.seed(args.seed+run-1)
            folder=root/(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+args.task+'-'+str(run)); folder.mkdir()
            task=None
            if args.freeform_goal:
                goal=args.freeform_goal
                print('Preparing a clean Android state for a free-form request.',flush=True)
                env.reset(go_home=True)
                info={'task':None,'run':run,'seed':args.seed+run-1,'label':args.label,'goal':goal,'params':None,'model':'GELab-Zero-4B-preview','observation':'screenshot','grounding':'normalized coordinates','step_budget':args.max_steps,'verifier':'NOT_APPLICABLE','failure_class':None,'configuration':'mac-intel-api33-host-gpu-4gb-4core-540x1200','mode':'freeform'}
            else:
                task=catalog[args.task](catalog[args.task].generate_random_params())
                print('Preparing a clean task state; this can take a few minutes on this Mac.',flush=True)
                env.reset(go_home=True); task.initialize_task(env)
                goal=task.goal
                info={'task':args.task,'run':run,'seed':args.seed+run-1,'label':args.label,'goal':goal,'params':task.params,'model':'GELab-Zero-4B-preview','observation':'screenshot','grounding':'normalized coordinates','step_budget':args.max_steps,'verifier':'NOT_RUN','failure_class':None,'configuration':'mac-intel-api33-host-gpu-4gb-4core-540x1200','mode':'verified_task'}
            if args.user_command: info['user_command']=args.user_command
            _write_result(folder/'result.json',info)
            print('TASK:',goal,'\nOUTPUT:',folder,flush=True)
            agent=GelabAgent(env,folder,args.max_steps); recording=Recorder(adb,folder).start(); start=time.time(); done=False
            try:
                for _ in range(args.max_steps):
                    result=agent.step(goal); print('STEP',agent.count,result.data['parsed_action'],result.data['fields'],flush=True)
                    if result.done: done=True; break
                time.sleep(1)
                Image.fromarray(env.get_state().pixels).save(folder/'final.png')
                if task is None:
                    info.update(agent_reported_done=done)
                    if not done: info['termination_reason']='step_budget'
                else:
                    score=float(task.is_successful(env)); info.update(verifier='PASS' if score==1 else 'FAIL',score=score,agent_reported_done=done)
                    if score!=1: info['failure_class']='false_done' if done else None
                    if not done: info['termination_reason']='step_budget'
            except (Exception, KeyboardInterrupt) as exc:
                info.update(error=str(exc) or type(exc).__name__,termination_reason='interrupted' if isinstance(exc,KeyboardInterrupt) else 'error')
                if 'Blocked' in str(exc): info['failure_class']='wrong_app'
                try:
                    if task is not None:
                        score=float(task.is_successful(env)); info.update(score=score,verifier='PASS' if score==1 else 'FAIL')
                except Exception as v: info['verifier_error']=str(v)
                traceback.print_exc()
            finally:
                try:
                    info['recording']=str(recording.stop())
                    if recording.error: info['recording_warning']=recording.error; info['recording_incomplete']=True
                except Exception as exc: info['recording_error']=str(exc)
                info.update(steps=agent.count,seconds=round(time.time()-start,2))
                _write_result(folder/'result.json',info)
                print('RESULT:',info['verifier'],flush=True)
                print('VIDEO:',info.get('recording','Not saved: '+info.get('recording_error','unknown error')),flush=True)
                if task is not None: task.tear_down(env)
    finally: env.close()
if __name__=='__main__': main()
