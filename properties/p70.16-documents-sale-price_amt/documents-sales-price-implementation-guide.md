# Documents Sale Price Amount - Implementation Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Overview](#overview)
3. [Step-by-Step Implementation](#step-by-step-implementation)
4. [Testing Procedures](#testing-procedures)
5. [Validation](#validation)
6. [Troubleshooting](#troubleshooting)
7. [Integration Checklist](#integration-checklist)

## Prerequisites

Before implementing this property, ensure you have:

- [ ] Access to the gmn_ontology.ttl file
- [ ] Access to the gmn_to_cidoc_transform.py file
- [ ] Python 3.7+ installed
- [ ] Understanding of CIDOC-CRM E97_Monetary_Amount structure
- [ ] Familiarity with the existing P70_17 currency property
- [ ] A TTL validator (e.g., rapper, Apache Jena)
- [ ] Test data with decimal monetary amounts

## Overview

### What You're Implementing

The `gmn:P70_16_documents_sale_price_amount` property is a datatype property that allows direct specification of the numeric monetary amount in sales contracts. It is designed to work in tandem with `gmn:P70_17_documents_sale_price_currency` to create complete monetary values.

### Transformation Logic

**Input** (Simplified):
```turtle
<sale> gmn:P70_16_documents_sale_price_amount "1000.50"^^xsd:decimal .
```

**Output** (CIDOC-CRM):
```turtle
<sale> cidoc:P70_documents <sale/acquisition> .
<sale/acquisition> cidoc:P177_assigned_property_of_type <sale/acquisition/monetary_amount> .
<sale/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P181_has_amount "1000.50"^^xsd:decimal .
```

### Key Design Decisions

1. **Decimal Type**: Uses xsd:decimal to preserve exact monetary precision
2. **E97_Monetary_Amount**: Creates a formal monetary amount entity
3. **Acquisition Context**: Embeds amount within the E8_Acquisition event
4. **Coordinate with Currency**: Designed to share the E97_Monetary_Amount node with P70_17

## Step-by-Step Implementation

### Step 1: Verify Ontology Definition

The property should already exist in your `gmn_ontology.ttl` file (created 2025-10-17). Verify its presence:

#### 1.1 Locate the Property Definition

Open `gmn_ontology.ttl` and search for `P70_16_documents_sale_price_amount`. You should find:

```turtle
# Property: P70.16 documents sale price amount
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

#### 1.2 Verify the Definition

Check that:
- ✓ It's defined as both `owl:DatatypeProperty` and `rdf:Property`
- ✓ Range is `xsd:decimal` (not string or integer)
- ✓ Domain is `gmn:E31_2_Sales_Contract`
- ✓ SubPropertyOf is `cidoc:P70_documents`
- ✓ Comment mentions P181_has_amount (not P180_has_currency_amount)

#### 1.3 Validate TTL Syntax

Run your TTL validator:

```bash
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null
```

If there are errors, check for:
- Missing prefixes
- Incorrect property chains
- Typos in URIs

### Step 2: Implement Python Transformation Function

#### 2.1 Locate the Transformation File

Open `gmn_to_cidoc_transform.py` and find the section with P70 transformation functions (around line 700-1200).

#### 2.2 Verify Function Presence

The function `transform_p70_16_documents_sale_price_amount()` should already exist. Locate it after the `transform_p70_15_documents_witness()` function.

#### 2.3 Review the Implementation

```python
def transform_p70_16_documents_sale_price_amount(data):
    """
    Transform gmn:P70_16_documents_sale_price_amount to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P177_assigned_property_of_type > E97_Monetary_Amount > P181_has_amount
    
    NOTE: The current implementation in the codebase uses 'cidoc:P180_has_currency_amount' 
    which is non-standard. According to CIDOC-CRM, the correct property should be:
    - cidoc:P181_has_amount for the numeric value
    - cidoc:P180_has_currency for the currency (used by P70_17)
    
    This function implements the correct CIDOC-CRM structure using P181_has_amount.
    """
    if 'gmn:P70_16_documents_sale_price_amount' not in data:
        return data
    
    amounts = data['gmn:P70_16_documents_sale_price_amount']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure E8_Acquisition exists
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Process each amount (typically just one)
    for amount_obj in amounts:
        if isinstance(amount_obj, dict):
            amount_value = amount_obj.get('@value', '')
        else:
            amount_value = str(amount_obj)
        
        if not amount_value:
            continue
        
        # Create or get E97_Monetary_Amount entity
        if 'cidoc:P177_assigned_property_of_type' not in acquisition:
            monetary_uri = f"{acquisition['@id']}/monetary_amount"
            acquisition['cidoc:P177_assigned_property_of_type'] = {
                '@id': monetary_uri,
                '@type': 'cidoc:E97_Monetary_Amount'
            }
        
        monetary_amount = acquisition['cidoc:P177_assigned_property_of_type']
        
        # Add the amount using P181_has_amount (correct CIDOC-CRM property)
        monetary_amount['cidoc:P181_has_amount'] = amount_value
    
    # Remove the shortcut property
    del data['gmn:P70_16_documents_sale_price_amount']
    return data
```

#### 2.4 Important Implementation Note

**CRITICAL**: The current codebase uses `cidoc:P180_has_currency_amount` which is **not a standard CIDOC-CRM property**. The correct implementation should use:
- `cidoc:P181_has_amount` for numeric amounts (this property, P70_16)
- `cidoc:P180_has_currency` for currency types (P70_17)

If you find the old implementation using `P180_has_currency_amount`, update it to use `P181_has_amount` as shown above.

#### 2.5 Verify Import Statements

Ensure the required imports are at the top of the file:

```python
from uuid import uuid4
import json
```

### Step 3: Integrate with transform_item()

#### 3.1 Locate the transform_item() Function

Find the main `transform_item()` function (usually near the end of the file).

#### 3.2 Verify Function Call

The function call should already be present. Verify it appears in the correct sequence:

```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)
    item = transform_p70_7_documents_buyers_guarantor(item)
    item = transform_p70_8_documents_broker(item)
    item = transform_p70_9_documents_payment_provider_for_buyer(item)
    item = transform_p70_10_documents_payment_recipient_for_seller(item)
    item = transform_p70_11_documents_referenced_person(item)
    item = transform_p70_12_documents_payment_through_organization(item)
    item = transform_p70_13_documents_referenced_place(item)
    item = transform_p70_14_documents_referenced_object(item)
    item = transform_p70_15_documents_witness(item)
    item = transform_p70_16_documents_sale_price_amount(item)      # ← Verify this line
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # ... other transformations ...
```

**Important**: The P70_16 transformation should run **before** P70_17 so that the E97_Monetary_Amount entity is created first, then P70_17 can add the currency to the same entity.

### Step 4: Handle Currency Integration

#### 4.1 Review P70_17 Integration

The P70_17 (currency) transformation should coordinate with P70_16. Verify that the P70_17 function:

1. Checks if E97_Monetary_Amount already exists
2. Adds currency to the same entity
3. Uses the same URI pattern

Example coordination:

```python
def transform_p70_17_documents_sale_price_currency(data):
    """Transform currency, coordinating with P70_16 amount transformation."""
    
    # ... get currency data ...
    
    # Get or create the E97_Monetary_Amount entity
    if 'cidoc:P177_assigned_property_of_type' not in acquisition:
        monetary_uri = f"{acquisition['@id']}/monetary_amount"
        acquisition['cidoc:P177_assigned_property_of_type'] = {
            '@id': monetary_uri,
            '@type': 'cidoc:E97_Monetary_Amount'
        }
    
    monetary_amount = acquisition['cidoc:P177_assigned_property_of_type']
    
    # Add currency using P180_has_currency
    monetary_amount['cidoc:P180_has_currency'] = currency_data
```

## Testing Procedures

### Test 1: Basic Amount Transformation

**Input**:
```python
test_data = {
    '@id': 'http://example.org/sale001',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_16_documents_sale_price_amount': ['1500.50']
}

result = transform_p70_16_documents_sale_price_amount(test_data)
```

**Expected Output**:
```python
{
    '@id': 'http://example.org/sale001',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P70_documents': [{
        '@id': 'http://example.org/sale001/acquisition',
        '@type': 'cidoc:E8_Acquisition',
        'cidoc:P177_assigned_property_of_type': {
            '@id': 'http://example.org/sale001/acquisition/monetary_amount',
            '@type': 'cidoc:E97_Monetary_Amount',
            'cidoc:P181_has_amount': '1500.50'
        }
    }]
}
```

**Verification**:
- ✓ E8_Acquisition is created
- ✓ E97_Monetary_Amount is created with correct URI
- ✓ P181_has_amount contains the decimal value
- ✓ Original property is removed

### Test 2: Amount with Existing Acquisition

**Input**:
```python
test_data = {
    '@id': 'http://example.org/sale002',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P70_documents': [{
        '@id': 'http://example.org/sale002/acquisition',
        '@type': 'cidoc:E8_Acquisition',
        'cidoc:P23_transferred_title_from': {'@id': 'http://example.org/person_seller'}
    }],
    'gmn:P70_16_documents_sale_price_amount': ['2000.00']
}

