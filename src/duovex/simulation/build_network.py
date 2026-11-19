"""Create a simple four-arm junction scenario using SUMO netconvert."""
from pathlib import Path
import subprocess

def main():
    root = Path(__file__).resolve().parents[3]
    sim = root / "simulation"
    sim.mkdir(exist_ok=True)
    nodes = sim / "nodes.nod.xml"
    edges = sim / "edges.edg.xml"
    nodes.write_text('''<nodes>
<node id="C" x="0" y="0" type="traffic_light"/>
<node id="N" x="0" y="300"/><node id="S" x="0" y="-300"/>
<node id="E" x="300" y="0"/><node id="W" x="-300" y="0"/>
</nodes>''', encoding="utf-8")
    edges.write_text('''<edges>
<edge id="n_in" from="N" to="C" numLanes="2" speed="13.9"/>
<edge id="s_in" from="S" to="C" numLanes="2" speed="13.9"/>
<edge id="e_in" from="E" to="C" numLanes="2" speed="13.9"/>
<edge id="w_in" from="W" to="C" numLanes="2" speed="13.9"/>
<edge id="n_out" from="C" to="N" numLanes="2" speed="13.9"/>
<edge id="s_out" from="C" to="S" numLanes="2" speed="13.9"/>
<edge id="e_out" from="C" to="E" numLanes="2" speed="13.9"/>
<edge id="w_out" from="C" to="W" numLanes="2" speed="13.9"/>
</edges>''', encoding="utf-8")
    subprocess.run(["netconvert","--node-files",str(nodes),"--edge-files",str(edges),
                    "-o",str(sim/"junction.net.xml")], check=True)
    (sim/"routes.rou.xml").write_text('''<routes>
<vType id="car" vClass="passenger" accel="2.6" decel="4.5" length="5" maxSpeed="13.9"/>
<vType id="bike" vClass="motorcycle" accel="3" decel="5" length="2" maxSpeed="11"/>
<vType id="bus" vClass="bus" accel="1.2" decel="4" length="10" maxSpeed="10"/>
<vType id="ambulance" vClass="emergency" accel="3" decel="5" length="5" maxSpeed="16"/>
<route id="ns" edges="n_in s_out"/><route id="sn" edges="s_in n_out"/>
<route id="ew" edges="e_in w_out"/><route id="we" edges="w_in e_out"/>
<flow id="cars_ns" type="car" route="ns" begin="0" end="1800" vehsPerHour="500"/>
<flow id="bikes_ew" type="bike" route="ew" begin="0" end="1800" vehsPerHour="180"/>
<flow id="bus_sn" type="bus" route="sn" begin="0" end="1800" vehsPerHour="60"/>
<vehicle id="ambulance_1" type="ambulance" route="we" depart="300"/>
</routes>''', encoding="utf-8")
    (sim/"duovex.sumocfg").write_text('''<configuration><input>
<net-file value="junction.net.xml"/><route-files value="routes.rou.xml"/>
</input><time><begin value="0"/><end value="1800"/></time></configuration>''', encoding="utf-8")
    print("Scenario generated. Inspect routes, connections and signal phases in SUMO-GUI.")
if __name__ == "__main__": main()
