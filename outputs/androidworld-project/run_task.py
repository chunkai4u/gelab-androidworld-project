import argparse, dataclasses, datetime, json, os, pathlib, random, re, time, traceback
import numpy as np
from absl import flags, logging
from PIL import Image
from recorder import Recorder

TASKS=[
    'SystemWifiTurnOn',
    'SimpleCalendarAddOneEvent',
    'MarkorCreateNote',
    'MarkorCreateNoteAndSms',
    'ExpenseAddMultipleFromMarkor',
]
def _require_pro_expense(env):
    """Pro Expense first-run setup needs the UI tree, which this screenshot-only runner does not read."""
    from android_world.task_evals.utils import sqlite_utils
    if not sqlite_utils.table_exists('expense','/data/data/com.arduia.expense/databases/accounting.db',env):
        raise SystemExit('Pro Expense is not set up on this emulator. Run Install-Pro-Expense.command once, then start the task again.')
def _json_value(value):
    """Preserve generated AndroidWorld task metadata without breaking runs."""
    if dataclasses.is_dataclass(value): return dataclasses.asdict(value)
    if isinstance(value, (datetime.date, datetime.datetime)): return value.isoformat()
    return str(value)
def _write_result(path, info):
    path.write_text(json.dumps(info,ensure_ascii=False,indent=2,default=_json_value))
def _verify_freeform_calendar(goal, env):
    """Checks the Calendar database, so a model COMPLETE claim cannot be a false success."""
    from android_world.task_evals.single.calendar import calendar_utils
    from android_world.task_evals.utils import sqlite_schema_utils, sqlite_utils
    title=re.search(r"Title: ([^.]+)",goal); start=re.search(r"Start time: (\d{2}):(\d{2})",goal); end=re.search(r"End time: (\d{2}):(\d{2})",goal); date=re.search(r"Date: (\d{1,2})/(\d{1,2})",goal)
    rows=sqlite_utils.get_rows_from_remote_device(calendar_utils.EVENTS_TABLE,calendar_utils.DB_PATH,sqlite_schema_utils.CalendarEvent,env)
    expected={'title':title.group(1).strip() if title else None,'start':start.groups() if start else None,'end':end.groups() if end else None,'date':date.groups() if date else None}
    for row in rows:
        start_at=datetime.datetime.fromtimestamp(row.start_ts,datetime.timezone.utc); end_at=datetime.datetime.fromtimestamp(row.end_ts,datetime.timezone.utc)
        if expected['title'] and row.title != expected['title']: continue
        if expected['date'] and (start_at.month,start_at.day) != tuple(map(int,expected['date'])): continue
        if expected['start'] and (start_at.hour,start_at.minute) != tuple(map(int,expected['start'])): continue
        if expected['end'] and (end_at.hour,end_at.minute) != tuple(map(int,expected['end'])): continue
        return True, {'expected':expected,'matched_title':row.title,'matched_start':start_at.isoformat(),'matched_end':end_at.isoformat()}
    return False, {'expected':expected,'rows_checked':len(rows)}
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
    if args.task.startswith('Expense') and not args.freeform_goal: _require_pro_expense(env)
    catalog=registry.TaskRegistry().get_registry(registry.TaskRegistry.ANDROID_WORLD_FAMILY)
    root=pathlib.Path(__file__).parent/'runs'; root.mkdir(exist_ok=True)
    try:
        for run in range(1,args.runs+1):
            random.seed(args.seed+run-1); np.random.seed(args.seed+run-1)
            run_name='FreeformCalendar' if args.freeform_goal else args.task
            folder=root/(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+run_name+'-'+str(run)); folder.mkdir()
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
            if task is None:
                print('REQUEST:',args.user_command or goal,flush=True)
                print('MODE: free-form Calendar with database verification',flush=True)
            else:
                print('TASK:',goal,flush=True)
            print('OUTPUT:',folder,flush=True)
            agent=GelabAgent(env,folder,args.max_steps); recording=Recorder(adb,folder).start(); start=time.time(); done=False
            try:
                for _ in range(args.max_steps):
                    result=agent.step(goal); print('STEP',agent.count,result.data['parsed_action'],result.data['fields'],flush=True)
                    if result.done: done=True; break
                    if task is None:
                        verified,details=_verify_freeform_calendar(goal,env)
                        if verified:
                            done=True
                            info.update(completion_source='calendar_database',verification_details=details)
                            print('Calendar database matches the requested event; stopping agent.',flush=True)
                            break
                time.sleep(1)
                Image.fromarray(env.get_state().pixels).save(folder/'final.png')
                if task is None:
                    verified,details=_verify_freeform_calendar(goal,env)
                    info.update(agent_reported_done=done,verifier='CUSTOM_CALENDAR_PASS' if verified else 'CUSTOM_CALENDAR_FAIL',score=1.0 if verified else 0.0,verification_scope='freeform Calendar database',verification_details=details)
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
