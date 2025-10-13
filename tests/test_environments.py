#!/usr/bin/env python3
"""
Test validation of environment files in rhylthyme-examples.
"""

import json
from pathlib import Path

import pytest


@pytest.mark.validation
@pytest.mark.unit
def test_environments_directory_exists(environments_dir):
    """Test that the environments directory exists and contains files."""
    assert environments_dir.exists(), "Environments directory does not exist"

    # Check for at least some environment files
    env_files = list(environments_dir.glob("*.json"))
    assert len(env_files) > 0, "No environment files found in environments directory"

    print(f"Found {len(env_files)} environment files")


@pytest.mark.validation
@pytest.mark.unit
def test_all_environments_are_valid_json(environments_dir):
    """Test that all environment files can be parsed as valid JSON."""
    env_files = list(environments_dir.glob("*.json"))

    if not env_files:
        pytest.skip("No environment files found")

    parse_failures = []

    for filepath in env_files:
        try:
            with open(filepath, "r") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            parse_failures.append((filepath.name, f"JSON parse error: {e}"))

    if parse_failures:
        error_msg = "Environment file parse failures:\n"
        for filename, error in parse_failures:
            error_msg += f"\n{filename}:\n  - {error}\n"
        pytest.fail(error_msg)


@pytest.mark.validation
@pytest.mark.integration
def test_environments_have_required_fields(environments_dir):
    """Test that all environment files have required basic fields."""
    env_files = list(environments_dir.glob("*.json"))

    if not env_files:
        pytest.skip("No environment files found")

    print(f"\nValidating {len(env_files)} environment files")
    print("=" * 60)

    missing_fields = []

    for filepath in sorted(env_files):
        filename = filepath.name
        print(f"Validating {filename}...")

        try:
            with open(filepath, "r") as f:
                env_data = json.load(f)

            # Check for required fields
            required_fields = ["environmentId", "name"]
            file_missing_fields = []

            for field in required_fields:
                if field not in env_data:
                    file_missing_fields.append(field)

            # Check for recommended fields
            recommended_fields = ["type"]
            file_missing_recommended = []

            for field in recommended_fields:
                if field not in env_data:
                    file_missing_recommended.append(field)

            if file_missing_fields:
                missing_fields.append((filename, file_missing_fields))
                print(f"  ❌ Missing required fields: {', '.join(file_missing_fields)}")
            elif file_missing_recommended:
                print(
                    f"  ⚠️  Missing recommended fields: {', '.join(file_missing_recommended)}"
                )
            else:
                print(f"  ✅ All fields present")

        except Exception as e:
            missing_fields.append((filename, [f"Error reading file: {str(e)}"]))
            print(f"  ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("ENVIRONMENT VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(env_files)}")
    print(f"Files with missing required fields: {len(missing_fields)}")

    if missing_fields:
        error_msg = "Environment files with missing required fields:\n"
        for filename, fields in missing_fields:
            error_msg += f"\n{filename}:\n"
            for field in fields:
                error_msg += f"  - {field}\n"
        pytest.fail(error_msg)
    else:
        print("\n✅ All environment files have required fields")


@pytest.mark.validation
@pytest.mark.integration
def test_environment_structure(environments_dir):
    """Test that environment files have expected structure."""
    env_files = list(environments_dir.glob("*.json"))

    if not env_files:
        pytest.skip("No environment files found")

    structure_issues = []

    for filepath in sorted(env_files):
        filename = filepath.name

        try:
            with open(filepath, "r") as f:
                env_data = json.load(f)

            issues = []

            # Check environmentId format
            if "environmentId" in env_data:
                env_id = env_data["environmentId"]
                if not isinstance(env_id, str) or not env_id:
                    issues.append("environmentId must be a non-empty string")

            # Check name format
            if "name" in env_data:
                name = env_data["name"]
                if not isinstance(name, str) or not name:
                    issues.append("name must be a non-empty string")

            # Check type if present
            if "type" in env_data:
                env_type = env_data["type"]
                if not isinstance(env_type, str) or not env_type:
                    issues.append("type must be a non-empty string")

            # Check actors if present (can be int or list)
            if "actors" in env_data:
                actors = env_data["actors"]
                if not isinstance(actors, (int, list)):
                    issues.append("actors must be an integer or a list")
                elif isinstance(actors, int) and actors < 0:
                    issues.append("actors count must be non-negative")
                elif isinstance(actors, list) and len(actors) == 0:
                    issues.append("actors list is empty")

            # Check resources if present
            if "resources" in env_data:
                resources = env_data["resources"]
                if not isinstance(resources, dict):
                    issues.append("resources must be a dictionary")

            if issues:
                structure_issues.append((filename, issues))

        except Exception as e:
            structure_issues.append((filename, [f"Error processing file: {str(e)}"]))

    if structure_issues:
        error_msg = "Environment files with structure issues:\n"
        for filename, issues in structure_issues:
            error_msg += f"\n{filename}:\n"
            for issue in issues:
                error_msg += f"  - {issue}\n"
        pytest.fail(error_msg)


@pytest.mark.validation
@pytest.mark.unit
def test_known_good_environments(environments_dir):
    """Test that specific known environment files are valid."""
    # List of environments that should exist and be valid
    known_environments = [
        "home_kitchen.json",
        "laboratory.json",
    ]

    for env_name in known_environments:
        filepath = environments_dir / env_name

        if not filepath.exists():
            print(f"Skipping {env_name} - file not found")
            continue

        print(f"Validating known environment: {env_name}")

        with open(filepath, "r") as f:
            env_data = json.load(f)

        # Check required fields
        assert "environmentId" in env_data, f"{env_name} missing environmentId"
        assert "name" in env_data, f"{env_name} missing name"

        print(f"  ✅ {env_name} is valid")
