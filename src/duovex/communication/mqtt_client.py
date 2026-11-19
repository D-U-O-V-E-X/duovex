import json
import paho.mqtt.client as mqtt
from duovex.config import Settings

def publish_advisory(payload, settings=None):
    cfg = settings or Settings()
    cfg.validate()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(cfg.mqtt_host, cfg.mqtt_port, keepalive=30)
    client.loop_start()
    try:
        info = client.publish(cfg.mqtt_topic, json.dumps(payload), qos=cfg.mqtt_qos)
        info.wait_for_publish(timeout=5)
        if not info.is_published():
            raise TimeoutError("MQTT publish was not confirmed")
    finally:
        client.loop_stop()
        client.disconnect()
