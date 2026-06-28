# Automated Backup and Recovery Management System

## Overview

The Automated Backup and Recovery Management System is a Python-based application that automates file and folder backup operations, manages backup versions and provides recovery functionality for stored data.The system is designed to help users protect important files and directories from accidental deletion, system crashes, or other data-loss incidents by providing an easy-to-use backup and restoration solution.

---

## Features

### Backup Management

* Create manual backups of files and folders
* Backup complete directories
* Maintain multiple backup versions
* Store backup metadata
* Compress backups into ZIP archives

### Backup Monitoring

* Track backup status (Success/Failed)
* Record backup timestamps
* Generate backup logs
* Display backup history
* Monitor storage utilization

### Recovery Management

* Restore files from previous backups
* Preview available backups
* Verify backup integrity before restoration

### Reporting

* Backup summary reports
* Storage utilization reports
* Recovery activity logs
* Backup success/failure statistics

---

## Technologies Used

* Python
* Streamlit
* SQLite
* APScheduler
* Pandas
* Matplotlib
* shutil
* zipfile
* hashlib
* logging
* datetime

---

## Project Structure

```text
Backup and Recovery Management System/
│
├── app.py
├── backup_manager.py
├── recovery_manager.py
├── scheduler_manager.py
├── database.py
├── logger_manager.py
├── requirements.txt
├── README.md
│
├── backups/
├── Restored data
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/Automated-Backup-and-Recovery-Management-System.git
cd Automated-Backup-and-Recovery-Management-System
```

### Create a virtual environment (Optional)

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

The application will open in your browser automatically.

---

## How It Works

1. Select files or folders to back up.
2. The system creates a compressed backup archive.
3. Backup metadata is stored in the SQLite database.
4. Backup history and logs are generated automatically.
5. Users can restore any backup version whenever required.

---

## Future Enhancements
Cloud backup support
Backup encryption
Email notifications
User authentication


Author
Muhammad Uzair Younas
---
