# Documents Sale Price Currency - Semantic Documentation
## gmn:P70_17_documents_sale_price_currency

---

## Overview

The `gmn:P70_17_documents_sale_price_currency` property is a simplified convenience property for documenting the currency unit of a sale price in medieval Genoese sales contracts. It works in conjunction with `gmn:P70_16_documents_sale_price_amount` to provide complete monetary value information.

---

## Property Specification

### Basic Information

| Attribute | Value |
|-----------|-------|
| **IRI** | `gmn:P70_17_documents_sale_price_currency` |
| **Label** | "P70.17 documents sale price currency"@en |
| **Property Type** | `owl:ObjectProperty`, `rdf:Property` |
| **Domain** | `gmn:E31_2_Sales_Contract` |
| **Range** | `cidoc:E98_Currency` |
| **Superproperty** | `cidoc:P70_documents` |
| **Created** | 2025-10-17 |

### Related Properties

- **P70.16** - Documents sale price amount (companion property for numeric value)
- **cidoc:P70_documents** - Parent property linking documents to events
- **cidoc:P177_assigned_property_of_type** - Links acquisition to monetary amount
- **cidoc:P180_has_currency** - Target CIDOC-CRM property for currency

---

## Semantic Definition

### Purpose

This property serves as a data entry shortcut for expressing the currency type used in documenting a sale price. Instead of requiring data entry staff to create the full CIDOC-CRM chain of entities and relationships, they can simply attach a currency reference directly to the sales contract document.

### CIDOC-CRM Compliance

The property is transformed into full CIDOC-CRM compliance through the following path:

```
E31_Document (Sales Contract)
  |
  ├─ P70_documents ──→ E8_Acquisition (Sale Event)
       |
       └─ P177_assigned_property_of_type ──→ E97_Monetary_Amount (Price)
            |
            └─ P180_has_currency ──→ E98_Currency (Currency Type)
```

### Conceptual Model

```
┌─────────────────────────────┐
│   E31_2_Sales_Contract      │
│   (Document)                │
└──────────┬──────────────────┘
           │ P70_documents
           ▼
┌─────────────────────────────┐
│   E8_Acquisition            │
│   (Sale Transaction)        │
└──────────┬──────────────────┘
           │ P177_assigned_property_of_type
           ▼
┌─────────────────────────────┐
│   E97_Monetary_Amount       │────── P181_has_amount (from P70.16)
│   (Price Amount)            │
└──────────┬──────────────────┘
           │ P180_has_currency
           ▼
┌─────────────────────────────┐
│   E98_Currency              │
│   (e.g., Lira Genovese)     │
└─────────────────────────────┘
```

---

## CIDOC-CRM Mapping

### Entity Descriptions

#### E31_Document (Sales Contract)
**CIDOC-CRM Definition:** Information Carrier - instances of E31_Document are identified information carriers.

**GMN Usage:** Represents the physical notarial document recording the sales transaction. In our case, specifically a sales contract (`gmn:E31_2_Sales_Contract`).

**Properties:**
- `@id`: URI of the document
- `@type`: `gmn:E31_2_Sales_Contract`
- Contains the simplified currency property before transformation

#### E8_Acquisition (Sale Event)
**CIDOC-CRM Definition:** Acquisition Event - comprises transfers of legal ownership from one or more instances of E39 Actor to one or more other instances of E39 Actor.

**GMN Usage:** Represents the actual sale transaction documented by the contract. This is the event during which ownership of property transferred from seller to buyer.

**Properties:**
- `@id`: Generated as `{document_uri}/acquisition`
- `@type`: `cidoc:E8_Acquisition`
- Links to seller, buyer, transferred property, and monetary amount

#### E97_Monetary_Amount
**CIDOC-CRM Definition:** Monetary Amount - a quantifiable monetary value expressed in a particular currency.

**GMN Usage:** Represents the complete price information including both the numeric amount and currency type. This entity is shared between P70.16 (amount) and P70.17 (currency) transformations.

**Properties:**
- `@id`: Generated as `{acquisition_uri}/monetary_amount`
- `@type`: `cidoc:E97_Monetary_Amount`
- `cidoc:P180_has_currency_amount`: Numeric value (from P70.16)
- `cidoc:P180_has_currency`: Currency entity (from P70.17)

**Note:** The property name for amount may vary; some implementations use `P181_has_amount`.

#### E98_Currency
**CIDOC-CRM Definition:** Currency - type of monetary unit used for expressing a monetary amount.

