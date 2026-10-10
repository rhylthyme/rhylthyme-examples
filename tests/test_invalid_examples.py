#!/usr/bin/env python3
"""
Negative examples: every ``invalid/<CODE>.json`` declares the validator
finding it exists to provoke in ``metadata.expectedFinding`` (``code`` and
``severity``). Both Python validators, the root ``rhylthyme`` package and the
``rhylthyme-cli-runner`` fork, must emit exactly that code with a non-empty
fix hint. Error findings make the program invalid; warning findings do not.
``I_IMPLICIT_BARRIER`` is info-level and JS-only (PRD open question 5), so
for it the Python validators must merely keep the program valid. The JS
validator is checked by the same loop in
``rhylthyme-server/mcp-api/schedule.test.js``.
"""

import json
from pathlib import Path

import pytest

try:  # the root `rhylthyme` package is a monorepo-only import
    from rhylthyme import validate_program_structured
except ImportError:  # pragma: no cover - CI checks out only spec + cli-runner
    validate_program_structured = None
from rhylthyme_cli_runner.validate_program import validate_program_file_structured

INVALID_DIR = Path(__file__).resolve().parent.parent / "invalid"
INVALID_FILES = sorted(INVALID_DIR.glob("*.json")) if INVALID_DIR.exists() else []

# Codes that only the JS validator emits (info-level notes).
JS_ONLY_CODES = {"I_IMPLICIT_BARRIER"}


def _expected(path):
    with open(path) as fh:
        program = json.load(fh)
    expected = (program.get("metadata") or {}).get("expectedFinding")
    assert expected and expected.get("code") and expected.get("severity"), (
        f"{path.name}: metadata.expectedFinding must declare code and severity"
    )
    return program, expected


def _check(findings, is_valid, expected, label):
    code, severity = expected["code"], expected["severity"]
    matches = [f for f in findings if f["code"] == code]
    if code in JS_ONLY_CODES:
        assert not matches, f"{label}: {code} is JS-only"
        assert is_valid, f"{label}: program must stay valid; findings: {findings}"
        return
    assert matches, f"{label}: expected {code}, got {[f['code'] for f in findings]}"
    for f in matches:
        assert f["severity"] == severity, f"{label}: {code} severity {f['severity']} != {severity}"
        assert f["fix"], f"{label}: {code} has no fix hint"
        assert f["message"], f"{label}: {code} has no message"
        assert f["where"], f"{label}: {code} has no where"
    if severity == "error":
        assert not is_valid, f"{label}: an error finding must invalidate the program"
    else:
        assert is_valid, f"{label}: a {severity} must not invalidate the program"
        assert not any(f["severity"] == "error" for f in findings), (
            f"{label}: unexpected errors alongside {code}: {findings}"
        )


@pytest.mark.validation
@pytest.mark.unit
def test_invalid_directory_covers_every_code(invalid_dir):
    names = {p.stem for p in invalid_dir.glob("*.json")}
    for code in (
        "E_INSTANCES_ON_SINGLE",
        "E_EACH_WITH_REPLICATES",
        "E_EACH_COUNT_MISMATCH",
        "E_INFLIGHT_GT_COUNT",
        "E_INFLIGHT_NO_CHAIN",
        "W_UNBARRIERED_CHAIN",
        "I_IMPLICIT_BARRIER",
        "W_ALERT_BEFORE_MANUAL_START",
        "W_ALERT_BEFORE_INDEFINITE_END",
        "W_ALERT_BEFORE_PROGRAM_START",
        "E_ALERT_BAD_OFFSET",
    ):
        assert code in names, f"invalid/{code}.json is missing"


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("path", INVALID_FILES, ids=[p.stem for p in INVALID_FILES])
def test_negative_example_file_is_named_after_its_code(path):
    _, expected = _expected(path)
    assert path.stem == expected["code"], "file name must equal metadata.expectedFinding.code"


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("path", INVALID_FILES, ids=[p.stem for p in INVALID_FILES])
def test_root_validator_emits_expected_code(path, schema_file_for):
    program, expected = _expected(path)
    with open(schema_file_for(path)) as fh:
        schema = json.load(fh)
    if validate_program_structured is None:
        pytest.skip("root rhylthyme package not installed")
    result = validate_program_structured(program, schema)
    assert not result["schema_errors"], f"{path.name}: schema errors {result['schema_errors']}"
    _check(result["findings"], result["is_valid"], expected, f"root/{path.name}")
    # The legacy string list renders the code and the fix hint.
    if expected["severity"] == "error":
        assert any(f"[{expected['code']}]" in e and "(fix:" in e for e in result["logic_errors"])
    elif expected["severity"] == "warning":
        assert any(f"[{expected['code']}]" in w for w in result["warnings"])
        assert not result["logic_errors"]


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("path", INVALID_FILES, ids=[p.stem for p in INVALID_FILES])
def test_cli_runner_validator_emits_expected_code(path, schema_file_for):
    _, expected = _expected(path)
    result = validate_program_file_structured(str(path), schema_file_for(path))
    assert not result["schema_errors"], f"{path.name}: schema errors {result['schema_errors']}"
    _check(result["findings"], result["is_valid"], expected, f"cli-runner/{path.name}")
    if expected["severity"] == "error":
        assert any(f"[{expected['code']}]" in e and "(fix:" in e for e in result["logic_errors"])
    elif expected["severity"] == "warning":
        assert any(f"[{expected['code']}]" in w for w in result["warnings"])
        assert not result["logic_errors"]
