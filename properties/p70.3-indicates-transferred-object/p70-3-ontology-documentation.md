# P70.3 Indicates Transferred Object - Ontology Documentation

## Table of Contents

1. [Property Definition](#property-definition)
2. [Semantic Structure](#semantic-structure)
3. [Full CIDOC-CRM Pattern](#full-cidoc-crm-pattern)
4. [Object Properties](#object-properties)
5. [Domain and Range](#domain-and-range)
6. [Transformation Examples](#transformation-examples)
7. [Comparison with Related Properties](#comparison-with-related-properties)
8. [Implementation Notes](#implementation-notes)
9. [Use Cases](#use-cases)
10. [AAT References](#aat-references)

## Property Definition

### Core Property

```turtle
gmn:P70_3_indicates_transferred_object
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.3 indicates transferred object"@en ;
    rdfs:comment "Simplified property for associating a contract document with a physical thing (object) that is being transferred through the transaction documented by the contract. This property uses the E13 Attribute Assignment pattern to model objects with rich semantic properties including type, quantity, monetary value, measurements, color, and provenance. Represents the full CIDOC-CRM path: E31_Document > P67_refers_to > E7/E8/E10_Activity > P140i_was_assigned_by > E13_Attribute_Assignment > P141_assigned > E18_Physical_Thing. The E13 also uses P177_assigned_property_of_type to specify whether this is a transfer of title (P24) or custody (P30), and P2_has_type to categorize the object. This property is provided as a convenience for data entry in Omeka-S and should be transformed to the full CIDOC-CRM structure for formal compliance. The range includes all physical things that can be transferred: buildings (gmn:E22_1_Building), moveable property (gmn:E22_2_Moveable_Property), and general physical things (E18_Physical_Thing)."@en ;
    rdfs:subPropertyOf cidoc:P67_refers_to ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_2_Sales_Contract
            gmn:E31_6_Lease_Contract
            gmn:E31_7_Donation_Contract
            gmn:E31_8_Dowry_Contract
        )
    ] ;
    rdfs:range [
        a owl:Class ;
        owl:unionOf (
            cidoc:E18_Physical_Thing
            cidoc:E21_Person
            gmn:E22_1_Building
            gmn:E22_2_Moveable_Property
            cidoc:E24_Physical_Human-Made_Thing
            cidoc:E53_Place
        )
    ] ;
    dcterms:created "2025-10-28"^^xsd:date ;
    rdfs:seeAlso cidoc:P67_refers_to, cidoc:E13_Attribute_Assignment, cidoc:P24_transferred_title_of, cidoc:P30_transferred_custody_of .
```

### Key Characteristics

- **Shortcut Nature**: Simplifies complex E13 pattern for Omeka-S data entry
- **Bidirectional**: Links contract to object and implicitly object to contract
- **Multiple Objects**: Can be used multiple times on same contract
- **Rich Semantics**: Each object can have detailed properties
- **Transformation Required**: Must be expanded to full CIDOC-CRM for compliance

## Semantic Structure

### Overview

The property implements the E13 Attribute Assignment pattern, which is the formal CIDOC-CRM method for assigning properties to entities within the context of an activity:

```
Document Layer:
E31_Document (contract) --[shortcut]--> E18_Physical_Thing (object)

Semantic Layer:
E31_Document (contract)
  └─ P67_refers_to
      └─ E7/E8/E10_Activity (the transfer event)
          └─ P140i_was_assigned_by
              └─ E13_Attribute_Assignment
                  ├─ P177_assigned_property_of_type (P24 or P30)
                  ├─ P141_assigned → E18_Physical_Thing (the object)
                  └─ P2_has_type → E55_Type (object category)
```

### Why E13 Attribute Assignment?

The E13 pattern is necessary because:

1. **Contextual Attribution**: We're not just saying "this object exists" but "this contract assigns this object to this activity"
2. **Property Disambiguation**: Distinguishes between title transfer (P24) and custody transfer (P30)
3. **Temporal Binding**: Properties are assigned in the context of the historical activity
4. **Source Citation**: Attribution is explicitly linked to the documentary evidence

### Activity Type Selection

The choice of activity type depends on contract type:

| Contract Type | Activity Class | Property Type | Rationale |
|---------------|---------------|---------------|-----------|
| Sales Contract | `E8_Acquisition` | P24 (title) | Ownership changes |
| Lease Contract | `E10_Transfer_of_Custody` | P30 (custody) | Temporary control, not ownership |
| Donation Contract | `E8_Acquisition` | P24 (title) | Ownership changes |
| Dowry Contract | `E8_Acquisition` | P24 (title) | Ownership changes |

## Full CIDOC-CRM Pattern

### Complete Structure with Object Properties

```turtle
# Contract document
<contract001> a gmn:E31_2_Sales_Contract ;
    cidoc:P67_refers_to <contract001/acquisition> .

# The acquisition/transfer activity
<contract001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <seller001> ;
    cidoc:P22_transferred_title_to <buyer001> ;
    cidoc:P140i_was_assigned_by <contract001/acquisition/attribution_001> .

# E13 Attribute Assignment - assigns object to activity
<contract001/acquisition/attribution_001> a cidoc:E13_Attribute_Assignment ;
    # What property is being assigned (P24 or P30)
    cidoc:P177_assigned_property_of_type cidoc:P24_transferred_title_of ;
    # The actual object being assigned
    cidoc:P141_assigned <object_salt_001> ;
    # Category/type of the object
    cidoc:P2_has_type <aat:300010967> . # salt

# The object resource with its properties
<object_salt_001> a cidoc:E24_Physical_Human-Made_Thing ;
    cidoc:P1_is_identified_by <object_salt_001/appellation_001> ;
    cidoc:P2_has_type <aat:300010967> ; # salt
    cidoc:P43_has_dimension <dimension_weight_001> ;
    cidoc:P56_bears_feature <feature_color_white> ;
    cidoc:P27_moved_from <place_ibiza> .

# Object name/appellation
<object_salt_001/appellation_001> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ; # name
    cidoc:P190_has_symbolic_content "White salt from Ibiza" .

# Dimension (weight)
<dimension_weight_001> a cidoc:E54_Dimension ;
    cidoc:P2_has_type <aat:300056240> ; # weight measurement
    cidoc:P90_has_value "100"^^xsd:decimal ;
    cidoc:P91_has_unit <unit_rubbi> .

# Color feature
<feature_color_white> a cidoc:E26_Physical_Feature ;
    cidoc:P2_has_type <aat:300056130> ; # color
    cidoc:P3_has_note "white" .

# Provenance/origin
<place_ibiza> a cidoc:E53_Place ;
    cidoc:P1_is_identified_by "Ibiza" .
```

## Object Properties

Each transferred object can have multiple properties modeled using appropriate CIDOC-CRM patterns:

### 1. Object Type/Commodity

**Shortcut Property**: `gmn:P2_1_has_type`

**Full Pattern**: `E18 > P2_has_type > E55_Type`

**Controlled Vocabulary**: Recommended to use Getty AAT or custom project vocabulary

**Examples**:
- Salt: `<http://vocab.getty.edu/page/aat/300010967>`
- Wool: `<http://vocab.getty.edu/page/aat/300243430>`
- Cloth: `<http://vocab.getty.edu/page/aat/300014063>`
- Wine: `<http://vocab.getty.edu/page/aat/300379690>`

### 2. Number/Count

**Shortcut Property**: `gmn:P54_1_has_count`

**Full Pattern**: `E18 > P57_has_number_of_parts > xsd:integer`

**Data Type**: Integer

**Examples**:
```turtle
<object001> gmn:P54_1_has_count "100"^^xsd:integer .
<object002> gmn:P54_1_has_count "50"^^xsd:integer .
```

### 3. Monetary Value (L.S.D Format)

**Components**:
- Lire (pounds)
- Soldi (shillings) 
- Denari (pence)

**Properties** (custom, project-specific):
```turtle
gmn:has_monetary_value_lire
    a owl:DatatypeProperty ;
    rdfs:domain cidoc:E18_Physical_Thing ;
    rdfs:range xsd:decimal .

gmn:has_monetary_value_soldi
    a owl:DatatypeProperty ;
    rdfs:domain cidoc:E18_Physical_Thing ;
    rdfs:range xsd:integer .

gmn:has_monetary_value_denari
    a owl:DatatypeProperty ;
    rdfs:domain cidoc:E18_Physical_Thing ;
    rdfs:range xsd:integer .

gmn:has_monetary_value_currency
    a owl:ObjectProperty ;
    rdfs:domain cidoc:E18_Physical_Thing ;
    rdfs:range cidoc:E98_Currency .

gmn:has_monetary_value_provenance
    a owl:DatatypeProperty ;
    rdfs:domain cidoc:E18_Physical_Thing ;
    rdfs:range xsd:string .
```

**Example**:
```turtle
<object_cloth_001>
    gmn:has_monetary_value_lire "125.5"^^xsd:decimal ;
    gmn:has_monetary_value_soldi "10"^^xsd:integer ;
    gmn:has_monetary_value_denari "6"^^xsd:integer ;
    gmn:has_monetary_value_currency <lira_genovese> ;
    gmn:has_monetary_value_provenance "Contract text, line 23: 'precio librarum .cxxv. solidorum .x. denariorum .vi.'" .
```

**Full CIDOC-CRM Pattern** (for transformation):
```turtle
<object_cloth_001> cidoc:P43_has_dimension <object_cloth_001/value> .

<object_cloth_001/value> a cidoc:E54_Dimension ;
    cidoc:P2_has_type <aat:300055997> ; # monetary value
    cidoc:P90_has_value "125.5"^^xsd:decimal ;
    cidoc:P91_has_unit <lira_genovese> .
```

### 4. Measurement (Weight/Volume)

**Shortcut Property**: `gmn:P43_1_has_dimension`

**Full Pattern**: `E18 > P43_has_dimension > E54_Dimension > P2 (type), P90 (value), P91 (unit)`

**Dimension Types**:
- Weight: `<http://vocab.getty.edu/page/aat/300056240>`
- Volume: `<http://vocab.getty.edu/page/aat/300055624>`
- Length: `<http://vocab.getty.edu/page/aat/300055645>`

**Medieval Units** (examples):

*Weight:*
- Rubbio/Rubbi (Genoese weight ≈ 8-9 kg)
- Mina/Minae
- Cantaro/Cantari (≈ 47 kg)
- Libra/Libre (pound)

*Volume:*
- Congio/Congii
- Modio/Modii
- Barile/Barili (barrel)

*Length:*
- Palmo/Palmi (palm, ≈ 25 cm)
- Canna/Canne (≈ 2.5 m)
- Braccio/Braccia (arm's length)

**Example**:
```turtle
<object_salt_001> gmn:P43_1_has_dimension <dimension_weight_001> .

<dimension_weight_001> a cidoc:E54_Dimension ;
    cidoc:P2_has_type <aat:300056240> ; # weight
    cidoc:P90_has_value "100"^^xsd:decimal ;
    cidoc:P91_has_unit <unit_rubbi> .

<unit_rubbi> a cidoc:E58_Measurement_Unit ;
    rdfs:label "Rubbio (Genoese weight)" .
```

### 5. Color

**Shortcut Property**: `gmn:P56_1_has_color`

**Full Pattern**: `E18 > P56_bears_feature > E26_Physical_Feature > P2_has_type (color)`

**Controlled Vocabulary**:
- White (albus)
- Black (niger)
- Red (ruber)
- Blue (caeruleus)
- Green (viridis)
- Yellow (flavus)
- Brown (brunneus)
- Gray (griseus)

**Example**:
```turtle
# Shortcut
<object_cloth_001> gmn:P56_1_has_color "red" .

# Full pattern
<object_cloth_001> cidoc:P56_bears_feature <feature_color_001> .

<feature_color_001> a cidoc:E26_Physical_Feature ;
    cidoc:P2_has_type <aat:300056130> ; # color
    cidoc:P3_has_note "red (ruber)" .
```

### 6. Provenance/Origin

**Shortcut Property**: `gmn:P27_1_has_origin`

**Full Pattern**: `E18 > P27_moved_from > E53_Place`

**Usage**: Indicates where the object came from, its place of production, or its source

**Example**:
```turtle
<object_wool_001> gmn:P27_1_has_origin <place_england> .

<place_england> a cidoc:E53_Place ;
    cidoc:P1_is_identified_by "England" ;
    cidoc:P89_falls_within <place_britain> .
```

## Domain and Range

### Domain (Contracts)

The property can be used with these contract types:

```turtle
rdfs:domain [
    a owl:Class ;
    owl:unionOf (
        gmn:E31_2_Sales_Contract      # Sales of property
        gmn:E31_6_Lease_Contract       # Leases (custody transfer)
        gmn:E31_7_Donation_Contract    # Donations (gratuitous transfer)
        gmn:E31_8_Dowry_Contract       # Dowry transfers
    )
]
```

### Range (Objects)

The property can point to these object types:

```turtle
rdfs:range [
    a owl:Class ;
    owl:unionOf (
        cidoc:E18_Physical_Thing              # General physical things
        cidoc:E21_Person                      # Persons (e.g., slaves, servants)
        gmn:E22_1_Building                    # Buildings (real estate)
        gmn:E22_2_Moveable_Property          # Moveable goods
        cidoc:E24_Physical_Human-Made_Thing  # Manufactured objects
        cidoc:E53_Place                       # Places (e.g., land parcels)
    )
]
```

**Range Rationale**:

- **E18_Physical_Thing**: Most general, covers all physical objects
- **E21_Person**: For contracts involving persons (historical context: servants, slaves)
- **E22.1_Building**: Real estate, structures
- **E22.2_Moveable_Property**: Goods, merchandise, transportable items
- **E24_Physical_Human-Made_Thing**: Manufactured/crafted objects
- **E53_Place**: Land parcels, fields, vineyards

## Transformation Examples

### Example 1: Simple Object Transfer

**Input (Omeka-S shortcut):**
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_indicates_seller <merchant_giovanni> ;
    gmn:P70_2_indicates_buyer <merchant_paolo> ;
    gmn:P70_3_indicates_transferred_object <object_salt_001> .

<object_salt_001> a cidoc:E24_Physical_Human-Made_Thing ;
    gmn:P2_1_has_type <aat:300010967> ; # salt
    gmn:P54_1_has_count "100"^^xsd:integer .
```

**Output (CIDOC-CRM compliant):**
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    cidoc:P67_refers_to <contract001/acquisition> .

<contract001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <merchant_giovanni> ;
    cidoc:P22_transferred_title_to <merchant_paolo> ;
    cidoc:P140i_was_assigned_by <contract001/acquisition/attribution_001> .

<contract001/acquisition/attribution_001> a cidoc:E13_Attribute_Assignment ;
    cidoc:P177_assigned_property_of_type cidoc:P24_transferred_title_of ;
    cidoc:P141_assigned <object_salt_001> ;
    cidoc:P2_has_type <aat:300010967> . # salt

<object_salt_001> a cidoc:E24_Physical_Human-Made_Thing ;
    cidoc:P2_has_type <aat:300010967> ;
    cidoc:P57_has_number_of_parts "100"^^xsd:integer .
```

### Example 2: Object with Multiple Properties

**Input (Omeka-S shortcut):**
```turtle
<contract002> a gmn:E31_2_Sales_Contract ;
    gmn:P70_3_indicates_transferred_object <object_wool_001> .

<object_wool_001> a cidoc:E24_Physical_Human-Made_Thing ;
    gmn:P1_1_has_name "English wool" ;
    gmn:P2_1_has_type <aat:300243430> ; # wool
    gmn:P54_1_has_count "50"^^xsd:integer ;
    gmn:P43_1_has_dimension <dimension_weight_001> ;
    gmn:P56_1_has_color "white" ;
    gmn:P27_1_has_origin <place_england> ;
    gmn:has_monetary_value_lire "200.00"^^xsd:decimal ;
    gmn:has_monetary_value_currency <lira_genovese> .

<dimension_weight_001> a cidoc:E54_Dimension ;
    cidoc:P2_has_type <aat:300056240> ;
    cidoc:P90_has_value "50"^^xsd:decimal ;
    cidoc:P91_has_unit <unit_minae> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<contract002> a gmn:E31_2_Sales_Contract ;
    cidoc:P67_refers_to <contract002/acquisition> .

<contract002/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P140i_was_assigned_by <contract002/acquisition/attribution_001> .

<contract002/acquisition/attribution_001> a cidoc:E13_Attribute_Assignment ;
    cidoc:P177_assigned_property_of_type cidoc:P24_transferred_title_of ;
    cidoc:P141_assigned <object_wool_001> ;
    cidoc:P2_has_type <aat:300243430> . # wool

<object_wool_001> a cidoc:E24_Physical_Human-Made_Thing ;
    cidoc:P1_is_identified_by <object_wool_001/appellation_001> ;
    cidoc:P2_has_type <aat:300243430> ; # wool
    cidoc:P57_has_number_of_parts "50"^^xsd:integer ;
    cidoc:P43_has_dimension <dimension_weight_001> ;
    cidoc:P56_bears_feature <feature_color_white> ;
    cidoc:P27_moved_from <place_england> ;
    cidoc:P43_has_dimension <dimension_value_001> .

<object_wool_001/appellation_001> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "English wool" .

<dimension_weight_001> a cidoc:E54_Dimension ;
    cidoc:P2_has_type <aat:300056240> ;
    cidoc:P90_has_value "50"^^xsd:decimal ;
    cidoc:P91_has_unit <unit_minae> .

<feature_color_white> a cidoc:E26_Physical_Feature ;
    cidoc:P2_has_type <aat:300056130> ;
    cidoc:P3_has_note "white" .

<dimension_value_001> a cidoc:E54_Dimension ;
    cidoc:P2_has_type <aat:300055997> ; # monetary value
    cidoc:P90_has_value "200.00"^^xsd:decimal ;
    cidoc:P91_has_unit <lira_genovese> .

<place_england> a cidoc:E53_Place ;
    cidoc:P1_is_identified_by "England" .
```

### Example 3: Lease Contract (Custody Transfer)

**Input (Omeka-S shortcut):**
```turtle
<lease001> a gmn:E31_6_Lease_Contract ;
    gmn:P70_3_indicates_transferred_object <building_warehouse_001> .

<building_warehouse_001> a gmn:E22_1_Building ;
    gmn:P1_1_has_name "Warehouse at Porto" ;
    gmn:P53i_1_has_location <place_porto_genoa> .
```

**Output (CIDOC-CRM compliant with P30):**
```turtle
<lease001> a gmn:E31_6_Lease_Contract ;
    cidoc:P67_refers_to <lease001/custody_transfer> .

<lease001/custody_transfer> a cidoc:E10_Transfer_of_Custody ;
    cidoc:P140i_was_assigned_by <lease001/custody_transfer/attribution_001> .

<lease001/custody_transfer/attribution_001> a cidoc:E13_Attribute_Assignment ;
    # Note: P30 instead of P24 for custody transfer
    cidoc:P177_assigned_property_of_type cidoc:P30_transferred_custody_of ;
    cidoc:P141_assigned <building_warehouse_001> ;
    cidoc:P2_has_type <aat:300004795> . # warehouse building

<building_warehouse_001> a gmn:E22_1_Building ;
    cidoc:P1_is_identified_by <building_warehouse_001/appellation_001> ;
    cidoc:P2_has_type <aat:300004795> ; # warehouse
    cidoc:P53_has_former_or_current_location <place_porto_genoa> .

<building_warehouse_001/appellation_001> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Warehouse at Porto" .
```

### Example 4: Multiple Objects in One Contract

**Input (Omeka-S shortcut):**
```turtle
<contract003> a gmn:E31_2_Sales_Contract ;
    gmn:P70_3_indicates_transferred_object <object_salt_001> ;
    gmn:P70_3_indicates_transferred_object <object_wool_001> ;
    gmn:P70_3_indicates_transferred_object <object_wine_001> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<contract003> a gmn:E31_2_Sales_Contract ;
    cidoc:P67_refers_to <contract003/acquisition> .

<contract003/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P140i_was_assigned_by 
        <contract003/acquisition/attribution_001> ,
        <contract003/acquisition/attribution_002> ,
        <contract003/acquisition/attribution_003> .

# First object
<contract003/acquisition/attribution_001> a cidoc:E13_Attribute_Assignment ;
    cidoc:P177_assigned_property_of_type cidoc:P24_transferred_title_of ;
    cidoc:P141_assigned <object_salt_001> ;
    cidoc:P2_has_type <aat:300010967> . # salt

# Second object
<contract003/acquisition/attribution_002> a cidoc:E13_Attribute_Assignment ;
    cidoc:P177_assigned_property_of_type cidoc:P24_transferred_title_of ;
    cidoc:P141_assigned <object_wool_001> ;
    cidoc:P2_has_type <aat:300243430> . # wool

# Third object
<contract003/acquisition/attribution_003> a cidoc:E13_Attribute_Assignment ;
    cidoc:P177_assigned_property_of_type cidoc:P24_transferred_title_of ;
    cidoc:P141_assigned <object_wine_001> ;
    cidoc:P2_has_type <aat:300379690> . # wine
```

## Comparison with Related Properties

### P70.3 vs. P70.33 (Object of Donation)

| Aspect | P70.3 | P70.33 |
|--------|-------|--------|
| Scope | Multiple contract types | Donation contracts only |
| Pattern | E13 Attribute Assignment | Direct P24 on E8 |
| Object Properties | Rich properties via E13 | Simpler, direct link |
| Transformation | More complex | Simpler |
| Use When | Need object properties | Simple donation |

**Example Comparison:**

```turtle
# P70.33 (simpler)
<donation001> gmn:P70_33_indicates_object_of_donation <house001> .
# Transforms to:
<donation001> P70 > E8 > P24 > <house001>

# P70.3 (richer)
<donation001> gmn:P70_3_indicates_transferred_object <house001> .
# Transforms to:
<donation001> P67 > E8 > P140i > E13 > P141 > <house001>
#                              AND E13 > P177 > P24
#                              AND E13 > P2 > [type]
```

### P70.3 vs. P70.34 (Object of Dowry)

Similar comparison to P70.33 - P70.3 provides richer semantic structure when object properties need to be captured.

### P70.3 vs. P70.16-17 (Sale Price)

| Aspect | P70.3 | P70.16-17 |
|--------|-------|-----------|
| What | Individual object values | Overall transaction price |
| Level | Object-specific | Contract-level |
| Usage | Per-object pricing | Total consideration |
| Can Combine | Yes | Yes |

**Example:**
```turtle
<contract001>
    gmn:P70_16_documents_sale_price_amount "500.00"^^xsd:decimal ; # total
    gmn:P70_3_indicates_transferred_object <object001> . # worth 300
    gmn:P70_3_indicates_transferred_object <object002> . # worth 200
```

## Implementation Notes

### 1. Object Resource Requirements

Each object resource should have:
- **Minimum**: Type (P2_1_has_type)
- **Recommended**: Name, count, at least one measurement
- **Optional**: Color, provenance, monetary value

### 2. E13 Attribution Creation

For each `gmn:P70_3` use:
1. Create or reference activity (E8/E10)
2. Create E13_Attribute_Assignment node
3. Link E13 to activity via P140i
4. Set P177 to appropriate property (P24 or P30)
5. Set P141 to point to object
6. Set P2 to object type

### 3. URI Generation Patterns

```
Contract: <base_uri>
Activity: <base_uri>/acquisition (or /custody_transfer)
Attribution: <base_uri>/acquisition/attribution_NNN
Object: Independent URI (can be reused)
Dimension: <object_uri>/dimension_NNN
Feature: <object_uri>/feature_NNN
```

### 4. Property Type Selection Logic

```python
if contract_type == "E31_6_Lease_Contract":
    property_type = "cidoc:P30_transferred_custody_of"
    activity_type = "cidoc:E10_Transfer_of_Custody"
else:  # Sales, Donations, Dowries
    property_type = "cidoc:P24_transferred_title_of"
    activity_type = "cidoc:E8_Acquisition"
```

### 5. Multiple Objects Handling

- Create separate E13 node for each object
- All E13 nodes link to same activity
- Each E13 has unique URI
- Maintain order if relevant

### 6. Object Reuse

Objects can be linked from multiple contracts:
```turtle
<object001>
    # Property definitions...
    
# Used in multiple contracts:
<contract_001> gmn:P70_3_indicates_transferred_object <object001> .
<contract_050> gmn:P70_3_indicates_transferred_object <object001> .
<contract_125> gmn:P70_3_indicates_transferred_object <object001> .
```

## Use Cases

### Use Case 1: Commodity Sale

**Scenario**: Sale of 100 rubbi of white salt from Ibiza

```turtle
<contract_salt_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_indicates_seller <merchant_giovanni> ;
    gmn:P70_2_indicates_buyer <merchant_paolo> ;
    gmn:P70_3_indicates_transferred_object <object_salt_001> ;
    gmn:P70_16_documents_sale_price_amount "450.00"^^xsd:decimal .

<object_salt_001> a cidoc:E24_Physical_Human-Made_Thing ;
    gmn:P1_1_has_name "White salt from Ibiza" ;
    gmn:P2_1_has_type <aat:300010967> ;
    gmn:P54_1_has_count "100"^^xsd:integer ;
    gmn:P43_1_has_dimension <dimension_weight_001> ;
    gmn:P56_1_has_color "white" ;
    gmn:P27_1_has_origin <place_ibiza> ;
    gmn:has_monetary_value_lire "450.00"^^xsd:decimal .

<dimension_weight_001> a cidoc:E54_Dimension ;
    cidoc:P2_has_type <aat:300056240> ;
    cidoc:P90_has_value "100"^^xsd:decimal ;
    cidoc:P91_has_unit <unit_rubbi> .
```

### Use Case 2: Textile Sale

**Scenario**: Sale of 50 pieces of red Flemish cloth

```turtle
<contract_cloth_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_3_indicates_transferred_object <object_cloth_001> .

<object_cloth_001> a cidoc:E24_Physical_Human-Made_Thing ;
    gmn:P1_1_has_name "Red Flemish cloth" ;
    gmn:P2_1_has_type <aat:300014063> ;
    gmn:P54_1_has_count "50"^^xsd:integer ;
    gmn:P43_1_has_dimension <dimension_length_001> ;
    gmn:P56_1_has_color "red" ;
    gmn:P27_1_has_origin <place_flanders> .

<dimension_length_001> a cidoc:E54_Dimension ;
    cidoc:P2_has_type <aat:300055645> ;
    cidoc:P90_has_value "25"^^xsd:decimal ;
    cidoc:P91_has_unit <unit_canne> ;
    cidoc:P3_has_note "Per piece" .
```

### Use Case 3: Real Estate Lease

**Scenario**: Lease of warehouse building

```turtle
<lease_warehouse_001> a gmn:E31_6_Lease_Contract ;
    gmn:P70_3_indicates_transferred_object <building_warehouse_001> .

<building_warehouse_001> a gmn:E22_1_Building ;
    gmn:P1_1_has_name "Warehouse at Porto" ;
    gmn:P2_1_has_type <aat:300004795> ; # warehouse
    gmn:P53i_1_has_location <place_porto_genoa> ;
    gmn:P122_1_borders_with <building_adjacent_001> .
```

### Use Case 4: Mixed Commodity Sale

**Scenario**: Bulk sale of various goods

```turtle
<contract_mixed_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_3_indicates_transferred_object <object_salt_001> ;
    gmn:P70_3_indicates_transferred_object <object_wool_001> ;
    gmn:P70_3_indicates_transferred_object <object_wine_001> ;
    gmn:P70_16_documents_sale_price_amount "1500.00"^^xsd:decimal .

# Each object has full properties...
```

### Use Case 5: Donation with Conditions

**Scenario**: Donation of building to religious institution

```turtle
<donation_church_001> a gmn:E31_7_Donation_Contract ;
    gmn:P70_32_indicates_donor <nobleman_filippo> ;
    gmn:P70_22_indicates_receiving_party <monastery_san_lorenzo> ;
    gmn:P70_3_indicates_transferred_object <building_chapel_001> ;
    gmn:P3_1_has_editorial_note "Donation conditional on saying masses for donor's soul" .

<building_chapel_001> a gmn:E22_1_Building ;
    gmn:P1_1_has_name "Chapel of San Pietro" ;
    gmn:P2_1_has_type <aat:300000308> ; # chapel
    gmn:P53i_1_has_location <place_genoa_center> .
```

### Use Case 6: Dowry Transfer

**Scenario**: Dowry including multiple properties

```turtle
<dowry_maria_001> a gmn:E31_8_Dowry_Contract ;
    gmn:P70_32_indicates_donor <father_giacomo> ;
    gmn:P70_22_indicates_receiving_party <bride_maria> ;
    gmn:P70_3_indicates_transferred_object <house_piazza_banchi> ;
    gmn:P70_3_indicates_transferred_object <vineyard_albaro> ;
    gmn:P70_16_documents_sale_price_amount "1000.00"^^xsd:decimal .

<house_piazza_banchi> a gmn:E22_1_Building ;
    gmn:P1_1_has_name "House on Piazza Banchi" ;
    gmn:P2_1_has_type <aat:300005413> ; # house
    gmn:has_monetary_value_lire "800.00"^^xsd:decimal .

<vineyard_albaro> a cidoc:E53_Place ;
    gmn:P1_1_has_name "Vineyard in Albaro" ;
    gmn:P2_1_has_type <aat:300000371> ; # vineyard
    gmn:has_monetary_value_lire "200.00"^^xsd:decimal .
```

## AAT References

### Object Types (Common Historical Commodities)

- **Salt**: http://vocab.getty.edu/page/aat/300010967
- **Wool**: http://vocab.getty.edu/page/aat/300243430
- **Cloth/Textile**: http://vocab.getty.edu/page/aat/300014063
- **Wine**: http://vocab.getty.edu/page/aat/300379690
- **Wheat**: http://vocab.getty.edu/page/aat/300387009
- **Pepper**: http://vocab.getty.edu/page/aat/300375067
- **Wax**: http://vocab.getty.edu/page/aat/300014118
- **Oil (olive)**: http://vocab.getty.edu/page/aat/300011966
- **Leather**: http://vocab.getty.edu/page/aat/300011845
- **Wood/Timber**: http://vocab.getty.edu/page/aat/300011914

### Building Types

- **House**: http://vocab.getty.edu/page/aat/300005413
- **Warehouse**: http://vocab.getty.edu/page/aat/300004795
- **Shop**: http://vocab.getty.edu/page/aat/300005449
- **Palace**: http://vocab.getty.edu/page/aat/300005734
- **Chapel**: http://vocab.getty.edu/page/aat/300000308
- **Tower**: http://vocab.getty.edu/page/aat/300004847

### Measurement Types

- **Weight**: http://vocab.getty.edu/page/aat/300056240
- **Volume**: http://vocab.getty.edu/page/aat/300055624
- **Length**: http://vocab.getty.edu/page/aat/300055645
- **Monetary Value**: http://vocab.getty.edu/page/aat/300055997

### Color

- **Color (general)**: http://vocab.getty.edu/page/aat/300056130

### Places/Land

- **Vineyard**: http://vocab.getty.edu/page/aat/300000371
- **Field**: http://vocab.getty.edu/page/aat/300000518
- **Orchard**: http://vocab.getty.edu/page/aat/300008890

## Best Practices

### 1. Always Specify Object Type

Even if uncertain, provide best approximation:
```turtle
<object_unknown> gmn:P2_1_has_type <aat:300404126> . # "goods" general category
```

### 2. Document Uncertainty

Use notes for ambiguous information:
```turtle
<object001> 
    gmn:P2_1_has_type <aat:300014063> ; # cloth
    gmn:P3_1_has_editorial_note "Type uncertain, contract says 'res diversas' (various things)" .
```

### 3. Maintain Source Citations

Track where values come from:
```turtle
<object001>
    gmn:has_monetary_value_lire "100.00"^^xsd:decimal ;
    gmn:has_monetary_value_provenance "Contract text, folio 23r, line 15" .
```

### 4. Use Consistent Units

Within a project, standardize measurement units:
- Weight: Prefer rubbi for Genoese context
- Volume: Document local variations
- Length: Note regional differences

### 5. Separate Prices Clearly

Distinguish:
- **Object-level value**: Worth of individual item
- **Contract-level price**: Overall transaction price

### 6. Link Related Objects

For composite items:
```turtle
<cargo_ship_001>
    gmn:P70_3_indicates_transferred_object <ship_santa_maria> ;
    gmn:P70_3_indicates_transferred_object <cargo_salt_001> ;
    gmn:P70_3_indicates_transferred_object <cargo_wine_001> .
```

## Validation Checklist

Before transformation, verify:

- [ ] Each object has a type (P2_1)
- [ ] Numeric values are properly formatted
- [ ] Units are specified for all measurements
- [ ] Controlled vocabulary terms are used
- [ ] Place references are valid
- [ ] Monetary values include provenance
- [ ] Object is linked to at least one contract
- [ ] Activity type matches contract type
- [ ] Property type (P24/P30) is appropriate

## Related Documentation

- **Implementation Guide**: P70_3_Implementation_Guide.md
- **Python Transformation**: P70_3_Transformation.py
- **TTL Definitions**: P70_3_TTL_Additions.ttl
- **Main GMN Ontology**: gmn_ontology.ttl
- **Transformation Script**: gmn_to_cidoc_transform.py

---

**Version**: 1.0  
**Created**: October 28, 2025  
**Author**: Genoese Merchant Networks Project  
**CIDOC-CRM Version**: 7.x compatible
