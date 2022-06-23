from datetime import datetime
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler


def task():
    print("timeNow is : %s" % datetime.now())
    os.system('python main.py')


if __name__ == "__main__":
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(task, 'cron', day_of_week='mon-fri', hour=11, minute=30)
    scheduler.start()
    print("Press Ctrl + F2 to exit")
    try:
        while True:
            time.sleep(3600)
            print(f"{datetime.now()}")
            print('wait...')
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Exit The Job !")
