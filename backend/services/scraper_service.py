import requests
from bs4 import BeautifulSoup

def scrape_machine(url: str) -> dict:
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        # TODO: fill in the real selectors after you scan a QR code
        return {
            "status": "unknown",
            "time_remaining": None,
            "raw_html": soup.text[:200]  # temp debug
        }

    except Exception as e:
        return {
            "status": "error",
            "time_remaining": None,
            "error": str(e)
        }
