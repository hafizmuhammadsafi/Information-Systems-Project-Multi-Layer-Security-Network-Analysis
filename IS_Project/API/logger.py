# logger.py
from datetime import datetime

LOG_FILE = "security.log"


def log_event(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

