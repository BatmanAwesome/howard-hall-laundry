import requests
import json

# The endpoint you found in the Network tab
api_url = "https://mycscgo.com/api/v3/machine/info/8e6bbe77-24ac-49dc-99e9-2e4cb119ba0b"

headers = {
    "accept": "application/json",
    "referer": "https://mycscgo.com/laundry/started/8e6bbe77-24ac-49dc-99e9-2e4cb119ba0b",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    # Note: If this fails with a 401, copy the 'cookie' line from your DevTools 
    # and paste it here: "cookie": "ajs_anonymous_id=..."
}

def get_laundry_data():
    try:
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # The CSC GO API usually returns a list of machines under a key
            # like 'machines', 'items', or just the root list.
            # I'll assume it's 'machines' based on their common structure.
            machines = data.get('machines', data) 
            
            if isinstance(machines, list):
                print(f"{'ID':<10} | {'Type':<10} | {'Status'}")
                print("-" * 40)
                for m in machines:
                    # 1. Get the machine number (stickerNumber is 405 in your example)
                    m_num = m.get('stickerNumber', '???')
                    
                    # 2. Get the machine type (dryer/washer)
                    m_type = m.get('type', 'Unknown')
                    
                    # 3. Handle the Status logic using the 'available' boolean
                    is_available = m.get('available') # This is True or False
                    
                    if is_available:
                        display_status = "FREE"
                    else:
                        # Get timeRemaining (36 in your example)
                        time_val = m.get('timeRemaining')
                        if time_val is not None and time_val > 0:
                            display_status = f"{time_val} mins left"
                        else:
                            # If available is false but time is 0, it might be 'ending' or 'offline'
                            reason = m.get('notAvailableReason', 'In Use')
                            display_status = f"Busy ({reason})"

                    print(f"{m_num:<10} | {m_type:<10} | {display_status}")
            else:
                # If it's not a list, print the raw JSON to see what we got
                print("Unexpected data format. Raw JSON:")
                print(json.dumps(data, indent=2))
                
        else:
            print(f"Server returned status: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_laundry_data()