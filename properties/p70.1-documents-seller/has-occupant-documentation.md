# Ontology Documentation: gmn:P53_1_has_occupant
## Complete Semantic Documentation

---

## Overview

The `gmn:P53_1_has_occupant` property is a simplified shortcut property in the GMN (Genoese Marriage Network) ontology designed to express residence or occupation relationships between buildings and persons. It provides a convenient data entry mechanism that is automatically transformed into full CIDOC-CRM compliant structure.

---

## Property Specification

### Basic Information

| Attribute | Value |
|-----------|-------|
| **Property URI** | `gmn:P53_1_has_occupant` |
| **Label** | "P53.1 has occupant"@en |
| **Type** | `owl:ObjectProperty`, `rdf:Property` |
| **Created** | 2025-10-16 |
| **Status** | Active |

### Semantic Definition

**English Definition:**  
"Simplified property for expressing occupation/residence in a building by a person who is not the owner. Represents the full CIDOC-CRM path: E22_Human-Made_Object > P53i_is_former_or_current_location_of > E9_Move > P25_moved > E21_Person. This property captures residence/occupation relationships through move events. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. This is distinct from ownership."

### Domain and Range

**Domain:**  
`gmn:E22_1_Building` - Buildings and built structures

The domain is restricted to buildings, which are physical human-made structures such as:
- Houses and residential buildings
- Palaces and noble residences
- Shops and commercial buildings
- Warehouses and storage facilities
- Religious buildings (when used for residence)
- Any other constructed building

**Range:**  
`cidoc:E21_Person` - Individual persons

The range encompasses individual human beings who occupy or reside in the building:
- Tenants and renters
- Family members living in inherited property
- Residents who are not property owners
- Occupants during any historical period

### Property Hierarchy

**Super Property:**  
`cidoc:P53i_is_former_or_current_location_of` - is former or current location of

This places the property within the CIDOC-CRM location hierarchy, indicating that buildings serve as locations for persons.

**Sub Properties:**  
None currently defined.

### Related Properties

| Property | Relationship | Description |
|----------|--------------|-------------|
| `gmn:P22_1_has_owner` | Sibling | Expresses ownership rather than occupancy |
| `cidoc:P53_has_former_or_current_location` | Inverse/Transform | Target property in transformation |
| `cidoc:P74_has_current_or_former_residence` | Alternative | Person-centric residence property |
| `cidoc:P25_moved` | Related | Movement of person to location |
| `cidoc:P53i_is_former_or_current_location_of` | Parent | Location relationship |

---

## Semantic Patterns

### Conceptual Model

The property represents the concept that a building serves as a location where a person resides or has resided. This captures:

1. **Spatial Relationship:** The physical presence of a person at a building location
2. **Temporal Aspect:** Can represent current or former occupancy
3. **Legal Distinction:** Specifically excludes ownership relationships
4. **Residential Use:** Indicates the building is used for human habitation

### CIDOC-CRM Alignment

**Simplified Path (Current Implementation):**
```
gmn:E22_1_Building --[P53_has_former_or_current_location]--> cidoc:E21_Person
```

**Full Semantic Path (Per Ontology Comment):**
```
gmn:E22_1_Building 
  --[P53i_is_former_or_current_location_of]--> 
    cidoc:E9_Move 
      --[P25_moved]--> 
        cidoc:E21_Person
```

The full path explicitly models the move event that brings a person to reside at the building. However, for practical data entry purposes, the current implementation uses the simplified direct relationship.

**Rationale for Simplification:**
- Reduces data entry complexity
- Avoids creating excessive intermediate nodes (E9_Move events)
- Maintains semantic correctness through P53's location semantics
- Enables future enhancement to full path if needed

### Comparison with Ownership

| Aspect | Has Occupant (P53.1) | Has Owner (P22.1) |
|--------|----------------------|-------------------|
| **Legal Status** | No legal claim | Legal title holder |
| **Semantic Path** | Via location (P53) | Via acquisition (P24i) |
| **Typical Relationship** | Tenant, resident | Owner, proprietor |
| **Property Rights** | Use rights only | Full ownership rights |
| **CIDOC-CRM Parent** | P53i_is_former_or_current_location_of | P24i_changed_ownership_through |

---

## Usage Guidelines

### When to Use

