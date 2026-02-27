from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

ROOM_IDS = [
    "8e6bbe77-24ac-49dc-99e9-2e4cb119ba0b", # Dryers
    "31e7a700-d31a-4543-8be8-089f2b9302a8"  # Washers
]

def get_laundry_data():
    all_machines = []
    headers = {"accept": "application/json", "user-agent": "Mozilla/5.0"}
    
    for rid in ROOM_IDS:
        try:
            r = requests.get(f"https://mycscgo.com/api/v3/machine/info/{rid}", headers=headers)
            if r.status_code == 200:
                machines = r.json().get('machines', [])
                all_machines.extend(machines)
        except:
            pass
    
    # Sort by sticker number
    all_machines.sort(key=lambda x: x.get('stickerNumber', 0))
    return all_machines

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify(get_laundry_data())

if __name__ == '__main__':
    app.run(debug=True, port=5000)