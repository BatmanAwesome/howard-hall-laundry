# Howard Hall Laundry Dashboard

A Flask dashboard that displays washer and dryer status from the existing public CSC GO API. Machines are grouped by type, with available machines first and sticker numbers in numeric order. Each section keeps the horizontally scrolling, two-row card layout.

## 🚀 Live Dashboard

Check the current laundry status here: [Dorm Laundry Tracker](https://howard-hall-laundry.onrender.com/)

## Run locally

Requires Python 3.10 or newer.

```sh
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` on Windows PowerShell, or `source .venv/bin/activate` on macOS/Linux. Then:

```sh
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. On Linux, a production entry point is `gunicorn app:app`.

## Project structure

- `app.py`: Flask routes for the dashboard and `/api/status`.
- `laundry.py`: CSC GO requests, room IDs, 60-second cache, and machine sorting.
- `templates/index.html`: dashboard markup.
- `static/dashboard.css` and `static/dashboard.js`: layout, cards, and refresh behavior.
- `tests/test_laundry.py`: mocked API and route tests.

The browser checks every 30 seconds. Each server process caches complete snapshots for 60 seconds, with a five-second timeout per upstream request. Failed refreshes are also throttled for 60 seconds. If either room fails or returns malformed data, `/api/status` returns HTTP 503 instead of a misleading partial or empty list. The browser retains any displayed snapshot and labels it as potentially out of date until recovery. Successful responses remain JSON arrays of CSC GO machine objects.

The two existing dorm room IDs live in `laundry.py`. No credentials, browser automation, database, or local machine inventory is required. Bootstrap styles load from jsDelivr. Upstream availability and the existing undocumented response format remain external dependencies.

The earlier FastAPI backend, HTML/Selenium scrapers, QR inventory, duplicate Flask entry point, and exploratory API scripts have been removed; their history remains in Git.

## Test

```sh
python -m unittest discover -s tests -v
```

Tests use mocked responses and do not contact CSC GO.
