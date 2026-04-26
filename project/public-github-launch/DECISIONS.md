# Rx Shortage Radar Public GitHub Launch Decisions

Created on `2026-04-26`

## Classification Rules

- `Phase 1`: contributor/release work that directly affects the public launch.
- `Phase 2`: small product improvements that make the dashboard more useful.
- `Phase 3`: repository maintenance, contributor hygiene, and operational guardrails.
- `Exception`: explicit keep-as-is or do-not-do cases.

## Current Decisions

- 2026-04-26: Keep strengthening `rx-shortage-radar` before starting another repo. One active maintained repo with real contributor activity is more valuable than multiple thin repos.
- 2026-04-26: Treat public FDA/openFDA and NLM RxNorm as approved data sources.
- 2026-04-26: Treat patient data, hospital inventory, vendor files, credentials, local private paths, and non-public scraping as out of scope.
- 2026-04-26: Keep maintainer replies friendly but specific. Confirm the contributor can proceed, define scope, and keep safety language concise.
- 2026-04-26: Before telling someone to work on an issue, check whether a PR already exists for it. This avoids duplicate contributor work.
- 2026-04-26: PR #8 should be reviewed first for #7 because it already implements the usage examples. Later interest in #7 should be redirected to #9 or #10.
- 2026-04-26: Do not merge duplicate docs pages when canonical docs already exist. Close duplicates politely and point contributors to active tasks.
- 2026-04-26: Use small releases after meaningful public changes. Next expected release is `v0.1.1` after a clean contributor PR merge.

## Contribution Rules

- Use public repo files and public API URLs only.
- Avoid credentials, tokens, cookies, private certificates, PHI, patient records, hospital data, vendor files, private paths, and non-public scraping.
- Prefer standard-library examples and low-dependency changes for `good first issue` tasks.
- Keep dashboard UI changes accessible and responsive.
- Require tests or an explicit note when a contributor could not run them.

## Update Rule

If a file/task changes bucket, add a new dated note with:

- old bucket
- new bucket
- why the classification changed
