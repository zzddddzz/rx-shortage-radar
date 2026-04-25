# Rx Shortage Radar

Rx Shortage Radar is a public FDA drug-shortage dashboard and CLI. It pulls the FDA drug shortage feed from openFDA, normalizes the records for search, and publishes a static web app that can run on GitHub Pages.

This project is intentionally public-safe:

- Uses public FDA/openFDA data only.
- Does not use patient data, hospital inventory, vendor files, or PHI.
- Preserves FDA source metadata and disclaimer in the generated dataset.
- Runs as a static site with no server-side database.

Live site, after GitHub Pages is enabled:

https://zzddddzz.github.io/rx-shortage-radar/

## What It Shows

- Current, resolved, and to-be-discontinued FDA shortage records.
- Drug search across generic name, brand name, RxCUI, NDC, company, route, and therapeutic category.
- Status counts and source freshness.
- A downloadable JSON dataset at `site/data/shortages.json`.

## Quick Start

```bash
python3 -m pip install -e .
rx-shortage-radar refresh --output site/data/shortages.json
rx-shortage-radar serve --root site --port 8765
```

Then open:

```text
http://127.0.0.1:8765/
```

Search from the terminal:

```bash
rx-shortage-radar search phenobarbital
rx-shortage-radar search amoxicillin --status Current
rx-shortage-radar search 0603-5167
```

## Data Source

The generated dataset comes from the public openFDA drug shortages endpoint:

https://api.fda.gov/drug/shortages.json

openFDA documentation:

https://open.fda.gov/apis/drug/drugshortages/

The dataset includes FDA/openFDA metadata fields such as `last_updated`, `terms_url`, `license_url`, and `disclaimer`.

## Automation

This repo includes three GitHub Actions workflows:

- `ci.yml`: runs the Python unit tests.
- `refresh-data.yml`: refreshes `site/data/shortages.json` daily and commits changes.
- `deploy-pages.yml`: deploys the `site/` directory to GitHub Pages.

Optional: set `OPENFDA_API_KEY` as a repository secret if you want higher openFDA rate limits.

## Development

```bash
python3 -m unittest discover -s tests
python3 -m rx_shortage_radar refresh --max-records 25 --output /tmp/shortages.json
```

## Medical Disclaimer

Rx Shortage Radar is for public data exploration and software demonstration only. Do not use it to make medical decisions, clinical decisions, procurement decisions, or patient-care decisions. Confirm all shortage information with authoritative FDA sources, manufacturers, pharmacists, prescribers, and local policies.