**GMN Usage:** Represents the specific currency type used in the transaction (e.g., Genoese lira, florin, ducat). Should reference controlled vocabulary terms when possible.

**Properties:**
- `@id`: URI reference to currency entity
- `@type`: `cidoc:E98_Currency`
- Additional properties: `rdfs:label`, `skos:prefLabel`, etc.

---

## Property Chain Explanation

### Path Breakdown

1. **E31_Document → E8_Acquisition** (via P70_documents)
   - The document records or documents the acquisition event
   - One document can document one acquisition (typically)

2. **E8_Acquisition → E97_Monetary_Amount** (via P177_assigned_property_of_type)
   - The acquisition has an associated monetary value (the price)
   - This property "assigns" the monetary amount as a property of the acquisition

3. **E97_Monetary_Amount → E98_Currency** (via P180_has_currency)
   - The monetary amount is expressed in a specific currency
   - Links the amount to its currency type

### Why This Structure?

**Separation of Concerns:**
- The document (E31) is separate from the event it records (E8)
- The price (E97) is a property of the acquisition, not the document
- The currency (E98) is a type classifier for the amount

**Semantic Precision:**
- Clearly distinguishes between documentation and documented event
- Separates monetary amount from its measurement unit
- Enables queries about prices in specific currencies

**Data Reusability:**
- E8_Acquisition can be referenced by multiple documents
- E97_Monetary_Amount can be compared across transactions
- E98_Currency entities can be reused across all monetary amounts

---

## Transformation Examples

### Example 1: Simple Currency Documentation

**Input (Simplified):**
```turtle
@prefix gmn: <http://genoese-merchants.net/ontology/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/contract/1455_05_10_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_17_documents_sale_price_currency <http://vocab.example.org/currency/lira_genovese> .
```

**Output (CIDOC-CRM Compliant):**
```turtle
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

<http://example.org/contract/1455_05_10_001> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <http://example.org/contract/1455_05_10_001/acquisition> .

<http://example.org/contract/1455_05_10_001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P177_assigned_property_of_type <http://example.org/contract/1455_05_10_001/acquisition/monetary_amount> .

<http://example.org/contract/1455_05_10_001/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P180_has_currency <http://vocab.example.org/currency/lira_genovese> .

<http://vocab.example.org/currency/lira_genovese> a cidoc:E98_Currency .
```

### Example 2: Complete Price with Currency

**Input (Simplified):**
```turtle
<http://example.org/contract/1460_03_15_042> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <http://example.org/person/giovanni_doria> ;
    gmn:P70_2_documents_buyer <http://example.org/person/raffaele_sacco> ;
    gmn:P70_3_documents_transfer_of <http://example.org/property/house_piazza_banchi_12> ;
    gmn:P70_16_documents_sale_price_amount "350.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <http://vocab.example.org/currency/lira_genovese> .
```

**Output (CIDOC-CRM Compliant):**
```turtle
<http://example.org/contract/1460_03_15_042> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <http://example.org/contract/1460_03_15_042/acquisition> .

<http://example.org/contract/1460_03_15_042/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <http://example.org/person/giovanni_doria> ;
    cidoc:P22_transferred_title_to <http://example.org/person/raffaele_sacco> ;
    cidoc:P24_transferred_title_of <http://example.org/property/house_piazza_banchi_12> ;
    cidoc:P177_assigned_property_of_type <http://example.org/contract/1460_03_15_042/acquisition/monetary_amount> .

<http://example.org/contract/1460_03_15_042/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P180_has_currency_amount "350.00"^^xsd:decimal ;
    cidoc:P180_has_currency <http://vocab.example.org/currency/lira_genovese> .

<http://vocab.example.org/currency/lira_genovese> a cidoc:E98_Currency ;
    rdfs:label "Genoese Lira"@en .
```

### Example 3: Currency with Additional Metadata

**Input (Simplified with structured currency):**
```turtle
<http://example.org/contract/1458_11_20_123> a gmn:E31_2_Sales_Contract ;
    gmn:P70_16_documents_sale_price_amount "1200.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency [
        a cidoc:E98_Currency ;
        rdfs:label "Florin"@en ;
        rdfs:label "Fiorino"@it ;
        skos:broader <http://vocab.example.org/currency/gold_coins>
    ] .
```

