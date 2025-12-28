import subprocess

def scan(network):
    cmd = ["arp-scan", network]
    result = subprocess.run(cmd, capture_output=True, text=True)
    devices = []

    for line in result.stdout.splitlines():
        if "\t" in line:
            parts = line.split("\t")
            if len(parts) >= 3:
                devices.append({
                    "ip": parts[0],
                    "mac": parts[1],
                    "vendor": parts[2]
                })

    return devices
