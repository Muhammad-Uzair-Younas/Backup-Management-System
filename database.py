import sqlite3

db_name = "backup.db"
def get_connection():
    return sqlite3.connect(db_name, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    # Backup Information
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS backups(
        backup_id INTEGER PRIMARY KEY AUTOINCREMENT,
        backup_date TEXT,
        backup_source TEXT,
        backup_destination TEXT,
        backup_size REAL,
        backup_status TEXT,
        hash_value TEXT
    )
    """)
    # Recovery Information
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recoveries(
        recovery_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recovery_date TEXT,
        restored_files TEXT,
        recovery_status TEXT,
        recovery_logs TEXT
    )
    """)

    # Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_logs(
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_time TEXT,
        event_type TEXT,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()


# ------ insering backupps---------
def insert_backup(backup_date,backup_source,backup_destination,backup_size, backup_status,hash_value):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO backups(backup_date,backup_source,backup_destination,backup_size,backup_status,hash_value)VALUES (?, ?, ?, ?, ?, ?)""", (
        backup_date,
        backup_source,
        backup_destination,
        backup_size,
        backup_status,
        hash_value
    ))
    
    conn.commit()
    conn.close()

# -----Retrieve all backups info----
def get_all_backups():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM backups
    ORDER BY backup_id DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data

# -----Insert Recovery details-----
def insert_recovery(recovery_date,restored_files,recovery_status,recovery_logs):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO recoveries(recovery_date,restored_files,recovery_status,recovery_logs)
    VALUES (?, ?, ?, ?)""", (recovery_date, restored_files,recovery_status,recovery_logs))
    conn.commit()
    conn.close()

# retrive all recovery details
def get_all_recoveries():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM recoveries 
    ORDER BY recovery_id DESC""")

    data = cursor.fetchall()
    conn.close()
    return data

# Insert Log info 
def insert_log(event_time,event_type,description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO system_logs(event_time,event_type,description)
    VALUES (?, ?, ?)
    """, (event_time,event_type,description))
    conn.commit()
    conn.close()

# Fetch all logs
def get_all_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM system_logs
    ORDER BY log_id DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data

create_tables()
