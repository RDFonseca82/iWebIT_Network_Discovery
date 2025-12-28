import time
import logging
import configparser

from networks import load_networks
from arp_scan import scan as arp_scan
from nmap_scan import enrich
from hostname import resolve
from logger import setup
from sender import send

CONFIG_FILE = "/opt/iWebIT_Network_Discovery/config/agent.conf"
NETWORKS_FILE = "/opt/iWebIT_Network_Discovery/config/networks.conf"

setup()

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

IDCOMPANY = config.getint("Agent", "IdCompany")
SCAN_INTERVAL = config.getint("Agent", "ScanInterval")

if IDCOMPANY <= 0:
    logging.error("IdCompany not configured. Agent will not run.")
    exit(1)

while True:
    logging.info("Starting network discovery scan")

    devices_payload = []

    for network in load_networks(NETWORKS_FILE):
        devices = arp_scan(network)

        for device in devices:
            device_payload = {
                "IP": device["ip"],
                "MAC": device["mac"],
                "Vendor": device.get("vendor"),
                "Hostname": resolve(device["ip"]),
                "OS": enrich(device["ip"]).get("os"),
                "Network": network
            }

            devices_payload.append(device_payload)

    if devices_payload:
        send(IDCOMPANY, devices_payload)
    else:
        logging.info("No devices discovered, nothing sent")

    logging.info("Scan completed")
    time.sleep(SCAN_INTERVAL)