**Output (CIDOC-CRM Compliant):**
```turtle
<http://example.org/contract/1458_11_20_123> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <http://example.org/contract/1458_11_20_123/acquisition> .

<http://example.org/contract/1458_11_20_123/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P177_assigned_property_of_type <http://example.org/contract/1458_11_20_123/acquisition/monetary_amount> .

<http://example.org/contract/1458_11_20_123/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P180_has_currency_amount "1200.00"^^xsd:decimal ;
    cidoc:P180_has_currency [
        a cidoc:E98_Currency ;
        rdfs:label "Florin"@en ;
        rdfs:label "Fiorino"@it ;
        skos:broader <http://vocab.example.org/currency/gold_coins>
    ] .
```

### Example 4: Multiple Transactions with Same Currency

**Input (Multiple contracts using lira):**
```turtle
<http://example.org/contract/1455_01_10_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_16_documents_sale_price_amount "100.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <http://vocab.example.org/currency/lira_genovese> .

<http://example.org/contract/1455_01_15_002> a gmn:E31_2_Sales_Contract ;
    gmn:P70_16_documents_sale_price_amount "250.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <http://vocab.example.org/currency/lira_genovese> .
```

**Output (Both reference same E98_Currency entity):**
```turtle
# Contract 1
<http://example.org/contract/1455_01_10_001> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <http://example.org/contract/1455_01_10_001/acquisition> .

<http://example.org/contract/1455_01_10_001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P177_assigned_property_of_type <http://example.org/contract/1455_01_10_001/acquisition/monetary_amount> .

<http://example.org/contract/1455_01_10_001/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P180_has_currency_amount "100.00"^^xsd:decimal ;
    cidoc:P180_has_currency <http://vocab.example.org/currency/lira_genovese> .

# Contract 2
<http://example.org/contract/1455_01_15_002> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <http://example.org/contract/1455_01_15_002/acquisition> .

<http://example.org/contract/1455_01_15_002/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P177_assigned_property_of_type <http://example.org/contract/1455_01_15_002/acquisition/monetary_amount> .

<http://example.org/contract/1455_01_15_002/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P180_has_currency_amount "250.00"^^xsd:decimal ;
    cidoc:P180_has_currency <http://vocab.example.org/currency/lira_genovese> .

# Shared currency entity
<http://vocab.example.org/currency/lira_genovese> a cidoc:E98_Currency ;
    rdfs:label "Genoese Lira"@en ;
    rdfs:label "Lira Genovese"@it .
```

---

## Historical Currency Context

### Common Genoese Currencies

| Currency | Latin Name | Description |
|----------|-----------|-------------|
| **Lira Genovese** | libra ianuensis | Genoese pound, primary unit of account |
| **Florin** | florenus | Gold coin, used for large transactions |
| **Ducat** | ducatus | Venetian gold coin, widely accepted |
| **Soldo** | solidus | Subdivision of lira (20 soldi = 1 lira) |
| **Denaro** | denarius | Smallest unit (12 denari = 1 soldo) |

### Currency Relationships

```
1 Lira Genovese = 20 Soldi = 240 Denari
1 Florin ≈ 25-30 Soldi (varied by period)
1 Ducat ≈ 28-32 Soldi (varied by period)
```

### Recommended URI Pattern

```
http://vocab.example.org/currency/{currency_type}

Examples:
- http://vocab.example.org/currency/lira_genovese
- http://vocab.example.org/currency/florin
- http://vocab.example.org/currency/ducat
- http://vocab.example.org/currency/soldo
- http://vocab.example.org/currency/denaro
```

---

## Comparison with Related Properties

### P70.16 vs P70.17

| Aspect | P70.16 (Amount) | P70.17 (Currency) |
|--------|----------------|-------------------|
| **Purpose** | Numeric value | Currency type |
| **Property Type** | DatatypeProperty | ObjectProperty |
| **Range** | xsd:decimal | E98_Currency |
| **CIDOC Target** | P180_has_currency_amount | P180_has_currency |
| **Example Value** | "350.00"^^xsd:decimal | <lira_genovese> |

### Shared Structure

Both properties:
- Share the same E8_Acquisition node
- Contribute to the same E97_Monetary_Amount entity
- Are simplified shortcuts for data entry
- Get transformed to full CIDOC-CRM structure

---

## Query Examples

### SPARQL Query 1: Find All Sales in Lira Genovese

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://genoese-merchants.net/ontology/>