result = transform_p70_16_documents_sale_price_amount(test_data)
```

**Expected Output**:
```python
{
    '@id': 'http://example.org/sale002',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P70_documents': [{
        '@id': 'http://example.org/sale002/acquisition',
        '@type': 'cidoc:E8_Acquisition',
        'cidoc:P23_transferred_title_from': {'@id': 'http://example.org/person_seller'},
        'cidoc:P177_assigned_property_of_type': {
            '@id': 'http://example.org/sale002/acquisition/monetary_amount',
            '@type': 'cidoc:E97_Monetary_Amount',
            'cidoc:P181_has_amount': '2000.00'
        }
    }]
}
```

**Verification**:
- ✓ Existing acquisition structure is preserved
- ✓ Monetary amount is added to existing acquisition
- ✓ Other acquisition properties remain intact

### Test 3: Coordinated Amount and Currency

**Input**:
```python
test_data = {
    '@id': 'http://example.org/sale003',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_16_documents_sale_price_amount': ['750.25'],
    'gmn:P70_17_documents_sale_price_currency': [{'@id': 'http://vocab.getty.edu/aat/lira'}]
}

# Transform in correct order
result = transform_p70_16_documents_sale_price_amount(test_data)
result = transform_p70_17_documents_sale_price_currency(result)
```

**Expected Output**:
```python
{
    '@id': 'http://example.org/sale003',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P70_documents': [{
        '@id': 'http://example.org/sale003/acquisition',
        '@type': 'cidoc:E8_Acquisition',
        'cidoc:P177_assigned_property_of_type': {
            '@id': 'http://example.org/sale003/acquisition/monetary_amount',
            '@type': 'cidoc:E97_Monetary_Amount',
            'cidoc:P181_has_amount': '750.25',
            'cidoc:P180_has_currency': {
                '@id': 'http://vocab.getty.edu/aat/lira',
                '@type': 'cidoc:E98_Currency'
            }
        }
    }]
}
```

**Verification**:
- ✓ Both amount and currency are in the same E97_Monetary_Amount entity
- ✓ Proper CIDOC-CRM properties (P181 for amount, P180 for currency)
- ✓ Both shortcut properties are removed

### Test 4: Edge Cases

#### Test 4a: Empty Amount
```python
test_data = {
    '@id': 'http://example.org/sale004',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_16_documents_sale_price_amount': ['']
}

