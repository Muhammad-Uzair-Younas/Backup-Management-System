from apscheduler.schedulers.background import BackgroundScheduler
from backup_manager import create_backup

scheduler = BackgroundScheduler()
def schedule_backup(path, hours=24):
    scheduler.add_job(create_backup,"interval",hours=hours,args=[path])
    if not scheduler.running:
        scheduler.start()
def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        return True