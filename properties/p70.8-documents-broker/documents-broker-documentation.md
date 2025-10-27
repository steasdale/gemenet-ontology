# Ontology Documentation: gmn:P70_8_documents_broker

## Complete Semantic Documentation with Examples

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Formal Definition](#formal-definition)
3. [Semantic Structure](#semantic-structure)
4. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
5. [Domain and Range](#domain-and-range)
6. [Role Specification](#role-specification)
7. [Historical Context](#historical-context)
8. [Usage Guidelines](#usage-guidelines)
9. [Transformation Examples](#transformation-examples)
10. [Relationship to Other Properties](#relationship-to-other-properties)

---

## Property Overview

### Basic Information

| Aspect | Value |
|--------|-------|
| **Property URI** | `gmn:P70_8_documents_broker` |
| **Label** | "P70.8 documents broker"@en |
| **Property Type** | `owl:ObjectProperty`, `rdf:Property` |
| **Super Property** | `cidoc:P70_documents` |
| **Domain** | `gmn:E31_2_Sales_Contract` |
| **Range** | `cidoc:E21_Person` |
| **Created** | 2025-10-17 |
| **Status** | Active |

### Purpose

This simplified property associates a sales contract with the person(s) named as broker(s) who facilitated the transaction. Brokers are neutral intermediaries who arrange transactions between buyers and sellers, typically receiving a commission for their services.

### Key Characteristics

1. **Neutral Facilitator**: Unlike procurators (who represent one party) or guarantors (who provide security for one party), brokers facilitate the transaction for both parties
2. **Professional Role**: Often licensed or officially recognized intermediaries
3. **Commission-Based**: Typically compensated through fees or commission
4. **No Legal Authority**: Unlike procurators, brokers don't have legal authority to act on behalf of parties
5. **Transaction Arrangers**: Focus on bringing parties together and facilitating agreement

---

## Formal Definition

### RDF/Turtle Representation

```turtle
# Property: P70.8 documents broker
gmn:P70_8_documents_broker
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.8 documents broker"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the broker who facilitated the transaction. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P14_carried_out_by > E21_Person. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Unlike procurators and guarantors who act for one party, brokers facilitate the transaction between both parties, arranging the sale and often receiving a commission."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

### OWL Axioms

The property is characterized by the following OWL semantics:

1. **Object Property**: Links two resources (contract and person)
2. **Functional**: Not necessarily functional (multiple brokers possible)
3. **Inverse Functional**: No (multiple contracts may have same broker)
4. **Transitive**: No
5. **Symmetric**: No
6. **Reflexive**: No

---

## Semantic Structure

### Simplified View (Data Entry)

```
E31_2_Sales_Contract --P70_8_documents_broker--> E21_Person (Broker)
```

### Full CIDOC-CRM Structure (After Transformation)

```
E31_2_Sales_Contract
  └─ P70_documents
      └─ E8_Acquisition
          └─ P14_carried_out_by
              └─ E21_Person (Broker)
                  └─ P14.1_in_the_role_of
                      └─ E55_Type (aat:300025234 "brokers")
```

### Detailed Structure

```turtle
# Document (Sales Contract)
<contract> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <acquisition> .

# Acquisition Event
<acquisition> a cidoc:E8_Acquisition ;
    cidoc:P14_carried_out_by <broker> .

# Broker Person
<broker> a cidoc:E21_Person ;
    rdfs:label "Name of Broker" ;
    cidoc:P14.1_in_the_role_of <aat:300025234> .

# Broker Role Type
<aat:300025234> a cidoc:E55_Type ;
    rdfs:label "brokers (people)" .
```

---

## CIDOC-CRM Mapping

### Property Chain

The simplified property represents this CIDOC-CRM property chain:

```
E31_Document 
  --P70_documents--> E8_Acquisition 
    --P14_carried_out_by--> E21_Person
```

### Why This Structure?

1. **P70_documents**: Links document to documented event (acquisition)
2. **E8_Acquisition**: Represents the actual transfer of ownership
3. **P14_carried_out_by**: Links event to actors who performed it
4. **E21_Person**: The broker who facilitated the transaction
5. **P14.1_in_the_role_of**: Qualifies the person's specific role as broker

### Difference from Procurator Structure

**Broker** (simpler - no P17 motivation):
```
E8_Acquisition --P14_carried_out_by--> E21_Person (broker with role)
```

**Procurator** (more complex - has P17 motivation):
```
E8_Acquisition --P9_consists_of--> E7_Activity 
  --P14_carried_out_by--> E21_Person (procurator with role)
  --P17_was_motivated_by--> E21_Person (principal)
```

**Why the difference?**
- Procurators represent a specific party (seller or buyer)
- Brokers facilitate for both parties equally
- Therefore, brokers attach directly to the acquisition without needing P17 to specify which party they represent

---

## Domain and Range

### Domain: gmn:E31_2_Sales_Contract

The property applies to sales contracts specifically because:
1. Brokers primarily facilitated commercial transactions
2. Sales of property commonly involved professional intermediaries
3. The acquisition event model (E8_Acquisition) is specific to ownership transfer

**Domain Class Hierarchy**:
```
cidoc:E31_Document
  └─ gmn:E31_1_Contract
      └─ gmn:E31_2_Sales_Contract  ← Domain of P70_8
```

### Range: cidoc:E21_Person

The property's range is restricted to persons because:
1. Brokers in medieval Genoa were individuals, not organizations
2. Brokerage required personal relationships and trust
3. Historical sources name individual brokers by name

**Range Class Hierarchy**:
```
cidoc:E1_CRM_Entity
  └─ cidoc:E77_Persistent_Item
      └─ cidoc:E70_Thing
          └─ cidoc:E72_Legal_Object
              └─ cidoc:E39_Actor
                  └─ cidoc:E21_Person  ← Range of P70_8
```

### Cardinality

- **Minimum**: 0 (not all contracts had brokers)
- **Maximum**: Unlimited (multiple brokers possible)
- **Typical**: 0-1 (most contracts with brokers had one)
- **Multiple**: Yes (some large transactions had multiple brokers)

---

## Role Specification

### Getty AAT Role Type

**URI**: http://vocab.getty.edu/page/aat/300025234

**Preferred Label**: "brokers (people)"

**Scope Note**: "People who act as intermediaries in negotiating contracts, purchases, or sales in return for a fee or commission."

**Hierarchical Position**:
```
agents (hierarchy name) (300024979)
  └─ agents (people) (300024978)
      └─ agents by general role (300025133)
          └─ brokers (people) (300025234)
```

### Related AAT Concepts

- **Procurators** (300386866): Legal representatives with authority
- **Guarantors** (300025614): Providers of security
- **Intermediaries** (300025188): General go-betweens
- **Merchants** (300025245): Commercial traders

### Why This AAT Term?

The AAT term "brokers (people)" precisely captures:
1. **Intermediary Role**: Acting between parties
2. **Negotiation Function**: Facilitating agreements
3. **Commercial Context**: Business transactions
4. **Commission Basis**: Fee-based service
5. **Professional Status**: Recognized role

---

## Historical Context

### Medieval Genoese Brokers (*Sensali*)

In medieval Genoa, brokers (Italian: *sensali*) were:

1. **Professional Intermediaries**
   - Often licensed by the commune
   - Specialized in different types of transactions
   - Required to maintain good reputation

2. **Transaction Facilitators**
   - Brought buyers and sellers together
   - Helped establish fair market prices
   - Witnessed agreements and sales

3. **Commission Recipients**
   - Received fees from one or both parties
   - Compensation based on transaction value
   - Sometimes paid in goods or services

4. **Neutral Parties**
   - Not advocates for either side
   - Balanced interests of both parties
   - Trustworthy intermediaries

5. **Record Keepers**
   - Maintained transaction records
   - Could testify about deals
   - Provided continuity of knowledge

### Typical Broker Activities

- Introducing potential buyers to sellers
- Assessing property values
- Negotiating terms and prices
- Facilitating payment arrangements
- Witnessing contract signatures
- Maintaining transaction records

### Distinction from Other Roles

| Role | Represents | Authority | Commission | Loyalty |
|------|------------|-----------|-----------|---------|
| **Broker** | Both parties | None | Yes | Neutral |
| **Procurator** | One party | Legal power | Usually no | Principal |
| **Guarantor** | One party | None | No | Principal |
| **Witness** | Neither | None | No | None |

---

## Usage Guidelines

### When to Use This Property

Use `gmn:P70_8_documents_broker` when:

1. ✅ Contract explicitly names a broker (*sensale*)
2. ✅ Person facilitated transaction for both parties
3. ✅ Person received commission or fee
4. ✅ Person acted as neutral intermediary
5. ✅ Document indicates brokerage role

### When NOT to Use This Property

Do NOT use for:

1. ❌ Procurators (use P70_4 or P70_5)
2. ❌ Guarantors (use P70_6 or P70_7)
3. ❌ Witnesses (use P70_15)
4. ❌ Payment providers (use P70_9)
5. ❌ Legal representatives
6. ❌ Family members facilitating transaction

### Data Entry Best Practices

1. **Verify Role**: Confirm person acted as broker, not in another capacity
2. **Check Terms**: Look for terms like *sensale*, *mediatore*, *broker*
3. **Multiple Roles**: Person may have multiple roles (e.g., broker and witness)
4. **Complete Information**: Include person's name and any identifying information
5. **Commission Note**: If commission is mentioned, note it separately

### Identification in Sources

Look for these indicators:

**Latin terms**:
- *sensalis*
- *mediator*
- *intermediarius*

**Italian terms**:
- *sensale*
- *sensaro*
- *mediatore*

**Contextual clues**:
- "pro eius mercede" (for his reward/commission)
- "intermediante" (intermediating)
- "qui dictum negotium procuravit" (who arranged said business)

---

## Transformation Examples

### Example 1: Simple Broker

#### Input (Simplified)

```turtle
@prefix gmn: <http://example.org/gmn#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

<contract_001> a gmn:E31_2_Sales_Contract ;
    rdfs:label "Sales Contract of 1345-03-15" ;
    gmn:P70_8_documents_broker <person_giovanni_broker> .

<person_giovanni_broker> a cidoc:E21_Person ;
    rdfs:label "Giovanni de Sancto Petro, sensale" .
```

#### Output (Full CIDOC-CRM)

```turtle
@prefix gmn: <http://example.org/gmn#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix aat: <http://vocab.getty.edu/page/aat/> .

<contract_001> a gmn:E31_2_Sales_Contract ;
    rdfs:label "Sales Contract of 1345-03-15" ;
    cidoc:P70_documents <contract_001/acquisition> .

<contract_001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P14_carried_out_by <person_giovanni_broker> .

<person_giovanni_broker> a cidoc:E21_Person ;
    rdfs:label "Giovanni de Sancto Petro, sensale" ;
    cidoc:P14.1_in_the_role_of aat:300025234 .

aat:300025234 a cidoc:E55_Type ;
    rdfs:label "brokers (people)" .
```

### Example 2: Multiple Brokers

#### Input (Simplified)

```turtle
<contract_002> a gmn:E31_2_Sales_Contract ;
    rdfs:label "Large Property Sale 1347" ;
    gmn:P70_8_documents_broker <person_giovanni_broker> ,
                                <person_marco_broker> .

<person_giovanni_broker> a cidoc:E21_Person ;
    rdfs:label "Giovanni Sensale" .

<person_marco_broker> a cidoc:E21_Person ;
    rdfs:label "Marco Broker" .
```

#### Output (Full CIDOC-CRM)

```turtle
<contract_002> a gmn:E31_2_Sales_Contract ;
    rdfs:label "Large Property Sale 1347" ;
    cidoc:P70_documents <contract_002/acquisition> .

<contract_002/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P14_carried_out_by <person_giovanni_broker> ,
                             <person_marco_broker> .

<person_giovanni_broker> a cidoc:E21_Person ;
    rdfs:label "Giovanni Sensale" ;
    cidoc:P14.1_in_the_role_of aat:300025234 .

<person_marco_broker> a cidoc:E21_Person ;
    rdfs:label "Marco Broker" ;
    cidoc:P14.1_in_the_role_of aat:300025234 .
```

### Example 3: Broker with Other Participants

#### Input (Simplified)

```turtle
<contract_003> a gmn:E31_2_Sales_Contract ;
    rdfs:label "House Sale with Broker 1350" ;
    gmn:P70_1_documents_seller <person_seller> ;
    gmn:P70_2_documents_buyer <person_buyer> ;
    gmn:P70_8_documents_broker <person_broker> ;
    gmn:P70_15_documents_witness <person_witness1> ,
                                  <person_witness2> .
```

#### Output (Full CIDOC-CRM) - Partial

```turtle
<contract_003> a gmn:E31_2_Sales_Contract ;
    rdfs:label "House Sale with Broker 1350" ;
    cidoc:P70_documents <contract_003/acquisition> .

<contract_003/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <person_seller> ;
    cidoc:P22_transferred_title_to <person_buyer> ;
    cidoc:P14_carried_out_by <person_broker> ;
    cidoc:P11_had_participant <person_witness1> ,
                               <person_witness2> .

<person_broker> a cidoc:E21_Person ;
    cidoc:P14.1_in_the_role_of aat:300025234 .

<person_witness1> a cidoc:E21_Person ;
    cidoc:P14.1_in_the_role_of aat:300028910 .

<person_witness2> a cidoc:E21_Person ;
    cidoc:P14.1_in_the_role_of aat:300028910 .
```

### Example 4: Complex Transaction

#### Input (Simplified)

```turtle
<contract_004> a gmn:E31_2_Sales_Contract ;
    rdfs:label "Complex Property Sale 1352" ;
    gmn:P70_1_documents_seller <person_seller> ;
    gmn:P70_2_documents_buyer <person_buyer> ;
    gmn:P70_4_documents_sellers_procurator <person_seller_procurator> ;
    gmn:P70_5_documents_buyers_procurator <person_buyer_procurator> ;
    gmn:P70_6_documents_sellers_guarantor <person_seller_guarantor> ;
    gmn:P70_8_documents_broker <person_broker> .
```

#### Output Shows Different Structural Levels

```turtle
<contract_004/acquisition> a cidoc:E8_Acquisition ;
    # Principals (direct participants)
    cidoc:P23_transferred_title_from <person_seller> ;
    cidoc:P22_transferred_title_to <person_buyer> ;
    
    # Broker (facilitator, attached to acquisition)
    cidoc:P14_carried_out_by <person_broker> ;
    
    # Procurators and guarantors (via E7_Activity with P17)
    cidoc:P9_consists_of <contract_004/seller_procurator_activity> ,
                        <contract_004/buyer_procurator_activity> ,
                        <contract_004/seller_guarantor_activity> .

<person_broker> cidoc:P14.1_in_the_role_of aat:300025234 .
```

---

## Relationship to Other Properties

### Related GMN Properties

| Property | Relationship | Notes |
|----------|--------------|-------|
| **P70_1_documents_seller** | Parallel | Broker facilitates seller's participation |
| **P70_2_documents_buyer** | Parallel | Broker facilitates buyer's participation |
| **P70_4_documents_sellers_procurator** | Contrasts | Procurator represents seller; broker is neutral |
| **P70_5_documents_buyers_procurator** | Contrasts | Procurator represents buyer; broker is neutral |
| **P70_6_documents_sellers_guarantor** | Contrasts | Guarantor backs seller; broker is neutral |
| **P70_7_documents_buyers_guarantor** | Contrasts | Guarantor backs buyer; broker is neutral |
| **P70_15_documents_witness** | Parallel | Witness observes; broker facilitates |

### Property Hierarchy

```
cidoc:P70_documents (documents)
  ├─ gmn:P70_1_documents_seller
  ├─ gmn:P70_2_documents_buyer
  ├─ gmn:P70_4_documents_sellers_procurator
  ├─ gmn:P70_5_documents_buyers_procurator
  ├─ gmn:P70_6_documents_sellers_guarantor
  ├─ gmn:P70_7_documents_buyers_guarantor
  └─ gmn:P70_8_documents_broker  ← This property
```

### Structural Comparison

| Property | CIDOC Path | Has P17? | Role Location |
|----------|-----------|----------|---------------|
| **P70_8 (broker)** | P70 > E8 > P14 > E21 | No | Direct to acquisition |
| **P70_4 (seller proc.)** | P70 > E8 > P9 > E7 > P14 > E21 | Yes | Via activity to seller |
| **P70_6 (seller guar.)** | P70 > E8 > P9 > E7 > P14 > E21 | Yes | Via activity to seller |

### Semantic Distinctions

**Broker vs. Procurator**:
- **Authority**: Procurator has legal authority; broker does not
- **Representation**: Procurator represents one party; broker serves both
- **Structure**: Procurator needs P17 link; broker does not
- **Commission**: Both may receive fees, but broker's is standard

**Broker vs. Guarantor**:
- **Function**: Guarantor provides security; broker facilitates agreement
- **Risk**: Guarantor assumes risk; broker does not
- **Payment**: Guarantor rarely paid; broker typically receives commission
- **Timing**: Guarantor involved if default; broker only at transaction

**Broker vs. Witness**:
- **Role**: Witness observes; broker actively facilitates
- **Expertise**: Broker has market knowledge; witness may not
- **Commission**: Broker paid; witness usually not
- **Authority**: Neither has legal authority

---

## Compliance and Standards

### CIDOC-CRM Compliance

This property and its transformation comply with:
- CIDOC-CRM version 7.1.3
- P70_documents property definition
- P14_carried_out_by property definition
- E8_Acquisition event model
- P14.1_in_the_role_of property for role qualification

### Linked Open Data Standards

- Uses Getty AAT for role types
- Follows RDF/OWL best practices
- Compatible with JSON-LD context
- Supports SPARQL querying

### Interoperability

The property supports integration with:
- ResearchSpace
- Metaphacts
- Other CIDOC-CRM-compliant systems
- SPARQL endpoints
- Linked Data platforms

---

## Query Examples

### SPARQL: Find All Brokers

```sparql
PREFIX gmn: <http://example.org/gmn#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/page/aat/>

SELECT ?contract ?broker ?brokerName
WHERE {
    ?contract a gmn:E31_2_Sales_Contract ;
        cidoc:P70_documents ?acquisition .
    ?acquisition cidoc:P14_carried_out_by ?broker .
    ?broker cidoc:P14.1_in_the_role_of aat:300025234 ;
        rdfs:label ?brokerName .
}
```

### SPARQL: Contracts with Multiple Brokers

```sparql
SELECT ?contract (COUNT(?broker) AS ?brokerCount)
WHERE {
    ?contract a gmn:E31_2_Sales_Contract ;
        cidoc:P70_documents ?acquisition .
    ?acquisition cidoc:P14_carried_out_by ?broker .
    ?broker cidoc:P14.1_in_the_role_of aat:300025234 .
}
GROUP BY ?contract
HAVING (COUNT(?broker) > 1)
```

### SPARQL: Broker Activity Statistics

```sparql
SELECT ?broker ?brokerName (COUNT(?contract) AS ?contractCount)
WHERE {
    ?contract a gmn:E31_2_Sales_Contract ;
        cidoc:P70_documents ?acquisition .
    ?acquisition cidoc:P14_carried_out_by ?broker .
    ?broker cidoc:P14.1_in_the_role_of aat:300025234 ;
        rdfs:label ?brokerName .
}
GROUP BY ?broker ?brokerName
ORDER BY DESC(?contractCount)
```

---

## References

### CIDOC-CRM Documentation
- E8 Acquisition: http://www.cidoc-crm.org/Entity/e8-acquisition/version-7.1.3
- P14 carried out by: http://www.cidoc-crm.org/Property/p14-carried-out-by/version-7.1.3
- P70 documents: http://www.cidoc-crm.org/Property/p70-documents/version-7.1.3

### Getty AAT
- Brokers (people): http://vocab.getty.edu/page/aat/300025234

### Related Standards
- RDF Schema: https://www.w3.org/TR/rdf-schema/
- OWL 2: https://www.w3.org/TR/owl2-overview/
- Dublin Core: http://purl.org/dc/terms/

---

## Appendix: Complete Example

### Full Contract with Broker

```turtle
@prefix gmn: <http://example.org/gmn#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix aat: <http://vocab.getty.edu/page/aat/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Contract Document
<contract_example_001> a gmn:E31_2_Sales_Contract ;
    rdfs:label "Sale of House in Via Nova, 1345-03-15" ;
    cidoc:P70_documents <contract_example_001/acquisition> ;
    cidoc:P94i_was_created_by <contract_example_001/creation> .

# Acquisition Event
<contract_example_001/acquisition> a cidoc:E8_Acquisition ;
    rdfs:label "Acquisition documented in contract of 1345-03-15" ;
    cidoc:P23_transferred_title_from <person_pietro_seller> ;
    cidoc:P22_transferred_title_to <person_antonio_buyer> ;
    cidoc:P14_carried_out_by <person_giovanni_broker> ;
    cidoc:P24_transferred_title_of <house_via_nova> .

# Broker
<person_giovanni_broker> a cidoc:E21_Person ;
    rdfs:label "Giovanni de Sancto Petro, sensale" ;
    cidoc:P14.1_in_the_role_of aat:300025234 .

# Seller
<person_pietro_seller> a cidoc:E21_Person ;
    rdfs:label "Pietro de Mari, seller" .

# Buyer
<person_antonio_buyer> a cidoc:E21_Person ;
    rdfs:label "Antonio de Nigro, buyer" .

# Property
<house_via_nova> a cidoc:E18_Physical_Thing ;
    rdfs:label "House in Via Nova" .

# Document Creation
<contract_example_001/creation> a cidoc:E65_Creation ;
    cidoc:P14_carried_out_by <notary_oberto> ;
    cidoc:P4_has_time-span <date_1345_03_15> .

<notary_oberto> a cidoc:E21_Person ;
    rdfs:label "Obertus de Placentia, notarius" .

<date_1345_03_15> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1345-03-15"^^xsd:date .
```

---

## Version History

- **1.0** (2025-10-27): Complete semantic documentation
- Property created: 2025-10-17
- Last updated: 2025-10-27
