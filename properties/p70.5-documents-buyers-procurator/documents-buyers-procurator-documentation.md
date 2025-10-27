# Ontology Documentation: P70.5 Documents Buyer's Procurator
## Complete Semantic Specification for gmn:P70_5_documents_buyers_procurator

---

## Property Overview

### Identification

| Attribute | Value |
|-----------|-------|
| **URI** | `gmn:P70_5_documents_buyers_procurator` |
| **Label** | "P70.5 documents buyer's procurator"@en |
| **Property Type** | `owl:ObjectProperty`, `rdf:Property` |
| **Created** | 2025-10-17 |
| **Version** | 1.0 |

### Classification

| Attribute | Value |
|-----------|-------|
| **Superproperty** | `cidoc:P70_documents` |
| **Domain** | `gmn:E31_2_Sales_Contract` |
| **Range** | `cidoc:E21_Person` |
| **Inverse** | Not defined (unidirectional simplification) |

### Related Properties

- `cidoc:P70_documents` - Superproperty
- `cidoc:P14_carried_out_by` - Used in transformation target
- `cidoc:P17_was_motivated_by` - Used to link procurator to buyer
- `gmn:P70_2_documents_buyer` - Documents the principal party
- `gmn:P70_4_documents_sellers_procurator` - Parallel property for seller's representative

---

## Semantic Definition

### Purpose

The `gmn:P70_5_documents_buyers_procurator` property provides a simplified method for data entry systems to directly associate a sales contract (E31_Document subclass) with the person who served as procurator (legal representative) for the buyer. This property is designed as a convenient shorthand that represents a more complex CIDOC-CRM structure involving intermediate entities and relationships.

### Conceptual Model

A procurator is a person who:
1. **Holds legal authority** to act on behalf of the buyer
2. **Makes binding decisions** in the transaction
3. **Represents the buyer's interests** before the notary
4. **Executes legal instruments** with the same force as if the principal were present

The property captures this essential relationship: "This contract documents [person] as the procurator for the buyer."

### CIDOC-CRM Semantics

While the simplified property directly connects contract and procurator, the full CIDOC-CRM semantics require modeling:

1. **The Acquisition Event** (E8_Acquisition) documented by the contract
2. **The Activity** (E7_Activity) of the procurator's participation within the acquisition
3. **The Carrying Out** (P14_carried_out_by) relationship between activity and procurator
4. **The Role Specification** (P14.1_in_the_role_of) qualifying the participation as agent
5. **The Motivation** (P17_was_motivated_by) linking the procurator's activity to the buyer they represent

---

## Formal Definition

### RDF/TTL Representation

```turtle
@prefix gmn: <https://w3id.org/genoa-maritime-notarial/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

gmn:P70_5_documents_buyers_procurator
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.5 documents buyer's procurator"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the procurator (legal representative) for the buyer. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (procurator), with P17_was_motivated_by linking to the buyer (E21_Person). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The transformation creates an E7_Activity node that explicitly links the procurator to the buyer they represent via P17_was_motivated_by."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P17_was_motivated_by .
```

### Property Characteristics

#### Functional Properties
- **Not Functional:** A contract may document multiple procurators for the buyer (e.g., joint representation)
- **Not Inverse Functional:** A person may serve as procurator for different buyers in different contracts

#### Transitivity
- **Not Transitive:** The procurator relationship does not chain (a procurator cannot appoint a sub-procurator without explicit authorization)

#### Symmetry
- **Not Symmetric:** Directional relationship from contract to person

---

## Transformation Specification

### Transformation Algorithm

The property undergoes automated transformation to full CIDOC-CRM structure:

#### Input Structure (Simplified)

