# Ontology Documentation: P70.18 Documents Disputing Party Property

Complete semantic documentation for the `gmn:P70_18_documents_disputing_party` property in the GMN ontology.

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Semantic Structure](#semantic-structure)
3. [Property Specification](#property-specification)
4. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
5. [Design Rationale](#design-rationale)
6. [Usage Guidelines](#usage-guidelines)
7. [Transformation Examples](#transformation-examples)
8. [SPARQL Queries](#sparql-queries)
9. [Integration with Other Properties](#integration-with-other-properties)
10. [References](#references)

---

## Property Overview

### Introduction

The `gmn:P70_18_documents_disputing_party` property is a simplified shortcut property designed for associating arbitration agreement documents with the parties involved in the dispute. This property is part of the GMN ontology's arbitration agreement modeling framework.

### Purpose

In medieval and early modern arbitration agreements, multiple parties (typically two or more) agree to submit their dispute to binding arbitration. This property captures the relationship between the document and these disputing parties, transforming the shortcut into full CIDOC-CRM compliant structure during processing.

### Context

Arbitration agreements represent a specific type of contractual transaction where parties:
1. Acknowledge an existing dispute
2. Agree to relinquish other forms of dispute resolution
3. Transfer the obligation to resolve the dispute to appointed arbitrator(s)
4. Commit to accepting the arbitrator's binding decision

The disputing parties are **active principals** who carry out this agreement, not passive participants.

---

## Semantic Structure

### Conceptual Model

```
gmn:E31_3_Arbitration_Agreement (Document)
  │
  └─ cidoc:P70_documents (documents)
      │
      └─ cidoc:E7_Activity (Arbitration Process)
          │
          ├─ cidoc:P2_has_type → AAT 300417271 (arbitration)
          │
          └─ cidoc:P14_carried_out_by (carried out by)
              │
              ├─ cidoc:E39_Actor (Disputing Party 1)
              ├─ cidoc:E39_Actor (Disputing Party 2)
              └─ cidoc:E39_Actor (Arbitrator)
```

### Shortcut vs. Full Structure

**Shortcut (Input):**
```
E31_3_Arbitration_Agreement
  └─ gmn:P70_18_documents_disputing_party → E39_Actor
```

**Full CIDOC-CRM (Output):**
```
E31_3_Arbitration_Agreement
  └─ cidoc:P70_documents
      └─ cidoc:E7_Activity
          └─ cidoc:P14_carried_out_by → E39_Actor
```

---

## Property Specification

### Basic Information

| Attribute | Value |
|-----------|-------|
| **URI** | `http://www.genoesemerchantnetworks.com/ontology#P70_18_documents_disputing_party` |
| **Label** | P70.18 documents disputing party |
| **Type** | owl:ObjectProperty, rdf:Property |
| **Status** | Active |
| **Version** | 1.0 |

### Property Characteristics

| Characteristic | Value |
|----------------|-------|
| **Domain** | gmn:E31_3_Arbitration_Agreement |
| **Range** | cidoc:E39_Actor |
| **Superproperty** | cidoc:P70_documents |
| **Cardinality** | One or many (typically two or more) |
| **Functional** | No |
| **Inverse Functional** | No |

### Metadata

| Field | Value |
|-------|-------|
| **Created** | 2025-10-17 |
| **Modified** | 2025-10-28 |
| **Creator** | GMN Ontology Team |
| **See Also** | cidoc:P70_documents, cidoc:P14_carried_out_by |

### Definition

**Official Definition:**

Simplified property for associating an arbitration agreement with a party involved in the dispute. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor. The E7_Activity should be typed as an arbitration agreement (AAT 300417271). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Disputing parties are the active principals who have agreed to submit their dispute to arbitration and are carrying out the arbitration agreement alongside the arbitrator(s).

---

## CIDOC-CRM Mapping

### Path Decomposition

The shortcut property represents this CIDOC-CRM path:

```
1. E31_3_Arbitration_Agreement (Source)
2. → P70_documents (Property)
3. → E7_Activity (Intermediate Node)
4. → P14_carried_out_by (Property)
5. → E39_Actor (Target)
```

### CIDOC-CRM Classes Used

#### E31_Document
- **Definition**: Information object that serves as documentary evidence
- **Usage**: The arbitration agreement document
- **Subclass**: gmn:E31_3_Arbitration_Agreement

#### E7_Activity
- **Definition**: Actions intentionally carried out by instances of E39_Actor
- **Usage**: The arbitration process/agreement
- **Typing**: AAT 300417271 (arbitration)

#### E39_Actor
- **Definition**: People, either individually or in groups
- **Usage**: Disputing parties (merchants, families, organizations)

### CIDOC-CRM Properties Used

#### P70_documents
- **Domain**: E31_Document
- **Range**: E1_CRM_Entity
- **Definition**: Links a document to what it documents
- **Usage**: Links arbitration agreement to arbitration activity

#### P14_carried_out_by
- **Domain**: E7_Activity
- **Range**: E39_Actor
- **Definition**: Links an activity to the actor who carried it out
- **Usage**: Links arbitration process to disputing parties and arbitrators

#### P2_has_type
- **Domain**: E1_CRM_Entity
- **Range**: E55_Type
- **Definition**: Links an entity to its type
- **Usage**: Types the activity as arbitration (AAT 300417271)

### Getty AAT Terms

#### AAT 300417271 - Arbitration
- **Label**: arbitration (process)
- **Definition**: Dispute resolution by neutral third party
- **Broader Term**: dispute resolution
- **Usage**: Type for E7_Activity node

---

## Design Rationale

### Why E7_Activity?

**Decision:** Use E7_Activity rather than E8_Acquisition

**Rationale:**
1. **Semantic Accuracy**: Arbitration is not an acquisition (transfer of ownership) but a process involving multiple parties
2. **Flexibility**: E7_Activity allows modeling various dispute resolution processes
3. **Proper Typing**: The activity type (AAT arbitration) specifies it as arbitration
4. **CIDOC-CRM Alignment**: E8 is for property transfer; E7 is appropriate for agreements and processes

### Why P14_carried_out_by?

**Decision:** Use P14_carried_out_by rather than P11_had_participant

**Rationale:**
1. **Active Agency**: Disputing parties actively agree to and carry out the arbitration
2. **Principal Role**: Parties are principals who consent to and enact the agreement
3. **Avoids Passivity**: P11 would imply passive presence rather than active engagement
4. **Consistency**: Aligns with how arbitrators are also modeled (using P14)
5. **Semantic Parallel**: Similar to sales contracts using P23/P22 for seller/buyer as active principals

### Single Shared Activity

**Decision:** All arbitration properties (P70.18, P70.19, P70.20) contribute to one E7_Activity

**Rationale:**
1. **Semantic Unity**: One arbitration agreement = one arbitration process
2. **Data Integrity**: Prevents fragmentation of related information
3. **Query Efficiency**: Easier to retrieve complete arbitration information
4. **CIDOC-CRM Pattern**: Matches sales contract pattern (one acquisition event)
5. **Logical Coherence**: Parties, arbitrators, and subject are all part of same process

### Shortcut Approach

**Decision:** Provide shortcut property that transforms to full CIDOC-CRM structure

**Rationale:**
1. **Usability**: Simplified data entry for content creators
2. **Compliance**: Ensures CIDOC-CRM conformance in output
3. **Flexibility**: Allows system to handle both formats
4. **Best Practice**: Common pattern in cultural heritage ontologies

---

## Usage Guidelines

### When to Use This Property

Use `gmn:P70_18_documents_disputing_party` when:

1. **Document Type**: Working with arbitration agreement documents (gmn:E31_3_Arbitration_Agreement)
2. **Party Identification**: You need to specify who the disputing parties are
3. **Multiple Parties**: Typically two or more parties with a conflict
4. **Active Principals**: Parties who actively agreed to arbitration

### When NOT to Use This Property

Do NOT use for:

1. **Arbitrators**: Use gmn:P70_19_documents_arbitrator instead
2. **Non-Arbitration Documents**: Limited to arbitration agreements only
3. **Passive References**: Use cidoc:P67_refers_to for mere mentions
4. **Other Contract Types**: Use appropriate properties for sales, donations, etc.
5. **Witnesses**: Use appropriate witness properties

### Cardinality Considerations

**Minimum**: While technically one party is possible, arbitration semantically requires at least two disputing parties

**Maximum**: No limit; complex disputes may involve many parties

**Typical**: Two parties (bilateral dispute)

**Example Scenarios**:
- Two merchants disputing contract terms (typical)
- Three heirs disputing inheritance (common)
- Multiple families disputing property rights (complex)

### Data Quality Guidelines

**Required Information:**
- Valid E39_Actor URI for each party
- Party must exist or be created in system

**Optional Information:**
- Party names (via P1_is_identified_by on actor)
- Party roles (future enhancement via P14.1)
- Party relationships

**Validation Rules:**
1. Each party URI must resolve to an E39_Actor
2. Minimum two parties recommended (though not enforced)
3. No duplicate parties in same agreement
4. Parties should differ from arbitrator(s)

---

## Transformation Examples

### Example 1: Simple Two-Party Arbitration

**Input:**
```json
{
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [
    {"@value": "Arbitration between Spinola and Doria"}
  ],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/antonio_spinola"},
    {"@id": "http://example.org/persons/giovanni_doria"}
  ]
}
```

**Output:**
```json
{
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P1_is_identified_by": [{
    "@id": "http://example.org/contracts/arb001/appellation/abc123",
    "@type": "cidoc:E41_Appellation",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300404650",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P190_has_symbolic_content": "Arbitration between Spinola and Doria"
  }],
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P14_carried_out_by": [
      {
        "@id": "http://example.org/persons/antonio_spinola",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/giovanni_doria",
        "@type": "cidoc:E39_Actor"
      }
    ]
  }]
}
```

### Example 2: Multiple Parties (Three-Way Dispute)

**Input:**
```json
{
  "@id": "http://example.org/contracts/arb002",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/heir1"},
    {"@id": "http://example.org/persons/heir2"},
    {"@id": "http://example.org/persons/heir3"}
  ]
}
```

**Output:**
```json
{
  "@id": "http://example.org/contracts/arb002",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb002/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P14_carried_out_by": [
      {"@id": "http://example.org/persons/heir1", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/heir2", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/heir3", "@type": "cidoc:E39_Actor"}
    ]
  }]
}
```

### Example 3: Complete Arbitration (With Arbitrator and Subject)

**Input:**
```json
{
  "@id": "http://example.org/contracts/arb003",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/judge_marco"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/property/palazzo_genoa"}
  ]
}
```

**Output:**
```json
{
  "@id": "http://example.org/contracts/arb003",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb003/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P14_carried_out_by": [
      {"@id": "http://example.org/persons/party1", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/party2", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/judge_marco", "@type": "cidoc:E39_Actor"}
    ],
    "cidoc:P16_used_specific_object": [
      {"@id": "http://example.org/property/palazzo_genoa", "@type": "cidoc:E1_CRM_Entity"}
    ]
  }]
}
```

**Note**: All three properties (P70.18, P70.19, P70.20) contribute to the same activity node.

### Example 4: Parties as URIs (String Format)

**Input:**
```json
{
  "@id": "http://example.org/contracts/arb004",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    "http://example.org/persons/merchant_a",
    "http://example.org/persons/merchant_b"
  ]
}
```

**Output:**
```json
{
  "@id": "http://example.org/contracts/arb004",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb004/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P14_carried_out_by": [
      {"@id": "http://example.org/persons/merchant_a", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/merchant_b", "@type": "cidoc:E39_Actor"}
    ]
  }]
}
```

**Note**: Transformation handles both object format (`{"@id": "..."}`) and string format.

---

## SPARQL Queries

### Query 1: Find All Arbitrations for a Specific Person

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?name ?date
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by <http://example.org/persons/antonio_spinola> .
  
  OPTIONAL {
    ?agreement cidoc:P1_is_identified_by ?appellation .
    ?appellation cidoc:P190_has_symbolic_content ?name .
  }
  
  OPTIONAL {
    ?agreement gmn:P94i_2_has_enactment_date ?date .
  }
}
ORDER BY ?date
```

### Query 2: Find All Disputing Parties in Arbitrations

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT DISTINCT ?agreement ?party ?party_name
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by ?party .
  
  # Get party name
  OPTIONAL {
    ?party cidoc:P1_is_identified_by ?party_appellation .
    ?party_appellation cidoc:P190_has_symbolic_content ?party_name .
  }
}
ORDER BY ?agreement ?party_name
```

### Query 3: Count Arbitrations by Number of Parties

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement (COUNT(?party) AS ?party_count)
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by ?party .
}
GROUP BY ?agreement
ORDER BY DESC(?party_count)
```

### Query 4: Find Arbitrations Between Specific Parties

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?date
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  
  # Must include both specific parties
  ?activity cidoc:P14_carried_out_by <http://example.org/persons/spinola> .
  ?activity cidoc:P14_carried_out_by <http://example.org/persons/doria> .
  
  OPTIONAL {
    ?agreement gmn:P94i_2_has_enactment_date ?date .
  }
}
ORDER BY ?date
```

### Query 5: Find All Parties Who Have Been in Arbitration

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT DISTINCT ?party ?party_name (COUNT(DISTINCT ?agreement) AS ?arbitration_count)
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by ?party .
  
  OPTIONAL {
    ?party cidoc:P1_is_identified_by ?appellation .
    ?appellation cidoc:P190_has_symbolic_content ?party_name .
  }
}
GROUP BY ?party ?party_name
ORDER BY DESC(?arbitration_count)
```

### Query 6: Distinguish Disputing Parties from Arbitrators

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?person ?role
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by ?person .
  
  # Before transformation, we can check source properties
  OPTIONAL {
    ?agreement gmn:P70_18_documents_disputing_party ?person .
    BIND("Disputing Party" AS ?role)
  }
  OPTIONAL {
    ?agreement gmn:P70_19_documents_arbitrator ?person .
    BIND("Arbitrator" AS ?role)
  }
}
```

**Note**: This query works on pre-transformation data. Post-transformation, roles must be distinguished by context or future P14.1 role typing.

---

## Integration with Other Properties

### Related Arbitration Properties

The P70.18 property works in conjunction with:

#### gmn:P70_19_documents_arbitrator
- **Purpose**: Specifies the arbitrator(s)
- **Relationship**: Shares same E7_Activity node
- **Usage**: Add after or alongside P70.18

#### gmn:P70_20_documents_dispute_subject
- **Purpose**: Specifies what the dispute is about
- **Relationship**: Shares same E7_Activity node
- **Usage**: Add after or alongside P70.18

### Standard Document Properties

Can be combined with:

#### Creation Properties
- `gmn:P94i_1_was_created_by` - Notary who recorded agreement
- `gmn:P94i_2_has_enactment_date` - Date of agreement
- `gmn:P94i_3_has_place_of_enactment` - Location of agreement

#### Identification Properties
- `gmn:P1_1_has_name` - Name/title of agreement
- `gmn:P102_1_has_title` - Formal title from document

#### Archival Properties
- `gmn:P46i_1_is_contained_in` - Archival location

### Example Combined Usage

```json
{
  "@id": "http://example.org/contracts/arb_complete",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  
  "gmn:P1_1_has_name": [
    {"@value": "Arbitration Agreement - Trade Dispute"}
  ],
  
  "gmn:P94i_1_was_created_by": [
    {"@id": "http://example.org/notaries/giovanni_notary"}
  ],
  
  "gmn:P94i_2_has_enactment_date": [
    {"@value": "1450-06-15", "@type": "xsd:date"}
  ],
  
  "gmn:P94i_3_has_place_of_enactment": [
    {"@id": "http://example.org/places/genoa"}
  ],
  
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/merchant1"},
    {"@id": "http://example.org/persons/merchant2"}
  ],
  
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator"}
  ],
  
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/objects/shipment_goods"}
  ]
}
```

---

## References

### CIDOC-CRM References

- **CIDOC-CRM Homepage**: http://www.cidoc-crm.org/
- **E7_Activity**: http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.1
- **E31_Document**: http://www.cidoc-crm.org/Entity/E31-Document/version-7.1.1
- **E39_Actor**: http://www.cidoc-crm.org/Entity/E39-Actor/version-7.1.1
- **P14_carried_out_by**: http://www.cidoc-crm.org/Property/P14-carried-out-by/version-7.1.1
- **P70_documents**: http://www.cidoc-crm.org/Property/P70-documents/version-7.1.1

### Getty AAT References

- **Arbitration (process)**: http://vocab.getty.edu/page/aat/300417271
- **AAT Browser**: http://www.getty.edu/research/tools/vocabularies/aat/

### GMN Documentation

- Arbitration Agreement Ontology: `arbitration-ontology.md`
- GMN Ontology Main File: `gmn_ontology.ttl`
- Transformation Script: `gmn_to_cidoc_transform.py`

### Academic References

1. Greif, A. (2006). *Institutions and the Path to the Modern Economy*. Cambridge University Press.
2. Padgett, J. F., & McLean, P. D. (2006). "Organizational Invention and Elite Transformation: The Birth of Partnership Systems in Renaissance Florence." *American Journal of Sociology*, 111(5), 1463-1568.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-28 | GMN Team | Initial documentation |

---

## Appendix: Transformation Pseudocode

```python
FUNCTION transform_p70_18_documents_disputing_party(data):
    # Check if property exists
    IF 'gmn:P70_18_documents_disputing_party' NOT IN data:
        RETURN data
    
    # Get parties and document URI
    parties = data['gmn:P70_18_documents_disputing_party']
    document_uri = data['@id']
    
    # Create or locate activity
    IF 'cidoc:P70_documents' NOT IN data OR data['cidoc:P70_documents'] IS EMPTY:
        activity_uri = document_uri + "/arbitration"
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity'
        }
        data['cidoc:P70_documents'] = [activity]
    ELSE:
        activity = data['cidoc:P70_documents'][0]
    
    # Initialize P14 array if needed
    IF 'cidoc:P14_carried_out_by' NOT IN activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    # Add each party
    FOR EACH party IN parties:
        IF party IS dict:
            party_data = copy(party)
            IF '@type' NOT IN party_data:
                party_data['@type'] = 'cidoc:E39_Actor'
        ELSE:
            party_data = {
                '@id': str(party),
                '@type': 'cidoc:E39_Actor'
            }
        
        activity['cidoc:P14_carried_out_by'].append(party_data)
    
    # Remove shortcut property
    DELETE data['gmn:P70_18_documents_disputing_party']
    
    RETURN data
```

---

**Document Status**: Complete and ready for implementation