result = transform_p70_16_documents_sale_price_amount(test_data)
# Should skip empty values but still remove property
```

#### Test 4b: Multiple Amounts
```python
test_data = {
    '@id': 'http://example.org/sale005',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_16_documents_sale_price_amount': ['1000.00', '500.00']
}

result = transform_p70_16_documents_sale_price_amount(test_data)
# Should handle last value (or consider if multiple amounts need different handling)
```

#### Test 4c: Decimal Precision
```python
test_data = {
    '@id': 'http://example.org/sale006',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_16_documents_sale_price_amount': ['1234.567890']
}

result = transform_p70_16_documents_sale_price_amount(test_data)
# Should preserve decimal precision
```

### Test 5: Integration Test

Run a full transformation pipeline:

```python
def test_full_transformation():
    """Test complete transformation with multiple properties."""
    
    input_data = {
        '@id': 'http://example.org/contract_1450_05_20',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_1_documents_seller': [{'@id': 'http://example.org/giovanni_rossi'}],
        'gmn:P70_2_documents_buyer': [{'@id': 'http://example.org/marco_bianchi'}],
        'gmn:P70_3_documents_transfer_of': [{'@id': 'http://example.org/house_genoa_1'}],
        'gmn:P70_16_documents_sale_price_amount': ['1500.50'],
        'gmn:P70_17_documents_sale_price_currency': [{'@id': 'http://vocab.getty.edu/aat/lira_genovese'}]
    }
    
    # Run through transform_item()
    result = transform_item(input_data)
    
    # Verify structure
    assert 'cidoc:P70_documents' in result
    acquisition = result['cidoc:P70_documents'][0]
    assert acquisition['@type'] == 'cidoc:E8_Acquisition'
    assert 'cidoc:P23_transferred_title_from' in acquisition
    assert 'cidoc:P22_transferred_title_to' in acquisition
    assert 'cidoc:P24_transferred_title_of' in acquisition
    assert 'cidoc:P177_assigned_property_of_type' in acquisition
    
    monetary_amount = acquisition['cidoc:P177_assigned_property_of_type']
    assert monetary_amount['@type'] == 'cidoc:E97_Monetary_Amount'
    assert 'cidoc:P181_has_amount' in monetary_amount
    assert 'cidoc:P180_has_currency' in monetary_amount
    
    print("✓ Full integration test passed")