```json
{
  "@id": "contract_uri",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_5_documents_buyers_procurator": [
    {
      "@id": "procurator_uri",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

#### Output Structure (CIDOC-CRM Compliant)

```json
{
  "@id": "contract_uri",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "contract_uri/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P9_consists_of": [{
      "@id": "contract_uri/activity/procurator_{hash}",
      "@type": "cidoc:E7_Activity",
      "cidoc:P14_carried_out_by": [{
        "@id": "procurator_uri",
        "@type": "cidoc:E21_Person"
      }],
      "cidoc:P14.1_in_the_role_of": {
        "@id": "http://vocab.getty.edu/aat/300411835",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P17_was_motivated_by": {
        "@id": "buyer_uri",
        "@type": "cidoc:E21_Person"
      }
    }]
  }]
}
```

### Transformation Steps

1. **Locate or Create E8_Acquisition**
   - Check if `cidoc:P70_documents` exists
   - If not, create acquisition with URI: `{contract_uri}/acquisition`

2. **Initialize P9_consists_of**
   - Ensure acquisition has `cidoc:P9_consists_of` array
   - This will hold activity instances

3. **Identify Buyer**
   - Extract buyer URI from `cidoc:P22_transferred_title_to` in acquisition
   - Used for P17_was_motivated_by linkage

4. **Process Each Procurator**
   - For each procurator in the input array:
     - Generate unique activity URI using hash
     - Create E7_Activity instance
     - Add P14_carried_out_by relationship
     - Add P14.1_in_the_role_of qualification (AAT agent)
     - Add P17_was_motivated_by relationship to buyer

5. **Remove Simplified Property**
   - Delete `gmn:P70_5_documents_buyers_procurator` from data
   - Ensures clean CIDOC-CRM output

### URI Generation

Activity URIs follow the pattern:
```
{contract_uri}/activity/procurator_{hash}
```

Where `{hash}` is the last 8 characters of the hash of: `procurator_uri + property_name`

This ensures:
- **Uniqueness** per procurator and property combination
- **Deterministic** URIs for the same inputs
- **Collision resistance** through hash function

---

## Domain and Range Constraints

### Domain: gmn:E31_2_Sales_Contract

The property can only be applied to sales contracts. This restriction ensures:

1. **Semantic Coherence:** Procurators are specifically relevant to acquisitions
2. **Type Safety:** Prevents application to irrelevant document types
3. **Clear Transformation:** Acquisition structure is appropriate for sales

**Valid Domain Instance:**
```turtle
:contract_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_5_documents_buyers_procurator :person_procurator .
```

**Invalid Domain Instance:**
```turtle
:letter_001 a gmn:E31_3_Correspondence ;
    gmn:P70_5_documents_buyers_procurator :person_procurator .  # INVALID
```

### Range: cidoc:E21_Person

The property can only point to persons (individuals, not organizations). This restriction ensures:

1. **Legal Reality:** Procurators are individual persons, not corporations
2. **CIDOC-CRM Compliance:** E21_Person is the appropriate class
3. **Clear Semantics:** Person-specific properties and relationships apply

**Valid Range Instance:**
```turtle
:procurator_001 a cidoc:E21_Person ;
    rdfs:label "Oberto Spinola" .
```

**Invalid Range Instance:**
```turtle
:bank_001 a cidoc:E74_Group ;
    rdfs:label "Bank of St. George" .

