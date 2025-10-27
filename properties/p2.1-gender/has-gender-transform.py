# Python Transformation Code for gmn:P2_1_gender

## Overview

This file contains ready-to-copy Python code to implement the transformation of `gmn:P2_1_gender` (simplified gender property) to the full CIDOC-CRM `P2_has_type` structure.

---

## Implementation Instructions

### Step 1: Add the Transformation Function

**Location**: Add this function **after line 2486** in `gmn_to_cidoc_transform.py` (after the `transform_p107i_3_has_occupation` function and before the `transform_p3_1_has_editorial_note` call in `transform_item`).

**Code to Copy**:

```python
def transform_p2_1_gender(data):
    """
    Transform gmn:P2_1_gender to full CIDOC-CRM structure.
    
    Converts:
        gmn:P2_1_gender → cidoc:P2_has_type
    
    The gmn:P2_1_gender property is a simplified way to record biological sex
    characteristics using a controlled vocabulary of three Getty AAT terms:
    - aat:300189559 (male)
    - aat:300189557 (female) 
    - aat:300417544 (intersex)
    
    This function transforms it to the standard CIDOC-CRM P2_has_type pattern
    with proper E55_Type instances.
    
    Input example:
        {
            "@id": "person/p123",
            "@type": "cidoc:E21_Person",
            "gmn:P2_1_gender": {
                "@id": "aat:300189559"
            }
        }
    
    Output example:
        {
            "@id": "person/p123",
            "@type": "cidoc:E21_Person",
            "cidoc:P2_has_type": [
                {
                    "@id": "aat:300189559",
                    "@type": "cidoc:E55_Type"
                }
            ]
        }
    
    Args:
        data: Item data dictionary containing person information
        
    Returns:
        Transformed data dictionary with P2_has_type instead of P2_1_gender
    """
    # Check if the property exists
    if 'gmn:P2_1_gender' not in data:
        return data
    
    gender = data['gmn:P2_1_gender']
    
    # Handle both string and object formats
    if isinstance(gender, str):
        gender_uri = gender
    elif isinstance(gender, dict) and '@id' in gender:
        gender_uri = gender['@id']
    else:
        # Invalid format, skip transformation
        return data
    
    # Create the P2_has_type structure with E55_Type
    gender_type = {
        '@id': gender_uri,
        '@type': 'cidoc:E55_Type'
    }
    
    # Initialize cidoc:P2_has_type if it doesn't exist
    if 'cidoc:P2_has_type' not in data:
        data['cidoc:P2_has_type'] = []
    elif not isinstance(data['cidoc:P2_has_type'], list):
        # Convert single value to list
        data['cidoc:P2_has_type'] = [data['cidoc:P2_has_type']]
    
    # Add the gender type to the list
    data['cidoc:P2_has_type'].append(gender_type)
    
    # Remove the simplified property
    del data['gmn:P2_1_gender']
    
    return data
```

---

### Step 2: Add Function Call to transform_item

**Location**: In the `transform_item` function, add the function call **after line 2486** (after group membership transformations, before editorial notes).

**Code to Copy**:

```python
    # Gender
    item = transform_p2_1_gender(item)
```

**Full Context**:

