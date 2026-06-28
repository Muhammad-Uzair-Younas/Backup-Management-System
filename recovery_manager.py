import os
import zipfile
import hashlib
from datetime import datetime
from database import (insert_recovery, get_connection )
from logger_manager import (log_recovery_event,log_error,log_user_action)

restoreFolder = "restored data"

os.makedirs(restoreFolder,exist_ok=True)


def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(
                lambda: f.read(4096),
                b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def verify_backup(backup_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT backup_destination,hash_value
    FROM backups
    WHERE backup_id=?
    """, (backup_id,))

    row = cursor.fetchone()
    conn.close()
    if not row:
        return False
    backup_file = row[0]
    stored_hash = row[1]
    if not os.path.exists(backup_file):
        return False
    current_hash = calculate_hash(backup_file)
    return current_hash == stored_hash


def restore_backup(backup_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT backup_destination
        FROM backups
        WHERE backup_id=?
        """, (backup_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise Exception("Backup record not found")
        backup_file = row[0]
        if not verify_backup(backup_id):
            raise Exception("Backup integrity verification failed")
        restore_folder = os.path.join(restoreFolder,f"restore_{backup_id}")

        os.makedirs(restore_folder,exist_ok=True)
        with zipfile.ZipFile(backup_file,"r") as zipf:
            zipf.extractall(restore_folder)
        insert_recovery(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),os.path.basename(backup_file),"Success",f"Restored to {restore_folder}")
        log_recovery_event(f"Backup restored: {backup_file}")
        log_user_action(f"User restored backup ID {backup_id}")

        return True, restore_folder
    except Exception as e:
        insert_recovery(
            recovery_date=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            restored_files="N/A",
            recovery_status="Failed",
            recovery_logs=str(e)
        )
        log_error(str(e))
        return False, str(e)