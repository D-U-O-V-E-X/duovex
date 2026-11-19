"""Structural checks of the checked-in synthetic SUMO starter scenario.

These checks do not replace a live SUMO/TraCI rerun.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulation"


def test_checked_in_configuration_references_existing_assets():
    config = ET.parse(SIM / "duovex.sumocfg").getroot()
    for xml_path in config.findall("./input/*"):
        for name in xml_path.attrib["value"].split(","):
            assert (SIM / name).is_file(), name


def test_routes_reference_network_edges():
    network = ET.parse(SIM / "junction.net.xml").getroot()
    edges = {item.attrib["id"] for item in network.findall("edge")
             if item.attrib.get("function") != "internal"}
    routes = ET.parse(SIM / "routes.rou.xml").getroot()
    assert len(routes.findall("flow")) >= 1
    assert len(routes.findall("vehicle")) >= 1
    for route in routes.findall("route"):
        assert set(route.attrib["edges"].split()) <= edges


def test_signal_program_is_fixed_ninety_seconds():
    network = ET.parse(SIM / "junction.net.xml").getroot()
    signal = network.find("./tlLogic")
    assert signal is not None
    durations = [int(float(phase.attrib["duration"])) for phase in signal.findall("phase")]
    assert durations == [42, 3, 42, 3]
    assert sum(durations) == 90


def test_validated_source_files_are_parseable():
    for name in ("nodes.nod.xml", "edges.edg.xml", "validated.nod.xml",
                 "validated.edg.xml", "validated.con.xml", "validated.tll.xml",
                 "validated.netccfg"):
        assert ET.parse(SIM / name).getroot() is not None
