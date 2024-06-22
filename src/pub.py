import paho.mqtt.client as mqtt_client
import time
from models import Publisher
import threading

L=1000
pubs=[]
for i in range(L):
    pubs.append(Publisher("station"+str(i),"localhost","station/data"))
def publ(pub):

    pub.connect()
    pub.loop_start()
    for i in range (5):
        pub.publish(f"{pub.station}@%@%!data - {i}")
        
    pub.disconnect()
    pub.loop_stop()

threads=[]
for i in range(L):
    threads.append(threading.Thread(target=publ, args=(pubs[i],)))
for i in range(L):
    threads[i].start()
for i in range(L):
    threads[i].join()
pubs[0].connect()
pubs[0].loop_start()
pubs[0].publish(f"{pubs[0].station}@%@%!All data was sent")
pubs[0].disconnect()
pubs[0].loop_stop()


