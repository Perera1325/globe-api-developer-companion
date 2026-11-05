#!/usr/bin/env python3
"""
GLOBE API Response Validator (local, offline)
================================================

Validates sample JSON responses against community-derived JSON Schemas
for the publicly documented GLOBE API (api.globe.gov/search/).

IMPORTANT SCOPE NOTE
---------------------
This tool never sends network requests. It only validates local JSON
files (either synthetic fixtures shipped in ../fixtures/, or a file you
point it at) against the schemas in ../schemas/. See docs/EVIDENCE_REGISTER.md
for which schema fields are confirmed-documented vs. best-effort guesses.

Usage
-----
    python validate.py                      # validate all shipped fixtures
    python validate.py path/to/your.json --schema measurement_response

Exit code is non-zero if any validation fails.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft7Validator
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "Missing dependency 'jsonschema'. Install it inside a virtual environment:\n"
        "  python3 -m venv .venv\n"
        "  source .venv/bin/activate   # Windows: .venv\\Scripts\\activate\n"
        "  pip install -r validator/requirements.txt\n"
    )
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
FIXTURES_DIR = ROOT / "fixtures"

# Maps a short schema name -> schema filename, and the fixture(s) that
# exercise it by default when no explicit file is given.
SCHEMA_MAP = {
    "measurement_response": {
        "schema_file": "measurement_response.schema.json",
        "default_fixtures": [
            "measurement_valid.json",
            "measurement_invalid_latitude.json",
        ],
    },
    "dev_country_all": {
        "schema_file": "dev_country_all.schema.json",
        "default_fixtures": ["dev_country_all_valid.json"],
    },
    "dev_lastpublishdate": {
        "schema_file": "dev_lastpublishdate.schema.json",
        "default_fixtures": ["dev_lastpublishdate_valid.json"],
    },
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_one(data: dict, schema: dict, label: str) -> list[str]:
    """Return a list of human-readable error strings (empty if valid)."""
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    out = []
    for err in errors:
        path = ".".join(str(p) for p in err.path) or "<root>"
        out.append(f"  [{label}] at '{path}': {err.message}")
    return out


def run_default_suite() -> int:
    """Validate every shipped fixture against its matching schema."""
    total_checked = 0
    total_failed = 0

    print("GLOBE API Response Validator -- default fixture suite\n" + "-" * 56)

    for schema_name, cfg in SCHEMA_MAP.items():
        schema_path = SCHEMAS_DIR / cfg["schema_file"]
        schema = load_json(schema_path)

        for fixture_name in cfg["default_fixtures"]:
            fixture_path = FIXTURES_DIR / fixture_name
            data = load_json(fixture_path)
            total_checked += 1

            errors = validate_one(data, schema, fixture_name)
            expected_invalid = "invalid" in fixture_name

            if errors:
                status = (
                    "FAIL (expected -- demonstrates validator catching an error)"
                    if expected_invalid
                    else "FAIL (unexpected)"
                )
                if not expected_invalid:
                    total_failed += 1
                print(f"\n{fixture_name}  ->  {status}")
                for e in errors:
                    print(e)
            else:
                status = "PASS"
                if expected_invalid:
                    # A fixture named "invalid" that passed is itself a problem.
                    total_failed += 1
                    status = "PASS (unexpected -- fixture named 'invalid' did not fail)"
                print(f"\n{fixture_name}  ->  {status}")

    print("\n" + "-" * 56)
    print(f"Checked {total_checked} fixture(s). Unexpected outcomes: {total_failed}.")
    return 1 if total_failed else 0


def run_single(file_path: str, schema_name: str) -> int:
    if schema_name not in SCHEMA_MAP:
        sys.stderr.write(
            f"Unknown schema '{schema_name}'. Choices: {', '.join(SCHEMA_MAP)}\n"
        )
        return 2
    schema = load_json(SCHEMAS_DIR / SCHEMA_MAP[schema_name]["schema_file"])
    data = load_json(Path(file_path))
    errors = validate_one(data, schema, Path(file_path).name)
    if errors:
        print(f"INVALID against schema '{schema_name}':")
        for e in errors:
            print(e)
        return 1
    print(f"VALID against schema '{schema_name}'.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file", nargs="?", help="Path to a local JSON file to validate (optional)."
    )
    parser.add_argument(
        "--schema",
        choices=list(SCHEMA_MAP),
        default="measurement_response",
        help="Which schema to validate 'file' against (only used with 'file').",
    )
    args = parser.parse_args()

    if args.file:
        return run_single(args.file, args.schema)
    return run_default_suite()


if __name__ == "__main__":
    sys.exit(main())
