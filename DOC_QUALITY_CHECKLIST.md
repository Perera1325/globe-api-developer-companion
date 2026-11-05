# Documentation-Quality Checklist — GLOBE API

A review of NASA GLOBE's *public documentation itself* (not the API's behavior), scored
against standard API-documentation criteria. Each row cites the evidence register entry
backing it.

| Criterion | Status | Notes | Evidence |
|---|---|---|---|
| Authentication requirements described, if any apply | ⚠️ Gap | No auth is documented, but 401/403 are declared as possible responses on every operation — contradictory signal, not resolved by docs. | D-010 |
| Parameters clearly named and typed | ✅ Mostly clear | Query parameters in the live spec are typed and named; the enum of 53 protocols is explicit. | D-007 |
| Response schema documented in the machine-readable spec | ❌ Missing | `APIResponse` is an empty object schema in both OpenAPI specs; no field names are machine-documented. | D-011 |
| Response schema documented *anywhere* | ⚠️ Partial | 16 fields are documented, but only in the PDF guide, not the spec — a spec-only integration (e.g., code generation from OpenAPI) would miss them entirely. | D-016 |
| Field naming consistency across documents | ❌ Inconsistent | `userID` (Appendix 1) vs. `userid` (Appendix 2) in the same guide. | D-013 |
| Endpoint descriptions match the live spec | ⚠️ Partial | Public Dev API's HTML description promises a "places" capability absent from the live spec. | D-009 |
| Worked examples internally consistent | ❌ Inconsistent | Docs page's stated date range doesn't match its own example URL's dates. | D-006 |
| Privacy/data-handling guidance present | ✅ Present | Clear statement that student data is tied to the school/teacher, not the individual student; home addresses/emails never exposed. | D-015 |
| Edge-case / undocumented-field guidance (e.g. student `userid`) | ❌ Missing | No source documents what `userid` holds for student-submitted records. | D-014 |
| Rate limits / pagination guidance | ⚠️ Partial | A 1,000,000-record cap is documented; no pagination mechanism (page tokens, cursors) is described for results near that cap. | D-005 |
| Error-response documentation (beyond HTTP codes) | ❌ Missing | No documented error body shape for 401/403/404 — a developer cannot distinguish "really unauthorized" from "framework boilerplate" from the response body alone. | D-010, D-011 |

## Summary

Of 11 criteria checked, **2 pass fully**, **3 pass partially**, and **6 show a clear gap**.
The most actionable fix for NASA/GLOBE's own documentation team would be: publish the
Data User Guide's field definitions directly in the OpenAPI spec (closes D-011, D-013,
D-016 at once) and either remove or clarify the 401/403 response declarations (closes
D-010).

None of this reflects on the API's actual security posture — only on the clarity and
internal consistency of its *public documentation*.
