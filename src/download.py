import requests
import schedule
from datetime import datetime, timedelta
import time
from datetime import datetime

def start_download():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_2 = yesterday.strftime("%Y-%m-%d")
    link = f"http://127.0.0.1:8001/download/{yesterday_2}"
    response = requests.get(link, stream=True)

schedule.every().day.at("21:43").do(start_download)
while True:
    schedule.run_pending()