```python
def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    
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
    item = transform_p70_12_documents_payment_through_organization(item)
    item = transform_p70_13_documents_referenced_place(item)
    item = transform_p70_14_documents_referenced_object(item)
    item = transform_p70_15_documents_witness(item)
    item = transform_p70_16_documents_sale_price_amount(item)
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # Arbitration properties (P70.18-P70.20)
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
    
    # Cession properties (P70.21-P70.23)
    item = transform_p70_21_indicates_conceding_party(item)
    item = transform_p70_22_indicates_receiving_party(item)
    item = transform_p70_23_indicates_object_of_cession(item)
    
    # Declaration properties (P70.24-P70.25)
    item = transform_p70_24_indicates_declarant(item)
    item = transform_p70_25_indicates_declaration_subject(item)
    
    # Correspondence properties (P70.26-P70.31)
    item = transform_p70_26_indicates_sender(item)
    item = transform_p70_27_has_address_of_origin(item)
    item = transform_p70_28_indicates_addressee(item)
    item = transform_p70_29_describes_subject(item)
    item = transform_p70_30_mentions_person(item)
    item = transform_p70_31_has_address_of_destination(item)
    
    # Donation properties (P70.32-P70.33)
    item = transform_p70_32_indicates_donor(item)
    item = transform_p70_33_indicates_object_of_donation(item)

    # Dowry properties (P70.34)
    item = transform_p70_34_indicates_object_of_dowry(item)

    # Visual representation
    item = transform_p138i_1_has_representation(item)
    
    # Person attestation and relationship properties
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)
    item = transform_p11i_3_has_spouse(item)
    
    # Property ownership and occupation
    item = transform_p22_1_has_owner(item)
    item = transform_p53_1_has_occupant(item)
    
    # Family relationships
    item = transform_p96_1_has_mother(item)
    item = transform_p97_1_has_father(item)
    
    # Group memberships
    item = transform_p107i_1_has_regional_provenance(item)
    item = transform_p107i_2_has_social_category(item)
    item = transform_p107i_3_has_occupation(item)
    
    # Gender (ADD THIS LINE HERE)
    item = transform_p2_1_gender(item)
    
    # Editorial notes (last, with optional inclusion)
    item = transform_p3_1_has_editorial_note(item, include_internal)
    
    return item
```

---

## Function Explanation

### Purpose

The `transform_p2_1_gender` function converts the simplified GMN property to the full CIDOC-CRM structure:

- **Input**: `gmn:P2_1_gender` with an AAT URI
- **Output**: `cidoc:P2_has_type` with proper E55_Type instance
- **Action**: Removes simplified property, adds CIDOC-CRM compliant structure

### Key Features

1. **Graceful Handling**: Returns data unchanged if property is missing
2. **Format Flexibility**: Handles both string and object URI formats
3. **List Management**: Properly initializes and manages P2_has_type as a list
4. **Multiple Types**: Supports persons with multiple P2_has_type values
5. **Cleanup**: Removes the simplified property from output

### Control Flow

```
1. Check if 'gmn:P2_1_gender' exists
   ├─ No: Return data unchanged
   └─ Yes: Continue to step 2

2. Extract gender URI
   ├─ String format: Use directly
   ├─ Object format: Extract from '@id'
   └─ Invalid format: Return data unchanged

3. Create E55_Type structure with gender URI

4. Initialize/prepare cidoc:P2_has_type
   ├─ Doesn't exist: Create empty list
   ├─ Is single value: Convert to list
   └─ Is already list: Use as-is

5. Append gender type to list

6. Delete gmn:P2_1_gender property

7. Return transformed data
```

---

## Testing the Implementation

### Test Script

Create a test file `test_gender_transform.py`:

