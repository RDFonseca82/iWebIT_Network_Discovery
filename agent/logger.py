import logging
import os

LOG_DIR = "/opt/iWebIT_Network_Discovery/logs"
LOG_FILE = f"{LOG_DIR}/discovery.log"

def setup():
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
