import json
import os
import urllib.request
import unittest

BASE = os.environ.get("SERVICE_URL", "http://localhost:8081")


class GivenReportApiTests(unittest.TestCase):
    def test_health(self):
        with urllib.request.urlopen(f"{BASE}/health", timeout=10) as response:
            self.assertEqual(response.status, 200)

    def test_filtered_report_shape(self):
        with urllib.request.urlopen(f"{BASE}/reports?type=reconciliation", timeout=10) as response:
            body = json.load(response)
        self.assertEqual(body["report_type"], "reconciliation")
        self.assertGreater(body["count"], 0)

    def test_version_is_present(self):
        with urllib.request.urlopen(f"{BASE}/version", timeout=10) as response:
            self.assertTrue(json.load(response)["version"])


if __name__ == "__main__":
    unittest.main()
