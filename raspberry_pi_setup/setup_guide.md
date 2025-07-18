Mueez Ur Rehman – Raspberry Pi Task Log & Run Instructions

==============================
1. System Monitoring (CPU, RAM, Disk logging)
   - Script: system_monitor.py
   - Location: /home/pi/system_monitor.py
   - Log File: /home/pi/logs/system_status.log
   - Runs every 10 minutes using cron

2. Daily Backup Script
   - Script: backup.sh
   - Location: /home/pi/backup.sh
   - Backup Folder: /home/pi/backups/
   - Runs daily at 11 PM using cron

==============================
Setup Steps
==============================

🔹 To run system monitor script manually:
$ python3 /home/pi/system_monitor.py

🔹 To test backup script manually:
$ bash /home/pi/backup.sh

🔹 To schedule system monitor every 10 minutes (edit cron):
$ crontab -e
Add this line:
*/10 * * * * /usr/bin/python3 /home/pi/system_monitor.py

🔹 To schedule backup script daily at 11 PM:
$ crontab -e
Add this line:
0 23 * * * /home/pi/backup.sh

🔹 To make backup.sh executable:
$ chmod +x /home/pi/backup.sh