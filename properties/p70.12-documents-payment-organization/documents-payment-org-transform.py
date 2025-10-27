# GMN Ontology: P70.12 Documents Payment Through Organization
## Python Additions for gmn_to_cidoc_transform.py

This file contains ready-to-copy Python code to add to the transformation script.

---

## INSTRUCTIONS FOR USE

1. Open the file `gmn_to_cidoc_transform.py`
2. Locate the `transform_p70_11_documents_referenced_person()` function
3. Insert the new function immediately after it
4. Locate the `transform_gmn_to_cidoc()` function
5. Add the function call in the appropriate location (after P70.11, before P70.13)
6. Test the transformation with sample data
7. Commit changes to version control

---

## TRANSFORMATION FUNCTION

Copy and paste this complete function into `gmn_to_cidoc_transform.py`:

```python
def transform_p70_12_documents_payment_through_organization(data):
    """
    Transform gmn:P70_12_documents_payment_through_organization to full CIDOC-CRM structure:
    P67_refers_to > E74_Group
    """
    if 'gmn:P70_12_documents_payment_through_organization' not in data:
        return data
    
    organizations = data['gmn:P70_12_documents_payment_through_organization']
    
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
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
    
    del data['gmn:P70_12_documents_payment_through_organization']
    return data
```

---

## FUNCTION PLACEMENT

The function should be inserted in this location:

```python
def transform_p70_11_documents_referenced_person(data):
    """
    Transform gmn:P70_11_documents_referenced_person to full CIDOC-CRM structure:
    P67_refers_to > E21_Person
    """
    if 'gmn:P70_11_documents_referenced_person' not in data:
        return data
    
    persons = data['gmn:P70_11_documents_referenced_person']
    
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    for person_obj in persons:
        if isinstance(person_obj, dict):
            person_data = person_obj.copy()
            if '@type' not in person_data:
                person_data['@type'] = 'cidoc:E21_Person'
        else:
            person_uri = str(person_obj)
            person_data = {
                '@id': person_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        data['cidoc:P67_refers_to'].append(person_data)
    
    del data['gmn:P70_11_documents_referenced_person']
    return data


def transform_p70_12_documents_payment_through_organization(data):
    """
    Transform gmn:P70_12_documents_payment_through_organization to full CIDOC-CRM structure:
    P67_refers_to > E74_Group
    """
    if 'gmn:P70_12_documents_payment_through_organization' not in data:
        return data
    
    organizations = data['gmn:P70_12_documents_payment_through_organization']
    
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
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
    
    del data['gmn:P70_12_documents_payment_through_organization']
    return data


def transform_p70_13_documents_referenced_place(data):
    """
    Transform gmn:P70_13_documents_referenced_place to full CIDOC-CRM structure:
    P67_refers_to > E53_Place
    """
    # ... rest of function ...
```

---

## PIPELINE INTEGRATION

Add the function call to `transform_gmn_to_cidoc()`:

```python
def transform_gmn_to_cidoc(item, include_internal=False):
    """
    Transform GMN shortcut properties to full CIDOC-CRM structure.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    
    Returns:
        Transformed item dictionary
    """
    # Name and title properties
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    item = transform_p1_3_has_patrilineal_name(item)
    item = transform_p1_4_has_loconym(item)
    item = transform_p102_1_has_title(item)
    
    # Creation properties (notary, date, place)
    item = transform_p94i_1_was_created_by(item)
    item = transform_p94i_2_has_enactment_date(item)
    item = transform_p94i_3_has_place_of_enactment(item)
    
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
    item = transform_p70_12_documents_payment_through_organization(item)  # ADD THIS LINE
    item = transform_p70_13_documents_referenced_place(item)
    item = transform_p70_14_documents_referenced_object(item)
    item = transform_p70_15_documents_witness(item)
    item = transform_p70_16_documents_sale_price_amount(item)
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # ... rest of pipeline ...
```

---

## FUNCTION BREAKDOWN

### Function Signature
```python
def transform_p70_12_documents_payment_through_organization(data):
```
- Function name follows naming convention
- Takes `data` dictionary as parameter
- Returns modified `data` dictionary

### Documentation String
```python
    """
    Transform gmn:P70_12_documents_payment_through_organization to full CIDOC-CRM structure:
    P67_refers_to > E74_Group
    """
```
- Explains transformation target
- Documents the CIDOC-CRM path created
- Follows project documentation style

### Early Return Check
```python
    if 'gmn:P70_12_documents_payment_through_organization' not in data:
        return data
```
- Checks if property exists
- Returns unmodified data if property not present
- Prevents KeyError exceptions

