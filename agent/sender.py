import json
import requests
import logging
import os

API_URL = "https://agent.iwebit.app/scripts/script_network_discovery.php"
PAYLOAD_LOG = "/opt/iWebIT_Network_Discovery/logs/last_payload.json"


def send(id_company, devices):
    payload = {
        "IdCompany": id_company,
        "Devices": devices
    }

    # GUARDA O PAYLOAD LOCALMENTE
    try:
        os.makedirs("/opt/iWebIT_Network_Discovery/logs", exist_ok=True)
        with open(PAYLOAD_LOG, "w") as f:
            json.dump(payload, f, indent=2)
        logging.info(f"Payload written to {PAYLOAD_LOG}")
    except Exception as e:
        logging.error(f"Failed writing payload log: {e}")

    # ENVIA À API
    try:
        r = requests.post(
            API_URL,
            json=payload,
            timeout=20
        )

        if r.status_code == 200:
            logging.info("Data successfully sent to API")
        else:
            logging.error(f"API error {r.status_code}: {r.text}")

    except Exception as e:
        logging.error(f"Failed to send data to API: {e}")
