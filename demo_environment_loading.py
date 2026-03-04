#!/usr/bin/env python3
"""
Demonstration script showing how to load environment catalogs from the CLI
using the actual directory structure in rhylthyme-examples.

This script demonstrates:
1. Automatic detection of environments in current directory
2. Explicit environment directory specification
3. Environment variable configuration
4. Program validation with environment references
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and display the results."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        if result.returncode != 0:
            print(f"Command failed with exit code: {result.returncode}")
    except Exception as e:
        print(f"Error running command: {e}")

def main():
    """Demonstrate environment loading capabilities."""
    
    # Get the current directory
    current_dir = Path.cwd()
    environments_dir = current_dir / "environments"
    
    print("🚀 Rhylthyme Environment Catalog Loading Demonstration")
    print(f"📍 Working Directory: {current_dir}")
    print(f"📁 Environments Directory: {environments_dir}")
    print(f"📁 Environments Exist: {environments_dir.exists()}")
    
    # Method 1: Automatic detection (environments in current directory)
    print("\n" + "="*80)
    print("📋 METHOD 1: Automatic Environment Detection")
    print("="*80)
    print("The CLI automatically detects environments in the current directory.")
    print("When you run 'rhylthyme environments' from a directory containing")
    print("an 'environments' subdirectory, it will load those environments.")
    
    run_command("rhylthyme environments", 
                "Listing environments with automatic detection")
    
    # Method 2: Explicit environment directory
    print("\n" + "="*80)
    print("📋 METHOD 2: Explicit Environment Directory")
    print("="*80)
    print("Use the --environments-dir option to specify a custom directory.")
    print("This is useful when environments are in a different location.")
    
    run_command(f"rhylthyme --environments-dir {environments_dir} environments", 
                "Listing environments with explicit directory")
    
    # Method 3: Environment variable
    print("\n" + "="*80)
    print("📋 METHOD 3: Environment Variable")
    print("="*80)
    print("Set the RHYLTHYME_ENVIRONMENTS_DIR environment variable to")
    print("configure the default environment directory.")
    
    env_cmd = f"RHYLTHYME_ENVIRONMENTS_DIR={environments_dir} rhylthyme environments"
    run_command(env_cmd, "Listing environments using environment variable")
    
    # Method 4: JSON output format
    print("\n" + "="*80)
    print("📋 METHOD 4: Different Output Formats")
    print("="*80)
    print("The environments command supports different output formats:")
    print("- table (default): Human-readable table")
    print("- json: Machine-readable JSON")
    print("- yaml: YAML format")
    
    run_command("rhylthyme environments --format json | head -20", 
                "JSON output format (first 20 lines)")
    
    # Method 5: Environment validation
    print("\n" + "="*80)
    print("📋 METHOD 5: Environment Validation")
    print("="*80)
    print("Validate all environment files against their schemas.")
    
    run_command(f"rhylthyme validate-environments --environments-dir {environments_dir}", 
                "Validating environment files")
    
    # Method 6: Program validation with environment references
    print("\n" + "="*80)
    print("📋 METHOD 6: Program Validation with Environment References")
    print("="*80)
    print("Validate programs that reference environments.")
    print("The CLI will automatically load the referenced environment.")
    
    # Find a program that uses an environment
    airport_program = "programs/airport_program_example.json"
    if Path(airport_program).exists():
        run_command(f"rhylthyme validate {airport_program}", 
                    "Validating airport program with environment reference")
    else:
        print("Airport program not found, skipping validation test")
    
    # Method 7: Environment information
    print("\n" + "="*80)
    print("📋 METHOD 7: Environment Type Information")
    print("="*80)
    print("Get information about specific environment types.")
    
    run_command("rhylthyme environment-info kitchen", 
                "Information about kitchen environment type")
    
    # Summary
    print("\n" + "="*80)
    print("📋 SUMMARY: How to Load Environment Catalogs")
    print("="*80)
    print("✅ Automatic Detection:")
    print("   - Place environments in an 'environments' subdirectory")
    print("   - Run 'rhylthyme environments' from that directory")
    print()
    print("✅ Explicit Directory:")
    print("   - Use: rhylthyme --environments-dir /path/to/environments environments")
    print()
    print("✅ Environment Variable:")
    print("   - Set: export RHYLTHYME_ENVIRONMENTS_DIR=/path/to/environments")
    print("   - Run: rhylthyme environments")
    print()
    print("✅ Program Validation:")
    print("   - Programs with 'environment' or 'environmentType' fields")
    print("   - CLI automatically resolves environment references")
    print()
    print("✅ Available Commands:")
    print("   - rhylthyme environments [--format table|json|yaml]")
    print("   - rhylthyme validate-environments [--environments-dir PATH]")
    print("   - rhylthyme environment-info TYPE")
    print("   - rhylthyme validate PROGRAM_FILE")
    print("   - rhylthyme run PROGRAM_FILE [-e ENVIRONMENT_ID]")
    
    print("\n🎉 Environment catalog loading demonstration complete!")

if __name__ == "__main__":
    main() 