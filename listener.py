import socket
import requests
import sys
from datetime import datetime

# --- CONFIGURATION ---
LISTEN_IP = "0.0.0.0"  # Listens on all interfaces
LISTEN_PORT = 9999     # Feel free to change this to 8080 or 4444
LOG_FILE = "ghost_hits.log"
GEO_API = "http://ip-api.com/json/"

def defang_ip(ip):
    """Safety first: Returns a defanged IP (e.g., 1.1.1[.]1)"""
    return ip.replace(".", "[.]")

def get_intel(ip):
    """Queries OSINT data for the attacker IP."""
    if ip == '127.0.0.1' or ip == 'localhost':
        return "Internal Test (Localhost Loopback)"
    
    try:
        # 5-second timeout to prevent the listener from hanging
        response = requests.get(f"{GEO_API}{ip}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return f"{data.get('city')}, {data.get('country')} | ISP: {data.get('isp')}"
        return "No public geolocation data found."
    except Exception as e:
        return f"Enrichment unavailable: {str(e)}"

def start_honeypot():
    # Create TCP Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow the port to be reused immediately after restart
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((LISTEN_IP, LISTEN_PORT))
        server_socket.listen(5)
        
        print(f"👻 [Ghost-Listener] STATUS: ONLINE")
        print(f"📍 Monitoring Port: {LISTEN_PORT}")
        print(f"📂 Logging hits to: {LOG_FILE}")
        print("-" * 50)

        while True:
            # Accept incoming connection
            client_conn, client_addr = server_socket.accept()
            attacker_ip = client_addr[0]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Triage the hit
            intel = get_intel(attacker_ip)
            safe_ip = defang_ip(attacker_ip)

            # Terminal Output
            print(f"\n⚠️  ALERT: Connection Attempt Detected!")
            print(f"🕒 Time:  {timestamp}")
            print(f"🌐 IP:    {safe_ip}")
            print(f"🌍 Intel: {intel}")
            
            # Log to File
            with open(LOG_FILE, "a") as f:
                f.write(f"[{timestamp}] IP: {attacker_ip} | Intel: {intel}\n")
            
            # Send a fake 'Unauthorized' banner and close
            try:
                client_conn.send(b"HTTP/1.1 401 Unauthorized\r\nServer: Ghost-Sensor/1.0\r\n\r\n")
                client_conn.close()
            except:
                pass

    except KeyboardInterrupt:
        print("\n🛑 Ghost-Listener shutting down safely. Out.")
        server_socket.close()
        sys.exit(0)
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_honeypot()
