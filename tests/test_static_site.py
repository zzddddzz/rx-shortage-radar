import unittest
from pathlib import Path

class StaticSiteTests(unittest.TestCase):
    def test_dashboard_keyboard_shortcuts_are_wired(self):
        app_js = Path("site/app.js").read_text(encoding="utf-8")
        self.assertIn("function handleKeyboardShortcuts(event)", app_js)
        self.assertIn('event.key === "/"', app_js)
        self.assertIn('event.key === "Escape"', app_js)
        self.assertIn("!isEditableTarget(event.target)", app_js)
        self.assertIn('document.addEventListener("keydown", handleKeyboardShortcuts)', app_js)

    def test_dashboard_search_filtering_is_wired(self):
        app_js = Path("site/app.js").read_text(encoding="utf-8")
        self.assertIn("function filteredRecords()", app_js)
        self.assertIn("function setQuery(value)", app_js)
        self.assertIn('elements.searchInput.addEventListener("input"', app_js)

    def test_dashboard_rxnorm_selection_is_wired(self):
        app_js = Path("site/app.js").read_text(encoding="utf-8")
        self.assertIn("async function resolveRxNorm()", app_js)
        self.assertIn("function renderRxNormPanel(records)", app_js)
        self.assertIn('elements.rxnormButton.addEventListener("click", resolveRxNorm)', app_js)

if __name__ == "__main__":
    unittest.main()