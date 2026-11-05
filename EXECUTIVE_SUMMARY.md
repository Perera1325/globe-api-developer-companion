# Executive Summary — GLOBE API Developer & Data-Quality Companion

**Prepared by:** Vinod Ravindu Perera (independent researcher)
**Date:** 2026-11-05
**Subject:** Documentation review and open-source developer tooling for the public NASA
GLOBE API (`api.globe.gov/search/`)

---

## Purpose

This is unsolicited, independent developer feedback on the **public documentation** of
the GLOBE API, packaged as a small open-source companion project: a reference dashboard,
a set of community-derived JSON Schemas, a local response validator, and a documentation-
quality checklist. It is intended to help other developers integrate with the API more
reliably, and to give the GLOBE documentation team a concrete, evidence-backed list of
gaps they may want to close.

**This is not a security assessment.** No live requests were sent to any NASA or GLOBE
system to produce it; every claim comes from reading publicly available pages and
specifications. Six documentation observations are flagged as open questions rather than
findings — see below.

## What was reviewed

- The GLOBE API documentation page and its worked example
- The GLOBE Data User Guide v3.0 (Appendices 1 and 2)
- Both live OpenAPI specifications (Public API and Public Dev API groups)
- The GLOBE privacy policy page
- The NASA Vulnerability Disclosure Policy (for scope/conduct, not as an API reference)

Full citations with dates are in `docs/EVIDENCE_REGISTER.md`.

**Note on scope:** this project performs no testing of any kind against any NASA-,
USGEO-, or GLOBE-managed host. The NASA VDP Policy domain list (reviewed only for its
scope/conduct rules, not as an API reference) describes what NASA's own published policy
treats as eligible for testing under that program — it is a separate matter from any
specific host-by-host confirmation a researcher might separately receive from NASA in
writing, and nothing in this project should be read as claiming or relying on either
form of authorization.

## What was built

| Deliverable | What it does |
|---|---|
| `dashboard/` | A static, accessible, offline web page summarizing documented endpoints, parameters, and common integration pitfalls |
| `schemas/` | Three JSON Schemas reconstructed from the Data User Guide, each explicitly flagged where the official OpenAPI spec itself documents no fields |
| `fixtures/` | Synthetic (non-real) example responses used to exercise the schemas |
| `validator/validate.py` | A local, offline tool that checks a JSON file against these schemas |
| `tests/` | An 8-test automated suite (pytest) covering the schemas, fixtures, and validator, run entirely against local files |
| `docs/DOC_QUALITY_CHECKLIST.md` | An 11-point scorecard of the official documentation's own clarity and internal consistency |
| `docs/DEVELOPER_GUIDE.md` | Practical guidance on request construction, input/response validation, error handling, pagination awareness, and responsible data handling |

Two of the three schemas (`dev_country_all`, `dev_lastpublishdate`) are **illustrative
and non-authoritative** — best-effort guesses, since no live request was made to either
endpoint and the official spec documents no response fields for them. This is stated on
the schema files themselves, in the dashboard, and in the README.

## Top findings (documentation quality, not security)

1. **No response schema is machine-documented.** The OpenAPI spec's `APIResponse` model
   is an empty object; real field names exist only in a PDF guide, invisible to any
   code-generation or contract-testing tooling that reads the spec.
2. **401/403 are declared without any documented authentication mechanism.** This is
   confusing for integrators and is flagged as an open question, not a vulnerability.
3. **Two internal inconsistencies** were found between the HTML docs, the PDF guide, and
   the live spec (a "places" endpoint that doesn't exist in the spec; mismatched example
   dates in the docs page's own prose).
4. **Field-name casing is inconsistent** within the same PDF guide (`userID` vs.
   `userid`).
5. **No guidance exists** on what the `userid` field contains for measurements submitted
   via a student account — a privacy-adjacent gap in an otherwise clear privacy policy.

## Findings at a glance

| Observation | Evidence ID | Suggested documentation improvement | Developer benefit | Verification status |
|---|---|---|---|---|
| Response model (`APIResponse`) is an empty schema in both OpenAPI specs | D-011 | Publish the Data User Guide's field definitions directly in the OpenAPI spec | Spec-driven tooling (codegen, contract tests) would see real field names | Verified documentation fact |
| 401/403 declared on every operation with no documented auth scheme | D-010 | Either remove the 401/403 declarations or document the actual auth boundary (if any) | Removes ambiguity about whether error-handling code for auth failures is needed | Unverified security hypothesis — not a vulnerability claim |
| "Places" capability described in HTML docs, absent from live spec | D-009 | Update the HTML docs page to match the live spec, or add the missing endpoint | Prevents developers building against a non-existent endpoint | Potential usability improvement |
| Field casing differs between guide appendices (`userID` vs `userid`) | D-013 | Standardize casing across the guide | Reduces copy-paste bugs when referencing the field by name | Potential usability improvement |
| Worked example's prose date range doesn't match its own example URL | D-006 | Correct the prose to match the example URL (or vice versa) | Prevents a developer copying a misleading example | Potential usability improvement |
| 16 PDF-documented fields absent from the machine-readable spec | D-016 | Same fix as D-011 — sync the spec with the guide | A spec-only integration would otherwise silently miss these fields | Potential usability improvement |
| `userid` meaning for student-submitted records is undocumented | D-014 | Add a sentence to the Data User Guide or privacy page covering this case | Clarifies a privacy-adjacent edge case for anyone handling student data | Unverified security hypothesis — not a vulnerability claim |

## What still needs human review

- Whether NASA/GLOBE consider any of the five findings above worth a documentation
  update (this project makes no claim about priority or severity from NASA's side).
- Whether the 401/403-without-auth-scheme observation reflects an actual access-control
  boundary — this requires NASA's own confirmation, not further probing by this project.
- Legal/licensing review before any public GitHub publication (this project has not been
  published; see Safety Boundaries below).
- A native speaker/accessibility reviewer pass on the dashboard beyond the automated
  structural checks already applied (semantic HTML, skip link, focus states, reduced-
  motion and light/dark support).

## Safety boundaries honored

No scanning, fuzzing, enumeration, or authentication-bypass testing was performed. No
requests were sent to protected or undocumented endpoints. No GLOBE data was created,
modified, or read from a live system. No vulnerability is claimed, and no claim is made
that NASA has reviewed or endorsed this project. This project has **not** been published
to any public repository, and NASA has **not** been contacted as part of this work.
