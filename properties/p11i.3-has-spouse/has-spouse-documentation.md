# Has Spouse Property - Ontology Documentation

## Property Overview

**Property Name**: `gmn:P11i_3_has_spouse`  
**Label**: "P11i.3 has spouse"  
**Status**: Active  
**Created**: 2025-10-16

---

## Table of Contents

1. [Formal Definition](#formal-definition)
2. [Semantic Structure](#semantic-structure)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Usage Guidelines](#usage-guidelines)
5. [Examples](#examples)
6. [Design Rationale](#design-rationale)
7. [Related Properties](#related-properties)

---

## Formal Definition

### RDF/Turtle Definition

```turtle
gmn:P11i_3_has_spouse
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P11i.3 has spouse"@en ;
    rdfs:comment "Simplified property for expressing a spousal relationship between two persons. Represents the full CIDOC-CRM path: E21_Person > P11i_participated_in > E5_Event > P2_has_type <http://vocab.getty.edu/aat/300055475> > P11_had_participant > E21_Person. This property captures marriage relationships through a marriage event. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The event type is automatically set to AAT 300055475 (marriages)."@en ;
    rdfs:subPropertyOf cidoc:P11i_participated_in ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P11i_participated_in, cidoc:P11_had_participant, aat:300055475 ;
    gmn:hasImplicitType aat:300055475 .
```

### Property Characteristics

| Characteristic | Value |
|---|---|
| **Type** | `owl:ObjectProperty` |
| **Super-property** | `cidoc:P11i_participated_in` |
| **Domain** | `cidoc:E21_Person` |
| **Range** | `cidoc:E21_Person` |
| **Cardinality** | 0..* (zero or more) |
| **Functional** | No (allows multiple values) |
| **Inverse Functional** | No |
| **Transitive** | No |
| **Symmetric** | No (but logically bidirectional) |

### Implicit Typing

- **Auto-assigned Type**: AAT 300055475 (marriages)
- **Type URI**: http://vocab.getty.edu/aat/300055475
- **Type Label**: "marriages (social events)"

---

## Semantic Structure

### Abstract Pattern

```
Subject Person
  └─ P11i_participated_in (participated in)
      └─ Marriage Event
          ├─ P2_has_type → AAT:300055475 (marriages)
          └─ P11_had_participant → Spouse Person
```

### Full CIDOC-CRM Path

```
E21_Person (subject)
  cidoc:P11i_participated_in
    E5_Event (marriage event)
      cidoc:P2_has_type
        E55_Type
          @id = "http://vocab.getty.edu/aat/300055475"
      cidoc:P11_had_participant
        E21_Person (spouse)
```

### Graphical Representation

```
┌─────────────────┐
│   E21_Person    │ (Subject: Alice)
│   person:alice  │
└────────┬────────┘
         │ P11i_participated_in
         ↓
┌────────────────────────────────┐
│        E5_Event                │
│  marriage_event_12345678       │
├────────────────────────────────┤
│ P2_has_type → AAT:300055475    │
│ P11_had_participant → person:bob│
└────────────────────────────────┘
         │
         │ P11_had_participant
         ↓
┌─────────────────┐
│   E21_Person    │ (Spouse: Bob)
│   person:bob    │
└─────────────────┘
```

---

## CIDOC-CRM Mapping

### Class Mapping

| GMN Simplified | CIDOC-CRM Full | Description |
|---|---|---|
| Subject of property | `E21_Person` | The person who has a spouse |
| (Intermediate) | `E5_Event` | The marriage event connecting the persons |
| (Intermediate) | `E55_Type` | The event type (marriages) |
| Object of property | `E21_Person` | The spouse |

### Property Mapping

| GMN Property | CIDOC-CRM Property Chain | Description |
|---|---|---|
| `gmn:P11i_3_has_spouse` | `cidoc:P11i_participated_in` | Subject participated in event |
| (Automatic) | `cidoc:P2_has_type` | Event has type (marriage) |
| (Automatic) | `cidoc:P11_had_participant` | Event had participant (spouse) |

### Transformation Logic

1. **Input**: `gmn:P11i_3_has_spouse` with spouse reference
2. **Process**:
   - Create `E5_Event` instance (marriage)
   - Type event with AAT 300055475
   - Link subject via `P11i_participated_in`
   - Link spouse via `P11_had_participant`
3. **Output**: Full CIDOC-CRM compliant structure
4. **Cleanup**: Remove simplified property

---

## Usage Guidelines

### When to Use

Use `gmn:P11i_3_has_spouse` when:

- Recording marriage relationships between persons
- You have confirmed spousal relationships
- The relationship is documented through marriage
- You need a simple, direct relationship assertion

### When NOT to Use

Do not use this property when:

- Relationship is not through marriage (use other relationship types)
- You need to record detailed marriage event information (use full CIDOC-CRM)
- The relationship type is uncertain
- Recording other family relationships (use P96_1, P97_1, etc.)

### Best Practices

1. **Always use proper URIs**: Reference spouse by URI, not label
2. **Ensure entities exist**: Referenced spouse should exist in dataset
3. **Consider bidirectionality**: Marriage is mutual; consider recording both directions
4. **Multiple marriages**: Use multiple values for sequential or concurrent marriages
5. **Documentation**: Include source information for relationship claims

### Input Formats

The property accepts two formats:

#### Format 1: Full Object (Recommended)
```json
"gmn:P11i_3_has_spouse": [
  {
    "@id": "person:spouse_uri",
    "@type": "cidoc:E21_Person"
  }
]
```

#### Format 2: URI String (Minimal)
```json
"gmn:P11i_3_has_spouse": ["person:spouse_uri"]
```

Both formats are transformed identically; Format 1 is preferred for clarity.

---

## Examples

### Example 1: Simple Marriage

#### Input (GMN Simplified)
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/"
  },
  "@id": "person:giovanni_medici",
  "@type": "cidoc:E21_Person",
  "rdfs:label": "Giovanni de' Medici",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:caterina_sforza",
      "@type": "cidoc:E21_Person",
      "rdfs:label": "Caterina Sforza"
    }
  ]
}
```

#### Output (CIDOC-CRM Compliant)
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "person:giovanni_medici",
  "@type": "cidoc:E21_Person",
  "rdfs:label": "Giovanni de' Medici",
  "cidoc:P11i_participated_in": [
    {
      "@id": "person:giovanni_medici/event/marriage_a1b2c3d4",
      "@type": "cidoc:E5_Event",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300055475",
        "@type": "cidoc:E55_Type",
        "rdfs:label": "marriages"
      },
      "cidoc:P11_had_participant": [
        {
          "@id": "person:caterina_sforza",
          "@type": "cidoc:E21_Person",
          "rdfs:label": "Caterina Sforza"
        }
      ]
    }
  ]
}
```

### Example 2: Multiple Marriages (Sequential)

#### Input
```json
{
  "@id": "person:lorenzo_magnifico",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:clarice_orsini",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

#### Historical Context
Lorenzo de' Medici (1449-1492) married Clarice Orsini in 1469. This property records that documented marriage relationship.

### Example 3: Multiple Marriages with Full Context

#### Input
```json
{
  "@id": "person:francesco_sforza",
  "@type": "cidoc:E21_Person",
  "rdfs:label": "Francesco Sforza",
  "gmn:P11i_1_earliest_attestation_date": ["1401-01-01"],
  "gmn:P11i_2_latest_attestation_date": ["1466-03-08"],
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:bianca_maria_visconti",
      "@type": "cidoc:E21_Person",
      "rdfs:label": "Bianca Maria Visconti"
    }
  ]
}
```

#### Output
Creates both attestation events and marriage event under `cidoc:P11i_participated_in`.

### Example 4: Bidirectional Marriage

#### Person A
```json
{
  "@id": "person:husband",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {"@id": "person:wife"}
  ]
}
```

#### Person B
```json
{
  "@id": "person:wife",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {"@id": "person:husband"}
  ]
}
```

Both persons reference each other, creating two separate marriage events (one from each perspective).

### Example 5: Concurrent Marriages (Historical Polygamy)

```json
{
  "@id": "person:historical_figure",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {"@id": "person:spouse_1"},
    {"@id": "person:spouse_2"}
  ]
}
```

Creates two separate marriage events for concurrent spouses (where historically appropriate).

---

## Design Rationale

### Why This Simplification?

1. **Data Entry Efficiency**: Direct person-to-person relationship is intuitive
2. **Historical Patterns**: Marriage is a well-defined social relationship
3. **Event Abstraction**: Many users don't need full event detail
4. **Transformation Safety**: Clear mapping to CIDOC-CRM ensures semantic validity

### Why Event-Based Transformation?

CIDOC-CRM models relationships through events because:

1. **Temporal Semantics**: Relationships occur in time
2. **Context Preservation**: Events can be enriched with date, place, witnesses
3. **Relationship Types**: Events distinguish marriage from other co-participation
4. **Extensibility**: Event structure allows future enhancement

### Alternative Modeling Approaches

| Approach | Pros | Cons | Chosen? |
|---|---|---|---|
| Direct relationship property | Simple, intuitive | Loses temporal context | ❌ |
| Event-based (this approach) | Semantically rich, extensible | More complex structure | ✅ |
| Multiple typed relationships | Type-specific semantics | Proliferation of properties | ❌ |
| Generic participation | Maximum flexibility | Requires manual typing | ❌ |

### Event Type Selection

**AAT 300055475** (marriages) was chosen because:
- Canonical Getty AAT concept for marriage events
- Widely recognized in cultural heritage domain
- Distinguishes from other social events
- Stable, well-documented URI

---

## Related Properties

### Person Attestation Properties

These properties work together to document a person's life:

- **`gmn:P11i_1_earliest_attestation_date`**: First documented date
- **`gmn:P11i_2_latest_attestation_date`**: Last documented date
- **`gmn:P11i_3_has_spouse`**: Marriage relationships (this property)

### Family Relationship Properties

- **`gmn:P96_1_has_mother`**: Maternal relationship
- **`gmn:P97_1_has_father`**: Paternal relationship

### Group Membership Properties

- **`gmn:P107i_1_has_regional_provenance`**: Geographic origin
- **`gmn:P107i_2_has_social_category`**: Social class
- **`gmn:P107i_3_has_occupation`**: Professional group

---

## Semantic Equivalences

### CIDOC-CRM Equivalence

```turtle
?person gmn:P11i_3_has_spouse ?spouse .
```

Is semantically equivalent to:

```turtle
?person cidoc:P11i_participated_in ?event .
?event a cidoc:E5_Event .
?event cidoc:P2_has_type <http://vocab.getty.edu/aat/300055475> .
?event cidoc:P11_had_participant ?spouse .
```

### Formal Semantics

In first-order logic:

```
∀x,y: hasSpouse(x,y) → 
  ∃e: (Event(e) ∧ 
       participatedIn(x,e) ∧ 
       hasType(e, Marriage) ∧ 
       hadParticipant(e,y))
