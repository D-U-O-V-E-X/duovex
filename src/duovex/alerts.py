from dataclasses import dataclass
from math import atan2, degrees, hypot
from time import time
from uuid import uuid4


@dataclass(frozen=True)
class VehicleState:
    vehicle_id: str
    x: float
    y: float
    heading_deg: float

def _delta(a, b):
    return abs((a - b + 180) % 360 - 180)

def build_ambulance_alert(ambulance: VehicleState, driver: VehicleState,
                          radius_m=300, direction_tolerance_deg=65):
    dx, dy = ambulance.x-driver.x, ambulance.y-driver.y
    distance = hypot(dx, dy)
    if distance > radius_m: return None
    bearing = (degrees(atan2(dx, dy)) + 360) % 360
    if _delta(driver.heading_deg, bearing) > direction_tolerance_deg: return None
    return {"schema_version":"1.0", "message_id":str(uuid4()),
            "event_type":"emergency_vehicle_approach", "created_at_unix":time(),
            "expires_in_s":10, "ambulance_id":ambulance.vehicle_id,
            "distance_m":round(distance,2), "bearing_deg":round(bearing,1),
            "message":"Emergency vehicle approaching; remain alert and give way safely."}