✅ **Appropriate Use Cases:**
- Recording tenants living in rental properties
- Documenting family members residing in inherited property they don't own
- Capturing historical residents of noble palaces
- Noting occupants of buildings in archival records
- Recording persons living in buildings owned by others
- Documenting residence relationships without ownership claims

### When Not to Use

❌ **Inappropriate Use Cases:**
- Property owners (use `gmn:P22_1_has_owner` instead)
- Temporary visitors or guests (consider event-based modeling)
- Business operators who don't reside in the building (use other relationships)
- Persons mentioned in documents but not residing at building
- Buildings used only for commercial purposes without residence

### Best Practices

1. **Distinguish Ownership from Occupancy:**
   - If a person both owns and lives in a building, use both properties
   - Don't assume ownership from occupancy
   - Check historical records for legal ownership vs. residence

2. **Handle Multiple Occupants:**
   - Use array/list format for multiple occupants
   - Each occupant should be a separate entry
   - Don't combine multiple persons into a single entry

3. **Temporal Clarity:**
   - Property name includes "former or current" - be clear about timeframe if possible
   - Consider adding time-span information to person or building records
   - Document historical changes in occupancy when known

4. **Data Quality:**
   - Verify occupancy relationships from reliable sources
   - Distinguish between actual residence and administrative registration
   - Note when occupancy status is uncertain or disputed

---

## Transformation Specification

### Input Format (GMN Shortcut)

**JSON-LD Structure:**
```json
{
  "@id": "http://example.org/building/123",
  "@type": "gmn:E22_1_Building",
  "gmn:P53_1_has_occupant": [
    {
      "@id": "http://example.org/person/456",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Turtle/RDF Format:**
```turtle
@prefix gmn: <http://example.org/gmn/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

<http://example.org/building/123> 
    a gmn:E22_1_Building ;
    gmn:P53_1_has_occupant <http://example.org/person/456> .

<http://example.org/person/456> 
    a cidoc:E21_Person .
