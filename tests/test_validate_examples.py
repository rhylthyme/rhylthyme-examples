#!/usr/bin/env python3
"""
Validate all example programs in rhylthyme-examples.

This module validates all JSON and YAML program files against the Rhylthyme schema.
"""

import glob
import json
from pathlib import Path

import pytest

# Import the validation function from rhylthyme-cli-runner
from rhylthyme_cli_runner.validate_program import validate_program_file_structured


@pytest.mark.validation
@pytest.mark.integration
@pytest.mark.slow
def test_validate_all_json_programs(programs_dir, schema_file):
    """Test that all JSON program files validate successfully against the schema."""
    json_files = list(programs_dir.glob("*.json"))

    if not json_files:
        pytest.skip("No JSON program files found")

    print(f"\nValidating {len(json_files)} JSON program files")
    print("=" * 60)

    schema_failures = []
    logic_warnings = []
    valid_count = 0

    for filepath in sorted(json_files):
        filename = filepath.name
        print(f"Validating {filename}...")

        try:
            result = validate_program_file_structured(str(filepath), schema_file)

            if result["schema_errors"]:
                schema_failures.append((filename, result["schema_errors"]))
                print(f'  ❌ Schema errors: {len(result["schema_errors"])}')
            else:
                print(f"  ✅ Schema: OK")

            if result["logic_errors"]:
                logic_warnings.append((filename, result["logic_errors"]))
                print(f'  ⚠️  Logic warnings: {len(result["logic_errors"])}')
            else:
                print(f"  ✅ Logic: OK")

            if not result["schema_errors"] and not result["logic_errors"]:
                valid_count += 1

        except Exception as e:
            schema_failures.append((filename, [f"Validation failed: {str(e)}"]))
            print(f"  ❌ Exception: {e}")

    print("\n" + "=" * 60)
    print("JSON VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(json_files)}")
    print(f"Fully valid: {valid_count}")
    print(f"Files with schema errors: {len(schema_failures)}")
    print(f"Files with logic warnings: {len(logic_warnings)}")

    if logic_warnings:
        print("\n⚠️  LOGIC WARNINGS:")
        print("-" * 40)
        for filename, errors in logic_warnings:
            print(f"\n{filename}:")
            for error in errors:
                print(f"  - {error}")

    # Schema errors cause test failure
    if schema_failures:
        print("\n❌ SCHEMA ERRORS (FATAL):")
        print("-" * 40)
        error_msg = "Schema validation failures:\n"
        for filename, errors in schema_failures:
            error_msg += f"\n{filename}:\n"
            for error in errors:
                error_msg += f"  - {error}\n"
        pytest.fail(error_msg)
    else:
        print("\n✅ All JSON programs passed schema validation")


@pytest.mark.validation
@pytest.mark.integration
@pytest.mark.slow
def test_validate_all_yaml_programs(programs_dir, schema_file):
    """Test that all YAML program files validate successfully against the schema."""
    yaml_files = list(programs_dir.glob("*.yaml")) + list(programs_dir.glob("*.yml"))

    if not yaml_files:
        pytest.skip("No YAML program files found")

    print(f"\nValidating {len(yaml_files)} YAML program files")
    print("=" * 60)

    schema_failures = []
    logic_warnings = []
    parse_errors = []
    valid_count = 0

    for filepath in sorted(yaml_files):
        filename = filepath.name
        print(f"Validating {filename}...")

        try:
            result = validate_program_file_structured(str(filepath), schema_file)

            if result["schema_errors"]:
                schema_failures.append((filename, result["schema_errors"]))
                print(f'  ❌ Schema errors: {len(result["schema_errors"])}')
            else:
                print(f"  ✅ Schema: OK")

            if result["logic_errors"]:
                logic_warnings.append((filename, result["logic_errors"]))
                print(f'  ⚠️  Logic warnings: {len(result["logic_errors"])}')
            else:
                print(f"  ✅ Logic: OK")

            if not result["schema_errors"] and not result["logic_errors"]:
                valid_count += 1

        except Exception as e:
            parse_errors.append((filename, str(e)))
            print(f"  ⚠️  Parse error: {e}")

    print("\n" + "=" * 60)
    print("YAML VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(yaml_files)}")
    print(f"Fully valid: {valid_count}")
    print(f"Files with schema errors: {len(schema_failures)}")
    print(f"Files with logic warnings: {len(logic_warnings)}")
    print(f"Files with parse errors: {len(parse_errors)}")

    if parse_errors:
        print("\n⚠️  YAML PARSE ERRORS:")
        print("-" * 40)
        for filename, error in parse_errors:
            print(f"\n{filename}:")
            print(f"  - {error}")

    if logic_warnings:
        print("\n⚠️  LOGIC WARNINGS:")
        print("-" * 40)
        for filename, errors in logic_warnings:
            print(f"\n{filename}:")
            for error in errors:
                print(f"  - {error}")

    # Schema errors cause test failure
    if schema_failures:
        print("\n❌ SCHEMA ERRORS (FATAL):")
        print("-" * 40)
        error_msg = "Schema validation failures:\n"
        for filename, errors in schema_failures:
            error_msg += f"\n{filename}:\n"
            for error in errors:
                error_msg += f"  - {error}\n"
        pytest.fail(error_msg)
    else:
        print("\n✅ All YAML programs that parsed successfully passed schema validation")


@pytest.mark.validation
@pytest.mark.unit
def test_validate_specific_known_good_examples(programs_dir, schema_file):
    """Test validation of specific known good example programs."""
    # List of examples that should always validate without errors
    known_good_examples = [
        "breakfast_schedule.json",
        "lab_experiment.json",
    ]

    for example_name in known_good_examples:
        filepath = programs_dir / example_name

        if not filepath.exists():
            print(f"Skipping {example_name} - file not found")
            continue

        print(f"Validating known good example: {example_name}")

        result = validate_program_file_structured(str(filepath), schema_file)

        # These examples should have no schema errors
        assert not result[
            "schema_errors"
        ], f"{example_name} has schema errors: {result['schema_errors']}"

        # Logic warnings are acceptable for known good examples
        if result["logic_errors"]:
            print(f"  ⚠️  Logic warnings: {result['logic_errors']}")

        print(f"  ✅ {example_name} validated successfully")


@pytest.mark.validation
@pytest.mark.unit
def test_programs_directory_exists(programs_dir):
    """Test that the programs directory exists and contains files."""
    assert programs_dir.exists(), "Programs directory does not exist"

    # Check for at least some program files
    program_files = list(programs_dir.glob("*.json")) + list(
        programs_dir.glob("*.yaml")
    )
    assert len(program_files) > 0, "No program files found in programs directory"

    print(f"Found {len(program_files)} program files")


@pytest.mark.validation
@pytest.mark.unit
def test_programs_are_valid_json_or_yaml(programs_dir):
    """Test that all program files can be parsed as JSON or YAML."""
    import yaml

    json_files = list(programs_dir.glob("*.json"))
    yaml_files = list(programs_dir.glob("*.yaml")) + list(programs_dir.glob("*.yml"))

    parse_failures = []

    # Test JSON files
    for filepath in json_files:
        try:
            with open(filepath, "r") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            parse_failures.append((filepath.name, f"JSON parse error: {e}"))

    # Test YAML files
    for filepath in yaml_files:
        try:
            with open(filepath, "r") as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            parse_failures.append((filepath.name, f"YAML parse error: {e}"))

    if parse_failures:
        error_msg = "Parse failures:\n"
        for filename, error in parse_failures:
            error_msg += f"\n{filename}:\n  - {error}\n"
        pytest.fail(error_msg)