test_full_transformation()
```

## Validation

### Validation Checklist

After implementation, verify:

#### Ontology Validation
- [ ] TTL syntax is valid (no parser errors)
- [ ] Property has correct domain and range
- [ ] Property is subPropertyOf cidoc:P70_documents
- [ ] Comments accurately describe the transformation path
- [ ] dcterms:created date is present

#### Python Validation
- [ ] Function exists and is properly named
- [ ] Function is called in transform_item()
- [ ] Function handles missing property gracefully
- [ ] Function creates E8_Acquisition if needed
- [ ] Function creates E97_Monetary_Amount with correct URI
- [ ] Function uses P181_has_amount (not P180_has_currency_amount)
- [ ] Function removes shortcut property after transformation
- [ ] Function preserves existing acquisition data

#### Integration Validation
- [ ] Works with P70_17 currency property
- [ ] Shares E97_Monetary_Amount entity with P70_17
- [ ] Proper transformation order (P70_16 before P70_17)
- [ ] URI patterns are consistent
- [ ] No data loss during transformation

#### Output Validation
- [ ] Output conforms to CIDOC-CRM structure
- [ ] E97_Monetary_Amount has proper type
- [ ] Decimal precision is maintained
- [ ] All required properties are present
- [ ] No shortcut properties remain in output

### Automated Validation Script

```python
def validate_p70_16_implementation():
    """Automated validation of P70_16 implementation."""
    
    errors = []
    warnings = []
    
    # Test 1: Basic transformation
    test1 = {
        '@id': 'test:001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_16_documents_sale_price_amount': ['100.50']
    }
    
    result1 = transform_p70_16_documents_sale_price_amount(test1.copy())
    
    if 'gmn:P70_16_documents_sale_price_amount' in result1:
        errors.append("Shortcut property not removed")
    
    if 'cidoc:P70_documents' not in result1:
        errors.append("E8_Acquisition not created")
    else:
        acq = result1['cidoc:P70_documents'][0]
        if 'cidoc:P177_assigned_property_of_type' not in acq:
            errors.append("E97_Monetary_Amount not created")
        else:
            mon = acq['cidoc:P177_assigned_property_of_type']
            if 'cidoc:P181_has_amount' not in mon:
                errors.append("P181_has_amount not present")
            if 'cidoc:P180_has_currency_amount' in mon:
                errors.append("Using non-standard P180_has_currency_amount instead of P181_has_amount")
    
    # Test 2: Coordination with P70_17
    test2 = {
        '@id': 'test:002',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_16_documents_sale_price_amount': ['200.75'],
        'gmn:P70_17_documents_sale_price_currency': [{'@id': 'test:lira'}]
    }
    
    result2 = transform_p70_16_documents_sale_price_amount(test2.copy())
    result2 = transform_p70_17_documents_sale_price_currency(result2)
    
    acq2 = result2['cidoc:P70_documents'][0]
    mon2 = acq2['cidoc:P177_assigned_property_of_type']
    
    if 'cidoc:P181_has_amount' not in mon2:
        errors.append("Amount lost during currency transformation")
    if 'cidoc:P180_has_currency' not in mon2:
        errors.append("Currency not added to same monetary amount")
    
    # Report results
    if errors:
        print("❌ VALIDATION FAILED")
        for error in errors:
            print(f"  ERROR: {error}")
    else:
        print("✅ VALIDATION PASSED")
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    return len(errors) == 0

