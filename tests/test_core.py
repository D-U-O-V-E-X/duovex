import pytest
from duovex.traffic import TrafficObservation, PersistenceBaseline, HistoricalAverageBaseline
from duovex.reliability import impair_messages, summarize
from duovex.alerts import VehicleState, build_ambulance_alert

def observation(t, count):
    return TrafficObservation(t, "edge", count, 5.0, 2)

def test_prediction_baselines():
    history = [observation(0,10), observation(1,20)]
    assert PersistenceBaseline().predict(history) == 20
    assert HistoricalAverageBaseline().predict(history) == 15

def test_empty_history_rejected():
    with pytest.raises(ValueError): PersistenceBaseline().predict([])

def test_seeded_application_impairment():
    messages = [{"id":i} for i in range(100)]
    a,_ = impair_messages(messages, 0.2, 25, 7)
    b,_ = impair_messages(messages, 0.2, 25, 7)
    assert a == b and len(a) < 100

def test_delivery_metrics():
    result = summarize(10,8,[10,20])
    assert result.delivery_ratio == 0.8
    assert result.mean_latency_ms == 15

def test_ambulance_alert_direction_and_range():
    ambulance = VehicleState("amb",0,100,180)
    driver = VehicleState("car",0,0,0)
    assert build_ambulance_alert(ambulance,driver,200) is not None
    assert build_ambulance_alert(ambulance,driver,50) is None
