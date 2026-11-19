# DUOVEX ESA Demo Kit

Additive review evidence utilities; existing SUMO code and results are untouched.

## SUMO evidence
From the repository root, activate the project's Python environment, run the established SUMO simulation with seed 42, and preserve the original output. To inspect an existing CSV:

```powershell
python -m pip install -r esa-demo/analysis/requirements.txt
python esa-demo/analysis/inspect_traffic.py --csv results/raw/traffic.csv --out esa-demo/evidence
```

Check the output against a second independent run. Prior reference only: 1,800 seconds, 371 vehicles, 1,440 rows, eight monitored edges, 90-second fixed signal cycle. Do not infer unique vehicle counts from summed edge occupancies.

## MQTT local demonstration
```powershell
cd esa-demo/mqtt
docker compose up -d
python -m pip install -r requirements.txt
python driver_subscriber.py
```
In a second terminal in the same folder: `python ambulance_publisher.py`.

This is localhost-only simulated messaging. It does not establish Android, cellular delay, emergency routing, or real-world safety performance.

## Screenshots
Capture SUMO GUI, SUMO config, simulation console, CSV, generated graph, credited OSM junction reference, and MQTT subscriber. Phone screenshot is optional and only after an authenticated LAN test.

## Review sequence
OSM reference → SUMO simulation → CSV and graph → MQTT publish/subscribe → results and limitations. Real junction calibration, traffic prediction MAE, phone measurements, and direction-aware alerts remain future work.

Do not commit private footage, credentials, personally identifying location traces, or unreviewed results.
