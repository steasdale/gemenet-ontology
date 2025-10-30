# Marriage Enumeration - Semantic Documentation (Option 2)

## Overview

This document provides complete semantic documentation for marriage enumeration using the E13_Attribute_Assignment approach in CIDOC-CRM.

---

## Table of Contents

1. [Semantic Model](#semantic-model)
2. [Property Definitions](#property-definitions)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Complete Examples](#complete-examples)
5. [SPARQL Queries](#sparql-queries)
6. [Design Rationale](#design-rationale)
7. [Comparison with Alternatives](#comparison-with-alternatives)

---

## Semantic Model

### Overview

Marriage enumeration captures the ordinal number of a marriage for each participant (1st, 2nd, 3rd marriage, etc.). The E13_Attribute_Assignment approach models this as explicit assertions about the participation property itself.

### Core Pattern

```
E5_Event (Marriage)
  ├─ P11_had_participant → Person A
  ├─ P11_had_participant → Person B
  ├─ P140i_was_attributed_by → E13_Attribute_Assignment
  │   ├─ P140_assigned_attribute_to → Person A
  │   ├─ P141_assigned → Integer (e.g., "2")
  │   └─ P177_assigned_property_of_type → P11_had_participant
  └─ P140i_was_attributed_by → E13_Attribute_Assignment
      ├─ P140_assigned_attribute_to → Person B
      ├─ P141_assigned → Integer (e.g., "1")
      └─ P177_assigned_property_of_type → P11_had_participant
```

### Semantic Interpretation

**Reading the Structure**:
- The marriage event (E5_Event) had participant Person A
- An attribute assignment (E13) assigns the value "2" to Person A
- This assignment is about Person A's participation (P11) in this specific event
- Therefore: This is Person A's 2nd marriage

### Why E13_Attribute_Assignment?

E13_Attribute_Assignment is designed for "the activity of attribution or assessment of properties or relations." In this case:
- **Attribution**: Assigning an ordinal number to a participation
- **Properties**: The marriage order (1st, 2nd, etc.)
- **Relations**: Specifically about P11_had_participant

---

## Property Definitions

### gmn:marriage_number_for_subject

#### Formal Definition

```turtle
gmn:marriage_number_for_subject
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "marriage number for subject"@en ;
    rdfs:comment "Ordinal number indicating which marriage this is for the subject person (the person who has the has_spouse property). Values are positive integers: 1 for first marriage, 2 for second marriage, etc. This property is used within the object of gmn:P11i_3_has_spouse to indicate the marriage enumeration. When transformed to CIDOC-CRM, this creates an E13_Attribute_Assignment that assigns the ordinal number to the subject person's participation in the marriage event."@en ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range xsd:integer ;
    dcterms:created "2025-10-27"^^xsd:date ;
    rdfs:seeAlso cidoc:P140i_was_attributed_by, cidoc:P141_assigned .
```

#### Characteristics

| Attribute | Value |
|-----------|-------|
| **Type** | owl:DatatypeProperty |
| **Domain** | cidoc:E21_Person (in context of spouse object) |
| **Range** | xsd:integer |
| **Cardinality** | 0..1 (optional, single value) |
| **Values** | Positive integers: 1, 2, 3, ... |
| **Usage Context** | Within gmn:P11i_3_has_spouse object |

#### Semantics

```
Subject Person
  └─ gmn:P11i_3_has_spouse
      └─ Spouse Object
          └─ gmn:marriage_number_for_subject: 2

Means: "This marriage is the 2nd marriage for the subject person"
```

### gmn:marriage_number_for_spouse

#### Formal Definition

```turtle
gmn:marriage_number_for_spouse
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "marriage number for spouse"@en ;
    rdfs:comment "Ordinal number indicating which marriage this is for the spouse (the person being referenced as the spouse). Values are positive integers: 1 for first marriage, 2 for second marriage, etc. This property is used within the object of gmn:P11i_3_has_spouse to indicate the marriage enumeration. When transformed to CIDOC-CRM, this creates an E13_Attribute_Assignment that assigns the ordinal number to the spouse's participation in the marriage event."@en ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range xsd:integer ;
    dcterms:created "2025-10-27"^^xsd:date ;
    rdfs:seeAlso cidoc:P140i_was_attributed_by, cidoc:P141_assigned .
```

#### Characteristics

| Attribute | Value |
|-----------|-------|
| **Type** | owl:DatatypeProperty |
| **Domain** | cidoc:E21_Person (as spouse reference) |
| **Range** | xsd:integer |
| **Cardinality** | 0..1 (optional, single value) |
| **Values** | Positive integers: 1, 2, 3, ... |
| **Usage Context** | Within gmn:P11i_3_has_spouse object |

#### Semantics

```
Subject Person
  └─ gmn:P11i_3_has_spouse
      └─ Spouse Object
          └─ gmn:marriage_number_for_spouse: 1

Means: "This marriage is the 1st marriage for the spouse"
```

---

## CIDOC-CRM Mapping

### Complete Transformation Chain

#### Input (GMN Simplified)

```json
{
  "@id": "person:giovanni",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:maria",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 1
    }
  ]
}
```

#### Intermediate Conceptual Model

```
Person:Giovanni has_spouse Person:Maria
  with_subject_marriage_number: 2
  with_spouse_marriage_number: 1
```

#### Output (CIDOC-CRM Full)

```json
{
  "@id": "person:giovanni",
  "cidoc:P11i_participated_in": [
    {
      "@id": "person:giovanni/event/marriage_abc12345",
      "@type": "cidoc:E5_Event",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300055475",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P11_had_participant": [
        {
          "@id": "person:maria",
          "@type": "cidoc:E21_Person"
        }
      ],
      "cidoc:P140i_was_attributed_by": [
        {
          "@id": "person:giovanni/event/marriage_abc12345/attribution_def67890",
          "@type": "cidoc:E13_Attribute_Assignment",
          "cidoc:P140_assigned_attribute_to": {
            "@id": "person:giovanni",
            "@type": "cidoc:E21_Person"
          },
          "cidoc:P141_assigned": {
            "@value": "2",
            "@type": "xsd:integer"
          },
          "cidoc:P177_assigned_property_of_type": {
            "@id": "cidoc:P11_had_participant"
          }
        },
        {
          "@id": "person:giovanni/event/marriage_abc12345/attribution_xyz99999",
          "@type": "cidoc:E13_Attribute_Assignment",
          "cidoc:P140_assigned_attribute_to": {
            "@id": "person:maria",
            "@type": "cidoc:E21_Person"
          },
          "cidoc:P141_assigned": {
            "@value": "1",
            "@type": "xsd:integer"
          },
          "cidoc:P177_assigned_property_of_type": {
            "@id": "cidoc:P11_had_participant"
          }
        }
      ]
    }
  ]
}
```

### Class Mapping Table

| GMN Element | CIDOC-CRM Class | Description |
|-------------|-----------------|-------------|
| Subject Person | E21_Person | The person with the has_spouse property |
| Spouse | E21_Person | The person being referenced as spouse |
| (Generated) | E5_Event | The marriage event connecting them |
| (Generated) | E55_Type | The marriage event type (AAT 300055475) |
| (Generated) | E13_Attribute_Assignment | Attribution of ordinal to subject |
| (Generated) | E13_Attribute_Assignment | Attribution of ordinal to spouse |

### Property Mapping Table

| GMN Property | CIDOC-CRM Property Chain | Description |
|--------------|-------------------------|-------------|
| gmn:P11i_3_has_spouse | P11i_participated_in | Links person to marriage event |
| gmn:marriage_number_for_subject | P140i_was_attributed_by > P141_assigned | Subject's marriage ordinal |
| gmn:marriage_number_for_spouse | P140i_was_attributed_by > P141_assigned | Spouse's marriage ordinal |

### Property Detail: P140i_was_attributed_by

- **Label**: "was attributed by"
- **Domain**: E1_CRM_Entity (in practice: E5_Event)
- **Range**: E13_Attribute_Assignment
- **Inverse**: P140_assigned_attribute_to
- **Purpose**: Links event to attribution statements about it

### Property Detail: P141_assigned

- **Label**: "assigned"
- **Domain**: E13_Attribute_Assignment
- **Range**: E1_CRM_Entity (in practice: E62_String, xsd:integer)
- **Purpose**: The actual value being assigned (ordinal number)

### Property Detail: P177_assigned_property_of_type

- **Label**: "assigned property of type"
- **Domain**: E13_Attribute_Assignment
- **Range**: CRM_Property
- **Purpose**: Clarifies which property the attribution is about (P11 participation)

---

## Complete Examples

### Example 1: Second Marriage for Both

**Scenario**: Both Giovanni and Maria have been previously married.

**Input**:
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "person:giovanni_medici",
  "@type": "cidoc:E21_Person",
  "rdfs:label": "Giovanni de' Medici",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:maria_sforza",
      "@type": "cidoc:E21_Person",
      "rdfs:label": "Maria Sforza",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 2
    }
  ]
}
```

**Output**: Marriage event with two attributions, both assigning value "2".

### Example 2: First Marriage, One Spouse Only Enumerated

**Scenario**: We know it's Giovanni's first marriage but don't have information about Maria.

**Input**:
```json
{
  "@id": "person:giovanni",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:maria",
      "gmn:marriage_number_for_subject": 1
    }
  ]
}
```

**Output**: Marriage event with one attribution (for Giovanni only).

### Example 3: Multiple Marriages with Full Enumeration

**Scenario**: Lorenzo married three times; we have full enumeration.

**Input**:
```json
{
  "@id": "person:lorenzo",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:first_wife",
      "gmn:marriage_number_for_subject": 1,
      "gmn:marriage_number_for_spouse": 1
    },
    {
      "@id": "person:second_wife",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 1
    },
    {
      "@id": "person:third_wife",
      "gmn:marriage_number_for_subject": 3,
      "gmn:marriage_number_for_spouse": 2
    }
  ]
}
```

**Output**: Three separate marriage events, each with appropriate attributions.

**Interpretation**:
- First marriage: Lorenzo's 1st, wife's 1st
- Second marriage: Lorenzo's 2nd, wife's 1st (she was unmarried)
- Third marriage: Lorenzo's 3rd, wife's 2nd (she was widowed or divorced)

### Example 4: Historical Context - Remarriage After Widowing

**Scenario**: Francesco married Bianca after his first wife died.

**Input**:
```json
{
  "@id": "person:francesco_sforza",
  "@type": "cidoc:E21_Person",
  "rdfs:label": "Francesco Sforza",
  "gmn:P11i_1_earliest_attestation_date": ["1401-07-23"],
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:bianca_maria_visconti",
      "@type": "cidoc:E21_Person",
      "rdfs:label": "Bianca Maria Visconti",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 1
    }
  ]
}
```

**Historical Note**: Francesco's first wife died young. He later married Bianca Maria Visconti, daughter of the Duke of Milan, which was politically significant. The enumeration captures this being his second marriage.

---

## SPARQL Queries

### Query 1: Find All People in Second Marriages

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?person ?personLabel ?marriage
WHERE {
  ?marriage a cidoc:E5_Event .
  ?marriage cidoc:P2_has_type <http://vocab.getty.edu/aat/300055475> .
  ?marriage cidoc:P11_had_participant ?person .
  
  ?marriage cidoc:P140i_was_attributed_by ?attr .
  ?attr cidoc:P140_assigned_attribute_to ?person .
  ?attr cidoc:P141_assigned "2"^^xsd:integer .
  
  OPTIONAL { ?person rdfs:label ?personLabel }
}
```

