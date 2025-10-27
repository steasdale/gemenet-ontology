# Ontology Documentation: gmn:P11i_2_latest_attestation_date
## Semantic Model and CIDOC-CRM Mapping

**Property IRI:** `http://example.org/gmn/P11i_2_latest_attestation_date`  
**Version:** 1.0  
**Last Updated:** October 2025

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Semantic Model](#semantic-model)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Domain and Range](#domain-and-range)
5. [Property Hierarchy](#property-hierarchy)
6. [Transformation Examples](#transformation-examples)
7. [Use Cases and Scenarios](#use-cases-and-scenarios)
8. [Relationship to Other Properties](#relationship-to-other-properties)
9. [Competency Questions](#competency-questions)
10. [References and Standards](#references-and-standards)

---

## Executive Summary

### Purpose

The `gmn:P11i_2_latest_attestation_date` property is a **simplified convenience property** for expressing the latest date at which a person is documented or attested to have been alive in historical sources. It captures the **last known documentary evidence** of a person's existence.

### Key Characteristics

- **Type:** Datatype Property (owl:DatatypeProperty)
- **Domain:** `cidoc:E21_Person`
- **Range:** `xsd:date`
- **Super Property:** `cidoc:P11i_participated_in`
- **Purpose:** Data entry convenience with automatic expansion to full CIDOC-CRM
- **Status:** Fully implemented in GMN ontology and transformation pipeline

### Transformation Path

```
Simplified Form (GMN):
  E21_Person → gmn:P11i_2_latest_attestation_date → xsd:date

Expanded Form (CIDOC-CRM):
  E21_Person 
    → P11i_participated_in 
      → E5_Event 
        → P4_has_time-span 
          → E52_Time-Span 
            → P82b_end_of_the_end → xsd:date
```

---

## Semantic Model

### Conceptual Foundation

#### What is an Attestation Date?

An **attestation date** is a date on which there is documentary evidence that a person existed and was active. The **latest attestation date** specifically refers to:

- The **last known date** on which a person appears in historical records
- A **terminus ante quem** (latest possible date) for establishing when a person was alive
- Documentary evidence that serves as a proxy for biographical information when exact life dates are unknown

#### Historical Context

In prosopographical research, especially for medieval and early modern periods:

1. **Incomplete Records**: Many individuals lack documented birth or death dates
2. **Document-Based Evidence**: Attestations come from:
   - Contract signatures and witnessing
   - Property transactions
   - Legal proceedings
   - Official appointments
   - Letters and correspondence
3. **Biographical Reconstruction**: Earliest and latest attestations bracket a person's documented lifespan
4. **Uncertainty Management**: Attestations represent certain knowledge while acknowledging gaps

### Ontological Commitment

#### Entity Types

1. **E21_Person** (Domain)
   - The historical individual being documented
   - May have incomplete biographical information
   - Subject of the attestation

2. **E5_Event** (Implicit)
   - The activity or occurrence in which the person participated
   - May be a contract signing, court appearance, property transfer, etc.
   - Documented in historical sources

3. **E52_Time-Span** (Implicit)
   - The temporal extent of the event
   - In this case, specifically the end boundary (P82b_end_of_the_end)
   - Represents when the attestation occurred

#### Relationships

1. **P11i_participated_in** (E21 Person → E5 Event)
   - Inverse of P11_had_participant
   - Indicates the person took part in some documented event
   - Generic relationship that encompasses many types of activities

2. **P4_has_time-span** (E5 Event → E52 Time-Span)
   - Associates the event with its temporal bounds
   - Allows precise or imprecise temporal expressions
   - Connects activities to chronology

3. **P82b_end_of_the_end** (E52 Time-Span → date)
   - Specifically the latest possible end of the time-span
   - Used for "latest attestation" to indicate the final bound
   - Corresponds to the right boundary of a temporal interval

### Semantic Interpretation

#### Latest vs. Death

It is crucial to distinguish:

- **Latest Attestation**: Last date person appears in records
- **Death**: Actual date of death (if known)

```turtle
# Latest attestation (this property)
person:p001 gmn:P11i_2_latest_attestation_date "1595-08-20"^^xsd:date .
# Means: "Last seen in records on 1595-08-20"

# Death (different property)
person:p001 cidoc:P100i_died_in [
  a cidoc:E69_Death ;
  cidoc:P4_has_time-span [
    a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1596-01-01"^^xsd:date
  ]
] .
# Means: "Actually died on 1596-01-01"
```

Latest attestation provides a **lower bound** for death: the person must have died on or after the latest attestation date.

#### Multiple Attestations

A person may have multiple latest attestation dates if:

1. Multiple documents from approximately the same time period
2. Refined research reveals later documents
3. Different types of evidence with different dates
4. Attestations from different roles or contexts

Each date creates a separate event:

```turtle
person:p001 gmn:P11i_2_latest_attestation_date 
  "1595-06-10"^^xsd:date,
  "1595-08-20"^^xsd:date,
  "1595-12-15"^^xsd:date .
```

This expands to three distinct E5_Event instances, preserving granular temporal information.

---

## CIDOC-CRM Mapping

### Full Expansion

#### Simplified Form (Input)

```turtle
@prefix gmn: <http://example.org/gmn/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

person:lorenzo_giustiniani 
  a cidoc:E21_Person ;
  gmn:P1_1_has_name "Lorenzo Giustiniani" ;
  gmn:P11i_2_latest_attestation_date "1595-08-20"^^xsd:date .
```

#### Expanded Form (Output)

```turtle
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

person:lorenzo_giustiniani 
  a cidoc:E21_Person ;
  cidoc:P1_is_identified_by [
    a cidoc:E41_Appellation ;
    cidoc:P190_has_symbolic_content "Lorenzo Giustiniani"
  ] ;
  cidoc:P11i_participated_in [
    a cidoc:E5_Event ;
    cidoc:P4_has_time-span [
      a cidoc:E52_Time-Span ;
      cidoc:P82b_end_of_the_end "1595-08-20"^^xsd:date
    ]
  ] .
```

### Step-by-Step Mapping

#### Step 1: Person Declaration

**Simplified:**
```turtle
person:lorenzo_giustiniani a cidoc:E21_Person .
```

**Expanded:**
```turtle
person:lorenzo_giustiniani a cidoc:E21_Person .
```

*No change - person declaration remains the same.*

#### Step 2: Date Property

**Simplified:**
```turtle
gmn:P11i_2_latest_attestation_date "1595-08-20"^^xsd:date .
```

**Expanded:**
```turtle
cidoc:P11i_participated_in [
  a cidoc:E5_Event ;
  cidoc:P4_has_time-span [
    a cidoc:E52_Time-Span ;
    cidoc:P82b_end_of_the_end "1595-08-20"^^xsd:date
  ]
] .
```

*The date is embedded in a nested event→timespan→date structure.*

#### Step 3: URI Generation

The transformation creates deterministic URIs:

```turtle
# Event URI
person:lorenzo_giustiniani/event/latest_45678901
  a cidoc:E5_Event .

# Time-Span URI  
person:lorenzo_giustiniani/event/latest_45678901/timespan
  a cidoc:E52_Time-Span .
```

URI components:
- **Base:** Person's URI
- **Type:** `event/latest_` (vs `event/earliest_`)
- **Hash:** Last 8 characters of hash(date + 'latest')

### CIDOC-CRM Property Semantics

#### P11i_participated_in

**Definition:** "This property describes the active or passive participation of instances of E39 Actors in an E5 Event." (inverse of P11_had_participant)

**Scope Note:** 
- Covers any form of participation
- Does not imply a specific type of role
- Allows for multiple participants in the same event

**In This Context:**
- The person participated in some documented event
- The specific nature of the event is not explicitly typed
- The attestation is evidence of participation

#### P4_has_time-span

**Definition:** "This property describes the temporal confinement of an instance of an E2 Temporal Entity."

**Scope Note:**
- Associates events with their temporal bounds
- Allows for fuzzy, precise, or approximate temporal expressions
- Does not require exact dates

**In This Context:**
- The event occurred during a specific time-span
- For attestations, the time-span is typically a single point or narrow window
- Provides chronological ordering

#### P82b_end_of_the_end

**Definition:** "This property describes the ending point of the inner range of the time-span."

**Scope Note:**
- Represents the latest possible end of a time-span
- Part of CIDOC-CRM's Allen Interval Algebra implementation
- Used when the exact end is known or when expressing a latest bound

**In This Context:**
- For a "latest attestation," this is the appropriate property
- Represents the right boundary of the temporal interval
- Pairs conceptually with P82a_begin_of_the_begin (used for earliest attestation)

### Comparison with CIDOC-CRM Best Practices

#### Recommended Pattern

CIDOC-CRM documentation recommends using events for biographical information:

```turtle
# Birth
person:p001 cidoc:P98i_was_born [
  a cidoc:E67_Birth ;
  cidoc:P4_has_time-span [...]
] .

# Death
person:p001 cidoc:P100i_died_in [
  a cidoc:E69_Death ;
  cidoc:P4_has_time-span [...]
] .
```

#### Attestation Pattern (This Property)

For attestations where specific event types are unknown:

```turtle
# Attestation (unknown event type)
person:p001 cidoc:P11i_participated_in [
  a cidoc:E5_Event ;  # Generic event, not typed
  cidoc:P4_has_time-span [...]
] .
```

#### When to Use Each

| Use Case | Pattern | Example |
|----------|---------|---------|
| Known birth date | P98i_was_born → E67_Birth | "Born on 1550-03-15" |
| Known death date | P100i_died_in → E69_Death | "Died on 1610-08-20" |
| Earliest attestation | P11i_participated_in → E5_Event + P82a | "First appears in 1575" |
| Latest attestation | P11i_participated_in → E5_Event + P82b | "Last appears in 1595" |
| Specific documented event | P11i_participated_in → E5_Event + P2_has_type | "Signed contract in 1585" |

---

## Domain and Range

### Domain: E21_Person

#### Class Definition

**E21 Person** (from CIDOC-CRM):

> "This class comprises real persons who live or are assumed to have lived. Legendary figures that may have existed, such as Ulysses and King Arthur, fall into this class if the documentation refers to them as historical figures."

#### Scope in GMN

- Individual historical persons documented in sources
- Both named and anonymous persons (identified only by role or description)
- Includes persons with complete biographical information and those with minimal documentation

#### Examples

```turtle
# Named person with details
person:maria_corner a cidoc:E21_Person ;
  gmn:P1_1_has_name "Maria Corner" ;
  gmn:P11i_2_latest_attestation_date "1598-11-20"^^xsd:date .

# Person known only through role
person:anonymous_witness_001 a cidoc:E21_Person ;
  gmn:P1_1_has_name "Anonymous Witness" ;
  gmn:P11i_2_latest_attestation_date "1590-05-15"^^xsd:date .
```

### Range: xsd:date

#### Datatype Definition

**xsd:date** (from XML Schema):

> "The value space of xsd:date consists of top-open intervals of exactly one day in length on the timelines of dateTime, beginning on the beginning moment of each day."

#### Format

Standard ISO 8601 date format:
- **Full date:** `YYYY-MM-DD` (e.g., "1595-08-20")
- **Year-month:** `YYYY-MM` (e.g., "1595-08")
- **Year only:** `YYYY` (e.g., "1595")

#### Precision and Uncertainty

Different levels of temporal precision:

```turtle
# Precise date
person:p001 gmn:P11i_2_latest_attestation_date "1595-08-20"^^xsd:date .

# Month precision
person:p002 gmn:P11i_2_latest_attestation_date "1595-08"^^xsd:date .

# Year only
person:p003 gmn:P11i_2_latest_attestation_date "1595"^^xsd:date .
```

For uncertainty beyond this (e.g., "circa 1595"), use full CIDOC-CRM E52_Time-Span with P79_beginning_is_qualified_by and P80_end_is_qualified_by.

#### Calendar Systems

The xsd:date datatype assumes the proleptic Gregorian calendar. For historical dates:

- Pre-1582 dates in the Julian calendar should be converted to Gregorian equivalents
- If preserving original calendar, document in notes or use E52_Time-Span with P79/P80 qualifiers
- For medieval dating (e.g., "more veneto"), normalize to modern calendar

---

## Property Hierarchy

### Super Properties

```turtle
gmn:P11i_2_latest_attestation_date rdfs:subPropertyOf cidoc:P11i_participated_in .
```

**Implication:** Any instance of gmn:P11i_2_latest_attestation_date is also a cidoc:P11i_participated_in relationship.

This allows:
- Querying for all participation events (including attestations)
- Reasoning over the property hierarchy
- Semantic interoperability with CIDOC-CRM tools

### Related Properties in GMN

| Property | Relationship | Notes |
|----------|--------------|-------|
| `gmn:P11i_1_earliest_attestation_date` | Sibling | Uses P82a_begin_of_the_begin |
| `gmn:P11i_3_has_spouse` | Sibling | Also uses P11i_participated_in with typed E5_Event |

### Relationship to CIDOC-CRM Property Hierarchy

```
cidoc:P01i_is_domain_of (top property)
  ├─ cidoc:P11i_participated_in
  │   ├─ gmn:P11i_1_earliest_attestation_date
  │   ├─ gmn:P11i_2_latest_attestation_date
  │   └─ gmn:P11i_3_has_spouse
  ├─ cidoc:P98i_was_born
  └─ cidoc:P100i_died_in
```

---

## Transformation Examples

### Example 1: Single Person, Single Date

#### Input (GMN)

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "person:francesco_corner",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Francesco Corner",
  "gmn:P11i_2_latest_attestation_date": "1592-06-15"
}
```

#### Output (CIDOC-CRM)

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "person:francesco_corner",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": {
    "@id": "person:francesco_corner/appellation",
    "@type": "cidoc:E41_Appellation",
    "cidoc:P190_has_symbolic_content": "Francesco Corner"
  },
  "cidoc:P11i_participated_in": [
    {
      "@id": "person:francesco_corner/event/latest_45678901",
      "@type": "cidoc:E5_Event",
      "cidoc:P4_has_time-span": {
        "@id": "person:francesco_corner/event/latest_45678901/timespan",
        "@type": "cidoc:E52_Time-Span",
        "cidoc:P82b_end_of_the_end": "1592-06-15"
      }
    }
  ]
}
```

### Example 2: Person with Earliest and Latest Attestations

#### Input (GMN)

```turtle
@prefix gmn: <http://example.org/gmn/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

person:maria_venier a cidoc:E21_Person ;
  gmn:P1_1_has_name "Maria Venier" ;
  gmn:P11i_1_earliest_attestation_date "1575-03-12"^^xsd:date ;
  gmn:P11i_2_latest_attestation_date "1598-11-20"^^xsd:date .
```

#### Output (CIDOC-CRM)

```turtle
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

person:maria_venier a cidoc:E21_Person ;
  cidoc:P1_is_identified_by [
    a cidoc:E41_Appellation ;
    cidoc:P190_has_symbolic_content "Maria Venier"
  ] ;
  cidoc:P11i_participated_in [
    a cidoc:E5_Event ;
    cidoc:P4_has_time-span [
      a cidoc:E52_Time-Span ;
      cidoc:P82a_begin_of_the_begin "1575-03-12"^^xsd:date
    ]
  ] ,
  [
    a cidoc:E5_Event ;
    cidoc:P4_has_time-span [
      a cidoc:E52_Time-Span ;
      cidoc:P82b_end_of_the_end "1598-11-20"^^xsd:date
    ]
  ] .
```

#### SPARQL Query

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?name ?earliest ?latest
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name ;
          cidoc:P11i_participated_in ?event1, ?event2 .
  
  ?event1 cidoc:P4_has_time-span/cidoc:P82a_begin_of_the_begin ?earliest .
  ?event2 cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?latest .
  
  FILTER(?earliest < ?latest)
}
ORDER BY ?earliest
```

### Example 3: Multiple Latest Attestations

#### Input (GMN)

```turtle
person:lorenzo_giustiniani a cidoc:E21_Person ;
  gmn:P1_1_has_name "Lorenzo Giustiniani" ;
  gmn:P11i_2_latest_attestation_date 
    "1595-06-10"^^xsd:date,
    "1595-08-20"^^xsd:date,
    "1595-12-15"^^xsd:date .
```

#### Output (CIDOC-CRM)

```turtle
person:lorenzo_giustiniani a cidoc:E21_Person ;
  cidoc:P1_is_identified_by [...] ;
  cidoc:P11i_participated_in 
    [
      a cidoc:E5_Event ;
      cidoc:P4_has_time-span [
        a cidoc:E52_Time-Span ;
        cidoc:P82b_end_of_the_end "1595-06-10"^^xsd:date
      ]
    ] ,
    [
      a cidoc:E5_Event ;
      cidoc:P4_has_time-span [
        a cidoc:E52_Time-Span ;
        cidoc:P82b_end_of_the_end "1595-08-20"^^xsd:date
      ]
    ] ,
    [
      a cidoc:E5_Event ;
      cidoc:P4_has_time-span [
        a cidoc:E52_Time-Span ;
        cidoc:P82b_end_of_the_end "1595-12-15"^^xsd:date
      ]
    ] .
```

#### SPARQL Query - Get All Latest Attestations

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?name ?latestDate
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name ;
          cidoc:P11i_participated_in ?event .
  
  ?event cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?latestDate .
}
ORDER BY ?person DESC(?latestDate)
```

### Example 4: Combined with Other Person Properties

#### Input (GMN)

```turtle
person:andrea_gritti a cidoc:E21_Person ;
  gmn:P1_1_has_name "Andrea Gritti" ;
  gmn:P11i_1_earliest_attestation_date "1480-05-10"^^xsd:date ;
  gmn:P11i_2_latest_attestation_date "1538-12-28"^^xsd:date ;
  gmn:P11i_3_has_spouse person:benedetta_vendramin ;
  gmn:P107i_2_has_social_category "Venetian nobility" .
```

#### Output (CIDOC-CRM) - Partial

```turtle
person:andrea_gritti a cidoc:E21_Person ;
  cidoc:P1_is_identified_by [...] ;
  cidoc:P11i_participated_in 
    # Earliest attestation
    [ a cidoc:E5_Event ; ... ] ,
    # Latest attestation
    [ a cidoc:E5_Event ; 
      cidoc:P4_has_time-span [
        a cidoc:E52_Time-Span ;
        cidoc:P82b_end_of_the_end "1538-12-28"^^xsd:date
      ]
    ] ,
    # Marriage
    [ a cidoc:E5_Event ;
      cidoc:P2_has_type <http://vocab.getty.edu/aat/300055475> ;
      cidoc:P11_had_participant person:benedetta_vendramin
    ] ;
  cidoc:P107i_is_current_or_former_member_of [...] .
```

---

## Use Cases and Scenarios

### Use Case 1: Prosopographical Database

**Scenario:** Building a database of medieval merchants with incomplete biographical data.

**Problem:** Most merchants lack documented birth/death dates, but appear in commercial records.

**Solution:**
```turtle
merchant:francesco_datini a cidoc:E21_Person ;
  gmn:P1_1_has_name "Francesco Datini" ;
  gmn:P11i_1_earliest_attestation_date "1350"^^xsd:date ;  # First business record
  gmn:P11i_2_latest_attestation_date "1410"^^xsd:date ;    # Last will and testament
  gmn:P107i_3_has_occupation "Merchant" .
```

**Benefit:** Establishes documented lifespan without claiming false precision about birth/death.

### Use Case 2: Biographical Timeline Visualization

**Scenario:** Creating a visual timeline of when historical figures were active.

**Query:**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?name ?earliest ?latest
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
  
  OPTIONAL {
    ?person cidoc:P11i_participated_in ?event1 .
    ?event1 cidoc:P4_has_time-span/cidoc:P82a_begin_of_the_begin ?earliest .
  }
  
  OPTIONAL {
    ?person cidoc:P11i_participated_in ?event2 .
    ?event2 cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?latest .
  }
}
ORDER BY ?earliest
```

**Visualization:** Plot each person as a bar from earliest to latest attestation.

### Use Case 3: Genealogical Research

**Scenario:** Reconstructing family trees where exact dates are uncertain.

**Example:**
```turtle
person:giovanni_soranzo a cidoc:E21_Person ;
  gmn:P1_1_has_name "Giovanni Soranzo" ;
  gmn:P11i_2_latest_attestation_date "1485-07-20"^^xsd:date ;
  gmn:P96_1_has_mother person:caterina_morosini ;
  gmn:P97_1_has_father person:marco_soranzo .

# Father must have been alive before son's latest attestation
person:marco_soranzo a cidoc:E21_Person ;
  gmn:P11i_2_latest_attestation_date "1465-03-10"^^xsd:date .
```

**Inference:** Marco Soranzo's latest attestation (1465) predates Giovanni's (1485), consistent with father-son relationship.

### Use Case 4: Historical Network Analysis

**Scenario:** Analyzing social networks based on co-attestations in documents.

**Query:** Find persons who were attested in overlapping time periods:

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person1 ?name1 ?person2 ?name2
WHERE {
  ?person1 a cidoc:E21_Person ;
           cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name1 ;
           cidoc:P11i_participated_in ?event1 .
  
  ?person2 a cidoc:E21_Person ;
           cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name2 ;
           cidoc:P11i_participated_in ?event2 .
  
  ?event1 cidoc:P4_has_time-span/cidoc:P82a_begin_of_the_begin ?start1 .
  ?event1 cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?end1 .
  
  ?event2 cidoc:P4_has_time-span/cidoc:P82a_begin_of_the_begin ?start2 .
  ?event2 cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?end2 .
  
  # Temporal overlap: start1 <= end2 AND start2 <= end1
  FILTER(?start1 <= ?end2 && ?start2 <= ?end1)
  FILTER(?person1 != ?person2)
}
```

### Use Case 5: Data Quality Assessment

**Scenario:** Identifying persons with suspicious attestation dates.

**Query:** Find persons where latest attestation precedes earliest:

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?name ?earliest ?latest
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
  
  ?person cidoc:P11i_participated_in ?event1, ?event2 .
  
  ?event1 cidoc:P4_has_time-span/cidoc:P82a_begin_of_the_begin ?earliest .
  ?event2 cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?latest .
  
  FILTER(?latest < ?earliest)  # Data quality issue!
}
```

---

## Relationship to Other Properties

### Complementary Properties

#### gmn:P11i_1_earliest_attestation_date

**Relationship:** Forms a pair with the latest attestation date.

**Together they define:**
- The **attested lifespan**: period during which documentary evidence exists
- A biographical bracket: person was active at least from earliest to latest attestation

**Example:**
```turtle
person:p001 
  gmn:P11i_1_earliest_attestation_date "1575"^^xsd:date ;
  gmn:P11i_2_latest_attestation_date "1598"^^xsd:date .
# Interpretation: Person documented between 1575-1598
```

#### gmn:P11i_3_has_spouse

**Relationship:** Also uses P11i_participated_in but with typed marriage events.

**Difference:**
- Latest attestation: Generic E5_Event (unknown type)
- Spouse: E5_Event typed with AAT 300055475 (marriages)

**Example:**
```turtle
person:p001 cidoc:P11i_participated_in 
  # Latest attestation (untyped)
  [ a cidoc:E5_Event ; 
    cidoc:P4_has_time-span [...] 
  ] ,
  # Marriage (typed)
  [ a cidoc:E5_Event ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300055475> ;
    cidoc:P11_had_participant person:spouse
  ] .
```

### Contrasting Properties

#### Standard CIDOC-CRM: P98i_was_born / P100i_died_in

**Difference:**

| Property | Event Type | Temporal Precision | Uncertainty |
|----------|------------|-------------------|-------------|
| P98i_was_born | E67_Birth | Exact birth date | Known event |
| P100i_died_in | E69_Death | Exact death date | Known event |
| gmn:P11i_1 | E5_Event | First attestation | Documentary evidence only |
| gmn:P11i_2 | E5_Event | Last attestation | Documentary evidence only |

**When to use each:**

```turtle
# If birth date is known
person:p001 cidoc:P98i_was_born [
  a cidoc:E67_Birth ;
  cidoc:P4_has_time-span [
    a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1550-03-15"^^xsd:date
  ]
] .

# If only earliest attestation is known
person:p001 gmn:P11i_1_earliest_attestation_date "1575-01-10"^^xsd:date .

# If both are known
person:p001 
  cidoc:P98i_was_born [...] ;  # Actual birth
  gmn:P11i_1_earliest_attestation_date "1575-01-10"^^xsd:date .  # First record
```

### Property Inference Rules

#### Rule 1: Latest Attestation implies Earliest Bound

```turtle
# If:
person:p001 gmn:P11i_2_latest_attestation_date "1595"^^xsd:date .

# Then:
person:p001 cidoc:P98i_was_born [
  cidoc:P4_has_time-span [
    cidoc:P82b_end_of_the_end "1595"^^xsd:date  # Born no later than 1595
  ]
] .
```

#### Rule 2: Death must post-date Latest Attestation

```turtle
# If:
person:p001 gmn:P11i_2_latest_attestation_date "1595-08-20"^^xsd:date .
person:p001 cidoc:P100i_died_in [
  cidoc:P4_has_time-span/cidoc:P82_at_some_time_within ?deathDate
] .

# Then:
FILTER(?deathDate >= "1595-08-20"^^xsd:date)
```

---

## Competency Questions

Competency questions that this property enables:

### Question 1: What is the documented lifespan of a person?

**SPARQL:**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?name ?lifespan_start ?lifespan_end
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
  
  OPTIONAL {
    ?person cidoc:P11i_participated_in ?event1 .
    ?event1 cidoc:P4_has_time-span/cidoc:P82a_begin_of_the_begin ?lifespan_start .
  }
  
  OPTIONAL {
    ?person cidoc:P11i_participated_in ?event2 .
    ?event2 cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?lifespan_end .
  }
}
```

### Question 2: Who was alive during a specific year?

**SPARQL:**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT DISTINCT ?person ?name
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name ;
          cidoc:P11i_participated_in ?event1, ?event2 .
  
  ?event1 cidoc:P4_has_time-span/cidoc:P82a_begin_of_the_begin ?earliest .
  ?event2 cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?latest .
  
  FILTER(YEAR(?earliest) <= 1590 && YEAR(?latest) >= 1590)
}
```

### Question 3: Find persons with short documented lifespans

**SPARQL:**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?name ?earliest ?latest 
       (YEAR(?latest) - YEAR(?earliest) AS ?years_attested)
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name ;
          cidoc:P11i_participated_in ?event1, ?event2 .
  
  ?event1 cidoc:P4_has_time-span/cidoc:P82a_begin_of_the_begin ?earliest .
  ?event2 cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?latest .
  
  FILTER(YEAR(?latest) - YEAR(?earliest) < 5)
}
ORDER BY ?years_attested
```

### Question 4: What was the actual latest attestation date?

**SPARQL (for persons with multiple latest attestations):**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?name (MAX(?latestDate) AS ?actual_latest)
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name ;
          cidoc:P11i_participated_in ?event .
  
  ?event cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?latestDate .
}
GROUP BY ?person ?name
```

### Question 5: Find chronological gaps in attestations

**SPARQL:**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?name ?earliest ?latest 
       ((YEAR(?latest) - YEAR(?earliest)) AS ?gap_years)
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name ;
          cidoc:P11i_participated_in ?event1, ?event2 .
  
  ?event1 cidoc:P4_has_time-span/cidoc:P82a_begin_of_the_begin ?earliest .
  ?event2 cidoc:P4_has_time-span/cidoc:P82b_end_of_the_end ?latest .
  
  FILTER((YEAR(?latest) - YEAR(?earliest)) > 50)  # 50+ year gap
}
ORDER BY DESC(?gap_years)
```

---

## References and Standards

### CIDOC-CRM

- **CIDOC-CRM Version:** 7.1.x
- **Specification:** http://www.cidoc-crm.org/
- **Relevant Classes:**
  - E21_Person: http://www.cidoc-crm.org/Entity/E21-Person/version-7.1.1
  - E5_Event: http://www.cidoc-crm.org/Entity/E5-Event/version-7.1.1
  - E52_Time-Span: http://www.cidoc-crm.org/Entity/E52-Time-Span/version-7.1.1
- **Relevant Properties:**
  - P11i_participated_in: http://www.cidoc-crm.org/Property/P11i-participated-in/version-7.1.1
  - P4_has_time-span: http://www.cidoc-crm.org/Property/P4-has-time-span/version-7.1.1
  - P82b_end_of_the_end: http://www.cidoc-crm.org/Property/P82b-end-of-the-end/version-7.1.1

### XML Schema Datatypes

- **xsd:date Specification:** https://www.w3.org/TR/xmlschema-2/#date
- **ISO 8601 Date Format:** https://www.iso.org/iso-8601-date-and-time-format.html

### Prosopographical Standards

- **SNAP:DRGN** (Standards for Networking Ancient Prosopographies)
- **Factoid-based Prosopography Model**
- **Pelagios Network** (for geographical attestations)

### Related Documentation

- **GMN Ontology Documentation:** Complete GMN ontology reference
- **Transformation Pipeline Guide:** Technical documentation for gmn_to_cidoc_transform.py
- **CIDOC-CRM Implementation Patterns:** Best practices for CRM implementation

---

## Glossary

- **Attestation:** Documentary evidence of a person's existence at a specific time
- **Latest Attestation Date:** The last known date when historical records show evidence of a person's existence
- **Terminus ante quem:** Latin for "limit before which" - the latest possible date
- **Prosopography:** The study of persons, especially through collective biographies
- **Event-based modeling:** Representing information through events that entities participate in
- **Blank node:** An RDF resource without a URI (used for nested structures)
- **Property path:** A SPARQL expression navigating through multiple properties

---

**Document Version:** 1.0  
**Last Updated:** October 2025  
**Ontology Namespace:** http://example.org/gmn/  
**CIDOC-CRM Version:** 7.1.x
