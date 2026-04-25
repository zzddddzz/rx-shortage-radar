import unittest

from rx_shortage_radar.openfda import build_payload


class OpenFDATests(unittest.TestCase):
    def test_build_payload_has_source_summary_and_records(self):
        payload = build_payload(
            {
                "last_updated": "2026-04-24",
                "terms": "https://open.fda.gov/terms/",
                "license": "https://open.fda.gov/license/",
                "disclaimer": "Use responsibly.",
            },
            [
                {
                    "generic_name": "Example Drug Injection",
                    "package_ndc": "1234-5678-90",
                    "status": "Current",
                    "update_date": "04/24/2026",
                    "initial_posting_date": "04/01/2026",
                    "openfda": {"brand_name": ["EXAMPLE"], "rxcui": ["123456"]},
                }
            ],
        )
        self.assertEqual(payload["source"]["last_updated"], "2026-04-24")
        self.assertEqual(payload["summary"]["status_counts"], {"Current": 1})
        self.assertEqual(payload["records"][0]["generic_name"], "Example Drug Injection")


if __name__ == "__main__":
    unittest.main()

