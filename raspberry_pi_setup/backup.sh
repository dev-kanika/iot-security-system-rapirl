#!/bin/bash
DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/home/pi/backups"
PROJECT_DIR="/home/pi/my_project"

mkdir -p $BACKUP_DIR
tar -czvf $BACKUP_DIR/project_backup_$DATE.tar.gz $PROJECT_DIR