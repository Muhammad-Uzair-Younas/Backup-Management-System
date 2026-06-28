import os
import zipfile
import hashlib
from datetime import datetime
from database import insert_backup
from logger_manager import (log_backup_event,log_error,log_user_action)

backup_folder = "backups"
os.makedirs(backup_folder, exist_ok=True)

def calculate_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sha256.update(chunk)

    return sha256.hexdigest()

def get_file_size_mb(file_path):

    return round(os.path.getsize(file_path) / (1024 * 1024),2)


def create_backup(source_path):
    try:

        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source not found: {source_path}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        source_name = os.path.basename(source_path.rstrip("\\/"))

        backup_name = (f"{source_name}_{timestamp}.zip")

        backup_path = os.path.join(backup_folder,backup_name)
        with zipfile.ZipFile(backup_path,"w",zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isfile(source_path):
                zipf.write(source_path,os.path.basename(source_path))
            else:
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        full_path = os.path.join(root,file)
                        arcname = os.path.relpath(full_path,source_path)
                        zipf.write(full_path,arcname)

        backup_size = get_file_size_mb(backup_path)

        hash_value = calculate_hash(backup_path)
        insert_backup(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),source_path,backup_path,backup_size=backup_size,backup_status="Success",hash_value=hash_value)
        
        log_backup_event(f"Backup created successfully: {backup_name}")

        log_user_action(f"User created backup for {source_path}")

        return True, backup_name

    except Exception as e:
        log_error(str(e))
        return False, str(e)
