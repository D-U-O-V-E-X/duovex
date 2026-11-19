from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    mqtt_host: str = os.getenv("DUOVEX_MQTT_HOST", "127.0.0.1")
    mqtt_port: int = int(os.getenv("DUOVEX_MQTT_PORT", "1883"))
    mqtt_topic: str = os.getenv("DUOVEX_MQTT_TOPIC", "duovex/advisories")
    mqtt_qos: int = int(os.getenv("DUOVEX_MQTT_QOS", "1"))
    alert_radius_m: float = float(os.getenv("DUOVEX_ALERT_RADIUS_METRES", "300"))
    message_ttl_s: int = int(os.getenv("DUOVEX_MESSAGE_TTL_SECONDS", "10"))

    def validate(self):
        if self.mqtt_qos not in (0, 1, 2):
            raise ValueError("MQTT QoS must be 0, 1, or 2")
        if self.alert_radius_m <= 0 or self.message_ttl_s <= 0:
            raise ValueError("Radius and message TTL must be positive")
