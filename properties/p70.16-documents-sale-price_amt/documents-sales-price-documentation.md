# Documents Sale Price Amount - Ontology Documentation

## Table of Contents
1. [Property Overview](#property-overview)
2. [Semantic Definition](#semantic-definition)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Property Specifications](#property-specifications)
5. [Usage Guidelines](#usage-guidelines)
6. [Transformation Examples](#transformation-examples)
7. [Relationship to Other Properties](#relationship-to-other-properties)
8. [Historical Context](#historical-context)

## Property Overview

### Basic Information

**URI**: `gmn:P70_16_documents_sale_price_amount`  
**Label**: "P70.16 documents sale price amount" (English)  
**Property Type**: owl:DatatypeProperty, rdf:Property  
**Domain**: `gmn:E31_2_Sales_Contract`  
**Range**: `xsd:decimal`  
**Created**: 2025-10-17  
**Status**: Active

### Purpose

The `gmn:P70_16_documents_sale_price_amount` property provides a simplified mechanism for expressing the numeric monetary amount of a sale price documented in historical sales contracts. It serves as a "shortcut" property that simplifies data entry while ensuring transformation to full CIDOC-CRM compliant structures.

This property is specifically designed for documenting economic information from Genoese merchant contracts, where precise monetary amounts are crucial for historical economic research and analysis.

### Design Philosophy

1. **Simplification**: Allows direct specification of decimal amounts without requiring users to manually create E8_Acquisition, E97_Monetary_Amount, and associated property chains
2. **Precision**: Uses xsd:decimal to preserve exact monetary values as recorded in historical documents
3. **Complementary Design**: Works in tandem with P70_17 (currency) to express complete monetary values
4. **CIDOC-CRM Compliance**: Transforms to semantically rich CIDOC-CRM structures for formal ontological compliance
5. **Data Entry Focus**: Optimized for practical data entry workflows while maintaining semantic rigor

## Semantic Definition

### Natural Language Definition

This property associates a sales contract document (E31_2_Sales_Contract) with the numeric monetary amount of the sale price documented in that contract. The value represents the quantity of currency units (e.g., 1500.50 lira) involved in the documented transaction.

### Formal Definition

```
gmn:P70_16_documents_sale_price_amount ⊆ cidoc:P70_documents

Domain: gmn:E31_2_Sales_Contract
Range: xsd:decimal

For any instance x of gmn:E31_2_Sales_Contract and any decimal value y,
if (x, y) ∈ gmn:P70_16_documents_sale_price_amount, then:
  ∃ a (acquisition), ∃ m (monetary_amount) such that:
    (x, a) ∈ cidoc:P70_documents ∧
    a ∈ cidoc:E8_Acquisition ∧
    (a, m) ∈ cidoc:P177_assigned_property_of_type ∧
    m ∈ cidoc:E97_Monetary_Amount ∧
    (m, y) ∈ cidoc:P181_has_amount
```

### Scope and Constraints

**In Scope**:
- Numeric amounts recorded in sales contracts
- Decimal values representing monetary quantities
- Prices expressed in any historical currency
- Partial payments or deposit amounts when documented separately
- Amounts expressed with decimal precision

**Out of Scope**:
- Currency types (use P70_17 for this)
- Non-monetary valuations
- Estimated or inferred prices not documented in the contract
- Prices for non-sales transactions (use appropriate properties for donations, dowries, etc.)

## CIDOC-CRM Mapping

### Full CIDOC-CRM Path

The property represents this complete path in CIDOC-CRM:

```
E31_Document [Sales Contract]
  └─ P70_documents → E8_Acquisition [Sale Transaction]
      └─ P177_assigned_property_of_type → E97_Monetary_Amount [Price Amount]
          └─ P181_has_amount → xsd:decimal [Numeric Value]
```

### Component Breakdown

#### E31_Document (Sales Contract)
- The source document containing the sale information
- Specific subclass: gmn:E31_2_Sales_Contract
- Represents the notarial contract or other documentary evidence

#### P70_documents
- CIDOC-CRM property linking documents to events/activities
- Indicates that the document provides evidence for the acquisition
- Scope note: "documents instances of E5 Event"

#### E8_Acquisition
- The central event class for ownership transfers
- Represents the historical sale transaction
- Contains seller, buyer, object, and monetary information
- Scope note: "the acquisition of physical things and their transfer of legal ownership"

#### P177_assigned_property_of_type
- Links the acquisition to its monetary valuation
- Scope note: "allows the assignment of a property to an instance of E70 Thing"
- Used to specify the monetary amount as a property of the acquisition

#### E97_Monetary_Amount
- Represents a monetary value as a cultural construct
- Combines numeric amount with currency type
- Scope note: "monetary value with a currency"
- Can include both amount (P181) and currency (P180) properties

#### P181_has_amount
- Links the monetary amount to its numeric value
- Range: xsd:decimal (for precision)
- Scope note: "allows the quantification of a monetary amount"

### Why This Structure?

The CIDOC-CRM structure separates concerns:

1. **E8_Acquisition**: Models the ownership transfer event
2. **E97_Monetary_Amount**: Models the monetary value as a distinct entity
3. **P181_has_amount**: Links to the numeric quantity
4. **P180_has_currency** (via P70_17): Links to the currency type

This separation allows:
- Multiple monetary amounts for complex transactions
- Reuse of currency entities across contracts
- Precise semantic modeling of economic data
- Clear distinction between amount and currency

## Property Specifications

### RDF/OWL Specification

```turtle
gmn:P70_16_documents_sale_price_amount
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P70.16 documents sale price amount"@en ;
    rdfs:comment "Simplified property for expressing the monetary amount of the sale price documented in a sales contract. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P177_assigned_property_of_type > E97_Monetary_Amount > P181_has_amount > xsd:decimal. This property captures only the numeric value; use P70.17 to specify the currency. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The value should be a decimal number representing the quantity in the specified currency."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range xsd:decimal ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P177_assigned_property_of_type, cidoc:P181_has_amount .
```

### Property Characteristics

**Type**: Datatype Property
- Links an instance to a literal value (decimal)
- Not an object property (which would link to another resource)

**Cardinality**: 
- Minimum: 0 (optional - not all contracts document prices)
- Maximum: Unbounded (theoretically, though typically 1)
- Typical: 1 (one price per contract)

**Functional**: No
- A contract could theoretically have multiple price amounts
- However, best practice is one amount per contract
- Multiple amounts may indicate need for separate transaction modeling

**Inverse Functional**: No
- Multiple contracts can have the same price amount

### Data Type Requirements

**xsd:decimal**:
- Exact representation of decimal numbers
- No floating-point rounding errors
- Preserves precision as recorded in source
- Examples: "100", "1500.50", "0.25", "1234567.89"

**NOT xsd:float or xsd:double**:
- These can introduce rounding errors
- Inappropriate for currency values
- May lose precision in computation

**NOT xsd:integer**:
- Many historical prices include fractional currency units
- Limits precision unnecessarily

**Format Guidelines**:
- Use decimal point (not comma)
- No thousands separators
- No currency symbols
- Examples: "1500.50" ✓, "1,500.50" ✗, "€1500" ✗

## Usage Guidelines

### When to Use This Property

Use `gmn:P70_16_documents_sale_price_amount` when:

1. **Documented Price**: The sales contract explicitly states a monetary amount
2. **Primary Price**: This is the main sale price (not secondary fees or taxes)
3. **Numeric Value**: You have a specific decimal number to record
4. **Sales Context**: The document is a sales contract (E31_2_Sales_Contract)

### When NOT to Use This Property

Do not use this property when:

1. **No Price Stated**: The contract doesn't mention a specific amount
2. **Price Implied**: The price is inferred but not explicitly documented
3. **Non-Sales**: The transaction is not a sale (use appropriate property for donations, dowries, etc.)
4. **Currency Only**: You only have currency information (use P70_17 alone)
5. **Complex Pricing**: Multiple component prices that need separate modeling

### Best Practices

#### Always Use with P70_17
```turtle
# Good: Amount and currency together
<sale001> gmn:P70_16_documents_sale_price_amount "1500.50"^^xsd:decimal ;
          gmn:P70_17_documents_sale_price_currency <lira_genovese> .

# Poor: Amount without currency
<sale002> gmn:P70_16_documents_sale_price_amount "1500.50"^^xsd:decimal .
```

#### Preserve Source Precision
```turtle
# Good: Preserve decimals as recorded
<sale003> gmn:P70_16_documents_sale_price_amount "1234.567"^^xsd:decimal .

# Poor: Unnecessary rounding
<sale004> gmn:P70_16_documents_sale_price_amount "1235"^^xsd:decimal .
```

#### Record Exact Values
```turtle
# Good: Exact value from source
<sale005> gmn:P70_16_documents_sale_price_amount "1500.00"^^xsd:decimal .

# Poor: Approximation
<sale006> gmn:P70_16_documents_sale_price_amount "1500"^^xsd:decimal .  # Missing .00
```

#### Handle Complex Pricing Separately
If a contract has multiple price components (deposit, final payment, etc.), consider:

1. **Option A**: Model as separate transactions
2. **Option B**: Use only the total if that's what's most relevant
3. **Option C**: Add a note property explaining the structure

```turtle
# Complex pricing - document the total
<sale007> gmn:P70_16_documents_sale_price_amount "2000.00"^^xsd:decimal ;
          rdfs:comment "Total price: 500 deposit + 1500 on delivery"@en .
```

### Common Patterns

#### Standard Sale
```turtle
<contract_1450_03_15> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <giovanni_merchant> ;
    gmn:P70_2_documents_buyer <marco_banker> ;
    gmn:P70_3_documents_transfer_of <house_genoa> ;
    gmn:P70_16_documents_sale_price_amount "2500.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <lira_genovese> .
```

#### Sale with Fractional Currency
```turtle
<contract_1455_07_20> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <antonio_silk_merchant> ;
    gmn:P70_2_documents_buyer <francesco_trader> ;
    gmn:P70_3_documents_transfer_of <silk_bales> ;
    gmn:P70_16_documents_sale_price_amount "345.75"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <florin> .
```

#### Large Transaction
```turtle
<contract_1460_12_05> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <spinola_family> ;
    gmn:P70_2_documents_buyer <doria_family> ;
    gmn:P70_3_documents_transfer_of <palazzo_genoa> ;
    gmn:P70_16_documents_sale_price_amount "50000.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <lira_genovese> .
```

## Transformation Examples

### Example 1: Basic Sale Price

**Input (GMN Shortcut)**:
```turtle
<sale_1450_01_15> a gmn:E31_2_Sales_Contract ;
    gmn:P1_1_has_name "Sale of House on Via del Campo"@en ;
    gmn:P70_1_documents_seller <andrea_rossi> ;
    gmn:P70_2_documents_buyer <paolo_bianchi> ;
    gmn:P70_3_documents_transfer_of <house_via_campo_12> ;
    gmn:P70_16_documents_sale_price_amount "1500.50"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <lira_genovese> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<sale_1450_01_15> a gmn:E31_2_Sales_Contract ;
    cidoc:P1_is_identified_by <sale_1450_01_15/appellation/1> ;
    cidoc:P70_documents <sale_1450_01_15/acquisition> .

<sale_1450_01_15/appellation/1> a cidoc:E41_Appellation ;
    cidoc:P190_has_symbolic_content "Sale of House on Via del Campo"@en .

<sale_1450_01_15/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <andrea_rossi> ;
    cidoc:P22_transferred_title_to <paolo_bianchi> ;
    cidoc:P24_transferred_title_of <house_via_campo_12> ;
    cidoc:P177_assigned_property_of_type <sale_1450_01_15/acquisition/monetary_amount> .

<sale_1450_01_15/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P181_has_amount "1500.50"^^xsd:decimal ;
    cidoc:P180_has_currency <lira_genovese> .

<lira_genovese> a cidoc:E98_Currency .
```

**Explanation**:
1. The sales contract document (E31_2) remains the root entity
2. An E8_Acquisition event is created to model the ownership transfer
3. The acquisition links to seller, buyer, and object
4. An E97_Monetary_Amount entity captures the complete monetary value
5. P181_has_amount contains the numeric value from P70_16
6. P180_has_currency contains the currency from P70_17

### Example 2: Price Without Currency (Not Recommended)

**Input**:
```turtle
<sale_1452_06_10> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <giuseppe_merchant> ;
    gmn:P70_2_documents_buyer <lorenzo_banker> ;
    gmn:P70_3_documents_transfer_of <vineyard_albaro> ;
    gmn:P70_16_documents_sale_price_amount "3000.00"^^xsd:decimal .
```

**Output**:
```turtle
<sale_1452_06_10> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <sale_1452_06_10/acquisition> .

<sale_1452_06_10/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <giuseppe_merchant> ;
    cidoc:P22_transferred_title_to <lorenzo_banker> ;
    cidoc:P24_transferred_title_of <vineyard_albaro> ;
    cidoc:P177_assigned_property_of_type <sale_1452_06_10/acquisition/monetary_amount> .

<sale_1452_06_10/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P181_has_amount "3000.00"^^xsd:decimal .
    # Note: Missing P180_has_currency - incomplete monetary amount
```

**Note**: While technically valid, an E97_Monetary_Amount without a currency is incomplete. Best practice is to always specify both amount and currency.

### Example 3: Complex Sale with Multiple Properties

**Input**:
```turtle
<sale_1455_11_20> a gmn:E31_2_Sales_Contract ;
    gmn:P1_1_has_name "Sale of Palazzo Spinola"@en ;
    gmn:P102_1_has_title "Venditio palatii Spinola"@la ;
    gmn:P70_1_documents_seller <giacomo_spinola> ;
    gmn:P70_2_documents_buyer <oberto_doria> ;
    gmn:P70_3_documents_transfer_of <palazzo_piazza_fontane_marose> ;
    gmn:P70_4_documents_sellers_procurator <giovanni_procurator> ;
    gmn:P70_6_documents_sellers_guarantor <antonio_guarantor> ;
    gmn:P70_15_documents_witness <pietro_witness>, <marco_witness> ;
    gmn:P70_16_documents_sale_price_amount "25000.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <lira_genovese> ;
    gmn:P94i_1_was_created_by <notary_basso> ;
    gmn:P94i_2_has_enactment_date "1455-11-20"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <genoa> .
```

**Output** (Partial - showing monetary amount structure):
```turtle
<sale_1455_11_20> a gmn:E31_2_Sales_Contract ;
    cidoc:P1_is_identified_by <sale_1455_11_20/appellation/1> ;
    cidoc:P102_has_title <sale_1455_11_20/title/1> ;
    cidoc:P70_documents <sale_1455_11_20/acquisition> ;
    cidoc:P94i_was_created_by <sale_1455_11_20/creation> .

<sale_1455_11_20/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <giacomo_spinola> ;
    cidoc:P22_transferred_title_to <oberto_doria> ;
    cidoc:P24_transferred_title_of <palazzo_piazza_fontane_marose> ;
    cidoc:P9_consists_of <sale_1455_11_20/acquisition/activity/procurator_...> ,
                         <sale_1455_11_20/acquisition/activity/guarantor_...> ,
                         <sale_1455_11_20/acquisition/activity/witness_...> ;
    cidoc:P177_assigned_property_of_type <sale_1455_11_20/acquisition/monetary_amount> .

<sale_1455_11_20/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P181_has_amount "25000.00"^^xsd:decimal ;
    cidoc:P180_has_currency <lira_genovese> .

# ... other structures for procurator, guarantor, witnesses, creation ...
```

**Explanation**: In complex contracts with many properties, the monetary amount structure remains clean and consistent, embedded within the E8_Acquisition alongside other acquisition details.

### Example 4: Comparison with Related Contract Types

**Sales Contract**:
```turtle
<sale> gmn:P70_16_documents_sale_price_amount "1000.00"^^xsd:decimal .
# → P23_transferred_title_from (seller)
# → P22_transferred_title_to (buyer)
# → Economic exchange
```

**Donation Contract** (using same price properties):
```turtle
<donation> gmn:P70_16_documents_sale_price_amount "1000.00"^^xsd:decimal .
# → P23_transferred_title_from (donor) via P70_32
# → P22_transferred_title_to (donee) via P70_22
# → Documents value for tax/legal purposes
```

**Dowry Contract** (using same price properties):
```turtle
<dowry> gmn:P70_16_documents_sale_price_amount "1000.00"^^xsd:decimal .
# → P23_transferred_title_from (donor) via P70_32
# → P22_transferred_title_to (bride) via P70_22
# → Documents dowry value
```

All three use the same E97_Monetary_Amount structure, but in different legal/social contexts.

## Relationship to Other Properties

### Direct Relationships

#### Complementary: P70_17 (Currency)
- **Relationship**: These two properties work together to form complete monetary values
- **Pattern**: Always use both together when documenting prices
- **Shared Structure**: Both contribute to the same E97_Monetary_Amount entity

```turtle
# P70_16 contributes amount, P70_17 contributes currency
<sale> gmn:P70_16_documents_sale_price_amount "1500.50"^^xsd:decimal ;
       gmn:P70_17_documents_sale_price_currency <lira> .
# Both transform to the same E97_Monetary_Amount
```

#### Parent: P70_documents
- **Relationship**: P70_16 is a subPropertyOf P70_documents
- **Rationale**: The price amount is part of what the document documents
- **Inheritance**: Inherits domain and basic semantics from P70_documents

#### Sibling: Other P70.x Properties
- **P70_1 (seller)**: Who receives the payment
- **P70_2 (buyer)**: Who makes the payment
- **P70_3 (transfer of)**: What is being purchased
- **Context**: All siblings contribute to the E8_Acquisition structure

### Indirect Relationships

#### Temporal Context: P94i_2 (Enactment Date)
```turtle
<sale> gmn:P70_16_documents_sale_price_amount "1000.00"^^xsd:decimal ;
       gmn:P94i_2_has_enactment_date "1450-03-15"^^xsd:date .
# Price is valid at the time of contract enactment
```

#### Spatial Context: P94i_3 (Place of Enactment)
```turtle
<sale> gmn:P70_16_documents_sale_price_amount "1000.00"^^xsd:decimal ;
       gmn:P94i_3_has_place_of_enactment <genoa> .
# Price may vary by location (currency exchange, local economy)
```

#### Documentary Context: P46i_1 (Contained in Register)
```turtle
<sale> gmn:P70_16_documents_sale_price_amount "1000.00"^^xsd:decimal ;
       gmn:P46i_1_is_contained_in <notarial_register_1450> .
# Links to archival context
```

### Property Hierarchy

```
cidoc:P70_documents (documents events)
  └─ gmn:P70_16_documents_sale_price_amount (documents amount)
  └─ gmn:P70_17_documents_sale_price_currency (documents currency)
  └─ gmn:P70_1_documents_seller (documents seller)
  └─ gmn:P70_2_documents_buyer (documents buyer)
  └─ gmn:P70_3_documents_transfer_of (documents object)
  └─ ... (other P70.x properties)
```

## Historical Context

### Genoese Monetary System

The prices documented using P70_16 reflect the historical monetary system of Genoa:

**Common Currencies**:
- **Lira Genovese**: Primary accounting unit
- **Florin**: Gold coin used in international trade
- **Ducat**: Venetian gold coin also used in Genoa
- **Soldo**: Subdivision of lira (1 lira = 20 soldi)
- **Denaro**: Further subdivision (1 soldo = 12 denari)

**Decimal Representation**:
```
15.50 lire = 15 lire, 10 soldi
123.75 lire = 123 lire, 15 soldi
1000.00 lire = 1000 lire exactly
```

### Price Ranges in Historical Context

Typical price ranges for different types of property:

**Real Estate**:
- Small house: 500-2000 lire
- Palazzo: 10,000-100,000 lire
- Vineyard: 1,000-5,000 lire
- Shop: 2,000-10,000 lire

**Moveable Property**:
- Silk bales: 50-500 lire
- Cloth: 10-100 lire
- Books: 5-50 lire
- Ships: 5,000-50,000 lire

**Note**: These are approximate ranges and varied by period, location, and quality.

### Research Implications

The precise recording of monetary amounts enables:

1. **Economic Analysis**: Tracking price changes over time
2. **Market Studies**: Comparing prices across different types of property
3. **Social Network Analysis**: Understanding wealth distribution
4. **Currency Studies**: Analyzing exchange rates and monetary policy
5. **Family History**: Documenting economic status of individuals and families

### Data Quality Considerations

When entering historical price data:

1. **Source Accuracy**: Record amounts exactly as written in source documents
2. **Currency Conversion**: Don't convert; record original currency
3. **Decimal Precision**: Preserve subdivisions (soldi, denari) as decimals
4. **Incomplete Data**: If amount is unclear, don't guess - document uncertainty
5. **Multiple Amounts**: If contract shows staged payments, consider how to model

## Summary

The `gmn:P70_16_documents_sale_price_amount` property provides an essential bridge between simple data entry and semantically rich CIDOC-CRM structures. By using this property correctly:

- **Historians** can efficiently document economic data from Genoese contracts
- **Researchers** gain access to precisely modeled monetary information
- **Systems** can transform data to fully CIDOC-CRM compliant formats
- **Interoperability** is maintained with other cultural heritage systems

Key Takeaways:
1. Always use with P70_17 to specify both amount and currency
2. Use xsd:decimal for exact precision
3. Record amounts exactly as they appear in source documents
4. The property transforms to E97_Monetary_Amount with P181_has_amount
5. Part of the larger E8_Acquisition structure modeling ownership transfer

---

**Version**: 1.0  
**Last Updated**: October 2025  
**Property Creation Date**: 2025-10-17
