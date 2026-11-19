import json
import os
import time
import paho.mqtt.client as mqtt

HOST = os.getenv("MQTT_HOST", "127.0.0.1")
TOPIC = "duovex/demo/ambulance/alert"
payload = {"vehicle_id": "AMB001", "event": "SIMULATED_AMBULANCE_APPROACHING",
           "advice": "SLOW_DOWN", "sent_at_unix_s": time.time(),
           "note": "Demonstration only; not an emergency service"}
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(HOST, 1883, 30)
client.loop_start()
result = client.publish(TOPIC, json.dumps(payload), qos=1)
result.wait_for_publish(timeout=10)
print("Published:", json.dumps(payload))
client.loop_stop()
client.disconnect()
