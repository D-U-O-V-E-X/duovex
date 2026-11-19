"""Console simulated-driver MQTT subscriber."""
import json
import paho.mqtt.client as mqtt
from duovex.config import Settings

def main():
    cfg = Settings()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected: {reason_code}")
        client.subscribe(cfg.mqtt_topic, qos=cfg.mqtt_qos)
    def on_message(client, userdata, message):
        try:
            payload = json.loads(message.payload.decode("utf-8"))
            print(f"DRIVER ADVISORY [{payload.get('event_type','unknown')}]: {payload}")
        except (UnicodeDecodeError, json.JSONDecodeError):
            print("Ignored malformed advisory payload")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(cfg.mqtt_host, cfg.mqtt_port, keepalive=30)
    print(f"Listening on {cfg.mqtt_topic}; Ctrl+C to stop")
    try: client.loop_forever()
    except KeyboardInterrupt: client.disconnect()
if __name__ == "__main__": main()
