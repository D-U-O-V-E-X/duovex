"""Generate a *synthetic* SUMO junction demand scenario from a traffic image.

One image is not enough to reconstruct lane geometry, signal timings, or hourly flow.
Use --counts for documented human annotations; --weights for a locally available
Ultralytics detector (optional). Counts are a single-frame observation, not flow.
"""
import argparse
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from duovex.communication.mqtt_client import publish_advisory


SUPPORTED = ("car", "motorcycle", "bus", "truck")
ALIASES = {"car": "car", "motorcycle": "motorcycle", "motorbike": "motorcycle",
           "bus": "bus", "truck": "truck"}

def validate_counts(counts):
    if not isinstance(counts, dict):
        raise TypeError("Counts must be a JSON object")
    result = dict.fromkeys(SUPPORTED, 0)
    for name, value in counts.items():
        if name not in SUPPORTED or type(value) is not int or value < 0:
            raise ValueError(f"Invalid count {name}={value}; expected nonnegative integers for {SUPPORTED}")
        result[name] = value
    return result

def detect_counts(image, weights, confidence):
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError("Install optional detector: pip install ultralytics") from exc
    if not Path(weights).is_file():
        raise FileNotFoundError(f"Model weights not found locally: {weights}")
    model = YOLO(str(weights))
    output = model.predict(source=str(image), conf=confidence, verbose=False)
    counts = dict.fromkeys(SUPPORTED, 0)
    for prediction in output:
        for class_id in prediction.boxes.cls.tolist():
            label = str(prediction.names[int(class_id)]).lower()
            mapped = ALIASES.get(label)
            if mapped:
                counts[mapped] += 1
    return counts

def write_scenario(out, counts, duration_s, multiplier):
    """Each vehicle detected in one photo is replicated multiplier times over duration.

    This is a declared *assumption*, not an inferred arrival rate or traffic count.
    """
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    nodes = ET.Element("nodes")
    ET.SubElement(nodes, "node", id="C", x="0", y="0", type="traffic_light")
    for name, x, y in (("N", 0, 300), ("S", 0, -300), ("E", 300, 0), ("W", -300, 0)):
        ET.SubElement(nodes, "node", id=name, x=str(x), y=str(y))
    ET.ElementTree(nodes).write(out / "nodes.nod.xml", encoding="unicode")
    edges = ET.Element("edges")
    for direction in ("n", "s", "e", "w"):
        outer = direction.upper()
        ET.SubElement(edges, "edge", id=f"{direction}_in", attrib={"from": outer, "to": "C", "numLanes": "2", "speed": "13.9"})
        ET.SubElement(edges, "edge", id=f"{direction}_out", attrib={"from": "C", "to": outer, "numLanes": "2", "speed": "13.9"})
    ET.ElementTree(edges).write(out / "edges.edg.xml", encoding="unicode")
    subprocess.run(["netconvert", "--node-files", str(out / "nodes.nod.xml"),
                    "--edge-files", str(out / "edges.edg.xml"),
                    "-o", str(out / "junction.net.xml")], check=True)
    types = {"car": ("passenger", "5", "13.9"),
             "motorcycle": ("motorcycle", "2", "11"),
             "bus": ("bus", "10", "10"),
             "truck": ("truck", "8", "10")}
    routes = ET.Element("routes")
    for typ, (vehicle_class, length, speed) in types.items():
        ET.SubElement(routes, "vType", id=typ, vClass=vehicle_class,
                      length=length, maxSpeed=speed, accel="2", decel="4.5")
    for name, path in (("ns", "n_in s_out"), ("sn", "s_in n_out"),
                       ("ew", "e_in w_out"), ("we", "w_in e_out")):
        ET.SubElement(routes, "route", id=name, edges=path)
    for typ, number in counts.items():
        total = number * multiplier
        if total == 0:
            continue
        for index, direction in enumerate(("ns", "sn", "ew", "we")):
            allocated = total // 4 + (1 if index < total % 4 else 0)
            if allocated:
                ET.SubElement(routes, "flow", id=f"{typ}_{direction}", type=typ,
                              route=direction, begin="0", end=str(duration_s),
                              number=str(allocated))
    ET.ElementTree(routes).write(out / "routes.rou.xml", encoding="unicode")
    config = ET.Element("configuration")
    cfg_input = ET.SubElement(config, "input")
    ET.SubElement(cfg_input, "net-file", value="junction.net.xml")
    ET.SubElement(cfg_input, "route-files", value="routes.rou.xml")
    timeline = ET.SubElement(config, "time")
    ET.SubElement(timeline, "begin", value="0")
    ET.SubElement(timeline, "end", value=str(duration_s))
    ET.ElementTree(config).write(out / "duovex.sumocfg", encoding="unicode")
    return out / "duovex.sumocfg"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--counts", help='JSON e.g. {"car":8,"motorcycle":12,"bus":1}')
    parser.add_argument("--weights", type=Path, help="Already downloaded Ultralytics model weights")
    parser.add_argument("--confidence", type=float, default=0.3)
    parser.add_argument("--out", type=Path, default=Path("results/image_demo"))
    parser.add_argument("--duration", type=int, default=600)
    parser.add_argument("--multiplier", type=int, default=10)
    parser.add_argument("--publish-mqtt", action="store_true", help="Publish one observation via existing MQTT module")
    args = parser.parse_args()
    if not args.image.is_file():
        parser.error("Image does not exist")
    if bool(args.counts) == bool(args.weights):
        parser.error("Provide exactly one of --counts or --weights")
    if args.duration <= 0 or args.multiplier <= 0 or not 0 < args.confidence <= 1:
        parser.error("duration, multiplier, and confidence must be positive")
    counts = validate_counts(json.loads(args.counts)) if args.counts else detect_counts(
        args.image, args.weights, args.confidence)
    config = write_scenario(args.out, counts, args.duration, args.multiplier)
    metadata = {"source_image":str(args.image), "counts":counts,
                "count_method":"manual" if args.counts else "optional_object_detection",
                "scenario_type":"synthetic_four_arm", "duration_s":args.duration,
                "assumed_repetitions_per_detected_vehicle":args.multiplier,
                "caveat":"One-frame counts are not measured arrival rates; road geometry is not image-reconstructed"}
    (args.out / "provenance.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print("Scenario:", config)
    print("Counts:", json.dumps(counts))
    print("Assumption:", metadata["caveat"])
    if args.publish_mqtt:
        publish_advisory({"event_type":"synthetic_image_traffic_observation", **metadata})
        print("Published one synthetic observation to the configured MQTT topic")

if __name__ == "__main__":
    main()
