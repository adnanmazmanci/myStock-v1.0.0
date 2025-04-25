import os
from datetime import datetime

def log_message(message, log_file="logs/logs.txt"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"

    with open(log_file, "a") as f:
        f.write(entry)

    return entry  # for Telegram status updates