# Run validation
validate_p70_16_implementation()
```

## Troubleshooting

### Issue 1: Property Not Found in Ontology

**Symptom**: TTL validator reports undefined property

**Solution**:
1. Verify the prefix declarations at the top of gmn_ontology.ttl
2. Check that the property URI matches exactly: `gmn:P70_16_documents_sale_price_amount`
3. Ensure the property is in the correct section (sales contract properties)
4. Copy the definition from documents-sales-price-ontology.ttl if missing

### Issue 2: Transformation Function Not Called

**Symptom**: Shortcut property remains in output

**Solution**:
1. Check that the function is called in transform_item()
2. Verify the function name matches exactly
3. Ensure it's in the correct sequence (before P70_17)
4. Check for syntax errors that might prevent the function from running

### Issue 3: E97_Monetary_Amount Not Created

**Symptom**: Amount appears directly in E8_Acquisition

**Solution**:
1. Verify the P177_assigned_property_of_type property is being created
2. Check that the E97_Monetary_Amount type is correctly set
3. Ensure the URI pattern is correct
4. Review the function logic for creating the monetary amount entity

### Issue 4: Wrong CIDOC Property Used

**Symptom**: Output uses P180_has_currency_amount instead of P181_has_amount

**Solution**:
1. This is a known issue in the current codebase
2. Update the function to use `cidoc:P181_has_amount`
3. P180 should only be used for currency (P180_has_currency)
4. Refer to CIDOC-CRM documentation for correct property usage

### Issue 5: Currency and Amount in Separate Entities

**Symptom**: P70_16 and P70_17 create different E97_Monetary_Amount entities

**Solution**:
1. Verify that P70_16 runs before P70_17 in transform_item()
2. Check that both functions use the same URI pattern for the monetary amount
3. Ensure P70_17 checks for existing monetary amount before creating new one
4. Review the coordination logic in both functions

### Issue 6: Decimal Precision Lost

**Symptom**: Decimal values truncated or rounded

**Solution**:
1. Ensure xsd:decimal datatype is preserved
2. Don't convert to float (use string or Decimal type in Python)
3. Verify JSON serialization preserves precision
4. Check that amount_value retains original format

### Issue 7: Empty Values Create Invalid Structure

**Symptom**: Empty strings create E97_Monetary_Amount with no amount

**Solution**:
1. Add validation to skip empty values
2. Check for empty strings before creating entities
3. Consider logging warnings for invalid data
4. Implement data quality checks in input validation

### Issue 8: Multiple Amounts Not Handled

**Symptom**: Only one amount appears when multiple are provided

**Solution**:
1. Decide on business logic: Should multiple amounts be supported?
2. If yes, consider creating multiple E97_Monetary_Amount entities
3. If no, document that only the last value is used
4. Consider validating input to reject multiple amounts

## Integration Checklist

### Pre-Implementation
- [ ] Backed up gmn_ontology.ttl
- [ ] Backed up gmn_to_cidoc_transform.py
- [ ] Reviewed CIDOC-CRM E97_Monetary_Amount documentation
- [ ] Understood P181_has_amount vs P180_has_currency distinction
- [ ] Reviewed existing P70_17 implementation

### Implementation
- [ ] Verified property definition in TTL file
- [ ] Verified transformation function in Python file
- [ ] Verified function call in transform_item()
- [ ] Confirmed proper sequencing with P70_17
- [ ] Updated any old P180_has_currency_amount references

### Testing
- [ ] Ran basic transformation test
- [ ] Tested with existing acquisition
- [ ] Tested coordination with P70_17
- [ ] Tested edge cases (empty, multiple, precision)
- [ ] Ran full integration test
- [ ] Validated output structure

### Validation
- [ ] Ran TTL syntax validation
- [ ] Ran automated validation script
- [ ] Manually inspected sample outputs
- [ ] Verified no data loss
- [ ] Confirmed CIDOC-CRM compliance

### Documentation
- [ ] Updated user documentation with examples
- [ ] Added notes about decimal precision
- [ ] Documented relationship with P70_17
- [ ] Updated data entry guidelines
- [ ] Added troubleshooting notes

### Deployment
- [ ] Tested with production-like data
- [ ] Performed regression testing
- [ ] Updated version numbers
- [ ] Created backup of old system
- [ ] Deployed to staging environment
- [ ] Validated in staging
- [ ] Deployed to production

## Summary

This implementation guide has walked you through integrating the `gmn:P70_16_documents_sale_price_amount` property into your GMN system. Key points to remember:

1. **Use P181_has_amount**: The correct CIDOC-CRM property for numeric amounts
2. **Coordinate with P70_17**: Both properties share the same E97_Monetary_Amount entity
3. **Preserve Precision**: Use xsd:decimal to maintain exact monetary values
4. **Test Thoroughly**: Validate both standalone and integrated transformations
5. **Follow CIDOC-CRM**: Ensure semantic compliance with formal ontology standards

If you encounter issues not covered in this guide, consult the CIDOC-CRM documentation or review the related P70_17 currency implementation for comparison.

---

**Version**: 1.0  
**Last Updated**: October 2025
