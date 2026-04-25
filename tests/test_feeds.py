import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from rx_shortage_radar.feeds import build_rss, write_rss


class FeedTests(unittest.TestCase):
    def sample_payload(self):
        return {
            "generated_at": "2026-04-25T05:00:00+00:00",
            "source": {"docs_url": "https://open.fda.gov/apis/drug/drugshortages/"},
            "records": [
                {
                    "id": "a",
                    "generic_name": "Older Drug",
                    "package_ndc": "1111-2222-33",
                    "status": "Current",
                    "update_date": "2026-01-01",
                },
                {
                    "id": "b",
                    "generic_name": "Newer Drug",
                    "package_ndc": "9999-8888-77",
                    "status": "Resolved",
                    "update_date": "2026-04-24",
                },
            ],
        }

    def test_build_rss_orders_newest_first(self):
        tree = build_rss(self.sample_payload())
        titles = [node.text for node in tree.findall("./channel/item/title")]
        self.assertEqual(titles[0], "Resolved: Newer Drug (9999-8888-77)")

    def test_write_rss_outputs_valid_xml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "feed.xml"
            write_rss(self.sample_payload(), path, status="Current")
            root = ET.parse(path).getroot()
            titles = [node.text for node in root.findall("./channel/item/title")]
            self.assertEqual(titles, ["Current: Older Drug (1111-2222-33)"])


if __name__ == "__main__":
    unittest.main()

