import json
from pathlib import Path
from multi_scraper import check_machine_status

# single file example --------------------------------------
with open('data/machines.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for machine in data.get('machines', []):           # loop over every element
    #print(machine.get('url'))                      # print url on its own line
    url = machine.get('url')
    print(check_machine_status(url))                       # call function on url