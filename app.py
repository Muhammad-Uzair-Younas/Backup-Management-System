import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backup_manager import create_backup
from recovery_manager import restore_backup,verify_backup
from database import get_all_backups,get_all_recoveries,get_all_logs
from scheduler_manager import schedule_backup, stop_scheduler
import logger_manager

#----- PAGE CONFIG----------
st.set_page_config(page_title="Backup Management System",page_icon="logo.png",layout="wide")
st.logo("logo.png",size="large")
right, center, left = st.columns(3)
with center:
    st.image('logo.png',width=120)
st.title("Backup Management System")

# SIDEBAR
menu = st.sidebar.selectbox("Navigation",["Dashboard","Create Backup","Backup History","Restore Backup","Recovery History","System Logs","Scheduled Backup"])

# -----------DASHBOARD-------------
if menu == "Dashboard":
    st.header("Dashboard")

    backups = get_all_backups()
    recoveries = get_all_recoveries()
    total_backups = len(backups)
    successful_backups = len([b for b in backups if b[5] == "Success"])
    failed_backups = len([b for b in backups if b[5] == "Failed"])
    total_recoveries = len(recoveries)
    total_storage = 0
    for backup in backups:
        try:
            total_storage += float(backup[4])
        except:
            pass
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Backups",total_backups)
    col2.metric("Successful",successful_backups)
    col3.metric("Failed",failed_backups)
    col4.metric("Recoveries",total_recoveries)
    col5.metric("Storage Used (MB)",round(total_storage, 2))
    st.divider()

    if backups:
        df = pd.DataFrame(backups,columns=["Backup ID","Backup Date","Source","Destination","Size(MB)","Status","Hash"])
        col1, col2 = st.columns(2)
        
        #-------------- Pie Chart-----------
        with col1:
            st.subheader("Backup Status Distribution")
            status_counts = (df["Status"].value_counts())
            fig1, ax1 = plt.subplots(figsize=(5, 5))
            ax1.pie(status_counts,labels=status_counts.index,autopct="%1.1f%%")
            ax1.set_title("Backup Status")
            st.pyplot(fig1)

        # -----------Size Chart-----------
        with col2:
            st.subheader("Backup Size Analysis")
            fig2, ax2 = plt.subplots(figsize=(7, 6))
            ax2.bar(df["Backup ID"].astype(str),df["Size(MB)"])
            ax2.set_xlabel("Backup ID")
            ax2.set_ylabel("Size (MB)")
            ax2.set_title("Backup Sizes")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
    else:
        st.info("No backup records found.")


# -------CREATE BACKUP-----------
elif menu == "Create Backup":
    st.header("Create Backup")
    source_path = st.text_input("Enter File or Folder Path")
    if st.button("Create Backup"):
        if source_path:
            success, message = create_backup(source_path)
            if success:
                st.success(f"Backup Created Successfully\n\n{message}")
            else:
                st.error(message)


# --------- BACKUP HISTORY -----------
elif menu == "Backup History":
    st.header("Backup History")
    backups = get_all_backups()
    if backups:
        df = pd.DataFrame(backups)
        st.dataframe(df,use_container_width=True)
    else:
        st.info("No backup records available.")

# ------------RESTORE BACKUP
elif menu == "Restore Backup":
    st.header("Restore Backup")
    backups = get_all_backups()
    if backups:
        backup_ids = [row[0] for row in backups]
        selected_id = st.selectbox("Select Backup ID",backup_ids)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Verify Integrity"):
                if verify_backup(selected_id):
                    st.success("Backup Integrity Verified")
                else:
                    st.error("Integrity Check Failed")
        with col2:
            if st.button("Restore Backup"):
                success, message = restore_backup(selected_id)
                if success:
                    st.success(f"Restored Successfully\n\n{message}")
                else:
                    st.error(message)
    else:
        st.info("No backups available.")

# -----------RECOVERY HISTORY--------------
elif menu == "Recovery History":
    st.header("Recovery History")
    recoveries = get_all_recoveries()
    if recoveries:
        df = pd.DataFrame(recoveries)
        st.dataframe(df,use_container_width=True)
    else:
        st.info("No recovery records available.")

# -------SYSTEM LOGS------------
elif menu == "System Logs":
    st.header("System Logs")
    logs = get_all_logs()
    if logs:
        df = pd.DataFrame(logs,columns=["log_id", "event_time", "event_type", "description"])
        selected_type = st.selectbox("Filter Logs",[ "All","Backup Event", "Recovery Event","Error Log","User Action"])
        if selected_type != "All":
            df = df[df["event_type"] == selected_type]
        st.dataframe(df,use_container_width=True)
    else:
        st.info("No logs available.")

# ---------SCHEDULED BACKUP------------

elif menu == "Scheduled Backup":
    st.header("Scheduled Backup")
    backup_path = st.text_input("Enter File/Folder Path")
    hours = st.number_input("Backup Interval (Hours)",min_value=1,value=24)
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Start Scheduled Backup"):
            if backup_path:
                schedule_backup(backup_path,hours)
                st.success(f"Backup scheduled every {hours} hour(s).")

            else:
                st.warning("Please enter a valid path.")
    with col2:
        if st.button("Stop Scheduled Backup"):
            stop_scheduler()
            st.success("Scheduled backups stopped successfully...")
    
