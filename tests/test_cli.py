import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from rx_shortage_radar.cli import main


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


if __name__ == "__main__":
    unittest.main()

