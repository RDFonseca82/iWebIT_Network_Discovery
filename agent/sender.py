import json
import requests
import logging

API_URL = "https://agent.iwebit.app/scripts/script_network_discovery.php"

def send(id_company, devices):
    payload = {
        "IdCompany": id_company,
        "Devices": devices
    }

    try:
        r = requests.post(
            API_URL,
            json=payload,
            timeout=15
        )

        if r.status_code == 200:
            logging.info("Data successfully sent to API")
        else:
            logging.error(
                f"API error {r.status_code}: {r.text}"
            )

    except Exception as e:
        logging.error(f"Failed to send data to API: {e}")
