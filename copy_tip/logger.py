from datetime import datetime
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "keystrokes.log")

os.makedirs(LOG_DIR, exist_ok=True)

def log_event(event_type, value):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {event_type}: {value}\n")
