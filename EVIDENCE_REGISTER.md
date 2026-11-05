# Evidence Register

All entries below are from **passive review of public documentation only**. No live API
requests were sent to any NASA/GLOBE system to produce this register. Dates are the date
the source was reviewed for *this* project (2026-11-05).

Three categories are used throughout this project, consistently:

- **Verified documentation fact** — the cited page/spec states this directly.
- **Potential usability improvement** — a documentation or developer-experience issue,
  not a security claim.
- **Unverified security hypothesis** — a possibility raised by a documentation gap, not
  confirmed by any test, and not to be read as a vulnerability finding.

| ID | Category | Observation | Source | Date reviewed |
|----|----|----|----|----|
| D-001 | Verified documentation fact | Base host `api.globe.gov`, versioned path `/search/v1/`; example call `GET /search/v1/measurement/protocol/measureddate/`. | https://www.globe.gov/globe-data/globe-api | 2026-11-05 |
| D-002 | Verified documentation fact | Public API covers measurement data queries filtered by protocol and date field/range. Public Dev API is reached via the "public-api" selector box, switched to "public-dev-api". | https://www.globe.gov/globe-data/globe-api | 2026-11-05 |
| D-003 | Verified documentation fact | The docs page does not mention API keys, tokens, or any authentication requirement. | https://www.globe.gov/globe-data/globe-api | 2026-11-05 |
| D-004 | Verified documentation fact | Swagger UI at `api.globe.gov/search/swagger-ui.html#/`. The page does not separately link a raw OpenAPI/JSON spec file (the spec URLs below were found via the Swagger UI's own network calls, not a documented link). | https://www.globe.gov/globe-data/globe-api | 2026-11-05 |
| D-005 | Verified documentation fact | Query results are capped at 1,000,000 records per query; the docs recommend using "Request URL" rather than "Try it out" for bulk access. | https://www.globe.gov/globe-data/globe-api | 2026-11-05 |
| D-006 | Potential usability improvement | The docs page's prose states a date range as "1 January 2020 to 1 January 2012" while the worked example URL uses 2010-01-01 to 2012-01-02 — the prose and the example don't match, which can mislead a developer copying the example. | https://www.globe.gov/globe-data/globe-api | 2026-11-05 |
| D-007 | Verified documentation fact | Public API (`v-1-controller` tag): 14 documented `GET` endpoints under `/v1/measurement/...`; filterable by protocol (53-value enum), date range, country, GLOBE team, lat/lon, organization, site, polygon (GeoJSON/WKT), and user ID. | https://api.globe.gov/search/v1/api-docs?group=public-api (reviewed via Swagger UI, 2026-11-05) | 2026-11-05 |
| D-008 | Verified documentation fact | Public Dev API (`dev-controller` tag): 2 documented `GET` endpoints — `/dev/country/all/` and `/dev/lastpublishdate/`. | https://api.globe.gov/search/v1/api-docs?group=public-dev-api (reviewed via Swagger UI, 2026-11-05) | 2026-11-05 |
| D-009 | Potential usability improvement | The HTML docs page describes the Public Dev API as covering "a list of all countries, places, last published dates and more," but the live spec defines only the two endpoints in D-008 — no "places" endpoint exists in the current spec. | https://www.globe.gov/globe-data/globe-api vs. the public-dev-api spec | 2026-11-05 |
| D-010 | Unverified security hypothesis | Both OpenAPI specs declare `401 Unauthorized` and `403 Forbidden` as possible responses on every documented operation, yet no security scheme (API key, OAuth, Basic Auth) is defined anywhere in either spec or in the HTML docs. This could be an undocumented auth boundary, or generic framework/tooling boilerplate. Not resolved by documentation alone. **Not a confirmed vulnerability.** | Both OpenAPI spec URLs above | 2026-11-05 |
| D-011 | Verified documentation fact | Both specs define their response model (`APIResponse`) as an empty object schema — i.e., the specification itself documents no response field names. This is a documentation gap, not evidence that actual responses are empty (no live requests were made). | Both OpenAPI spec URLs above | 2026-11-05 |
| D-012 | Verified documentation fact | The GLOBE Data User Guide v3.0 (Nov 2025), Appendix 2, p.61, explicitly defines `<protocol>:userid` as "the numerical GLOBE user-id of the person that submitted the measurement" — a numeric, opaque identifier, not a username or email. | GLOBE Data User Guide v3.0, Appendix 2, p.61 | 2026-11-05 |
| D-013 | Potential usability improvement | Appendix 1 (API Metadata, p.60) spells the field `userID`; Appendix 2 (p.61) spells it `userid`. Same guide, inconsistent casing. | GLOBE Data User Guide v3.0, pp.60–61 | 2026-11-05 |
| D-014 | Unverified security hypothesis | What the `userid` field contains for a measurement submitted via a GLOBE student account (teacher's ID, a placeholder, or something else) is not documented in the Data User Guide, either OpenAPI spec, or the GLOBE privacy page. | Absence across all four sources reviewed | 2026-11-05 |
| D-015 | Verified documentation fact | GLOBE's privacy page states student-account data is associated with the school's name and the teacher's account, not the individual student, and that home addresses/emails are never exposed with measurement data. | https://www.globe.gov/en/about/policies/privacy | 2026-11-05 |
| D-016 | Potential usability improvement | 16 response field names documented in the PDF guide have no corresponding declaration in the machine-readable OpenAPI spec (which declares an empty response schema, see D-011) — a developer reading only the spec would not discover these fields. | Data User Guide vs. both OpenAPI specs | 2026-11-05 |
| D-017 | Verified documentation fact | NASA VDP Policy, "Scope" section: "Testing is only authorized on the targets listed as in scope... Any service not expressly listed above... [is] not authorized for testing." In-scope domains: `nasa.gov`, `usgeo.gov`, `globe.gov`, `nspires.nasaprs.com`, `nsc.nasa.gov`. | https://www.nasa.gov/vulnerability-disclosure-policy/ | 2026-11-05 |
| D-018 | Verified documentation fact | NASA VDP Policy, "Guidelines" section: "If a non-production or public test environment is available, all testing must be performed exclusively in that environment," and exploitation must be limited to "the extent necessary to confirm the presence of a vulnerability" — no data exfiltration, persistence, or pivoting. | https://www.nasa.gov/vulnerability-disclosure-policy/ | 2026-11-05 |

### Note on D-017 — policy domain list vs. a specific confirmation

D-017's domain list (`nasa.gov`, `usgeo.gov`, `globe.gov`, `nspires.nasaprs.com`,
`nsc.nasa.gov`) is what the **published policy** states is eligible for testing under
NASA's own VDP process. That is a different thing from any specific host-by-host
confirmation a researcher may separately receive from NASA in written correspondence —
the published list does not by itself confirm every subdomain under those domains is in
scope, and it is not a substitute for a direct confirmation where one is needed. This
project performs no testing of either kind, so this note is recorded for clarity only,
not because a scope decision was required here.

## What this project does NOT claim

- It does not claim any of the D-010 / D-014 unverified hypotheses represent an actual
  vulnerability or privacy failure.
- It does not claim NASA or the GLOBE Program has reviewed, endorsed, or approved this
  project.
- It does not claim the best-effort response schemas in `schemas/` are authoritative —
  they are illustrative, non-authoritative reconstructions for local validation and
  learning, clearly flagged as such via each schema's `x-documentation-gap` field.
- It does not claim, imply, or rely on authorization to test any host or subdomain
  beyond what is stated in D-017/D-018 above — and in fact performs no testing of any
  kind against any host.
