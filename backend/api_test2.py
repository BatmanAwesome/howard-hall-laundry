import requests
import json

api_url = "https://mycscgo.com/api/v3/machine/info/8e6bbe77-24ac-49dc-99e9-2e4cb119ba0b"

headers = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def check_for_washers():
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return

        data = response.json()
        # In case the list is wrapped in a key like 'machines' or 'items'
        machines = data.get('machines', data)

        print(f"Found {len(machines)} total top-level items.")
        print("-" * 30)

        for m in machines:
            m_id = m.get('stickerNumber')
            m_type = m.get('type')
            has_stack = "YES" if m.get('stackItems') else "NO"
            
            print(f"ID: {m_id} | Type: {m_type} | Has Stacked Item: {has_stack}")
            
            # If there IS a stack, let's see what's inside it
            if m.get('stackItems'):
                for sub_item in m['stackItems']:
                    print(f"   ---> STACKED ID: {sub_item.get('stickerNumber')} | Type: {sub_item.get('type')}")

    except Exception as e:
        print(f"Fail: {e}")

if __name__ == "__main__":
    check_for_washers()