import time
import logging
import configparser
import ipaddress
import subprocess
import socket

from networks import load_networks
from arp_scan import scan as arp_scan
from nmap_scan import enrich
from logger import setup
from sender import send

CONFIG_FILE = "/opt/iWebIT_Network_Discovery/config/agent.conf"
NETWORKS_FILE = "/opt/iWebIT_Network_Discovery/config/networks.conf"

setup()
logging.info("iWebIT Network Discovery Agent starting")

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

IDCOMPANY = config.getint("Agent", "IdCompany")
SCAN_INTERVAL = config.getint("Agent", "ScanInterval")

if IDCOMPANY <= 0:
    logging.error("IdCompany not configured. Agent will not run.")
    exit(1)


def get_local_network():
    """
    Descobre a rede local onde o host está (ex: 10.10.8.0/21)
    """
    cmd = ["ip", "-o", "-f", "inet", "addr", "show"]
    out = subprocess.check_output(cmd).decode()

    for line in out.splitlines():
        parts = line.split()
        iface = parts[1]
        cidr = parts[3]

        if iface.startswith("lo"):
            continue

        try:
            net = ipaddress.ip_network(cidr, strict=False)
            return str(net)
        except:
            pass

    return None


def nmap_ping_scan(network):
    """
    Faz descoberta ativa com Nmap Ping Scan (ICMP + TCP SYN)
    """
    logging.info(f"Running Nmap discovery on {network}")

    cmd = ["nmap", "-sn", "-PE", "-PS22,80,443", network]
    result = subprocess.run(cmd, capture_output=True, text=True)

    devices = []
    current_ip = None
    hostname = None

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("Nmap scan report for"):
            parts = line.split()

            if "(" in line:
                hostname = parts[4]
                current_ip = parts[-1].strip("()")
            else:
                hostname = None
                current_ip = parts[-1]

        if "Host is up" in line and current_ip:
            devices.append({
                "ip": current_ip,
                "hostname": hostname
            })
            current_ip = None
            hostname = None

    return devices


def resolve(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None


LOCAL_NET = get_local_network()
logging.info(f"Local network detected as: {LOCAL_NET}")


while True:
    logging.info("Starting network discovery scan")

    devices_payload = []
    networks = load_networks(NETWORKS_FILE)

    for network in networks:

        # --- LOCAL NETWORK → ARP + NMAP ---
        if LOCAL_NET and network == LOCAL_NET:
            logging.info(f"Using ARP + Nmap on LOCAL network {network}")

            devices = arp_scan(network)

            for d in devices:
                payload = {
                    "IP": d["ip"],
                    "MAC": d["mac"],
                    "Vendor": d.get("vendor"),
                    "Hostname": resolve(d["ip"]),
                    "OS": enrich(d["ip"]).get("os"),
                    "Network": network
                }
                devices_payload.append(payload)

        # --- REMOTE NETWORK → NMAP ONLY ---
        else:
            logging.info(f"Using Nmap discovery on REMOTE network {network}")

            devices = nmap_ping_scan(network)

            for d in devices:
                payload = {
                    "IP": d["ip"],
                    "MAC": None,  # Nem sempre disponível remotamente
                    "Vendor": None,
                    "Hostname": d.get("hostname") or resolve(d["ip"]),
                    "OS": enrich(d["ip"]).get("os"),
                    "Network": network
                }
                devices_payload.append(payload)

    if devices_payload:
        logging.info(f"{len(devices_payload)} devices discovered — sending to API")
        send(IDCOMPANY, devices_payload)
    else:
        logging.info("No devices discovered, nothing sent")

    logging.info("Scan completed")
    time.sleep(SCAN_INTERVAL)
