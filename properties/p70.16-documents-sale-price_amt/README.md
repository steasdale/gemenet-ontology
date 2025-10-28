# Documents Sale Price Amount Property Implementation Package

## Overview

This package contains all necessary materials for implementing the `gmn:P70_16_documents_sale_price_amount` property in the Genoese Merchants Network (GMN) ontology. This property provides a simplified way to document the monetary amount of sale prices in historical sales contracts, which is then transformed to full CIDOC-CRM compliant structures.

**Property**: `gmn:P70_16_documents_sale_price_amount`  
**Label**: "P70.16 documents sale price amount"  
**Property Type**: DatatypeProperty  
**Domain**: `gmn:E31_2_Sales_Contract`  
**Range**: `xsd:decimal`  
**Created**: 2025-10-17

### Key Characteristics

- **Shortcut Property**: Simplifies data entry by allowing direct specification of sale price amounts
- **Transformation Target**: Full CIDOC-CRM path via E8_Acquisition → E97_Monetary_Amount → P181_has_amount
- **Complementary Property**: Works with `gmn:P70_17_documents_sale_price_currency` to express complete monetary values
- **Decimal Values**: Accepts decimal numbers representing monetary quantities (e.g., 1000.50)

### CIDOC-CRM Transformation Path

The property represents this full path:
```
E31_Document → P70_documents → E8_Acquisition → P177_assigned_property_of_type → 
E97_Monetary_Amount → P181_has_amount → xsd:decimal
```

## Package Contents

1. **README.md** (this file)
   - Complete overview and quick-start guide
   - Implementation checklist
   - Package navigation

2. **documents-sales-price-implementation-guide.md**
   - Step-by-step implementation instructions
   - Code integration procedures
   - Testing and validation procedures
   - Troubleshooting guide

3. **documents-sales-price-documentation.md**
   - Complete semantic documentation
   - Property specifications and examples
   - CIDOC-CRM mapping details
   - Usage guidelines and best practices

4. **documents-sales-price-ontology.ttl**
   - Ready-to-copy TTL snippets
   - Formatted for direct insertion into gmn_ontology.ttl
   - Includes all necessary annotations

5. **documents-sales-price-transform.py**
   - Complete Python transformation function
   - Ready to integrate into gmn_to_cidoc_transform.py
   - Includes error handling and edge cases

6. **documents-sales-price-doc-note.txt**
   - Examples and tables for main documentation
   - Ready to insert into correspondence-documentation.md or other docs
   - Formatted text with clear insertion points

## Quick Start Checklist

### Phase 1: Review (15 minutes)
- [ ] Read the complete documentation file to understand the property semantics
- [ ] Review the CIDOC-CRM transformation path and rationale
- [ ] Examine the example transformations to understand input/output patterns
- [ ] Check compatibility with existing P70_17 currency property

### Phase 2: Ontology Integration (10 minutes)
- [ ] Open your gmn_ontology.ttl file
- [ ] Locate the sales contract properties section (around P70.15-P70.17)
- [ ] Copy the TTL snippet from documents-sales-price-ontology.ttl
- [ ] Verify the property is already present (created 2025-10-17)
- [ ] Validate the TTL syntax

### Phase 3: Python Implementation (20 minutes)
- [ ] Open your gmn_to_cidoc_transform.py file
- [ ] Locate the P70.15 witness transformation function
- [ ] Copy the transformation function from documents-sales-price-transform.py
- [ ] Add the function call to transform_item() (should already be present)
- [ ] Test with sample data

### Phase 4: Testing (15 minutes)
- [ ] Run the test cases from the implementation guide
- [ ] Verify decimal value handling
- [ ] Test integration with P70_17 currency property
- [ ] Validate output against CIDOC-CRM structure
- [ ] Check edge cases (missing values, multiple amounts)

### Phase 5: Documentation (10 minutes)
- [ ] Add examples from documents-sales-price-doc-note.txt to your documentation
- [ ] Update any relevant user guides or data entry instructions
- [ ] Document the relationship with P70_17 currency property
- [ ] Add notes about decimal precision requirements

**Total Estimated Time**: 70 minutes

## Implementation Summary

### What This Property Does

The `gmn:P70_16_documents_sale_price_amount` property allows users to directly specify the numeric monetary amount of a sale price in a sales contract. For example:

