import json
from pathlib import Path

DATA_DIR = Path("../data")
MACHINE_FILE = DATA_DIR / "machines.json"
STATUS_FILE = DATA_DIR / "status.json"

def load_machines():
    with open(MACHINE_FILE) as f:
        return json.load(f)

def save_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f, indent=2)
