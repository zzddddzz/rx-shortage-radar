import json
import unittest
from pathlib import Path


class DataSchemaDocsTests(unittest.TestCase):
    def test_machine_readable_schema_matches_generated_payload_shape(self):
        schema = json.loads(Path("docs/shortages.schema.json").read_text(encoding="utf-8"))
        payload = json.loads(Path("site/data/shortages.json").read_text(encoding="utf-8"))

        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(set(schema["required"]), set(payload.keys()))

        record_schema = schema["$defs"]["shortage_record"]
        self.assertEqual(set(record_schema["required"]), set(payload["records"][0].keys()))

    def test_human_docs_include_public_source_and_regeneration_notes(self):
        docs = Path("docs/data-schema.md").read_text(encoding="utf-8")
        self.assertIn("site/data/shortages.json", docs)
        self.assertIn("https://api.fda.gov/drug/shortages.json", docs)
        self.assertIn("regenerated", docs.lower())
        self.assertIn("public FDA/openFDA data", docs)
        self.assertIn("schema_version", docs)
        self.assertIn("records[]", docs)


if __name__ == "__main__":
    unittest.main()

