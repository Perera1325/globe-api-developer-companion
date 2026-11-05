# GLOBE API — Endpoint Reference (Community-Documented)

Source: official docs page, Swagger UI, and both OpenAPI specs, reviewed 2026-11-05.
See `EVIDENCE_REGISTER.md` for exact citations per claim.

## Base

| | |
|---|---|
| Host | `api.globe.gov` |
| Versioned path | `/search/v1/` |
| Swagger UI | `api.globe.gov/search/swagger-ui.html#/` |
| Public API spec | `api.globe.gov/search/v1/api-docs?group=public-api` |
| Public Dev API spec | `api.globe.gov/search/v1/api-docs?group=public-dev-api` |
| Authentication | None documented |
| Result cap | 1,000,000 records per query |

## Public API (`v-1-controller`)

**`GET /v1/measurement/{protocol}/{dateField}/`**

14 documented GET endpoints share this pattern, differing by protocol family. Common
query parameters observed in the live spec:

| Parameter | Type | Notes |
|---|---|---|
| `protocol` | string (enum, 53 values) | e.g. `aerosols`, `land_covers`, `soil_phs` |
| `startdate` / `enddate` | string (date) | date-range filter |
| `countryName` | string | |
| `organizationName` / `organizationId` | string | |
| `siteName` / `siteId` | string | |
| `userid` | string/number | numeric, opaque GLOBE user ID — see `EVIDENCE_REGISTER.md` D-012 |
| `geoJson` / `wkt` | string | polygon-based spatial filter |

Response: declared as the `APIResponse` model, which the spec defines with **no
properties** (see D-011). Field names in the table below come only from the Data User
Guide, not the machine-readable spec — treat them as best-effort, not contractual.

| Field (per Data User Guide) | Guide location |
|---|---|
| `userid` / `userID` | Appendix 1 (p.60), Appendix 2 (p.61) — casing differs between the two |
| site, organization, country, lat/lon fields | Appendix 2 |
| protocol-specific measured values | Appendix 2, varies per protocol |

## Public Dev API (`dev-controller`)

| Method | Path | Purpose (per docs) |
|---|---|---|
| GET | `/dev/country/all/` | All country reference data |
| GET | `/dev/lastpublishdate/` | Last published date for the dataset |

The HTML docs page's broader description ("a list of all countries, places, last
published dates and more") does not match the two endpoints actually defined in the live
spec — see `EVIDENCE_REGISTER.md` D-009.

## Response codes documented (all operations, both groups)

| Code | Documented meaning in spec |
|---|---|
| 200 | Success (`APIResponse`, empty schema) |
| 401 | Unauthorized — **no security scheme is defined anywhere**, see D-010 |
| 403 | Forbidden — same caveat as 401 |
| 404 | Not Found |

Treat 401/403 as **undetermined** rather than confirmed access control. Do not build
retry/backoff logic that assumes these codes are reachable in practice without first
getting NASA's clarification (this project's companion research notebook has an open
question on exactly this).
