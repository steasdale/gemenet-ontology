# Ontology Documentation: P70.10 Documents Payment Recipient for Seller

Complete semantic documentation for the `gmn:P70_10_documents_payment_recipient_for_seller` property and its transformation to CIDOC-CRM.

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Semantic Definition](#semantic-definition)
3. [Class Definitions](#class-definitions)
4. [Property Specifications](#property-specifications)
5. [Transformation Patterns](#transformation-patterns)
6. [Use Cases and Examples](#use-cases-and-examples)
7. [Comparison with Related Properties](#comparison-with-related-properties)
8. [Implementation Patterns](#implementation-patterns)

---

## Property Overview

### Core Property

**URI**: `gmn:P70_10_documents_payment_recipient_for_seller`

**Label**: "P70.10 documents payment recipient for seller" (English)

**Definition**: Simplified property for associating a sales contract with a third party who receives the payment (funds) on behalf of the seller.

**Category**: Sales Contract Property (P70 series)

**Purpose**: To document situations where payment for a sale is received by someone other than the seller themselves, particularly in cases involving family members, business partners, or creditors.

---

## Semantic Definition

### Full Description

The `gmn:P70_10_documents_payment_recipient_for_seller` property establishes a relationship between a sales contract document and a person who receives payment on behalf of the seller. This property captures an important aspect of historical commercial transactions where the actual flow of funds often involved intermediaries or designated recipients.

### Key Characteristics

1. **Third-Party Nature**: The payment recipient is neither the seller nor the buyer
2. **Financial Role**: The person receives actual funds, not just documentation
3. **Authorization**: Implicit or explicit authorization by the seller
4. **Distinct from Other Roles**: Not a procurator, guarantor, or broker

### Historical Context

In medieval and early modern commercial transactions, payment recipients served various functions:

- **Family Representatives**: Adult children receiving payment for elderly parents
- **Business Proxies**: Partners receiving payment for shared business ventures
- **Debt Settlement**: Creditors receiving direct payment to settle seller's obligations
- **Estate Management**: Executors or administrators collecting payment for estates
- **Agent Services**: Authorized agents collecting funds on behalf of absent principals

### Distinction from Related Roles

| Role | Function | Authorization Type | Payment Involvement |
|------|----------|-------------------|-------------------|
| **Payment Recipient** | Receives funds | Seller authorization | Receives actual payment |
| Procurator | Legal representative | Formal power of attorney | May handle transaction |
| Guarantor | Security provider | Contractual obligation | Contingent payment |
| Broker | Transaction facilitator | Commission agreement | Facilitates but doesn't receive |

---

## Class Definitions

### Domain Class: gmn:E31_2_Sales_Contract

**Hierarchy**: 
```
cidoc:E31_Document
  └── gmn:E31_1_Notarial_Document
       └── gmn:E31_2_Sales_Contract
```

**Definition**: A formal document recording the transfer of ownership of property from a seller to a buyer in exchange for payment.

**Key Properties**:
- Documents seller (P70.1)
- Documents buyer (P70.2)
- Documents transfer of property (P70.3)
- Documents payment arrangements (P70.9, P70.10)

### Range Class: cidoc:E21_Person

**Definition**: Real persons who live or are assumed to have lived, as documented in historical records.

**Scope**: Includes all individual human beings, whether they have known identity or are merely referenced in documents.

**In This Context**: The payment recipient is an E21_Person who is distinct from both the seller and the buyer.

---

## Property Specifications

### Main Property: gmn:P70_10_documents_payment_recipient_for_seller

**Full Formal Specification**:

```turtle
gmn:P70_10_documents_payment_recipient_for_seller
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.10 documents payment recipient for seller"@en ;
    rdfs:comment "Simplified property for associating a sales contract with a third party who receives the payment (funds) on behalf of the seller. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (payment recipient), with P17_was_motivated_by linking to the seller (E21_Person). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Unlike procurators (legal representatives), guarantors (security providers), or brokers (facilitators), payment recipients are third parties who receive the actual funds from the purchase on behalf of the seller, often in situations involving family members, business partners, or creditors to whom the seller owes money."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P17_was_motivated_by .
```

**Property Attributes**:

| Attribute | Value |
|-----------|-------|
| **Type** | owl:ObjectProperty, rdf:Property |
| **Domain** | gmn:E31_2_Sales_Contract |
| **Range** | cidoc:E21_Person |
| **Super Property** | cidoc:P70_documents |
| **Cardinality** | 0..n (multiple recipients possible) |
| **Functional** | No (one-to-many relationship) |
| **Inverse** | None (unidirectional) |

### Supporting Property: gmn:has_payment_received_by

**Full Formal Specification**:

```turtle
gmn:has_payment_received_by
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "has payment received by"@en ;
    rdfs:comment "Direct relationship linking a person (seller) to another person (payment recipient) who receives the funds from their sale. This property provides a simple semantic link between sellers and those who collect payment on their behalf. When used in the context of sales contracts, this relationship is documented within the contract and elaborated through E7_Activity nodes in the acquisition event structure. This property enables Omeka-S annotations to directly connect sellers with their payment recipients."@en ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date .
```

**Property Attributes**:

| Attribute | Value |
|-----------|-------|
| **Type** | owl:ObjectProperty, rdf:Property |
| **Domain** | cidoc:E21_Person (seller) |
| **Range** | cidoc:E21_Person (payment recipient) |
| **Super Property** | None (top-level custom property) |
| **Cardinality** | 0..n |
| **Purpose** | Omeka-S annotations and simplified querying |

---

## Transformation Patterns

### Pattern 1: Simplified to Full CIDOC-CRM

**Input (Simplified GMN)**:

```turtle
@prefix gmn: <http://example.org/gmn/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

contract:123 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller person:Giovanni ;
    gmn:P70_2_documents_buyer person:Marco ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Antonio .
```

**Output (Full CIDOC-CRM)**:

```turtle
contract:123 a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents acquisition:123 .

acquisition:123 a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from person:Giovanni ;
    cidoc:P22_transferred_title_to person:Marco ;
    cidoc:P9_consists_of activity:payment_abc123 .

activity:payment_abc123 a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417629> ; # financial transaction
    cidoc:P14_carried_out_by person:Antonio ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300025555> . # payee

person:Giovanni a cidoc:E21_Person ;
    gmn:has_payment_received_by person:Antonio .

person:Antonio a cidoc:E21_Person .
```

### Pattern 2: Multiple Payment Recipients

**Input**:

```turtle
contract:456 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller person:Pietro ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Lorenzo ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Matteo .
```

**Output**:

```turtle
contract:456 cidoc:P70_documents acquisition:456 .

acquisition:456 a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from person:Pietro ;
    cidoc:P9_consists_of activity:payment_def456 ;
    cidoc:P9_consists_of activity:payment_ghi789 .

activity:payment_def456 a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417629> ;
    cidoc:P14_carried_out_by person:Lorenzo ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300025555> .

activity:payment_ghi789 a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417629> ;
    cidoc:P14_carried_out_by person:Matteo ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300025555> .

person:Pietro gmn:has_payment_received_by person:Lorenzo ;
    gmn:has_payment_received_by person:Matteo .
```

### Pattern 3: Integration with Other P70 Properties

**Input**:

```turtle
contract:789 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller person:Roberto ;
    gmn:P70_2_documents_buyer person:Franco ;
    gmn:P70_4_documents_sellers_procurator person:Sergio ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Claudio .
```

**Output**:

```turtle
contract:789 cidoc:P70_documents acquisition:789 .

acquisition:789 a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from person:Roberto ;
    cidoc:P22_transferred_title_to person:Franco ;
    cidoc:P9_consists_of activity:representation_xyz123 ;
    cidoc:P9_consists_of activity:payment_jkl012 .

# Procurator activity
activity:representation_xyz123 a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300435126> ; # legal representation
    cidoc:P14_carried_out_by person:Sergio ;
    cidoc:P17_was_motivated_by person:Roberto .

# Payment receipt activity
activity:payment_jkl012 a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417629> ; # financial transaction
    cidoc:P14_carried_out_by person:Claudio ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300025555> . # payee
```

---

## Use Cases and Examples

### Use Case 1: Family Member as Payment Recipient

**Scenario**: An elderly father sells property, but his adult son receives the payment on his behalf.

**Simplified Data Entry**:

```turtle
contract:elderly_father_sale a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller person:Giovanni_the_Elder ;
    gmn:P70_2_documents_buyer person:Merchant_Marco ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Giovanni_the_Younger .

person:Giovanni_the_Elder gmn:has_payment_received_by person:Giovanni_the_Younger .
```

**Semantic Explanation**: The contract documents that Giovanni the Elder is selling property to Merchant Marco, but payment is received by Giovanni the Younger (presumably his son).

### Use Case 2: Creditor as Direct Payment Recipient

**Scenario**: A seller directs that payment be made directly to a creditor to settle a debt.

**Simplified Data Entry**:

```turtle
contract:debt_settlement_sale a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller person:Debtor_Paolo ;
    gmn:P70_2_documents_buyer person:Buyer_Luca ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Creditor_Antonio .

person:Debtor_Paolo gmn:has_payment_received_by person:Creditor_Antonio .
```

**Semantic Explanation**: Paolo is selling to Luca, but instructs that payment go directly to Antonio (to whom Paolo owes money).

### Use Case 3: Business Partner Collecting Joint Venture Payment

**Scenario**: Two partners jointly own property; one partner (the seller) directs payment to the other partner.

**Simplified Data Entry**:

```turtle
contract:partnership_sale a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller person:Partner_Francesco ;
    gmn:P70_2_documents_buyer person:Outside_Buyer ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Partner_Stefano .

person:Partner_Francesco gmn:has_payment_received_by person:Partner_Stefano .
```

**Semantic Explanation**: Francesco is selling his partnership interest, but payment is collected by his business partner Stefano.

### Use Case 4: Multiple Recipients for Partial Payments

**Scenario**: Payment is split among multiple recipients on behalf of the seller.

**Simplified Data Entry**:

```turtle
contract:split_payment_sale a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller person:Estate_Executor ;
    gmn:P70_2_documents_buyer person:Property_Buyer ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Heir_One ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Heir_Two ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Heir_Three .

person:Estate_Executor gmn:has_payment_received_by person:Heir_One ;
    gmn:has_payment_received_by person:Heir_Two ;
    gmn:has_payment_received_by person:Heir_Three .
```

**Semantic Explanation**: The executor is selling estate property, with payment divided among three heirs.

---

## Comparison with Related Properties

### Comparison Table

| Property | Role Type | Relationship to Principal | Payment Involvement | Typical Authorization |
|----------|-----------|-------------------------|-------------------|---------------------|
| **P70.10 Payment Recipient** | Financial collector | Acts for seller | Receives payment | Seller authorization |
| P70.4 Seller's Procurator | Legal representative | Represents seller | May handle funds | Power of attorney |
| P70.6 Seller's Guarantor | Security provider | Guarantees seller | Contingent payment | Contractual bond |
| P70.8 Broker | Transaction facilitator | Neutral intermediary | Commission only | Service agreement |
| P70.9 Payment Provider | Financial source | Acts for buyer | Provides payment | Buyer authorization |

### Semantic Distinctions

**Payment Recipient vs. Procurator**:
- **Payment Recipient**: Receives funds; may or may not have legal authority
- **Procurator**: Has legal authority to act; may or may not receive funds

**Payment Recipient vs. Guarantor**:
- **Payment Recipient**: Receives payment as authorized collector
- **Guarantor**: Only receives payment if principal defaults

**Payment Recipient vs. Broker**:
- **Payment Recipient**: Receives principal's payment
- **Broker**: Receives commission for facilitating transaction

### Modeling Rationale

The `P70_10` property models the payment recipient as the actor of a payment receipt activity (`E7_Activity`) rather than as a direct property of the acquisition. This approach:

1. **Distinguishes Activity from Status**: Receiving payment is an action, not an attribute
2. **Enables Multiple Recipients**: Each recipient has their own activity node
3. **Supports Role Specification**: The `P14.1_in_the_role_of` property clarifies the person's role
4. **Maintains Event Structure**: Payment receipt is a constituent activity of the acquisition
5. **Aligns with CIDOC-CRM Patterns**: Follows established patterns for transaction participants

---

## Implementation Patterns

### Pattern A: Simple Single Recipient

```python
# Input data
contract_data = {
    '@id': 'contract:001',
    'gmn:P70_10_documents_payment_recipient_for_seller': [
        {'@id': 'person:recipient', '@type': 'cidoc:E21_Person'}
    ]
}

# Transformation creates
acquisition = {
    '@id': 'contract:001/acquisition',
    '@type': 'cidoc:E8_Acquisition',
    'cidoc:P9_consists_of': [
        {
            '@id': 'contract:001/activity/payment_xyz',
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {'@id': AAT_FINANCIAL_TRANSACTION},
            'cidoc:P14_carried_out_by': [
                {'@id': 'person:recipient', '@type': 'cidoc:E21_Person'}
            ],
            'cidoc:P14.1_in_the_role_of': {'@id': AAT_PAYEE}
        }
    ]
}
```

### Pattern B: Multiple Recipients

```python
# Input data
contract_data = {
    '@id': 'contract:002',
    'gmn:P70_10_documents_payment_recipient_for_seller': [
        {'@id': 'person:recipient_a'},
        {'@id': 'person:recipient_b'}
    ]
}

# Transformation creates separate activities
acquisition = {
    '@id': 'contract:002/acquisition',
    '@type': 'cidoc:E8_Acquisition',
    'cidoc:P9_consists_of': [
        {
            '@id': 'contract:002/activity/payment_abc',
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [{'@id': 'person:recipient_a'}],
            'cidoc:P14.1_in_the_role_of': {'@id': AAT_PAYEE}
        },
        {
            '@id': 'contract:002/activity/payment_def',
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [{'@id': 'person:recipient_b'}],
            'cidoc:P14.1_in_the_role_of': {'@id': AAT_PAYEE}
        }
    ]
}
```

### Pattern C: Integration with Existing Acquisition

```python
# Input data with existing acquisition
contract_data = {
    '@id': 'contract:003',
    'cidoc:P70_documents': [{
        '@id': 'contract:003/acquisition',
        '@type': 'cidoc:E8_Acquisition',
        'cidoc:P23_transferred_title_from': [{'@id': 'person:seller'}]
    }],
    'gmn:P70_10_documents_payment_recipient_for_seller': [
        {'@id': 'person:recipient'}
    ]
}

# Transformation appends to existing acquisition
# acquisition['cidoc:P9_consists_of'] is extended with payment activity
```

---

## Validation Rules

### Data Entry Validation

1. **Domain Check**: Subject must be `gmn:E31_2_Sales_Contract`
2. **Range Check**: Object must be `cidoc:E21_Person`
3. **Existence Check**: Referenced person must exist in person registry
4. **Uniqueness Check**: Same person shouldn't be both seller and payment recipient
5. **Completeness Check**: If payment recipient specified, seller should be documented

### Transformation Validation

1. **Activity Creation**: Each recipient generates exactly one E7_Activity
2. **Activity Type**: Each activity must have P2_has_type pointing to AAT financial transaction
3. **Actor Link**: Each activity must link to recipient via P14_carried_out_by
4. **Role Specification**: Each activity must include P14.1_in_the_role_of pointing to AAT payee
5. **Nesting**: All activities must be nested in E8_Acquisition via P9_consists_of
6. **Cleanup**: Original simplified property must be removed

### Semantic Validation

1. **Role Coherence**: Payment recipient should not also be buyer
2. **Authorization**: Consider if seller is documented
3. **Context**: Payment recipient makes sense in historical/legal context
4. **Completeness**: Consider if payment amount (P70.16) is also documented

---

## References

### CIDOC-CRM Documentation

- **E7 Activity**: http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.3
- **E8 Acquisition**: http://www.cidoc-crm.org/Entity/E8-Acquisition/version-7.1.3
- **P9 consists of**: http://www.cidoc-crm.org/Property/P9-consists-of/version-7.1.3
- **P14 carried out by**: http://www.cidoc-crm.org/Property/P14-carried-out-by/version-7.1.3
- **P70 documents**: http://www.cidoc-crm.org/Property/P70-documents/version-7.1.3

### Getty AAT

- **Financial Transactions**: http://vocab.getty.edu/aat/300417629
- **Payee**: http://vocab.getty.edu/aat/300025555

### Related GMN Properties

- **P70.1 documents seller**: The seller on whose behalf payment is received
- **P70.9 documents payment provider for buyer**: Parallel property for buyer's side
- **has_payment_received_by**: Direct person-to-person payment relationship

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-17 | 1.0 | Initial property definition |
| 2025-10-27 | 1.1 | Complete documentation package |

---

*This documentation provides the complete semantic specification for implementing the payment recipient for seller property in the GMN ontology.*