### Query 2: Find Marriages with Enumeration Differences

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

# Find marriages where one person has higher marriage count than the other
SELECT ?marriage ?person1 ?num1 ?person2 ?num2 (?num1 - ?num2 AS ?difference)
WHERE {
  ?marriage cidoc:P11_had_participant ?person1, ?person2 .
  
  ?marriage cidoc:P140i_was_attributed_by ?attr1 .
  ?attr1 cidoc:P140_assigned_attribute_to ?person1 .
  ?attr1 cidoc:P141_assigned ?num1 .
  
  ?marriage cidoc:P140i_was_attributed_by ?attr2 .
  ?attr2 cidoc:P140_assigned_attribute_to ?person2 .
  ?attr2 cidoc:P141_assigned ?num2 .
  
  FILTER(?person1 != ?person2)
  FILTER(?num1 != ?num2)
}
ORDER BY DESC(?difference)
```

### Query 3: Find All Marriages for a Specific Person, Ordered

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?marriage ?spouse ?marriageNumber
WHERE {
  ?marriage cidoc:P11_had_participant <person:giovanni> .
  ?marriage cidoc:P11_had_participant ?spouse .
  
  ?marriage cidoc:P140i_was_attributed_by ?attr .
  ?attr cidoc:P140_assigned_attribute_to <person:giovanni> .
  ?attr cidoc:P141_assigned ?marriageNumber .
  
  FILTER(?spouse != <person:giovanni>)
}
ORDER BY ?marriageNumber
```