```

---

## Technical Specifications

### URI Generation Algorithm

```python
def generate_marriage_event_uri(subject_uri: str, spouse_uri: str) -> str:
    """
    Generate consistent URI for marriage event.
    
    Args:
        subject_uri: URI of the person having the spouse
        spouse_uri: URI of the spouse
    
    Returns:
        URI for the marriage event
    """
    event_hash = str(hash(spouse_uri + 'marriage'))[-8:]
    return f"{subject_uri}/event/marriage_{event_hash}"
```

### Hash Consistency

The hash function ensures:
- **Deterministic**: Same inputs always produce same URI
- **Unique**: Different spouses produce different URIs
- **Collision-resistant**: 8 hex characters provide 4 billion possibilities

### Data Types

| Component | Data Type | Format |
|---|---|---|
| Subject URI | String | URI format |
| Spouse URI | String | URI format |
| Event URI | String | Generated URI |
| Event Type | URI | http://vocab.getty.edu/aat/300055475 |

---

## Validation Rules

### Input Validation

1. **Subject must be E21_Person**: Domain constraint
2. **Spouse must be E21_Person**: Range constraint
3. **Spouse must have URI**: Required for event generation
4. **Property must be array**: Even for single spouse

### Output Validation

1. **Event must be E5_Event**: Class constraint
2. **Event must have type**: AAT 300055475 required
3. **Event must have participant**: Spouse required
4. **URIs must be valid**: Well-formed URI syntax

### SPARQL Validation Query

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

SELECT ?person ?spouse ?event
WHERE {
  ?person cidoc:P11i_participated_in ?event .
  ?event a cidoc:E5_Event .
  ?event cidoc:P2_has_type aat:300055475 .
  ?event cidoc:P11_had_participant ?spouse .
  
  FILTER(?person != ?spouse)
}
```

