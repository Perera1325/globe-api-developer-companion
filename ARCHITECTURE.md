# Architecture

This project is entirely static/local: a documentation set, a dashboard that runs by
opening an HTML file (no server, no build step), and a Python validator exercised by a
local test suite. It never calls the live GLOBE API.

```mermaid
flowchart TD
    subgraph Sources["Official NASA/GLOBE sources (read-only, reviewed 2026-11-05)"]
        A1["GLOBE API docs page<br/>globe.gov/globe-data/globe-api"]
        A2["GLOBE Data User Guide v3.0<br/>(PDF, Appendices 1-2)"]
        A3["Live OpenAPI specs<br/>public-api / public-dev-api"]
        A4["GLOBE Privacy page"]
        A5["NASA VDP Policy"]
    end

    subgraph Project["globe-api-companion (this repo)"]
        B1["docs/EVIDENCE_REGISTER.md<br/>(facts, dated, cited)"]
        B2["docs/ENDPOINTS.md<br/>docs/DOC_QUALITY_CHECKLIST.md<br/>docs/DEVELOPER_GUIDE.md"]
        B3["schemas/*.schema.json<br/>(community-derived)"]
        B4["fixtures/*.json<br/>(synthetic only)"]
        B5["validator/validate.py"]
        B6["tests/test_validator.py<br/>(pytest)"]
        B7["dashboard/ (static HTML/CSS/JS)"]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    A5 --> B1

    B1 --> B2
    B1 --> B3
    B3 --> B5
    B4 --> B5
    B5 --> B6
    B1 --> B7
    B2 --> B7

    style Sources fill:#1d252f,stroke:#2b3542,color:#e7edf3
    style Project fill:#161c24,stroke:#2b3542,color:#e7edf3
```

## Design choices

- **No network calls anywhere in the shipped code.** The dashboard is static HTML; the
  validator reads only local JSON files. This keeps the project safe to run and safe to
  hand to anyone, with zero risk of it accidentally hitting NASA systems.
- **Schemas are explicitly labeled community-derived**, with an `x-documentation-gap`
  field on every schema file, so nobody mistakes them for an official contract.
- **Evidence register is the single source of truth.** Every claim in the dashboard, the
  developer guide, and the doc-quality checklist traces back to a dated, cited row in
  `docs/EVIDENCE_REGISTER.md`.
- **Tests only touch fixtures**, never the network, so the suite is deterministic and
  safe to run in CI without secrets or external access.
