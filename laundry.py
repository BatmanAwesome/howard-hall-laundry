"""CSC GO access, shared caching, and dashboard ordering."""
import logging
from threading import Lock
from time import monotonic

import requests

ROOM_IDS = (
    "8e6bbe77-24ac-49dc-99e9-2e4cb119ba0b",  # Dryers
    "31e7a700-d31a-4543-8be8-089f2b9302a8",  # Washers
)
API_URL = "https://mycscgo.com/api/v3/machine/info/{}"
logger = logging.getLogger(__name__)


class LaundryUnavailable(Exception):
    """A complete machine snapshot could not be retrieved."""


def machine_sort_key(machine):
    machine_type = str(machine.get("type") or "").lower()
    try:
        sticker = int(machine.get("stickerNumber"))
    except (TypeError, ValueError):
        sticker = 10**9
    return (
        {"washer": 0, "dryer": 1}.get(machine_type, 2),
        0 if machine.get("available") else 1,
        sticker,
    )


class LaundryClient:
    def __init__(self, room_ids=ROOM_IDS, cache_seconds=60):
        self.room_ids = tuple(room_ids)
        self.cache_seconds = cache_seconds
        self._machines = []
        self._next_refresh = 0
        self._failed = False
        self._lock = Lock()

    def get_machines(self):
        # Serialize refreshes so simultaneous visitors share one upstream fetch.
        with self._lock:
            if monotonic() >= self._next_refresh:
                try:
                    machines = self._fetch_machines()
                except (requests.RequestException, ValueError) as exc:
                    logger.warning("CSC GO refresh failed: %s", exc)
                    self._failed = True
                else:
                    self._machines = sorted(machines, key=machine_sort_key)
                    self._failed = False
                self._next_refresh = monotonic() + self.cache_seconds
            if self._failed:
                raise LaundryUnavailable()
            return self._machines

    def _fetch_machines(self):
        machines = []
        for room_id in self.room_ids:
            response = requests.get(
                API_URL.format(room_id),
                headers={"accept": "application/json", "user-agent": "Mozilla/5.0"},
                timeout=5,
            )
            response.raise_for_status()
            payload = response.json()
            room_machines = payload.get("machines") if isinstance(payload, dict) else None
            if not isinstance(room_machines, list) or any(
                not isinstance(machine, dict) for machine in room_machines
            ):
                raise ValueError("Unexpected CSC GO machine response")
            machines.extend(room_machines)
        return machines
