#!/usr/bin/env python3
"""
Pytest configuration and fixtures for rhylthyme-examples tests.
"""

import json
import os
import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def programs_dir(project_root):
    """Get the programs directory."""
    programs = project_root / "programs"
    if not programs.exists():
        pytest.skip("Programs directory not found")
    return programs


@pytest.fixture(scope="session")
def invalid_dir(project_root):
    """Get the negative-example directory (one program per validator code)."""
    invalid = project_root / "invalid"
    if not invalid.exists():
        pytest.skip("Invalid-examples directory not found")
    return invalid


@pytest.fixture(scope="session")
def environments_dir(project_root):
    """Get the environments directory."""
    environments = project_root / "environments"
    if not environments.exists():
        pytest.skip("Environments directory not found")
    return environments


# Program schema files shipped by rhylthyme-spec, keyed by the schemaVersion
# values that select them. Anything older than 0.3.0-alpha (0.1.0, 0.2.0,
# 0.2.0-alpha, missing) validates against 0.2.0-alpha, which is what the
# default `schema_file` fixture returns.
DEFAULT_SCHEMA_VERSION = "0.2.0-alpha"
SCHEMA_FILE_BY_VERSION = {
    "0.3.0-alpha": "program_schema_0.3.0-alpha.json",
}


def _locate_schema(schema_name):
    """Return the path to a schema file from rhylthyme-spec, or skip the test."""
    try:
        from importlib import resources

        schema_path = str(resources.files("rhylthyme_spec") / "schemas" / schema_name)
        if os.path.exists(schema_path):
            return schema_path
    except (ImportError, FileNotFoundError):
        pass
    # Try relative path
    spec_path = Path(__file__).parent.parent.parent / "rhylthyme-spec"
    schema_path = spec_path / "src" / "rhylthyme_spec" / "schemas" / schema_name
    if not schema_path.exists():
        pytest.skip("Schema file not found")
    return str(schema_path)


def schema_version_of(program_path):
    """Read a program file's declared schemaVersion (None if absent/unreadable)."""
    try:
        with open(program_path, "r") as fh:
            if str(program_path).endswith((".yaml", ".yml")):
                import yaml

                data = yaml.safe_load(fh)
            else:
                data = json.load(fh)
        return data.get("schemaVersion") if isinstance(data, dict) else None
    except Exception:
        return None


@pytest.fixture(scope="session")
def schema_file():
    """Get the default (0.2.0-alpha) program schema file from rhylthyme-spec."""
    return _locate_schema(f"program_schema_{DEFAULT_SCHEMA_VERSION}.json")


@pytest.fixture(scope="session")
def schema_file_for():
    """
    Return a callable mapping a program path to the schema file that matches
    the program's declared schemaVersion (0.3.0-alpha programs get the 0.3.0
    schema; everything else the 0.2.0-alpha one).
    """

    def _select(program_path):
        version = schema_version_of(program_path)
        name = SCHEMA_FILE_BY_VERSION.get(
            version, f"program_schema_{DEFAULT_SCHEMA_VERSION}.json"
        )
        return _locate_schema(name)

    return _select


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "validation: Validation tests")
    config.addinivalue_line("markers", "slow: Slow tests")
