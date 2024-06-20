import paho.mqtt.client as mqtt_client
import time
broker="broker.emqx.io"
def on_message(client, userdata, message):
    time.sleep(1)
    data = str(message.payload.decode("utf-8"))
    print(f"received message = {data}")

client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION2,
            "yuji"
        )
client.on_message=on_message
client.connect(broker)
client.loop_start()
client.subscribe("station/data")
while True:
    try:
        time.sleep(1800)
    except KeyboardInterrupt:
        print("\nending subscribing")
        break

client.disconnect()
client.loop_stop()

