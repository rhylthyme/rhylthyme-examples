# Environment Catalog System

The Rhylthyme environment catalog system allows you to define resource constraints for different environments (restaurants, bakeries, laboratories, etc.) separately from your programs. This enables the same program to run in different environments with appropriate resource limits.

## Overview

Instead of embedding resource constraints directly in program files, you can:
1. Define environment catalogs with resource constraints
2. Reference an environment in your program
3. Run the same program in different environments

## Environment Catalog Structure

Environment catalogs are JSON or YAML files stored in the `environments/` directory:

```json
{
  "environmentId": "restaurant-standard",
  "name": "Standard Restaurant Kitchen",
  "description": "Resource constraints for a typical restaurant kitchen",
  "type": "restaurant",
  "actors": 6,  // Number of people who can work in this environment
  "resourceConstraints": [
    {
      "task": "stove-burner",
      "maxConcurrent": 6,
      "actorsRequired": 1.0,  // How much actor attention this task requires
      "description": "6-burner commercial range (1 cook can manage multiple burners)"
    },
    {
      "task": "oven",
      "maxConcurrent": 2,
      "actorsRequired": 0.3,  // Only requires 30% of one person's attention
      "description": "Double-stack convection ovens (mostly monitoring)"
    }
  ],
  "metadata": {
    "capacity": "medium",
    "certifications": ["health-department", "fire-safety"]
  }
}
```

## Actor Constraints

The environment system includes sophisticated human resource (actor) constraints that support different types of actors with specific qualifications for equipment.

### Actor Types System

Instead of just specifying a total number of actors, environments can define different types of actors with their counts and qualifications:

```json
{
  "actorTypes": {
    "head-chef": {
      "name": "Head Chef",
      "count": 1,
      "description": "Day-to-day kitchen operations, can use all equipment"
    },
    "chef-de-partie": {
      "name": "Chef de Partie",
      "count": 3,
      "description": "Runs a specific kitchen section"
    },
    "prep-cook": {
      "name": "Prep Cook",
      "count": 2,
      "description": "Ingredient preparation"
    }
  }
}
```

### Qualified Actor Types

Each task specifies which actor types are qualified to perform it:

```json
{
  "task": "stove-burner",
  "maxConcurrent": 8,
  "actorsRequired": 1.0,
  "qualifiedActorTypes": ["head-chef", "sous-chef", "chef-de-partie"],
  "description": "8-burner commercial range (qualified cooks only)"
}
```

### How Actor Type Constraints Work

1. **Actor Types**: Each environment defines different types of actors (e.g., head chef, prep cook, kitchen porter)
2. **Actor Counts**: Each actor type has a specific count available
3. **Qualified Types**: Each task lists which actor types are qualified to perform it
4. **Attention Required**: Each task specifies how much attention it requires (0.0 to 1.0+)
5. **Smart Assignment**: The system automatically assigns the best available qualified actor type

### Example: Commercial Kitchen

```json
{
  "actorTypes": {
    "head-chef": {"name": "Head Chef", "count": 1},
    "chef-de-partie": {"name": "Chef de Partie", "count": 3},
    "prep-cook": {"name": "Prep Cook", "count": 2},
    "kitchen-porter": {"name": "Kitchen Porter", "count": 2}
  },
  "resourceConstraints": [
    {
      "task": "stove-burner",
      "maxConcurrent": 8,
      "actorsRequired": 1.0,
      "qualifiedActorTypes": ["head-chef", "chef-de-partie"],
      "description": "Only qualified cooks can use stoves"
    },
    {
      "task": "prep-station",
      "maxConcurrent": 6,
      "actorsRequired": 1.0,
      "qualifiedActorTypes": ["head-chef", "chef-de-partie", "prep-cook"],
      "description": "Most kitchen staff can do prep work"
    },
    {
      "task": "dishwashing",
      "maxConcurrent": 3,
      "actorsRequired": 1.0,
      "qualifiedActorTypes": ["kitchen-porter"],
      "description": "Only kitchen porters handle dishwashing"
    }
  ]
}
```

In this example:
- Only head chefs and chefs de partie can use stoves (safety/skill requirement)
- Most staff can do prep work (broader qualification)
- Only kitchen porters handle dishwashing (role specialization)

### Backward Compatibility

The system maintains backward compatibility with the simple `actors` field:

