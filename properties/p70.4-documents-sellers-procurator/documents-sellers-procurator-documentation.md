# Ontology Documentation: gmn:P70_4_documents_sellers_procurator

Complete semantic documentation for the `gmn:P70_4_documents_sellers_procurator` property, including class definitions, property specifications, and transformation patterns.

---

## Table of Contents

1. [Property Specification](#property-specification)
2. [Semantic Model](#semantic-model)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Usage Guidelines](#usage-guidelines)
5. [Examples](#examples)
6. [Formal Semantics](#formal-semantics)

---

## Property Specification

### Basic Information

| Attribute | Value |
|-----------|-------|
| **URI** | `http://genizah.org/ontology/P70_4_documents_sellers_procurator` |
| **Prefix Form** | `gmn:P70_4_documents_sellers_procurator` |
| **Label** | "P70.4 documents seller's procurator" (en) |
| **Type** | `owl:ObjectProperty`, `rdf:Property` |
| **Date Created** | 2025-10-17 |
| **Status** | Active |

### Property Characteristics

| Characteristic | Value |
|----------------|-------|
| **Domain** | `gmn:E31_2_Sales_Contract` |
| **Range** | `cidoc:E21_Person` |
| **Super-Property** | `cidoc:P70_documents` |
| **Inverse** | Not defined (asymmetric) |
| **Functional** | No (multiple values allowed) |
| **Transitive** | No |

### Related Standards

| Standard | Reference |
|----------|-----------|
| **CIDOC-CRM** | P70 documents, P14 carried out by, P17 was motivated by |
| **Getty AAT** | 300025972 (agent) |
| **RDF/OWL** | ObjectProperty construct |

---

## Semantic Model

### Conceptual Overview

The `gmn:P70_4_documents_sellers_procurator` property represents the relationship between a sales contract and the person who acted as the legal representative (procurator) for the seller in the documented transaction.

**Key Concepts**:
- **Procurator**: A legal representative authorized to act on behalf of another person
- **Seller**: The party transferring title in a sales transaction
- **Representation**: The procurator acts for and in the interest of the seller
- **Documentation**: The contract explicitly names the procurator

### Historical Context

In Genizah documents and medieval Mediterranean legal practice:
- Procurators were commonly appointed to handle property transactions
- They possessed legal authority through written or verbal authorization
- Their actions bound the principal (seller) in contractual matters
- They often handled transactions when principals were absent or incapacitated

### Distinguishing from Similar Roles

| Role | Property | Key Difference |
|------|----------|----------------|
| **Procurator** | P70.4/P70.5 | Legal representative with authority to act |
| **Guarantor** | P70.6/P70.7 | Provides security, doesn't act on behalf of party |
| **Broker** | P70.8 | Facilitates transaction, represents neither party |
| **Witness** | P70.15 | Observes and attests, doesn't participate |

---

## CIDOC-CRM Mapping

### Full Semantic Path

The shortcut property represents this complete CIDOC-CRM structure:

```
E31_Document (Sales Contract)
  └─ P70_documents
      └─ E8_Acquisition
          └─ P23_transferred_title_from
          │   └─ E21_Person (Seller)
          └─ P9_consists_of
              └─ E7_Activity
                  ├─ P14_carried_out_by
                  │   └─ E21_Person (Procurator)
                  ├─ P14.1_in_the_role_of
                  │   └─ E55_Type (AAT: agent)
                  └─ P17_was_motivated_by
                      └─ E21_Person (Seller)
```

### Node Descriptions

#### E31_Document
- **Type**: `gmn:E31_2_Sales_Contract`
- **Purpose**: The contract document itself
- **Properties**: Contains all contract information

#### E8_Acquisition
- **Purpose**: Models the transfer of ownership
- **Created by**: Initial transformation of P70 properties
- **URI Pattern**: `{contract_uri}/acquisition`

#### E7_Activity
- **Purpose**: Models the procurator's actions in the transaction
- **Created by**: P70.4 transformation
- **URI Pattern**: `{contract_uri}/activity/procurator_{hash}`
- **Hash**: Last 8 digits of hash(procurator_uri + property_name)

#### E21_Person (Procurator)
- **Purpose**: The individual acting as legal representative
- **Linked via**: P14_carried_out_by
- **Role**: Qualified by P14.1_in_the_role_of → AAT:agent

#### E21_Person (Seller)
- **Purpose**: The principal whom the procurator represents
- **Linked via**: P17_was_motivated_by
- **Primary Link**: P23_transferred_title_from

#### E55_Type (Role)
- **URI**: `http://vocab.getty.edu/page/aat/300025972`
- **Term**: "agent"
- **Qualifier**: P14.1_in_the_role_of
- **Purpose**: Explicitly identifies the procurator role

### Property Semantics

#### cidoc:P70_documents
- **Domain**: E31_Document
- **Range**: E8_Acquisition
- **Meaning**: Links contract to the acquisition event it documents

#### cidoc:P9_consists_of
- **Domain**: E8_Acquisition
- **Range**: E7_Activity
- **Meaning**: The acquisition includes the procurator's activity

#### cidoc:P14_carried_out_by
- **Domain**: E7_Activity
- **Range**: E21_Person
- **Meaning**: Identifies who performed the activity

#### cidoc:P14.1_in_the_role_of
- **Domain**: E7_Activity
- **Range**: E55_Type
- **Meaning**: Qualifies the role in which the activity was performed

#### cidoc:P17_was_motivated_by
- **Domain**: E7_Activity
- **Range**: E21_Person
- **Meaning**: Links to the person on whose behalf the activity was performed

#### cidoc:P23_transferred_title_from
- **Domain**: E8_Acquisition
- **Range**: E21_Person
- **Meaning**: Identifies the seller in the transaction

---

## Usage Guidelines

### When to Use P70.4

Use `gmn:P70_4_documents_sellers_procurator` when:

✅ The contract explicitly names a procurator for the seller  
✅ The procurator has legal authority to represent the seller  
✅ The procurator actively participates in the transaction  
✅ The document clearly distinguishes the procurator from the seller  

### When NOT to Use P70.4

Do NOT use this property when:

❌ The person is merely a witness (use P70.15)  
❌ The person guarantees the transaction (use P70.6)  
❌ The person is the actual seller (use P70.1)  
❌ The relationship is unclear or ambiguous  

### Data Entry Best Practices

1. **Always pair with P70.1**: Define the seller before the procurator
2. **Use consistent URIs**: Ensure procurator and seller have stable identifiers
3. **Document authority**: Note the source of the procurator's authority in separate properties if available
4. **Check for multiple procurators**: A seller may appoint multiple procurators
5. **Verify terminology**: Ensure source text indicates legal representation, not other roles

### Multiple Values

The property accepts multiple values to accommodate:
- Multiple procurators acting jointly
- Multiple procurators for different aspects of the transaction
- Multiple instances of the same person (rare, but possible in complex contracts)

Each procurator generates a separate E7_Activity with unique URI.

---

## Examples

### Example 1: Simple Sale with Procurator

#### Scenario
David sells a house to Sarah. His brother Isaac acts as his procurator for the transaction.

#### GMN Input
```json
{
  "@id": "contract/genizah_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [{
    "@id": "person/david",
    "rdfs:label": "David ben Abraham"
  }],
  "gmn:P70_2_documents_buyer": [{
    "@id": "person/sarah",
    "rdfs:label": "Sarah bat Moses"
  }],
  "gmn:P70_4_documents_sellers_procurator": [{
    "@id": "person/isaac",
    "rdfs:label": "Isaac ben Abraham"
  }],
  "gmn:P70_3_documents_transfer_of": [{
    "@id": "place/house_123",
    "rdfs:label": "House on Street of the Goldsmiths"
  }]
}
```

#### CIDOC-CRM Output
```json
{
  "@id": "contract/genizah_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "contract/genizah_001/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P23_transferred_title_from": [{
      "@id": "person/david",
      "@type": "cidoc:E21_Person",
      "rdfs:label": "David ben Abraham"
    }],
    "cidoc:P22_transferred_title_to": [{
      "@id": "person/sarah",
      "@type": "cidoc:E21_Person",
      "rdfs:label": "Sarah bat Moses"
    }],
    "cidoc:P24_transferred_title_of": [{
      "@id": "place/house_123",
      "@type": "cidoc:E18_Physical_Thing",
      "rdfs:label": "House on Street of the Goldsmiths"
    }],
    "cidoc:P9_consists_of": [{
      "@id": "contract/genizah_001/activity/procurator_a1b2c3d4",
      "@type": "cidoc:E7_Activity",
      "cidoc:P14_carried_out_by": [{
        "@id": "person/isaac",
        "@type": "cidoc:E21_Person",
        "rdfs:label": "Isaac ben Abraham"
      }],
      "cidoc:P14.1_in_the_role_of": {
        "@id": "http://vocab.getty.edu/page/aat/300025972",
        "@type": "cidoc:E55_Type",
        "rdfs:label": "agent"
      },
      "cidoc:P17_was_motivated_by": {
        "@id": "person/david",
        "@type": "cidoc:E21_Person"
      }
    }]
  }]
}
```

#### Interpretation
- David is the seller (P23_transferred_title_from)
- Isaac acts on David's behalf (P17_was_motivated_by)
- Isaac's role is explicitly "agent" (procurator)
- The activity is part of the acquisition (P9_consists_of)

---

### Example 2: Multiple Procurators

#### Scenario
Merchant Jacob has two procurators (his sons) who jointly handle a major sale.

#### GMN Input
```json
{
  "@id": "contract/genizah_002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [{
    "@id": "person/jacob"
  }],
  "gmn:P70_4_documents_sellers_procurator": [
    {"@id": "person/joseph"},
    {"@id": "person/benjamin"}
  ]
}
```

#### CIDOC-CRM Output
```json
{
  "@id": "contract/genizah_002",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "contract/genizah_002/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P23_transferred_title_from": [{
      "@id": "person/jacob",
      "@type": "cidoc:E21_Person"
    }],
    "cidoc:P9_consists_of": [
      {
        "@id": "contract/genizah_002/activity/procurator_x1y2z3w4",
        "@type": "cidoc:E7_Activity",
        "cidoc:P14_carried_out_by": [{
          "@id": "person/joseph",
          "@type": "cidoc:E21_Person"
        }],
        "cidoc:P14.1_in_the_role_of": {
          "@id": "http://vocab.getty.edu/page/aat/300025972",
          "@type": "cidoc:E55_Type"
        },
        "cidoc:P17_was_motivated_by": {
          "@id": "person/jacob",
          "@type": "cidoc:E21_Person"
        }
      },
      {
        "@id": "contract/genizah_002/activity/procurator_p5q6r7s8",
        "@type": "cidoc:E7_Activity",
        "cidoc:P14_carried_out_by": [{
          "@id": "person/benjamin",
          "@type": "cidoc:E21_Person"
        }],
        "cidoc:P14.1_in_the_role_of": {
          "@id": "http://vocab.getty.edu/page/aat/300025972",
          "@type": "cidoc:E55_Type"
        },
        "cidoc:P17_was_motivated_by": {
          "@id": "person/jacob",
          "@type": "cidoc:E21_Person"
        }
      }
    ]
  }]
}
```

#### Interpretation
- Two separate E7_Activity nodes created
- Each has unique URI (different hash values)
- Both link to Jacob as the motivating principal
- Represents joint procuratorship

---

### Example 3: Complex Transaction with Multiple Roles

#### Scenario
A transaction where the seller has both a procurator and a guarantor.

#### GMN Input
```json
{
  "@id": "contract/genizah_003",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [{
    "@id": "person/abraham"
  }],
  "gmn:P70_4_documents_sellers_procurator": [{
    "@id": "person/moses"
  }],
  "gmn:P70_6_documents_sellers_guarantor": [{
    "@id": "person/aaron"
  }]
}
```

#### CIDOC-CRM Output
```json
{
  "@id": "contract/genizah_003",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "contract/genizah_003/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P23_transferred_title_from": [{
      "@id": "person/abraham",
      "@type": "cidoc:E21_Person"
    }],
    "cidoc:P9_consists_of": [
      {
        "@id": "contract/genizah_003/activity/procurator_m1n2o3p4",
        "@type": "cidoc:E7_Activity",
        "cidoc:P14_carried_out_by": [{
          "@id": "person/moses",
          "@type": "cidoc:E21_Person"
        }],
        "cidoc:P14.1_in_the_role_of": {
          "@id": "http://vocab.getty.edu/page/aat/300025972",
          "@type": "cidoc:E55_Type"
        },
        "cidoc:P17_was_motivated_by": {
          "@id": "person/abraham",
          "@type": "cidoc:E21_Person"
        }
      },
      {
        "@id": "contract/genizah_003/activity/guarantor_g7h8i9j0",
        "@type": "cidoc:E7_Activity",
        "cidoc:P14_carried_out_by": [{
          "@id": "person/aaron",
          "@type": "cidoc:E21_Person"
        }],
        "cidoc:P14.1_in_the_role_of": {
          "@id": "http://vocab.getty.edu/page/aat/300025614",
          "@type": "cidoc:E55_Type"
        },
        "cidoc:P17_was_motivated_by": {
          "@id": "person/abraham",
          "@type": "cidoc:E21_Person"
        }
      }
    ]
  }]
}
```

#### Interpretation
- Moses (procurator) has AAT:agent role
- Aaron (guarantor) has AAT:guarantor role (different URI)
- Both support Abraham (seller)
- Roles clearly distinguished by AAT type

---

## Formal Semantics

### OWL/RDF Representation

```turtle
@prefix gmn: <http://genizah.org/ontology/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

gmn:P70_4_documents_sellers_procurator
    a owl:ObjectProperty , rdf:Property ;
    rdfs:label "P70.4 documents seller's procurator"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the procurator (legal representative) for the seller. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (procurator), with P17_was_motivated_by linking to the seller (E21_Person). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The transformation creates an E7_Activity node that explicitly links the procurator to the seller they represent via P17_was_motivated_by."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents , cidoc:P14_carried_out_by , cidoc:P17_was_motivated_by .
```

### Axioms

#### Domain Axiom
```
∀x (P70_4_documents_sellers_procurator(x, y) → E31_2_Sales_Contract(x))
```
If x documents seller's procurator y, then x is a Sales Contract.

#### Range Axiom
```
∀x,y (P70_4_documents_sellers_procurator(x, y) → E21_Person(y))
```
If x documents seller's procurator y, then y is a Person.

#### Transformation Axiom
```
∀x,y (P70_4_documents_sellers_procurator(x, y) →
  ∃a,e (E8_Acquisition(a) ∧ E7_Activity(e) ∧
        P70_documents(x, a) ∧
        P9_consists_of(a, e) ∧
        P14_carried_out_by(e, y)))
```
If contract x documents procurator y, then there exists an acquisition a and activity e such that x documents a, a consists of e, and e is carried out by y.

#### Motivation Axiom (with seller)
```
∀x,y,z (P70_4_documents_sellers_procurator(x, y) ∧
        P70_1_documents_seller(x, z) →
  ∃e (E7_Activity(e) ∧ P17_was_motivated_by(e, z)))
```
If x documents procurator y and seller z, then the procurator's activity is motivated by z.

### Inference Rules

#### Rule 1: Activity Creation
```
IF   contract P70_4_documents_sellers_procurator procurator
THEN create Activity
     AND Activity P14_carried_out_by procurator
```

#### Rule 2: Role Assignment
```
IF   Activity P14_carried_out_by procurator
     AND context is seller's procurator
THEN Activity P14.1_in_the_role_of AAT:agent
```

#### Rule 3: Motivation Linkage
```
IF   contract P70_4_documents_sellers_procurator procurator
     AND contract P70_1_documents_seller seller
     AND Activity P14_carried_out_by procurator
THEN Activity P17_was_motivated_by seller
```

---

## Compatibility and Standards

### CIDOC-CRM Compliance

| Version | Compatible | Notes |
|---------|------------|-------|
| 7.1.1 | ✅ Yes | Full support |
| 7.0.x | ✅ Yes | Full support |
| 6.2.x | ✅ Yes | Full support |

### RDF/OWL Standards

| Standard | Version | Compliance |
|----------|---------|------------|
| RDF | 1.1 | Full |
| OWL | 2 | Full |
| RDFS | 1.1 | Full |
| JSON-LD | 1.1 | Full |

### Getty AAT Integration

- **Term Used**: agent (300025972)
- **Hierarchy**: Agents Facet > people > people by activity > agents
- **Broader Terms**: people by activity
- **Related Terms**: attorneys, proxies, representatives

---

## Quality Assurance

### Validation Queries

#### SPARQL: Find all seller procurators
```sparql
PREFIX gmn: <http://genizah.org/ontology/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?procurator ?seller
WHERE {
  ?contract gmn:P70_4_documents_sellers_procurator ?procurator .
  ?contract gmn:P70_1_documents_seller ?seller .
}
```

#### SPARQL: Verify transformation
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?activity ?procurator ?seller
WHERE {
  ?contract cidoc:P70_documents ?acquisition .
  ?acquisition cidoc:P9_consists_of ?activity .
  ?activity cidoc:P14_carried_out_by ?procurator .
  ?activity cidoc:P17_was_motivated_by ?seller .
}
```

### Consistency Checks

1. ✅ Every procurator activity has P14.1_in_the_role_of
2. ✅ Every procurator activity links to exactly one person via P14
3. ✅ P17_was_motivated_by only present when seller exists
4. ✅ Activity URIs are unique
5. ✅ Original shortcut property removed after transformation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-17 | Initial creation of property |

---

## References

1. CIDOC-CRM. (2021). *Definition of the CIDOC Conceptual Reference Model* (Version 7.1.1).
2. Getty Research Institute. *Art & Architecture Thesaurus Online*. http://www.getty.edu/research/tools/vocabularies/aat/
3. Goitein, S.D. *A Mediterranean Society* (multiple volumes)
4. RDF Working Group. (2014). *RDF 1.1 Concepts and Abstract Syntax*. W3C Recommendation.

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**Authors**: GMN Ontology Working Group
