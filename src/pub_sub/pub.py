import paho.mqtt.client as mqtt_client
sys.path.append("../models")
from models import Publisher
import sys

'''
скрипт вызывается командой вида^

python3 pub.py {station} {arg1 arg2 arg3}

т.е.

python3 pub.py station1 1 2 3 4 5 6



'''
station = sys.argv[1] #Тогда здесь будет station1
data = sys.argv[2:] #А здесь будет список ['1', '2', '3', '4', '5', '6']

'''
Предполагается, что в data будут передаваться пропарсенные данные, 
которые нужно опубликовать
'''
pub = Publisher(station,"localhost","station/data")
pub.connect()
pub.loop_start()
for i in data:
    pub.publish(f"{pub.station}@%@%!{i}")
pub.disconnect()
pub.loop_stop()