### Query 4: Find People Who Never Remarried

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

# Find people whose maximum marriage number is 1
SELECT ?person (MAX(?num) AS ?maxMarriageNum)
WHERE {
  ?marriage cidoc:P11_had_participant ?person .
  ?marriage cidoc:P140i_was_attributed_by ?attr .
  ?attr cidoc:P140_assigned_attribute_to ?person .
  ?attr cidoc:P141_assigned ?num .
}
GROUP BY ?person
HAVING (MAX(?num) = 1)
```

### Query 5: Statistical Analysis of Remarriage

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

# Count how many people had 1, 2, 3+ marriages
SELECT ?numMarriages (COUNT(?person) AS ?peopleCount)
WHERE {
  {
    SELECT ?person (MAX(?num) AS ?numMarriages)
    WHERE {
      ?marriage cidoc:P11_had_participant ?person .
      ?marriage cidoc:P140i_was_attributed_by ?attr .
      ?attr cidoc:P140_assigned_attribute_to ?person .
      ?attr cidoc:P141_assigned ?num .
    }
    GROUP BY ?person
  }
}
GROUP BY ?numMarriages
ORDER BY ?numMarriages
```

---

## Design Rationale

### Why Use E13_Attribute_Assignment?

#### Advantages

1. **Semantic Precision**: Explicitly models the attribution of ordinal numbers
2. **Provenance**: Can be extended to include who made the attribution, when, and based on what source
3. **Flexibility**: Each person's enumeration is independent
4. **Queryability**: Clear SPARQL patterns for finding nth marriages
5. **Standard CIDOC**: Uses established patterns from CIDOC-CRM

