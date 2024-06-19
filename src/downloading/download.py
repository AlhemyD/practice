import requests
import sys
from datetime import datetime, timedelta
import schedule
import time

def download_file_from_url():
    today = datetime.now()
    date = (today - timedelta(days=200)).strftime('%Y-%m-%d')
    #link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    #link = "https://bki.matecdn.ru/-/10e7e137-4fc3-45d1-a37e-bdd4a390e537/darw00aus-r-20240010000-01d-30s-mocrx.gz"
    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"{date}.zip"

    with open(file_name, "wb") as f:
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()

schedule.every().day.at("20:39").do(download_file_from_url)

while True:
    schedule.run_pending()