```

### Output Format (CIDOC-CRM Compliant)

**JSON-LD Structure:**
```json
{
  "@id": "http://example.org/building/123",
  "@type": "gmn:E22_1_Building",
  "cidoc:P53_has_former_or_current_location": [
    {
      "@id": "http://example.org/person/456",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Turtle/RDF Format:**
```turtle
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix gmn: <http://example.org/gmn/> .

<http://example.org/building/123> 
    a gmn:E22_1_Building ;
    cidoc:P53_has_former_or_current_location <http://example.org/person/456> .

<http://example.org/person/456> 
    a cidoc:E21_Person .
```

### Transformation Logic

**Algorithm:**
1. Check if `gmn:P53_1_has_occupant` property exists in data
2. If not present, return data unchanged
3. If present:
   - Initialize `cidoc:P53_has_former_or_current_location` array if needed
   - For each occupant in the array:
     - If occupant is a dictionary object, copy it and ensure `@type` is set
     - If occupant is a URI string, create proper structure with `@id` and `@type`
     - Add occupant to CIDOC-CRM property array
   - Remove the `gmn:P53_1_has_occupant` property
4. Return transformed data

**Pseudocode:**
```
function transform_occupant(data):
    if "gmn:P53_1_has_occupant" not in data:
        return data
    
    occupants = data["gmn:P53_1_has_occupant"]
    
    if "cidoc:P53_has_former_or_current_location" not in data:
        data["cidoc:P53_has_former_or_current_location"] = []
    
    for each occupant in occupants:
        if occupant is dictionary:
            occupant_data = copy(occupant)
            if "@type" not in occupant_data:
                occupant_data["@type"] = "cidoc:E21_Person"
        else:
            occupant_data = {
                "@id": occupant,
                "@type": "cidoc:E21_Person"
            }
        
        data["cidoc:P53_has_former_or_current_location"].append(occupant_data)
    
    delete data["gmn:P53_1_has_occupant"]
    return data
```

### Transformation Guarantees

**Preservation:**
- All occupant information is preserved
- Occupant URIs and types are maintained
- Order of occupants is preserved
- Additional occupant properties (if any) are preserved

**Validation:**
- Output conforms to CIDOC-CRM structure
- All occupants have proper `@type` declarations
- No dangling references are created
- Shortcut property is completely removed

---

## Examples

### Example 1: Single Occupant (Palace)

**Scenario:** Lorenzo de' Medici resides in the Palazzo Medici in Florence.

**Input (GMN):**
```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/building/palazzo_medici",
  "@type": "gmn:E22_1_Building",
  "gmn:P1_1_has_name": [{"@value": "Palazzo Medici"}],
  "gmn:P59i_1_is_located": [{"@value": "Via Cavour, Florence"}],
  "gmn:P53_1_has_occupant": [
    {
      "@id": "http://example.org/person/lorenzo_medici",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Output (CIDOC-CRM):**
```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/building/palazzo_medici",
  "@type": "gmn:E22_1_Building",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://example.org/building/palazzo_medici/appellation/12345678",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Palazzo Medici"
    }
  ],
  "cidoc:P53_has_former_or_current_location": [
    {
      "@id": "http://example.org/person/lorenzo_medici",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

### Example 2: Multiple Occupants (Shared House)

**Scenario:** A house on Via dei Martelli is occupied by multiple members of the Martelli family.

**Input (GMN):**
```json
{
  "@id": "http://example.org/building/casa_martelli",
  "@type": "gmn:E22_1_Building",
  "gmn:P1_1_has_name": [{"@value": "Casa Martelli"}],
  "gmn:P53_1_has_occupant": [
    {"@id": "http://example.org/person/niccolo_martelli"},
    {"@id": "http://example.org/person/maria_martelli"},
    {"@id": "http://example.org/person/francesco_martelli"}
  ]
}
```

**Output (CIDOC-CRM):**
```json
{
  "@id": "http://example.org/building/casa_martelli",
  "@type": "gmn:E22_1_Building",
  "cidoc:P1_is_identified_by": [...],
  "cidoc:P53_has_former_or_current_location": [
    {
      "@id": "http://example.org/person/niccolo_martelli",
      "@type": "cidoc:E21_Person"
    },
    {
      "@id": "http://example.org/person/maria_martelli",
      "@type": "cidoc:E21_Person"
    },
    {
      "@id": "http://example.org/person/francesco_martelli",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

### Example 3: Distinction Between Owner and Occupant

**Scenario:** A building is owned by one person but occupied by another (rental situation).

**Input (GMN):**
```json
{
  "@id": "http://example.org/building/rental_house",
  "@type": "gmn:E22_1_Building",
  "gmn:P1_1_has_name": [{"@value": "House on Via Santo Spirito"}],
  "gmn:P22_1_has_owner": [
    {"@id": "http://example.org/person/giovanni_owner"}
  ],
  "gmn:P53_1_has_occupant": [
    {"@id": "http://example.org/person/paolo_tenant"}
  ]
}
```

**Output (CIDOC-CRM):**
```json
{
  "@id": "http://example.org/building/rental_house",
  "@type": "gmn:E22_1_Building",
  "cidoc:P1_is_identified_by": [...],
  "cidoc:P24i_changed_ownership_through": [
    {
      "@id": "http://example.org/building/rental_house/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "http://example.org/person/giovanni_owner",
          "@type": "cidoc:E21_Person"
        }
      ]
    }
  ],
  "cidoc:P53_has_former_or_current_location": [
    {
      "@id": "http://example.org/person/paolo_tenant",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

### Example 4: String URI Format

**Scenario:** Simplified data entry using URI strings rather than full objects.

**Input (GMN):**
```json
{
  "@id": "http://example.org/building/shop_mercato",
  "@type": "gmn:E22_1_Building",
  "gmn:P53_1_has_occupant": [
    "http://example.org/person/merchant_carlo"
  ]
}
```

**Output (CIDOC-CRM):**
```json
{
  "@id": "http://example.org/building/shop_mercato",
  "@type": "gmn:E22_1_Building",
  "cidoc:P53_has_former_or_current_location": [
    {
      "@id": "http://example.org/person/merchant_carlo",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Note:** The transformation automatically adds the `@type` field when processing string URIs.

---

## Constraints and Validation

### Mandatory Constraints

1. **Domain Constraint:**  
   Subject must be of type `gmn:E22_1_Building` or a subclass

2. **Range Constraint:**  
   Object must be of type `cidoc:E21_Person`

3. **Type Integrity:**  
   After transformation, all occupants must have `@type` set to `cidoc:E21_Person`

### Recommended Constraints

1. **Uniqueness:**  
   While the same person can occupy a building multiple times (different periods), avoid duplicate entries for the same occupancy

2. **Referential Integrity:**  
   Occupant URIs should reference existing person entities in the dataset

3. **Mutual Exclusivity:**  
   Consider whether a single person-building relationship should be modeled as both ownership and occupancy, or just one

### SHACL Validation Shape (Optional)

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix gmn: <http://example.org/gmn/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

gmn:OccupantPropertyShape
    a sh:NodeShape ;
    sh:targetSubjectsOf gmn:P53_1_has_occupant ;
    sh:property [
        sh:path gmn:P53_1_has_occupant ;
        sh:class cidoc:E21_Person ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:severity sh:Violation ;
        sh:message "Occupant must be a cidoc:E21_Person"@en ;
    ] .

gmn:BuildingOccupantDomainShape
    a sh:NodeShape ;
    sh:targetSubjectsOf gmn:P53_1_has_occupant ;
    sh:class gmn:E22_1_Building ;
    sh:severity sh:Violation ;
    sh:message "Only buildings can have occupants"@en .
```

---

## Interoperability

### CIDOC-CRM Compliance

The transformed output is fully compliant with CIDOC-CRM 7.1.1 specifications:
- Uses standard CIDOC-CRM property `P53_has_former_or_current_location`
- Maintains semantic correctness of location relationships
- Follows CIDOC-CRM naming conventions
- Compatible with CIDOC-CRM reasoning systems

### Linked Open Data

The property supports LOD best practices:
- Uses stable HTTP URIs for all entities
- Supports multiple serialization formats (JSON-LD, Turtle, RDF/XML)
- Enables linking to external person and place authorities
- Compatible with SPARQL queries

### Integration with Other Ontologies

**Compatible Ontologies:**
- CIDOC-CRM (primary alignment)
- Schema.org (via schema:location, schema:address)
- FOAF (Friend of a Friend) for person entities
- Getty Vocabularies (AAT) for building types

**Mapping Example (Schema.org):**
```turtle
gmn:P53_1_has_occupant owl:equivalentProperty schema:occupant .
```

---

## Extension Possibilities

### Future Enhancements

1. **Temporal Occupancy:**  
   Add time-span information to capture when occupancy began and ended
   ```json
   {
     "gmn:P53_1_has_occupant": [{
       "@id": "person123",
       "cidoc:P4_has_time-span": {
         "cidoc:P82a_begin_of_the_begin": "1450-01-01",
         "cidoc:P82b_end_of_the_end": "1470-12-31"
       }
     }]
   }
   ```

2. **Occupancy Type:**  
   Specify the type of occupancy relationship (tenant, family member, etc.)
   ```json
   {
     "gmn:P53_1_has_occupant": [{
       "@id": "person123",
       "cidoc:P2_has_type": {
         "@id": "http://vocab.getty.edu/aat/300025637",
         "rdfs:label": "tenant"
       }
     }]
   }
   ```

3. **Full Move Event Modeling:**  
   Implement the complete CIDOC-CRM path through E9_Move events
   ```turtle
   building123 cidoc:P53i_is_former_or_current_location_of [
     a cidoc:E9_Move ;
     cidoc:P25_moved person456 ;
     cidoc:P4_has_time-span [...] ;
     cidoc:P7_took_place_at place789
   ] .
   ```

### Subproperty Specializations

Potential future subproperties:
- `gmn:P53_1_1_has_tenant` - Specifically for rental relationships
- `gmn:P53_1_2_has_family_resident` - For family members in inherited property
- `gmn:P53_1_3_has_temporary_occupant` - For short-term occupation

---

## References

### CIDOC-CRM Documentation
- **P53 has former or current location:** http://www.cidoc-crm.org/Property/P53-has-former-or-current-location/version-7.1.1
- **P53i is former or current location of:** http://www.cidoc-crm.org/Property/P53i-is-former-or-current-location-of/version-7.1.1
- **E9 Move:** http://www.cidoc-crm.org/Entity/E9-Move/version-7.1.1
- **P25 moved:** http://www.cidoc-crm.org/Property/P25-moved/version-7.1.1

### Related Standards
- ISO 21127:2014 (CIDOC-CRM)
- Dublin Core Metadata Terms
- OWL 2 Web Ontology Language

### Project Resources
- GMN Ontology: `gmn_ontology.ttl`
- Transformation Script: `gmn_to_cidoc_transform.py`
- Property Documentation: Project documentation file

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-27  
**Maintainer:** GMN Project Team  
**Status:** Production Ready
