"""Run SUMO through TraCI and save per-edge traffic observations."""
import argparse
import csv
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=1800)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="results/raw/traffic.csv")
    args = parser.parse_args()
    if args.steps <= 0: parser.error("--steps must be positive")
    try:
        import traci
    except ImportError as exc:
        raise SystemExit("TraCI unavailable. Install SUMO and add SUMO_HOME/tools to PYTHONPATH.") from exc
    root = Path(__file__).resolve().parents[3]
    config = root / "simulation" / "duovex.sumocfg"
    if not config.exists():
        raise SystemExit("Scenario missing; run python -m duovex.simulation.build_network first.")
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    binary = os.environ.get("SUMO_BINARY", "sumo")
    traci.start([binary, "-c", str(config), "--seed", str(args.seed), "--end", str(args.steps)])
    try:
        edge_ids = [e for e in traci.edge.getIDList() if not e.startswith(":")]
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["time_s","edge_id","vehicle_count","mean_speed_mps","queue_length"])
            writer.writeheader()
            while traci.simulation.getMinExpectedNumber() > 0 and traci.simulation.getTime() < args.steps:
                traci.simulationStep()
                now = traci.simulation.getTime()
                if int(now) % 10 == 0:
                    for edge in edge_ids:
                        writer.writerow({"time_s":now,"edge_id":edge,
                            "vehicle_count":traci.edge.getLastStepVehicleNumber(edge),
                            "mean_speed_mps":round(traci.edge.getLastStepMeanSpeed(edge),3),
                            "queue_length":traci.edge.getLastStepHaltingNumber(edge)})
    finally:
        traci.close()
    print(f"Saved observations: {output}")
if __name__ == "__main__": main()
