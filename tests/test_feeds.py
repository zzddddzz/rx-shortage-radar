import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from rx_shortage_radar.feeds import build_rss, write_rss, write_status_feeds


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
            self.assertEqual(root.findtext("./channel/title"), "Rx Shortage Radar - Current")
            self.assertEqual(titles, ["Current: Older Drug (1111-2222-33)"])

    def test_write_status_feeds_outputs_expected_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = write_status_feeds(self.sample_payload(), tmpdir)
            self.assertEqual(set(paths), {"Current", "Resolved", "To Be Discontinued"})

            current_root = ET.parse(paths["Current"]).getroot()
            resolved_root = ET.parse(paths["Resolved"]).getroot()
            discontinued_root = ET.parse(paths["To Be Discontinued"]).getroot()

            self.assertEqual(current_root.findtext("./channel/item/title"), "Current: Older Drug (1111-2222-33)")
            self.assertEqual(resolved_root.findtext("./channel/item/title"), "Resolved: Newer Drug (9999-8888-77)")
            self.assertEqual(discontinued_root.findall("./channel/item"), [])
            self.assertEqual(paths["To Be Discontinued"].name, "feed-discontinued.xml")


if __name__ == "__main__":
    unittest.main()
