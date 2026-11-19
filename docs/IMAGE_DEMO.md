# Image → synthetic SUMO + MQTT demo

This **is not one-image reconstruction of real junction geometry**. A single photo cannot provide the intersection topology, true arrival-rate time series, signal timings, coordinates, or road calibration. The generator uses a declared **generic four-arm junction**. Vehicles detected in a single frame are repeated over a synthetic time window using an explicit multiplier. It does not prove prediction quality or ambulance detection.

## Prerequisites
Windows PowerShell, Python >=3.11, SUMO/netconvert on PATH, Docker Desktop for MQTT, and `python -m pip install -e ".[dev]"`.

## Run using a traffic photo and documented manual counts
Use a properly licensed or self-captured image. Review it and manually count each supported vehicle category:
```powershell
python -m duovex.simulation.image_demo --image "C:\path\to\traffic.jpg" --counts '{\"car\":8,\"motorcycle\":12,\"bus\":1,\"truck\":2}' --out results/image_demo --duration 600 --multiplier 10
sumo-gui -c results/image_demo/duovex.sumocfg --seed 42
```
Note: In PowerShell quoting, pass the JSON as a single string. If parsing fails, first run `python -m duovex.simulation.image_demo --help` and verify shell escaping.

## Optional automatic detection
Install Ultralytics separately (`pip install ultralytics`), obtain the model weights from a legitimate source and check their licence, then:
```powershell
python -m duovex.simulation.image_demo --image "C:\path\to\traffic.jpg" --weights "C:\path\to\model.pt" --out results/image_demo
```
This requires compatible class labels; detector accuracy on Indian mixed traffic is not established. The script never auto-downloads weights.

## MQTT subscriber
Start the existing broker: `docker compose up -d mosquitto`.
In terminal A: `python -m duovex.communication.driver_subscriber`.
In terminal B add `--publish-mqtt` to the image-demo command. This publishes a single **synthetic observation**, not continuous vehicle-to-vehicle messaging.

For a real mapped SUMO network, use OSM road geometry and inspect/correct its routes and signals. For valid traffic calibration, obtain timestamped counts and multiple observations.

## Evidence
Record original image source/licence, manually verified counts or model version, multiplier, simulation seed, generated `provenance.json`, screenshot, and MQTT message.
