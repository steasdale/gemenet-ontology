# Ontology Documentation: gmn:P11i_1_earliest_attestation_date

## Complete Semantic Documentation

This document provides comprehensive semantic documentation for the `gmn:P11i_1_earliest_attestation_date` property, including its formal definition, CIDOC-CRM mapping, usage guidelines, and examples.

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Formal Definition](#formal-definition)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Semantic Interpretation](#semantic-interpretation)
5. [Usage Guidelines](#usage-guidelines)
6. [Transformation Examples](#transformation-examples)
7. [Related Properties](#related-properties)
8. [Use Cases](#use-cases)

---

## Property Overview

### Basic Information

| Attribute | Value |
|-----------|-------|
| **Property IRI** | `gmn:P11i_1_earliest_attestation_date` |
| **Label** | "P11i.1 earliest attestation date" |
| **Property Type** | `owl:DatatypeProperty`, `rdf:Property` |
| **Domain** | `cidoc:E21_Person` |
| **Range** | `xsd:date` |
| **Superproperty** | `cidoc:P11i_participated_in` |
| **Created** | 2025-10-16 |

### Purpose Statement

This property captures the earliest date at which a person is documented or attested to have been alive in historical sources. It represents the first known documentary evidence of a person's existence, which is crucial for prosopographical research and establishing chronological boundaries for historical figures.

### Design Rationale

The property is designed as a **shortcut** for data entry convenience while maintaining semantic precision through transformation to full CIDOC-CRM structure. This approach:

1. **Simplifies data entry** - Users can record dates directly without creating intermediate event and time-span nodes
2. **Preserves semantic precision** - Transformation expands to full CIDOC-CRM event-based temporal model
3. **Maintains CIDOC-CRM compliance** - Output is fully conformant with CIDOC-CRM specifications
4. **Supports reasoning** - Explicit event structure enables temporal reasoning and queries

---

## Formal Definition

### RDF/OWL Definition

```turtle
@prefix gmn: <http://genoa-medieval-notarial.org/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

# Property: P11i.1 earliest attestation date
gmn:P11i_1_earliest_attestation_date
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P11i.1 earliest attestation date"@en ;
    rdfs:comment "Simplified property for expressing the earliest date at which a person is documented or attested to have been alive in historical sources. Represents the full CIDOC-CRM path: E21_Person > P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82a_begin_of_the_begin. This property captures the earliest known documentary evidence of a person's existence. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P11i_participated_in ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range xsd:date ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P11i_participated_in, cidoc:P4_has_time-span, cidoc:P82a_begin_of_the_begin .
```

### Property Characteristics

**Functional**: No - A person may have multiple earliest attestation dates recorded from different sources  
**Inverse Functional**: No  
**Transitive**: No  
**Symmetric**: No  
**Asymmetric**: No  
**Reflexive**: No  
**Irreflexive**: Yes

---

## CIDOC-CRM Mapping

### Complete Expansion Path

```
E21_Person 
  ↓ [cidoc:P11i_participated_in]
  E5_Event (attestation event)
    ↓ [cidoc:P4_has_time-span]
    E52_Time-Span
      ↓ [cidoc:P82a_begin_of_the_begin]
      xsd:date (earliest attestation date value)
```

### Property Chain Axiom

If expressed as an OWL property chain:

```turtle
gmn:P11i_1_earliest_attestation_date owl:propertyChainAxiom (
    cidoc:P11i_participated_in
    cidoc:P4_has_time-span
    cidoc:P82a_begin_of_the_begin
) .
```

### Involved CIDOC-CRM Classes

#### E21 Person
**Definition**: This class comprises real persons who live or are assumed to have lived.  
**Scope Note**: Persons may be either individuals or groups that are treated as units (corporations, communities).  
**Examples**: Giovanni Rossi, Caterina Spinola

#### E5 Event
**Definition**: This class comprises changes of states in cultural, social, or physical systems.  
**Scope Note**: Events are limited in duration (begin and end) and are instances that can be located in space-time.  
**Examples**: An attestation in a notarial document, appearance as witness

#### E52 Time-Span
**Definition**: This class comprises abstract temporal extents having a beginning, an end, and a duration.  
**Scope Note**: Time-Spans may be identified by any number of culturally distinct date forms.  
**Examples**: 15 March 1450, The year 1450

### Involved CIDOC-CRM Properties

#### P11i participated in (participated in)
**Domain**: E39 Actor  
**Range**: E5 Event  
**Superproperty**: P12i was present at  
**Inverse**: P11 had participant  
**Definition**: This property describes the active or passive participation of instances of E39 Actors in an E5 Event.

#### P4 has time-span (is time-span of)
**Domain**: E2 Temporal Entity  
**Range**: E52 Time-Span  
**Definition**: This property describes the temporal confinement of an instance of an E2 Temporal Entity.

#### P82a begin of the begin
**Domain**: E52 Time-Span  
**Range**: xsd:dateTime  
**Subproperty of**: P81 ongoing throughout  
**Definition**: The earliest possible beginning of the time-span.

---

## Semantic Interpretation

### What Does "Earliest Attestation" Mean?

An **attestation** is documentary evidence that demonstrates a person's existence at a particular point in time. The **earliest attestation** represents:

1. **Not necessarily birth** - This is not the person's birth date (use `gmn:P98i_1_has_birth_date` for that)
2. **Documentary evidence** - The date comes from historical sources (contracts, letters, registers, etc.)
3. **Earliest known** - This is the first documented reference currently known to researchers
4. **Subject to revision** - New document discoveries may push the attestation date earlier

### Epistemic Status

This property makes an **epistemic claim** about our knowledge:
- "We know this person existed by at least this date"
- NOT: "This person first existed on this date"

The property captures the state of historical knowledge, acknowledging:
- Documentary gaps and losses
- Incomplete archival coverage
- Ongoing research and discoveries

### Relationship to Other Temporal Properties

```
Timeline:
|-----------|---------------|---------------|-------------|
Birth       Earliest        Latest          Death
Date        Attestation     Attestation     Date
(P98i)      (P11i.1)        (P11i.2)        (P100i)

← Unknown → ← Known Period →  ← Unknown →
```

The attestation dates define a **documented period** within which we have evidence of the person's activity, distinct from their actual lifespan.

---

## Usage Guidelines

### When to Use This Property

✅ **Appropriate Uses:**
- Recording the date of the earliest known document mentioning a person
- Establishing terminus post quem for person's documented activity
- Capturing first attestation from archival sources
- Dating historical figures with limited biographical information

❌ **Inappropriate Uses:**
- Recording birth dates (use `gmn:P98i_1_has_birth_date`)
- Recording estimated or calculated dates (use qualified time-spans)
- Recording dates from secondary literature without source verification
- Recording any date other than actual documentary attestation

### Data Quality Considerations

**Source Documentation**: Always link attestation dates to source documents:
```turtle
<person/giovanni> a cidoc:E21_Person ;
    gmn:P11i_1_earliest_attestation_date "1450-03-15"^^xsd:date ;
    cidoc:P70i_is_documented_in <document/ASG_Not_843_f12r> .
```

**Date Precision**: Use ISO 8601 format with appropriate precision:
- Full date: `"1450-03-15"^^xsd:date`
- Year-month: `"1450-03"^^xsd:gYearMonth`
- Year only: `"1450"^^xsd:gYear`

**Multiple Attestations**: Record all known early attestations, not just the single earliest:
```turtle
<person/giovanni> 
    gmn:P11i_1_earliest_attestation_date "1450-03-15"^^xsd:date ;
    gmn:P11i_1_earliest_attestation_date "1450-07-22"^^xsd:date .
```

This allows for:
- Multiple independent sources
- Verification and corroboration
- Handling of uncertain date sequences

### Cardinality

**Allowed**: 0 to many  
**Recommended**: 1 to 3 (record earliest attestations from multiple sources)  
**Typical**: 1 (single earliest known attestation)

---

## Transformation Examples

### Example 1: Basic Single Date

**Input (GMN Shortcut):**
```turtle
@prefix gmn: <http://genoa-medieval-notarial.org/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

<http://example.org/person/giovanni_rossi> 
    a cidoc:E21_Person ;
    gmn:P11i_1_earliest_attestation_date "1450-03-15"^^xsd:date .
```

**Output (Full CIDOC-CRM):**
```turtle
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/person/giovanni_rossi> 
    a cidoc:E21_Person ;
    cidoc:P11i_participated_in <http://example.org/person/giovanni_rossi/event/earliest_a1b2c3d4> .

<http://example.org/person/giovanni_rossi/event/earliest_a1b2c3d4> 
    a cidoc:E5_Event ;
    cidoc:P4_has_time-span <http://example.org/person/giovanni_rossi/event/earliest_a1b2c3d4/timespan> .

<http://example.org/person/giovanni_rossi/event/earliest_a1b2c3d4/timespan> 
    a cidoc:E52_Time-Span ;
    cidoc:P82a_begin_of_the_begin "1450-03-15"^^xsd:date .
```

### Example 2: Multiple Attestation Dates

**Input:**
```turtle
<http://example.org/person/caterina_spinola> 
    a cidoc:E21_Person ;
    gmn:P11i_1_earliest_attestation_date "1450-03-15"^^xsd:date ;
    gmn:P11i_1_earliest_attestation_date "1450-07-22"^^xsd:date .
```

**Output:**
```turtle
<http://example.org/person/caterina_spinola> 
    a cidoc:E21_Person ;
    cidoc:P11i_participated_in 
        <http://example.org/person/caterina_spinola/event/earliest_a1b2c3d4> ,
        <http://example.org/person/caterina_spinola/event/earliest_e5f6g7h8> .

<http://example.org/person/caterina_spinola/event/earliest_a1b2c3d4> 
    a cidoc:E5_Event ;
    cidoc:P4_has_time-span <.../timespan> .

<http://example.org/person/caterina_spinola/event/earliest_a1b2c3d4/timespan> 
    a cidoc:E52_Time-Span ;
    cidoc:P82a_begin_of_the_begin "1450-03-15"^^xsd:date .

<http://example.org/person/caterina_spinola/event/earliest_e5f6g7h8> 
    a cidoc:E5_Event ;
    cidoc:P4_has_time-span <.../timespan> .

<http://example.org/person/caterina_spinola/event/earliest_e5f6g7h8/timespan> 
    a cidoc:E52_Time-Span ;
    cidoc:P82a_begin_of_the_begin "1450-07-22"^^xsd:date .
```

### Example 3: Combined with Document Reference

**Input:**
```turtle
<http://example.org/person/bartolomeo_vignolo> 
    a cidoc:E21_Person ;
    gmn:P1_1_has_name "Bartolomeo Vignolo" ;
    gmn:P11i_1_earliest_attestation_date "1450-03-15"^^xsd:date ;
    cidoc:P70i_is_documented_in <http://example.org/document/ASG_Not_843_f12r> .

<http://example.org/document/ASG_Not_843_f12r>
    a cidoc:E31_Document ;
    gmn:P94i_2_has_enactment_date "1450-03-15"^^xsd:date .
```

**Output:**
```turtle
<http://example.org/person/bartolomeo_vignolo> 
    a cidoc:E21_Person ;
    cidoc:P1_is_identified_by [
        a cidoc:E41_Appellation ;
        cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
        cidoc:P190_has_symbolic_content "Bartolomeo Vignolo"
    ] ;
    cidoc:P11i_participated_in <.../event/earliest_...> ;
    cidoc:P70i_is_documented_in <http://example.org/document/ASG_Not_843_f12r> .

<.../event/earliest_...> 
    a cidoc:E5_Event ;
    cidoc:P4_has_time-span [
        a cidoc:E52_Time-Span ;
        cidoc:P82a_begin_of_the_begin "1450-03-15"^^xsd:date
    ] .
```

### Example 4: With Earliest and Latest Attestation

**Input:**
```turtle
<http://example.org/person/maria_doria> 
    a cidoc:E21_Person ;
    gmn:P1_1_has_name "Maria Doria" ;
    gmn:P11i_1_earliest_attestation_date "1450-03-15"^^xsd:date ;
    gmn:P11i_2_latest_attestation_date "1475-11-30"^^xsd:date .
```

**Output:**
```turtle
<http://example.org/person/maria_doria> 
    a cidoc:E21_Person ;
    cidoc:P1_is_identified_by [
        a cidoc:E41_Appellation ;
        cidoc:P190_has_symbolic_content "Maria Doria"
    ] ;
    cidoc:P11i_participated_in 
        <.../event/earliest_...> ,
        <.../event/latest_...> .

<.../event/earliest_...> 
    a cidoc:E5_Event ;
    cidoc:P4_has_time-span [
        a cidoc:E52_Time-Span ;
        cidoc:P82a_begin_of_the_begin "1450-03-15"^^xsd:date
    ] .

<.../event/latest_...> 
    a cidoc:E5_Event ;
    cidoc:P4_has_time-span [
        a cidoc:E52_Time-Span ;
        cidoc:P82b_end_of_the_end "1475-11-30"^^xsd:date
    ] .
```

### Example 5: JSON-LD Format

**Input:**
```json
{
  "@context": {
    "gmn": "http://genoa-medieval-notarial.org/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "http://example.org/person/giovanni_rossi",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_1_earliest_attestation_date": {
    "@value": "1450-03-15",
    "@type": "xsd:date"
  }
}
```

**Output:**
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "http://example.org/person/giovanni_rossi",
  "@type": "cidoc:E21_Person",
  "cidoc:P11i_participated_in": [{
    "@id": "http://example.org/person/giovanni_rossi/event/earliest_a1b2c3d4",
    "@type": "cidoc:E5_Event",
    "cidoc:P4_has_time-span": {
      "@id": "http://example.org/person/giovanni_rossi/event/earliest_a1b2c3d4/timespan",
      "@type": "cidoc:E52_Time-Span",
      "cidoc:P82a_begin_of_the_begin": "1450-03-15"
    }
  }]
}
```

---

## Related Properties

### Direct Relations

| Property | Relationship | Description |
|----------|--------------|-------------|
| `gmn:P11i_2_latest_attestation_date` | Sibling | Latest date person is attested, using P82b_end_of_the_end |
| `gmn:P11i_3_has_spouse` | Sibling | Also uses P11i_participated_in for marriage events |
| `cidoc:P11i_participated_in` | Parent | Superproperty for all participation in events |

### Temporal Properties Network

```
Person Temporal Properties:
├── Birth/Death (Biological)
│   ├── gmn:P98i_1_has_birth_date
│   └── gmn:P100i_1_has_death_date
├── Attestation (Documentary)
│   ├── gmn:P11i_1_earliest_attestation_date ← THIS PROPERTY
│   └── gmn:P11i_2_latest_attestation_date
└── Events (Activity)
    ├── gmn:P11i_3_has_spouse (marriage)
    └── cidoc:P11i_participated_in (generic)
```

### Complementary Properties

**For complete person records, combine with:**
- `gmn:P1_1_has_name` - Person's name
- `gmn:P2_1_gender` - Person's gender
- `gmn:P96_1_has_mother` - Mother relationship
- `gmn:P97_1_has_father` - Father relationship
- `gmn:P107i_1_has_regional_provenance` - Geographic origin
- `cidoc:P70i_is_documented_in` - Source documents

---

## Use Cases

### Use Case 1: Prosopographical Database

**Scenario**: Building a database of Genoese notaries from archival sources

**Implementation**:
```turtle
<notary/giovanni_de_amandolesio>
    a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giovanni de Amandolesio" ;
    gmn:P107i_3_has_occupation <occupation/notary> ;
    gmn:P11i_1_earliest_attestation_date "1445-01-20"^^xsd:date ;
    gmn:P11i_2_latest_attestation_date "1470-12-15"^^xsd:date ;
    cidoc:P70i_is_documented_in 
        <document/ASG_Not_841>,
        <document/ASG_Not_843> .
```

**Benefits**:
- Establishes documented career period
- Enables chronological queries
- Links to source documentation
- Supports biographical research

### Use Case 2: Family Reconstruction

**Scenario**: Reconstructing family networks across generations

**Implementation**:
```turtle
<person/caterina_spinola>
    a cidoc:E21_Person ;
    gmn:P1_1_has_name "Caterina Spinola" ;
    gmn:P11i_1_earliest_attestation_date "1450-03-15"^^xsd:date ;
    gmn:P96_1_has_mother <person/maria_doria> ;
    gmn:P97_1_has_father <person/luca_spinola> .

<person/maria_doria>
    gmn:P11i_1_earliest_attestation_date "1425-06-10"^^xsd:date ;
    gmn:P11i_2_latest_attestation_date "1460-11-20"^^xsd:date .
```

**Benefits**:
- Establishes generational chronology
- Validates parent-child relationships
- Identifies anachronisms
- Supports genealogical research

### Use Case 3: Document Dating

**Scenario**: Using attestation dates to validate document chronology

**Query Example**:
```sparql
# Find documents where attestation date conflicts with document date
SELECT ?person ?personAttestation ?doc ?docDate
WHERE {
    ?person gmn:P11i_1_earliest_attestation_date ?personAttestation .
    ?person cidoc:P70i_is_documented_in ?doc .
    ?doc gmn:P94i_2_has_enactment_date ?docDate .
    FILTER (?docDate < ?personAttestation)
}
```

**Benefits**:
- Identifies chronological inconsistencies
- Validates document dating
- Flags potential data entry errors
- Supports archival research

### Use Case 4: Historical Timeline Visualization

**Scenario**: Creating visual timeline of documented persons

**Implementation**:
```turtle
# Multiple persons with attestation dates
<person/p1> gmn:P11i_1_earliest_attestation_date "1445-01-01"^^xsd:date .
<person/p2> gmn:P11i_1_earliest_attestation_date "1447-06-15"^^xsd:date .
<person/p3> gmn:P11i_1_earliest_attestation_date "1450-03-20"^^xsd:date .
```

**Query for timeline**:
```sparql
SELECT ?person ?name ?earliest ?latest
WHERE {
    ?person a cidoc:E21_Person ;
            gmn:P1_1_has_name ?name ;
            gmn:P11i_1_earliest_attestation_date ?earliest .
    OPTIONAL { ?person gmn:P11i_2_latest_attestation_date ?latest }
}
ORDER BY ?earliest
```

**Benefits**:
- Chronological visualization
- Period analysis
- Activity patterns
- Research planning

### Use Case 5: Source Coverage Analysis

**Scenario**: Analyzing temporal coverage of archival sources

**Query Example**:
```sparql
# Count attestations by year
SELECT (YEAR(?date) AS ?year) (COUNT(?person) AS ?attestations)
WHERE {
    ?person gmn:P11i_1_earliest_attestation_date ?date .
}
GROUP BY YEAR(?date)
ORDER BY ?year
```

**Benefits**:
- Identifies archival gaps
- Reveals source preservation patterns
- Guides research priorities
- Supports metadata analysis

---

## Formal Semantics

### OWL 2 Axioms

```turtle
# Domain axiom
gmn:P11i_1_earliest_attestation_date rdfs:domain cidoc:E21_Person .

# Range axiom
gmn:P11i_1_earliest_attestation_date rdfs:range xsd:date .

# Subproperty axiom
gmn:P11i_1_earliest_attestation_date rdfs:subPropertyOf cidoc:P11i_participated_in .

# Disjoint with latest attestation
gmn:P11i_1_earliest_attestation_date owl:propertyDisjointWith gmn:P11i_2_latest_attestation_date .
```

### SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .

# Shape for P11i.1 validation
:EarliestAttestationShape
    a sh:NodeShape ;
    sh:targetSubjectsOf gmn:P11i_1_earliest_attestation_date ;
    sh:property [
        sh:path gmn:P11i_1_earliest_attestation_date ;
        sh:datatype xsd:date ;
        sh:minCount 0 ;
        sh:maxCount 10 ;  # Reasonable limit
        sh:severity sh:Warning ;
        sh:message "Earliest attestation date must be xsd:date"@en ;
    ] ;
    sh:property [
        sh:path rdf:type ;
        sh:hasValue cidoc:E21_Person ;
        sh:minCount 1 ;
        sh:severity sh:Violation ;
        sh:message "Subject must be a cidoc:E21_Person"@en ;
    ] .

# Temporal consistency constraint
:TemporalConsistencyShape
    a sh:NodeShape ;
    sh:targetSubjectsOf gmn:P11i_1_earliest_attestation_date ;
    sh:sparql [
        sh:message "Earliest attestation must precede latest attestation"@en ;
        sh:prefixes :prefixes ;
        sh:select """
            SELECT $this (?earliest AS ?value)
            WHERE {
                $this gmn:P11i_1_earliest_attestation_date ?earliest ;
                      gmn:P11i_2_latest_attestation_date ?latest .
                FILTER (?earliest > ?latest)
            }
        """ ;
    ] .
```

---

## Implementation Notes

### URI Generation Strategy

The transformation generates stable URIs using:
1. Subject URI as base
2. Event type identifier ("earliest")
3. Hash of date value for uniqueness

**Pattern**: `{subject_uri}/event/earliest_{hash}`

**Example**: 
- Subject: `http://example.org/person/giovanni`
- Date: `1450-03-15`
- Event URI: `http://example.org/person/giovanni/event/earliest_a1b2c3d4`
- Timespan URI: `{event_uri}/timespan`

### Multiple Values Handling

When multiple dates are provided:
- Each creates a separate E5_Event
- Each event gets unique hash-based URI
- All events added to P11i_participated_in array
- Order preservation not guaranteed

### Date Format Support

Supported formats:
- String: `"1450-03-15"`
- Typed literal: `"1450-03-15"^^xsd:date`
- Object: `{"@value": "1450-03-15", "@type": "xsd:date"}`

### Integration with Existing Data

If subject already has `cidoc:P11i_participated_in`:
- New attestation events are appended
- Existing events preserved
- No duplication or overwriting

---

*Ontology Documentation v1.0 - Last updated: 2025-10-26*
