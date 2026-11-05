# Developer Guide — Integrating with the GLOBE API Safely

This guide is written for developers building against the public GLOBE API. It focuses
on practices that are safe for *you* (avoiding breakage from undocumented behavior) and
respectful of the *data source* (avoiding abusive request patterns against a publicly
funded, free service).

## 1. Safe request construction

- **Always specify a protocol and a date range.** The 53-value protocol enum and a
  narrow date range keep you well under the documented 1,000,000-record cap
  (`docs/ENDPOINTS.md`).
- **URL-encode all parameter values**, especially `countryName`, `organizationName`, and
  `siteName`, which may contain spaces or non-ASCII characters.
- **Use the "Request URL" pattern from the official docs for bulk access**, rather than
  the Swagger UI's interactive "Try it out" — this is NASA's own stated guidance for
  anything beyond ad hoc lookups.

## 2. Input validation (your side, before you send a request)

- Validate `protocol` client-side against the documented 53-value enum before sending —
  fail fast locally rather than relying on the API to reject an invalid value, since the
  API's error-body shape for invalid input is not documented (see `DOC_QUALITY_CHECKLIST.md`).
- Validate date parameters are well-formed and `startdate <= enddate` before sending.
- Treat `userid`, when you use it as a filter, as an opaque numeric token — never parse
  it, store it next to other data as if it were a username, or display it as if it
  identified a specific person beyond "some GLOBE contributor."

## 3. Response validation (your side, after you receive a response)

Because the OpenAPI spec's response model is an empty schema (no field names), **do not
assume any field will always be present**. Concretely:

- Use the local validator in `validator/validate.py` (and the schemas in `schemas/`) as a
  starting point for checking shapes in your own integration tests, against your own
  fixtures.
- Treat every field documented only in the PDF guide (see `docs/ENDPOINTS.md`) as
  "likely present, not guaranteed."
- Write defensive code: check for a key's existence before indexing into it; don't let a
  missing field crash a batch job.

## 4. Error handling

- A `401` or `403` from this API is currently of **unknown real-world meaning** — no
  security scheme is documented, so these codes may be generic framework responses, not
  evidence of a real permission boundary. Log the full response (status + body) rather
  than assuming a specific cause, and don't build retry-with-different-credentials logic
  around them without first getting it confirmed by NASA/GLOBE.
- A `404` likely means a malformed path (e.g., an invalid `protocol` segment) — validate
  client-side first (Section 2) to avoid triggering this.
- Because no documented error-body schema exists, log raw response bodies during
  development so you can adapt if the shape changes.

## 5. Pagination / result-size awareness

- The documented cap is 1,000,000 records per query. No pagination mechanism (cursor,
  page token) is documented.
- Practical approach: chunk large pulls by date range yourself (e.g., month-by-month)
  rather than relying on any undocumented pagination behavior.

## 6. Responsible data handling

- This is citizen-science data about environmental measurements, much of it submitted by
  students. Even though GLOBE's privacy page states student data isn't tied to an
  individual student, treat any `userid` values you fetch as a form of personal data by
  default: don't republish raw `userid` values in a public dashboard without a reason,
  and don't attempt to correlate `userid` across protocols to build a profile of a single
  contributor.
- Respect the 1,000,000-record cap as a signal about intended usage scale — this is a
  public-interest dataset, not a high-throughput production API; avoid tight polling
  loops.

## 7. Before you rely on this in production

- Confirm current behavior against the **live** Swagger UI yourself — this guide reflects
  documentation reviewed on 2026-11-05 and may drift from the live service over time.
- If you plan security-relevant testing (not just integration against documented
  behavior), that is out of scope for this guide — see NASA's own Vulnerability
  Disclosure Policy and go through Bugcrowd, not ad hoc probing.
