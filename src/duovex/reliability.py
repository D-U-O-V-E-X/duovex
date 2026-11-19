from dataclasses import dataclass
from statistics import mean
import random

@dataclass(frozen=True)
class ReliabilityResult:
    attempted: int
    delivered: int
    delivery_ratio: float
    mean_latency_ms: float | None

def impair_messages(messages, drop_probability=0.0, delay_ms=0.0, seed=42):
    """Simulate application-level drop/delay before publish, not network packet loss."""
    if not 0 <= drop_probability <= 1 or delay_ms < 0:
        raise ValueError("Invalid impairment settings")
    rng = random.Random(seed)
    kept = [m for m in messages if rng.random() >= drop_probability]
    return kept, [float(delay_ms)] * len(kept)

def summarize(attempted, delivered, latencies_ms):
    if attempted < 0 or not 0 <= delivered <= attempted:
        raise ValueError("Require 0 <= delivered <= attempted")
    return ReliabilityResult(attempted, delivered, delivered/attempted if attempted else 0.0,
                             mean(latencies_ms) if latencies_ms else None)