```python
#!/usr/bin/env python3
"""Test script for gender transformation."""

import json
from gmn_to_cidoc_transform import transform_p2_1_gender

def test_male_gender():
    """Test transformation of male gender."""
    input_data = {
        "@id": "person/p001",
        "@type": "cidoc:E21_Person",
        "gmn:P2_1_gender": {
            "@id": "aat:300189559"
        }
    }
    
    result = transform_p2_1_gender(input_data)
    
    assert 'gmn:P2_1_gender' not in result
    assert 'cidoc:P2_has_type' in result
    assert isinstance(result['cidoc:P2_has_type'], list)
    assert len(result['cidoc:P2_has_type']) == 1
    assert result['cidoc:P2_has_type'][0]['@id'] == 'aat:300189559'
    assert result['cidoc:P2_has_type'][0]['@type'] == 'cidoc:E55_Type'
    
    print("✓ Male gender test passed")

def test_female_gender():
    """Test transformation of female gender."""
    input_data = {
        "@id": "person/p002",
        "@type": "cidoc:E21_Person",
        "gmn:P2_1_gender": {
            "@id": "aat:300189557"
        }
    }
    
    result = transform_p2_1_gender(input_data)
    
    assert 'gmn:P2_1_gender' not in result
    assert result['cidoc:P2_has_type'][0]['@id'] == 'aat:300189557'
    
    print("✓ Female gender test passed")

def test_intersex_gender():
    """Test transformation of intersex gender."""
    input_data = {
        "@id": "person/p003",
        "@type": "cidoc:E21_Person",
        "gmn:P2_1_gender": {
            "@id": "aat:300417544"
        }
    }
    
    result = transform_p2_1_gender(input_data)
    
    assert 'gmn:P2_1_gender' not in result
    assert result['cidoc:P2_has_type'][0]['@id'] == 'aat:300417544'
    
    print("✓ Intersex gender test passed")

def test_missing_gender():
    """Test handling of missing gender property."""
    input_data = {
        "@id": "person/p004",
        "@type": "cidoc:E21_Person"
    }
    
    result = transform_p2_1_gender(input_data)
    
    assert 'gmn:P2_1_gender' not in result
    assert 'cidoc:P2_has_type' not in result
    
    print("✓ Missing gender test passed")

def test_multiple_types():
    """Test person with existing P2_has_type."""
    input_data = {
        "@id": "person/p005",
        "@type": "cidoc:E21_Person",
        "cidoc:P2_has_type": [
            {
                "@id": "aat:300025565",  # scholar
                "@type": "cidoc:E55_Type"
            }
        ],
        "gmn:P2_1_gender": {
            "@id": "aat:300189559"
        }
    }
    
    result = transform_p2_1_gender(input_data)
    
    assert 'gmn:P2_1_gender' not in result
    assert len(result['cidoc:P2_has_type']) == 2
    assert result['cidoc:P2_has_type'][1]['@id'] == 'aat:300189559'
    
    print("✓ Multiple types test passed")

def test_string_format():
    """Test string URI format."""
    input_data = {
        "@id": "person/p006",
        "@type": "cidoc:E21_Person",
        "gmn:P2_1_gender": "aat:300189559"
    }
    
    result = transform_p2_1_gender(input_data)
    
    assert 'gmn:P2_1_gender' not in result
    assert result['cidoc:P2_has_type'][0]['@id'] == 'aat:300189559'
    
    print("✓ String format test passed")

if __name__ == '__main__':
    print("Running gender transformation tests...\n")
    
    test_male_gender()
    test_female_gender()
    test_intersex_gender()
    test_missing_gender()
    test_multiple_types()
    test_string_format()
    
    print("\n✓ All tests passed!")
```

**Run tests**:
```bash
python test_gender_transform.py
```

---

## Integration Verification

### Verify Function Exists

```bash
grep -n "def transform_p2_1_gender" gmn_to_cidoc_transform.py
```

**Expected output**: Should show line number where function is defined (around line 2487)

### Verify Function Call

```bash
grep -n "transform_p2_1_gender(item)" gmn_to_cidoc_transform.py
```

**Expected output**: Should show line number in `transform_item` function (around line 2488)

### Verify Integration Order

```bash
grep -B 2 -A 2 "transform_p2_1_gender" gmn_to_cidoc_transform.py
```

**Expected output**:
```python
    item = transform_p107i_3_has_occupation(item)
    
    # Gender
    item = transform_p2_1_gender(item)
    
    # Editorial notes
```

---

## Complete Test Data

### Test Input File

**File**: `test_gender_input.json`

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "https://data.geniza.org/ontology/",
    "aat": "http://vocab.getty.edu/page/aat/"
  },
  "@graph": [
    {
      "@id": "person/male-example",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Abraham ben Moses",
      "gmn:P2_1_gender": {
        "@id": "aat:300189559"
      }
    },
    {
      "@id": "person/female-example",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Esther bat David",
      "gmn:P2_1_gender": {
        "@id": "aat:300189557"
      }
    },
    {
      "@id": "person/intersex-example",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Person Name",
      "gmn:P2_1_gender": {
        "@id": "aat:300417544"
      }
    },
    {
      "@id": "person/no-gender",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Unknown Person"
    },
    {
      "@id": "person/multiple-types",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Scholar Name",
      "gmn:P2_1_gender": {
        "@id": "aat:300189559"
      },
      "gmn:P107i_3_has_occupation": "scholar"
    }
  ]
}
```

### Run Transformation

```bash
python gmn_to_cidoc_transform.py test_gender_input.json test_gender_output.json
```

### Verify Output

```bash
# Check transformation success
echo $?  # Should output 0

# View formatted output
python -m json.tool test_gender_output.json | less

# Count transformed types
grep -c '"cidoc:P2_has_type"' test_gender_output.json

