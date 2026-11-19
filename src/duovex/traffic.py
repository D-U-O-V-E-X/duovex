from dataclasses import dataclass
from collections import defaultdict, deque
from statistics import mean

@dataclass(frozen=True)
class TrafficObservation:
    timestamp_s: float
    edge_id: str
    vehicle_count: int
    mean_speed_mps: float
    queue_length: int
    mean_travel_time_s: float | None = None

class PersistenceBaseline:
    def predict(self, history: list[TrafficObservation]) -> float:
        if not history: raise ValueError("History cannot be empty")
        return float(history[-1].vehicle_count)

class HistoricalAverageBaseline:
    def predict(self, history: list[TrafficObservation]) -> float:
        if not history: raise ValueError("History cannot be empty")
        return float(mean(o.vehicle_count for o in history))

class ObservationStore:
    def __init__(self, maxlen=1000):
        self._items = defaultdict(lambda: deque(maxlen=maxlen))
    def add(self, observation):
        self._items[observation.edge_id].append(observation)
    def history(self, edge_id):
        return list(self._items[edge_id])
