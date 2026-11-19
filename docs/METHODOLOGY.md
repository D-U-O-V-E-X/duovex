# Methodology and claims
Record seed, simulation demand, vehicle mix, run duration, software versions, MQTT QoS, impairment probability/delay and run ID.

Collect vehicle count, mean speed, queue length and (where available) travel time at fixed intervals. Persistence predicts the next count as the latest observation; historical average uses the arithmetic mean of the history window. Evaluate on a chronological holdout using MAE/RMSE.

Emergency alerts use simulated position and heading geometry. This heuristic is not a validated collision-warning model.

Distinguish application-level dropping before MQTT publish from network impairment. MQTT QoS acknowledgements do not prove driver-visible receipt. Preserve raw outputs and derive charts from saved data. SUMO results are not real-world validation; mobile-app deployment and real-camera validation remain future work.
