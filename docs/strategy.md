# 🕸️ Ghost-Listener: Collection Strategy
## 1. Role in the Intelligence Cycle
Ghost-Listener serves as a **Low-Interaction Production Honeypot**. Its primary goal is to provide "Zero-Noise" telemetry. Since no legitimate service runs on Port 9999, any connection attempt is categorized as **pre-attack reconnaissance**.

## 2. Intelligence Value
- **Early Warning:** Detecting IP addresses scanning for non-standard ports before they hit production assets.
- **TTP Mapping:** Identifying if attackers are using automated scanners (Masscan/ZMap) or manual probes (Curl/Telnet).
- **Attribution:** Correlating hits with known botnet infrastructure or VPN/Tor exit nodes via the Sentinel Hunter Agent.

## 3. Deployment Model
This sensor is designed to be deployed on "Edge" subnets. Data collected here feeds directly into the **Sentinel Dashboard**, where it is triaged and converted into STIX-formatted indicators for blocking at the firewall level.
