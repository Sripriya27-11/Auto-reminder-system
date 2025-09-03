import json, time, threading
from datetime import datetime
from plyer import notification

FILE = "reminders.json"
FMT = "%Y-%m-%d %I:%M:%S %p"   # 12-hour format with AM/PM

def load():
    try:
        with open(FILE, "r") as f: return json.load(f)
    except: return []

def save(rem):
    with open(FILE, "w") as f:
        json.dump(rem, f, indent=4)

def add(rem):
    try:
        cat = input("Category: ").title() or "General"
        msg = input("Message: ")
        dt = datetime.strptime(input("Time (YYYY-MM-DD HH:MM:SS AM/PM): "), FMT)
        rem.append({
            "category": cat,
            "message": msg,
            "time": dt.strftime(FMT),
            "notified": False
        })
        save(rem)
        print("✅ Added!\n")
    except:
        print("❌ Wrong format! Example: 2025-09-03 02:30:00 PM")

def view(rem):
    if not rem: 
        print("📭 No reminders"); return
    for r in rem:
        status = "✅ Done" if r["notified"] else "⏳ Pending"
        print(f"[{r['category']}] {r['message']} at {r['time']} - {status}")

def check(rem):
    while True:
        now = datetime.now().replace(microsecond=0)
        changed = False
        for r in rem:
            rt = datetime.strptime(r["time"], FMT)
            if rt <= now and not r["notified"]:
                notification.notify(
                    title=f"{r['category']} Reminder",
                    message=r["message"],
                    timeout=10
                )
                r["notified"] = True
                changed = True
        if changed:   # save only when something changed
            save(rem)
        time.sleep(1)

def menu(rem):
    while True:
        c = input("\n1.Add  2.View  3.Exit: ")
        if c == "1": add(rem)
        elif c == "2": view(rem)
        elif c == "3": exit()
        else: print("❌ Invalid!")

if __name__ == "__main__":
    reminders = load()
    threading.Thread(target=check, args=(reminders,), daemon=True).start()
    menu(reminders)

