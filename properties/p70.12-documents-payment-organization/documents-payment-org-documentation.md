# GMN Ontology: P70.12 Documents Payment Through Organization
## Ontology Documentation

Complete semantic documentation for the `gmn:P70_12_documents_payment_through_organization` property including class definitions, property specifications, and transformation examples.

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Semantic Definition](#semantic-definition)
3. [Domain and Range](#domain-and-range)
4. [CIDOC-CRM Alignment](#cidoc-crm-alignment)
5. [Transformation Specification](#transformation-specification)
6. [Usage Examples](#usage-examples)
7. [Design Rationale](#design-rationale)
8. [Relationship to Other Properties](#relationship-to-other-properties)

---

## Property Overview

### Basic Information

**URI:** `http://www.genoesemerchantnetworks.com/ontology#P70_12_documents_payment_through_organization`

**Label:** P70.12 documents payment through organization

**Property Type:** `owl:ObjectProperty`, `rdf:Property`

**Created:** 2025-10-17

**Status:** Active

### Purpose

This property associates a sales contract with an organization (typically a bank or financial institution) through which payment for the transaction is made or facilitated. It captures financial intermediaries that handle the payment mechanism without being principal parties to the transaction or individual agents.

### Key Characteristics

- **Simplified property** providing convenient data entry
- **Transforms** to full CIDOC-CRM structure
- **References** organizations in contract text
- **Distinguishes** financial institutions from individual agents and principals

---

## Semantic Definition

### Full Definition

The `gmn:P70_12_documents_payment_through_organization` property is a simplified property for associating a sales contract with an organization (typically a bank) through which payment for the transaction is made or facilitated. This captures financial institutions that serve as intermediaries in the payment process, such as banks holding deposits, making transfers, or providing credit facilities for the transaction.

### Scope Notes

**What This Property Captures:**
- Banks facilitating payment transfers
- Credit institutions providing transaction financing
- Deposit houses holding funds for the transaction
- Financial intermediaries managing payment mechanisms
- Organizations referenced in contract as payment facilitators

**What This Property Does NOT Capture:**
- Principal parties (buyer/seller) - use P70.1, P70.2
- Individual payment providers - use P70.9
- Individual payment recipients - use P70.10
- Individual guarantors - use P70.6, P70.7
- Individual procurators - use P70.4, P70.5
- Brokers - use P70.8

### Intended Use Cases

1. **Bank Transfer Documentation:**
   - Contract specifies payment through Banco di San Giorgio
   - Property captures the bank as payment intermediary

2. **Credit Facility References:**
   - Contract mentions credit institution financing purchase
   - Property documents the financial organization

3. **Deposit Management:**
   - Contract indicates funds held at financial house
   - Property records the deposit institution

4. **Multiple Payment Channels:**
   - Contract uses multiple financial intermediaries
   - Property can list all organizations involved

---

## Domain and Range

### Domain

**Class:** `gmn:E31_2_Sales_Contract`

**Definition:** A subclass of `cidoc:E31_Document` representing a sales contract or bill of sale documenting the transfer of ownership of property.

**Domain Constraints:**
- Property can only be applied to sales contract documents
- Not applicable to other document types (arbitration, correspondence, etc.)
- Multiple organizations can be associated with single contract

### Range

**Class:** `cidoc:E74_Group`

**Definition:** CIDOC-CRM class representing a group of people organized for specific purposes, including institutions, corporations, and organized entities.

**Range Constraints:**
- Organizations must be instances of E74_Group
- Includes: banks, credit houses, financial institutions
- Excludes: individual persons (E21_Person)

**Typical Range Instances:**
- Financial institutions (banks, credit houses)
- Merchant banks and banking families
- Deposit houses (casa di deposito)
- Credit cooperatives
- Transfer agencies

---

## CIDOC-CRM Alignment

### Superproperty

**Property:** `cidoc:P70_documents`

**Definition:** "This property describes the CRM Entities documented as instances of E31 Document. Documents are interpreted as describing facts, not opinions. Thus, this property allows connecting facts established in a document with instances of E2 Temporal Entity through P70 documents. This property links an instance of E31 Document to the E1 CRM Entity or entities that the document formally documents."

**Alignment:**
- P70.12 is a specialized form of documentation
- Follows CIDOC-CRM pattern for document-entity relationships
- Inherits P70 semantics of formal documentation

### See Also Properties

- **cidoc:P70_documents** - Parent property defining documentation relationship
- **cidoc:P14_carried_out_by** - Referenced in comment for ideal path
- **cidoc:P67_refers_to** - Used in current transformation

### Ontological Path

The property represents a simplified shortcut for the following CIDOC-CRM path:

```
E31_Document (Sales Contract)
  → P70_documents
    → E8_Acquisition (Sale Transaction)
      → P9_consists_of
        → E7_Activity (Payment Facilitation Activity)
          → P14_carried_out_by
            → E74_Group (Financial Institution)
```

**Current Implementation:**
For practical reasons, the current transformation uses:

```
E31_Document (Sales Contract)
  → P67_refers_to
    → E74_Group (Financial Institution)
```

This acknowledges that the organization is referenced in the contract text without modeling the full activity structure.

---

## Transformation Specification

### Input Format

The property accepts organizations in two formats:

**Format 1: URI Reference**
```json
{
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_12_documents_payment_through_organization": [
    "http://example.org/organization/banco_san_giorgio"
  ]
}
```

**Format 2: Inline Object**
```json
{
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_12_documents_payment_through_organization": [
    {
      "@id": "http://example.org/organization/banco_san_giorgio",
      "@type": "cidoc:E74_Group",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Banco di San Giorgio"
      }
    }
  ]
}
```

### Transformation Algorithm

**Step 1:** Check if property exists
```python
if 'gmn:P70_12_documents_payment_through_organization' not in data:
    return data
```

**Step 2:** Extract organizations list
```python
organizations = data['gmn:P70_12_documents_payment_through_organization']
```

**Step 3:** Initialize P67_refers_to if needed
```python
if 'cidoc:P67_refers_to' not in data:
    data['cidoc:P67_refers_to'] = []
```

**Step 4:** Process each organization
```python
for org_obj in organizations:
    if isinstance(org_obj, dict):
        org_data = org_obj.copy()
        if '@type' not in org_data:
            org_data['@type'] = 'cidoc:E74_Group'
    else:
        org_uri = str(org_obj)
        org_data = {
            '@id': org_uri,
            '@type': 'cidoc:E74_Group'
        }
    
    data['cidoc:P67_refers_to'].append(org_data)
```

**Step 5:** Remove original property
```python
del data['gmn:P70_12_documents_payment_through_organization']
```

### Output Format

**After Transformation (URI Reference):**
```json
{
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "http://example.org/organization/banco_san_giorgio",
      "@type": "cidoc:E74_Group"
    }
  ]
}
```

**After Transformation (Inline Object):**
```json
{
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "http://example.org/organization/banco_san_giorgio",
      "@type": "cidoc:E74_Group",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Banco di San Giorgio"
      }
    }
  ]
}
```

### Transformation Properties

- **Idempotent:** Running transformation multiple times produces same result
- **Preserves data:** All organization properties maintained
- **Type-safe:** E74_Group type always assigned
- **Append-only:** Adds to existing P67_refers_to list

---

## Usage Examples

### Example 1: Simple Bank Reference

**Turtle Input:**
```turtle
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

:contract_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_12_documents_payment_through_organization :banco_san_giorgio .

:banco_san_giorgio a cidoc:E74_Group ;
    cidoc:P1_is_identified_by [
        a cidoc:E41_Appellation ;
        cidoc:P190_has_symbolic_content "Banco di San Giorgio"
    ] .
```

**Turtle Output:**
```turtle
:contract_001 a gmn:E31_2_Sales_Contract ;
    cidoc:P67_refers_to :banco_san_giorgio .

:banco_san_giorgio a cidoc:E74_Group ;
    cidoc:P1_is_identified_by [
        a cidoc:E41_Appellation ;
        cidoc:P190_has_symbolic_content "Banco di San Giorgio"
    ] .
```

### Example 2: Multiple Financial Institutions

**JSON-LD Input:**
```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contract/002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_12_documents_payment_through_organization": [
    {
      "@id": "http://example.org/org/banco_san_giorgio",
      "@type": "cidoc:E74_Group",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Banco di San Giorgio"
      }
    },
    {
      "@id": "http://example.org/org/casa_credito_genova",
      "@type": "cidoc:E74_Group",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Casa di Credito di Genova"
      }
    }
  ]
}
```

**JSON-LD Output:**
```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contract/002",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "http://example.org/org/banco_san_giorgio",
      "@type": "cidoc:E74_Group",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Banco di San Giorgio"
      }
    },
    {
      "@id": "http://example.org/org/casa_credito_genova",
      "@type": "cidoc:E74_Group",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Casa di Credito di Genova"
      }
    }
  ]
}
```

### Example 3: Complete Sales Contract Context

**Turtle Input:**
```turtle
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix aat: <http://vocab.getty.edu/aat/> .

:contract_003 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller :giovanni_doria ;
    gmn:P70_2_documents_buyer :pietro_spinola ;
    gmn:P70_3_documents_transfer_of :house_in_genoa ;
    gmn:P70_9_documents_payment_provider_for_buyer :luca_spinola ;
    gmn:P70_12_documents_payment_through_organization :banco_san_giorgio ;
    gmn:P70_16_documents_sale_price_amount "5000"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency aat:300037222 .

:giovanni_doria a cidoc:E21_Person .
:pietro_spinola a cidoc:E21_Person .
:luca_spinola a cidoc:E21_Person .
:house_in_genoa a gmn:E22_1_Building .
:banco_san_giorgio a cidoc:E74_Group .
```

**Interpretation:**
This contract documents:
- Giovanni Doria selling a house to Pietro Spinola
- Pietro's relative Luca providing the purchase funds
- Payment facilitated through Banco di San Giorgio
- Sale price of 5000 (currency units)

The bank (P70.12) is the payment mechanism, while Luca (P70.9) is the actual funding source.

### Example 4: Bank with Location and Type

**JSON-LD:**
```json
{
  "@id": "http://example.org/contract/004",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_12_documents_payment_through_organization": [
    {
      "@id": "http://example.org/org/banco_san_giorgio",
      "@type": "cidoc:E74_Group",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Banco di San Giorgio"
      },
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300026816",
        "@type": "cidoc:E55_Type",
        "rdfs:label": "banks (institutions)"
      },
      "cidoc:P74_has_current_or_former_residence": {
        "@id": "http://example.org/place/genoa",
        "@type": "cidoc:E53_Place",
        "cidoc:P87_is_identified_by": {
          "@type": "cidoc:E44_Place_Appellation",
          "cidoc:P190_has_symbolic_content": "Genoa"
        }
      }
    }
  ]
}
```

---

## Design Rationale

### Why P67_refers_to Instead of P9_consists_of?

**Decision:** Use `cidoc:P67_refers_to` for the transformation target rather than creating full activity structure with `P9_consists_of`.

**Rationale:**

1. **Textual Reference Pattern:**
   - Organizations are mentioned in contract text
   - They don't actively participate in documented transaction
   - Contract references them as payment mechanisms
   - Similar to referenced persons (P70.11) and places (P70.13)

2. **Participation vs. Reference:**
   - P14_carried_out_by implies active participation in event
   - P67_refers_to indicates textual presence without participation claim
   - Banks facilitate payment but aren't transaction parties
   - Distinction matters for accurate event modeling

3. **Practical Considerations:**
   - Simpler transformation maintains data quality
   - Easier to query and process
   - Consistent with other reference properties
   - Avoids complex activity node creation

4. **Semantic Accuracy:**
   - Organization is **mentioned** in contract
   - Organization provides **mechanism** for payment
   - Organization doesn't **execute** the acquisition
   - P67 captures this relationship accurately

### Why E74_Group Instead of E39_Actor?

**Decision:** Use specific `cidoc:E74_Group` class rather than more general `cidoc:E39_Actor`.

**Rationale:**

1. **Semantic Precision:**
   - E74_Group specifically represents organizations
   - More precise than general E39_Actor
   - Enables organization-specific queries
   - Clarifies distinction from individual persons

2. **Data Quality:**
   - Type checking can catch person/organization confusion
   - Explicit organization typing improves data consistency
   - Supports validation and quality control

3. **Interoperability:**
   - Other systems expect E74_Group for organizations
   - Standard CIDOC-CRM practice
   - Better alignment with museum/archival practice

### Why Subproperty of P70_documents?

**Decision:** Make P70.12 a subproperty of `cidoc:P70_documents` rather than P67_refers_to.

**Rationale:**

1. **Semantic Alignment:**
   - P70 indicates formal documentation relationship
   - Contract formally documents payment mechanism
   - Maintains consistency with other P70.x properties
   - Groups all transaction documentation properties

2. **Property Hierarchy:**
   - All GMN P70.x properties share P70 parent
   - Enables reasoning about documentation relationships
   - Supports queries across all documented entities

3. **Transformation Flexibility:**
   - Subproperty relationship independent of transformation target
   - Allows future transformation changes without affecting ontology
   - Separates logical property from implementation details

---

## Relationship to Other Properties

### Related GMN Properties

#### P70.9 documents payment provider for buyer
- **Relationship:** Complementary
- **Distinction:** P70.9 captures **individual persons** who provide funds; P70.12 captures **organizations** facilitating payment mechanism
- **Can co-exist:** Yes - contract can specify both funding source (person) and payment channel (bank)

**Example:**
```turtle
:contract a gmn:E31_2_Sales_Contract ;
    gmn:P70_9_documents_payment_provider_for_buyer :luca_spinola ;
    gmn:P70_12_documents_payment_through_organization :banco_san_giorgio .
```
Interpretation: Luca provides the funds, bank handles the transfer.

#### P70.10 documents payment recipient for seller
- **Relationship:** Complementary
- **Distinction:** P70.10 captures **individual persons** receiving funds; P70.12 captures **organizations** facilitating payment mechanism
- **Can co-exist:** Yes - contract can specify both recipient (person) and payment channel (bank)

**Example:**
```turtle
:contract a gmn:E31_2_Sales_Contract ;
    gmn:P70_10_documents_payment_recipient_for_seller :marco_grimaldi ;
    gmn:P70_12_documents_payment_through_organization :banco_san_giorgio .
```
Interpretation: Marco receives the payment, bank handles the transfer.

#### P70.11 documents referenced person
- **Relationship:** Parallel pattern
- **Distinction:** P70.11 for persons (E21_Person); P70.12 for organizations (E74_Group)
- **Transformation:** Both use P67_refers_to
- **Design:** Same reference semantics, different entity types

**Common Pattern:**
```
P70.11: E31_Document → P67_refers_to → E21_Person
P70.12: E31_Document → P67_refers_to → E74_Group
```

#### P70.13 documents referenced place
- **Relationship:** Parallel pattern
- **Distinction:** P70.13 for places (E53_Place); P70.12 for organizations (E74_Group)
- **Transformation:** Both use P67_refers_to
- **Design:** Same reference semantics, different entity types

**Common Pattern:**
```
P70.12: E31_Document → P67_refers_to → E74_Group
P70.13: E31_Document → P67_refers_to → E53_Place
```

#### P70.4 documents seller's procurator
#### P70.5 documents buyer's procurator
- **Relationship:** Distinct roles
- **Distinction:** Procurators are legal representatives (persons); payment organizations are financial facilitators (organizations)
- **Participation:** Procurators participate in transaction; organizations provide mechanism
- **Transformation:** Procurators create activity nodes; organizations use P67_refers_to

#### P70.6 documents seller's guarantor
#### P70.7 documents buyer's guarantor
- **Relationship:** Distinct roles
- **Distinction:** Guarantors provide security (persons); payment organizations provide mechanism (organizations)
- **Function:** Guarantors assume risk; organizations facilitate transfer
- **Transformation:** Guarantors create activity nodes; organizations use P67_refers_to

#### P70.8 documents broker
- **Relationship:** Distinct roles
- **Distinction:** Brokers facilitate transaction (persons); payment organizations facilitate payment (organizations)
- **Scope:** Brokers arrange entire sale; organizations handle payment aspect
- **Transformation:** Both create activity nodes (broker is active participant)

### Related CIDOC-CRM Properties

#### P14_carried_out_by
- **Relationship:** Mentioned in rdfs:seeAlso
- **Usage:** Would be used in full activity structure
- **Current:** Not used in current transformation
- **Future:** Could be adopted if modeling payment activities

#### P67_refers_to
- **Relationship:** Used in transformation
- **Semantics:** "This property documents that an E89 Propositional Object makes a statement about an E1 CRM Entity"
- **Application:** Contract references organization without claiming participation

#### P70_documents
- **Relationship:** Parent property
- **Inheritance:** P70.12 inherits P70 semantics
- **Semantics:** "This property describes the CRM Entities documented as instances of E31 Document"

---

## Validation Rules

### Required Constraints

1. **Domain Constraint:**
   - Subject must be instance of `gmn:E31_2_Sales_Contract`
   - Validation: `?contract rdf:type/rdfs:subClassOf* gmn:E31_2_Sales_Contract`

2. **Range Constraint:**
   - Object must be instance of `cidoc:E74_Group`
   - Validation: `?organization rdf:type/rdfs:subClassOf* cidoc:E74_Group`

3. **Type Safety:**
   - Cannot use with E21_Person instances (use P70.9 or P70.10 instead)
   - Cannot use with E53_Place instances (use P70.13 instead)

### Recommended Practices

1. **Organization Identification:**
   - Organizations should have E41_Appellation with name
   - Organizations should have P2_has_type with institution type (AAT)
   - Organizations should have location data when available

2. **Cardinality:**
   - Zero or more organizations per contract
   - Multiple organizations should be distinct entities
   - Avoid duplicate references to same organization

3. **Disambiguation:**
   - Use URIs for well-known institutions
   - Include location for disambiguation (multiple banks with same name)
   - Add temporal existence information when relevant

---

## SPARQL Query Examples

### Query 1: Find all contracts with payment organizations

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?organization ?name
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P67_refers_to ?organization .
  ?organization a cidoc:E74_Group ;
                cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
}
```

### Query 2: Count contracts by payment organization

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?organization ?name (COUNT(?contract) AS ?contract_count)
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P67_refers_to ?organization .
  ?organization a cidoc:E74_Group ;
                cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
}
GROUP BY ?organization ?name
ORDER BY DESC(?contract_count)
```

### Query 3: Find contracts with both payment provider and organization

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?provider ?organization
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition .
  
  ?acquisition a cidoc:E8_Acquisition ;
               cidoc:P9_consists_of ?provider_activity .
  
  ?provider_activity cidoc:P14_carried_out_by ?provider .
  ?provider a cidoc:E21_Person .
  
  ?contract cidoc:P67_refers_to ?organization .
  ?organization a cidoc:E74_Group .
}
```

---

## Future Enhancements

### Potential Improvements

1. **Activity Modeling:**
   - Future version could create E7_Activity nodes for payment facilitation
   - Would use P14_carried_out_by to link organizations
   - Would provide richer event structure
   - Would enable temporal and spatial data about payment activity

2. **Role Typing:**
   - Add P14.1_in_the_role_of to specify organization function
   - Distinguish deposit holders, transfer agents, credit providers
   - Enable more precise queries about payment mechanisms

3. **Temporal Information:**
   - Link organizations to time periods of activity
   - Capture duration of payment facilitation
   - Enable historical analysis of banking practices

4. **Network Analysis:**
   - Link organizations to their agents and representatives
   - Capture relationships between financial institutions
   - Enable social network analysis of financial systems

---

*Documentation Version 1.0 - Created 2025-10-27*
