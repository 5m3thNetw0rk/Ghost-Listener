import requests
from pyahmia import psearch

def dark_web_hunt(target_ip):
    print(f"🕵️  Agent Mission: Hunting for {target_ip} on the Dark Web...")
    
    try:
        # Use pyahmia to search indexed .onion sites
        # We search for the IP to see if it's in any 'Proxy Lists' or 'Target Lists'
        results = psearch(target_ip, limit=5)
        
        if not results:
            return "✅ Clean: No immediate mentions found in Dark Web indexes."
        
        report = f"⚠️  CRITICAL: Found {len(results)} mentions on Darknet sites!\n"
        for res in results:
            # Ahmia returns (title, link, snippet)
            report += f"- Site: {res[0]} | Link: {res[1]}\n"
        
        return report

    except Exception as e:
        return f"❌ Hunter Error: {e}"

# Simple test block
if __name__ == "__main__":
    test_ip = "193.168.1.1" # Replace with a real 'bad' IP to test later
    print(dark_web_hunt(test_ip))
