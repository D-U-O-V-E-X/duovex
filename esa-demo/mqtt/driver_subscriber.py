import os
import paho.mqtt.client as mqtt

HOST = os.getenv("MQTT_HOST", "127.0.0.1")
TOPIC = "duovex/demo/ambulance/alert"

def connected(client, userdata, flags, reason_code, properties):
    if reason_code != 0:
        raise RuntimeError(f"MQTT connection failed: {reason_code}")
    client.subscribe(TOPIC, qos=1)
    print("Subscribed:", TOPIC, flush=True)

def received(client, userdata, message):
    print("Received:", message.payload.decode("utf-8"), flush=True)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = connected
client.on_message = received
client.connect(HOST, 1883, 30)
client.loop_forever()
