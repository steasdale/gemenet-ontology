# Arbitration Agreement Ontology Documentation

**Version:** 1.0  
**Date:** October 26, 2025  
**Ontology Version:** GMN 1.4

## Table of Contents

1. [Introduction](#introduction)
2. [Conceptual Model](#conceptual-model)
3. [Class Specification](#class-specification)
4. [Property Specifications](#property-specifications)
5. [Transformation Logic](#transformation-logic)
6. [Complete Examples](#complete-examples)
7. [Design Rationale](#design-rationale)

---

## Introduction

This document provides complete semantic documentation for the Arbitration Agreement contract subclass implementation in the Genoese Merchant Networks CIDOC-CRM extension ontology. Arbitration agreements are legal contracts that document the transfer of dispute resolution obligations from disputing parties to appointed arbitrators.

### Purpose

Arbitration agreements in medieval and early modern commerce served as binding contracts where:
1. Two or more parties involved in a dispute agree to submit their conflict to arbitration
2. One or more neutral arbitrators are appointed to hear the dispute
3. All parties agree to be bound by the arbitrator's decision
4. The dispute involves specific subject matter (property, debts, rights, obligations, etc.)

### Scope

This implementation covers:
- The arbitration agreement document itself (E31_3_Arbitration_Agreement)
- The arbitration activity/process documented by the agreement (E7_Activity)
- Parties to the dispute (P70.18)
- Appointed arbitrators (P70.19)
- Subject matter of the dispute (P70.20)

---

## Conceptual Model

### Overview

The arbitration agreement ontology models the contract as documenting an **E7_Activity** (the arbitration process) in which:
- **Disputing parties** are active principals carrying out the agreement (P14_carried_out_by)
- **Arbitrators** are active principals carrying out the agreement (P14_carried_out_by)
- **Dispute subject** is the matter being arbitrated (P16_used_specific_object)

### Semantic Structure

```
gmn:E31_3_Arbitration_Agreement
  └─ cidoc:P70_documents
      └─ cidoc:E7_Activity
          ├─ cidoc:P2_has_type → AAT 300417271 (arbitration)
          ├─ cidoc:P14_carried_out_by → E39_Actor (disputing party 1)
          ├─ cidoc:P14_carried_out_by → E39_Actor (disputing party 2)
          ├─ cidoc:P14_carried_out_by → E39_Actor (arbitrator)
          └─ cidoc:P16_used_specific_object → E1_CRM_Entity (dispute subject)
```

### Comparison with Sales Contracts

| Aspect | Sales Contract | Arbitration Agreement |
|--------|---------------|----------------------|
| **Document Class** | gmn:E31_2_Sales_Contract | gmn:E31_3_Arbitration_Agreement |
| **Central Event** | E8_Acquisition | E7_Activity (typed as arbitration) |
| **Main Actors** | P23 (seller), P22 (buyer) | P14 (disputing parties, arbitrators) |
| **Object** | P24 (property transferred) | P16 (dispute subject) |
| **Transaction Type** | Transfer of ownership | Transfer of obligation |

Both follow the pattern: **Document → P70_documents → Event → Actors & Objects**

---

## Class Specification

### gmn:E31_3_Arbitration_Agreement

**URI:** `http://www.genoesemerchantnetworks.com/ontology#E31_3_Arbitration_Agreement`

**Label:** E31.3 Arbitration Agreement

**Definition:** Specialized class that describes arbitration agreement documents. This is a specialized type of gmn:E31_1_Contract used to represent legal documents that record the agreement between disputing parties to transfer the obligation to resolve their dispute to one or more arbitrators.

**Superclass:** gmn:E31_1_Contract

**Subclass of CIDOC-CRM:** E31_Document (via gmn:E31_1_Contract)

**Domain Context:** Medieval and early modern legal documents, particularly Genoese notarial contracts

**Rationale:** 

Arbitration agreements represent a specific type of contractual transaction where parties:
1. Acknowledge an existing dispute
2. Agree to relinquish other forms of dispute resolution
3. Transfer the obligation to resolve the dispute to appointed arbitrator(s)
4. Commit to accepting the arbitrator's binding decision

This is conceptually similar to sales contracts (transfer of ownership) in that it represents a **transfer of legal obligations**. The disputing parties transfer the authority and obligation to resolve their dispute from themselves to the arbitrator(s).

**Historical Context:**

In medieval Italian commerce, arbitration was a common and efficient alternative to lengthy court proceedings. Merchants preferred arbitration because:
- Arbitrators had specialized knowledge of commercial practices
- Proceedings were faster than formal courts
- Decisions were binding and enforceable
- The process could be conducted privately

**Class Hierarchy:**

```
cidoc:E31_Document
  └─ gmn:E31_1_Contract (general contract)
      ├─ gmn:E31_2_Sales_Contract (sales/acquisition)
      └─ gmn:E31_3_Arbitration_Agreement (arbitration)
```

---

## Property Specifications

### gmn:P70_18_documents_disputing_party

**URI:** `http://www.genoesemerchantnetworks.com/ontology#P70_18_documents_disputing_party`

**Label:** P70.18 documents disputing party

**Definition:** Simplified property for associating an arbitration agreement with a party involved in the dispute.

**Domain:** gmn:E31_3_Arbitration_Agreement

**Range:** cidoc:E39_Actor

**Superproperty:** cidoc:P70_documents

**Full CIDOC-CRM Path:**
```
E31_Document 
  → P70_documents 
    → E7_Activity 
      → P14_carried_out_by 
        → E39_Actor
```

**Cardinality:** One or many (typically two or more disputing parties)

**Usage Notes:**

- Disputing parties are the individuals or groups who have a conflict and agree to submit it to arbitration
- They are **active principals** in the arbitration agreement, not passive participants
- Both/all disputing parties use this same property
- The property links to the same E7_Activity used by arbitrators

**Transformation Behavior:**

When transformed, this property:
1. Creates or locates an E7_Activity node typed as arbitration (AAT 300417271)
2. Adds the actor to the activity's P14_carried_out_by property
3. Removes the shortcut property from the document

**Example Values:**
- Reference to a person: `<person_uri>`
- Reference to a group/organization: `<organization_uri>`

**Design Decision - P14 vs P11:**

This property uses **P14_carried_out_by** rather than P11_had_participant because:
- Disputing parties actively carry out the arbitration agreement
- They are principals who consent to and enact the agreement
- P11 would imply passive presence rather than active agency
- This aligns with treating the agreement as a joint activity

---

### gmn:P70_19_documents_arbitrator

**URI:** `http://www.genoesemerchantnetworks.com/ontology#P70_19_documents_arbitrator`

**Label:** P70.19 documents arbitrator

**Definition:** Simplified property for associating an arbitration agreement with the person or persons appointed to resolve the dispute.

**Domain:** gmn:E31_3_Arbitration_Agreement

**Range:** cidoc:E39_Actor

**Superproperty:** cidoc:P70_documents

**Full CIDOC-CRM Path:**
```
E31_Document 
  → P70_documents 
    → E7_Activity 
      → P14_carried_out_by 
        → E39_Actor
```

**Cardinality:** One or many (one or more arbitrators)

**Usage Notes:**

- Arbitrators are neutral third parties appointed to hear and decide the dispute
- They are **active principals** who carry out the arbitration process
- Multiple arbitrators can be appointed (panels of arbitrators)
- Arbitrators and disputing parties share the same E7_Activity node
- Arbitrators use the same CIDOC-CRM property (P14) as disputing parties

**Transformation Behavior:**

When transformed, this property:
1. Locates the existing E7_Activity node (or creates one if none exists)
2. Adds the arbitrator to the activity's P14_carried_out_by property
3. Removes the shortcut property from the document

**Example Values:**
- Reference to a person: `<person_uri>`
- Reference to an institutional arbitrator: `<organization_uri>`

**Role Differentiation:**

While arbitrators and disputing parties both use P14_carried_out_by, they can be distinguished by:
- Context (arbitrators resolve, parties dispute)
- Order of appearance in data entry
- Future enhancement: role typing via P14.1_in_the_role_of

---

### gmn:P70_20_documents_dispute_subject

**URI:** `http://www.genoesemerchantnetworks.com/ontology#P70_20_documents_dispute_subject`

**Label:** P70.20 documents dispute subject

**Definition:** Simplified property for associating an arbitration agreement with the subject matter of the dispute being arbitrated.

**Domain:** gmn:E31_3_Arbitration_Agreement

**Range:** cidoc:E1_CRM_Entity

**Superproperty:** cidoc:P70_documents

**Full CIDOC-CRM Path:**
```
E31_Document 
  → P70_documents 
    → E7_Activity 
      → P16_used_specific_object 
        → E1_CRM_Entity
```

**Cardinality:** One or many (one or more subjects in dispute)

**Usage Notes:**

- The dispute subject can be any entity type
- Common subjects include:
  - Physical property (buildings, land, goods): E18_Physical_Thing
  - Legal objects (rights, obligations): E72_Legal_Object
  - Monetary debts or claims: E97_Monetary_Amount
  - Contract disputes: E31_Document
  - Services or performances: E7_Activity
- Multiple subjects can be referenced if the dispute involves several items

**Transformation Behavior:**

When transformed, this property:
1. Locates the existing E7_Activity node
2. Adds the entity to the activity's P16_used_specific_object property
3. Removes the shortcut property from the document

**Example Values:**
- A building: `<building_uri>` (E22_1_Building)
- A debt: `<debt_uri>` (E72_Legal_Object)
- A prior contract: `<contract_uri>` (E31_Document)
- A ship: `<ship_uri>` (E22_2_Moveable_Property)

**Semantic Meaning:**

The use of P16_used_specific_object indicates that the arbitration activity **operates on** or **concerns** the dispute subject. The arbitration process uses knowledge of the subject to render a decision about it.

---

## Transformation Logic

### Shared Activity Pattern

All three properties (P70.18, P70.19, P70.20) contribute to a single shared E7_Activity node. This is implemented through:

1. **Activity Detection:** Each transformation function first checks if a P70_documents array exists
2. **Activity Reuse:** If found, the existing E7_Activity is used
3. **Activity Creation:** If not found, a new E7_Activity is created with:
   - Type: AAT 300417271 (arbitration)
   - URI: `{contract_uri}/arbitration`

### Transformation Function Pattern

All three functions follow this pattern:

```python
def transform_p70_XX_documents_YYY(data):
    # 1. Check if property exists
    if 'gmn:P70_XX_documents_YYY' not in data:
        return data
    
    # 2. Get property values
    values = data['gmn:P70_XX_documents_YYY']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # 3. Find or create E7_Activity
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        activity_uri = f"{subject_uri}/arbitration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # 4. Initialize target property
    if 'cidoc:PXX_property' not in existing_activity:
        existing_activity['cidoc:PXX_property'] = []
    
    # 5. Add values to activity
    for value_obj in values:
        # Handle URI references and full objects
        # Add to activity
    
    # 6. Remove shortcut property
    del data['gmn:P70_XX_documents_YYY']
    
    return data
```

### Order Independence

The three transformation functions can be called in any order because:
- Each function checks for an existing activity
- The activity URI is deterministically generated
- All functions operate on the same shared node

### URI Generation

**Activity URI Pattern:** `{contract_uri}/arbitration`

**Examples:**
- Contract: `http://example.org/contracts/123`
- Activity: `http://example.org/contracts/123/arbitration`

This ensures:
- Predictable URIs
- No duplicate activities
- Clear relationship to parent document

---

## Complete Examples

### Example 1: Simple Arbitration Agreement

**Input (Omeka-S shortcut format):**

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [
    {"@value": "Arbitration between Giovanni and Marco"}
  ],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/giovanni"},
    {"@id": "http://example.org/persons/marco"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/judge_antonio"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/property/palazzo_spinola"}
  ]
}
```

**Output (CIDOC-CRM compliant):**

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P1_is_identified_by": [{
    "@id": "http://example.org/contracts/arb001/appellation/abc123",
    "@type": "cidoc:E41_Appellation",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300404650",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P190_has_symbolic_content": [{
      "@value": "Arbitration between Giovanni and Marco"
    }]
  }],
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P14_carried_out_by": [
      {
        "@id": "http://example.org/persons/giovanni",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/marco",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/judge_antonio",
        "@type": "cidoc:E39_Actor"
      }
    ],
    "cidoc:P16_used_specific_object": [{
      "@id": "http://example.org/property/palazzo_spinola",
      "@type": "cidoc:E1_CRM_Entity"
    }]
  }]
}
```

### Example 2: Complex Arbitration with Multiple Subjects

**Input:**

```json
{
  "@id": "http://example.org/contracts/arb002",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/merchant_a"},
    {"@id": "http://example.org/persons/merchant_b"},
    {"@id": "http://example.org/persons/merchant_c"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_1"},
    {"@id": "http://example.org/persons/arbitrator_2"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/debts/debt_xyz"},
    {"@id": "http://example.org/ships/ship_santa_maria"},
    {"@id": "http://example.org/contracts/partnership_001"}
  ],
  "gmn:P94i_2_has_enactment_date": [
    {"@value": "1450-06-15", "@type": "xsd:date"}
  ]
}
```

**Output (CIDOC-CRM compliant, showing arbitration activity only):**

```json
{
  "@id": "http://example.org/contracts/arb002",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb002/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P14_carried_out_by": [
      {"@id": "http://example.org/persons/merchant_a", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/merchant_b", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/merchant_c", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/arbitrator_1", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/arbitrator_2", "@type": "cidoc:E39_Actor"}
    ],
    "cidoc:P16_used_specific_object": [
      {"@id": "http://example.org/debts/debt_xyz", "@type": "cidoc:E1_CRM_Entity"},
      {"@id": "http://example.org/ships/ship_santa_maria", "@type": "cidoc:E1_CRM_Entity"},
      {"@id": "http://example.org/contracts/partnership_001", "@type": "cidoc:E1_CRM_Entity"}
    ]
  }],
  "cidoc:P94i_was_created_by": [{
    "@id": "http://example.org/contracts/arb002/creation",
    "@type": "cidoc:E65_Creation",
    "cidoc:P4_has_time-span": [{
      "@id": "http://example.org/contracts/arb002/timespan/xyz",
      "@type": "cidoc:E52_Time-Span",
      "cidoc:P82_at_some_time_within": {
        "@value": "1450-06-15",
        "@type": "xsd:date"
      }
    }]
  }]
}
```

### Example 3: Partial Transformation (Only Disputing Parties)

**Input:**

```json
{
  "@id": "http://example.org/contracts/arb003",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"}
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
      {"@id": "http://example.org/persons/party2", "@type": "cidoc:E39_Actor"}
    ]
  }]
}
```

**Note:** The activity is created even with only disputing parties. Arbitrator and dispute subject can be added later and will attach to the same activity.

---

## Design Rationale

### Why E7_Activity Instead of E8_Acquisition?

**Decision:** Use E7_Activity (general activity class) rather than E8_Acquisition

**Rationale:**

1. **Semantic Accuracy:** Arbitration is not an acquisition (transfer of physical ownership) but an activity involving multiple parties
2. **Flexibility:** E7_Activity allows modeling various dispute resolution processes
3. **Proper Typing:** The activity type (AAT arbitration) specifies it as arbitration
4. **CIDOC-CRM Alignment:** E8 is specifically for property transfer; E7 is appropriate for agreements and processes

### Why P14_carried_out_by for Both Parties and Arbitrators?

**Decision:** Use P14_carried_out_by for both disputing parties and arbitrators

**Rationale:**

1. **Active Agency:** Both parties and arbitrators are active principals in the agreement
   - Disputing parties **actively agree** to submit to arbitration
   - Arbitrators **actively agree** to conduct the arbitration
   
2. **Semantic Parallel:** Similar to how sales contracts use P23/P22 for seller/buyer as active principals

3. **Avoids Passive Interpretation:** P11_had_participant would suggest passive presence rather than active engagement

4. **Contractual Nature:** The arbitration agreement is a joint activity that all parties carry out together

5. **Historical Accuracy:** Medieval arbitration required active consent and participation from all parties

**Alternative Considered:** P11_had_participant
- **Rejected because:** Implies passive participation
- **Use case for P11:** Would be appropriate for witnesses to the arbitration, not the principals

### Why P16_used_specific_object for Dispute Subject?

**Decision:** Use P16_used_specific_object to link dispute subjects

**Rationale:**

1. **Semantic Fit:** The arbitration activity operates on/uses knowledge of the disputed object
2. **CIDOC-CRM Pattern:** P16 is used when an activity involves a specific object
3. **Flexibility:** Range of E1_CRM_Entity allows any type of dispute subject
4. **Clarity:** Distinguishes the dispute subject from the participants

**Alternative Considered:** P67_refers_to
- **Rejected because:** Too general; doesn't capture that the activity operates on the subject
- **P67 use case:** Better for general references, not operational relationships

### Why Single Shared E7_Activity Node?

**Decision:** All three properties contribute to one shared E7_Activity

**Rationale:**

1. **Semantic Unity:** One arbitration agreement = one arbitration activity
2. **Data Integrity:** Prevents fragmentation of related information
3. **Query Efficiency:** Easier to retrieve all information about an arbitration
4. **CIDOC-CRM Pattern:** Matches the sales contract pattern (one acquisition event)
5. **Logical Coherence:** The parties, arbitrators, and subject are all part of the same process

---

## Usage Guidelines

### When to Use Arbitration Agreement Class

Use `gmn:E31_3_Arbitration_Agreement` when:
- The document records an agreement to submit a dispute to arbitration
- Two or more parties agree to be bound by an arbitrator's decision
- The document identifies the arbitrator(s)
- The dispute subject is specified or implied

### When NOT to Use Arbitration Agreement Class

Do NOT use for:
- Court proceedings (use different class or E31_Document)
- Mediation without binding decision (consider E31_1_Contract with different typing)
- Arbitration awards/decisions (use E33_Linguistic_Object referring to the arbitration)
- General dispute mentions (use cidoc:P67_refers_to on relevant document)

### Property Usage Recommendations

**P70.18 (Disputing Parties):**
- Always include all parties to the dispute
- Minimum: two parties
- Can include groups/organizations

**P70.19 (Arbitrators):**
- Include all appointed arbitrators
- Can be individual or panel
- Use even if single arbitrator

**P70.20 (Dispute Subject):**
- Include primary subject(s) of dispute
- Can be multiple subjects
- Link to existing entities when possible
- Create new entities for unmodeled subjects

### Integration with Other Properties

Arbitration agreements can use all standard contract properties:

**Document Creation:**
- `gmn:P94i_1_was_created_by` - notary who recorded the agreement
- `gmn:P94i_2_has_enactment_date` - date(s) of the agreement
- `gmn:P94i_3_has_place_of_enactment` - where agreement was made

**Identification:**
- `gmn:P1_1_has_name` - name/title of the agreement
- `gmn:P102_1_has_title` - formal title from the document

**References:**
- `cidoc:P67_refers_to` - other entities mentioned in the agreement
- `gmn:P46i_1_is_contained_in` - archival location

**Example Combined Usage:**

```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [{"@value": "Arbitration Agreement - Spinola Property"}],
  "gmn:P94i_1_was_created_by": [{"@id": "http://example.org/notaries/giovanni"}],
  "gmn:P94i_2_has_enactment_date": [{"@value": "1450-03-15", "@type": "xsd:date"}],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"}
  ],
  "gmn:P70_19_documents_arbitrator": [{"@id": "http://example.org/persons/arbitrator"}],
  "gmn:P70_20_documents_dispute_subject": [{"@id": "http://example.org/property/building123"}]
}
```

---

## SPARQL Query Examples

### Query 1: Find All Arbitration Agreements

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

SELECT ?agreement ?name
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement .
  OPTIONAL {
    ?agreement gmn:P1_1_has_name ?name .
  }
}
```

### Query 2: Find Arbitrations Involving Specific Person

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?person ?role
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by ?person .
  
  # Determine role based on property used
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

### Query 3: Find Arbitrations About Specific Property

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?property ?date
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P16_used_specific_object ?property .
  
  OPTIONAL {
    ?agreement gmn:P94i_2_has_enactment_date ?date .
  }
  
  FILTER(?property = <http://example.org/property/palazzo_123>)
}
```

### Query 4: Count Arbitrations by Year

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (YEAR(?date) AS ?year) (COUNT(?agreement) AS ?count)
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement .
  ?agreement cidoc:P94i_was_created_by ?creation .
  ?creation cidoc:P4_has_time-span ?timespan .
  ?timespan cidoc:P82_at_some_time_within ?date .
}
GROUP BY (YEAR(?date))
ORDER BY ?year
```

---

## Ontology Maintenance

### Version Control

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-26 | Initial implementation |
| 1.1 | TBD | Future enhancements |

### Future Enhancements

**Potential Additions:**

1. **Role Typing:** Add P14.1_in_the_role_of to explicitly distinguish disputing parties from arbitrators
2. **Arbitration Award:** Create property to link arbitration agreement to the resulting decision/award
3. **Timespan:** Add properties for arbitration duration or deadline
4. **Cost:** Add properties for arbitration fees or costs
5. **Conditions:** Add properties for conditions of the arbitration agreement

**Compatibility:**

All future enhancements will maintain backward compatibility with this version.

---

## References

### CIDOC-CRM References

- **E7_Activity:** http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.1
- **P14_carried_out_by:** http://www.cidoc-crm.org/Property/P14-carried-out-by/version-7.1.1
- **P16_used_specific_object:** http://www.cidoc-crm.org/Property/P16-used-specific-object/version-7.1.1
- **P70_documents:** http://www.cidoc-crm.org/Property/P70-documents/version-7.1.1

### Getty AAT References

- **Arbitration (process):** http://vocab.getty.edu/page/aat/300417271

### Related Documentation

- GMN Ontology Main Documentation
- Sales Contract Documentation
- CIDOC-CRM Official Documentation
- Implementation Guide (arbitration-agreement-implementation-guide.md)

---

## Appendix: Transformation Pseudocode

### High-Level Logic

```
FOR EACH arbitration agreement document:
    
    # Step 1: Process P70.18 (disputing parties)
    IF document has gmn:P70_18_documents_disputing_party:
        activity = get_or_create_arbitration_activity(document)
        FOR EACH party in P70_18 values:
            ADD party to activity.P14_carried_out_by
        REMOVE gmn:P70_18_documents_disputing_party from document
    
    # Step 2: Process P70.19 (arbitrators)
    IF document has gmn:P70_19_documents_arbitrator:
        activity = get_or_create_arbitration_activity(document)
        FOR EACH arbitrator in P70_19 values:
            ADD arbitrator to activity.P14_carried_out_by
        REMOVE gmn:P70_19_documents_arbitrator from document
    
    # Step 3: Process P70.20 (dispute subject)
    IF document has gmn:P70_20_documents_dispute_subject:
        activity = get_or_create_arbitration_activity(document)
        FOR EACH subject in P70_20 values:
            ADD subject to activity.P16_used_specific_object
        REMOVE gmn:P70_20_documents_dispute_subject from document

FUNCTION get_or_create_arbitration_activity(document):
    IF document has cidoc:P70_documents array:
        RETURN first element of P70_documents
    ELSE:
        CREATE new E7_Activity with:
            - @id: document_uri + "/arbitration"
            - @type: cidoc:E7_Activity
            - P2_has_type: AAT 300417271
        ADD activity to document.cidoc:P70_documents
        RETURN activity
```

---

## Glossary

**Arbitration:** A process of dispute resolution where parties agree to submit their conflict to a neutral third party (arbitrator) for a binding decision.

**Arbitrator:** A neutral third party appointed to hear a dispute and render a binding decision.

**Disputing Parties:** The individuals or groups involved in a conflict who agree to submit their dispute to arbitration.

**Dispute Subject:** The matter, object, or issue that is the subject of the dispute being arbitrated.

**E7_Activity:** CIDOC-CRM class representing actions or processes carried out by actors.

**P14_carried_out_by:** CIDOC-CRM property linking an activity to the actor(s) who perform it.

**P16_used_specific_object:** CIDOC-CRM property linking an activity to specific objects involved in or used by that activity.

**Shortcut Property:** A simplified property provided for data entry that represents a more complex CIDOC-CRM path.

---

**Document Version:** 1.0  
**Last Updated:** October 26, 2025  
**Maintained by:** Genoese Merchant Networks Project