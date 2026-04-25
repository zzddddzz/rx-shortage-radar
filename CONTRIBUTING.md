# Contributing

Thanks for considering a contribution. Rx Shortage Radar is intentionally small: public FDA/openFDA data, public NLM RxNorm APIs, a Python CLI, and a static dashboard.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests
```

Run the dashboard locally:

```bash
rx-shortage-radar refresh --output site/data/shortages.json
rx-shortage-radar serve --root site --port 8765
```

## Contribution Rules

- Use public data only.
- Do not add patient data, hospital data, vendor files, credentials, or private operational paths.
- Do not add non-public scraping, private site automation, or license-restricted data.
- Keep generated data reproducible from public APIs.
- Keep clinical language careful: this project is for public data exploration, not medical advice.
- Add tests when changing Python behavior.
- Verify the static dashboard still loads after UI changes.

If you find a security issue or accidental sensitive-data exposure, follow [SECURITY.md](SECURITY.md) instead of posting sensitive details in a public issue.

## Starter Tasks

Look for issues labeled `good first issue`, or start with one of the tasks in [ROADMAP.md](ROADMAP.md).
