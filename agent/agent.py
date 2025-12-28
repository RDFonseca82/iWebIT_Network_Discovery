import time
import logging

from networks import load_networks
from arp_scan import scan as arp_scan
from nmap_scan import enrich
from hostname import resolve
from cache import save
from logger import setup

setup()

NETWORKS_FILE = "/opt/iWebIT_Network_Discovery/config/networks.conf"
SCAN_INTERVAL = 3600

while True:
    logging.info("Starting network discovery scan")
    results = []

    for network in load_networks(NETWORKS_FILE):
        devices = arp_scan(network)

        for device in devices:
            device["hostname"] = resolve(device["ip"])
            device.update(enrich(device["ip"]))

        results.append({
            "network": network,
            "devices": devices
        })

    save(results)
    logging.info("Network discovery scan completed")

    time.sleep(SCAN_INTERVAL)