### Extract Organizations
```python
    organizations = data['gmn:P70_12_documents_payment_through_organization']
```
- Extracts organization list from data
- Assumes list format (array of organizations)

### Initialize P67 Array
```python
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
```
- Creates P67_refers_to array if it doesn't exist
- Preserves existing P67_refers_to values
- Allows multiple entities to be referenced

### Process Each Organization
```python
    for org_obj in organizations:
```
- Iterates through all organizations in list
- Handles multiple organizations per contract

### Handle Dictionary Format
```python
        if isinstance(org_obj, dict):
            org_data = org_obj.copy()
            if '@type' not in org_data:
                org_data['@type'] = 'cidoc:E74_Group'
```
- Checks if organization is inline object (dict)
- Creates copy to avoid modifying original
- Adds E74_Group type if missing
- Preserves other properties (names, identifiers, etc.)

### Handle URI Format
```python
        else:
            org_uri = str(org_obj)
            org_data = {
                '@id': org_uri,
                '@type': 'cidoc:E74_Group'
            }
```
- Handles simple URI reference format
- Converts to string in case of URI object
- Creates minimal object with ID and type
- Ensures consistent structure

### Append to P67
```python
        data['cidoc:P67_refers_to'].append(org_data)
```
- Adds organization to reference list
- Uses append to preserve existing references
- Allows multiple organizations and other referenced entities

### Remove Original Property
```python
    del data['gmn:P70_12_documents_payment_through_organization']
```
- Removes GMN shortcut property
- Ensures clean CIDOC-CRM output
- Prevents property duplication

### Return Result
```python
    return data
```
- Returns modified data dictionary
- Enables function chaining in pipeline

---

## TEST CASES

### Test 1: Simple Organization URI

**Input:**
```python
test_data = {
    '@id': 'http://example.org/contract/001',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_12_documents_payment_through_organization': [
        'http://example.org/org/banco_san_giorgio'
    ]
}
```

**Expected Output:**
```python
{
    '@id': 'http://example.org/contract/001',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P67_refers_to': [
        {
            '@id': 'http://example.org/org/banco_san_giorgio',
            '@type': 'cidoc:E74_Group'
        }
    ]
}
```

**Test Code:**
```python
result = transform_p70_12_documents_payment_through_organization(test_data)
assert 'gmn:P70_12_documents_payment_through_organization' not in result
assert 'cidoc:P67_refers_to' in result
assert len(result['cidoc:P67_refers_to']) == 1
assert result['cidoc:P67_refers_to'][0]['@type'] == 'cidoc:E74_Group'
```

### Test 2: Inline Organization Data

**Input:**
```python
test_data = {
    '@id': 'http://example.org/contract/002',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_12_documents_payment_through_organization': [
        {
            '@id': 'http://example.org/org/banco_san_giorgio',
            'cidoc:P1_is_identified_by': {
                '@type': 'cidoc:E41_Appellation',
                'cidoc:P190_has_symbolic_content': 'Banco di San Giorgio'
            }
        }
    ]
}
```

**Expected Output:**
```python
{
    '@id': 'http://example.org/contract/002',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P67_refers_to': [
        {
            '@id': 'http://example.org/org/banco_san_giorgio',
            '@type': 'cidoc:E74_Group',
            'cidoc:P1_is_identified_by': {
                '@type': 'cidoc:E41_Appellation',
                'cidoc:P190_has_symbolic_content': 'Banco di San Giorgio'
            }
        }
    ]
}
```

**Test Code:**
```python
result = transform_p70_12_documents_payment_through_organization(test_data)
assert result['cidoc:P67_refers_to'][0]['@type'] == 'cidoc:E74_Group'
assert 'cidoc:P1_is_identified_by' in result['cidoc:P67_refers_to'][0]
```

### Test 3: Multiple Organizations

**Input:**
```python
test_data = {
    '@id': 'http://example.org/contract/003',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_12_documents_payment_through_organization': [
        'http://example.org/org/banco_san_giorgio',
        'http://example.org/org/casa_credito_genova'
    ]
}
```

**Expected Output:**
```python
{
    '@id': 'http://example.org/contract/003',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P67_refers_to': [
        {
            '@id': 'http://example.org/org/banco_san_giorgio',
            '@type': 'cidoc:E74_Group'
        },
        {
            '@id': 'http://example.org/org/casa_credito_genova',
            '@type': 'cidoc:E74_Group'
        }
    ]
}
```