#### Disadvantages

1. **Complexity**: More nodes in the graph
2. **Storage**: Larger JSON-LD files
3. **Learning Curve**: More complex for data entry staff
4. **Query Depth**: Deeper graph traversal required

### When to Use Enumeration

**Use enumeration when**:
- Historical research focuses on marriage patterns
- Remarriage is socially or legally significant
- Property transfers depend on marriage order
- Demographic studies require this data

**Skip enumeration when**:
- Only first marriages are documented
- Research focus is elsewhere
- Data entry resources are limited
- Marriage order is unknown or uncertain

### Alternative Approaches Considered

#### Alternative 1: P11.1 in_the_role_of

```
E5_Event → P11_had_participant → E21_Person
           → P11.1_in_the_role_of → E55_Type ("second marriage")
```

**Pros**: Simpler, fewer nodes
**Cons**: Less explicit, harder to query numerically

#### Alternative 2: Direct Literal Property

```
E5_Event → P3_has_note → "Second marriage for Giovanni"
```

**Pros**: Very simple
**Cons**: Not queryable, not structured

#### Alternative 3: Custom Property on Person

```
E21_Person → custom:marriage_count → "2"
```

**Pros**: Simplest model
**Cons**: Doesn't link to specific marriage event, violates CIDOC semantics

