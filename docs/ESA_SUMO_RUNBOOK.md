# DUOVEX Phase-I SUMO ESA runbook

The `simulation/` directory contains the preserved 2026-11-19 local starter junction, committed from backup `6effd0a`. It is a **synthetic four-arm network**, not the surveyed Hosur Road–Hewlett Packard Avenue junction. The checked-in `junction.net.xml` was generated with SUMO netconvert 1.28.0 and defines 42 s / 3 s / 42 s / 3 s signal phases (90 s total).

## Install prerequisites (Windows)

- Python 3.11 or newer, Python package dependencies: `python -m pip install -e ".[dev]"`
- Eclipse SUMO tools `sumo`, `sumo-gui`, `netconvert`, and Python `traci` available. Add SUMO's `tools` to `PYTHONPATH` or install the supported TraCI package.
- Docker Desktop for optional MQTT broker and simulated driver.

**Do not regenerate `simulation/` before the review** unless you intentionally want to overwrite the checked-in scenario and invalidate direct comparisons.

## Verify the committed network

```powershell
python -m pytest -q
python -m duovex.simulation.run --steps 1800 --seed 42 --output results/raw/traffic_esa.csv
$env:SUMO_BINARY = "sumo-gui"
python -m duovex.simulation.run --steps 1800 --seed 42 --output results/raw/traffic_esa_gui.csv
Remove-Item Env:SUMO_BINARY
```

For a second independent headless run, save another CSV filename and compare hashes. Different output paths should not change the recorded observations when the scenario and software are unchanged.

```powershell
python -m duovex.simulation.run --steps 1800 --seed 42 --output results/raw/traffic_esa_repeat.csv
Get-FileHash results/raw/traffic_esa.csv
Get-FileHash results/raw/traffic_esa_repeat.csv
```

If hashes differ, investigate software versions, file contents, seed, and run settings. Capture terminal output, CSV, SUMO-GUI, and the recorded signal phases.

## Graph

```powershell
python -m pip install -r esa-demo/analysis/requirements.txt
python esa-demo/analysis/inspect_traffic.py --csv results/raw/traffic_esa.csv --out results/plots/esa
```

CSV columns are `time_s, edge_id, vehicle_count, mean_speed_mps, queue_length`. The sum of per-edge vehicle counts is **not** the unique number of vehicles inserted into the simulation.

## MQTT demonstration

```powershell
docker compose up -d mosquitto
python -m duovex.communication.driver_subscriber
```

In another terminal run the image demo with `--publish-mqtt` as described in `docs/IMAGE_DEMO.md`. This proves local MQTT transportation of a traffic observation, not cellular network delay or driver-specific warning accuracy.

## Evidence boundary

Python CI checks structure, unit tests and lint; it does not run SUMO binaries, MQTT broker containers, camera inference, or any mobile phone. These require local demonstrations. For source and licence/consent, document your actual photograph provenance before reuse.
