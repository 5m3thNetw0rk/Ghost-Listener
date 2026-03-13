# 👻 Ghost-Listener: Tactical Reconnaissance Sensor

## 📋 Overview
Ghost-Listener is a **Low-Interaction Honeypot** designed to detect internal reconnaissance and lateral movement. It acts as a network "tripwire," logging unauthorized connection attempts and automatically enriching source IPs with OSINT geolocation data.

## 🚀 Features
* **Real-time Detection**: Monitors specific ports for TCP connection attempts.
* **OSINT Enrichment**: Automatically identifies the ISP and geographic origin of the attacker.
* **Safety First**: Implements "Defanging" on all logged IPs to prevent accidental execution in reports.
* **Passive Response**: Mimics a standard service banner to encourage attackers to reveal their tooling.

## 🎯 Usage
1. **Initialize**: `python3 listener.py`
2. **Logs**: All hits are recorded in `ghost_hits.log` for post-incident analysis.

> **💂 OpSec Note**: This tool is intended for lab environments or internal network monitoring. Always ensure you have authorization to bind to ports on your host network.
