# Changelog

All notable changes to Rx Shortage Radar will be documented here.

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

