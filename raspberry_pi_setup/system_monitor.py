import psutil
from datetime import datetime
import os

log_dir = "/home/pi/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "system_status.log")

with open(log_file, "a") as f:
    f.write(f"\n--- {datetime.now()} ---\n")
    f.write(f"CPU Usage: {psutil.cpu_percent()}%\n")
    f.write(f"RAM Usage: {psutil.virtual_memory().percent}%\n")
    f.write(f"Disk Usage: {psutil.disk_usage('/').percent}%\n")