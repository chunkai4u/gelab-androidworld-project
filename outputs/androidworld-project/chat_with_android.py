"""Small natural-language terminal front end for verified AndroidWorld tasks."""
import pathlib
import re
import subprocess
import sys

PROJECT = pathlib.Path(__file__).resolve().parent
VERSION = "2.1"
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
    # Only the exact generic phrasing requests a generated, verifier-scored task.
    # Any added detail must be preserved as the user's live request.
    return lowered not in generic

def chinese_number(value: str) -> int:
    digits={"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
    if value == "十": return 10
    if "十" in value:
        left, right = value.split("十", 1)
        return (digits.get(left, 1) if left else 1) * 10 + (digits.get(right, 0) if right else 0)
    return digits[value]

def freeform_goal(text: str) -> str:
    lowered = text.lower()
    person = re.search(r"(?:with|跟)\s*([a-z]+)", lowered)
    month_day = re.search(r"(\d{1,2})\s*月\s*(\d{1,2})\s*(?:號|日)?", text)
    chinese_month_day = re.search(r"([一二三四五六七八九十]+)月([一二三四五六七八九十]+)(?:號|日)?", text)
    english_month_day = re.search(r"\b([a-z]+)\s+(\d{1,2})\b", lowered)
    hour = re.search(r"\b(\d{1,2})\s*(?:pm|p\.m\.)\b", lowered)
    if hour is None:
        hour = re.search(r"(?:下午|晚上)\s*(\d{1,2})\s*(?:點|时|時)?", text)
    chinese_hour = re.search(r"(?:下午|晚上)\s*([一二三四五六七八九十]+)\s*(?:點|时|時)", text)
    duration_match = re.search(r"\b(\d+)\s*(?:minutes?|mins?)\b", lowered)
    duration = int(duration_match.group(1)) if duration_match else (60 if any(phrase in lowered for phrase in ("one hour", "an hour", "1 hour")) or "一個小時" in text or "一个小时" in text else 30 if "半小時" in text or "半小时" in text else None)
    details=[]
    if month_day:
        details.append(f"Date: {month_day.group(1)}/{month_day.group(2)} in the emulator's current year")
    elif chinese_month_day:
        details.append(f"Date: {chinese_number(chinese_month_day.group(1))}/{chinese_number(chinese_month_day.group(2))} in the emulator's current year")
    elif english_month_day:
        details.append(f"Date: {english_month_day.group(1).title()} {english_month_day.group(2)} in the emulator's current year")
    elif "today" in lowered or "今天" in text:
        details.append("Date: today, as displayed in the app")
    if hour or chinese_hour:
        raw_hour = int(hour.group(1)) if hour else chinese_number(chinese_hour.group(1))
        start_hour = raw_hour + 12 if raw_hour < 12 else raw_hour
        details.append(f"Start time: {start_hour:02d}:00 (24-hour clock)")
        if duration:
            end_minutes = start_hour * 60 + duration
            suffix = " on the next day" if end_minutes >= 24 * 60 else " on the same date"
            details.append(f"End time: {(end_minutes // 60) % 24:02d}:{end_minutes % 60:02d} (24-hour clock){suffix}")
    elif duration:
        details.append(f"Duration: {duration} minutes")
    if person:
        details.append(f"Title: Date with {person.group(1).title()}")
    return (
        "Open Simple Calendar Pro and create exactly one event. Set the upper date/time rows "
        "as the start and the lower date/time rows as the end. Use the exact 24-hour values "
        "below, do not use All-day, then save with the checkmark. "
        "Do not substitute event details. " + ". ".join(details) + ". "
        "Original user request: " + text
    )

def main():
    print(f"GELab-Zero Android assistant v{VERSION}")
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
        command=[sys.executable,str(PROJECT / "run_task.py"),"--runs","1","--max-steps",str(40 if specific else steps),"--label","terminal-chat","--user-command",text]
        command += ["--freeform-goal",freeform_goal(text)] if specific else ["--task",task]
        result = subprocess.run(command)
        print("\nVerification complete." if result.returncode == 0 else "\nRun stopped; inspect the terminal output above.")

if __name__ == "__main__":
    main()
