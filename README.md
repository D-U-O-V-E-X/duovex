# DUOVEX
Smartphone-based V2N2V traffic assistance research prototype.

## Scope
SUMO/TraCI heterogeneous-traffic simulation; traffic observations and persistence/historical-average baselines; simulated ambulance proximity/direction advisories; MQTT broker and simulated driver endpoint; controlled reliability experiments.

This project provides advisories only. It does not actuate public signals or provide production emergency dispatch. The initial driver endpoint is simulated; a mobile app and real-camera validation are future work unless supported by separate evidence.

## Setup (Windows PowerShell)
Install Python 3.11+, SUMO and Docker Desktop. Ensure `python`, `sumo`, and `netconvert` are on PATH and configure `SUMO_HOME`.
```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
docker compose up -d mosquitto
python -m duovex.simulation.build_network
python -m pytest
```
If `py` is not recognized, use `python --version` and `where.exe python`; install Python 3.11 if neither works.

## Architecture
SUMO -> traffic-state extraction -> prediction baselines -> advisory generation -> MQTT -> simulated driver. Reliability evaluation measures attempted/received messages, delivery ratio and latency.

**Measurement discipline:** application-level dropping before MQTT publish is not network packet loss. MQTT QoS 0/1/2 are protocol delivery semantics, not proof that a driver received or displayed an alert. Record seeds, versions, run IDs and impairment settings. Never present simulation as real-world validation.

## ESA review demo (checked-in reference scenario)
The preserved synthetic SUMO junction and routes are now in `simulation/`. See [the reproducible SUMO runbook](docs/ESA_SUMO_RUNBOOK.md) for Windows prerequisites, SUMO-GUI, CSV evidence and MQTT steps. Do not run `build_network` before replaying the committed scenario: it rewrites several simulation inputs.

A separate [image-conditioned scenario demo](docs/IMAGE_DEMO.md) turns human-annotated vehicle counts or optional local object-detector output into *synthetic* demand for a generic junction. A single photo does not reconstruct real junction geometry or signal phase timings. Camera inference, end-to-end SUMO execution, and real-phone MQTT delivery still need independent local verification.
