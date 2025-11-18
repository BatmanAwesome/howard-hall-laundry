from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI()



@app.get("/")
def home():
    return {"message": "API is running!"}

DATA_DIR = Path("../data")
STATUS_FILE = DATA_DIR / "status.json"

@app.get("/machines")
def get_machine_status():
    if not STATUS_FILE.exists():
        return {"error": "No status data found. Run scraper first."}

    with open(STATUS_FILE) as f:
        data = json.load(f)

    return data
