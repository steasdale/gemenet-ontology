# GMN P70.15 Documents Witness - Semantic Documentation

Complete semantic documentation for the `gmn:P70_15_documents_witness` property, including class definitions, property specifications, and transformation examples.

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Ontological Definition](#ontological-definition)
3. [Semantic Explanation](#semantic-explanation)
4. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
5. [Transformation Patterns](#transformation-patterns)
6. [Usage Examples](#usage-examples)
7. [Comparison with Related Properties](#comparison-with-related-properties)
8. [Implementation Notes](#implementation-notes)

---

## Property Overview

### Basic Information

| Attribute | Value |
|-----------|-------|
| **Property URI** | `gmn:P70_15_documents_witness` |
| **Label** | P70.15 documents witness |
| **Property Type** | `owl:ObjectProperty`, `rdf:Property` |
| **Domain** | `gmn:E31_2_Sales_Contract` |
| **Range** | `cidoc:E21_Person` |
| **Super Property** | `cidoc:P70_documents` |
| **Created** | 2025-10-17 |
| **Status** | Active |

### Purpose

This property associates a sales contract document with persons who served as witnesses to the acquisition event. Witnesses were present at the transaction and formally observed the transfer of property, providing legal validation of the event.

### Key Distinction

Unlike `gmn:P70_11_documents_referenced_person` (which captures persons merely mentioned in document text), witnesses **actively participated** in the acquisition event by observing and validating the transaction. This distinction is crucial for proper semantic modeling.

---

## Ontological Definition

### TTL Definition

```turtle
# Property: P70.15 documents witness
gmn:P70_15_documents_witness
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.15 documents witness"@en ;
    rdfs:comment "Simplified property for associating a sales contract with a person who served as a witness to the acquisition. Witnesses were present at the transaction and formally observed the transfer of property, providing legal validation of the event. Unlike referenced persons (P70.11) who are merely mentioned in the text, witnesses actively participated in the acquisition event. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P11_had_participant > E21_Person, with the person's role typed as 'witness' (AAT 300028910). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P11_had_participant .
```

### Property Characteristics

- **Functional:** No (a contract can have multiple witnesses)
- **Inverse Functional:** No (a person can witness multiple contracts)
- **Transitive:** No
- **Symmetric:** No
- **Reflexive:** No

---

## Semantic Explanation

### Historical Context

In medieval and early modern Genoa, witnesses played a crucial legal role in property transactions:

1. **Legal Requirement:** Many transactions required witnesses for validity
2. **Validation Function:** Witnesses provided third-party verification of the transaction
3. **Memory Function:** Witnesses could later testify about the transaction if disputes arose
4. **Social Function:** Choice of witnesses could indicate social networks and relationships

### Witness vs. Other Roles

| Role | Property | Relationship to Transaction | Example |
|------|----------|---------------------------|---------|
| **Witness** | P70.15 | Observed and validated the event | "Present were witnesses Antonio and Paolo" |
| **Referenced Person** | P70.11 | Mentioned in text but not participating | "The property previously owned by the late Marco" |
| **Seller** | P70.1 | Primary party transferring property | "Giovanni sells to Luca" |
| **Buyer** | P70.2 | Primary party acquiring property | "Luca buys from Giovanni" |
| **Broker** | P70.8 | Facilitated the transaction | "Through the mediation of Antonio" |
| **Notary** | P94i.1 | Created the legal document | "Before notary Paolo" |

### Participation Model

Witnesses participate in the acquisition through observation:
- They are **present** at the event
- They **observe** the transaction
- They provide **validation** through their presence
- They may later **testify** if needed

This is modeled in CIDOC-CRM through:
- E8_Acquisition (the transaction event)
- E7_Activity (the witnessing activity)
- P14_carried_out_by (links activity to witness)
- P14.1_in_the_role_of (specifies role as "witness")

---

## CIDOC-CRM Mapping

### Full CIDOC-CRM Path

The shortcut property represents this complete CIDOC-CRM structure:

```
E31_Document 
  ↓ P70_documents
E8_Acquisition
  ↓ P9_consists_of
E7_Activity (witnessing activity)
  ↓ P14_carried_out_by
E21_Person (witness)
  
E7_Activity
  ↓ P14.1_in_the_role_of
E55_Type (AAT: witness, 300028910)
```

### Class Definitions

#### E8_Acquisition
- **Definition:** Comprises transfers of legal ownership from one or more instances of E39_Actor to one or more other instances of E39_Actor
- **Role:** Represents the property transfer event documented by the contract

#### E7_Activity
- **Definition:** Comprises actions intentionally carried out by instances of E39_Actor that result in changes of state in the cultural, social, or physical systems
- **Role:** Represents the witnessing activity as a component of the acquisition

#### E21_Person
- **Definition:** Comprises real persons who live or are assumed to have lived
- **Role:** The individual who served as witness

#### E55_Type
- **Definition:** Comprises concepts denoted by terms from thesauri and controlled vocabularies used to characterize and classify instances of CIDOC-CRM classes
- **Role:** Specifies the role "witness" using AAT concept 300028910

### Property Definitions

#### P70_documents
- **Domain:** E31_Document
- **Range:** E1_CRM_Entity
- **Definition:** Describes the CRM entities documented as instances of E31_Document
- **Role:** Links the sales contract to the acquisition event

#### P9_consists_of
- **Domain:** E4_Period
- **Range:** E4_Period
- **Definition:** Associates an instance of E4_Period with another instance of E4_Period that is defined by a subset of the phenomena
- **Role:** Links the acquisition to component activities (witnessing)

#### P14_carried_out_by
- **Domain:** E7_Activity
- **Range:** E39_Actor
- **Definition:** Describes the active or passive participation of instances of E39_Actor in an instance of E7_Activity
- **Role:** Links the witnessing activity to the witness person

#### P14.1_in_the_role_of
- **Domain:** E7_Activity
- **Range:** E55_Type
- **Definition:** A property qualifier that specifies the role of an actor in an activity
- **Role:** Specifies that the person participated as a witness

### AAT Concept

**Witness (AAT 300028910)**
- **URI:** http://vocab.getty.edu/page/aat/300028910
- **Definition:** People who give testimony or evidence
- **Scope Note:** Refers to those who observe an event and may be called upon to give testimony about it

---

## Transformation Patterns

### Pattern 1: Simple Witness (URI String)

**Input:**
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_15_documents_witness <witness_antonio> .
```

**Output:**
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <contract001/acquisition> .

<contract001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P9_consists_of <contract001/activity/witness_hash> .

<contract001/activity/witness_hash> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <witness_antonio> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .

<witness_antonio> a cidoc:E21_Person .
```

### Pattern 2: Multiple Witnesses

**Input:**
```turtle
<contract002> a gmn:E31_2_Sales_Contract ;
    gmn:P70_15_documents_witness <witness_antonio>, <witness_paolo>, <witness_giovanni> .
```

**Output:**
```turtle
<contract002> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <contract002/acquisition> .

<contract002/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P9_consists_of <contract002/activity/witness_hash1>,
                         <contract002/activity/witness_hash2>,
                         <contract002/activity/witness_hash3> .

<contract002/activity/witness_hash1> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <witness_antonio> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .

<contract002/activity/witness_hash2> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <witness_paolo> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .

<contract002/activity/witness_hash3> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <witness_giovanni> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .
```

### Pattern 3: Witness with Full Person Data

**Input:**
```turtle
<contract003> a gmn:E31_2_Sales_Contract ;
    gmn:P70_15_documents_witness [
        a cidoc:E21_Person ;
        cidoc:P1_is_identified_by [
            a cidoc:E41_Appellation ;
            cidoc:P190_has_symbolic_content "Antonio Spinola" ;
            cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650>
        ]
    ] .
```

**Output:**
```turtle
<contract003> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <contract003/acquisition> .

<contract003/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P9_consists_of <contract003/activity/witness_hash> .

<contract003/activity/witness_hash> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by [
        a cidoc:E21_Person ;
        cidoc:P1_is_identified_by [
            a cidoc:E41_Appellation ;
            cidoc:P190_has_symbolic_content "Antonio Spinola" ;
            cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650>
        ]
    ] ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .
```

### Pattern 4: Complete Transaction with Witnesses

**Input:**
```turtle
<contract004> a gmn:E31_2_Sales_Contract ;
    gmn:P1_1_has_name "Sale of house on Via Garibaldi" ;
    gmn:P70_1_documents_seller <giovanni_doria> ;
    gmn:P70_2_documents_buyer <luca_spinola> ;
    gmn:P70_3_documents_transfer_of <house_via_garibaldi_15> ;
    gmn:P70_15_documents_witness <witness_antonio>, <witness_paolo> ;
    gmn:P94i_1_was_created_by <notary_oberto> ;
    gmn:P94i_2_has_enactment_date "1445-06-15"^^xsd:date .
```

**Output:**
```turtle
<contract004> a gmn:E31_2_Sales_Contract ;
    cidoc:P1_is_identified_by <contract004/appellation> ;
    cidoc:P70_documents <contract004/acquisition> ;
    cidoc:P94i_was_created_by <contract004/creation> .

<contract004/appellation> a cidoc:E41_Appellation ;
    cidoc:P190_has_symbolic_content "Sale of house on Via Garibaldi" .

<contract004/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <giovanni_doria> ;
    cidoc:P22_transferred_title_to <luca_spinola> ;
    cidoc:P24_transferred_title_of <house_via_garibaldi_15> ;
    cidoc:P9_consists_of <contract004/activity/witness_hash1>,
                         <contract004/activity/witness_hash2> .

<contract004/activity/witness_hash1> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <witness_antonio> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .

<contract004/activity/witness_hash2> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <witness_paolo> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .

<contract004/creation> a cidoc:E65_Creation ;
    cidoc:P14_carried_out_by <notary_oberto> ;
    cidoc:P4_has_time-span <contract004/creation/timespan> .

<contract004/creation/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1445-06-15"^^xsd:date .
```

---

## Usage Examples

### Example 1: Basic Contract with Two Witnesses

```turtle
# Source document: "Sale of vineyard in Albaro. Present as witnesses were 
# Antonio de Marini and Paolo Grimaldi."

<contract_1445_07_12> a gmn:E31_2_Sales_Contract ;
    gmn:P1_1_has_name "Sale of vineyard in Albaro"@en ;
    gmn:P70_1_documents_seller <merchant_battista> ;
    gmn:P70_2_documents_buyer <nobleman_filippo> ;
    gmn:P70_3_documents_transfer_of <vineyard_albaro> ;
    gmn:P70_15_documents_witness <antonio_marini>, <paolo_grimaldi> ;
    gmn:P94i_2_has_enactment_date "1445-07-12"^^xsd:date .
```

### Example 2: Contract with Detailed Witness Information

```turtle
# Source document: "In the presence of witnesses Antonio Spinola, 
# son of the late Giovanni, and Paolo Doria, notary"

<contract_1450_03_20> a gmn:E31_2_Sales_Contract ;
    gmn:P70_15_documents_witness <antonio_spinola_witness>, <paolo_doria_notary> .

<antonio_spinola_witness> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by [
        a cidoc:E41_Appellation ;
        cidoc:P190_has_symbolic_content "Antonio Spinola"
    ] ;
    gmn:P1_3_has_patrilineal_name [
        a cidoc:E41_Appellation ;
        cidoc:P190_has_symbolic_content "filius quondam Giovanni"@la
    ] .

<paolo_doria_notary> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by [
        a cidoc:E41_Appellation ;
        cidoc:P190_has_symbolic_content "Paolo Doria"
    ] ;
    gmn:P102_1_has_title [
        a cidoc:E35_Title ;
        cidoc:P190_has_symbolic_content "notarius"@la
    ] .
```

### Example 3: Query for All Witnesses

```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

# Find all witnesses in the database (after transformation)
SELECT ?contract ?acquisition ?activity ?witness ?witness_name
WHERE {
    ?contract a gmn:E31_2_Sales_Contract ;
              cidoc:P70_documents ?acquisition .
    
    ?acquisition a cidoc:E8_Acquisition ;
                 cidoc:P9_consists_of ?activity .
    
    ?activity a cidoc:E7_Activity ;
              cidoc:P14_carried_out_by ?witness ;
              cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .
    
    ?witness a cidoc:E21_Person .
    
    OPTIONAL {
        ?witness cidoc:P1_is_identified_by ?appellation .
        ?appellation cidoc:P190_has_symbolic_content ?witness_name .
    }
}
```

### Example 4: Query for Contracts with Specific Witness

```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

# Find all contracts witnessed by Antonio Spinola
SELECT ?contract ?date
WHERE {
    ?contract a gmn:E31_2_Sales_Contract ;
              cidoc:P70_documents ?acquisition ;
              cidoc:P94i_was_created_by ?creation .
    
    ?acquisition cidoc:P9_consists_of ?activity .
    
    ?activity cidoc:P14_carried_out_by <antonio_spinola> ;
              cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .
    
    ?creation cidoc:P4_has_time-span ?timespan .
    ?timespan cidoc:P82_at_some_time_within ?date .
}
ORDER BY ?date
```

---

## Comparison with Related Properties

### vs. gmn:P70_11_documents_referenced_person

| Aspect | P70.15 (Witness) | P70.11 (Referenced Person) |
|--------|------------------|---------------------------|
| **Participation** | Active participant in event | Mentioned in text only |
| **Relationship** | To E8_Acquisition via E7_Activity | Direct to E31_Document |
| **CIDOC Path** | P70 > E8 > P9 > E7 > P14 > E21 | P67 > E21 |
| **Role** | Always "witness" | No role specified |
| **Example** | "Present were witnesses Antonio and Paolo" | "The property of the late Marco" |

### vs. gmn:P94i_1_was_created_by (Notary)

| Aspect | P70.15 (Witness) | P94i.1 (Notary) |
|--------|------------------|------------------|
| **Event** | Acquisition event | Document creation event |
| **Activity Type** | E7_Activity (witnessing) | E65_Creation (writing) |
| **Role** | Witness (observer) | Creator (author) |
| **Multiplicity** | Usually multiple | Usually single |
| **Example** | "Witnessed by Antonio" | "Written by notary Paolo" |

### vs. gmn:P70_8_documents_broker

| Aspect | P70.15 (Witness) | P70.8 (Broker) |
|--------|------------------|----------------|
| **Function** | Observes transaction | Facilitates transaction |
| **Active Role** | Passive observer | Active facilitator |
| **Legal Status** | Validates event | Intermediary |
| **Example** | "In the presence of Antonio" | "Through the mediation of Paolo" |

---

## Implementation Notes

### Data Entry Considerations

1. **Multiple Witnesses:** Most contracts have 2-4 witnesses; support multiple values
2. **Witness Identity:** May need to disambiguate common names (multiple Antonio Spinola)
3. **Witness Roles:** Some witnesses may have multiple roles (e.g., notary serving as witness)
4. **Witness Relationships:** Consider linking witnesses to other persons in the database

### Technical Considerations

1. **Hash Function:** Uses `hash(witness_uri + 'witness')` to generate unique activity URIs
2. **Blank Nodes:** Supports both URI references and blank node witness descriptions
3. **Data Preservation:** The `.copy()` method preserves all witness properties during transformation
4. **Acquisition Creation:** Automatically creates E8_Acquisition if it doesn't exist

### Query Optimization

For large datasets, consider:
1. Indexing witness URIs
2. Pre-computing witness participation counts
3. Creating materialized views for common witness queries
4. Caching AAT role lookups

### Validation Rules

Recommended validation:
```python
def validate_witness(witness_data):
    """Validate witness data before transformation."""
    # Must be E21_Person
    if '@type' in witness_data:
        assert 'E21_Person' in witness_data['@type']
    
    # Must have identifier
    if isinstance(witness_data, dict):
        assert '@id' in witness_data or 'cidoc:P1_is_identified_by' in witness_data
    
    return True
```

---

## References

### CIDOC-CRM Documentation
- **E8_Acquisition:** http://www.cidoc-crm.org/Entity/E8-Acquisition
- **E7_Activity:** http://www.cidoc-crm.org/Entity/E7-Activity
- **P14_carried_out_by:** http://www.cidoc-crm.org/Property/P14-carried-out-by

### Getty AAT
- **Witness (300028910):** http://vocab.getty.edu/page/aat/300028910

### Related GMN Properties
- **P70.11 documents referenced person:** For non-participating persons
- **P70.1 documents seller:** For sellers
- **P70.2 documents buyer:** For buyers
- **P94i.1 was created by:** For notaries/document creators

---

**Last Updated:** 2025-10-27  
**Version:** 1.0  
**Status:** Active
