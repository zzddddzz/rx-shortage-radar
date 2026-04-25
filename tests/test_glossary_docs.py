import unittest
from pathlib import Path


class GlossaryDocsTests(unittest.TestCase):
    def test_glossary_covers_required_terms_and_official_links(self):
        glossary = Path("docs/glossary.md").read_text(encoding="utf-8")
        required_terms = [
            "## NDC",
            "## RxCUI",
            "## RxNorm",
            "## openFDA",
            "## Current",
            "## Resolved",
            "## To Be Discontinued",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, glossary)

        required_links = [
            "https://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm",
            "https://www.nlm.nih.gov/research/umls/rxnorm/docs/techdoc.html",
            "https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html",
            "https://www.fda.gov/science-research/health-informatics-fda/openfda",
            "https://open.fda.gov/apis/drug/drugshortages/",
            "https://www.fda.gov/drugs/drug-shortages/frequently-asked-questions-about-drug-shortages",
        ]
        for link in required_links:
            with self.subTest(link=link):
                self.assertIn(link, glossary)

    def test_readme_and_dashboard_link_glossary(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        dashboard = Path("site/index.html").read_text(encoding="utf-8")
        self.assertIn("docs/glossary.md", readme)
        self.assertIn("docs/glossary.md", dashboard)


if __name__ == "__main__":
    unittest.main()

