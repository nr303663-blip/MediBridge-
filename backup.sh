#!/usr/bin/env bash
# MediBridge — local data backup (Phase 6: Deployment - Data Backup)
# Usage: ./backup.sh
set -e
cd "$(dirname "$0")"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups"
mkdir -p "$BACKUP_DIR"

echo "Backing up database data to ${BACKUP_DIR}/db_backup_${TIMESTAMP}.json ..."
python manage.py dumpdata \
    --natural-foreign --natural-primary \
    --exclude auth.permission --exclude contenttypes \
    > "${BACKUP_DIR}/db_backup_${TIMESTAMP}.json"

echo "Backing up media files..."
if [ -d "media" ]; then
    tar -czf "${BACKUP_DIR}/media_backup_${TIMESTAMP}.tar.gz" media/
fi

echo "Done. Backup files are in ${BACKUP_DIR}/"
echo "To restore data: python manage.py loaddata ${BACKUP_DIR}/db_backup_${TIMESTAMP}.json"
