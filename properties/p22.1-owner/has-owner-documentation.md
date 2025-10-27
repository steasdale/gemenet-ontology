# GMN Ontology P22.1 Has Owner Property
## Complete Semantic Documentation

This document provides comprehensive semantic documentation for the `gmn:P22_1_has_owner` property, including its definition, usage patterns, transformation examples, and relationship to CIDOC-CRM.

---

## Table of Contents

1. [Property Definition](#property-definition)
2. [Semantic Specification](#semantic-specification)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Usage Guidelines](#usage-guidelines)
5. [Transformation Examples](#transformation-examples)
6. [Relationship to Other Properties](#relationship-to-other-properties)
7. [Use Cases](#use-cases)
8. [Best Practices](#best-practices)

---

## Property Definition

### Basic Information

**Property IRI**: `gmn:P22_1_has_owner`

**Label**: "P22.1 has owner"@en

**Definition**: Simplified property for expressing ownership of a building or moveable property by a person. Represents the full CIDOC-CRM path: E22_Human-Made_Object > P24i_changed_ownership_through > E8_Acquisition > P22_transferred_title_to > E21_Person.

**Purpose**: This property captures ownership relationships through acquisition events. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Applies to both buildings (E22.1) and moveable property (E22.2).

### Property Characteristics

| Characteristic | Value |
|----------------|-------|
| **Type** | `owl:ObjectProperty` |
| **Subproperty of** | `cidoc:P24i_changed_ownership_through` |
| **Domain** | `cidoc:E22_Human-Made_Object` |
| **Range** | `cidoc:E21_Person` |
| **Inverse** | Not explicitly defined |
| **Functional** | No (can have multiple owners) |
| **Created** | 2025-10-16 |

### Referenced Specifications

- **CIDOC-CRM P24i**: changed ownership through (was acquisition of)
- **CIDOC-CRM E8**: Acquisition
- **CIDOC-CRM P22**: transferred title to

---

## Semantic Specification

### Domain Restriction

**Domain**: `cidoc:E22_Human-Made_Object`

This includes:
- **gmn:E22_1_Building**: Houses, shops, warehouses, churches, etc.
- **gmn:E22_2_Moveable_Property**: Furniture, textiles, tools, merchandise, etc.

**Does NOT include**:
- Land parcels (use appropriate land properties)
- Natural features (E26_Physical_Feature)
- Abstract objects (E28_Conceptual_Object)
- Documents (E31_Document)

### Range Restriction

**Range**: `cidoc:E21_Person`

The range is restricted to persons, which means:
- ✅ Individual persons (historical or contemporary)
- ✅ Named persons with identifiers
- ❌ Organizations (use E74_Group or appropriate subclasses)
- ❌ Groups of persons (use E74_Group)
- ❌ Unspecified agents (use E39_Actor)

### Cardinality

The property has **no cardinality restrictions**:
- Can be used **zero or more times** per subject
- Multiple owners can be specified for the same object
- Each owner statement creates a separate acquisition event

---

## CIDOC-CRM Mapping

### Full CIDOC-CRM Path

The simplified property `gmn:P22_1_has_owner` represents this full CIDOC-CRM structure:

```
E22_Human-Made_Object
  ├─ P24i_changed_ownership_through ────────┐
                                             ↓
                                      E8_Acquisition
                                             ├─ P22_transferred_title_to ──→ E21_Person
                                             ├─ P4_has_time-span (optional)
                                             ├─ P7_took_place_at (optional)
                                             └─ P9_consists_of (optional)
```

### Property Alignment

| GMN Property | CIDOC Property | Class | Next Property | Class |
|--------------|----------------|-------|---------------|-------|
| **P22.1** | P24i | → E8 | P22 | → E21 |
| has owner | changed ownership through | Acquisition | transferred title to | Person |

### Why Use E8_Acquisition?

**Event-Based Modeling**: CIDOC-CRM models relationships through events rather than direct links. This allows:

1. **Temporal Context**: When was ownership acquired?
   ```turtle
   <acquisition001> cidoc:P4_has_time-span <timespan001> .
   <timespan001> cidoc:P82a_begin_of_the_begin "1445-03-15"^^xsd:date .
   ```

2. **Spatial Context**: Where did the acquisition take place?
   ```turtle
   <acquisition001> cidoc:P7_took_place_at <genoa_city> .
   ```

3. **Involved Parties**: Who witnessed or participated?
   ```turtle
   <acquisition001> cidoc:P11_had_participant <witness001> .
   ```

4. **Transfer Details**: What was transferred from whom?
   ```turtle
   <acquisition001> 
       cidoc:P23_transferred_title_from <previous_owner> ;
       cidoc:P22_transferred_title_to <new_owner> ;
       cidoc:P24_transferred_title_of <property> .
   ```

### Transformation Logic

When `gmn:P22_1_has_owner` is transformed:

1. **Create E8_Acquisition**: One acquisition event per owner
2. **Link via P24i**: Object → P24i → Acquisition
3. **Link via P22**: Acquisition → P22 → Person
4. **Generate URI**: Use hash of owner URI for uniqueness
5. **Remove shortcut**: Delete gmn:P22_1_has_owner from output

---

## Usage Guidelines

### When to Use P22.1

Use `gmn:P22_1_has_owner` when:

✅ **Documenting ownership** of buildings or moveable property  
✅ **Source explicitly states** ownership relationship  
✅ **Owner is a person** (not an organization)  
✅ **Expressing current or historical** ownership  
✅ **Multiple co-owners** need to be documented  

### When NOT to Use P22.1

Do NOT use `gmn:P22_1_has_owner` when:

❌ **Expressing occupation/residence** (use `gmn:P53_1_has_occupant`)  
❌ **Owner is an organization** (use appropriate organizational properties)  
❌ **Documenting sales transactions** (use `gmn:P70_1`, `P70_2`, `P70_3`)  
❌ **Property is land** (use land-specific properties)  
❌ **Ownership is contested** (use more complex modeling)

### Syntax Patterns

#### Pattern 1: Single Owner (URI Reference)
```turtle
<building001> a gmn:E22_1_Building ;
    gmn:P22_1_has_owner <person_giovanni> .
```

#### Pattern 2: Single Owner (Embedded Object)
```turtle
<building001> a gmn:E22_1_Building ;
    gmn:P22_1_has_owner [
        a cidoc:E21_Person ;
        gmn:P1_2_has_name_from_source "Giovanni Spinola"
    ] .
```

#### Pattern 3: Multiple Owners
```turtle
<building001> a gmn:E22_1_Building ;
    gmn:P22_1_has_owner <person_giovanni> , <person_francesco> .
```

#### Pattern 4: Owner with Full Details
```turtle
<building001> a gmn:E22_1_Building ;
    gmn:P22_1_has_owner [
        a cidoc:E21_Person ;
        rdfs:label "Maria Lomellini" ;
        gmn:P1_2_has_name_from_source "Maria Lomellini" ;
        gmn:P107i_1_has_regional_provenance <genoa>
    ] .
```

---

## Transformation Examples

### Example 1: Single Owner of a Building

**Input (GMN Shortcut)**:
```turtle
<building_spinola_house> a gmn:E22_1_Building ;
    rdfs:label "Spinola House on Vico San Giovanni" ;
    gmn:P22_1_has_owner <person_antonio_spinola> .

<person_antonio_spinola> a cidoc:E21_Person ;
    gmn:P1_2_has_name_from_source "Antonio Spinola" .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<building_spinola_house> a gmn:E22_1_Building ;
    rdfs:label "Spinola House on Vico San Giovanni" ;
    cidoc:P24i_changed_ownership_through <building_spinola_house/acquisition/ownership_7a3f2b9e> .

<building_spinola_house/acquisition/ownership_7a3f2b9e> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to <person_antonio_spinola> .

<person_antonio_spinola> a cidoc:E21_Person ;
    gmn:P1_2_has_name_from_source "Antonio Spinola" .
```

### Example 2: Multiple Owners (Joint Ownership)

**Input (GMN Shortcut)**:
```turtle
<building_lomellini_warehouse> a gmn:E22_1_Building ;
    rdfs:label "Lomellini Warehouse in Porto" ;
    gmn:P22_1_has_owner <person_stefano_lomellini> , <person_giovanni_lomellini> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<building_lomellini_warehouse> a gmn:E22_1_Building ;
    rdfs:label "Lomellini Warehouse in Porto" ;
    cidoc:P24i_changed_ownership_through 
        <building_lomellini_warehouse/acquisition/ownership_8c4d1e5f> ,
        <building_lomellini_warehouse/acquisition/ownership_2a9b6c3d> .

<building_lomellini_warehouse/acquisition/ownership_8c4d1e5f> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to <person_stefano_lomellini> .

<building_lomellini_warehouse/acquisition/ownership_2a9b6c3d> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to <person_giovanni_lomellini> .
```

**Note**: Each owner gets a separate E8_Acquisition event, allowing for different acquisition contexts if needed.

### Example 3: Moveable Property Owner

**Input (GMN Shortcut)**:
```turtle
<property_furniture_set> a gmn:E22_2_Moveable_Property ;
    rdfs:label "Bedroom furniture set" ;
    gmn:P22_1_has_owner <person_maria_doria> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<property_furniture_set> a gmn:E22_2_Moveable_Property ;
    rdfs:label "Bedroom furniture set" ;
    cidoc:P24i_changed_ownership_through <property_furniture_set/acquisition/ownership_5e7a9b2c> .

<property_furniture_set/acquisition/ownership_5e7a9b2c> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to <person_maria_doria> .
```

### Example 4: Complex Ownership with Context

This example shows how the acquisition event can be expanded with additional context:

**Input (GMN Shortcut)**:
```turtle
<building_doria_palace> a gmn:E22_1_Building ;
    rdfs:label "Doria Palace on Piazza San Matteo" ;
    gmn:P22_1_has_owner <person_giacomo_doria> .
```

**Output (CIDOC-CRM with Context)**:
```turtle
<building_doria_palace> a gmn:E22_1_Building ;
    rdfs:label "Doria Palace on Piazza San Matteo" ;
    cidoc:P24i_changed_ownership_through <building_doria_palace/acquisition/ownership_1b4c7d8e> .

<building_doria_palace/acquisition/ownership_1b4c7d8e> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to <person_giacomo_doria> ;
    # Additional context can be added:
    cidoc:P4_has_time-span [
        a cidoc:E52_Time-Span ;
        cidoc:P82a_begin_of_the_begin "1443-06-15"^^xsd:date
    ] ;
    cidoc:P7_took_place_at <genoa_city> ;
    cidoc:P23_transferred_title_from <person_previous_owner> .
```

### Example 5: Owner as Embedded Object

**Input (GMN Shortcut)**:
```turtle
<building_grimaldi_shop> a gmn:E22_1_Building ;
    rdfs:label "Grimaldi Shop on Via degli Orefici" ;
    gmn:P22_1_has_owner [
        a cidoc:E21_Person ;
        gmn:P1_2_has_name_from_source "Nicolò Grimaldi q. Luca" ;
        gmn:P97_1_has_father <person_luca_grimaldi>
    ] .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<building_grimaldi_shop> a gmn:E22_1_Building ;
    rdfs:label "Grimaldi Shop on Via degli Orefici" ;
    cidoc:P24i_changed_ownership_through <building_grimaldi_shop/acquisition/ownership_9d2e5a6b> .

<building_grimaldi_shop/acquisition/ownership_9d2e5a6b> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to [
        a cidoc:E21_Person ;
        gmn:P1_2_has_name_from_source "Nicolò Grimaldi q. Luca" ;
        gmn:P97_1_has_father <person_luca_grimaldi>
    ] .
```

**Note**: Embedded owner object with properties is preserved in the transformation.

---

## Relationship to Other Properties

### Distinction: Ownership vs. Occupation

| Aspect | P22.1 Has Owner | P53.1 Has Occupant |
|--------|-----------------|---------------------|
| **Relationship** | Legal ownership | Physical residence |
| **Rights** | Title to property | Right to occupy |
| **CIDOC Path** | P24i > E8 > P22 | P53i > E9 > P25 |
| **Event Type** | E8_Acquisition | E9_Move |
| **Can Overlap** | No (same property) | Yes (owner can also occupy) |

**Example**: A building can have both an owner and an occupant:
```turtle
<building001> a gmn:E22_1_Building ;
    gmn:P22_1_has_owner <landlord_giovanni> ;    # Legal owner
    gmn:P53_1_has_occupant <tenant_francesco> .  # Resident
```

### Integration with Sales Contracts

In sales contracts, ownership transfer is documented through:

| Property | Purpose | Contract Type |
|----------|---------|---------------|
| **P70.1** | Documents seller (previous owner) | Sales Contract |
| **P70.2** | Documents buyer (new owner) | Sales Contract |
| **P70.3** | Documents property transferred | Sales Contract |
| **P22.1** | Documents current owner | Property Record |

**Relationship**: A sales contract documents the transfer (P70.1, P70.2, P70.3), while P22.1 documents the resulting ownership state.

### Related Person Properties

Properties that can be used with the same persons:

- **P96.1 Has Mother**: Family relationships
- **P97.1 Has Father**: Family relationships
- **P11i.3 Has Spouse**: Marital relationships
- **P107i.1 Has Regional Provenance**: Geographic identity
- **P107i.2 Has Social Category**: Social class
- **P107i.3 Has Occupation**: Professional identity

---

## Use Cases

### Use Case 1: Property Registry

**Scenario**: Creating a database of property ownership in 15th-century Genoa.

**Data Entry**:
```turtle
<building_2345> a gmn:E22_1_Building ;
    gmn:P1_1_has_name "House on Vico Dritto Ponticello" ;
    gmn:P22_1_has_owner <person_antonio_cattaneo> ;
    gmn:P87_1_is_identified_by "Cart. 804, f. 89r" .
```

**Purpose**: Quick documentation of ownership relationships that can later be enriched with temporal and spatial context.

### Use Case 2: Family Property Holdings

**Scenario**: Tracking all properties owned by members of the Spinola family.

**Query Pattern**:
```sparql
SELECT ?building ?owner ?ownerName
WHERE {
    ?building gmn:P22_1_has_owner ?owner .
    ?owner gmn:P1_2_has_name_from_source ?ownerName .
    FILTER(CONTAINS(LCASE(?ownerName), "spinola"))
}
```

### Use Case 3: Co-ownership Analysis

**Scenario**: Analyzing patterns of joint property ownership.

**Data**:
```turtle
<building_A> gmn:P22_1_has_owner <person_1> , <person_2> .
<building_B> gmn:P22_1_has_owner <person_2> , <person_3> .
<building_C> gmn:P22_1_has_owner <person_1> , <person_3> .
```

**Analysis**: Network analysis of co-ownership patterns.

### Use Case 4: Dowry Property

**Scenario**: Documenting property brought as dowry and owned by women.

**Data**:
```turtle
<dowry_contract_123> a gmn:E31_3_Dowry_Contract ;
    gmn:P70_34_indicates_object_of_dowry <building_house_123> .

<building_house_123> a gmn:E22_1_Building ;
    gmn:P22_1_has_owner <person_bride_maria> ;
    gmn:P1_1_has_name "House on Via San Lorenzo" .

<person_bride_maria> a cidoc:E21_Person ;
    gmn:P1_2_has_name_from_source "Maria q. Nicolò Lomellini" ;
    gmn:P107i_2_has_social_category <noblewoman> .
```

### Use Case 5: Property Inheritance

**Scenario**: Tracking property ownership across generations.

**Data**:
```turtle
# Generation 1
<building_family_house> gmn:P22_1_has_owner <person_father_luca> .

# Generation 2 (after inheritance)
<building_family_house> gmn:P22_1_has_owner <person_son_giovanni> .

<person_son_giovanni> gmn:P97_1_has_father <person_father_luca> .
```

**Note**: Historical changes in ownership would typically require temporal modeling with time-spans.

---

## Best Practices

### 1. Use for Current State

Use P22.1 to express the current or known ownership state:

✅ **Good**: "The building is owned by Giovanni"
```turtle
<building001> gmn:P22_1_has_owner <person_giovanni> .
```

❌ **Avoid for transitions**: "The building was sold from Giovanni to Francesco"
```turtle
# Use P70.1, P70.2, P70.3 instead for sales
<sales_contract> gmn:P70_1_documents_seller <giovanni> ;
                 gmn:P70_2_documents_buyer <francesco> ;
                 gmn:P70_3_documents_transfer_of <building001> .
```

### 2. Distinguish Owner from Occupant

Always distinguish legal ownership from physical occupation:

✅ **Good**:
```turtle
<building001> gmn:P22_1_has_owner <landlord> ;      # Legal owner
              gmn:P53_1_has_occupant <tenant> .      # Resident
```

❌ **Wrong**:
```turtle
<building001> gmn:P22_1_has_owner <tenant> .  # Tenant ≠ owner
```

### 3. Document Multiple Owners Separately

For co-ownership, list each owner:

✅ **Good**:
```turtle
<building001> gmn:P22_1_has_owner <person_A> , <person_B> .
```

❌ **Wrong**:
```turtle
<building001> gmn:P22_1_has_owner "Person A and Person B" .  # String, not URI
```

### 4. Use Person URIs, Not Strings

Always use proper person identifiers:

✅ **Good**:
```turtle
<building001> gmn:P22_1_has_owner <person_giovanni_spinola> .
```

❌ **Wrong**:
```turtle
<building001> gmn:P22_1_has_owner "Giovanni Spinola" .  # String literal
```

### 5. Provide Person Details Separately

Define person properties separately from ownership:

✅ **Good**:
```turtle
<building001> gmn:P22_1_has_owner <person_maria> .

<person_maria> a cidoc:E21_Person ;
    gmn:P1_2_has_name_from_source "Maria Lomellini" ;
    gmn:P107i_1_has_regional_provenance <genoa> .
```

✅ **Also Good** (embedded):
```turtle
<building001> gmn:P22_1_has_owner [
    a cidoc:E21_Person ;
    gmn:P1_2_has_name_from_source "Maria Lomellini"
] .
```

### 6. Combine with Building Properties

Ownership is just one aspect of a building:

✅ **Good**:
```turtle
<building001> a gmn:E22_1_Building ;
    gmn:P1_1_has_name "House on Vico Dritto Ponticello" ;
    gmn:P22_1_has_owner <person_giovanni> ;
    gmn:P89_1_falls_within <genoa_district_san_lorenzo> ;
    gmn:P53_1_has_occupant <person_francesco> ;
    gmn:P87_1_is_identified_by "Cart. 804, f. 89r" .
```

### 7. Preserve Source Information

Link ownership claims to their documentary sources:

✅ **Good**:
```turtle
<building001> gmn:P22_1_has_owner <person_antonio> ;
              gmn:P87_1_is_identified_by "Notarial cart. 804, f. 89r" .
```

---

## Technical Notes

### URI Generation Algorithm

The transformation generates acquisition URIs using this algorithm:

```python
owner_uri = "http://example.org/person/giovanni"
subject_uri = "http://example.org/building001"

# Create hash
hash_input = owner_uri + 'ownership'
hash_value = hash(hash_input)
hash_suffix = str(hash_value)[-8:]  # Last 8 characters

# Generate acquisition URI
acquisition_uri = f"{subject_uri}/acquisition/ownership_{hash_suffix}"
# Result: "http://example.org/building001/acquisition/ownership_a1b2c3d4"
```

**Benefits**:
- Deterministic: Same input always produces same URI
- Unique: Hash ensures different owners get different URIs
- Consistent: Repeated transformations produce identical results
- Collision-resistant: 8-character hex provides 4.3 billion combinations

### JSON-LD Context

When using JSON-LD, ensure proper context:

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "http://example.org/building001",
  "@type": "gmn:E22_1_Building",
  "gmn:P22_1_has_owner": [
    {
      "@id": "http://example.org/person/giovanni",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

### SPARQL Queries

**Find all owners of a specific building**:
```sparql
SELECT ?owner ?ownerName
WHERE {
    <http://example.org/building001> gmn:P22_1_has_owner ?owner .
    OPTIONAL { ?owner gmn:P1_2_has_name_from_source ?ownerName }
}
```

**Find all buildings owned by a specific person**:
```sparql
SELECT ?building ?buildingName
WHERE {
    ?building gmn:P22_1_has_owner <http://example.org/person/giovanni> .
    OPTIONAL { ?building gmn:P1_1_has_name ?buildingName }
}
```

**Find co-owned buildings**:
```sparql
SELECT ?building (COUNT(?owner) as ?ownerCount)
WHERE {
    ?building gmn:P22_1_has_owner ?owner .
}
GROUP BY ?building
HAVING (COUNT(?owner) > 1)
```

---

## Validation Rules

When validating data using P22.1:

1. ✅ **Domain Check**: Subject must be E22_Human-Made_Object or subclass
2. ✅ **Range Check**: Object must be E21_Person or have @type cidoc:E21_Person
3. ✅ **URI Format**: Both subject and object should use valid URIs
4. ✅ **Transformation**: Must transform to P24i > E8 > P22 structure
5. ✅ **Uniqueness**: Each owner-object pair should generate unique acquisition URI

---

## Comparison with CIDOC-CRM Direct Modeling

### GMN Shortcut Approach

**Advantages**:
- Simple data entry
- Less verbose
- Quick documentation
- Easier for non-specialists

**Disadvantages**:
- Requires transformation
- Less expressive (no temporal/spatial context)
- Must be converted for CIDOC-CRM compliance

### Full CIDOC-CRM Approach

**Advantages**:
- Fully compliant
- Rich contextual information
- No transformation needed
- Standard ontology patterns

**Disadvantages**:
- Verbose
- Complex for data entry
- Requires deeper CIDOC-CRM knowledge
- More prone to errors

### Recommendation

Use GMN shortcuts (P22.1) for:
- Initial data entry
- Simple ownership documentation
- Quick property registries
- Teaching/learning phases

Use full CIDOC-CRM for:
- Final published datasets
- Complex temporal modeling
- Rich contextual requirements
- Interoperability with other CIDOC-CRM data

---

## Future Enhancements

Potential future developments for P22.1:

1. **Temporal Extension**: Add optional time-spans to track ownership periods
2. **Fraction Modeling**: Express fractional ownership (e.g., 1/2, 1/3)
3. **Conditional Ownership**: Model ownership with conditions or limitations
4. **Ownership Types**: Distinguish full ownership, usufruct, etc.
5. **Reverse Property**: Define explicit inverse (is_owned_by)

---

## Conclusion

The `gmn:P22_1_has_owner` property provides a practical shortcut for documenting ownership relationships while maintaining semantic alignment with CIDOC-CRM through transformation. It balances ease of use with formal rigor, making it suitable for digital humanities projects working with historical property records.

---

**Documentation Version**: 1.0  
**Last Updated**: October 2025  
**Property**: gmn:P22_1_has_owner  
**Semantic Standard**: CIDOC-CRM 7.1.1
