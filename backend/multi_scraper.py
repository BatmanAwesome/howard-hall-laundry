from bs4 import BeautifulSoup

def check_machine_status(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    machines_data = []

    # CSC GO usually wraps machines in cards or specific grid items
    # We look for the common 'machine-card' or 'machine-container' patterns
    machine_elements = soup.find_all('div', class_='machine-card') 
    
    # If the above class doesn't match your specific local DOM, 
    # we can fall back to searching for text patterns.
    if not machine_elements:
        # Searching for divs that contain machine-related text
        machine_elements = soup.find_all('div', {'data-machine-id': True})

    for machine in machine_elements:
        # 1. Get Machine Number
        # Often in a header or a span with a specific class
        num_tag = machine.find(['span', 'div', 'h5'], class_='machine-number')
        m_number = num_tag.get_text(strip=True) if num_tag else "Unknown"

        # 2. Get Machine Type (Washer/Dryer)
        # Usually identified by text or an icon class
        m_text = machine.get_text().lower()
        if 'washer' in m_text:
            m_type = 'Washer'
        elif 'dryer' in m_text:
            m_type = 'Dryer'
        else:
            m_type = 'Unknown'

        # 3. Get Status (Free or Time Remaining)
        status_tag = machine.find('div', class_='machine-status')
        status_text = status_tag.get_text(strip=True).lower() if status_tag else ""
        
        if 'available' in status_text or 'free' in status_text:
            status = 'Free'
        else:
            # Extract numbers for time remaining (e.g., "25 min left")
            import re
            time_match = re.search(r'(\d+)\s*min', status_text)
            status = f"{time_match.group(1)} mins remaining" if time_match else status_text

        machines_data.append({
            "number": m_number,
            "type": m_type,
            "status": status
        })

    return machines_data

# Example usage with your DOM:
# data = parse_laundry_info(your_html_string)
# print(data)