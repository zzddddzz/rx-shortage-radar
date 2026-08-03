# Roadmap

This roadmap keeps the project easy to contribute to while staying public-safe. All planned work should continue to use public, non-PHI data sources.

## Good First Issues

- [Add a data freshness badge](https://github.com/zzddddzz/rx-shortage-radar/issues/9).
- [Add a shareable permalink for selected medication groups](https://github.com/zzddddzz/rx-shortage-radar/issues/15).

## Near-Term Features

- [Add a therapeutic-category summary for filtered results](https://github.com/zzddddzz/rx-shortage-radar/issues/17).
- Add optional RxNorm concept detail lookup from selected RxCUIs.

## Quality and Accessibility

- [Add a browser regression test for medication grouping](https://github.com/zzddddzz/rx-shortage-radar/issues/16).
- Add an accessibility audit workflow for the dashboard.

## Larger Ideas

- Publish a small Python API for downstream users.
- Add historical snapshots so users can see which records changed over time.

## Completed

- Added keyboard shortcuts for focusing search and clearing filters.
- Added dashboard wiring tests for search filtering and RxNorm interactions.
- Grouped package-level records by medication, manufacturer, and status in `v0.2.0`.

## Out of Scope

- Patient-specific or hospital-specific recommendations.
- Inventory or procurement decisioning.
- Vendor integrations.
- Scraping non-public or license-restricted data.
