import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from pathlib import Path

from rx_shortage_radar.cli import main
from rx_shortage_radar.rxnorm import RxNormCandidate


class CliTests(unittest.TestCase):
    def test_search_prints_matching_record(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "shortages.json"
            path.write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "generic_name": "Phenobarbital Tablet",
                                "brand_names": ["PHENOBARBITAL"],
                                "status": "Current",
                                "package_ndc": "0603-5167-32",
                                "update_date": "2026-04-24",
                                "search_text": "phenobarbital tablet 0603 5167 32",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["search", "phenobarbital", "--data", str(path)])
            self.assertEqual(exit_code, 0)
            self.assertIn("Phenobarbital Tablet", output.getvalue())
            self.assertIn("1 match", output.getvalue())

    def test_rxnorm_prints_candidates(self):
        output = io.StringIO()
        with patch(
            "rx_shortage_radar.cli.approximate_term",
            return_value=[RxNormCandidate(rxcui="142153", name="Albuterol Sulfate", score=10.9, rank=1, source="RXNORM")],
        ):
            with redirect_stdout(output):
                exit_code = main(["rxnorm", "albutrol sulfate"])
        self.assertEqual(exit_code, 0)
        self.assertIn("142153\tAlbuterol Sulfate", output.getvalue())

    def test_export_csv_writes_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "shortages.json"
            output_path = Path(tmpdir) / "shortages.csv"
            data_path.write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "generic_name": "Albuterol Sulfate Solution",
                                "status": "Current",
                                "package_ndc": "0487-9901-30",
                                "update_date": "2026-04-20",
                                "company_name": "Nephron Pharmaceuticals Corporation",
                                "rxcuis": ["245314"],
                                "source_url": "https://api.fda.gov/drug/shortages.json",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["export-csv", "--data", str(data_path), "--output", str(output_path)])
            self.assertEqual(exit_code, 0)
            self.assertIn("Wrote 1 CSV rows", output.getvalue())
            self.assertIn("Albuterol Sulfate Solution", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
