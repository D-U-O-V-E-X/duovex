import xml.etree.ElementTree as ET
from unittest.mock import patch

import pytest

from duovex.simulation.image_demo import validate_counts, write_scenario


def test_counts_are_strict():
    assert validate_counts({"car": 2})["motorcycle"] == 0
    for invalid in ({"car": -1}, {"bus": 1.2}, {"van": 3}, {"car": True}):
        with pytest.raises(ValueError):
            validate_counts(invalid)

def test_generated_synthetic_scenario(tmp_path):
    with patch("duovex.simulation.image_demo.subprocess.run") as call:
        cfg = write_scenario(tmp_path, {"car": 2, "motorcycle": 1, "bus": 0, "truck": 0}, 600, 10)
    assert cfg.exists()
    call.assert_called_once()
    routes = ET.parse(tmp_path / "routes.rou.xml").getroot()
    assert sum(int(flow.attrib["number"]) for flow in routes.findall("flow")) == 30
    assert len(routes.findall("route")) == 4
    assert ET.parse(cfg).getroot().tag == "configuration"
