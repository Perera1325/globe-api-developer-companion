"""
Automated tests for the GLOBE API response validator.

All inputs are local, synthetic fixtures under ../fixtures/. No network
calls are made anywhere in this test suite.
"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "validator"))

from validate import load_json, validate_one, SCHEMA_MAP, SCHEMAS_DIR, FIXTURES_DIR  # noqa: E402


def test_schema_files_exist():
    for cfg in SCHEMA_MAP.values():
        schema_path = SCHEMAS_DIR / cfg["schema_file"]
        assert schema_path.exists(), f"missing schema file: {schema_path}"


def test_fixture_files_exist():
    for cfg in SCHEMA_MAP.values():
        for fixture_name in cfg["default_fixtures"]:
            fixture_path = FIXTURES_DIR / fixture_name
            assert fixture_path.exists(), f"missing fixture file: {fixture_path}"


def test_valid_measurement_fixture_passes():
    schema = load_json(SCHEMAS_DIR / "measurement_response.schema.json")
    data = load_json(FIXTURES_DIR / "measurement_valid.json")
    errors = validate_one(data, schema, "measurement_valid.json")
    assert errors == []


def test_invalid_latitude_fixture_is_caught():
    schema = load_json(SCHEMAS_DIR / "measurement_response.schema.json")
    data = load_json(FIXTURES_DIR / "measurement_invalid_latitude.json")
    errors = validate_one(data, schema, "measurement_invalid_latitude.json")
    assert errors, "expected the out-of-range latitude to be flagged"
    assert any("latitude" in e for e in errors)


def test_dev_country_all_fixture_is_a_list_of_objects():
    schema = load_json(SCHEMAS_DIR / "dev_country_all.schema.json")
    data = load_json(FIXTURES_DIR / "dev_country_all_valid.json")
    assert isinstance(data, list)
    errors = validate_one(data, schema, "dev_country_all_valid.json")
    assert errors == []


def test_dev_lastpublishdate_fixture_passes():
    schema = load_json(SCHEMAS_DIR / "dev_lastpublishdate.schema.json")
    data = load_json(FIXTURES_DIR / "dev_lastpublishdate_valid.json")
    errors = validate_one(data, schema, "dev_lastpublishdate_valid.json")
    assert errors == []


def test_no_fixture_contains_an_at_symbol_suggesting_an_email():
    """
    Lightweight guard: fixtures are synthetic, so none should accidentally
    contain anything resembling a real email address.
    """
    for path in FIXTURES_DIR.glob("*.json"):
        text = path.read_text(encoding="utf-8")
        assert "@" not in text, f"unexpected '@' character in fixture {path.name}"


def test_schemas_flag_undocumented_fields_explicitly():
    """
    Every schema must carry an 'x-documentation-gap' note, so a reader of
    the schema file alone understands which parts are confirmed vs guessed.
    """
    for cfg in SCHEMA_MAP.values():
        schema = load_json(SCHEMAS_DIR / cfg["schema_file"])
        assert "x-documentation-gap" in schema
