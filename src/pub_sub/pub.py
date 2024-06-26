import sys, requests, json, os, glob
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../modules'))
from models import Publisher
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log'))

from logger import get_logger
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
logger = get_logger("pub")

'''
скрипт вызывается командой вида^

python3 pub.py {rnx_file_name}

т.е.

python3 pub.py darw00aus-r-20240010000-01d-30s-mo.rnx



''' 
date = (datetime.now() - timedelta(days=200)).strftime('%Y-%m-%d')
data_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),f'../../data/{date}')
if len(sys.argv[1])==4:
    pattern=sys.argv[1]+"*o"
else:
    pattern=sys.argv[1]+"*.rnx"

data_path=os.path.join(data_path,pattern)
rnx_file_name=os.path.basename(glob.glob(data_path)[0])
print(rnx_file_name)


def publ(pub, data):
    pub.publish(f"{pub.station}@%@%!{data}")


pub = Publisher(rnx_file_name,"192.168.0.103","station/data")
pub.connect()
pub.loop_start()
#for i in data:
#    pub.publish(f"{pub.station}@%@%!{i}")


link=f"http://localhost:8000/parsing/{date}/{rnx_file_name}"
response = requests.get(link, stream=True).json()
if "error" in response:
    logger.error(f"error during request for station {pub.station} - error - {response['error']}")
    print(response)
    pub.disconnect()
    pub.loop_stop()
elif "parse_data" in response:
    logger.info(f"Parsed data for station {pub.station} successfully. Starting scheduler")

    '''
    '{} {}: {} {}'.format(
                    tec.timestamp,
                    tec.satellite,
                    tec.phase_tec,
                    tec.p_range_tec,
                )

    "2024-01-01 00:00:00 G12: 7.8285638894945935 22.766467356433278",
    '''
    for data in response["parse_data"]:
        date=list(map(int, (datetime.now().strftime('%Y-%m-%d')).split("-")))
        time = list(map(int, str(data.split(" ")[1]).split(":")))
        dt=datetime(date[0],date[1],date[2], time[0],time[1],time[2])

        scheduler.add_job(publ, 'date', run_date=dt, args=[pub,data])
    scheduler.start()

    try:
        while True:
            pass
    except Exception as e:
        pub.disconnect()
        pub.loop_stop()
        scheduler.shutdown()
        logger.error(f"Cought an Exception for station {pub.station} - Exception - {e}")
    except KeyboardInterrupt:
        pub.disconnect()
        pub.loop_stop()
        scheduler.shutdown()
        logger.warning(f"Ended publishing on {pub.station} due to {KeyboardInterrupt}")

else:
    logger.error(f"Unknown error during request for station {pub.station}")
    print(response)
    pub.disconnect()
    pub.loop_stop()