```json
{
  "actors": 2,  // Legacy format - converted to generic actor type
  "resourceConstraints": [
    {
      "task": "prep-work",
      "maxConcurrent": 2,
      "actorsRequired": 1.0
      // No qualifiedActorTypes - uses "generic" actor type
    }
  ]
}
```

### Benefits of Actor Types

1. **Realistic Constraints**: Models real-world staff qualifications and restrictions
2. **Safety Compliance**: Ensures only qualified staff use dangerous equipment
3. **Role Specialization**: Enforces proper division of labor
4. **Resource Optimization**: System finds the best available qualified staff
5. **Scalable**: Easy to add new actor types and qualifications

## Using Environments in Programs

To use an environment, add an `environment` field to your program:

```json
{
  "programId": "breakfast-with-buffers",
  "name": "Breakfast Preparation",
  "environment": "home-kitchen-standard",  // Reference environment ID
  "tracks": [
    // ... your tracks and steps
  ]
  // No resourceConstraints section needed!
}
```

## Available Environments

List available environments using the CLI:

```bash
rhylthyme environments
```

Output:
```
ID                     Name                         Type        Description
--------------------------------------------------------------------------------------------------------
bakery-artisan         Artisan Bakery               bakery      Resource constraints for an artisan b...
home-kitchen-standard  Standard Home Kitchen        home        Resource constraints for a typical ho...
laboratory-research    Research Laboratory          laboratory  Resource constraints for a multi-disc...
restaurant-standard    Standard Restaurant Kitchen  restaurant  Resource constraints for a typical re...
```

## Environment Types

### Restaurant Kitchen
- **File**: `environments/restaurant.json`
- **Use Case**: Commercial kitchens with professional equipment
- **Resources**: Multiple burners, ovens, prep stations, plating areas

### Bakery
- **File**: `environments/bakery.json`
- **Use Case**: Professional bakeries with specialized equipment
- **Resources**: Deck ovens, proofers, mixers, work benches

### Laboratory
- **File**: `environments/laboratory.json`
- **Use Case**: Research labs with scientific equipment
- **Resources**: Fume hoods, centrifuges, microscopes, incubators

### Home Kitchen
- **File**: `environments/home-kitchen.json`
- **Use Case**: Residential kitchens with basic equipment
- **Resources**: Limited burners, single oven, basic appliances

## Creating Custom Environments

Create a new environment catalog in the `environments/` directory:

```json
{
  "environmentId": "food-truck",
  "name": "Mobile Food Truck",
  "description": "Compact kitchen on wheels",
  "type": "restaurant",
  "resourceConstraints": [
    {
      "task": "grill",
      "maxConcurrent": 1,
      "description": "Single flat-top grill"
    },
    {
      "task": "fryer",
      "maxConcurrent": 1,
      "description": "Single fryer basket"
    },
    {
      "task": "prep-work",
      "maxConcurrent": 1,
      "description": "Limited prep space"
    }
  ]
}
```

## Resource Constraint Merging

When a program uses an environment:
1. Environment constraints are loaded first
2. Any constraints in the program override environment constraints
3. Tasks without constraints use actor count as default

Example with override:
```json
{
  "environment": "restaurant-standard",
  "resourceConstraints": [
    {
      "task": "stove-burner",
      "maxConcurrent": 4  // Override environment's 6 burners
    }
  ]
}
```

## Benefits

1. **Portability**: Same program works in different environments
2. **Reusability**: Share environments across multiple programs
3. **Maintenance**: Update constraints in one place
4. **Testing**: Test programs against different resource limitations
5. **Documentation**: Self-documenting resource capabilities

## Example: Running Breakfast in Different Kitchens

```bash
# Original with embedded constraints
rhylthyme run examples/breakfast_schedule.json

# Using home kitchen environment
rhylthyme run examples/breakfast_with_buffers.json

# Same program could run in a restaurant (with different environment)
# Just change the environment field in the program
```

## Validation

Programs with environment references are validated to ensure:
- The referenced environment exists
- All tasks used in the program are covered by constraints
- Environment file is properly formatted

```bash
rhylthyme validate examples/breakfast_with_buffers.json
```

## Best Practices

1. **Name environments clearly**: Use descriptive IDs like `laboratory-biosafety-2`
2. **Document constraints**: Add descriptions to each resource constraint
3. **Version environments**: Consider versioning for production use
4. **Group by type**: Organize environments by their type (restaurant, lab, etc.)
5. **Include metadata**: Add relevant certifications, capacity, hours, etc. 