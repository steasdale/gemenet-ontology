# Documents Sale Price Currency Implementation Guide
## Step-by-Step Instructions for gmn:P70_17_documents_sale_price_currency

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Ontology Implementation](#ontology-implementation)
3. [Python Transformation Implementation](#python-transformation-implementation)
4. [Testing Procedures](#testing-procedures)
5. [Integration Verification](#integration-verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before implementing this property, ensure you have:

- [ ] Access to the `gmn_ontology.ttl` file
- [ ] Access to the `gmn_to_cidoc_transform.py` file
- [ ] P70.16 (sale price amount) property already implemented
- [ ] Understanding of E97_Monetary_Amount structure
- [ ] Test data with currency information

**Required Knowledge:**
- CIDOC-CRM property chains
- E97_Monetary_Amount and E98_Currency entities
- Python transformation patterns
- TTL/RDF syntax

---

## Ontology Implementation

### Step 1: Locate the Insertion Point

Open `gmn_ontology.ttl` and find the P70.16 property definition (sale price amount). The new P70.17 property should be added immediately after it.

**Search for:**
```turtle
# Property: P70.16 documents sale price amount
gmn:P70_16_documents_sale_price_amount
```

### Step 2: Add the Property Definition

Insert the following TTL immediately after the P70.16 definition:

```turtle
# Property: P70.17 documents sale price currency
gmn:P70_17_documents_sale_price_currency
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.17 documents sale price currency"@en ;
    rdfs:comment "Simplified property for expressing the currency unit of the sale price documented in a sales contract. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P177_assigned_property_of_type > E97_Monetary_Amount > P180_has_currency > E98_Currency. This property captures the currency type (e.g., Genoese lira, florin, ducat). Use P70.16 to specify the numeric amount. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The value should reference a currency entity or use a controlled vocabulary of currency types."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E98_Currency ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P177_assigned_property_of_type, cidoc:P180_has_currency .
```

### Step 3: Verify the Property Structure

Check that all elements are correctly specified:

- [x] Property type: `owl:ObjectProperty` (since it relates to E98_Currency entity)
- [x] Multilingual label with language tag `@en`
- [x] Comprehensive comment explaining CIDOC-CRM path
- [x] Correct subproperty: `cidoc:P70_documents`
- [x] Correct domain: `gmn:E31_2_Sales_Contract`
- [x] Correct range: `cidoc:E98_Currency`
- [x] Creation date
- [x] Related properties listed

### Step 4: Validate TTL Syntax

Use a TTL validator or parser to ensure:
- No syntax errors
- Proper prefix declarations
- Valid IRIs
- Correct property hierarchy

---

## Python Transformation Implementation

### Step 1: Locate the Insertion Point

Open `gmn_to_cidoc_transform.py` and find the `transform_p70_16_documents_sale_price_amount()` function. The new P70.17 function should be added immediately after it.

### Step 2: Add the Transformation Function

Insert the following Python function:

```python
def transform_p70_17_documents_sale_price_currency(data):
    """
    Transform gmn:P70_17_documents_sale_price_currency to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P177_assigned_property_of_type > E97_Monetary_Amount > P180_has_currency > E98_Currency
    """
    if 'gmn:P70_17_documents_sale_price_currency' not in data:
        return data
    
    currencies = data['gmn:P70_17_documents_sale_price_currency']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure E8_Acquisition exists
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Ensure E97_Monetary_Amount exists (may have been created by P70.16)
    if 'cidoc:P177_assigned_property_of_type' not in acquisition:
        monetary_uri = f"{acquisition['@id']}/monetary_amount"
        acquisition['cidoc:P177_assigned_property_of_type'] = {
            '@id': monetary_uri,
            '@type': 'cidoc:E97_Monetary_Amount'
        }
    
    monetary_amount = acquisition['cidoc:P177_assigned_property_of_type']
    
    # Add currency to the monetary amount
    for currency_obj in currencies:
        if isinstance(currency_obj, dict):
            currency_data = currency_obj.copy()
            if '@type' not in currency_data:
                currency_data['@type'] = 'cidoc:E98_Currency'
        else:
            # Simple URI or string
            currency_uri = str(currency_obj)
            currency_data = {
                '@id': currency_uri,
                '@type': 'cidoc:E98_Currency'
            }
        
        monetary_amount['cidoc:P180_has_currency'] = currency_data
    
    # Remove the simplified property
    del data['gmn:P70_17_documents_sale_price_currency']
    return data
```

### Step 3: Understand the Function Logic

**Key operations:**

1. **Check for Property**: Returns early if property not present
2. **Get Subject URI**: Retrieves or generates document URI
3. **Ensure E8_Acquisition**: Creates if not already present (coordinates with P70.16)
4. **Ensure E97_Monetary_Amount**: Creates if not present (shared with P70.16)
5. **Add Currency**: Attaches P180_has_currency with E98_Currency entity
6. **Handle Multiple Formats**: Supports both object and URI currency references
7. **Clean Up**: Removes the simplified property

### Step 4: Add to Main Transformation Function

Locate the `transform_item()` function and add the function call in the sales contract properties section:

```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    # ... existing code ...
    
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
    item = transform_p70_16_documents_sale_price_amount(item)
    item = transform_p70_17_documents_sale_price_currency(item)  # ADD THIS LINE
    
    # ... rest of function ...
```

### Step 5: Verify Import Statements

Ensure the required modules are imported at the top of the file:

```python
from uuid import uuid4
# ... other imports ...
```

---

## Testing Procedures

### Test 1: Currency Only

**Input:**
```python
test_data_1 = {
    '@id': 'http://example.org/contract001',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_17_documents_sale_price_currency': ['http://example.org/currency/lira_genovese']
}
```

**Expected Output:**
```python
{
    '@id': 'http://example.org/contract001',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P70_documents': [{
        '@id': 'http://example.org/contract001/acquisition',
        '@type': 'cidoc:E8_Acquisition',
        'cidoc:P177_assigned_property_of_type': {
            '@id': 'http://example.org/contract001/acquisition/monetary_amount',
            '@type': 'cidoc:E97_Monetary_Amount',
            'cidoc:P180_has_currency': {
                '@id': 'http://example.org/currency/lira_genovese',
                '@type': 'cidoc:E98_Currency'
            }
        }
    }]
}
```

### Test 2: Currency with Amount

**Input:**
```python
test_data_2 = {
    '@id': 'http://example.org/contract002',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_16_documents_sale_price_amount': ['250.00'],
    'gmn:P70_17_documents_sale_price_currency': ['http://example.org/currency/florin']
}
```

**Expected Output:**
```python
{
    '@id': 'http://example.org/contract002',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P70_documents': [{
        '@id': 'http://example.org/contract002/acquisition',
        '@type': 'cidoc:E8_Acquisition',
        'cidoc:P177_assigned_property_of_type': {
            '@id': 'http://example.org/contract002/acquisition/monetary_amount',
            '@type': 'cidoc:E97_Monetary_Amount',
            'cidoc:P180_has_currency_amount': '250.00',
            'cidoc:P180_has_currency': {
                '@id': 'http://example.org/currency/florin',
                '@type': 'cidoc:E98_Currency'
            }
        }
    }]
}
```

### Test 3: Currency as Structured Object

**Input:**
```python
test_data_3 = {
    '@id': 'http://example.org/contract003',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_17_documents_sale_price_currency': [{
        '@id': 'http://example.org/currency/ducat',
        'rdfs:label': 'Venetian Ducat'
    }]
}
```

**Expected Output:**
```python
{
    '@id': 'http://example.org/contract003',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P70_documents': [{
        '@id': 'http://example.org/contract003/acquisition',
        '@type': 'cidoc:E8_Acquisition',
        'cidoc:P177_assigned_property_of_type': {
            '@id': 'http://example.org/contract003/acquisition/monetary_amount',
            '@type': 'cidoc:E97_Monetary_Amount',
            'cidoc:P180_has_currency': {
                '@id': 'http://example.org/currency/ducat',
                '@type': 'cidoc:E98_Currency',
                'rdfs:label': 'Venetian Ducat'
            }
        }
    }]
}
```

### Test 4: Complete Sales Contract

**Input:**
```python
test_data_4 = {
    '@id': 'http://example.org/contract004',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_1_documents_seller': ['http://example.org/person/giovanni'],
    'gmn:P70_2_documents_buyer': ['http://example.org/person/antonio'],
    'gmn:P70_3_documents_transfer_of': ['http://example.org/building/house001'],
    'gmn:P70_16_documents_sale_price_amount': ['1500.00'],
    'gmn:P70_17_documents_sale_price_currency': ['http://example.org/currency/lira_genovese']
}
```

**Run Test:**
```python
# Apply all transformations in order
result = transform_p70_1_documents_seller(test_data_4)
result = transform_p70_2_documents_buyer(result)
result = transform_p70_3_documents_transfer_of(result)
result = transform_p70_16_documents_sale_price_amount(result)
result = transform_p70_17_documents_sale_price_currency(result)

# Verify structure
assert 'cidoc:P70_documents' in result
acquisition = result['cidoc:P70_documents'][0]
assert acquisition['@type'] == 'cidoc:E8_Acquisition'
assert 'cidoc:P23_transferred_title_from' in acquisition
assert 'cidoc:P22_transferred_title_to' in acquisition
assert 'cidoc:P24_transferred_title_of' in acquisition
monetary = acquisition['cidoc:P177_assigned_property_of_type']
assert monetary['@type'] == 'cidoc:E97_Monetary_Amount'
assert 'cidoc:P180_has_currency_amount' in monetary
assert 'cidoc:P180_has_currency' in monetary
```

### Test 5: Edge Cases

**Test 5a: Missing Currency (No-op)**
```python
test_data_5a = {
    '@id': 'http://example.org/contract005',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_16_documents_sale_price_amount': ['100.00']
}
result = transform_p70_17_documents_sale_price_currency(test_data_5a)
# Should return unchanged (except P70.16 might have been processed)
```

**Test 5b: Multiple Currencies (Uses Last)**
```python
test_data_5b = {
    '@id': 'http://example.org/contract006',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_17_documents_sale_price_currency': [
        'http://example.org/currency/lira',
        'http://example.org/currency/florin'
    ]
}
result = transform_p70_17_documents_sale_price_currency(test_data_5b)
# Last currency in list will be assigned
```

---

## Integration Verification

### Verification Checklist

After implementation, verify:

- [ ] **Ontology File**: TTL property definition is valid and properly placed
- [ ] **Python Script**: Function is added in correct location
- [ ] **Transform Function**: Function call is added to `transform_item()`
- [ ] **No Syntax Errors**: Code runs without errors
- [ ] **Test Data Passes**: All test cases produce expected output
- [ ] **E97 Integration**: Works correctly with P70.16 transformation
- [ ] **URI Generation**: Proper URIs created for monetary amounts
- [ ] **Currency Types**: E98_Currency entities properly structured
- [ ] **Cleanup**: Simplified properties removed from output

### Integration with P70.16

The P70.17 transformation must coordinate with P70.16:

**Coordination Points:**
1. Both create/use the same E8_Acquisition node
2. Both create/use the same E97_Monetary_Amount node
3. P70.16 adds `P180_has_currency_amount` (was P181_has_amount in some versions)
4. P70.17 adds `P180_has_currency`

**Test Integration:**
```python
def test_price_integration():
    data = {
        '@id': 'http://example.org/contract_test',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_16_documents_sale_price_amount': ['500.00'],
        'gmn:P70_17_documents_sale_price_currency': ['http://example.org/currency/lira']
    }
    
    # Transform both
    data = transform_p70_16_documents_sale_price_amount(data)
    data = transform_p70_17_documents_sale_price_currency(data)
    
    # Verify single E97_Monetary_Amount with both properties
    monetary = data['cidoc:P70_documents'][0]['cidoc:P177_assigned_property_of_type']
    assert 'cidoc:P180_has_currency_amount' in monetary
    assert 'cidoc:P180_has_currency' in monetary
    
    print("✓ Integration test passed")
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Currency Not Appearing in Output

**Symptoms:**
- P180_has_currency property missing from E97_Monetary_Amount
- Currency data not transformed

**Solutions:**
- Verify input property name is exactly `gmn:P70_17_documents_sale_price_currency`
- Check that currency value is not empty or null
- Ensure function is called in `transform_item()`
- Verify currency is provided as list (even single values)

#### Issue 2: Multiple E97_Monetary_Amount Nodes

**Symptoms:**
- Separate monetary amount nodes created by P70.16 and P70.17
- Data duplication

**Solutions:**
- Ensure both transformations check for existing `P177_assigned_property_of_type`
- Verify same E8_Acquisition is being used
- Check URI generation consistency
- Process P70.16 before P70.17

#### Issue 3: Currency Type Not Set

**Symptoms:**
- Currency object missing `@type: cidoc:E98_Currency`

**Solutions:**
- Check the type assignment logic in currency handling
- Verify structured objects include or receive type
- Ensure simple URIs get wrapped with proper type

#### Issue 4: Invalid Currency References

**Symptoms:**
- Errors when currency values are not proper URIs
- Type validation failures

**Solutions:**
- Implement currency URI validation
- Use controlled vocabulary for currency types
- Document expected currency reference formats
- Provide helper function for currency URI generation

### Debug Mode

Add debug output to track transformation:

```python
def transform_p70_17_documents_sale_price_currency(data, debug=False):
    """Transform with optional debug output."""
    if debug:
        print(f"Starting P70.17 transformation for: {data.get('@id', 'unknown')}")
    
    if 'gmn:P70_17_documents_sale_price_currency' not in data:
        if debug:
            print("  No P70.17 property found, skipping")
        return data
    
    # ... transformation logic ...
    
    if debug:
        print(f"  Created E97_Monetary_Amount: {monetary_amount['@id']}")
        print(f"  Added currency: {monetary_amount.get('cidoc:P180_has_currency', {}).get('@id', 'N/A')}")
    
    return data
```

### Validation Script

```python
def validate_p70_17_transformation(original, transformed):
    """Validate that P70.17 was correctly transformed."""
    errors = []
    
    # Check property was removed
    if 'gmn:P70_17_documents_sale_price_currency' in transformed:
        errors.append("Simplified property not removed")
    
    # Check E8_Acquisition exists
    if 'cidoc:P70_documents' not in transformed:
        errors.append("E8_Acquisition not created")
        return errors
    
    acquisition = transformed['cidoc:P70_documents'][0]
    
    # Check E97_Monetary_Amount exists
    if 'cidoc:P177_assigned_property_of_type' not in acquisition:
        errors.append("E97_Monetary_Amount not created")
        return errors
    
    monetary = acquisition['cidoc:P177_assigned_property_of_type']
    
    # Check currency added
    if 'cidoc:P180_has_currency' not in monetary:
        errors.append("P180_has_currency not added to monetary amount")
    else:
        currency = monetary['cidoc:P180_has_currency']
        if '@type' not in currency or currency['@type'] != 'cidoc:E98_Currency':
            errors.append("Currency type not set correctly")
        if '@id' not in currency:
            errors.append("Currency URI missing")
    
    return errors

# Usage
errors = validate_p70_17_transformation(original_data, transformed_data)
if errors:
    print("❌ Validation failed:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✓ Validation passed")
```

---

## Best Practices

1. **Always Pair with P70.16**: Document both amount and currency for complete price data
2. **Use Controlled Vocabularies**: Reference standardized currency URIs when possible
3. **Preserve Original Data**: Keep original currency references in additional properties if needed
4. **Document Currency Types**: Maintain a registry of historical currencies used
5. **Test Integration**: Always test P70.16 and P70.17 together
6. **Handle Edge Cases**: Account for missing data, multiple currencies, etc.
7. **Validate Output**: Use validation scripts to ensure correct structure

---

## Next Steps

After successful implementation:

1. Update main documentation with examples
2. Create currency vocabulary/thesaurus
3. Add to data entry guidelines
4. Train data entry staff on currency codes
5. Implement currency validation tools
6. Create currency lookup service
7. Document historical currency values
8. Build economic analysis tools

---

*For additional support, refer to the complete semantic documentation in `documents-price-currency-documentation.md`.*
