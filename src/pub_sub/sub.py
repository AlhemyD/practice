import paho.mqtt.client as mqtt_client
import time, sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log'))
from logger import get_logger
logger=get_logger("sub")
broker="192.168.0.103"

date="1997-01-01"
def on_message(client, userdata, message):
    station, data = str(message.payload.decode("utf-8")).split("@%@%!")
    global date
    dt=data.split(" ")[0]
    if dt != date:
        date=dt
        print(f"\n------------------\n\nDate has changed to: {date}\n\n------------------\n")
    print(f"{station} received message = {data}")

client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION2,
            "yuji"
        )
client.on_message=on_message
client.connect(broker)
client.loop_start()
client.subscribe("station/data")
logger.info("Started subscription on station/data")
print("\nstarting subscribtion on station/data")
while True:
    try:
        time.sleep(1800)
    except KeyboardInterrupt:
        logger.warning("Ending subscription on station/data")
        print("\nending subscribing")
        break

client.disconnect()
client.loop_stop()

