import subprocess
import re

def enrich(ip):
    cmd = ["nmap", "-O", "-Pn", ip]
    r = subprocess.run(cmd, capture_output=True, text=True)

    os_match = re.search(r"OS details: (.+)", r.stdout)

    return {
        "os": os_match.group(1) if os_match else None
    }
