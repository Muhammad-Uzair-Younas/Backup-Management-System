from datetime import datetime
from database import insert_log

def log_backup_event(message):
    insert_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Backup Event",message)


def log_recovery_event(message):
    insert_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Recovery Event",message)


def log_error(message):
    insert_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Error Log",message)


def log_user_action(message):
    insert_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"User Action",message)
