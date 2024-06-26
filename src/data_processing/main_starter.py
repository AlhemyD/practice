import os,sys, subprocess
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log'))
from apscheduler.schedulers.blocking import BlockingScheduler
from logger import get_logger
from datetime import datetime, timedelta

logger=get_logger("main_starter")

def start_main():
    main_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'main.py')
    subprocess.run(f"python3 {main_path}", shell=True, check=True)

logger.info("Data loading will start at 22:00")
#start_main()
scheduler = BlockingScheduler()
scheduler.add_job(start_main, 'cron',hour=22, minute=0)
scheduler.start()
