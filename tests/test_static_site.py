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

    def test_dashboard_category_summary_is_accessible_and_safety_labeled(self):
        index_html = Path("site/index.html").read_text(encoding="utf-8")
        app_js = Path("site/app.js").read_text(encoding="utf-8")
        compact_html = " ".join(index_html.split())

        self.assertIn('aria-labelledby="category-summary-title"', index_html)
        self.assertIn('aria-live="polite"', index_html)
        self.assertIn("Matching shortage groups", compact_html)
        self.assertIn("category totals are non-additive", compact_html)
        self.assertIn("does not imply therapeutic interchangeability", compact_html)
        self.assertIn("do not indicate severity or criticality", compact_html)
        self.assertIn("function renderCategorySummary(records)", app_js)
        self.assertIn("CategorySummary.summarizeTherapeuticCategories(records)", app_js)
        self.assertIn("renderCategorySummary(records)", app_js)

    def test_dashboard_counts_distinguish_records_from_matching_groups(self):
        app_js = Path("site/app.js").read_text(encoding="utf-8")

        self.assertIn('const recordLabel = count === 1 ? "FDA record" : "FDA records"', app_js)
        self.assertIn("matching ${groupLabel}", app_js)
        self.assertNotIn("displayed ${groupLabel}", app_js)

    def test_dashboard_category_loading_state_clears_on_fetch_error(self):
        app_js = Path("site/app.js").read_text(encoding="utf-8")

        self.assertIn('elements.categoryGroupCount.textContent = "Unavailable"', app_js)
        self.assertIn("elements.categorySummaryList.replaceChildren()", app_js)
        self.assertIn(
            'elements.categorySummaryEmpty.textContent = "Therapeutic categories could not be loaded."',
            app_js,
        )

    def test_dashboard_category_summary_scripts_load_in_dependency_order(self):
        index_html = Path("site/index.html").read_text(encoding="utf-8")

        helper_position = index_html.index('<script src="category-summary.js"></script>')
        app_position = index_html.index('<script src="app.js"></script>')
        self.assertLess(helper_position, app_position)

if __name__ == "__main__":
    unittest.main()
