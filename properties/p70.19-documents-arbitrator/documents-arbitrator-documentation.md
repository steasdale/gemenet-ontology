# GMN P70.19 Documents Arbitrator - Semantic Documentation

Complete semantic documentation for the `gmn:P70_19_documents_arbitrator` property, including class definitions, property specifications, transformation logic, and usage examples.

---

## Table of Contents

1. [Overview](#overview)
2. [Conceptual Model](#conceptual-model)
3. [Property Specification](#property-specification)
4. [Transformation Logic](#transformation-logic)
5. [Usage Guidelines](#usage-guidelines)
6. [Complete Examples](#complete-examples)
7. [SPARQL Queries](#sparql-queries)
8. [Integration Patterns](#integration-patterns)
9. [References](#references)

---

## Overview

### Purpose

The `gmn:P70_19_documents_arbitrator` property provides a simplified way to associate arbitration agreements with the persons or entities appointed to resolve disputes. It is a convenience property that transforms into a full CIDOC-CRM compliant structure during processing.

### Context

In medieval and early modern commerce, arbitration was a common alternative to formal court proceedings. Merchants preferred arbitration because:
- Arbitrators had specialized knowledge of commercial practices
- Proceedings were faster than courts
- Decisions were binding and enforceable
- Process could be conducted privately

Arbitrators were neutral third parties chosen by mutual agreement or appointed according to contract terms. They had the authority to hear evidence, render decisions, and their judgments were legally binding on the disputing parties.

### Semantic Foundation

This property is based on CIDOC-CRM's P70_documents pattern, which connects documents to the activities they record. The property represents a shortcut for the full path:

```
E31_Document → P70_documents → E7_Activity → P14_carried_out_by → E39_Actor
```

The key semantic insight is that arbitrators are **active principals** in the arbitration process. They don't merely observe or participate passively—they carry out the arbitration by hearing arguments, evaluating evidence, and rendering binding decisions.

---

## Conceptual Model

### Class Hierarchy

```
cidoc:E31_Document
  └─ gmn:E31_1_Contract
      └─ gmn:E31_3_Arbitration_Agreement
```

### Activity Structure

```
gmn:E31_3_Arbitration_Agreement
  └─ cidoc:P70_documents
      └─ cidoc:E7_Activity [type: AAT 300417271 - arbitration]
          ├─ cidoc:P14_carried_out_by → E39_Actor [disputing party 1]
          ├─ cidoc:P14_carried_out_by → E39_Actor [disputing party 2]
          ├─ cidoc:P14_carried_out_by → E39_Actor [arbitrator]
          └─ cidoc:P16_used_specific_object → E1_CRM_Entity [dispute subject]
```

### Shared Activity Pattern

A critical design principle is that all three arbitration properties (P70.18, P70.19, P70.20) contribute to a **single shared E7_Activity**:

- **P70.18** (disputing parties) → adds actors to P14_carried_out_by
- **P70.19** (arbitrators) → adds actors to P14_carried_out_by  
- **P70.20** (dispute subject) → adds objects to P16_used_specific_object

This ensures semantic unity: one arbitration agreement = one arbitration activity.

### Comparison with Other Document Types

| Aspect | Sales Contract | Arbitration Agreement |
|--------|---------------|----------------------|
| **Document Class** | gmn:E31_2_Sales_Contract | gmn:E31_3_Arbitration_Agreement |
| **Central Activity** | E8_Acquisition | E7_Activity (typed as arbitration) |
| **Actor Properties** | P23 (seller), P22 (buyer) | P14 (parties & arbitrators) |
| **Object Property** | P24 (property transferred) | P16 (dispute subject) |
| **Transaction Type** | Transfer of ownership | Transfer of obligation |
| **Actor Roles** | Distinct (buyer ≠ seller) | Contextual (party vs. arbitrator) |

Both follow the document → activity → actors & objects pattern, but with different event types and relationships.

---

## Property Specification

### Basic Metadata

**URI:** `http://www.genoesemerchantnetworks.com/ontology#P70_19_documents_arbitrator`

**Label:** P70.19 documents arbitrator

**Definition:** Simplified property for associating an arbitration agreement with the person or persons appointed to resolve the dispute.

**Alternative Labels:**
- documents arbitrator
- has arbitrator
- appoints arbitrator

### Domain and Range

**Domain:** `gmn:E31_3_Arbitration_Agreement`
- Must be used only with arbitration agreement documents
- Invalid for other contract types

**Range:** `cidoc:E39_Actor`
- Can be persons (E21_Person)
- Can be organizations (E74_Group)
- Typically persons in medieval context

### Superproperty

**Superproperty:** `cidoc:P70_documents`

This property is a specialization of P70_documents, meaning:
- It inherits the semantics of P70_documents
- It adds specificity about what is documented (arbitration)
- It provides a shortcut for the full CIDOC path

### Cardinality

**Cardinality:** 1..*

- **Minimum:** 1 arbitrator required
- **Maximum:** Unlimited (supports arbitration panels)
- **Typical:** 1-3 arbitrators

### Full CIDOC-CRM Path

The property expands to:

```turtle
:arbitration_agreement a gmn:E31_3_Arbitration_Agreement ;
    cidoc:P70_documents [
        a cidoc:E7_Activity ;
        cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300417271> ;
        cidoc:P14_carried_out_by :arbitrator
    ] .
```

### Transformation Behavior

**Input Format:**
```json
{
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_1"}
  ]
}
```

**Output Format:**
```json
{
  "cidoc:P70_documents": [{
    "@type": "cidoc:E7_Activity",
    "cidoc:P14_carried_out_by": [
      {
        "@id": "http://example.org/persons/arbitrator_1",
        "@type": "cidoc:E39_Actor"
      }
    ]
  }]
}
```

### Usage Notes

**When to Use:**
- Document records arbitration agreement
- Arbitrator(s) explicitly named or referenced
- Neutral third party appointed to resolve dispute

**When NOT to Use:**
- Mediators (non-binding process)
- Judges (court proceedings, not arbitration)
- Witnesses to arbitration (use P67_refers_to)
- Advisory consultants (not decision-makers)

**Design Decisions:**

1. **Why P14_carried_out_by?**
   - Arbitrators actively conduct the arbitration process
   - They exercise agency and authority
   - They perform the decision-making activity
   - P11_had_participant would imply passive presence

2. **Why Same Property as Disputing Parties?**
   - Both are principals in the arbitration activity
   - Both carry out the agreement (parties to submit, arbitrator to decide)
   - Semantic unity maintained
   - Role differentiation by context, not property

3. **Why Not Use Role Typing?**
   - Current version keeps it simple
   - Context sufficiently distinguishes roles
   - Future enhancement could add P14.1_in_the_role_of
   - Maintains backward compatibility

---

## Transformation Logic

### Algorithm Overview

```
1. Check if gmn:P70_19_documents_arbitrator exists
2. If not, return data unchanged
3. Get arbitrator value(s)
4. Check if E7_Activity already exists (from P70.18 or P70.20)
5. If yes, reuse existing activity
6. If no, create new E7_Activity with AAT typing
7. Ensure P14_carried_out_by array exists in activity
8. For each arbitrator:
   a. Create/normalize actor data structure
   b. Add to P14_carried_out_by array
9. Remove gmn:P70_19_documents_arbitrator from data
10. Return modified data
```

### Python Implementation

```python
def transform_p70_19_documents_arbitrator(data):
    """
    Transform gmn:P70_19_documents_arbitrator to full CIDOC-CRM structure.
    
    Expands: E31 → P70 → E7 → P14 → E39
    
    This function handles arbitrators appointed to resolve disputes.
    Arbitrators are active principals who carry out the arbitration.
    """
    # Step 1: Check if property exists
    if 'gmn:P70_19_documents_arbitrator' not in data:
        return data
    
    # Step 2: Get arbitrator values
    arbitrators = data['gmn:P70_19_documents_arbitrator']
    if not isinstance(arbitrators, list):
        arbitrators = [arbitrators]
    
    # Step 3: Get document URI
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 4: Find or create E7_Activity
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        # Create new activity
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': 'http://vocab.getty.edu/page/aat/300417271',
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    # Step 5: Get activity reference
    activity = data['cidoc:P70_documents'][0]
    
    # Step 6: Ensure P14_carried_out_by exists
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    # Step 7: Add each arbitrator
    for arbitrator_obj in arbitrators:
        if isinstance(arbitrator_obj, dict):
            arbitrator_data = arbitrator_obj.copy()
            if '@type' not in arbitrator_data:
                arbitrator_data['@type'] = 'cidoc:E39_Actor'
        else:
            arbitrator_uri = str(arbitrator_obj)
            arbitrator_data = {
                '@id': arbitrator_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        activity['cidoc:P14_carried_out_by'].append(arbitrator_data)
    
    # Step 8: Remove shortcut property
    del data['gmn:P70_19_documents_arbitrator']
    
    return data
```

### Integration with Related Properties

The transformation coordinates with P70.18 and P70.20:

```python
# In main pipeline
def transform_gmn_to_cidoc(data):
    # Process in sequence - order matters for shared activity
    data = transform_p70_18_documents_disputing_party(data)  # Creates activity
    data = transform_p70_19_documents_arbitrator(data)       # Reuses activity
    data = transform_p70_20_documents_dispute_subject(data)  # Reuses activity
    return data
```

All three functions follow the same pattern:
1. Check for existing `cidoc:P70_documents`
2. Reuse first activity if present
3. Create new activity only if none exists
4. Add their specific contributions

### Edge Cases

**Case 1: Arbitrator Processed First**
```json
{
  "gmn:P70_19_documents_arbitrator": [{"@id": "arb1"}]
}
```
Creates activity with just arbitrator. Later properties add to it.

**Case 2: Multiple Arbitrators**
```json
{
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "arb1"},
    {"@id": "arb2"},
    {"@id": "arb3"}
  ]
}
```
All added to same P14_carried_out_by array.

**Case 3: String URI vs Object**
```json
{
  "gmn:P70_19_documents_arbitrator": "http://example.org/persons/arb1"
}
```
Normalized to object format internally.

**Case 4: Activity Pre-exists**
```json
{
  "cidoc:P70_documents": [{
    "@id": "activity1",
    "cidoc:P14_carried_out_by": [{"@id": "party1"}]
  }],
  "gmn:P70_19_documents_arbitrator": [{"@id": "arb1"}]
}
```
Adds arbitrator to existing P14_carried_out_by.

---

## Usage Guidelines

### When to Use This Property

**Appropriate Uses:**
- Recording formal arbitration appointments
- Documenting arbitration panels
- Linking agreements to specific arbitrators
- Historical arbitration contracts

**Examples:**
- "Pietro di Giovanni was appointed as arbitrator"
- "The parties agreed to arbitration by three merchants"
- "Arbitration before the guild council"

### When NOT to Use

**Inappropriate Uses:**
- Mediators (non-binding)
- Court judges (different process)
- Witnesses to arbitration
- Legal advisors
- Notaries recording the agreement

**Use Instead:**
- Notaries → `gmn:P94i_1_was_created_by`
- Witnesses → `cidoc:P67_refers_to`
- Mediators → Consider different typing or class
- Judges → Use different document class

### Multiple Arbitrators

Arbitration panels are fully supported:

```json
{
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "person:arbitrator_1"},
    {"@id": "person:arbitrator_2"},
    {"@id": "person:arbitrator_3"}
  ]
}
```

Common patterns:
- Single arbitrator: 1 value
- Panel of two: 2 values (requires tiebreaker mechanism)
- Panel of three: 3 values (common, allows majority decision)
- Larger panels: Rare but supported

### Integration with Other Properties

**Required/Recommended Companion Properties:**

```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [{"@value": "Arbitration Agreement"}],
  "gmn:P94i_2_has_enactment_date": [{"@value": "1450-06-15", "@type": "xsd:date"}],
  "gmn:P70_18_documents_disputing_party": [...],  // Required
  "gmn:P70_19_documents_arbitrator": [...],        // This property
  "gmn:P70_20_documents_dispute_subject": [...]    // Recommended
}
```

**Related Properties:**

| Property | Relationship | Usage |
|----------|--------------|-------|
| `gmn:P70_18_documents_disputing_party` | Sibling | Share activity, both required |
| `gmn:P70_20_documents_dispute_subject` | Sibling | Share activity, recommended |
| `gmn:P94i_1_was_created_by` | Orthogonal | Documents notary/creator |
| `gmn:P94i_2_has_enactment_date` | Orthogonal | Documents agreement date |
| `cidoc:P67_refers_to` | General | For other mentioned entities |

### Data Quality Considerations

**Best Practices:**
- Always link to existing person/organization entities
- Ensure arbitrators are properly typed (E39_Actor)
- Provide consistent URIs across documents
- Include dates and places for context

**Common Mistakes:**
- Using for notaries (wrong role)
- Mixing arbitrators with witnesses
- Creating multiple activities
- Inconsistent URI patterns

---

## Complete Examples

### Example 1: Simple Arbitration

**Scenario:** Two merchants agree to arbitration by one arbitrator over a debt dispute.

**Input (GMN):**
```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [{
    "@value": "Arbitration Agreement between Spinola and Doria"
  }],
  "gmn:P94i_2_has_enactment_date": [{
    "@value": "1450-03-15",
    "@type": "xsd:date"
  }],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/luca_spinola"},
    {"@id": "http://example.org/persons/andrea_doria"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/giovanni_rossi"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/debts/debt_spinola_doria_1449"}
  ]
}
```

**Output (CIDOC-CRM):**
```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [{
    "@value": "Arbitration Agreement between Spinola and Doria"
  }],
  "gmn:P94i_2_has_enactment_date": [{
    "@value": "1450-03-15",
    "@type": "xsd:date"
  }],
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271",
      "@type": "cidoc:E55_Type",
      "rdfs:label": "arbitration"
    },
    "cidoc:P14_carried_out_by": [
      {
        "@id": "http://example.org/persons/luca_spinola",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/andrea_doria",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/giovanni_rossi",
        "@type": "cidoc:E39_Actor"
      }
    ],
    "cidoc:P16_used_specific_object": [
      {
        "@id": "http://example.org/debts/debt_spinola_doria_1449",
        "@type": "cidoc:E1_CRM_Entity"
      }
    ]
  }]
}
```

### Example 2: Arbitration Panel

**Scenario:** Complex commercial dispute with three-member arbitration panel.

**Input:**
```json
{
  "@id": "http://example.org/contracts/arb002",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [{
    "@value": "Arbitration - Partnership Dissolution"
  }],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/marco_grimaldi"},
    {"@id": "http://example.org/persons/paolo_cattaneo"},
    {"@id": "http://example.org/persons/stefano_fieschi"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_centurione"},
    {"@id": "http://example.org/persons/arbitrator_lomellini"},
    {"@id": "http://example.org/persons/arbitrator_sauli"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/contracts/partnership_123"},
    {"@id": "http://example.org/ships/ship_santa_maria"},
    {"@id": "http://example.org/warehouses/warehouse_porto"}
  ]
}
```

**Key Features:**
- Three disputing parties
- Three-member arbitration panel
- Multiple dispute subjects
- All contribute to single E7_Activity

### Example 3: Arbitrator Only (Minimal)

**Scenario:** Document fragment with just arbitrator information.

**Input:**
```json
{
  "@id": "http://example.org/contracts/arb003",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/messer_antonio"}
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
      {
        "@id": "http://example.org/persons/messer_antonio",
        "@type": "cidoc:E39_Actor"
      }
    ]
  }]
}
```

### Example 4: Institutional Arbitrator

**Scenario:** Guild or corporate body serving as arbitrator.

**Input:**
```json
{
  "@id": "http://example.org/contracts/arb004",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/merchant_a"},
    {"@id": "http://example.org/persons/merchant_b"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {
      "@id": "http://example.org/organizations/merchant_guild_genoa",
      "@type": "cidoc:E74_Group"
    }
  ]
}
```

**Note:** Arbitrator is a group (E74_Group), not a person. This is semantically valid since E74_Group is a subclass of E39_Actor.

---

## SPARQL Queries

### Query 1: Find All Arbitrators

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT DISTINCT ?arbitrator ?name
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by ?arbitrator .
  
  # Filter to just arbitrators (not disputing parties)
  # This requires checking source data or using inference
  
  OPTIONAL {
    ?arbitrator rdfs:label ?name .
  }
}
ORDER BY ?name
```

### Query 2: Count Arbitrations by Arbitrator

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?arbitrator (COUNT(DISTINCT ?agreement) AS ?count)
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by ?arbitrator .
  
  # Additional filter needed to identify arbitrators vs. parties
}
GROUP BY ?arbitrator
ORDER BY DESC(?count)
```

### Query 3: Find Arbitrations for Specific Person

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?date ?subject
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by <http://example.org/persons/giovanni_rossi> .
  
  OPTIONAL {
    ?agreement gmn:P94i_2_has_enactment_date ?date .
  }
  
  OPTIONAL {
    ?activity cidoc:P16_used_specific_object ?subject .
  }
}
ORDER BY ?date
```

### Query 4: Panel Size Analysis

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement (COUNT(?arbitrator) AS ?panel_size)
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by ?arbitrator .
  
  # Note: This counts all actors, not just arbitrators
  # Requires additional filtering or role typing
}
GROUP BY ?agreement
HAVING (COUNT(?arbitrator) > 1)
ORDER BY DESC(?panel_size)
```

### Query 5: Arbitrations by Year

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (YEAR(?date) AS ?year) (COUNT(?agreement) AS ?count)
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             gmn:P94i_2_has_enactment_date ?date .
}
GROUP BY (YEAR(?date))
ORDER BY ?year
```

---

## Integration Patterns

### Pattern 1: Complete Arbitration Agreement

```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [{"@value": "Arbitration Agreement"}],
  "gmn:P94i_1_was_created_by": [{"@id": "notary:giovanni"}],
  "gmn:P94i_2_has_enactment_date": [{"@value": "1450-06-15", "@type": "xsd:date"}],
  "gmn:P94i_3_has_place_of_enactment": [{"@id": "place:genoa"}],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "person:party_1"},
    {"@id": "person:party_2"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "person:arbitrator"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "object:dispute_subject"}
  ]
}
```

### Pattern 2: Referencing the Arbitration

Other documents can reference the arbitration:

```json
{
  "@id": "award001",
  "@type": "cidoc:E33_Linguistic_Object",
  "cidoc:P67_refers_to": [
    {"@id": "contracts/arb001"}
  ],
  "cidoc:P3_has_note": [{
    "@value": "Arbitration award based on agreement arb001"
  }]
}
```

### Pattern 3: Linking to Outcomes

Future enhancement could link arbitration to award:

```json
{
  "@id": "contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "contracts/arb001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P9_consists_of": [{
      "@id": "contracts/arb001/decision",
      "@type": "cidoc:E7_Activity",
      "cidoc:P2_has_type": {
        "@id": "aat:300417272",
        "rdfs:label": "arbitration award"
      }
    }]
  }]
}
```

---

## References

### CIDOC-CRM

- **E7_Activity:** http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.1
- **P14_carried_out_by:** http://www.cidoc-crm.org/Property/P14-carried-out-by/version-7.1.1
- **P70_documents:** http://www.cidoc-crm.org/Property/P70-documents/version-7.1.1
- **E39_Actor:** http://www.cidoc-crm.org/Entity/E39-Actor/version-7.1.1

### Getty AAT

- **Arbitration (process):** http://vocab.getty.edu/page/aat/300417271
- **Arbitration award:** http://vocab.getty.edu/page/aat/300417272

### GMN Ontology

- **E31_3_Arbitration_Agreement:** `gmn:E31_3_Arbitration_Agreement`
- **P70.18 documents disputing party:** `gmn:P70_18_documents_disputing_party`
- **P70.20 documents dispute subject:** `gmn:P70_20_documents_dispute_subject`

### Project Documentation

- Main Arbitration Ontology: `/mnt/project/arbitration-ontology.md`
- GMN Ontology File: `/mnt/project/gmn_ontology.ttl`
- Transformation Script: `/mnt/project/gmn_to_cidoc_transform.py`

---

## Future Enhancements

### Potential Additions

1. **Role Typing**
   - Add P14.1_in_the_role_of to distinguish arbitrators from parties
   - Enable precise role queries
   - Maintain backward compatibility

2. **Arbitration Award Linkage**
   - Property to link agreement to resulting award
   - Track arbitration outcomes
   - Connect process to decision

3. **Temporal Properties**
   - Arbitration duration
   - Decision deadline
   - Timespan of arbitration process

4. **Procedural Properties**
   - Arbitration rules or procedures
   - Number of hearings
   - Evidence types

### Backward Compatibility

All future enhancements will:
- Maintain existing property semantics
- Not break existing transformations
- Allow gradual adoption
- Preserve data integrity

---

## Glossary

**Arbitration:** A process of dispute resolution where parties agree to submit their conflict to a neutral third party for a binding decision.

**Arbitrator:** A neutral third party appointed to hear a dispute and render a binding decision.

**Arbitration Agreement:** A contract in which disputing parties agree to submit their dispute to arbitration and be bound by the arbitrator's decision.

**Disputing Parties:** The individuals or entities involved in a conflict who agree to arbitration.

**Dispute Subject:** The matter, property, right, or obligation that is the focus of the dispute.

**Activity (E7):** A CIDOC-CRM class representing actions, events, or processes carried out by actors.

**P14_carried_out_by:** A CIDOC-CRM property linking activities to the actors who perform them as principals.

---

*This documentation provides complete semantic specification for the P70.19 documents arbitrator property.*
