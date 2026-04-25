import csv
import tempfile
import unittest
from pathlib import Path

from rx_shortage_radar.csv_export import CSV_COLUMNS, csv_rows, write_csv


class CsvExportTests(unittest.TestCase):
    def sample_payload(self):
        return {
            "records": [
                {
                    "generic_name": "Albuterol Sulfate Solution",
                    "status": "Current",
                    "package_ndc": "0487-9901-30",
                    "update_date": "2026-04-20",
                    "company_name": "Nephron Pharmaceuticals Corporation",
                    "rxcuis": ["245314"],
                    "brand_names": ["ALBUTEROL SULFATE"],
                    "product_ndcs": ["0487-9901"],
                    "therapeutic_categories": ["Pulmonary/Allergy", "Pediatric"],
                    "dosage_form": "Solution",
                    "source_url": "https://api.fda.gov/drug/shortages.json",
                },
                {
                    "generic_name": "Older Drug",
                    "status": "Resolved",
                    "package_ndc": "1111-2222-33",
                },
            ]
        }

    def test_csv_rows_serializes_stable_public_fields(self):
        rows = csv_rows(self.sample_payload()["records"], status="Current")
        self.assertEqual(list(rows[0].keys()), CSV_COLUMNS)
        self.assertEqual(rows[0]["generic_name"], "Albuterol Sulfate Solution")
        self.assertEqual(rows[0]["rxcuis"], "245314")
        self.assertEqual(rows[0]["therapeutic_categories"], "Pulmonary/Allergy; Pediatric")

    def test_write_csv_outputs_header_and_filtered_rows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "shortages.csv"
            output_path, count = write_csv(self.sample_payload(), path, status="Current")
            self.assertEqual(output_path, path)
            self.assertEqual(count, 1)
            with path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["package_ndc"], "0487-9901-30")
            self.assertEqual(rows[0]["company_name"], "Nephron Pharmaceuticals Corporation")


if __name__ == "__main__":
    unittest.main()

