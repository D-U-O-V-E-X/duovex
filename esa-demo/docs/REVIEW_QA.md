# ESA review questions and answers

**What is implemented?** A reproducible SUMO traffic-state baseline; local MQTT demonstration utilities are newly added and require a runtime test.

**Is the SUMO network the calibrated Hosur Road / Hewlett Packard Avenue junction?** Do not claim that unless topology and signal plans have been verified against the real junction.

**What does seed 42 prove?** Reproducibility under unchanged simulation configuration, demand, software and collection logic; independently rerun and compare outputs.

**Why MQTT?** It demonstrates publish/subscribe messaging for a future phone-to-server-to-phone advisory pipeline. A local demo does not establish cellular latency or alert effectiveness.

**What is not yet validated?** XGBoost and other prediction MAEs, actual phone-to-phone measurements, ambulance targeting, real signal timing and junction-level traffic counts.

**How is this different from direct V2X?** Ordinary phones communicate through mobile networks and servers; this is advisory and not suitable for split-second collision avoidance.

**How will results be evaluated?** Unseen-day prediction errors versus baselines; advice correctness against observed signal states; delivery ratios and end-to-end delay under measured phone-network conditions.
