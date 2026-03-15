import os
import socket
import requests
import sys
from datetime import datetime

# --- CONFIGURATION ---
LISTEN_IP = "0.0.0.0" 
LISTEN_PORT = 9999     
LOG_FILE = "/Users/mattsmethurst/Developer/Sentinel-Dashboard/ghost_hits.log"
≈GEO_API = "http://ip-api.com/json/"

def get_intel(ip):
    """Returns a tuple of (Description, Latitude, Longitude)."""
    # Hardcoded coordinates for your Manchester test so the map works locally
    if ip == '127.0.0.1' or ip == 'localhost':
        return "Internal Test (Manchester)", 53.4808, -2.2426
    
    try:
        # Querying public IP for Geo-Location
        response = requests.get(f"{GEO_API}{ip}", timeout=5)
        data = response.json()
        if data.get('status') == 'success':
            desc = f"{data.get('city')}, {data.get('country')}"
            return desc, data.get('lat'), data.get('lon')
    except Exception as e:
        print(f"Lookup Error: {e}")
    
    # Fallback if lookup fails
    return "Unknown Origin", 0.0, 0.0

def start_honeypot():
    # Create the TCP Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # This allows the script to restart without "Address already in use" errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((LISTEN_IP, LISTEN_PORT))
        server_socket.listen(5)
        
        print(f"👻 [Ghost-Listener] STATUS: ONLINE")
        print(f"📍 Monitoring Port: {LISTEN_PORT}")
        print(f"📂 Logging hits to: {LOG_FILE}")
        print("-" * 50)

        while True:
            # Wait for a connection
            client_conn, client_addr = server_socket.accept()
            attacker_ip = client_addr[0]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Triage the connection
            intel_desc, lat, lon = get_intel(attacker_ip)

            # WRITE TO LOG (CSV format for Streamlit)
            # Layout: Timestamp,IP,Description,Latitude,Longitude
            with open(LOG_FILE, "a") as f:
                f.write(f"{timestamp},{attacker_ip},{intel_desc},{lat},{lon}\n")
            
            print(f"⚠️  HIT DETECTED: {attacker_ip} | Location: {intel_desc}")
            
            # Send a fake response and close
            try:
                client_conn.send(b"HTTP/1.1 401 Unauthorized\r\nServer: Ghost-Sensor/1.0\r\n\r\n")
                client_conn.close()
            except:
                pass

    except KeyboardInterrupt:
        print("\n🛑 Ghost-Listener shutting down. Tactical retreat.")
        server_socket.close()
        sys.exit(0)
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_honeypot()
