import json
import os

CACHE_FILE = "/opt/iWebIT_Network_Discovery/cache.json"

def load():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE) as f:
        return json.load(f)

def save(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)
