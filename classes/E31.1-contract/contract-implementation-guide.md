# E31.1 General Contract - Implementation Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Conceptual Overview](#conceptual-overview)
3. [Class Structure](#class-structure)
4. [Implementation Status](#implementation-status)
5. [Using General Contracts](#using-general-contracts)
6. [Property Reference](#property-reference)
7. [Best Practices](#best-practices)
8. [Validation](#validation)
9. [Troubleshooting](#troubleshooting)

## Introduction

### Purpose of This Guide

This implementation guide explains the **gmn:E31_1_Contract** class and its role in the Genoese Merchant Networks ontology. Unlike implementation guides for specialized contract types (such as sales, donations, or dowries), this guide does not provide steps for adding new code or ontology definitions. Instead, it documents the existing E31_1_Contract class and explains how to properly use it and extend it.

### Key Points

- **E31_1_Contract is already implemented** in gmn_ontology.ttl
- It serves as the **parent class** for all specialized contract types
- **No new code or ontology additions are needed** for the general contract class
- This guide focuses on understanding, using, and extending the class

### Who Should Read This

- Ontologists working with the GMN ontology
- Developers creating new contract types
- Data entry specialists understanding the contract hierarchy
- Project members documenting contract instances

## Conceptual Overview

### What is E31_1_Contract?

E31_1_Contract is a specialized type of cidoc:E31_Document that represents notarial contract documents. It serves multiple roles:

1. **Parent Class**: Foundation for all specialized contract types
2. **Document Representation**: Models the contract document itself (not the transaction)
3. **Inheritance Base**: Provides common structure for all contract subclasses
4. **Semantic Anchor**: Links contracts to CIDOC-CRM document hierarchy

### Document vs. Transaction

A critical distinction in the ontology:

**The Contract (E31_1_Contract)**
- The physical or conceptual document
- The notarial record
- The written evidence

**The Transaction (E8_Acquisition, E7_Activity, etc.)**
- The actual transfer of property
- The legal event or agreement
- The activity documented by the contract

These are connected via `cidoc:P70_documents`:

```
Contract Document  --P70_documents-->  Transaction Event
```

### Inheritance Hierarchy

```
cidoc:E31_Document (CIDOC-CRM)
  │
  └── gmn:E31_1_Contract (General Contract) ← This class
      │
      ├── gmn:E31_2_Sales_Contract (Property sales)
      │
      ├── gmn:E31_3_Arbitration_Agreement (Dispute resolution)
      │
      ├── gmn:E31_4_Cession_of_Rights_Contract (Rights transfer)
      │
      ├── gmn:E31_7_Donation_Contract (Gifts)
      │
      └── gmn:E31_8_Dowry_Contract (Marriage property)
```

## Class Structure

### Current Implementation

The E31_1_Contract class is defined in `gmn_ontology.ttl` (lines 42-49):

```turtle
# Class: E31.1 Contract
gmn:E31_1_Contract
    a owl:Class ;
    rdfs:subClassOf cidoc:E31_Document ;
    rdfs:label "E31.1 Contract"@en ;
    rdfs:comment "General class that describes notarial contract documents. This is a specialized type of E31_Document used to represent legal documents recorded by notaries that formalize agreements, transactions, and legal acts between parties. Contracts are the primary documentary evidence for social, economic, and legal relationships in medieval and early modern societies. Instances of this class represent the physical or conceptual document itself, while the actual events documented (acquisitions, agreements, etc.) are modeled through appropriate event classes that the document documents (via P70_documents). This serves as a parent class for more specific contract types."@en ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:E31_Document, cidoc:P70_documents .
```

### Key Features

1. **Subclass Relationship**: Inherits from `cidoc:E31_Document`
2. **Parent Class Role**: Explicitly described as parent for specific contract types
3. **P70_documents Link**: References the property connecting contracts to transactions
4. **Created Date**: Established on 2025-10-17

### What Makes It "General"

E31_1_Contract is "general" because:

- It has **no transaction-specific properties** (like seller, buyer, donor)
- It represents **any type of notarial contract**, not just one kind
- It provides **common structure** inherited by specialized types
- It's used **primarily for inheritance**, not direct instantiation

## Implementation Status

### Already Implemented ✓

The following are already complete in the current ontology:

#### 1. Class Definition ✓
- Defined in gmn_ontology.ttl
- Properly subclassed from cidoc:E31_Document
- Complete rdfs:label and rdfs:comment
- Creation date and see-also references

#### 2. Subclass Structure ✓
All specialized contract types properly inherit:
- E31.2 Sales Contract
- E31.3 Arbitration Agreement
- E31.4 Cession of Rights Contract
- E31.7 Donation Contract
- E31.8 Dowry Contract

#### 3. Property Inheritance ✓
Specialized contracts inherit and use:
- Standard document properties (P1.1, P94i.1, P94i.2, P94i.3, P102.1, P46i.1)
- Custom properties defined for their specific transaction types

#### 4. Transformations ✓
- E31_1_Contract uses standard document property transformations
- No specialized transformation functions needed
- Specialized contracts add their own transformation functions

### No Changes Needed

**This is important**: Unlike implementing new specialized contract types, E31_1_Contract requires:

- ❌ No new class definitions to add
- ❌ No new properties to create
- ❌ No transformation functions to write
- ❌ No ontology file modifications needed

**The class is complete and functional as-is.**

## Using General Contracts

### When to Use E31_1_Contract

#### Use Cases for Direct Instantiation

Use E31_1_Contract directly when:

1. **Unclassified Contracts**: You have a contract that doesn't fit existing specialized types
2. **Temporary Classification**: You need to record a contract before determining its specific type
3. **Generic Queries**: You want to query all contracts regardless of type

#### More Common: Use Specialized Types

In most cases, you should **NOT** directly instantiate E31_1_Contract. Instead:

1. **For Property Sales**: Use `gmn:E31_2_Sales_Contract`
2. **For Gifts**: Use `gmn:E31_7_Donation_Contract`
3. **For Dowries**: Use `gmn:E31_8_Dowry_Contract`
4. **For Rights Transfers**: Use `gmn:E31_4_Cession_of_Rights_Contract`
5. **For Arbitrations**: Use `gmn:E31_3_Arbitration_Agreement`

### Example: Direct Instantiation (Rare)

```turtle
<contract_unknown_001> a gmn:E31_1_Contract ;
    gmn:P1_1_has_name "Unclassified notarial contract from 1450" ;
    gmn:P94i_1_was_created_by <notary_giovanni> ;
    gmn:P94i_2_has_enactment_date "1450-05-20"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <genoa> ;
    gmn:P46i_1_is_contained_in <register_1450_may> ;
    cidoc:P70_documents <contract_unknown_001/event> ;
    gmn:P3_1_has_editorial_note "Contract type not yet determined; requires further analysis" .
```

### Example: Using Specialized Type (Common)

```turtle
<contract_sale_001> a gmn:E31_2_Sales_Contract ;  # Specific type
    gmn:P1_1_has_name "Sale of house on Via San Lorenzo" ;
    gmn:P94i_1_was_created_by <notary_giovanni> ;
    gmn:P94i_2_has_enactment_date "1450-05-20"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <genoa> ;
    gmn:P70_14_indicates_seller <maria_doria> ;  # Specialized property
    gmn:P70_15_indicates_buyer <antonio_spinola> ;  # Specialized property
    gmn:P70_16_documents_sale_price_amount "500.00"^^xsd:decimal .  # Specialized property
```

### Querying All Contracts

To find all contracts (including specialized types):

```sparql
# Find all contract instances
SELECT ?contract ?type WHERE {
    ?contract a ?type .
    ?type rdfs:subClassOf* gmn:E31_1_Contract .
}
```

```sparql
# Count contracts by type
SELECT ?type (COUNT(?contract) as ?count) WHERE {
    ?contract a ?type .
    ?type rdfs:subClassOf* gmn:E31_1_Contract .
}
GROUP BY ?type
ORDER BY DESC(?count)
```

## Property Reference

### Inherited from cidoc:E31_Document

E31_1_Contract instances can use all standard document properties:

#### Identification Properties

**gmn:P1_1_has_name**
- Purpose: Name or title of the contract
- Range: String
- Example: "Contract between Giovanni and Marco"

**gmn:P102_1_has_title**
- Purpose: Formal title, often in Latin
- Range: String  
- Example: "Contractus venditionis domus"

#### Creation Properties

**gmn:P94i_1_was_created_by**
- Purpose: Notary who recorded the contract
- Range: cidoc:E21_Person
- Example: Link to notary resource

**gmn:P94i_2_has_enactment_date**
- Purpose: Date when contract was enacted
- Range: xsd:date
- Example: "1450-03-15"^^xsd:date

**gmn:P94i_3_has_place_of_enactment**
- Purpose: Location where contract was drawn up
- Range: cidoc:E53_Place
- Example: Link to place resource (notary's office, public building)

#### Context Properties

**gmn:P46i_1_is_contained_in**
- Purpose: Notarial register containing the contract
- Range: cidoc:E31_Document (register)
- Example: Link to register resource

**cidoc:P70_documents**
- Purpose: Links to the transaction/event documented
- Range: cidoc:E7_Activity or cidoc:E8_Acquisition
- Example: Link to acquisition or activity resource

#### Annotation Properties

**gmn:P3_1_has_editorial_note**
- Purpose: Internal notes about the contract
- Range: String
- Example: "Difficult to read; may need verification"

### Properties NOT on E31_1_Contract

General contracts do NOT have transaction-specific properties like:

- ❌ P70.14 (seller) - Only on E31_2_Sales_Contract
- ❌ P70.15 (buyer) - Only on E31_2_Sales_Contract
- ❌ P70.32 (donor) - Only on E31_7_Donation_Contract and E31_8_Dowry_Contract
- ❌ P70.18 (disputing party) - Only on E31_3_Arbitration_Agreement

**Use specialized contract types to access these properties.**

## Best Practices

### 1. Prefer Specialized Types

✅ **DO**: Use the most specific contract class available
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;  # Specific
    gmn:P70_14_indicates_seller <seller> .
```

❌ **DON'T**: Use general type when specific exists
```turtle
<contract001> a gmn:E31_1_Contract ;  # Too general
    # No way to properly indicate seller/buyer
```

### 2. Understand Inheritance

✅ **DO**: Recognize that specialized types inherit E31_1_Contract properties
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    gmn:P1_1_has_name "Sale Contract" ;  # From E31_1_Contract/E31_Document
    gmn:P70_14_indicates_seller <seller> .  # Specific to E31_2
```

❌ **DON'T**: Duplicate properties or create confusion
```turtle
<contract001> a gmn:E31_1_Contract ;
<contract001> a gmn:E31_2_Sales_Contract .  # Don't assign both types
```

### 3. Document the Transaction Separately

✅ **DO**: Use P70_documents to link to the transaction
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <contract001/acquisition> .

<contract001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <seller> ;
    cidoc:P22_transferred_title_to <buyer> .
```

❌ **DON'T**: Conflate document and transaction
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    cidoc:P23_transferred_title_from <seller> .  # Wrong: this is on E8_Acquisition
```

### 4. Use Editorial Notes for Ambiguity

✅ **DO**: Document uncertain classifications
```turtle
<contract001> a gmn:E31_1_Contract ;
    gmn:P3_1_has_editorial_note "Appears to be a donation, but transaction type unclear from damaged text. Requires further analysis." .
```

### 5. Follow Naming Conventions

✅ **DO**: Use clear, descriptive names
```turtle
gmn:P1_1_has_name "Sale of house in Genoa by Giovanni Doria to Marco Spinola"@en .
```

❌ **DON'T**: Use cryptic or abbreviated names
```turtle
gmn:P1_1_has_name "GD->MS hse"@en .  # Too cryptic
```

## Validation

### Checking Class Hierarchy

Verify that specialized contracts properly inherit from E31_1_Contract:

```sparql
# List all contract types and their parent classes
SELECT ?class ?parent WHERE {
    ?class rdfs:subClassOf+ gmn:E31_1_Contract .
    ?class rdfs:subClassOf ?parent .
}
```

Expected results should show:
- E31_2_Sales_Contract subClassOf E31_1_Contract
- E31_3_Arbitration_Agreement subClassOf E31_1_Contract
- E31_7_Donation_Contract subClassOf E31_1_Contract
- And so on...

### Checking Contract Instances

Verify that contracts are properly typed:

```sparql
# Find contracts without specific types (should be rare)
SELECT ?contract WHERE {
    ?contract a gmn:E31_1_Contract .
    FILTER NOT EXISTS {
        ?contract a ?specific_type .
        ?specific_type rdfs:subClassOf gmn:E31_1_Contract .
        FILTER(?specific_type != gmn:E31_1_Contract)
    }
}
```

### Checking Property Usage

Verify that properties are used correctly:

```sparql
# Find contracts using transaction-specific properties incorrectly
SELECT ?contract ?property WHERE {
    ?contract a gmn:E31_1_Contract .
    ?contract ?property ?value .
    
    # Check if property is specific to a specialized type
    FILTER(?property IN (
        gmn:P70_14_indicates_seller,
        gmn:P70_15_indicates_buyer,
        gmn:P70_32_indicates_donor
    ))
    
    # But contract is not of that specialized type
    FILTER NOT EXISTS {
        ?contract a ?specialized_type .
        ?specialized_type rdfs:subClassOf gmn:E31_1_Contract .
        FILTER(?specialized_type != gmn:E31_1_Contract)
    }
}
```

### Validation Checklist

- [ ] All specialized contract types have `rdfs:subClassOf gmn:E31_1_Contract`
- [ ] E31_1_Contract has `rdfs:subClassOf cidoc:E31_Document`
- [ ] Contracts use appropriate specialized types when possible
- [ ] Direct E31_1_Contract instances are justified (unclassified contracts)
- [ ] P70_documents links exist for contracts with known transactions
- [ ] Property domains match contract types (specialized properties on specialized types)

## Troubleshooting

### Issue: "I can't find properties for buyer/seller on E31_1_Contract"

**Solution**: E31_1_Contract is the general parent class. Use specialized types:
- For sales: Use `gmn:E31_2_Sales_Contract` with P70.14 (seller) and P70.15 (buyer)
- For donations: Use `gmn:E31_7_Donation_Contract` with P70.32 (donor) and P70.22 (receiving party)

### Issue: "My query returns too many results"

**Problem**: Querying for `?x a gmn:E31_1_Contract` returns all contracts including specialized types.

**Solution**: If you only want general contracts (rare):
```sparql
SELECT ?contract WHERE {
    ?contract a gmn:E31_1_Contract .
    FILTER NOT EXISTS {
        ?contract a ?specialized .
        ?specialized rdfs:subClassOf gmn:E31_1_Contract .
        FILTER(?specialized != gmn:E31_1_Contract)
    }
}
```

### Issue: "Should I use E31_1_Contract or E31_2_Sales_Contract?"

**Decision Tree**:

1. Is this a property sale? → Use E31_2_Sales_Contract
2. Is this a gift/donation? → Use E31_7_Donation_Contract
3. Is this a dowry? → Use E31_8_Dowry_Contract
4. Is this a rights transfer? → Use E31_4_Cession_of_Rights_Contract
5. Is this an arbitration? → Use E31_3_Arbitration_Agreement
6. None of the above? → Use E31_1_Contract temporarily, plan to create specialized type

### Issue: "I want to create a new contract type"

**Steps**:

1. Create a new subclass of gmn:E31_1_Contract
2. Add specific properties for your contract type
3. Create transformation functions for those properties
4. Follow the pattern of existing specialized types

**Example** (hypothetical rental contract):

```turtle
# In ontology file
gmn:E31_9_Rental_Contract
    a owl:Class ;
    rdfs:subClassOf gmn:E31_1_Contract ;
    rdfs:label "E31.9 Rental Contract"@en ;
    rdfs:comment "Describes rental agreements..." .

# Add specific properties
gmn:P70_35_indicates_lessor
    rdfs:domain gmn:E31_9_Rental_Contract ;
    rdfs:range cidoc:E39_Actor .

gmn:P70_36_indicates_lessee
    rdfs:domain gmn:E31_9_Rental_Contract ;
    rdfs:range cidoc:E39_Actor .
```

### Issue: "The transformation isn't working"

**Check**:
- Are you using E31_1_Contract directly? (Uses standard transformations)
- Or a specialized type? (Check specialized type's transformation functions)
- Are properties correctly defined with proper domains?

### Issue: "I see E31_5_Declaration - is that a contract?"

**No**: E31_5_Declaration is NOT a subclass of E31_1_Contract. It's a separate document type:

```
cidoc:E31_Document
  ├── gmn:E31_1_Contract (parent of contract types)
  ├── gmn:E31_5_Declaration (separate document type)
  └── gmn:E31_6_Correspondence (separate document type)
```

Declarations are unilateral statements, not bilateral contracts.

## Creating New Contract Types

If you need to extend the ontology with a new contract type:

### Step 1: Define the New Class

```turtle
gmn:E31_X_NewContract_Type
    a owl:Class ;
    rdfs:subClassOf gmn:E31_1_Contract ;  # Must inherit from E31_1_Contract
    rdfs:label "E31.X New Contract Type"@en ;
    rdfs:comment "Describes [specific type of contract]..." ;
    dcterms:created "YYYY-MM-DD"^^xsd:date ;
    rdfs:seeAlso gmn:E31_1_Contract .
```

### Step 2: Add Specific Properties

```turtle
gmn:P70_XX_indicates_party_1
    a owl:ObjectProperty ;
    rdfs:label "P70.XX indicates party 1"@en ;
    rdfs:comment "Describes the role of party 1..." ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_X_NewContract_Type ;
    rdfs:range cidoc:E39_Actor .
```

### Step 3: Create Transformation Functions

```python
def transform_p70_xx_party_1(data):
    """Transform P70.XX to full CIDOC-CRM structure."""
    # Implementation similar to other contract transformations
    pass
```

### Step 4: Document the New Type

Create a documentation package similar to this one, but for your specialized type.

## Conclusion

The E31_1_Contract class is a foundational element of the GMN ontology that:

1. **Provides structure** for all contract types through inheritance
2. **Separates concerns** between documents and transactions
3. **Enables flexibility** for future contract type additions
4. **Maintains CIDOC-CRM compliance** through proper subclassing

Remember:
- **E31_1_Contract is already implemented** - no changes needed
- **Use specialized types** for specific contract categories
- **Extend the class** when adding new contract types
- **Follow inheritance patterns** established by existing types

For questions about specific contract types, consult their individual documentation:
- Sales: See main ontology documentation
- Donations: See donation-documentation.md
- Dowries: See dowry-documentation.md
- Arbitrations: See arbitration-ontology.md
- Cessions: See main ontology documentation
