# Ontology Documentation: P70.9 Documents Payment Provider for Buyer

This document provides complete semantic documentation for the `gmn:P70_9_documents_payment_provider_for_buyer` property, including its definition, CIDOC-CRM mapping, transformation patterns, and usage examples.

---

## Table of Contents

1. [Property Definition](#property-definition)
2. [Semantic Structure](#semantic-structure)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Transformation Pattern](#transformation-pattern)
5. [Vocabulary References](#vocabulary-references)
6. [Usage Examples](#usage-examples)
7. [Comparison with Related Properties](#comparison-with-related-properties)
8. [Implementation Notes](#implementation-notes)

---

## Property Definition

### Basic Information

| Attribute | Value |
|-----------|-------|
| **URI** | `gmn:P70_9_documents_payment_provider_for_buyer` |
| **Label** | "P70.9 documents payment provider for buyer"@en |
| **Type** | `owl:ObjectProperty`, `rdf:Property` |
| **Domain** | `gmn:E31_2_Sales_Contract` |
| **Range** | `cidoc:E21_Person` |
| **Super-property** | `cidoc:P70_documents` |
| **Created** | 2025-10-17 |

### Description

This property associates a sales contract with a third party who provides the payment (funds) on behalf of the buyer. It represents a simplified shortcut for data entry that is transformed into the full CIDOC-CRM structure for formal compliance.

**Full CIDOC-CRM Path**:
```
E31_Document → P70_documents → E8_Acquisition → 
  P9_consists_of → E7_Activity → 
    P14_carried_out_by → E21_Person (payment provider)
    P14.1_in_the_role_of → E55_Type (payer)
    P2_has_type → E55_Type (financial transaction)
```

### Key Distinctions

Payment providers are distinct from:
- **Procurators** (P70.5): Legal representatives who act with legal authority
- **Guarantors** (P70.7): Provide security/assurance but not necessarily funds
- **Brokers** (P70.8): Facilitate transactions between parties
- **Buyers** (P70.2): The principal party receiving the property

Payment providers specifically supply the actual funds for the purchase, often in situations involving:
- Family support (parent funding child's purchase)
- Business partnerships (partner providing capital)
- Creditor arrangements (lender providing direct payment)
- Institutional financing (bank providing funds)

---

## Semantic Structure

### Class Hierarchy

```
cidoc:E1_CRM_Entity
  └─ cidoc:E89_Propositional_Object
      └─ cidoc:E73_Information_Object
          └─ cidoc:E31_Document
              └─ gmn:E31_1_Contract
                  └─ gmn:E31_2_Sales_Contract [domain]
```

### Property Hierarchy

```
rdf:Property
  └─ owl:ObjectProperty
      └─ cidoc:P70_documents [super-property]
          └─ gmn:P70_9_documents_payment_provider_for_buyer
```

### Range Class

```
cidoc:E1_CRM_Entity
  └─ cidoc:E77_Persistent_Item
      └─ cidoc:E70_Thing
          └─ cidoc:E72_Legal_Object
              └─ cidoc:E39_Actor
                  └─ cidoc:E21_Person [range]
```

---

## CIDOC-CRM Mapping

### Shortcut Property Structure

The simplified property in Omeka-S/data entry:

```turtle
<contract/123> a gmn:E31_2_Sales_Contract ;
    gmn:P70_9_documents_payment_provider_for_buyer <person/456> .
```

### Full CIDOC-CRM Structure

The expanded CIDOC-CRM compliant structure after transformation:

```turtle
<contract/123> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <contract/123/acquisition> .

<contract/123/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P9_consists_of <contract/123/activity/payment_12345678> .

<contract/123/activity/payment_12345678> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300055984> ;  # financial transaction
    cidoc:P14_carried_out_by <person/456> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300386048> .  # payer

<person/456> a cidoc:E21_Person .

<http://vocab.getty.edu/page/aat/300055984> a cidoc:E55_Type ;
    rdfs:label "financial transactions"@en .

<http://vocab.getty.edu/page/aat/300386048> a cidoc:E55_Type ;
    rdfs:label "payers"@en .
```

### Path Components

1. **E31_Document → P70_documents → E8_Acquisition**
   - The contract documents an acquisition event

2. **E8_Acquisition → P9_consists_of → E7_Activity**
   - The acquisition consists of a payment activity

3. **E7_Activity → P2_has_type → E55_Type (financial transaction)**
   - The activity is typed as a financial transaction

4. **E7_Activity → P14_carried_out_by → E21_Person**
   - The activity is carried out by the payment provider

5. **E7_Activity → P14.1_in_the_role_of → E55_Type (payer)**
   - The person acts in the role of payer

---

## Transformation Pattern

### JSON-LD Input

```json
{
  "@context": {
    "gmn": "https://w3id.org/geniza/ontology/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "https://example.org/contract/SalesContract_123",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": {
    "@id": "https://example.org/person/Giovanni_Rossi"
  },
  "gmn:P70_2_documents_buyer": {
    "@id": "https://example.org/person/Marco_Bianchi"
  },
  "gmn:P70_9_documents_payment_provider_for_buyer": [
    {
      "@id": "https://example.org/person/Pietro_Bianchi",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

### JSON-LD Output (Transformed)

```json
{
  "@context": {
    "gmn": "https://w3id.org/geniza/ontology/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "https://example.org/contract/SalesContract_123",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://example.org/contract/SalesContract_123/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "https://example.org/person/Marco_Bianchi"
        }
      ],
      "cidoc:P23_transferred_title_from": [
        {
          "@id": "https://example.org/person/Giovanni_Rossi"
        }
      ],
      "cidoc:P9_consists_of": [
        {
          "@id": "https://example.org/contract/SalesContract_123/activity/payment_a7b3c4d2",
          "@type": "cidoc:E7_Activity",
          "cidoc:P2_has_type": {
            "@id": "http://vocab.getty.edu/page/aat/300055984",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P14_carried_out_by": [
            {
              "@id": "https://example.org/person/Pietro_Bianchi",
              "@type": "cidoc:E21_Person"
            }
          ],
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/page/aat/300386048",
            "@type": "cidoc:E55_Type"
          }
        }
      ]
    }
  ]
}
```

### Transformation Algorithm

1. **Check for Property**: Verify `gmn:P70_9_documents_payment_provider_for_buyer` exists
2. **Extract Payment Providers**: Get list of payment provider URIs/objects
3. **Ensure E8_Acquisition**: Create if doesn't exist, or use existing
4. **Initialize P9_consists_of**: Ensure the consists_of list exists
5. **For Each Payment Provider**:
   a. Extract or create person data
   b. Generate unique activity URI using hash
   c. Create E7_Activity node with:
      - Financial transaction type (P2_has_type)
      - Payment provider as carried_out_by (P14)
      - Payer role (P14.1_in_the_role_of)
   d. Append activity to P9_consists_of
6. **Clean Up**: Remove shortcut property

---

## Vocabulary References

### Getty Art & Architecture Thesaurus (AAT)

#### Payer Concept
- **URI**: `http://vocab.getty.edu/page/aat/300386048`
- **Preferred Label**: "payers" (English)
- **Scope Note**: People or organizations that make payments
- **Hierarchy**: people → people by activity → payers

#### Financial Transaction Concept
- **URI**: `http://vocab.getty.edu/page/aat/300055984`
- **Preferred Label**: "financial transactions" (English)
- **Scope Note**: Commercial or legal transactions involving monetary exchange
- **Hierarchy**: activities → economic and business activities → financial transactions

### CIDOC-CRM Classes

#### E7 Activity
- **Definition**: Comprises actions intentionally carried out by instances of E39 Actor
- **Scope**: Used to represent the payment activity
- **Super-classes**: E5 Event

#### E8 Acquisition
- **Definition**: Comprises transfers of legal ownership from one or more instances of E39 Actor to one or more other instances of E39 Actor
- **Scope**: The main event documented by the sales contract
- **Super-classes**: E7 Activity

#### E21 Person
- **Definition**: Real persons who live or are assumed to have lived
- **Scope**: The payment provider, buyer, seller, etc.
- **Super-classes**: E20 Biological Object, E39 Actor

#### E55 Type
- **Definition**: Comprises concepts denoted by terms from thesauri and controlled vocabularies
- **Scope**: Used for typing activities and roles
- **Super-classes**: E28 Conceptual Object

### CIDOC-CRM Properties

#### P2 has type
- **Domain**: E1 CRM Entity
- **Range**: E55 Type
- **Usage**: Links the activity to its type (financial transaction)

#### P9 consists of
- **Domain**: E4 Period
- **Range**: E4 Period
- **Usage**: Links the acquisition to the payment activity

#### P14 carried out by
- **Domain**: E7 Activity
- **Range**: E39 Actor
- **Usage**: Links the payment activity to the payment provider

#### P14.1 in the role of
- **Domain**: E7 Activity
- **Range**: E55 Type
- **Usage**: Specifies the role (payer) of the actor in the activity

#### P70 documents
- **Domain**: E31 Document
- **Range**: E1 CRM Entity
- **Usage**: Links the contract to the acquisition event

---

## Usage Examples

### Example 1: Father Provides Payment for Son

**Scenario**: Marco Bianchi purchases a house, but his father Pietro Bianchi provides the funds.

```json
{
  "@id": "https://example.org/contract/1456",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": {
    "@id": "https://example.org/person/Marco_Bianchi"
  },
  "gmn:P70_9_documents_payment_provider_for_buyer": [
    {
      "@id": "https://example.org/person/Pietro_Bianchi",
      "rdfs:label": "Pietro Bianchi (father)"
    }
  ]
}
```

### Example 2: Business Partner Provides Capital

**Scenario**: Giovanni buys merchant inventory, with his business partner Antonio supplying the funds.

```json
{
  "@id": "https://example.org/contract/1789",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": {
    "@id": "https://example.org/person/Giovanni_Medici"
  },
  "gmn:P70_9_documents_payment_provider_for_buyer": [
    {
      "@id": "https://example.org/person/Antonio_Strozzi",
      "rdfs:label": "Antonio Strozzi (business partner)"
    }
  ]
}
```

### Example 3: Multiple Payment Providers

**Scenario**: A large purchase funded by two creditors.

```json
{
  "@id": "https://example.org/contract/2045",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": {
    "@id": "https://example.org/person/Francesco_Alberti"
  },
  "gmn:P70_9_documents_payment_provider_for_buyer": [
    {
      "@id": "https://example.org/person/Lorenzo_Pazzi",
      "rdfs:label": "Lorenzo Pazzi (partial payment)"
    },
    {
      "@id": "https://example.org/person/Cosimo_Rucellai",
      "rdfs:label": "Cosimo Rucellai (partial payment)"
    }
  ]
}
```

### Example 4: Integration with Other Properties

**Complete contract with payment provider, guarantor, and price**:

```json
{
  "@id": "https://example.org/contract/3456",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": {
    "@id": "https://example.org/person/Seller_123"
  },
  "gmn:P70_2_documents_buyer": {
    "@id": "https://example.org/person/Buyer_456"
  },
  "gmn:P70_7_documents_buyers_guarantor": [
    {
      "@id": "https://example.org/person/Guarantor_789"
    }
  ],
  "gmn:P70_9_documents_payment_provider_for_buyer": [
    {
      "@id": "https://example.org/person/Payer_101"
    }
  ],
  "gmn:P70_16_documents_sale_price_amount": [
    {
      "@value": "500",
      "@type": "xsd:decimal"
    }
  ],
  "gmn:P70_17_documents_sale_price_currency": [
    {
      "@id": "https://example.org/currency/Florin"
    }
  ]
}
```

---

## Comparison with Related Properties

### P70.9 vs. P70.5 (Buyer's Procurator)

| Aspect | P70.9 Payment Provider | P70.5 Buyer's Procurator |
|--------|------------------------|--------------------------|
| **Function** | Supplies funds | Legal representative |
| **Authority** | Financial only | Legal and financial |
| **Relationship** | May be family/creditor | Formal legal appointment |
| **Transformation** | E7_Activity with payer role | E7_Activity with agent role |
| **Typical Cases** | Family support, loans | Legal representation |

### P70.9 vs. P70.7 (Buyer's Guarantor)

| Aspect | P70.9 Payment Provider | P70.7 Buyer's Guarantor |
|--------|------------------------|-------------------------|
| **Function** | Provides payment | Provides security |
| **Obligation** | Immediate payment | Conditional obligation |
| **Relationship** | Direct financial support | Risk mitigation |
| **Transformation** | Financial transaction activity | Guarantor activity |
| **Typical Cases** | Direct funding | Security for obligations |

### P70.9 vs. P70.8 (Broker)

| Aspect | P70.9 Payment Provider | P70.8 Broker |
|--------|------------------------|--------------|
| **Function** | Supplies funds | Facilitates transaction |
| **Party** | Acts for buyer | Acts for both parties |
| **Compensation** | Not typically | Commission |
| **Transformation** | Part of E8_Acquisition | Direct P14 on E8 |
| **Typical Cases** | Family/creditor funding | Professional intermediary |

### P70.9 vs. P70.10 (Payment Recipient for Seller)

| Aspect | P70.9 Payment Provider | P70.10 Payment Recipient |
|--------|------------------------|---------------------------|
| **Direction** | Provides to buyer | Receives from seller |
| **Function** | Source of funds | Destination of funds |
| **Relationship** | Related to buyer | Related to seller |
| **Transformation** | Payer role activity | Payee role activity |
| **Typical Cases** | Funding buyer's purchase | Receiving seller's proceeds |

---

## Implementation Notes

### Data Entry Considerations

1. **When to Use This Property**:
   - When someone other than the buyer provides the actual payment
   - When explicit mention is made in the contract text
   - When the payment source is significant to the transaction

2. **When NOT to Use This Property**:
   - When the buyer themselves makes payment (use P70.2 only)
   - For legal representatives (use P70.5 procurator instead)
   - For security providers (use P70.7 guarantor instead)
   - For transaction facilitators (use P70.8 broker instead)

### Multiple Payment Providers

The property accepts multiple values when:
- Multiple parties jointly provide payment
- Payment is split among several sources
- Different portions come from different providers

Each provider gets its own E7_Activity node with unique URI.

### Relationship to Other Entities

Payment providers can be:
- Related to buyers through family relationships
- Linked as business partners
- Identified as creditors or lenders
- Organizations (though range is E21_Person for individuals)

### URI Generation

Activity URIs are generated using:
```python
activity_hash = str(hash(payer_uri + 'payment_provider'))[-8:]
activity_uri = f"{subject_uri}/activity/payment_{activity_hash}"
```

This ensures:
- Uniqueness per payment provider
- Consistency across transformations
- Readability in output

### Performance Impact

- **Memory**: One E7_Activity per payment provider
- **Processing**: Linear time with number of providers
- **URI Generation**: Constant time hash operation
- **Typical Case**: 1-2 payment providers per contract

---

## SPARQL Query Examples

### Find All Contracts with Payment Providers

```sparql
PREFIX gmn: <https://w3id.org/geniza/ontology/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?buyer ?payer
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition .
  ?acquisition cidoc:P22_transferred_title_to ?buyer ;
               cidoc:P9_consists_of ?activity .
  ?activity cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300386048> ;
            cidoc:P14_carried_out_by ?payer .
}
```

### Find Buyers Who Had Payment Providers

```sparql
PREFIX gmn: <https://w3id.org/geniza/ontology/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?buyer (COUNT(DISTINCT ?payer) as ?payerCount)
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition .
  ?acquisition cidoc:P22_transferred_title_to ?buyer ;
               cidoc:P9_consists_of ?activity .
  ?activity cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300386048> ;
            cidoc:P14_carried_out_by ?payer .
}
GROUP BY ?buyer
HAVING (COUNT(DISTINCT ?payer) > 0)
```

### Find Financial Transactions in Contracts

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?activity ?person ?role
WHERE {
  ?contract cidoc:P70_documents ?acquisition .
  ?acquisition cidoc:P9_consists_of ?activity .
  ?activity cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300055984> ;
            cidoc:P14_carried_out_by ?person ;
            cidoc:P14.1_in_the_role_of ?role .
}
```

---

## Validation Rules

### Required Elements After Transformation

1. E8_Acquisition must exist
2. E7_Activity must have:
   - Valid URI with hash
   - Type: financial transaction (AAT 300055984)
   - At least one P14_carried_out_by
   - Role: payer (AAT 300386048)
3. Payment provider must be E21_Person
4. Shortcut property must be removed

### Constraint Checking

```python
def validate_payment_provider_transformation(data):
    """Validate P70.9 transformation."""
    assert 'gmn:P70_9_documents_payment_provider_for_buyer' not in data
    assert 'cidoc:P70_documents' in data
    acquisition = data['cidoc:P70_documents'][0]
    assert 'cidoc:P9_consists_of' in acquisition
    
    for activity in acquisition['cidoc:P9_consists_of']:
        if activity.get('cidoc:P14.1_in_the_role_of', {}).get('@id') == AAT_PAYER:
            assert activity['@type'] == 'cidoc:E7_Activity'
            assert activity['cidoc:P2_has_type']['@id'] == AAT_FINANCIAL_TRANSACTION
            assert len(activity['cidoc:P14_carried_out_by']) > 0
            return True
    
    return False
```

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**Ontology Version**: GMN 1.0  
**CIDOC-CRM Version**: 7.1.1
