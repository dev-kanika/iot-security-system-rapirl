import csv
from datetime import datetime
import os

LOG_FILE = os.path.join("logs.csv")

def log_event(event_type, label):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, event_type, label])