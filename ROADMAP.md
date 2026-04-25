# Roadmap

This roadmap keeps the project easy to contribute to while staying public-safe. All planned work should continue to use public, non-PHI data sources.

## Good First Issues

- Add keyboard shortcuts for focusing search and clearing filters.
- Add small UI tests for search filtering and RxNorm candidate selection.
- Add a glossary for NDC, RxCUI, openFDA, RxNorm, shortage status, and discontinued status.

## Near-Term Features

- Add a compact drug-detail permalink mode.
- Add trend summaries by therapeutic category.
- Add duplicate grouping so package-level records can be viewed by medication.
- Add optional RxNorm concept detail lookup from selected RxCUIs.
- Add static JSON schema documentation for `site/data/shortages.json`.

## Larger Ideas

- Publish a small Python API for downstream users.
- Add a lightweight browser test workflow for the static dashboard.
- Add historical snapshots so users can see which records changed over time.
- Add an accessibility audit workflow for the dashboard.

## Out of Scope

- Patient-specific or hospital-specific recommendations.
- Inventory or procurement decisioning.
- Vendor integrations.
- Scraping non-public or license-restricted data.
