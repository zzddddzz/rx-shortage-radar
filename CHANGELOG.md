# Changelog

All notable changes to Rx Shortage Radar will be documented here.

## v0.2.0 - 2026-08-03

Community-maintained dashboard and contributor-readiness release.

### Added

- Dashboard grouping by medication, manufacturer, and shortage status.
- Aggregated brand names, RxCUIs, package and product NDCs, dosage forms, routes, therapeutic categories, and related information in grouped results.
- Accurate unique-package and FDA source-record counts for each group.
- Dashboard wiring tests for search and RxNorm interactions.
- CSV and JSON dataset usage examples.
- Community health files and public-data contribution guardrails.

### Changed

- Grouped records retain the earliest initial posting date and latest update date.
- Search results now show compact medication/manufacturer groups while the downloadable public data remains unchanged.

### Community

- [CrepuscularIRIS](https://github.com/CrepuscularIRIS) contributed the CSV and JSON usage examples in [#8](https://github.com/zzddddzz/rx-shortage-radar/pull/8).
- [Dibyanshu Mishra](https://github.com/dibyanshumishra) contributed dashboard tests in [#11](https://github.com/zzddddzz/rx-shortage-radar/pull/11) and medication grouping in [#12](https://github.com/zzddddzz/rx-shortage-radar/pull/12).

### Safety

- The grouped dashboard continues to use only the existing public FDA/openFDA and NLM RxNorm data.
- No patient, hospital, vendor, credential, or private operational data was added.

## v0.1.0 - 2026-04-25

Initial public release.

### Added

- Static FDA drug-shortage dashboard backed by public openFDA data.
- Python CLI for refresh, search, RxNorm approximate matching, RSS generation, CSV export, and local serving.
- Daily GitHub Actions refresh for JSON, CSV, and RSS outputs.
- GitHub Pages deployment.
- Downloadable public datasets:
  - `site/data/shortages.json`
  - `site/data/shortages.csv`
- RSS feeds:
  - `site/feed.xml`
  - `site/feed-current.xml`
  - `site/feed-resolved.xml`
  - `site/feed-discontinued.xml`
- RxNorm-assisted dashboard search for misspelled or free-text medication names.
- Dashboard keyboard shortcuts:
  - `/` focuses search.
  - `Escape` clears search.
- Public-safe documentation:
  - README with live demo links and screenshot.
  - Contributor guide.
  - Roadmap.
  - JSON dataset schema docs.
  - Machine-readable JSON Schema.
  - Terminology glossary.

### Safety

- Uses public FDA/openFDA and NLM RxNorm APIs only.
- Does not use patient data, hospital inventory, vendor files, credentials, or private operational paths.
- Includes medical-disclaimer language in the README, dashboard, and docs.
