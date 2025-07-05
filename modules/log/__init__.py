from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

log_file = os.getenv("LOG_FILE")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)