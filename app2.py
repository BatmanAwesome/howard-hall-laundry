import time
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Config
ROOM_IDS = ["8e6bbe77-24ac-49dc-99e9-2e4cb119ba0b", "31e7a700-d31a-4543-8be8-089f2b9302a8"]
CACHE_TIMEOUT = 60  # Only ping CSC GO once every 60 seconds

# Global Cache Storage
cache = {
    "data": [],
    "last_updated": 0
}

def fetch_from_csc():
    """The actual heavy lifting: Talking to CSC GO"""
    combined_list = []
    headers = {"accept": "application/json", "user-agent": "Mozilla/5.0"}
    
    for rid in ROOM_IDS:
        try:
            r = requests.get(f"https://mycscgo.com/api/v3/machine/info/{rid}", headers=headers, timeout=5)
            if r.status_code == 200:
                machines = r.json().get('machines', [])
                combined_list.extend(machines)
        except Exception as e:
            print(f"Fetch error: {e}")
            
    combined_list.sort(key=lambda x: x.get('stickerNumber', 0))
    return combined_list

@app.route('/api/status')
def get_status():
    current_time = time.time()
    
    # Check if cache is old (older than 60 seconds)
    if current_time - cache["last_updated"] > CACHE_TIMEOUT:
        print("Cache expired. Fetching fresh data from CSC GO...")
        cache["data"] = fetch_from_csc()
        cache["last_updated"] = current_time
    else:
        print("Serving data from cache. Saving bandwidth!")

    return jsonify(cache["data"])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # '0.0.0.0' allows other people on your Wi-Fi to visit the site
    app.run(host='0.0.0.0', port=5000)