**Test Code:**
```python
result = transform_p70_12_documents_payment_through_organization(test_data)
assert len(result['cidoc:P67_refers_to']) == 2
assert all(org['@type'] == 'cidoc:E74_Group' for org in result['cidoc:P67_refers_to'])
```

### Test 4: Empty Organization List

**Input:**
```python
test_data = {
    '@id': 'http://example.org/contract/004',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_12_documents_payment_through_organization': []
}
```

**Expected Output:**
```python
{
    '@id': 'http://example.org/contract/004',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P67_refers_to': []
}
```

**Test Code:**
```python
result = transform_p70_12_documents_payment_through_organization(test_data)
assert 'cidoc:P67_refers_to' in result
assert len(result['cidoc:P67_refers_to']) == 0
```

### Test 5: Property Not Present

**Input:**
```python
test_data = {
    '@id': 'http://example.org/contract/005',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_1_documents_seller': 'http://example.org/person/giovanni'
}
```

**Expected Output:**
```python
{
    '@id': 'http://example.org/contract/005',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_1_documents_seller': 'http://example.org/person/giovanni'
}
```

**Test Code:**
```python
result = transform_p70_12_documents_payment_through_organization(test_data)
assert result == test_data  # No changes
```

### Test 6: Existing P67_refers_to

**Input:**
```python
test_data = {
    '@id': 'http://example.org/contract/006',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P67_refers_to': [
        {
            '@id': 'http://example.org/person/marco',
            '@type': 'cidoc:E21_Person'
        }
    ],
    'gmn:P70_12_documents_payment_through_organization': [
        'http://example.org/org/banco_san_giorgio'
    ]
}
```

**Expected Output:**
```python
{
    '@id': 'http://example.org/contract/006',
    '@type': 'gmn:E31_2_Sales_Contract',
    'cidoc:P67_refers_to': [
        {
            '@id': 'http://example.org/person/marco',
            '@type': 'cidoc:E21_Person'
        },
        {
            '@id': 'http://example.org/org/banco_san_giorgio',
            '@type': 'cidoc:E74_Group'
        }
    ]
}
```

**Test Code:**
```python
result = transform_p70_12_documents_payment_through_organization(test_data)
assert len(result['cidoc:P67_refers_to']) == 2
assert result['cidoc:P67_refers_to'][0]['@type'] == 'cidoc:E21_Person'
assert result['cidoc:P67_refers_to'][1]['@type'] == 'cidoc:E74_Group'
```

---

## COMPLETE TEST SUITE

```python
import json
from gmn_to_cidoc_transform import transform_p70_12_documents_payment_through_organization

def test_p70_12_transformations():
    """Comprehensive test suite for P70.12 transformation."""
    
    print("Testing P70.12 Transformation Function")
    print("=" * 60)
    
    # Test 1: URI reference
    print("\nTest 1: Simple URI reference")
    test1 = {
        '@id': 'http://example.org/contract/001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_12_documents_payment_through_organization': [
            'http://example.org/org/banco_san_giorgio'
        ]
    }
    result1 = transform_p70_12_documents_payment_through_organization(test1)
    assert 'gmn:P70_12_documents_payment_through_organization' not in result1
    assert 'cidoc:P67_refers_to' in result1
    assert len(result1['cidoc:P67_refers_to']) == 1
    assert result1['cidoc:P67_refers_to'][0]['@type'] == 'cidoc:E74_Group'
    print("✓ Passed")
    
    # Test 2: Inline data
    print("\nTest 2: Inline organization data")
    test2 = {
        '@id': 'http://example.org/contract/002',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_12_documents_payment_through_organization': [
            {
                '@id': 'http://example.org/org/banco',
                'cidoc:P1_is_identified_by': {
                    '@type': 'cidoc:E41_Appellation',
                    'cidoc:P190_has_symbolic_content': 'Banco'
                }
            }
        ]
    }
    result2 = transform_p70_12_documents_payment_through_organization(test2)
    assert result2['cidoc:P67_refers_to'][0]['@type'] == 'cidoc:E74_Group'
    assert 'cidoc:P1_is_identified_by' in result2['cidoc:P67_refers_to'][0]
    print("✓ Passed")
    
    # Test 3: Multiple organizations
    print("\nTest 3: Multiple organizations")
    test3 = {
        '@id': 'http://example.org/contract/003',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_12_documents_payment_through_organization': [
            'http://example.org/org/banco1',
            'http://example.org/org/banco2'
        ]
    }
    result3 = transform_p70_12_documents_payment_through_organization(test3)
    assert len(result3['cidoc:P67_refers_to']) == 2
    print("✓ Passed")
    
    # Test 4: Property not present
    print("\nTest 4: Property not present")
    test4 = {
        '@id': 'http://example.org/contract/004',
        '@type': 'gmn:E31_2_Sales_Contract'
    }
    result4 = transform_p70_12_documents_payment_through_organization(test4)
    assert result4 == test4
    print("✓ Passed")
    
    # Test 5: Existing P67_refers_to
    print("\nTest 5: Existing P67_refers_to preservation")
    test5 = {
        '@id': 'http://example.org/contract/005',
        '@type': 'gmn:E31_2_Sales_Contract',
        'cidoc:P67_refers_to': [
            {'@id': 'http://example.org/person/marco', '@type': 'cidoc:E21_Person'}
        ],
        'gmn:P70_12_documents_payment_through_organization': [
            'http://example.org/org/banco'
        ]
    }
    result5 = transform_p70_12_documents_payment_through_organization(test5)
    assert len(result5['cidoc:P67_refers_to']) == 2
    assert result5['cidoc:P67_refers_to'][0]['@type'] == 'cidoc:E21_Person'
    assert result5['cidoc:P67_refers_to'][1]['@type'] == 'cidoc:E74_Group'
    print("✓ Passed")
    
    print("\n" + "=" * 60)
    print("All tests passed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    test_p70_12_transformations()
```

