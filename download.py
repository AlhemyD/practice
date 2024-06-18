from fastapi import FastAPI
import requests
import schedule
import datetime
from datetime import datetime, timedelta
import time
from datetime import datetime

def start_download():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_2 = yesterday.strftime("%Y-%m-%d")
    link = f"http://127.0.0.1:8001/download/{yesterday_2}"
    response = requests.get(link, stream=True)
    print(yesterday)
    total_length = response.headers.get('content-length')
    if total_length is None:
        print("No content")
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            done = int(50 * dl / total_length)
            print(f"[{'=' * done}{' ' * (50 - done)}]")

schedule.every().day.at("21:43").do(start_download)

while True:
    schedule.run_pending()
