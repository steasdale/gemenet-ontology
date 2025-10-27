# P70.6 Documents Seller's Guarantor - Ontology Documentation

Complete semantic documentation for the `gmn:P70_6_documents_sellers_guarantor` property.

---

## Table of Contents

1. [Property Definition](#property-definition)
2. [Semantic Relationships](#semantic-relationships)
3. [Transformation Specification](#transformation-specification)
4. [Usage Examples](#usage-examples)
5. [CIDOC-CRM Alignment](#cidoc-crm-alignment)
6. [Competency Questions](#competency-questions)
7. [Related Properties](#related-properties)

---

## Property Definition

### Basic Information

**URI:** `http://w3id.org/gmn/P70_6_documents_sellers_guarantor`

**Preferred Label:** "P70.6 documents seller's guarantor" (English)

**Property Type:** Object Property

**Status:** Active (since 2025-10-17)

### Formal Definition

Associates a sales contract document with a person who provides security (guarantee) for the seller's obligations in the transaction. A guarantor is a third party who promises to fulfill the seller's obligations if the seller defaults, thereby reducing risk for the buyer and other parties.

### Scope Note

This property captures the relationship between a sales contract and persons who serve as guarantors for the seller. In historical Mediterranean commerce, guarantors were commonly required to provide security for transactions, particularly when:
- The seller's creditworthiness was uncertain
- The transaction involved significant value
- The buyer required additional assurance
- Legal or customary practices mandated such security

The guarantor's role differs from other transaction participants:
- **Procurators** represent parties legally but don't assume financial liability
- **Brokers** facilitate transactions but remain neutral
- **Guarantors** accept conditional liability for the principal's obligations

### Domain and Range

**Domain:** `gmn:E31_2_Sales_Contract`
- Subclass of `cidoc:E31_Document`
- Documents that record transfer of ownership

**Range:** `cidoc:E21_Person`
- Includes historical persons identified in contracts
- May be referenced by URI or created as blank nodes

### Cardinality

- **Minimum:** 0 (not all contracts have seller's guarantors)
- **Maximum:** Unlimited (a seller may have multiple guarantors)

### Super-properties

**Direct super-property:** `cidoc:P70_documents`
- Inherits the basic document-event relationship
- Specialized for acquisition event structure

### Sub-properties

This property has no defined sub-properties, but could theoretically be specialized by:
- Type of guarantee (financial, performance, etc.)
- Degree of liability (full, partial, conditional)
- Geographic jurisdiction of guarantee

---

## Semantic Relationships

### Property Chain

The property represents this CIDOC-CRM relationship chain:

```
E31_Document 
  → P70_documents → E8_Acquisition
  → P9_consists_of → E7_Activity
  → P14_carried_out_by → E21_Person (guarantor)
  
E7_Activity
  → P17_was_motivated_by → E21_Person (seller)
  → P14.1_in_the_role_of → E55_Type (AAT: guarantor)
```

### Core Relationships

1. **Document to Acquisition:** E31 → P70 → E8
   - Links the contract to the documented acquisition event

2. **Acquisition to Activity:** E8 → P9 → E7
   - Decomposes acquisition into constituent activities
   - Guarantor participation is modeled as an activity

3. **Activity to Guarantor:** E7 → P14 → E21
   - Links activity to the person performing it
   - With role qualifier P14.1 → guarantor

4. **Activity to Seller:** E7 → P17 → E21
   - Links guarantor's activity to the seller
   - Expresses motivation/purpose relationship

### Inverse Relationships

While CIDOC-CRM defines inverse properties, GMN focuses on the forward relationships. The implicit inverses are:

- E8 `P70i_is_documented_in` E31
- E7 `P9i_forms_part_of` E8
- E21 `P14i_performed` E7
- E21 `P17i_motivated` E7

---

## Transformation Specification

### Input Structure (GMN)

Simplified property for data entry:

```turtle
@prefix gmn: <http://w3id.org/gmn/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

<contract_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <seller_001> ;
    gmn:P70_6_documents_sellers_guarantor <guarantor_001> .
```

### Output Structure (CIDOC-CRM)

Fully compliant CIDOC-CRM structure:

```turtle
<contract_001> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <contract_001/acquisition> .

<contract_001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <seller_001> ;
    cidoc:P9_consists_of <contract_001/activity/guarantor_abc123> .

<contract_001/activity/guarantor_abc123> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <guarantor_001> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300379835> ;
    cidoc:P17_was_motivated_by <seller_001> .

<guarantor_001> a cidoc:E21_Person .
<seller_001> a cidoc:E21_Person .
```

### Transformation Algorithm

**Step 1:** Extract guarantor references from input property

**Step 2:** Ensure E8_Acquisition node exists
- If missing, create with URI: `{contract_uri}/acquisition`

**Step 3:** Ensure P9_consists_of array exists in acquisition
- Initialize as empty array if missing

**Step 4:** For each guarantor:
- Create unique E7_Activity URI (hash-based)
- Set P14_carried_out_by to guarantor
- Set P14.1_in_the_role_of to AAT guarantor concept
- If seller exists, set P17_was_motivated_by to seller
- Append activity to P9_consists_of array

**Step 5:** Remove original GMN property from output

### URI Generation Pattern

Activity URIs follow the pattern:
```
{contract_uri}/activity/guarantor_{hash}
```

Where `{hash}` is the last 8 characters of `hash(guarantor_uri + property_name)`

This ensures:
- Uniqueness across multiple guarantors
- Reproducibility (same input → same URI)
- Readability in debugging

---

## Usage Examples

### Example 1: Single Guarantor

**Input (GMN):**
```json
{
  "@context": {
    "gmn": "http://w3id.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contract/1455_03_15",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": {
    "@id": "http://example.org/person/giovanni_rossi",
    "@type": "cidoc:E21_Person"
  },
  "gmn:P70_6_documents_sellers_guarantor": [{
    "@id": "http://example.org/person/marco_bianchi",
    "@type": "cidoc:E21_Person"
  }]
}
```

**Output (CIDOC-CRM):**
```json
{
  "@context": {
    "gmn": "http://w3id.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contract/1455_03_15",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contract/1455_03_15/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P23_transferred_title_from": [{
      "@id": "http://example.org/person/giovanni_rossi",
      "@type": "cidoc:E21_Person"
    }],
    "cidoc:P9_consists_of": [{
      "@id": "http://example.org/contract/1455_03_15/activity/guarantor_9a8b7c6d",
      "@type": "cidoc:E7_Activity",
      "cidoc:P14_carried_out_by": [{
        "@id": "http://example.org/person/marco_bianchi",
        "@type": "cidoc:E21_Person"
      }],
      "cidoc:P14.1_in_the_role_of": {
        "@id": "http://vocab.getty.edu/aat/300379835",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P17_was_motivated_by": {
        "@id": "http://example.org/person/giovanni_rossi",
        "@type": "cidoc:E21_Person"
      }
    }]
  }]
}
```

### Example 2: Multiple Guarantors

**Scenario:** Two brothers jointly guarantee their father's sale

```turtle
<contract_002> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <father> ;
    gmn:P70_6_documents_sellers_guarantor <son1>, <son2> .
```

**Transforms to:**

```turtle
<contract_002> cidoc:P70_documents <contract_002/acquisition> .

<contract_002/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <father> ;
    cidoc:P9_consists_of 
        <contract_002/activity/guarantor_aaa111>,
        <contract_002/activity/guarantor_bbb222> .

<contract_002/activity/guarantor_aaa111> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <son1> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300379835> ;
    cidoc:P17_was_motivated_by <father> .

<contract_002/activity/guarantor_bbb222> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <son2> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300379835> ;
    cidoc:P17_was_motivated_by <father> .
```

### Example 3: Guarantor Without Seller (Edge Case)

If seller is not yet defined when guarantor is processed:

```turtle
<contract_003> a gmn:E31_2_Sales_Contract ;
    gmn:P70_6_documents_sellers_guarantor <guarantor> .
```

**Transforms to:**

```turtle
<contract_003> cidoc:P70_documents <contract_003/acquisition> .

<contract_003/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P9_consists_of <contract_003/activity/guarantor_xyz789> .

<contract_003/activity/guarantor_xyz789> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <guarantor> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300379835> .
    # Note: P17_was_motivated_by is omitted when seller is unknown
```

---

## CIDOC-CRM Alignment

### Compliance with CIDOC-CRM 7.1.1

This property and its transformation adhere to CIDOC-CRM principles:

1. **Event-Centric Modeling:** Activities are modeled as E7_Activity instances
2. **Role Qualification:** P14.1 qualifies participation with controlled vocabulary
3. **Motivation Expression:** P17 links activities to their motivations
4. **Event Decomposition:** P9 allows complex events to be broken into parts

### Use of Standard Properties

| CIDOC Property | Usage in Transformation |
|---------------|------------------------|
| P70_documents | Links document to acquisition |
| P9_consists_of | Decomposes acquisition into activities |
| P14_carried_out_by | Links activity to person (guarantor) |
| P14.1_in_the_role_of | Qualifies role as guarantor |
| P17_was_motivated_by | Links guarantor to seller (principal) |
| P23_transferred_title_from | Identifies seller in acquisition |

### Getty AAT Integration

**Guarantor Concept:**
- URI: `http://vocab.getty.edu/aat/300379835`
- Preferred Label: "guarantors"
- Scope Note: "People or institutions that guarantee the performance of another, as in a pledge to answer for the payment of a debt or the fulfillment of a duty or promise by another person in the event of that person's default."

### Extension Beyond Core CIDOC-CRM

While CIDOC-CRM provides the base classes and properties, this implementation:
- Uses E7_Activity for guarantor participation (following procurement patterns)
- Applies P17_was_motivated_by to link guarantor to principal
- Uses AAT concepts for role qualification
- Creates intermediate activity nodes for semantic clarity

---

## Competency Questions

These questions test the semantic adequacy of the property:

### Basic Queries

**CQ1:** Who served as guarantors for seller Giovanni Rossi?

```sparql
PREFIX gmn: <http://w3id.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?guarantor WHERE {
  ?contract cidoc:P70_documents ?acquisition .
  ?acquisition cidoc:P23_transferred_title_from <http://example.org/person/giovanni_rossi> ;
               cidoc:P9_consists_of ?activity .
  ?activity cidoc:P14_carried_out_by ?guarantor ;
            cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300379835> ;
            cidoc:P17_was_motivated_by <http://example.org/person/giovanni_rossi> .
}
```

**CQ2:** Which contracts have seller's guarantors?

```sparql
SELECT DISTINCT ?contract WHERE {
  ?contract cidoc:P70_documents ?acquisition .
  ?acquisition cidoc:P9_consists_of ?activity .
  ?activity cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300379835> ;
            cidoc:P17_was_motivated_by ?seller .
  ?acquisition cidoc:P23_transferred_title_from ?seller .
}
```

### Advanced Queries

**CQ3:** Find all persons who served both as sellers and as guarantors (in different contracts)

```sparql
SELECT DISTINCT ?person WHERE {
  # Person as seller
  ?contract1 cidoc:P70_documents ?acq1 .
  ?acq1 cidoc:P23_transferred_title_from ?person .
  
  # Same person as guarantor
  ?contract2 cidoc:P70_documents ?acq2 .
  ?acq2 cidoc:P9_consists_of ?activity .
  ?activity cidoc:P14_carried_out_by ?person ;
            cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300379835> .
}
```

**CQ4:** Calculate average number of guarantors per seller

```sparql
SELECT (AVG(?count) AS ?avg_guarantors) WHERE {
  {
    SELECT ?seller (COUNT(?guarantor) AS ?count) WHERE {
      ?contract cidoc:P70_documents ?acquisition .
      ?acquisition cidoc:P23_transferred_title_from ?seller ;
                   cidoc:P9_consists_of ?activity .
      ?activity cidoc:P14_carried_out_by ?guarantor ;
                cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300379835> ;
                cidoc:P17_was_motivated_by ?seller .
    }
    GROUP BY ?seller
  }
}
```

---

## Related Properties

### Sibling Properties

| Property | Guarantees For | Motivated By Property |
|----------|---------------|----------------------|
| **P70.6** | **Seller** | **P23_transferred_title_from** |
| P70.7 | Buyer | P22_transferred_title_to |

### Procurator Properties (Comparison)

| Property | Role | Liability |
|----------|------|-----------|
| P70.4 | Seller's Procurator | Legal representation, no financial liability |
| **P70.6** | **Seller's Guarantor** | **Financial security, conditional liability** |

### Other Transaction Roles

- **P70.8** (Broker): Facilitates transaction, neutral party
- **P70.9** (Payment Provider for Buyer): Provides funds on buyer's behalf
- **P70.10** (Payment Recipient for Seller): Receives funds on seller's behalf

### Direct Person-Person Properties

GMN also defines direct relationships for simpler queries:

- `gmn:is_guaranteed_by` - Direct link from principal to guarantor
- Useful for Omeka-S annotations
- Complements the full CIDOC-CRM structure

---

## Validation Rules

### Required Conditions

1. **Type Constraint:** Domain must be `gmn:E31_2_Sales_Contract`
2. **Range Constraint:** Object must be `cidoc:E21_Person`
3. **Cardinality:** Zero or more values allowed

### Recommended Practices

1. **Define Seller First:** Transform seller (P70.1) before guarantor (P70.6)
2. **Use Consistent URIs:** Person URIs should be stable across properties
3. **Document Multiple Guarantors:** When multiple guarantors exist, all should be listed
4. **Role Clarity:** Distinguish guarantors from procurators in data entry

### Transformation Validation

After transformation, verify:
- Original GMN property is removed
- E8_Acquisition node exists
- Each guarantor has corresponding E7_Activity
- P14.1 points to correct AAT concept
- P17 links to seller when available

---

## Best Practices

### Data Entry

1. **Identify Guarantors Clearly:** Distinguish from witnesses or procurators
2. **Link to Seller:** Ensure seller is also documented
3. **Multiple Guarantors:** List all guarantors explicitly
4. **Note Relationships:** Document family or business relationships if evident

### Transformation

1. **Preserve Order:** Maintain guarantor order from input
2. **Handle Missing Sellers:** Gracefully omit P17 when seller unavailable
3. **Generate Stable URIs:** Use deterministic hash functions
4. **Validate Output:** Check structure conforms to CIDOC-CRM

### Querying

1. **Use Role Filtering:** Always filter by AAT guarantor concept
2. **Check Motivation:** Use P17 to distinguish seller's vs buyer's guarantors
3. **Join Carefully:** Activity nodes require intermediate joins
4. **Consider Performance:** Index key properties for large datasets

---

## Historical Context

### Role of Guarantors in Medieval Commerce

In the Mediterranean commercial world (13th-16th centuries):

1. **Credit and Risk:** Guarantors enabled transactions when credit was uncertain
2. **Social Networks:** Often drawn from family or business partnerships
3. **Legal Framework:** Recognized in civil law (ius commune) and local statutes
4. **Financial Instruments:** Part of evolving credit instruments (fideiussio, pledges)

### Documentary Evidence

Guarantors appear in notarial contracts with formulaic language:
- "...with Antonio as guarantor and principal payer..."
- "...Giovanni promises and binds himself as guarantor..."
- "...the said guarantor renounces the benefit of discussion and division..."

---

## Technical Notes

### UUID Generation

Activity URIs use hash-based generation:
```python
activity_hash = str(hash(guarantor_uri + property_name))[-8:]
activity_uri = f"{subject_uri}/activity/guarantor_{activity_hash}"
```

Benefits:
- Deterministic (reproducible)
- Unique per guarantor-property pair
- Human-readable component

### JSON-LD Context

Required context mappings:
```json
{
  "@context": {
    "gmn": "http://w3id.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "dcterms": "http://purl.org/dc/terms/"
  }
}
```

### RDF Serialization

Property appears differently in various RDF formats:

**Turtle:**
```turtle
gmn:P70_6_documents_sellers_guarantor <person_uri> .
```

**RDF/XML:**
```xml
<gmn:P70_6_documents_sellers_guarantor rdf:resource="person_uri" />
```

**JSON-LD:**
```json
"gmn:P70_6_documents_sellers_guarantor": [{"@id": "person_uri"}]
```

---

## References

1. CIDOC-CRM Version 7.1.1 (2021)
   - http://www.cidoc-crm.org/
   
2. Getty Art & Architecture Thesaurus (AAT)
   - http://vocab.getty.edu/aat/300379835 (guarantors)

3. Medieval Notarial Documentation Practices
   - Relevant for historical context

4. GMN Ontology Project Documentation
   - Internal project specifications

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-27  
**Authors:** GMN Ontology Development Team  
**Status:** Final
