# Security Policy

Rx Shortage Radar is a public-data project. It should not contain patient data, hospital inventory, vendor files, credentials, PHI, private operational paths, or non-public scraped data.

## Reporting a Security or Data Exposure Issue

Please do not open a public GitHub issue that contains secrets, PHI, credentials, private files, screenshots of private systems, or other sensitive details.

If you find a possible security issue or accidental sensitive-data exposure:

1. Use GitHub's private vulnerability reporting flow if it is available for this repository.
2. If private reporting is not available, open a public issue titled `Security contact request` with no sensitive details so a maintainer can coordinate a private channel.
3. If the issue involves a credential or token, rotate or revoke it immediately. Removing it from Git history is not enough once it has been published.

## Public Data Boundary

Allowed project data sources include:

- FDA/openFDA public drug shortage data.
- NLM RxNorm public API responses.
- Other public, redistributable datasets that are clearly documented and compatible with the repository license and purpose.

Do not submit:

- Patient records or PHI.
- Hospital, pharmacy, or vendor operational files.
- Private inventory, procurement, pricing, or dispensing data.
- Credentials, API keys, tokens, cookies, or private certificates.
- Local machine paths, screenshots, logs, or exports that reveal private environments.
- Non-public scraping or license-restricted data.

## Scope

This policy covers the code, generated public datasets, documentation, GitHub Actions workflows, GitHub Pages output, issues, pull requests, and release artifacts in this repository.
