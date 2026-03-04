# Environment Catalog Loading Guide

This guide shows how to load environment catalogs from the CLI using the actual directory structure in `rhylthyme-examples`.

**Important**: Environment catalogs are completely optional! They only serve to determine overutilized resources and provide resource constraints for validation. You can run programs without any environment specification.

## Directory Structure

```
rhylthyme-examples/
├── environments/          # Environment catalog files (optional)
│   ├── airport.json
│   ├── bakery.json
│   ├── kitchen.json
│   ├── laboratory.json
│   └── ...
├── programs/             # Example programs
│   ├── airport_program_example.json
│   ├── kitchen_program_example.json
│   └── ...
└── ...
```

## When to Use Environments

Environments are useful when you want to:
- **Validate Resource Usage**: Check if your program exceeds resource limits
- **Detect Overutilization**: Identify when resources are being used beyond capacity
- **Model Real-world Constraints**: Represent actual physical constraints (e.g., kitchen equipment, laboratory space)

## When Not to Use Environments

You don't need environments for:
- **Simple Programs**: Programs without resource constraints
- **Development/Testing**: When you don't need resource validation
- **Custom Resource Management**: When you handle resources differently

## Loading Methods

### 1. Automatic Detection (Recommended)

When you're in a directory that contains an `environments` subdirectory, the CLI automatically detects it:

```bash
# From rhylthyme-examples directory
rhylthyme environments
```

**Output:**
```
ID                           Name                                          Type        Icon            Description
airport-standard             Standard Airport                              airport     fa-plane        Resource constraints for standard air...
commercial-kitchen-standard  Standard Commercial Kitchen                   kitchen     fa-utensils     Resource constraints for a profession...
home-kitchen                 Home Kitchen (Base)                           kitchen     fa-home         Base home kitchen environment (default)...
...
```

### 2. Explicit Directory Specification

Use the `--environments-dir` option to specify a custom directory:

```bash
rhylthyme --environments-dir /path/to/environments environments
```

### 3. Environment Variable

Set the `RHYLTHYME_ENVIRONMENTS_DIR` environment variable:

```bash
export RHYLTHYME_ENVIRONMENTS_DIR=/path/to/environments
rhylthyme environments
```

## Available Commands

### List Environments (Optional)

```bash
# Table format (default)
rhylthyme environments

# JSON format
rhylthyme environments --format json

# YAML format
rhylthyme environments --format yaml
```

### Validate Environments (Optional)

```bash
# Validate all environment files
rhylthyme validate-environments

# Validate with custom directory
rhylthyme validate-environments --environments-dir /path/to/environments

# Verbose validation
rhylthyme validate-environments --verbose
```

### Get Environment Information (Optional)

```bash
# Get information about environment types
rhylthyme environment-info kitchen
rhylthyme environment-info laboratory
rhylthyme environment-info bakery
```

### Validate Programs (With or Without Environment)

```bash
# Validate a program without environment
rhylthyme validate programs/example.json

# Validate a program that references an environment
rhylthyme validate programs/airport_program_example.json

# Run a program without environment
rhylthyme run programs/example.json

# Run a program with environment file
rhylthyme run programs/airport_program_example.json -e environments/airport.json

# Override environment for a program
rhylthyme run programs/airport_program_example.json -e environments/kitchen.json
```

## Example Usage

### From rhylthyme-examples directory:

```bash
# List all available environments (optional)
rhylthyme environments

# Validate environment files (optional)
rhylthyme validate-environments

# Validate a program (works with or without environment)
rhylthyme validate programs/airport_program_example.json

# Run a program (works with or without environment)
rhylthyme run programs/airport_program_example.json

# Run with specific environment file
rhylthyme run programs/airport_program_example.json -e environments/airport.json
```

### From any directory:

```bash
# Use explicit path for environments
rhylthyme --environments-dir /path/to/rhylthyme-examples/environments environments

# Use environment variable
export RHYLTHYME_ENVIRONMENTS_DIR=/path/to/rhylthyme-examples/environments
rhylthyme environments

# Run with absolute path to environment file
rhylthyme run program.json -e /path/to/environments/kitchen.json
```

## Environment Resolution

The CLI handles environment references in programs:

1. **Direct Environment File**: `"environment": "environments/airport.json"`
2. **Environment Type**: `"environmentType": "kitchen"` → resolves to default kitchen environment file
3. **Command Line Override**: `-e environments/kitchen.json` overrides program setting
4. **No Environment**: Programs run without resource validation

## Available Environment Types

- **airport**: Airport operations (runways, gates, taxiways)
- **kitchen**: Kitchen environments (stove, prep, cleanup)
- **laboratory**: Laboratory environments (bench space, equipment)
- **bakery**: Bakery environments (mixer, oven, work bench)

## Troubleshooting

### No environments found
- **This is normal** - environments are optional
- Check that you're in the correct directory with an `environments` subdirectory (if using environments)
- Verify environment files have valid JSON/YAML format
- Use `--environments-dir` to specify the correct path

### Environment validation errors
- Run `rhylthyme validate-environments --verbose` for detailed error information
- Check that environment files conform to the schema
- Ensure required tasks are defined for the environment type

### Program validation fails
- **Programs can run without environments** - check if the error is environment-related
- Verify the referenced environment exists (if using environments)
- Check that the program's tasks match the environment's resource constraints
- Use `-e` to override the environment if needed

## Getting Started Without Environments

You can start using Rhylthyme immediately without any environment setup:

```bash
# Create a simple program
echo '{
  "programId": "simple-test",
  "name": "Simple Test",
  "tracks": [
    {
      "trackId": "main",
      "name": "Main Track",
      "steps": [
        {
          "stepId": "step1",
          "name": "First Step",
          "task": "test",
          "duration": {"type": "fixed", "seconds": 30},
          "startTrigger": {"type": "programStart"}
        }
      ]
    }
  ]
}' > simple_program.json

# Validate and run without environment
rhylthyme validate simple_program.json
rhylthyme run simple_program.json
```

## Next Steps

1. **Start Simple**: Create and run basic programs without environments
2. **Add Environments Later**: When you need resource validation
3. **Explore Examples**: Check out the programs in this repository
4. **Customize**: Create your own environment catalogs for your specific use cases 