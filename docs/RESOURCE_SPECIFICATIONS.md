# Resource Specification System

The rhylthyme workflow system includes a comprehensive resource specification system that allows you to define detailed equipment specifications including manufacturer information, capacity details, photos, and maintenance schedules.

## Overview

The resource specification system provides:

- **Detailed Equipment Specs**: Full manufacturer/model information, serial numbers, capacities, and physical specifications
- **Photo Management**: Attach photos of equipment for documentation and training
- **Document Storage**: Store manuals, warranties, and maintenance logs
- **Integration with Workflows**: Reference detailed specs directly in workflow steps
- **Command-Line Tools**: Easy management through CLI commands

## Core Components

### ResourceSpecification Class

The `ResourceSpecification` dataclass contains comprehensive equipment information:

```python
@dataclass
class ResourceSpecification:
    # Basic identification
    resource_id: str
    name: str
    category: str  # e.g., "oven", "mixer", "fryer", "prep-station"
    
    # Equipment details
    manufacturer: str
    model: str
    capacity: Dict[str, Union[float, str]]
    
    # Optional detailed information
    serial_number: Optional[str] = None
    year_manufactured: Optional[int] = None
    dimensions: Optional[Dict[str, float]] = None
    power_requirements: Optional[Dict[str, Any]] = None
    
    # Usage and safety
    qualified_actor_types: List[str] = None
    safety_requirements: List[str] = None
    maintenance_schedule: Optional[Dict[str, str]] = None
    
    # Documentation
    photos: List[Dict[str, str]] = None
    manuals: List[Dict[str, str]] = None
    certifications: List[str] = None
    
    # Operational data
    purchase_date: Optional[str] = None
    purchase_price: Optional[float] = None
    warranty_expiry: Optional[str] = None
    condition: str = "good"
```

## Example Resource Specifications

### Commercial Mixer

```json
{
  "resource_id": "mixer_a200_001",
  "name": "20-Quart Commercial Stand Mixer",
  "category": "mixer",
  "manufacturer": "Hobart",
  "model": "A-200",
  "serial_number": "H200-2023-001",
  "year_manufactured": 2023,
  "capacity": {
    "volume": 20,
    "unit": "quarts",
    "max_batch_size": "12 lbs dough"
  },
  "dimensions": {
    "width": 23.5,
    "height": 31.5,
    "depth": 17.5,
    "unit": "inches"
  },
  "power_requirements": {
    "voltage": 115,
    "amperage": 15,
    "phase": 1,
    "horsepower": 0.33
  },
  "qualified_actor_types": ["head-baker", "pastry-chef", "baker", "assistant-baker"],
  "safety_requirements": [
    "safety_guard_required",
    "training_certification",
    "no_loose_clothing",
    "tie_back_long_hair"
  ],
  "maintenance_schedule": {
    "daily": "clean_bowl_and_attachments",
    "weekly": "lubricate_planetary_gear",
    "monthly": "inspect_drive_belt",
    "quarterly": "professional_service"
  },
  "photos": [
    {
      "photo_id": "mixer_front_001",
      "filename": "hobart_a200_front_view.jpg",
      "description": "Front view showing control panel and bowl",
      "photo_type": "general"
    }
  ],
  "manuals": [
    {
      "doc_id": "mixer_manual_001",
      "filename": "hobart_a200_operating_manual.pdf",
      "doc_type": "manual",
      "description": "Complete operating and maintenance manual"
    }
  ],
  "purchase_date": "2023-06-15",
  "purchase_price": 2850.00,
  "warranty_expiry": "2025-06-15",
  "condition": "excellent"
}
```

### Convection Oven

```json
{
  "resource_id": "oven_dfg200_001",
  "name": "Double Deck Convection Oven",
  "category": "oven",
  "manufacturer": "Blodgett",
  "model": "DFG-200-ES",
  "capacity": {
    "chambers": 2,
    "pan_capacity_per_chamber": 5,
    "pan_size": "18x26 inch",
    "temperature_range": "200-500°F"
  },
  "power_requirements": {
    "fuel_type": "natural_gas",
    "gas_input": "120,000 BTU/hr per chamber",
    "electrical": "115V, 60Hz, 1-phase for controls"
  },
  "certifications": ["NSF", "CSA", "ENERGY_STAR"],
  "custom_fields": {
    "steam_injection": true,
    "digital_controls": true,
    "programmable_recipes": 99
  }
}
```

## CLI Usage

### Creating Resources

```bash
# Create a new resource specification
python -m rhylthyme.resource_cli create \
  --name "Commercial Mixer" \
  --category mixer \
  --manufacturer Hobart \
  --model A-200 \
  --capacity volume=20 \
  --capacity unit=quarts \
  --description "Heavy-duty stand mixer" \
  --serial-number H200-2023-001 \
  --year-manufactured 2023
```

### Managing Photos

```bash
# Add a photo to a resource
python -m rhylthyme.resource_cli add-photo mixer_abc123 \
  /path/to/mixer_photo.jpg \
  --description "Front view of mixer" \
  --photo-type general

# Supported photo types:
# - general: General equipment photos
# - manual: Photos of manual pages or instructions
# - installation: Installation and setup photos
# - maintenance: Maintenance and repair photos
# - damage: Documentation of damage or issues
```

### Managing Documents