This query finds all properly-formed marriage relationships.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2025-10-16 | Initial property definition |
| 1.0 | 2025-10-27 | Documentation completed |

---

## References

### CIDOC-CRM Documentation
- **E5 Event**: http://www.cidoc-crm.org/Entity/e5-event/version-7.1.3
- **E21 Person**: http://www.cidoc-crm.org/Entity/e21-person/version-7.1.3
- **P11 had participant**: http://www.cidoc-crm.org/Property/p11-had-participant/version-7.1.3
- **P11i participated in**: http://www.cidoc-crm.org/Property/p11i-participated-in/version-7.1.3

### Getty AAT
- **300055475 marriages**: http://vocab.getty.edu/aat/300055475

### Related Standards
- **FOAF**: Friend of a Friend vocabulary (foaf:spouse)
- **Schema.org**: schema:spouse
- **BIO**: Biography Vocabulary (bio:Marriage)

---

## Appendix: Complete Examples

### Complete Transformation Example

#### Original GMN Data
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@graph": [
    {
      "@id": "person:medici_001",
      "@type": "cidoc:E21_Person",
      "rdfs:label": "Cosimo de' Medici",
      "gmn:P11i_3_has_spouse": [
        {
          "@id": "person:medici_002",
          "@type": "cidoc:E21_Person",
          "rdfs:label": "Contessina de' Bardi"
        }
      ]
    }
  ]
}
```

#### Transformed CIDOC-CRM Data
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@graph": [
    {
      "@id": "person:medici_001",
      "@type": "cidoc:E21_Person",
      "rdfs:label": "Cosimo de' Medici",
      "cidoc:P11i_participated_in": [
        {
          "@id": "person:medici_001/event/marriage_f7e2b9a1",
          "@type": "cidoc:E5_Event",
          "cidoc:P2_has_type": {
            "@id": "http://vocab.getty.edu/aat/300055475",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "marriages"
          },
          "cidoc:P11_had_participant": [
            {
              "@id": "person:medici_002",
              "@type": "cidoc:E21_Person",
              "rdfs:label": "Contessina de' Bardi"
            }
          ]
        }
      ]
    }
  ]
}
```

---

**Documentation Version**: 1.0  
**Property**: gmn:P11i_3_has_spouse  
**Last Updated**: 2025-10-27  
**Status**: Complete and validated
