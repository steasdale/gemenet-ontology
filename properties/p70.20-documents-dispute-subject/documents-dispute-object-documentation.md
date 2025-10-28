# Property Documentation: P70.20 Documents Dispute Subject
## GMN Ontology - Arbitration Agreement Properties

**Property URI:** `http://www.genoesemerchantnetworks.com/ontology#P70_20_documents_dispute_subject`  
**Version:** 1.0  
**Status:** Active  
**Last Updated:** October 28, 2025

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Semantic Specification](#semantic-specification)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Usage Guidelines](#usage-guidelines)
5. [Examples](#examples)
6. [Transformation Details](#transformation-details)
7. [Design Rationale](#design-rationale)
8. [Related Properties](#related-properties)
9. [SPARQL Query Examples](#sparql-query-examples)
10. [References](#references)

---

## Property Overview

### Summary

The `gmn:P70_20_documents_dispute_subject` property provides a simplified way to associate an arbitration agreement document with the subject matter of the dispute being arbitrated. It represents what the conflict is about - the matter in contention that the arbitrators will decide upon.

### Key Information

| Aspect | Value |
|--------|-------|
| **Property Name** | P70_20_documents_dispute_subject |
| **Label** | P70.20 documents dispute subject |
| **Domain** | gmn:E31_3_Arbitration_Agreement |
| **Range** | cidoc:E1_CRM_Entity |
| **Superproperty** | cidoc:P70_documents |
| **Cardinality** | One or many (1..*) |
| **Created** | 2025-10-17 |
| **Modified** | 2025-10-18 |

### Purpose

This property serves as a **shortcut property** for data entry, representing a more complex CIDOC-CRM path. It enables:

1. **Simplified data entry** - Direct linking of disputes to their subjects
2. **Clear semantics** - Explicit representation of what disputes concern
3. **CIDOC-CRM compliance** - Transforms to full standards-compliant structure
4. **Flexible typing** - Supports any entity type as dispute subject
5. **Query efficiency** - Easy retrieval of dispute subjects

---

## Semantic Specification

### Definition

**Formal Definition:**  
Simplified property for associating an arbitration agreement with the subject matter of the dispute being arbitrated. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity.

**Plain Language:**  
This property indicates what the arbitration is about - what is being disputed and what the arbitrators need to make a decision about.

### Scope

**Includes:**
- Physical property (buildings, land, ships, goods)
- Legal rights and obligations
- Monetary debts or claims
- Contract disputes
- Services or performances
- Abstract legal objects
- Any entity that can be the subject of a dispute

**Excludes:**
- Mentions of entities not central to the dispute (use cidoc:P67_refers_to)
- Contextual background entities (use cidoc:P67_refers_to)
- Related but not disputed entities (use cidoc:P67_refers_to)

### Domain

**Class:** `gmn:E31_3_Arbitration_Agreement`

**Description:**  
The property's domain is restricted to arbitration agreement documents. Only documents explicitly classified as arbitration agreements should use this property.

**Rationale:**  
Arbitration agreements specifically document the transfer of dispute resolution obligations to arbitrators, making the dispute subject a central semantic element. Other document types have different relationships to their referenced entities.

### Range

**Class:** `cidoc:E1_CRM_Entity`

**Description:**  
The broadest possible CIDOC-CRM class, allowing any entity to be a dispute subject.

**Rationale:**  
Disputes in historical records involved remarkably diverse subjects:
- Physical objects (E18_Physical_Thing)
- Conceptual objects (E28_Conceptual_Object)
- Legal objects (E72_Legal_Object)
- Activities (E7_Activity)
- Documents (E31_Document)
- Temporal entities (E2_Temporal_Entity)

Using E1_CRM_Entity provides maximum flexibility while maintaining semantic precision through subtyping.

### Cardinality

**Minimum:** 1  
**Maximum:** Unlimited

**Typical Cases:**
- Single subject: One building, one debt, one right
- Multiple subjects: Several related properties, multiple contract clauses
- Complex disputes: Combination of different entity types

**Design Note:**  
While most disputes have a primary subject, medieval arbitrations often involved multiple interrelated subjects (e.g., a debt, the underlying transaction, and property collateral).

---

## CIDOC-CRM Mapping

### Shortcut Structure

```
gmn:P70_20_documents_dispute_subject
    ↓ (represents)
E31_Document 
  → P70_documents 
    → E7_Activity 
      → P16_used_specific_object 
        → E1_CRM_Entity
```

### Full Path Explanation

1. **E31_Document (Arbitration Agreement)**
   - The arbitration agreement document

2. **P70_documents**
   - Property linking document to the activity it documents

3. **E7_Activity (Arbitration Process)**
   - The arbitration activity/process
   - Typed with AAT 300417271 (arbitration)
   - Shared with P70.18 and P70.19 properties

4. **P16_used_specific_object**
   - Property indicating the activity operates on/concerns specific objects
   - Semantically: "the arbitration uses knowledge of [subject] to resolve the dispute"

5. **E1_CRM_Entity (Dispute Subject)**
   - Any entity that is the subject of the dispute

### Property Choice: P16 vs P67

**Selected:** `P16_used_specific_object`

**Alternative Considered:** `P67_refers_to`

**Rationale:**

| Criterion | P16 | P67 |
|-----------|-----|-----|
| **Semantic Strength** | ✅ Central to activity | ❌ Mere mention |
| **Activity Integration** | ✅ Object is used | ❌ Just referenced |
| **Query Precision** | ✅ Clearly dispute subjects | ❌ Mixed with other refs |
| **Ontological Clarity** | ✅ Active relationship | ❌ Passive relationship |

The dispute subject is not merely mentioned - it's what the arbitration **operates on**. The arbitrators use knowledge of the subject to render their decision. This active, operational relationship is better captured by P16.

### Activity Typing

The E7_Activity is typed using:

```json
{
  "cidoc:P2_has_type": {
    "@id": "http://vocab.getty.edu/page/aat/300417271",
    "@type": "cidoc:E55_Type",
    "rdfs:label": "arbitration (process)"
  }
}
```

This Getty AAT term explicitly identifies the activity as an arbitration process, distinguishing it from other legal activities.

---

## Usage Guidelines

### When to Use This Property

✅ **Use gmn:P70_20_documents_dispute_subject when:**

1. The document is an arbitration agreement
2. The subject is central to the dispute
3. The arbitrators must make a decision about the entity
4. The entity is specifically identified in the agreement
5. Multiple subjects are all matters in contention

### When NOT to Use This Property

❌ **Do NOT use for:**

1. **Background entities** - Use cidoc:P67_refers_to instead
   ```json
   // Wrong:
   "gmn:P70_20_documents_dispute_subject": [{"@id": "city_of_genoa"}]
   
   // Right:
   "cidoc:P67_refers_to": [{"@id": "city_of_genoa"}]
   ```

2. **Related but not disputed entities** - Use cidoc:P67_refers_to
   ```json
   // If dispute is about a building, but mentions a nearby church:
   "gmn:P70_20_documents_dispute_subject": [{"@id": "disputed_building"}]
   "cidoc:P67_refers_to": [{"@id": "neighboring_church"}]
   ```

3. **Non-arbitration documents** - This is domain-restricted
   ```json
   // Wrong:
   {
     "@type": "gmn:E31_2_Sales_Contract",
     "gmn:P70_20_documents_dispute_subject": [...]  // Error!
   }
   ```

4. **Arbitration outcomes** - Use different property for decisions
   ```json
   // The dispute subject is not the arbitration award itself
   ```

### Best Practices

1. **Link to existing entities when possible**
   ```json
   // Preferred:
   "gmn:P70_20_documents_dispute_subject": [
     {"@id": "http://example.org/property/building_123"}
   ]
   
   // Rather than creating inline:
   "gmn:P70_20_documents_dispute_subject": [{
     "@id": "_:blank_node",
     "@type": "cidoc:E22_1_Building",
     "rdfs:label": "some building"
   }]
   ```

2. **Type entities appropriately**
   ```json
   // Good - specific type:
   {
     "@id": "http://example.org/debts/debt_001",
     "@type": "cidoc:E72_Legal_Object"
   }
   
   // Acceptable - general type:
   {
     "@id": "http://example.org/subjects/unknown_type",
     "@type": "cidoc:E1_CRM_Entity"
   }
   ```

3. **Include all subjects equally**
   ```json
   // If dispute involves both a debt and collateral property:
   "gmn:P70_20_documents_dispute_subject": [
     {"@id": "http://example.org/debts/debt_xyz"},
     {"@id": "http://example.org/property/warehouse"}
   ]
   ```

4. **Coordinate with other arbitration properties**
   ```json
   {
     "@type": "gmn:E31_3_Arbitration_Agreement",
     "gmn:P70_18_documents_disputing_party": [...],   // Who
     "gmn:P70_19_documents_arbitrator": [...],        // Who decides
     "gmn:P70_20_documents_dispute_subject": [...]    // What about
   }
   ```

---

## Examples

### Example 1: Single Property Dispute

**Scenario:** Two merchants dispute ownership of a warehouse in Genoa.

**Input Data (simplified):**

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [
    {"@value": "Arbitration Agreement - Spinola Warehouse"}
  ],
  "gmn:P94i_2_has_enactment_date": [
    {"@value": "1450-03-15", "@type": "xsd:date"}
  ],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/merchant_a"},
    {"@id": "http://example.org/persons/merchant_b"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_giovanni"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {
      "@id": "http://example.org/property/warehouse_spinola_port",
      "@type": "gmn:E22_1_Building"
    }
  ]
}
```

**Output (transformed):**

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [
    {"@value": "Arbitration Agreement - Spinola Warehouse"}
  ],
  "gmn:P94i_2_has_enactment_date": [
    {"@value": "1450-03-15", "@type": "xsd:date"}
  ],
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271",
      "@type": "cidoc:E55_Type",
      "rdfs:label": "arbitration (process)"
    },
    "cidoc:P14_carried_out_by": [
      {
        "@id": "http://example.org/persons/merchant_a",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/merchant_b",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/arbitrator_giovanni",
        "@type": "cidoc:E39_Actor"
      }
    ],
    "cidoc:P16_used_specific_object": [
      {
        "@id": "http://example.org/property/warehouse_spinola_port",
        "@type": "gmn:E22_1_Building"
      }
    ]
  }]
}
```

### Example 2: Complex Multi-Subject Dispute

**Scenario:** Partnership dispute involving a debt, the underlying shipping contract, and a vessel.

**Input Data:**

```json
{
  "@id": "http://example.org/contracts/arb002",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [
    {"@value": "Arbitration - Doria Partnership Dispute"}
  ],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/partner1"},
    {"@id": "http://example.org/persons/partner2"},
    {"@id": "http://example.org/persons/partner3"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_panel1"},
    {"@id": "http://example.org/persons/arbitrator_panel2"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {
      "@id": "http://example.org/debts/partnership_debt_001",
      "@type": "cidoc:E72_Legal_Object"
    },
    {
      "@id": "http://example.org/contracts/shipping_contract_456",
      "@type": "gmn:E31_1_Contract"
    },
    {
      "@id": "http://example.org/ships/galley_santa_maria",
      "@type": "gmn:E22_2_Moveable_Property"
    }
  ]
}
```

**Output (arbitration activity only):**

```json
{
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb002/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P14_carried_out_by": [
      {"@id": "http://example.org/persons/partner1", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/partner2", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/partner3", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/arbitrator_panel1", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/arbitrator_panel2", "@type": "cidoc:E39_Actor"}
    ],
    "cidoc:P16_used_specific_object": [
      {
        "@id": "http://example.org/debts/partnership_debt_001",
        "@type": "cidoc:E72_Legal_Object"
      },
      {
        "@id": "http://example.org/contracts/shipping_contract_456",
        "@type": "gmn:E31_1_Contract"
      },
      {
        "@id": "http://example.org/ships/galley_santa_maria",
        "@type": "gmn:E22_2_Moveable_Property"
      }
    ]
  }]
}
```

### Example 3: Land Rights Dispute

**Scenario:** Dispute over land use rights between religious institution and merchant.

```json
{
  "@id": "http://example.org/contracts/arb003",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/institutions/monastery_san_lorenzo"},
    {"@id": "http://example.org/persons/merchant_grimaldi"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/bishop_representative"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {
      "@id": "http://example.org/legal/land_use_right_001",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Right to use land adjacent to monastery"
    }
  ],
  "cidoc:P67_refers_to": [
    {
      "@id": "http://example.org/places/land_parcel_near_monastery",
      "@type": "cidoc:E53_Place",
      "rdfs:comment": "The physical land (mentioned but not itself disputed)"
    }
  ]
}
```

**Note:** The legal right is the dispute subject (P70.20), while the physical land is merely referenced (P67).

---

## Transformation Details

### Transformation Algorithm

```python
def transform_p70_20_documents_dispute_subject(data):
    """
    Transform dispute subject shortcut property to full CIDOC-CRM structure.
    
    Steps:
    1. Check if property exists
    2. Extract dispute subjects (ensure list format)
    3. Find or create E7_Activity
    4. Initialize P16_used_specific_object array
    5. Add each subject with appropriate typing
    6. Remove shortcut property
    """
    
    # Step 1: Check existence
    if 'gmn:P70_20_documents_dispute_subject' not in data:
        return data
    
    # Step 2: Extract subjects
    subjects = data['gmn:P70_20_documents_dispute_subject']
    if not isinstance(subjects, list):
        subjects = [subjects]
    
    # Step 3: Get document URI
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 4: Find or create activity
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': 'http://vocab.getty.edu/page/aat/300417271',
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    # Step 5: Initialize P16 array
    if 'cidoc:P16_used_specific_object' not in activity:
        activity['cidoc:P16_used_specific_object'] = []
    
    # Step 6: Add subjects
    for subject_obj in subjects:
        if isinstance(subject_obj, dict):
            subject_data = subject_obj.copy()
            if '@type' not in subject_data:
                subject_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            subject_data = {
                '@id': str(subject_obj),
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    # Step 7: Remove shortcut
    del data['gmn:P70_20_documents_dispute_subject']
    
    return data
```

### Activity Sharing Mechanism

The transformation ensures all three arbitration properties (P70.18, P70.19, P70.20) share the same E7_Activity:

1. **First property processed** creates the activity
2. **Subsequent properties** detect existing activity
3. **All properties** add to same activity node

This creates a unified semantic structure:

```
E7_Activity (arbitration)
  ├─ P14_carried_out_by (from P70.18) → disputing parties
  ├─ P14_carried_out_by (from P70.19) → arbitrators
  └─ P16_used_specific_object (from P70.20) → dispute subjects
```

### Entity Typing Strategy

```python
# If subject already has @type, preserve it:
subject_data = {
    "@id": "http://example.org/property/house",
    "@type": "gmn:E22_1_Building"  # Preserved
}

# If subject lacks @type, add generic:
subject_data = {
    "@id": "http://example.org/unknown/entity",
    "@type": "cidoc:E1_CRM_Entity"  # Added
}

# Specific types are preferred when known:
PREFERRED_TYPES = {
    "building": "gmn:E22_1_Building",
    "ship": "gmn:E22_2_Moveable_Property",
    "debt": "cidoc:E72_Legal_Object",
    "contract": "gmn:E31_1_Contract"
}
```

---

## Design Rationale

### Why P16 Instead of P67?

**P16_used_specific_object** was chosen over **P67_refers_to** for semantic precision:

**P16 Semantics:**
- The activity **uses** or **operates on** the object
- The object is central to the activity's purpose
- Strong, operational relationship
- Examples: tools used, subjects examined, matters decided

**P67 Semantics:**
- The entity merely **mentions** or **references** the object
- The object provides context but isn't central
- Weak, referential relationship
- Examples: background information, related entities

For arbitration, the dispute subject is **what the activity is about** - the arbitrators must examine it, understand it, and make decisions about it. This is clearly P16 territory.

### Why E1_CRM_Entity Range?

Using the broadest possible range (E1_CRM_Entity) provides:

1. **Maximum Flexibility**
   - Any entity type can be a dispute subject
   - No artificial restrictions on historical data

2. **Historical Accuracy**
   - Medieval disputes involved diverse subjects
   - Restricting range would misrepresent historical reality

3. **Future-Proofing**
   - New entity types can be dispute subjects
   - No ontology changes needed for new cases

4. **Semantic Clarity via Subtyping**
   - Precision comes from specific @type on instances
   - Generic range doesn't prevent specific typing

### Shared Activity Design

All three arbitration properties contribute to one E7_Activity:

**Alternative Considered:** Separate activities for each aspect

**Chosen Approach:** Single shared activity

**Reasons:**
1. **Semantic Unity:** One agreement = one arbitration
2. **Data Integrity:** All info stays together
3. **Query Efficiency:** Single node to query
4. **CIDOC-CRM Pattern:** Matches acquisition pattern
5. **Logical Coherence:** Parties, arbitrators, and subject are aspects of one process

---

## Related Properties

### P70.18 Documents Disputing Party

```turtle
gmn:P70_18_documents_disputing_party
    rdfs:label "P70.18 documents disputing party" ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E39_Actor ;
    # Transforms to: P70_documents > E7_Activity > P14_carried_out_by
```

**Relationship:** Shares same E7_Activity; identifies WHO is disputing

### P70.19 Documents Arbitrator

```turtle
gmn:P70_19_documents_arbitrator
    rdfs:label "P70.19 documents arbitrator" ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E39_Actor ;
    # Transforms to: P70_documents > E7_Activity > P14_carried_out_by
```

**Relationship:** Shares same E7_Activity; identifies WHO decides

### P70.20 Documents Dispute Subject (this property)

```turtle
gmn:P70_20_documents_dispute_subject
    rdfs:label "P70.20 documents dispute subject" ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E1_CRM_Entity ;
    # Transforms to: P70_documents > E7_Activity > P16_used_specific_object
```

**Relationship:** Shares same E7_Activity; identifies WHAT is disputed

### Comparison Table

| Property | Range | CIDOC Path | Semantic Role |
|----------|-------|------------|---------------|
| P70.18 | E39_Actor | P14_carried_out_by | Disputing parties |
| P70.19 | E39_Actor | P14_carried_out_by | Arbitrators |
| P70.20 | E1_CRM_Entity | P16_used_specific_object | Dispute subjects |

---

## SPARQL Query Examples

### Query 1: Find All Dispute Subjects

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?agreementName ?subject ?subjectType
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  
  ?activity cidoc:P16_used_specific_object ?subject .
  
  OPTIONAL {
    ?agreement gmn:P1_1_has_name ?nameObj .
    ?nameObj rdf:value ?agreementName .
  }
  
  OPTIONAL {
    ?subject a ?subjectType .
  }
}
ORDER BY ?agreementName
```

### Query 2: Find Property Disputes

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?property ?propertyLabel
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  
  ?activity cidoc:P16_used_specific_object ?property .
  
  ?property a ?propertyType .
  
  # Filter for physical things (buildings, land, etc.)
  FILTER(?propertyType IN (gmn:E22_1_Building, cidoc:E18_Physical_Thing))
  
  OPTIONAL {
    ?property rdfs:label ?propertyLabel .
  }
}
```

### Query 3: Complex Disputes (Multiple Subjects)

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement (COUNT(?subject) AS ?subjectCount)
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  
  ?activity cidoc:P16_used_specific_object ?subject .
}
GROUP BY ?agreement
HAVING (COUNT(?subject) > 1)
ORDER BY DESC(?subjectCount)
```

### Query 4: Subjects by Type

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?subjectType (COUNT(?subject) AS ?count)
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  
  ?activity cidoc:P16_used_specific_object ?subject .
  
  ?subject a ?subjectType .
}
GROUP BY ?subjectType
ORDER BY DESC(?count)
```

### Query 5: Complete Arbitration Information

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?party ?arbitrator ?subject
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  
  # Get all parties and arbitrators
  ?activity cidoc:P14_carried_out_by ?actor .
  
  # Get dispute subjects
  ?activity cidoc:P16_used_specific_object ?subject .
  
  # Distinguish parties from arbitrators (simplified - both use P14)
  BIND(IF(EXISTS {?activity cidoc:P14_carried_out_by ?actor}, ?actor, "unknown") AS ?party)
  BIND(IF(EXISTS {?activity cidoc:P14_carried_out_by ?actor}, ?actor, "unknown") AS ?arbitrator)
}
```

### Query 6: Disputes by Date

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?agreement ?date ?subject
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             gmn:P94i_2_has_enactment_date ?dateObj ;
             cidoc:P70_documents ?activity .
  
  ?dateObj rdf:value ?date .
  
  ?activity cidoc:P16_used_specific_object ?subject .
  
  FILTER(?date >= "1450-01-01"^^xsd:date && ?date <= "1450-12-31"^^xsd:date)
}
ORDER BY ?date
```

---

## References

### CIDOC-CRM Documentation

- **E7_Activity:** http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.1
  - "This class comprises actions intentionally carried out by instances of E39_Actor that result in changes of state in the cultural, social, or physical systems documented."

- **P16_used_specific_object:** http://www.cidoc-crm.org/Property/P16-used-specific-object/version-7.1.1
  - "This property describes the use of material or immaterial things in a way essential to the performance or the outcome of an instance of E7_Activity."

- **E1_CRM_Entity:** http://www.cidoc-crm.org/Entity/E1-CRM-Entity/version-7.1.1
  - "This class comprises all things in the universe of discourse of the CIDOC Conceptual Reference Model."

- **P70_documents:** http://www.cidoc-crm.org/Property/P70-documents/version-7.1.1
  - "This property describes the CRM Entities documented as instances of E31_Document."

### Getty AAT

- **Arbitration (process):** http://vocab.getty.edu/page/aat/300417271
  - "The hearing and determining of a dispute or controversy by a person chosen by the parties or appointed under statutory authority."

### Related GMN Documentation

- **Arbitration Agreement Ontology:** `arbitration-ontology.md`
- **GMN Main Ontology:** `gmn_ontology.ttl`
- **Transformation Script:** `gmn_to_cidoc_transform.py`
- **Implementation Guide:** `documents-dispute-object-implementation-guide.md`

### Academic References

- Padgett, John F., and Paul D. McLean. "Organizational Invention and Elite Transformation: The Birth of Partnership Systems in Renaissance Florence." *American Journal of Sociology* 111.5 (2006): 1463-1568.

- Greif, Avner. "Contract Enforceability and Economic Institutions in Early Trade: The Maghribi Traders' Coalition." *American Economic Review* 83.3 (1993): 525-548.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-28 | Initial documentation |
| 0.9 | 2025-10-18 | Property modified, documentation updated |
| 0.1 | 2025-10-17 | Property created |

---

**Documentation Version:** 1.0  
**Property Version:** 1.0  
**Last Updated:** October 28, 2025  
**Status:** Production Ready  
**Maintained by:** Genoese Merchant Networks Project
