import unittest

from rx_shortage_radar.normalize import clean_list, normalize_text, parse_us_date, public_shortage_record, status_counts


class NormalizeTests(unittest.TestCase):
    def test_normalize_text_handles_punctuation_and_case(self):
        self.assertEqual(normalize_text("Acetaminophen 325-mg TAB."), "acetaminophen 325 mg tab")

    def test_clean_list_deduplicates_case_insensitively(self):
        self.assertEqual(clean_list(["Tylenol", " tylenol ", "", None, "Mapap"]), ["Tylenol", "Mapap"])

    def test_parse_us_date(self):
        self.assertEqual(parse_us_date("04/25/2026"), "2026-04-25")
        self.assertEqual(parse_us_date("2026-04-25"), "2026-04-25")

    def test_public_shortage_record_keeps_public_search_fields(self):
        raw = {
            "generic_name": "Phenobarbital Tablet",
            "package_ndc": "0603-5167-32",
            "status": "To Be Discontinued",
            "update_date": "10/31/2025",
            "initial_posting_date": "10/31/2025",
            "presentation": "Phenobarbital, Tablet, 64.8 mg",
            "openfda": {
                "brand_name": ["PHENOBARBITAL"],
                "rxcui": ["198086"],
                "product_ndc": ["0603-5167"],
            },
        }
        record = public_shortage_record(raw)
        self.assertEqual(record["update_date"], "2025-10-31")
        self.assertIn("phenobarbital", record["search_text"])
        self.assertEqual(record["rxcuis"], ["198086"])

    def test_status_counts_orders_by_count(self):
        self.assertEqual(status_counts([{"status": "Current"}, {"status": "Resolved"}, {"status": "Current"}]), {"Current": 2, "Resolved": 1})


if __name__ == "__main__":
    unittest.main()