# Verify no simplified properties remain
grep -c '"gmn:P2_1_gender"' test_gender_output.json  # Should be 0
```

---

## Error Handling

The function includes error handling for common issues:

### Invalid Format

**Input**:
```json
{
  "gmn:P2_1_gender": ["invalid", "array"]
}
```

**Behavior**: Returns data unchanged, skips transformation

### Missing @id

**Input**:
```json
{
  "gmn:P2_1_gender": {
    "value": "aat:300189559"
  }
}
```

**Behavior**: Returns data unchanged, skips transformation

### None Value

**Input**:
```json
{
  "gmn:P2_1_gender": null
}
```

**Behavior**: Returns data unchanged, skips transformation

---

## Performance Considerations

### Efficiency

- **Time Complexity**: O(1) - constant time operation
- **Space Complexity**: O(1) - minimal additional memory
- **Scalability**: Handles large datasets efficiently

### Optimization

The function is optimized for:
- Quick property checks
- Minimal dictionary operations
- Efficient list management
- Clean memory usage (deletes unused properties)

---

## Common Issues and Solutions

### Issue 1: Property Not Transforming

**Symptom**: `gmn:P2_1_gender` still appears in output

**Possible Causes**:
1. Function not called in `transform_item`
2. Function called after output is finalized
3. Syntax error in function

**Solution**: Verify function placement and check for errors

### Issue 2: Missing @type

**Symptom**: Gender type lacks `@type: "cidoc:E55_Type"`

**Cause**: Type assignment missing in function

**Solution**: Verify this line exists:
```python
gender_type = {
    '@id': gender_uri,
    '@type': 'cidoc:E55_Type'  # This line must be present
}
```

### Issue 3: List Conversion Error

**Symptom**: TypeError when appending to P2_has_type

**Cause**: Existing P2_has_type is not a list

**Solution**: Verify list initialization code:
```python
if 'cidoc:P2_has_type' not in data:
    data['cidoc:P2_has_type'] = []
elif not isinstance(data['cidoc:P2_has_type'], list):
    data['cidoc:P2_has_type'] = [data['cidoc:P2_has_type']]
```

---

## Documentation Updates

After implementing the transformation, update these files:

### 1. Script Docstring

Add to the main script docstring:

```python
"""
GMN to CIDOC-CRM Transformation Script
...
Supported Properties:
...
- gmn:P2_1_gender: Person biological sex (controlled vocabulary)
...
"""
```

### 2. Main Function Help Text

Update in the `main()` function:

```python
print("\nSupported person properties:")
print("  - gmn:P1_1_has_name, gmn:P1_2_has_name_from_source, ...")
print("  - gmn:P2_1_gender (biological sex with controlled vocabulary)")
print("  - gmn:P11i_1_earliest_attestation_date, ...")
```

### 3. README or CHANGELOG

```markdown
## Version X.X (2025-10-26)

### New Features
- Added transformation for gmn:P2_1_gender property
  - Converts to cidoc:P2_has_type with E55_Type instances
  - Supports three Getty AAT terms: male, female, intersex
  - Maintains compatibility with other P2_has_type values
```

---

## Validation Checklist

Use this checklist after implementation:

- [ ] Function `transform_p2_1_gender` created
- [ ] Function placed after line 2486
- [ ] Function called in `transform_item`
- [ ] Call placed before editorial notes transformation
- [ ] No Python syntax errors
- [ ] All test cases pass
- [ ] Male gender transforms correctly
- [ ] Female gender transforms correctly
- [ ] Intersex transforms correctly
- [ ] Missing gender handled gracefully
- [ ] Multiple types work together
- [ ] String format URIs handled
- [ ] Object format URIs handled
- [ ] E55_Type added to output
- [ ] gmn:P2_1_gender removed from output
- [ ] Documentation updated

---

## Summary

This file provides all the Python code needed to implement gender property transformation:

1. **Main function**: `transform_p2_1_gender(data)`
2. **Integration**: Add function call to `transform_item`
3. **Testing**: Comprehensive test script included
4. **Verification**: Commands to check implementation
5. **Error handling**: Robust handling of edge cases

**Copy the code blocks above into your transformation script to enable gender property support.**

---

*This Python code follows GMN project coding standards and integrates seamlessly with the existing transformation pipeline.*
