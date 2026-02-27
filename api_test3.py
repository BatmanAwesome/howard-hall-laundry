import requests
import time
import os

# The two Room/Group IDs you discovered
ROOM_IDS = [
    "8e6bbe77-24ac-49dc-99e9-2e4cb119ba0b", # Dryers
    "31e7a700-d31a-4543-8be8-089f2b9302a8"  # Washers
]

HEADERS = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    # If it fails with 401, add "cookie": "your_cookie_here"
}

def fetch_all_machines():
    combined_list = []
    for room_id in ROOM_IDS:
        url = f"https://mycscgo.com/api/v3/machine/info/{room_id}"
        try:
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                # CSC GO puts machines in a list; we extract them here
                machines = data.get('machines', data)
                if isinstance(machines, list):
                    combined_list.extend(machines)
            else:
                print(f"Warning: Room {room_id} returned status {response.status_code}")
        except Exception as e:
            print(f"Error connecting to room {room_id}: {e}")
    return combined_list

def display_dashboard():
    try:
        while True:
            machines = fetch_all_machines()
            
            # Sort by stickerNumber so Washers/Dryers stay in a logical order
            machines.sort(key=lambda x: x.get('stickerNumber', 0))

            # Clear terminal for a 'Live' feel
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("=" * 45)
            print(f"{'ID':<6} | {'TYPE':<10} | {'STATUS'}")
            print("=" * 45)

            for m in machines:
                m_id = m.get('stickerNumber', '???')
                m_type = m.get('type', 'Unknown').upper()
                
                if m.get('available'):
                    status_str = "🟢 FREE"
                else:
                    time_rem = m.get('timeRemaining', 0)
                    if time_rem and time_rem > 0:
                        status_str = f"🔴 {time_rem} mins left"
                    # 2. Check if the controller is Offline
                    elif m.get('mode') == "offline" or m.get('notAvailableReason') == "offline":
                        status_str = "⚪ OFFLINE"
                    
                        
                    else:
                        status_str = f"🔴 BUSY ({m.get('notAvailableReason', 'In Use')})"
                
                print(f"{m_id:<6} | {m_type:<10} | {status_str}")

            print("=" * 45)
            print(f"Last Updated: {time.strftime('%H:%M:%S')}")
            print("Updating in 60 seconds... (Ctrl+C to stop)")
            time.sleep(60)

    except KeyboardInterrupt:
        print("\nDashboard closed.")

if __name__ == "__main__":
    display_dashboard()