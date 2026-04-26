# Rx Shortage Radar Public GitHub Launch

Project folder: `project/public-github-launch`

## How To Use

1. Read this file first.
2. Pick exactly one unchecked item.
3. Do the work.
4. Add verification details to `VERIFICATION.md`.
5. Update status here immediately.
6. Record classification/exceptions in `DECISIONS.md`.

Status key:

- `[ ]` not started
- `[-]` in progress
- `[x]` done
- `[!]` blocked
- `[~]` explicit exception / keep-as-is

## Done-State

- [x] Create a public-safe health/medicine-related GitHub project.
- [x] Publish the repo, GitHub Pages dashboard, and `v0.1.0` release.
- [x] Add contributor guardrails for public data, PHI avoidance, and private-data reporting.
- [x] Seed contributor-ready issues and respond to first outside activity.
- [ ] Merge the first clean outside contributor PR.
- [ ] Cut `v0.1.1` after the first contributor merge.

## Current Focus

- Current phase: Maintenance
- Next recommended item: Review PR #8 after the contributor updates the local CSV path in the docs example.
- Rule: keep the repo focused on public FDA/openFDA and RxNorm data; do not add private, patient, hospital, vendor, credential, or non-public scraped data.

## Completed Work Already Landed

- [x] Built the initial public FDA shortage dashboard and CLI.
- [x] Added openFDA refresh, normalized JSON output, static dashboard, and unit tests.
- [x] Added RxNorm approximate lookup support and RSS feeds.
- [x] Added README polish, contributor docs, roadmap, issue templates, and starter issues.
- [x] Added CSV export and generated `site/data/shortages.csv`.
- [x] Added status-specific RSS feeds.
- [x] Added dashboard keyboard shortcuts.
- [x] Documented JSON dataset schema and added `docs/shortages.schema.json`.
- [x] Added terminology glossary.
- [x] Added changelog and published release `v0.1.0`.
- [x] Added PR template and `SECURITY.md`.
- [x] Enabled GitHub private vulnerability reporting.
- [x] Added repo topics for discovery, including `openfda`, `drug-shortages`, `healthcare`, `python`, `public-data`, and `rxnorm`.
- [x] Closed duplicate PR #6 politely and pointed contributor toward a better issue.
- [x] Opened #7, #9, and #10 as contributor-friendly tasks.
- [x] Reviewed PR #8 locally and requested one small docs change before merge.

## Phase 0: Inventory And Rules

- [x] Scope is this repo only: `zzddddzz/rx-shortage-radar`.
- [x] In-scope public outputs: GitHub repo, GitHub Pages, releases, issues, PRs, Actions, and generated public data files.
- [x] Out of scope: private local files, browser history, work systems, patient data, hospital data, vendor files, credentials, private paths, and non-public scraping.
- [x] Source APIs allowed by default: public FDA/openFDA drug shortages and public NLM RxNorm.
- [x] Maintainer style: concise, friendly, concrete scope, no overpromising.

## Phase 1: Contributor Flow

- [-] Review and merge PR #8 if the requested docs-path change is made and checks/tests remain clean.
- [ ] Close #7 after PR #8 merges.
- [ ] Comment on #9 or #10 when a contributor asks to claim one, but first verify no existing PR already covers it.
- [ ] After first contributor merge, publish `v0.1.1` with a short changelog entry.

## Phase 2: Product Improvements

- [ ] Implement or review #9: dashboard data freshness badge.
- [ ] Implement or review #10: simple shortage status chart.
- [ ] Consider a small dashboard accessibility pass after chart/freshness changes.
- [ ] Keep generated data format stable unless schema docs and tests are updated together.

## Phase 3: Repository Maintenance

- [ ] Keep issue labels clean: `good first issue`, `help wanted`, `documentation`, and `enhancement`.
- [ ] Keep `SECURITY.md`, PR template, and contribution rules aligned as the project grows.
- [ ] Review GitHub Actions after each merge; fix failures before adding new work.
- [ ] Consider `v0.1.2` only after one or two small useful changes land.

## Lower-Priority Cleanup

- [ ] Add a small "how to cite/source this data" note if users start consuming the dataset.
- [ ] Add screenshots after visible dashboard UI changes.
- [ ] Consider adding lightweight front-end tests if dashboard logic grows.

## Explicit Exceptions

- [~] Do not start a second repo until this repo has absorbed the first contributor PR and one follow-up release.
- [~] Do not rewrite history just to remove public author name metadata; name in license/package metadata was accepted as fine.
- [~] Do not add non-public scraping or private data integrations, even if requested by contributors.

## Inventory Snapshot

| Item | Bucket | Status | Notes |
| --- | --- | --- | --- |
| Public repo | Phase 1 | `[x]` | `https://github.com/zzddddzz/rx-shortage-radar` |
| GitHub Pages | Phase 1 | `[x]` | `https://zzddddzz.github.io/rx-shortage-radar/` |
| Release `v0.1.0` | Phase 1 | `[x]` | Initial public release published. |
| PR #8 | Phase 1 | `[-]` | Usage examples PR; tests pass locally; one docs-path tweak requested. |
| Issue #7 | Phase 1 | `[-]` | Usage examples; should close via PR #8 if merged. |
| Issue #9 | Phase 2 | `[ ]` | Data freshness badge. |
| Issue #10 | Phase 2 | `[ ]` | Status chart. |
| Public-data safety guardrails | Phase 3 | `[x]` | PR template, `SECURITY.md`, contribution rules, private vulnerability reporting. |

## Session Notes

- 2026-04-26: Created tracker after project launch, first external PR activity, and contributor issue seeding.
- Current repo signal snapshot: 2 forks, 0 stars, 0 watchers.
- Current open issues: #7, #9, #10.
- Current open PRs: #8.
- Keep future updates short and dated; record commit hashes and verification in `VERIFICATION.md`.
