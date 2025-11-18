from utils.file_utils import load_machines, save_status
from services.scraper_service import scrape_machine

def scrape_all():
    machines = load_machines()
    results = {}

    for machine in machines:
        url = machine["url"]
        results[machine["id"]] = scrape_machine(url)

    save_status(results)
    print("Scrape complete!")

if __name__ == "__main__":
    scrape_all()
