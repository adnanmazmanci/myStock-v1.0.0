import os
from datetime import datetime

def append_with_timestamp(content, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n--- {timestamp} ---\n{content}\n"
    with open(file_path, "a") as f:
        f.write(entry)
    return file_path
