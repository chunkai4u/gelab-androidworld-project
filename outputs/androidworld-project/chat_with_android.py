"""Small natural-language terminal front end for verified AndroidWorld tasks."""
import pathlib
import subprocess
import sys

PROJECT = pathlib.Path(__file__).resolve().parent
COMMANDS = (
    ("SystemWifiTurnOn", 15, ("wifi", "wi-fi", "無線網路", "開啟網路", "打开网络"), "Turn Wi-Fi on"),
    ("SimpleCalendarAddOneEvent", 30, ("calendar", "event", "行事曆", "行事历", "活動", "活动"), "Create a calendar event"),
)

def understand(text: str):
    lowered = text.lower()
    for task, steps, keywords, label in COMMANDS:
        if any(keyword in lowered for keyword in keywords):
            return task, steps, label
    return None

def is_specific_request(text: str) -> bool:
    lowered = text.lower().strip().rstrip('.。!！')
    generic = {"create a calendar event", "calendar event", "建立行事曆活動", "建立一个行事历活动"}
    return lowered not in generic and any(word in lowered for word in ("today", "tomorrow", "下午", "上午", "幾點", "几点", "at ", " on ", "約會", "约会"))

def main():
    print("GELab-Zero Android assistant")
    print("Try: 'Turn Wi-Fi on' or 'Create a calendar event'. Type 'quit' to leave.")
    while True:
        try:
            text = input("\nYou > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye."); return
        if text.lower() in {"quit", "exit", "離開", "退出"}:
            print("Goodbye."); return
        match = understand(text)
        if match is None:
            print("I currently support Wi-Fi and calendar-event requests only."); continue
        task, steps, label = match
        specific = task == "SimpleCalendarAddOneEvent" and is_specific_request(text)
        if specific:
            print(f"Understood: {label}. Running your exact request as a live free-form demo.")
            print("The run will be recorded, but it has no official PASS/FAIL because the request is not an AndroidWorld generated task.")
        else:
            print(f"Understood: {label}. Preparing AndroidWorld task {task}.")
            print("AndroidWorld generates the exact task details so the official verifier can score it.")
        subprocess.run([str(PROJECT / "start-emulator.command")], check=True)
        subprocess.run([sys.executable, str(PROJECT / "wait_ready.py")], check=True)
        command=[sys.executable,str(PROJECT / "run_task.py"),"--runs","1","--max-steps",str(steps),"--label","terminal-chat","--user-command",text]
        command += ["--freeform-goal",text] if specific else ["--task",task]
        result = subprocess.run(command)
        print("\nVerification complete." if result.returncode == 0 else "\nRun stopped; inspect the terminal output above.")

if __name__ == "__main__":
    main()
