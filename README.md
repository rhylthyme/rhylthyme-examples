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

## Importable source files

The directories below hold input files in their *native* formats — they
are NOT Rhylthyme program JSON. Each one is meant to be fed through the
matching importer (CLI, web upload, or MCP) to **produce** a Rhylthyme
program. Use these to try the importers end-to-end.

| Directory | Format | Importer | Try it on the web |
|---|---|---|---|
| [`opentrons/`](opentrons/) | Opentrons Protocol API v2 `.py` | `rhylthyme-import-opentrons <file.py>` | [kitchen.rhylthyme.com](https://kitchen.rhylthyme.com/) → sidebar → **Upload Program** → drop the `.py` |
| [`cooklang/`](cooklang/) | CookLang `.cook` recipe | `rhylthyme-import-cooklang <file.cook>` | same drop zone — accepts `.cook` |
| [`gold/`](gold/) | Plain-text source + `context.json` + expert `program.json` | `rhylthyme eval-prompts --score-only --gold gold --predicted <dir>` scores a model's programs against them | n/a (evaluation set, see [`gold/README.md`](gold/README.md)) |

### Opentrons protocols (`opentrons/`)

Five sample protocols covering the importer's full hardware surface.
Same files double as the importer's golden-fixture test inputs, so they
stay in sync with the code.

| File | What it exercises |
|---|---|
| `trivial.py` | Four-command protocol — `pickup_tip → aspirate → dispense → drop_tip` on one OT-2 single-channel. Best for a smoke test. |
| `pcr_setup.py` | `mix(repetitions=...)`, `protocol.delay()`, `protocol.pause()`, dedicated `Protocol` track for protocol-level steps. |
| `serial_dilution.py` | Two-mount protocol: 8-channel `distribute` + per-column transfers on the left, single-channel `transfer` on the right. Shows helper-method expansion. |
| `elisa.py` | Four module families on one program: heater-shaker, magnetic, temperature, absorbance. Each gets its own track + `maxConcurrent: 1` constraint. |
| `cell_culture_passage.py` | Flex 96-channel pipette (shared gantry constraint), Flex 1-channel on the right mount, and `gripper.move_labware(use_gripper=True)`. |

Full feature matrix + troubleshooting:
[docs.rhylthyme.com/development/opentrons](https://docs.rhylthyme.com/development/opentrons/).

### CookLang recipes (`cooklang/`)

| File | What it is |
|---|---|
| `easy_pancakes.cook` | A CookLang recipe with timed steps (`~{15%minutes}`) and explicit ingredients. Drops into the web upload modal or `rhylthyme-import-cooklang`. |

### Gold set (`gold/`)

Six expert-authored programs (three kitchen including Thanksgiving with one
oven, one laboratory protocol, one event run-of-show, one partner workout),
each paired with the text it was extracted from and a `context.json`. Every
step carries `metadata.sourceSpan = {quote, occurrence}` pointing into
`source.txt`, so an agent-authored program can be scored by span match,
not just by name. Layout, span format and authoring rules:
[`gold/README.md`](gold/README.md). Tests: `tests/test_gold.py`.

---

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

#### Per-instance triggers and in-flight limits (schema 0.3.0-alpha)
- **`cookies_three_trays.json`** - Three trays bake serially in one oven; each cools as it comes out (`instances: "each"`), boxing waits for all (`instances: "all"`), and `maxInFlight: 2` holds the third bake until a rack slot is free (74 min, PRD §7)
- **`compound_each_pairing.json`** - Two samples lysed and digested on staggered schedules; a compound `"each"` trigger pairs instance *i* of both, then a barrier pools them. Carries `metadata.expectedTimings` asserted by the parity tests
- **`pcr_twelve_samples.json`** - Twelve samples through a rotor that holds six (`maxInFlight: 6` over a three-step per-sample chain), pooled into two parallel thermocycler runs (`thermocycler maxConcurrent: 2`)
- **`airport_landings_taxi_gate.json`** - Four staggered landings, per-aircraft taxi and gate chain, and an apron that holds two (`maxInFlight: 2`), showing that a stagger delay is a minimum gap the gate may push out

Each of these carries `metadata.expectedTimings` (and a
`expectedTimingsNote` explaining the hand computation) which both toolchains
must reproduce exactly.

## Negative Examples (`invalid/`)

`invalid/` holds programs that are **deliberately wrong**, one file per
validator code, named after the code they provoke
(`invalid/E_EACH_COUNT_MISMATCH.json`, `invalid/W_UNBARRIERED_CHAIN.json`, …).
They are schema-valid JSON so that the only finding is the one they exist
for, and each declares it in `metadata`:

```json
"metadata": {"expectedFinding": {"code": "E_EACH_WITH_REPLICATES", "severity": "error"}}
```

Both Python validators (`tests/test_invalid_examples.py`) and the JS
validator (`rhylthyme-server/mcp-api/schedule.test.js`) must emit exactly
that code with a fix hint. Error findings make the program invalid;
`warning` and `info` findings leave it valid. `I_IMPLICIT_BARRIER` is
info-level and emitted by the JS validator only. The `programs/` test
globs do not descend into `invalid/`, so these files never count as
working examples. To add a code: write `invalid/<CODE>.json` with
`expectedFinding`, and make sure both validators emit it.

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

## Notebook Examples

Interactive notebooks that embed the Rhylthyme D3 timeline visualization inline.

- **`rhylthyme_notebook_example.ipynb`** - Jupyter notebook: load an example program and build one from scratch, rendered as interactive timelines
- **`rhylthyme_marimo_example.py`** - Marimo notebook: same examples using `mo.iframe()` for reactive, script-enabled embedding

```bash
# Jupyter
jupyter notebook rhylthyme_notebook_example.ipynb

# Marimo
marimo edit rhylthyme_marimo_example.py
```

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

All examples conform to the [Rhylthyme Schema](https://github.com/rhylthyme/rhylthyme-spec); programs using per-instance triggers declare `"schemaVersion": "0.3.0-alpha"`, the rest `0.1.0` / `0.2.0-alpha`.

## Related Repositories

- **[rhylthyme-spec](https://github.com/rhylthyme/rhylthyme-spec)** - Schema definitions and specifications
- **[rhylthyme-cli-runner](https://github.com/rhylthyme/rhylthyme-cli-runner)** - Command-line interface and runner
- **[rhylthyme-web](https://github.com/rhylthyme/rhylthyme-web)** - Web-based interface

## License

Apache License 2.0 