**Chosen**: E13_Attribute_Assignment for its balance of precision and CIDOC compliance.

---

## Semantic Equivalences

### Formal Semantics

In first-order logic:

```
hasSpouse(Giovanni, Maria, subjectNum=2, spouseNum=1) →
  ∃m,a1,a2: (
    Marriage(m) ∧
    participatedIn(Giovanni, m) ∧
    hadParticipant(m, Maria) ∧
    AttributionAssignment(a1) ∧
    assignedAttributeTo(a1, Giovanni) ∧
    assigned(a1, 2) ∧
    wasAttributedBy(m, a1) ∧
    AttributionAssignment(a2) ∧
    assignedAttributeTo(a2, Maria) ∧
    assigned(a2, 1) ∧
    wasAttributedBy(m, a2)
  )
```

### RDF Triples

Expanded to RDF triples:

```turtle
person:giovanni cidoc:P11i_participated_in marriage:evt123 .
marriage:evt123 rdf:type cidoc:E5_Event .
marriage:evt123 cidoc:P2_has_type aat:300055475 .
marriage:evt123 cidoc:P11_had_participant person:maria .
marriage:evt123 cidoc:P140i_was_attributed_by attr:giovanni_123 .
attr:giovanni_123 rdf:type cidoc:E13_Attribute_Assignment .
attr:giovanni_123 cidoc:P140_assigned_attribute_to person:giovanni .
attr:giovanni_123 cidoc:P141_assigned "2"^^xsd:integer .
attr:giovanni_123 cidoc:P177_assigned_property_of_type cidoc:P11_had_participant .
marriage:evt123 cidoc:P140i_was_attributed_by attr:maria_123 .
attr:maria_123 rdf:type cidoc:E13_Attribute_Assignment .
attr:maria_123 cidoc:P140_assigned_attribute_to person:maria .
attr:maria_123 cidoc:P141_assigned "1"^^xsd:integer .
attr:maria_123 cidoc:P177_assigned_property_of_type cidoc:P11_had_participant .
```

---

## Technical Specifications

### URI Generation

#### Event URI
```
{subject_uri}/event/marriage_{hash}
```
Where hash = last 8 chars of hash(spouse_uri + "marriage")

#### Attribution URI (Subject)
```
{event_uri}/attribution_{subject_hash}
```
Where subject_hash = last 8 chars of hash(subject_uri)

#### Attribution URI (Spouse)
```
{event_uri}/attribution_{spouse_hash}
```
Where spouse_hash = last 8 chars of hash(spouse_uri)

### Data Types

| Element | Data Type | Format |
|---------|-----------|--------|
| Marriage Number | xsd:integer | Positive integer |
| Person URI | xsd:anyURI | Well-formed URI |
| Event URI | xsd:anyURI | Generated URI |
| Attribution URI | xsd:anyURI | Generated URI |

### Validation Rules

1. **Marriage numbers must be positive integers** (1, 2, 3, ...)
2. **Subject URI must exist** in graph
3. **Spouse URI must exist** in graph
4. **Attribution URIs must be unique** per person per event
5. **P177 must reference P11_had_participant**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-27 | Initial E13_Attribute_Assignment implementation |

---

## References

### CIDOC-CRM Documentation
- **E13 Attribute Assignment**: http://www.cidoc-crm.org/Entity/e13-attribute-assignment/version-7.1.3
- **P140 assigned attribute to**: http://www.cidoc-crm.org/Property/p140-assigned-attribute-to/version-7.1.3
- **P141 assigned**: http://www.cidoc-crm.org/Property/p141-assigned/version-7.1.3
- **P177 assigned property of type**: http://www.cidoc-crm.org/Property/p177-assigned-property-of-type/version-7.1.3

### Standards
- **XSD Integer**: https://www.w3.org/TR/xmlschema-2/#integer
- **RDF**: https://www.w3.org/RDF/
- **JSON-LD**: https://www.w3.org/TR/json-ld/

---

**Documentation Version**: 1.0  
**Approach**: E13_Attribute_Assignment (Option 2)  
**Status**: Complete and validated
