import unittest
from unittest.mock import Mock, patch

import requests

from app import app
from laundry import LaundryClient, LaundryUnavailable


def response(machines):
    result = Mock()
    result.json.return_value = {"machines": machines}
    return result


class LaundryTests(unittest.TestCase):
    @patch("laundry.requests.get")
    def test_combines_sorts_and_caches_rooms(self, get):
        get.side_effect = [response([
            {"type": "dryer", "available": True, "stickerNumber": 1},
        ]), response([
            {"type": "washer", "available": False, "stickerNumber": 1},
            {"type": "washer", "available": True, "stickerNumber": "10"},
            {"type": "washer", "available": True, "stickerNumber": "2"},
            {"type": "washer", "available": True, "stickerNumber": None},
        ])]
        client = LaundryClient()
        machines = client.get_machines()
        self.assertEqual([m["stickerNumber"] for m in machines], ["2", "10", None, 1, 1])
        self.assertEqual(client.get_machines(), machines)
        self.assertEqual(get.call_count, 2)
        self.assertEqual(get.call_args.kwargs["timeout"], 5)

    @patch("laundry.monotonic")
    @patch("laundry.requests.get")
    def test_failure_throttle_and_recovery(self, get, clock):
        clock.return_value = 100
        get.side_effect = [response([]), requests.Timeout(), response([]), response([])]
        client = LaundryClient()
        with self.assertRaises(LaundryUnavailable):
            client.get_machines()
        with self.assertRaises(LaundryUnavailable):
            client.get_machines()
        self.assertEqual(get.call_count, 2)
        clock.return_value = 161
        self.assertEqual(client.get_machines(), [])
        self.assertEqual(get.call_count, 4)

    @patch("laundry.requests.get")
    def test_rejects_malformed_payloads(self, get):
        for payload in ({}, [], {"machines": [None]}, {"machines": {}}):
            with self.subTest(payload=payload):
                get.return_value = Mock()
                get.return_value.json.return_value = payload
                with self.assertRaises(LaundryUnavailable):
                    LaundryClient().get_machines()

    @patch("laundry.requests.get")
    def test_http_and_json_errors(self, get):
        for error in (requests.HTTPError(), ValueError("Invalid JSON")):
            with self.subTest(error=error):
                get.return_value = Mock()
                if isinstance(error, requests.HTTPError):
                    get.return_value.raise_for_status.side_effect = error
                else:
                    get.return_value.json.side_effect = error
                with self.assertRaises(LaundryUnavailable):
                    LaundryClient().get_machines()

    @patch("laundry.monotonic")
    @patch("laundry.requests.get")
    def test_expired_success_is_not_served_as_fresh_after_failure(self, get, clock):
        clock.return_value = 100
        get.side_effect = [response([{"type": "washer"}]), response([]), requests.Timeout()]
        client = LaundryClient()
        self.assertEqual(len(client.get_machines()), 1)
        clock.return_value = 161
        with self.assertRaises(LaundryUnavailable):
            client.get_machines()

    @patch("app.laundry")
    def test_routes_and_assets(self, laundry):
        client = app.test_client()
        self.assertEqual(client.get("/").status_code, 200)
        for asset in ("dashboard.css", "dashboard.js"):
            with client.get("/static/" + asset) as result:
                self.assertEqual(result.status_code, 200)
        laundry.get_machines.return_value = [{"type": "washer"}]
        result = client.get("/api/status")
        self.assertEqual(result.json, [{"type": "washer"}])
        self.assertEqual(result.headers["Cache-Control"], "no-store")
        laundry.get_machines.side_effect = LaundryUnavailable()
        result = client.get("/api/status")
        self.assertEqual(result.status_code, 503)
        self.assertIn("error", result.json)


if __name__ == "__main__":
    unittest.main()
