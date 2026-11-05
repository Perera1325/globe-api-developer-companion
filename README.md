# GLOBE API Developer & Data-Quality Companion

An independent, open-source companion for developers integrating with NASA's public
[GLOBE API](https://www.globe.gov/globe-data/globe-api) (`api.globe.gov/search/`). It
provides a documentation dashboard, community-derived response schemas, a local JSON
validator, and a documentation-quality review — all built from public documentation,
with zero live API calls anywhere in the code.

**Not affiliated with, endorsed by, or reviewed by NASA or the GLOBE Program.**

![Dashboard overview](docs/screenshots/dashboard_top.png)

## Why this exists

The GLOBE API's own OpenAPI specification documents its response model as an empty
object — real field names only exist in a 151-page PDF guide, and a few other
inconsistencies exist between the docs page, the guide, and the live spec (full list in
[`docs/EVIDENCE_REGISTER.md`](docs/EVIDENCE_REGISTER.md)). This project turns that
research into something reusable: a reference dashboard, validatable schemas, and a
documented set of pitfalls, instead of everyone re-discovering them independently.

## What's in here

| Path | What it is |
|---|---|
| `dashboard/` | Static, accessible, offline HTML/CSS/JS reference — open `dashboard/index.html` directly in a browser, no server needed |
| `schemas/` | Three community-derived JSON Schemas (measurement response, dev/country/all, dev/lastpublishdate), each flagged where the official spec documents no fields |
| `fixtures/` | Synthetic (non-real) example API responses used to exercise the schemas |
| `validator/validate.py` | Offline Python tool that validates a local JSON file against the schemas |
| `tests/` | Automated pytest suite (8 tests) covering schemas, fixtures, and the validator |
| `docs/ENDPOINTS.md` | Endpoint and parameter reference |
| `docs/DOC_QUALITY_CHECKLIST.md` | 11-point scorecard of the official documentation's own clarity |
| `docs/DEVELOPER_GUIDE.md` | Safe request construction, validation, error handling, pagination, and data-handling guidance |
| `docs/EVIDENCE_REGISTER.md` | Every claim in this project, dated and cited to its source |
| `docs/ARCHITECTURE.md` | How the pieces fit together (with a diagram) |
| `docs/EXECUTIVE_SUMMARY.md` | Two-page summary suitable for sharing as independent developer feedback |

## Setup

Requires Python 3.9+. Use a virtual environment rather than installing into your system
Python:

```bash
# from the repository root
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r validator/requirements.txt pytest

# run the validator against the shipped synthetic fixtures
python3 validator/validate.py

# run the automated test suite
python3 -m pytest tests/ -v

# view the dashboard — just open the file, no server required
open dashboard/index.html        # macOS
xdg-open dashboard/index.html    # Linux
# or double-click dashboard/index.html in Windows Explorer

# when done
deactivate
```

Validate your own JSON file against a schema:

```bash
python3 validator/validate.py path/to/response.json --schema measurement_response
```

## Verified vs. not verified

This project is careful to separate three kinds of claims throughout (see
`docs/EVIDENCE_REGISTER.md` for the full, dated list):

- **Verified documentation facts** — stated directly by an official source.
- **Potential usability improvements** — documentation clarity issues, not security
  claims.
- **Unverified security hypotheses** — raised by a documentation gap (e.g., 401/403
  codes declared with no documented auth scheme), explicitly *not* confirmed by any
  test, and never to be read as a vulnerability finding.

No live request was sent to any NASA/GLOBE system to build this project. The
`dev_country_all` and `dev_lastpublishdate` response schemas are **illustrative and
non-authoritative** — best-effort guesses built only to demonstrate how the validator
pattern works, not confirmed response formats. This labeling is repeated in the schema
files themselves, in the dashboard, and in `docs/EXECUTIVE_SUMMARY.md`, so it's visible
wherever those schemas are referenced.

## Scope & authorization note

NASA's Vulnerability Disclosure Policy lists `nasa.gov`, `usgeo.gov`, `globe.gov`,
`nspires.nasaprs.com`, and `nsc.nasa.gov` as domains eligible for testing *under NASA's
own VDP, by researchers who follow that policy's process* (see
`docs/EVIDENCE_REGISTER.md`, D-017). That published domain list is a separate thing from
any specific host-by-host confirmation a researcher may have received directly from
NASA in private correspondence — the policy's domain list does not itself constitute
such a confirmation for every subdomain under those domains.

This project performs **no testing of any kind** against any host, so no authorization
question actually arises here — this companion is documentation, static files, and a
local validator only. This note exists purely to avoid any reader mistakenly inferring
that this repository grants, implies, or relies on authorization to test any NASA-,
USGEO-, or GLOBE-managed host or subdomain. It does not, and nothing in this project
should be read as such.

## Limitations

- Schemas for the Public Dev API endpoints are unverified guesses (no live response was
  ever observed).
- The measurement-response schema's field list comes from a PDF guide, not the
  machine-readable spec, and may drift from the live API over time.
- The dashboard reflects documentation reviewed on 2026-11-05; the live API may change.
- This project has not been security-reviewed beyond its own (deliberately narrow)
  scope — it validates JSON shape, not API security.

## Contributing / license

Licensed under the MIT License — see [`LICENSE`](LICENSE) for the full text and the
reasoning behind choosing it.

## Status

This repository has **not** been published anywhere, and NASA has **not** been
contacted as part of building it. It exists as a local project pending the
researcher's own review before any publication decision.