```turtle
<sale_contract_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_16_documents_sale_price_amount "1500.50"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <lira_genovese> .
```

This shortcut is automatically transformed to the full CIDOC-CRM structure:

```turtle
<sale_contract_001> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <sale_contract_001/acquisition> .

<sale_contract_001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P177_assigned_property_of_type <sale_contract_001/acquisition/monetary_amount> .

<sale_contract_001/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P181_has_amount "1500.50"^^xsd:decimal ;
    cidoc:P180_has_currency <lira_genovese> .
```

### Why This Matters

1. **Simplified Data Entry**: Data entry personnel can record monetary amounts directly without creating complex intermediate nodes
2. **Semantic Precision**: The transformation ensures full CIDOC-CRM compliance for interoperability
3. **Historical Documentation**: Preserves exact monetary values from historical sales contracts
4. **Monetary Modeling**: Creates proper E97_Monetary_Amount entities with both amount and currency
5. **Research Facilitation**: Enables economic analysis across the merchant network

### Integration with Existing Properties

This property works closely with:
- **P70_17 (currency)**: Together they form complete monetary values
- **P70_1 (seller)**: Identifies who receives the payment
- **P70_2 (buyer)**: Identifies who makes the payment
- **P70_3 (transfer of)**: Links to what is being purchased
- **E8_Acquisition**: The central event that includes the monetary amount

### Common Use Cases

1. **Standard Sales**: Recording the agreed purchase price for property or goods
2. **Partial Payments**: Documenting installment amounts or deposits
3. **Complex Transactions**: Multiple amounts for different components of a sale
4. **Economic Analysis**: Aggregating prices across contracts for research

## File Descriptions

### Implementation Guide
The implementation guide provides detailed step-by-step instructions for integrating this property into your system. It includes code snippets, testing procedures, and troubleshooting guidance. Start here if you're ready to implement.

### Ontology Documentation
The documentation file provides comprehensive semantic information about the property, including its relationship to CIDOC-CRM, usage examples, and best practices. Read this to understand the theoretical foundation and proper usage.

### TTL Additions
This file contains the exact TTL code needed for the ontology file. The property should already be present in your gmn_ontology.ttl file (created 2025-10-17), but this file provides reference and can be used to verify the definition.

### Python Additions
This file contains the complete Python function for transforming the shortcut property to CIDOC-CRM compliant structures. The function should already be present in your gmn_to_cidoc_transform.py file.

### Document Additions
This file contains example text, tables, and figures that can be added to your main documentation files to explain the property to users and data entry personnel.

## Key Relationships

```
gmn:E31_2_Sales_Contract (Sales Contract Document)
    └─ gmn:P70_16_documents_sale_price_amount → xsd:decimal
    └─ gmn:P70_17_documents_sale_price_currency → cidoc:E98_Currency
    
Transforms to:
    └─ cidoc:P70_documents → cidoc:E8_Acquisition
        └─ cidoc:P177_assigned_property_of_type → cidoc:E97_Monetary_Amount
            ├─ cidoc:P181_has_amount → xsd:decimal (from P70_16)
            └─ cidoc:P180_has_currency → cidoc:E98_Currency (from P70_17)
```

## Next Steps

1. **Review**: Start with documents-sales-price-documentation.md to understand the property semantics
2. **Implement**: Follow documents-sales-price-implementation-guide.md for step-by-step integration
3. **Reference**: Use documents-sales-price-ontology.ttl and documents-sales-price-transform.py as needed
4. **Document**: Add examples from documents-sales-price-doc-note.txt to your documentation

## Important Notes

- **Decimal Precision**: Use appropriate decimal precision for historical monetary values
- **Currency Requirement**: Always use P70_16 with P70_17 to specify both amount and currency
- **Multiple Amounts**: If a contract has multiple amounts (e.g., deposits, final payment), use the property multiple times or model as separate transactions
- **Historical Accuracy**: Record amounts exactly as they appear in source documents
- **Coordinate with P70_17**: Ensure currency transformations are handled consistently

## Questions or Issues?

Refer to the troubleshooting section in documents-sales-price-implementation-guide.md for common issues and solutions.

---

**Version**: 1.0  
**Last Updated**: October 2025  
**Property Creation Date**: 2025-10-17
