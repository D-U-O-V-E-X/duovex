import argparse
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    data = pd.read_csv(args.csv)
    required = {"time_s", "edge_id", "vehicle_count", "queue_length"}
    missing = required - set(data.columns)
    if missing:
        raise SystemExit(f"Missing columns: {sorted(missing)}")
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    print("Rows:", len(data))
    print("Edges:", data.edge_id.nunique())
    print("Time range:", data.time_s.min(), data.time_s.max())
    print("Missing values:", data.isna().sum().to_dict())
    print("Maximum observed queue:", data.queue_length.max())
    print("Mean recorded speed:", data.mean_speed_mps.mean() if "mean_speed_mps" in data else "column unavailable")
    grouped = data.groupby("time_s", as_index=False).agg(
        vehicle_count=("vehicle_count", "sum"),
        queue_length=("queue_length", "sum"))
    grouped.to_csv(output / "traffic_by_time.csv", index=False)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(grouped.time_s, grouped.queue_length)
    ax.set(xlabel="Simulation time (s)", ylabel="Sum of edge queue observations",
           title="SUMO observed queues over time")
    fig.tight_layout()
    fig.savefig(output / "traffic_timeseries.png", dpi=160)
    plt.close(fig)
    print("Wrote:", output / "traffic_timeseries.png")

if __name__ == "__main__":
    main()
