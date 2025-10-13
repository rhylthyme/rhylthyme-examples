#!/usr/bin/env python3
"""
Pytest configuration and fixtures for rhylthyme-examples tests.
"""

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
def environments_dir(project_root):
    """Get the environments directory."""
    environments = project_root / "environments"
    if not environments.exists():
        pytest.skip("Environments directory not found")
    return environments


@pytest.fixture(scope="session")
def schema_file():
    """Get the schema file from rhylthyme-spec package."""
    try:
        import pkg_resources

        schema_path = pkg_resources.resource_filename(
            "rhylthyme_spec", "schemas/program_schema_0.1.0-alpha.json"
        )
        if not os.path.exists(schema_path):
            # Try alternative location
            spec_path = Path(__file__).parent.parent.parent / "rhylthyme-spec"
            schema_path = (
                spec_path
                / "src"
                / "rhylthyme_spec"
                / "schemas"
                / "program_schema_0.1.0-alpha.json"
            )
            if not schema_path.exists():
                pytest.skip("Schema file not found")
            return str(schema_path)
        return schema_path
    except (ImportError, FileNotFoundError):
        # Try relative path
        spec_path = Path(__file__).parent.parent.parent / "rhylthyme-spec"
        schema_path = (
            spec_path
            / "src"
            / "rhylthyme_spec"
            / "schemas"
            / "program_schema_0.1.0-alpha.json"
        )
        if not schema_path.exists():
            pytest.skip("Schema file not found")
        return str(schema_path)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "validation: Validation tests")
    config.addinivalue_line("markers", "slow: Slow tests")