SELECT ?contract ?amount
WHERE {
    ?contract a gmn:E31_2_Sales_Contract ;
              cidoc:P70_documents ?acquisition .
    
    ?acquisition cidoc:P177_assigned_property_of_type ?monetary .
    
    ?monetary cidoc:P180_has_currency <http://vocab.example.org/currency/lira_genovese> ;
              cidoc:P180_has_currency_amount ?amount .
}
ORDER BY DESC(?amount)
```

### SPARQL Query 2: Currency Distribution Analysis

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://genoese-merchants.net/ontology/>

SELECT ?currency (COUNT(?contract) as ?count) (AVG(?amount) as ?avg_price)
WHERE {
    ?contract a gmn:E31_2_Sales_Contract ;
              cidoc:P70_documents ?acquisition .
    
    ?acquisition cidoc:P177_assigned_property_of_type ?monetary .
    
    ?monetary cidoc:P180_has_currency ?currency ;
              cidoc:P180_has_currency_amount ?amount .
}
GROUP BY ?currency
ORDER BY DESC(?count)
```

### SPARQL Query 3: Price Comparison Across Currencies

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://genoese-merchants.net/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?contract ?amount ?currency_label
WHERE {
    ?contract a gmn:E31_2_Sales_Contract ;
              cidoc:P70_documents ?acquisition .
    
    ?acquisition cidoc:P177_assigned_property_of_type ?monetary .
    
    ?monetary cidoc:P180_has_currency ?currency ;
              cidoc:P180_has_currency_amount ?amount .
    
    ?currency rdfs:label ?currency_label .
    
    FILTER(?amount > 1000)
}
ORDER BY DESC(?amount)
```

---

## Validation Rules

### Required Structure

After transformation, the following structure must exist:

```turtle
?document a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents ?acquisition .

?acquisition a cidoc:E8_Acquisition ;
    cidoc:P177_assigned_property_of_type ?monetary .

?monetary a cidoc:E97_Monetary_Amount ;
    cidoc:P180_has_currency ?currency .

?currency a cidoc:E98_Currency .
```

### Validation Constraints

1. **Domain Constraint**: Property must only be used with `gmn:E31_2_Sales_Contract`
2. **Range Constraint**: Value must be or resolve to `cidoc:E98_Currency`
3. **Cardinality**: Typically one currency per sale (though format allows multiple)
4. **URI Validity**: Currency references should be valid URIs or structured objects
5. **Type Assignment**: Currency entities must have type `cidoc:E98_Currency`

---

## Implementation Notes

### Coordination with P70.16

The transformation must handle two scenarios:

**Scenario A: P70.16 Transformed First**
- E8_Acquisition already exists
- E97_Monetary_Amount already exists with amount
- P70.17 adds currency to existing E97

**Scenario B: P70.17 Transformed First**
- Creates E8_Acquisition if needed
- Creates E97_Monetary_Amount if needed
- P70.16 will add amount to same E97

The transformation code handles both scenarios by checking for existing nodes before creating new ones.

### URI Generation

**Pattern:**
```
{document_uri}/acquisition/monetary_amount
```

**Example:**
```
http://example.org/contract/1455_05_10_001/acquisition/monetary_amount
```

This ensures consistent URIs regardless of transformation order.

---

## Future Enhancements

### Potential Additions

1. **Currency Exchange Rates**: Link E98_Currency to historical exchange rates
2. **Measurement Uncertainty**: Model uncertainty in currency identification
3. **Multiple Currencies**: Handle transactions involving multiple currency types
4. **Currency Evolution**: Track changes in currency systems over time
5. **Purchasing Power**: Link to economic purchasing power data

### Research Applications

- Economic history analysis
- Currency circulation studies
- Price trend analysis
- Regional economic patterns
- Merchant network analysis based on currency preferences

---

## References

### CIDOC-CRM Documentation
- E31_Document: http://www.cidoc-crm.org/Entity/e31-document/
- E8_Acquisition: http://www.cidoc-crm.org/Entity/e8-acquisition/
- E97_Monetary_Amount: http://www.cidoc-crm.org/Entity/e97-monetary-amount/
- E98_Currency: http://www.cidoc-crm.org/Entity/e98-currency/
- P70_documents: http://www.cidoc-crm.org/Property/p70-documents/
- P177_assigned_property_of_type: http://www.cidoc-crm.org/Property/p177-assigned-property-of-type/
- P180_has_currency: http://www.cidoc-crm.org/Property/p180-has-currency/

### Related Standards
- ISO 4217 (Modern currency codes - for reference)
- RDF Schema: https://www.w3.org/TR/rdf-schema/
- OWL Web Ontology Language: https://www.w3.org/TR/owl2-overview/

---

*This semantic documentation provides the conceptual foundation for understanding and implementing the documents sale price currency property in the GMN ontology.*