```bash
# Add a manual or document
python -m rhylthyme.resource_cli add-document mixer_abc123 \
  /path/to/manual.pdf \
  --doc-type manual \
  --description "Operating manual"

# Supported document types:
# - manual: Operating manuals
# - spec_sheet: Technical specifications
# - warranty: Warranty information
# - maintenance_log: Maintenance records
# - certification: Safety and compliance certificates
```

### Listing and Searching

```bash
# List all resources
python -m rhylthyme.resource_cli list

# List resources by category
python -m rhylthyme.resource_cli list --category mixer

# Search resources
python -m rhylthyme.resource_cli search "Hobart"

# Show detailed resource information
python -m rhylthyme.resource_cli show mixer_abc123

# Export complete catalog
python -m rhylthyme.resource_cli export catalog.json
```

### Creating Examples

```bash
# Create example bakery resources
python -m rhylthyme.resource_cli create-examples
```

## Integration with Workflows

### Environment Definition

Resources can be embedded in environment definitions:

```json
{
  "environmentId": "artisan-bakery-detailed",
  "name": "Artisan Bakery with Detailed Equipment Specs",
  
  "resourceSpecifications": {
    "mixer_a200_001": {
      "resource_id": "mixer_a200_001",
      "name": "20-Quart Commercial Stand Mixer",
      "manufacturer": "Hobart",
      "model": "A-200",
      "capacity": {"volume": 20, "unit": "quarts"}
    }
  },
  
  "resourceConstraints": [
    {
      "task": "mixing",
      "maxConcurrent": 1,
      "description": "20-quart commercial mixer operations",
      "resourceSpecId": "mixer_a200_001",
      "capacityMetrics": {
        "max_batch_volume": 20,
        "unit": "quarts",
        "throughput_per_hour": 8
      }
    }
  ]
}
```

### Workflow Step Metadata

Steps can reference detailed equipment specifications:

```json
{
  "stepId": "final-mix",
  "name": "Final Dough Mixing",
  "task": "mixing",
  "metadata": {
    "equipment_used": {
      "resource_spec_id": "mixer_a200_001",
      "manufacturer": "Hobart",
      "model": "A-200",
      "settings": {
        "speed": "2 (medium-low)",
        "attachment": "dough_hook",
        "mixing_time": "12-15 minutes"
      },
      "safety_notes": [
        "Use safety guard during mixing",
        "Stop mixer before scraping bowl",
        "Ensure loose clothing is secured"
      ]
    }
  }
}
```

## File Storage Structure

The resource specification system organizes files as follows:

```
resources/
├── specs/           # JSON specification files
│   ├── mixer_abc123.json
│   ├── oven_def456.json
│   └── proofer_ghi789.json
├── photos/          # Equipment photos
│   ├── mixer_abc123_photo_001.jpg
│   ├── oven_def456_photo_001.jpg
│   └── oven_def456_photo_002.jpg
└── docs/           # Manuals and documents
    ├── mixer_abc123_manual_001.pdf
    ├── oven_def456_manual_001.pdf
    └── oven_def456_warranty_001.pdf
```

## Key Features

### 1. Make and Model Tracking
- Complete manufacturer and model information
- Serial numbers and manufacturing dates
- Purchase information and warranty tracking

### 2. Capacity Specifications
- Flexible capacity definitions (volume, weight, dimensions, etc.)
- Custom units and measurements
- Performance metrics and throughput data

### 3. Photo Management
- Multiple photos per resource
- Categorized photo types (general, manual, installation, etc.)
- Automatic file organization and integrity checking
- Metadata tracking (upload date, file size, description)

### 4. Safety and Compliance
- Safety requirement documentation
- Qualified actor type definitions
- Certification tracking (NSF, UL, ENERGY STAR, etc.)
- Maintenance schedule definitions

### 5. Integration Benefits
- Equipment-specific settings in workflow steps
- Capacity-aware resource allocation
- Safety requirement enforcement
- Maintenance schedule integration
- Cost analysis capabilities

## Advanced Features

### Custom Fields
Add industry-specific or equipment-specific fields:

```json
{
  "custom_fields": {
    "attachments": ["dough_hook", "wire_whip", "flat_beater"],
    "noise_level": "68 dB",
    "duty_cycle": "continuous",
    "energy_efficiency": "ENERGY STAR certified"
  }
}
```

### Search and Filtering
```python
# Search by manufacturer
results = manager.search_resources("Hobart")

# Filter by category
mixers = manager.list_resources(category="mixer")

# Search specific fields
results = manager.search_resources("A-200", fields=["model", "description"])
```

### Catalog Export
Export complete equipment catalogs for inventory management, insurance, or compliance reporting:

```bash
python -m rhylthyme.resource_cli export equipment_catalog.json
```

## Benefits

1. **Comprehensive Documentation**: Full equipment specifications with photos and manuals
2. **Safety Compliance**: Track safety requirements and qualified operators
3. **Workflow Integration**: Reference specific equipment in workflow steps
4. **Asset Management**: Track purchase dates, warranties, and maintenance
5. **Training Support**: Visual documentation for equipment operation
6. **Capacity Planning**: Make informed decisions based on actual equipment capabilities

This resource specification system transforms rhylthyme from a simple workflow tool into a comprehensive operational management platform suitable for professional environments requiring detailed equipment tracking and safety compliance. 