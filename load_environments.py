#!/usr/bin/env python3
"""
Script to demonstrate how to load environment catalogs from the rhylthyme-examples directory.
"""

import sys
import os
from pathlib import Path

# Add the CLI runner to the path
sys.path.insert(0, str(Path(__file__).parent.parent / 'rhylthyme-cli-runner' / 'src'))

from rhylthyme_cli_runner.environment_loader import EnvironmentLoader

def main():
    """Demonstrate environment loading from the current directory."""
    
    # Get the current directory (where this script is located)
    current_dir = Path(__file__).parent
    environments_dir = current_dir / "environments"
    
    print(f"Loading environments from: {environments_dir}")
    print(f"Directory exists: {environments_dir.exists()}")
    print()
    
    # Create an environment loader pointing to the local environments directory
    loader = EnvironmentLoader(str(environments_dir))
    
    # List all available environments
    print("Available environments:")
    environments = loader.list_environments()
    
    if not environments:
        print("No environments found!")
        return
    
    for env in environments:
        print(f"  - {env['id']} ({env['type']}): {env['name']}")
    
    print()
    
    # Show details for a specific environment
    if environments:
        first_env = environments[0]
        env_id = first_env['id']
        print(f"Loading details for: {env_id}")
        
        try:
            env_data = loader.load_environment(env_id)
            print(f"  Name: {env_data.get('name', 'Unknown')}")
            print(f"  Type: {env_data.get('type', 'Unknown')}")
            print(f"  Description: {env_data.get('description', 'No description')}")
            print(f"  Resource Constraints: {len(env_data.get('resourceConstraints', []))}")
            
            # Show resource constraints
            constraints = env_data.get('resourceConstraints', [])
            if constraints:
                print("  Resource Constraints:")
                for constraint in constraints[:3]:  # Show first 3
                    print(f"    - {constraint.get('task', 'Unknown')}: max {constraint.get('maxConcurrent', 'Unknown')}")
                if len(constraints) > 3:
                    print(f"    ... and {len(constraints) - 3} more")
            
        except Exception as e:
            print(f"  Error loading environment: {e}")
    
    print()
    print("To use these environments with the CLI runner:")
    print("1. Set the RHYLTHYME_ENVIRONMENTS_DIR environment variable:")
    print(f"   export RHYLTHYME_ENVIRONMENTS_DIR={environments_dir}")
    print("2. Or modify the CLI runner to use this directory by default")

if __name__ == "__main__":
    main() 