:contract_001 gmn:P70_5_documents_buyers_procurator :bank_001 .  # INVALID
```

---

## Usage Guidelines

### When to Use This Property

Use `gmn:P70_5_documents_buyers_procurator` when:

1. **Legal Representative Present:** The contract explicitly names someone acting for the buyer
2. **Power of Attorney:** The procurator holds legal authority (documented or implicit)
3. **Binding Capacity:** The procurator can make decisions binding on the buyer
4. **Historical Context:** Medieval/early modern legal documents use terms like *procurator*, *procuratore*, *actore in rem*

### When NOT to Use This Property

Do NOT use this property for:

1. **Guarantors:** Use `gmn:P70_7_documents_buyers_guarantor` for security providers
2. **Payment Providers:** Use `gmn:P70_9_documents_payment_provider_for_buyer` for financial backers
3. **Brokers:** Use `gmn:P70_8_documents_broker` for transaction facilitators
4. **Witnesses:** Use `gmn:P70_15_documents_witness` for attesters
5. **Organizations:** Use different properties for corporate entities

### Disambiguation: Similar Roles

| Role | Property | Key Distinction |
|------|----------|-----------------|
| **Procurator** | P70.5 | Legal representative with binding authority |
| **Buyer** | P70.2 | Principal party receiving title |
| **Guarantor** | P70.7 | Security provider, not decision-maker |
| **Payment Provider** | P70.9 | Financial supporter, not legal representative |
| **Broker** | P70.8 | Facilitator for both parties, not representative |

---

## Historical and Cultural Context

### Medieval Legal Practice

In medieval Genoa and other Mediterranean commercial centers, the institution of *procura* (power of attorney) was fundamental to commercial operations. Procurators enabled:

1. **Long-Distance Commerce:** Merchants at sea appointed agents ashore
2. **Family Management:** Members managed property for absent relatives
3. **Business Operations:** Companies employed professional representatives
4. **Legal Proceedings:** Parties designated representatives for court matters

### Documentary Evidence

Notarial contracts typically included phrases such as:

**Latin:**
- "nomine et vice [buyer's name]" (in the name and place of)
- "procurator constitutus" (appointed procurator)
- "actore in rem" (agent in the matter)

**Italian:**
- "procuratore di [buyer's name]" (procurator of)
- "in nome e per conto di" (in the name and on account of)

### Legal Authority

Procuratorial authority could be:

1. **General:** Broad powers across all matters (*procura generale*)
2. **Special:** Limited to specific transactions (*procura speciale*)
3. **Documented:** Established by separate procuration instrument
4. **Implicit:** Recognized by customary law (e.g., family relationships)

---

## Examples

### Example 1: Simple Procurator Assignment

**Scenario:** Giovanni de Marini purchases a house, but his brother Oberto acts as procurator.

**Input (GMN Simplified):**
```json
{
  "@context": {
    "gmn": "https://w3id.org/genoa-maritime-notarial/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "https://example.org/contract/1234",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P1_1_has_name": "Contract of Sale - House in Soziglia",
  "gmn:P70_1_documents_seller": [{
    "@id": "https://example.org/person/seller_001",
    "gmn:P1_1_has_name": "Lanfranco Pignolo"
  }],
  "gmn:P70_2_documents_buyer": [{
    "@id": "https://example.org/person/buyer_001",
    "gmn:P1_1_has_name": "Giovanni de Marini"
  }],
  "gmn:P70_5_documents_buyers_procurator": [{
    "@id": "https://example.org/person/procurator_001",
    "gmn:P1_1_has_name": "Oberto de Marini"
  }],
  "gmn:P70_3_documents_transfer_of": [{
    "@id": "https://example.org/property/house_001",
    "@type": "gmn:E22_1_Building",
    "gmn:P1_1_has_name": "House in Soziglia"
  }]
}
```

**Output (CIDOC-CRM Compliant):**
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "https://w3id.org/genoa-maritime-notarial/ontology#"
  },
  "@id": "https://example.org/contract/1234",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "https://example.org/contract/1234/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P23_transferred_title_from": [{
      "@id": "https://example.org/person/seller_001",
      "@type": "cidoc:E21_Person"
    }],
    "cidoc:P22_transferred_title_to": [{
      "@id": "https://example.org/person/buyer_001",
      "@type": "cidoc:E21_Person"
    }],
    "cidoc:P24_transferred_title_of": [{
      "@id": "https://example.org/property/house_001",
      "@type": "gmn:E22_1_Building"
    }],
    "cidoc:P9_consists_of": [{
      "@id": "https://example.org/contract/1234/activity/procurator_a1b2c3d4",
      "@type": "cidoc:E7_Activity",
      "cidoc:P14_carried_out_by": [{
        "@id": "https://example.org/person/procurator_001",
        "@type": "cidoc:E21_Person"
      }],
      "cidoc:P14.1_in_the_role_of": {
        "@id": "http://vocab.getty.edu/aat/300411835",
        "@type": "cidoc:E55_Type",
        "rdfs:label": "agents (people)"
      },
      "cidoc:P17_was_motivated_by": {
        "@id": "https://example.org/person/buyer_001",
        "@type": "cidoc:E21_Person"
      }
    }]
  }]
}
```

### Example 2: Multiple Procurators

**Scenario:** A buyer uses two joint procurators for a major transaction.

**Input:**
```json
{
  "@id": "https://example.org/contract/5678",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [{
    "@id": "https://example.org/person/buyer_002",
    "gmn:P1_1_has_name": "Ansaldo Spinola"
  }],
  "gmn:P70_5_documents_buyers_procurator": [
    {
      "@id": "https://example.org/person/procurator_002",
      "gmn:P1_1_has_name": "Filippo Doria"
    },
    {
      "@id": "https://example.org/person/procurator_003",
      "gmn:P1_1_has_name": "Nicolò Cattaneo"
    }
  ]
}
```

**Output:**
```json
{
  "@id": "https://example.org/contract/5678",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "https://example.org/contract/5678/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P22_transferred_title_to": [{
      "@id": "https://example.org/person/buyer_002",
      "@type": "cidoc:E21_Person"
    }],
    "cidoc:P9_consists_of": [
      {
        "@id": "https://example.org/contract/5678/activity/procurator_e5f6g7h8",
        "@type": "cidoc:E7_Activity",
        "cidoc:P14_carried_out_by": [{
          "@id": "https://example.org/person/procurator_002",
          "@type": "cidoc:E21_Person"
        }],
        "cidoc:P14.1_in_the_role_of": {
          "@id": "http://vocab.getty.edu/aat/300411835",
          "@type": "cidoc:E55_Type"
        },
        "cidoc:P17_was_motivated_by": {
          "@id": "https://example.org/person/buyer_002",
          "@type": "cidoc:E21_Person"
        }
      },
      {
        "@id": "https://example.org/contract/5678/activity/procurator_i9j0k1l2",
        "@type": "cidoc:E7_Activity",
        "cidoc:P14_carried_out_by": [{
          "@id": "https://example.org/person/procurator_003",
          "@type": "cidoc:E21_Person"
        }],
        "cidoc:P14.1_in_the_role_of": {
          "@id": "http://vocab.getty.edu/aat/300411835",
          "@type": "cidoc:E55_Type"
        },
        "cidoc:P17_was_motivated_by": {
          "@id": "https://example.org/person/buyer_002",
          "@type": "cidoc:E21_Person"
        }
      }
    ]
  }]
}
```

### Example 3: Procurator with Rich Person Data

**Scenario:** Full person data for the procurator is provided.

**Input:**
```json
{
  "@id": "https://example.org/contract/9012",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [{
    "@id": "https://example.org/person/buyer_003",
    "gmn:P1_1_has_name": "Percivalle Doria",
    "gmn:P1_3_has_patrilineal_name": "Doria"
  }],
  "gmn:P70_5_documents_buyers_procurator": [{
    "@id": "https://example.org/person/procurator_004",
    "@type": "cidoc:E21_Person",
    "gmn:P1_1_has_name": "Simone Vento",
    "gmn:P1_3_has_patrilineal_name": "Vento",
    "gmn:P1_4_has_loconym": "de Rapallo",
    "gmn:P11i_3_has_spouse": [{
      "@id": "https://example.org/person/spouse_001",
      "gmn:P1_1_has_name": "Margherita"
    }]
  }]
}
```

**Output:** The rich person data is preserved in the transformation.

```json
{
  "cidoc:P9_consists_of": [{
    "@id": "https://example.org/contract/9012/activity/procurator_m3n4o5p6",
    "@type": "cidoc:E7_Activity",
    "cidoc:P14_carried_out_by": [{
      "@id": "https://example.org/person/procurator_004",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": [
        {
          "@type": "cidoc:E41_Appellation",
          "cidoc:P190_has_symbolic_content": "Simone Vento"
        },
        {
          "@type": "gmn:E41_1_Patrilineal_Name",
          "cidoc:P190_has_symbolic_content": "Vento"
        },
        {
          "@type": "gmn:E41_2_Loconym",
          "cidoc:P190_has_symbolic_content": "de Rapallo"
        }
      ],
      "cidoc:P11i_participated_in": [{
        "@type": "gmn:E67_1_Marriage",
        "cidoc:P11_had_participant": [{
          "@id": "https://example.org/person/spouse_001",
          "@type": "cidoc:E21_Person"
        }]
      }]
    }],
    "cidoc:P14.1_in_the_role_of": {
      "@id": "http://vocab.getty.edu/aat/300411835",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P17_was_motivated_by": {
      "@id": "https://example.org/person/buyer_003",
      "@type": "cidoc:E21_Person"
    }
  }]
}
```

---

## SPARQL Query Patterns

### Query 1: Find All Procurators for a Specific Buyer

```sparql
PREFIX gmn: <https://w3id.org/genoa-maritime-notarial/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?procurator ?procuratorName
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition .
  
  ?acquisition cidoc:P22_transferred_title_to <https://example.org/person/buyer_001> ;
               cidoc:P9_consists_of ?activity .
  
  ?activity cidoc:P14_carried_out_by ?procurator ;
            cidoc:P17_was_motivated_by <https://example.org/person/buyer_001> .
  
  OPTIONAL {
    ?procurator cidoc:P1_is_identified_by ?name .
    ?name cidoc:P190_has_symbolic_content ?procuratorName .
  }
}
```

### Query 2: Count Contracts Using Procurators

```sparql
PREFIX gmn: <https://w3id.org/genoa-maritime-notarial/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT (COUNT(DISTINCT ?contract) AS ?contractCount)
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition .
  
  ?acquisition cidoc:P9_consists_of ?activity .
  
  ?activity cidoc:P14_carried_out_by ?procurator ;
            cidoc:P17_was_motivated_by ?buyer ;
            cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300411835> .
}
```

### Query 3: Find People Who Served as Both Buyer and Procurator

```sparql
PREFIX gmn: <https://w3id.org/genoa-maritime-notarial/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT DISTINCT ?person ?name
WHERE {
  # Person as buyer
  ?contract1 cidoc:P70_documents ?acq1 .
  ?acq1 cidoc:P22_transferred_title_to ?person .
  
  # Same person as procurator
  ?contract2 cidoc:P70_documents ?acq2 .
  ?acq2 cidoc:P9_consists_of ?activity .
  ?activity cidoc:P14_carried_out_by ?person .
  
  # Get name
  OPTIONAL {
    ?person cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
  }
}
```

### Query 4: Analyze Procurator Networks

```sparql
PREFIX gmn: <https://w3id.org/genoa-maritime-notarial/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?procurator ?buyer (COUNT(?contract) AS ?timesRepresented)
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition .
  
  ?acquisition cidoc:P22_transferred_title_to ?buyer ;
               cidoc:P9_consists_of ?activity .
  
  ?activity cidoc:P14_carried_out_by ?procurator ;
            cidoc:P17_was_motivated_by ?buyer .
}
GROUP BY ?procurator ?buyer
HAVING (?timesRepresented > 1)
ORDER BY DESC(?timesRepresented)
```

---

## Validation Rules

### Data Entry Validation

1. **Required Relationship:** If P70.5 is used, P70.2 (buyer) should also be present
2. **Type Consistency:** Procurator must be E21_Person
3. **No Self-Reference:** Procurator should not be same as buyer (though technically legal)
4. **No Organization:** Procurator cannot be E74_Group or other collective entity

### Transformation Validation

1. **Activity Creation:** Each procurator must generate exactly one E7_Activity
2. **URI Uniqueness:** Activity URIs must be unique within the contract
3. **Role Specification:** P14.1_in_the_role_of must reference AAT agent type
4. **Buyer Linkage:** If buyer exists in acquisition, P17_was_motivated_by must link to it
5. **Property Removal:** Original gmn:P70_5 property must not appear in output

---

## References and Standards

### CIDOC-CRM Classes Used

- **E31_Document** - Document class (contract domain)
- **E8_Acquisition** - Transfer of ownership event
- **E7_Activity** - Procurator's participation
- **E21_Person** - Person entity (procurator and buyer)
- **E55_Type** - Classification type (role specification)

### CIDOC-CRM Properties Used

- **P70_documents** - Links document to acquisition
- **P9_consists_of** - Links acquisition to constituent activities
- **P14_carried_out_by** - Links activity to agent
- **P14.1_in_the_role_of** - Qualifies the agent's role
- **P17_was_motivated_by** - Links activity to motivating entity
- **P22_transferred_title_to** - Links acquisition to buyer

### AAT Vocabulary

- **300411835** - agents (people in legal context)
  - Scope note: "People who conduct negotiations on behalf of a party"
  - URI: http://vocab.getty.edu/aat/300411835

### Related Standards

- **RDF 1.1** - Resource Description Framework
- **OWL 2** - Web Ontology Language
- **Dublin Core Terms** - Metadata vocabulary (dcterms:created)
- **JSON-LD 1.1** - JSON-based RDF serialization

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-17 | Initial property creation |

---

## See Also

- **gmn:P70_2_documents_buyer** - Principal party documentation
- **gmn:P70_4_documents_sellers_procurator** - Seller's procurator (parallel property)
- **gmn:P70_7_documents_buyers_guarantor** - Buyer's guarantor (different role)
- **gmn:P70_9_documents_payment_provider_for_buyer** - Buyer's payment provider
- **cidoc:P70_documents** - Superproperty documentation
- **CIDOC-CRM E7_Activity** - Activity class specification

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-27  
**Author:** GMN Ontology Team  
**Status:** Active