---

## DEBUGGING TIPS

### Add Debug Output

```python
def transform_p70_12_documents_payment_through_organization(data):
    """..."""
    # Add debug print
    print(f"DEBUG: Processing P70.12 for {data.get('@id', 'unknown')}")
    
    if 'gmn:P70_12_documents_payment_through_organization' not in data:
        print("DEBUG: P70.12 property not found")
        return data
    
    organizations = data['gmn:P70_12_documents_payment_through_organization']
    print(f"DEBUG: Found {len(organizations)} organization(s)")
    
    # ... rest of function ...
```

### Check Intermediate Values

```python
for org_obj in organizations:
    print(f"DEBUG: Processing org: {org_obj}")
    
    if isinstance(org_obj, dict):
        print(f"DEBUG: Org is dict with keys: {org_obj.keys()}")
        org_data = org_obj.copy()
        # ...
```

### Validate Output Structure

```python
# Before returning
print("DEBUG: Final P67_refers_to:", data.get('cidoc:P67_refers_to'))
return data
```

---

## PERFORMANCE CONSIDERATIONS

### Time Complexity
- **O(n)** where n = number of organizations
- Linear iteration through organization list
- Each organization processed once

### Space Complexity
- **O(n)** additional space for organization copies
- P67_refers_to list grows with number of organizations
- Minimal overhead from type checking

### Optimization Notes
- Function is already optimized for typical use cases
- Dictionary copy prevents accidental mutations
- Early return avoids unnecessary processing

---

## VERSION CONTROL

### Git Commit Message
```
Add P70.12 transformation function

- Add transform_p70_12_documents_payment_through_organization()
- Transforms organization references to P67_refers_to
- Handles both URI and inline object formats
- Preserves existing P67_refers_to values
- Integrate into transform_gmn_to_cidoc() pipeline
```

### File Diff Preview
```diff
 def transform_p70_11_documents_referenced_person(data):
     """..."""
     # ... function body ...
     return data
 
+
+def transform_p70_12_documents_payment_through_organization(data):
+    """
+    Transform gmn:P70_12_documents_payment_through_organization to full CIDOC-CRM structure:
+    P67_refers_to > E74_Group
+    """
+    if 'gmn:P70_12_documents_payment_through_organization' not in data:
+        return data
+    
+    organizations = data['gmn:P70_12_documents_payment_through_organization']
+    
+    if 'cidoc:P67_refers_to' not in data:
+        data['cidoc:P67_refers_to'] = []
+    
+    for org_obj in organizations:
+        if isinstance(org_obj, dict):
+            org_data = org_obj.copy()
+            if '@type' not in org_data:
+                org_data['@type'] = 'cidoc:E74_Group'
+        else:
+            org_uri = str(org_obj)
+            org_data = {
+                '@id': org_uri,
+                '@type': 'cidoc:E74_Group'
+            }
+        
+        data['cidoc:P67_refers_to'].append(org_data)
+    
+    del data['gmn:P70_12_documents_payment_through_organization']
+    return data
+
 
 def transform_p70_13_documents_referenced_place(data):
     """..."""
```

---

*Python Additions Version 1.0 - Created 2025-10-27*
