# Rhylthyme Examples

A comprehensive collection of example programs and environments for the Rhylthyme real-time scheduling system.

## Overview

This repository contains working examples of Rhylthyme programs and environments that demonstrate various features and use cases. All examples are validated against the Rhylthyme schema and can be run with the [rhylthyme-cli-runner](https://github.com/rhylthyme/rhylthyme-cli-runner).

## Quick Start

1. **Install the CLI runner:**
   ```bash
   pip install rhylthyme-cli-runner
   ```

2. **Validate an example:**
   ```bash
   rhylthyme validate programs/breakfast_schedule.json
   ```

3. **Run an example:**
   ```bash
   rhylthyme run programs/breakfast_schedule.json
   ```

## Program Examples

### 🍳 Kitchen & Food Service

#### Basic Examples
- **`breakfast_schedule.json`** - Simple breakfast preparation with eggs, bacon, and toast
- **`breakfast_manual_triggers.json`** - Breakfast with manual step completion
- **`breakfast_with_buffers.json`** - Breakfast with setup and cleanup buffers
- **`breakfast_from_tracks.json`** - Breakfast using track templates
- **`breakfast_with_environment.json`** - Breakfast referencing an environment file

#### Restaurant & Commercial
- **`restaurant_breakfast.json`** - Restaurant breakfast service
- **`commercial_kitchen_service.json`** - Commercial kitchen operations
- **`kitchen_actors_example.json`** - Kitchen with multiple actor types

#### Bakery & Artisan
- **`bakery_program_example.json`** - Commercial bakery operations
- **`artisan_bread_production.json`** - Artisan bread making process

### 🧪 Laboratory & Research

#### Academic & Research
- **`lab_experiment.json`** - Basic laboratory experiment
- **`cell_culture_experiment.json`** - Cell culture procedures
- **`protein_lysate_immunoblotting.json`** - Protein analysis workflow
- **`rat_psychopharmacology.json`** - Animal research protocol
- **`drug_screening_from_tracks.json`** - Drug screening using track templates

#### Industry & Pharma
- **`biotech-company-lab.json`** - Biotech company laboratory environment
- **`small-academic-lab.json`** - Small academic laboratory environment
- **`large_pharma_lab.json`** - Large pharmaceutical laboratory environment

### ✈️ Aviation & Transportation

- **`airport_program_example.json`** - Airport operations and scheduling
- **`airport_batch_example.json`** - Batch processing for airport operations
- **`go_around_example.yaml`** - Aircraft go-around procedures

### 🎭 Events & Entertainment

- **`academy_awards_ceremony.json`** - Complex event scheduling for awards ceremony

### 🔧 Advanced Features

#### Resource Management
- **`resource_contention_example.yaml`** - Demonstrates resource contention and optimization
- **`multi_resource_example.json`** - Multiple resource types and constraints
- **`fractional_resource_example.json`** - Fractional resource usage
- **`test_overutilization.json`** - Resource overutilization scenarios

#### Timing & Triggers
- **`time_format_stagger_example.yaml`** - Time format variations and staggering
- **`flexible_time_format_example.yaml`** - Flexible time format usage
- **`staggered_batch_example.yaml`** - Batch processing with staggered starts
- **`test_offset_example.json`** - Offset-based timing
- **`simple_trigger_test.json`** - Basic trigger testing
- **`simple_on_test.json`** - Simple trigger conditions

#### Code Execution
- **`code_execution_example.yaml`** - Python code execution in steps
- **`simplified_code_example.yaml`** - Simplified code execution
- **`variable_substitution_example.yaml`** - Variable substitution in code

#### Optimization & Planning
- **`optimal_duration_example.yaml`** - Optimal duration calculations
- **`test_flex_auto_plan.json`** - Flexible auto-planning features
- **`comprehensive_example.json`** - Comprehensive feature demonstration
- **`comprehensive_manual_demo.json`** - Manual control demonstration
- **`manual_controls_demo.json`** - Manual step controls

## Environment Examples

### 🏠 Home & Residential
- **`home-kitchen.json`** - Standard home kitchen with 2 cooks
- **`restaurant.json`** - Restaurant environment

### 🏢 Commercial & Industrial
- **`commercial-kitchen.json`** - Commercial kitchen with professional staff
- **`bakery.json`** - Bakery environment
- **`artisan-bakery-detailed.json`** - Detailed artisan bakery setup

### 🧪 Laboratory & Research
- **`laboratory.json`** - Basic laboratory environment
- **`biotech-company-lab.json`** - Biotech company laboratory
- **`small-academic-lab.json`** - Small academic laboratory
- **`large_pharma_lab.json`** - Large pharmaceutical laboratory

### ✈️ Transportation
- **`airport.json`** - Airport operations environment

## Example Categories

### By Complexity

#### Beginner Examples
- `breakfast_schedule.json` - Simple sequential cooking
- `simple_trigger_test.json` - Basic triggers
- `lab_experiment.json` - Basic laboratory workflow

#### Intermediate Examples
- `breakfast_with_buffers.json` - Buffers and cleanup
- `resource_contention_example.yaml` - Resource management
- `kitchen_actors_example.json` - Multiple actor types

#### Advanced Examples
- `academy_awards_ceremony.json` - Complex event scheduling
- `rat_psychopharmacology.json` - Complex research protocols
- `comprehensive_example.json` - All features combined

### By Environment Type

#### Kitchen Environments
- Home kitchen examples
- Restaurant examples
- Commercial kitchen examples
- Bakery examples

#### Laboratory Environments
- Academic lab examples
- Industry lab examples
- Research protocol examples

#### Specialized Environments
- Airport operations
- Event management
- Manufacturing processes

## Current Status

### ✅ Working Examples
Most program examples validate successfully against the schema:
- `breakfast_schedule.json` - ✅ Validates correctly
- `lab_experiment.json` - ✅ Validates correctly
- `restaurant_breakfast.json` - ✅ Validates correctly
- And many more...

### ⚠️ Environment Files
The environment files in the `environments/` directory have some validation issues:
- Missing required tasks for specific environment types
- Resource constraint mismatches
- These issues prevent some programs from running with environment references

### 🔧 Recommended Usage
1. **Start with validation**: Use `rhylthyme validate` to check program files
2. **Focus on programs**: Most program examples work well for learning
3. **Environment info**: Use `rhylthyme environment-info` to learn about environment types
4. **Fix environments**: Environment files can be corrected to resolve validation issues

## Running Examples

### Basic Validation
```bash
# Validate a single program
rhylthyme validate programs/breakfast_schedule.json

# Validate with verbose output
rhylthyme validate programs/breakfast_schedule.json --verbose
```

### Running Programs
```bash
# Note: Some programs may require properly configured environments
# The environment files in this repository may have validation issues

# Run with interactive UI (if environment is properly configured)
rhylthyme run programs/breakfast_schedule.json

# Run with automatic start (no manual trigger needed)
rhylthyme run programs/breakfast_schedule.json --auto-start

# Run with time scaling (2x faster)
rhylthyme run programs/breakfast_schedule.json --time-scale 2.0
```

### Using Environments
```bash
# Run without environment (uses embedded resource constraints)
rhylthyme run programs/breakfast_schedule.json

# Run with automatic start (no manual trigger needed)
rhylthyme run programs/breakfast_schedule.json --auto-start

# List available environments (if any are properly configured)
rhylthyme environments

# Get environment information for a specific type
rhylthyme environment-info kitchen

# Validate environment files (may show validation errors)
rhylthyme validate-environments --environments-dir environments
```

### Optimization
```bash
# Create optimized version
rhylthyme plan programs/resource_contention_example.yaml optimized_program.json

# Run the optimized version
rhylthyme run optimized_program.json
```

## Example Features Demonstrated

### Core Features
- ✅ **Sequential Steps** - Basic step-by-step execution
- ✅ **Parallel Tracks** - Multiple concurrent workflows
- ✅ **Resource Constraints** - Limited resource management
- ✅ **Manual Triggers** - Human-controlled step completion
- ✅ **Variable Durations** - Flexible timing with min/max ranges

### Advanced Features
- ✅ **Buffer Times** - Setup and cleanup periods
- ✅ **Code Execution** - Python code in steps
- ✅ **Track Templates** - Reusable track definitions
- ✅ **Environment References** - External environment files
- ✅ **Fractional Resources** - Partial resource usage
- ✅ **Batch Processing** - Multiple iterations
- ✅ **Time Offsets** - Delayed starts
- ✅ **Complex Triggers** - Multiple trigger conditions

### Environment Features
- ✅ **Actor Types** - Different types of workers
- ✅ **Qualified Actors** - Skill-based resource allocation
- ✅ **Resource Constraints** - Equipment and space limits
- ✅ **Metadata** - Additional environment information

## Contributing

To add new examples:

1. **Create your program file** in the `programs/` directory
2. **Validate it** using `rhylthyme validate your_program.json`
3. **Test it** using `rhylthyme run your_program.json`
4. **Add documentation** in this README
5. **Submit a pull request**

### Example Guidelines

- Use descriptive names that indicate the feature being demonstrated
- Include comments in the JSON/YAML for clarity
- Keep examples focused on specific features
- Ensure all examples validate successfully
- Test that examples run without errors

## Schema Reference

All examples conform to the [Rhylthyme Schema](https://github.com/rhylthyme/rhylthyme-spec) version 0.1.0-alpha.

## Related Repositories

- **[rhylthyme-spec](https://github.com/rhylthyme/rhylthyme-spec)** - Schema definitions and specifications
- **[rhylthyme-cli-runner](https://github.com/rhylthyme/rhylthyme-cli-runner)** - Command-line interface and runner
- **[rhylthyme-web](https://github.com/rhylthyme/rhylthyme-web)** - Web-based interface

## License

Apache License 2.0 