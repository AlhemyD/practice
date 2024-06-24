import paho.mqtt.client as mqtt_client
import time
broker="localhost"
def on_message(client, userdata, message):
    station, data = str(message.payload.decode("utf-8")).split("@%@%!")
    print(f"{station} received message = {data}")

client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION2,
            "yuji"
        )
client.on_message=on_message
client.connect(broker)
client.loop_start()
client.subscribe("station/data")
print("\nstarting subscribtion on station/data")
while True:
    try:
        time.sleep(1800)
    except KeyboardInterrupt:
        print("\nending subscribing")
        break

client.disconnect()
client.loop_stop()

