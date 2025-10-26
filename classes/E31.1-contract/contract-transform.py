# E31.1 General Contract - Python Transformation Reference

## Overview

This file provides reference information about Python transformation functions for gmn:E31_1_Contract in the GMN to CIDOC-CRM transformation script.

**IMPORTANT**: Unlike Python additions files for specialized contract types (such as dowry or donation contracts), this file does NOT contain new transformation functions to add. The E31_1_Contract class uses standard document property transformations that are ALREADY DEFINED in gmn_to_cidoc_transform.py.

This file serves as a **reference** explaining which existing transformation functions apply to E31_1_Contract and why no specialized transformations are needed.

## Status: No New Functions Needed ✓

- **Transformation Functions**: Uses existing standard document transformations
- **Location**: gmn_to_cidoc_transform.py (existing functions)
- **Action Required**: None - no new functions needed
- **Reason**: E31_1_Contract has no specialized properties unique to it

## Why No Specialized Transformations?

E31_1_Contract differs from specialized contract types (Sales, Donation, Dowry, etc.) in a fundamental way:

### General Contract (E31_1_Contract)
- **Properties**: Only uses inherited document properties
- **No Specialized Properties**: No properties unique to general contracts
- **Transformations**: Uses existing functions for P1.1, P94i.1, P94i.2, etc.
- **Result**: No new transformation functions required

### Specialized Contract Types (E31.2, E31.7, E31.8, etc.)
- **Properties**: Add specialized properties (seller, buyer, donor, etc.)
- **Unique Properties**: Properties specific to their transaction type
- **Transformations**: Require specialized transformation functions
- **Result**: New transformation functions are defined for each type

## Existing Transformation Functions

The following existing functions in gmn_to_cidoc_transform.py apply to E31_1_Contract:

### 1. Name/Title Transformations

```python
def transform_p1_1_has_name(data):
    """
    Transform gmn:P1_1_has_name to full CIDOC-CRM structure.
    
    Applies to: All E1_CRM_Entity instances, including E31_1_Contract
    
    Input: gmn:P1_1_has_name "Contract Name"
    Output: cidoc:P1_is_identified_by > E41_Appellation > P190_has_symbolic_content
    """
    return transform_name_property(data, 'gmn:P1_1_has_name', AAT_NAME)


def transform_p102_1_has_title(data):
    """
    Transform gmn:P102_1_has_title to full CIDOC-CRM structure.
    
    Applies to: All E71_Human-Made_Thing instances, including E31_1_Contract
    
    Input: gmn:P102_1_has_title "Contractus Venditionis"@la
    Output: cidoc:P102_has_title > E35_Title > P190_has_symbolic_content
    """
    if 'gmn:P102_1_has_title' not in data:
        return data
    
    # Implementation details in gmn_to_cidoc_transform.py
    pass
```

### 2. Creation Property Transformations

```python
def transform_p94i_1_was_created_by(data):
    """
    Transform gmn:P94i_1_was_created_by to full CIDOC-CRM structure.
    
    Applies to: All E31_Document instances, including E31_1_Contract
    
    Input: gmn:P94i_1_was_created_by <notary_resource>
    Output: cidoc:P94i_was_created_by > E65_Creation > P14_carried_out_by
    """
    if 'gmn:P94i_1_was_created_by' not in data:
        return data
    
    # Implementation details in gmn_to_cidoc_transform.py
    pass


def transform_p94i_2_has_enactment_date(data):
    """
    Transform gmn:P94i_2_has_enactment_date to full CIDOC-CRM structure.
    
    Applies to: All E31_Document instances, including E31_1_Contract
    
    Input: gmn:P94i_2_has_enactment_date "1450-03-15"^^xsd:date
    Output: cidoc:P94i_was_created_by > E65_Creation > P4_has_time-span > 
            E52_Time-Span > P82_at_some_time_within
    """
    if 'gmn:P94i_2_has_enactment_date' not in data:
        return data
    
    # Implementation details in gmn_to_cidoc_transform.py
    pass


def transform_p94i_3_has_place_of_enactment(data):
    """
    Transform gmn:P94i_3_has_place_of_enactment to full CIDOC-CRM structure.
    
    Applies to: All E31_Document instances, including E31_1_Contract
    
    Input: gmn:P94i_3_has_place_of_enactment <place_resource>
    Output: cidoc:P94i_was_created_by > E65_Creation > P7_took_place_at
    """
    if 'gmn:P94i_3_has_place_of_enactment' not in data:
        return data
    
    # Implementation details in gmn_to_cidoc_transform.py
    pass
```

### 3. Context Property Transformations

```python
def transform_p46i_1_is_contained_in(data):
    """
    Transform gmn:P46i_1_is_contained_in to full CIDOC-CRM structure.
    
    Applies to: All E18_Physical_Thing instances, including E31_1_Contract
    
    Input: gmn:P46i_1_is_contained_in <register_resource>
    Output: cidoc:P46i_forms_part_of
    """
    if 'gmn:P46i_1_is_contained_in' not in data:
        return data
    
    # Implementation details in gmn_to_cidoc_transform.py
    pass
```

### 4. Annotation Property Transformations

```python
def transform_p3_1_has_editorial_note(data):
    """
    Transform gmn:P3_1_has_editorial_note to full CIDOC-CRM structure.
    
    Applies to: All E1_CRM_Entity instances, including E31_1_Contract
    
    Input: gmn:P3_1_has_editorial_note "Editorial comment"
    Output: cidoc:P67i_is_referred_to_by > E33_Linguistic_Object > 
            P2_has_type <AAT_EDITORIAL_NOTE> > P190_has_symbolic_content
    """
    if 'gmn:P3_1_has_editorial_note' not in data:
        return data
    
    # Implementation details in gmn_to_cidoc_transform.py
    pass
```

## Main Transformation Function

The main transformation function in gmn_to_cidoc_transform.py processes items based on their type:

```python
def transform_item(item):
    """
    Main transformation function that applies appropriate transformations 
    based on item type.
    
    For E31_1_Contract:
    - Applies standard document property transformations
    - Does NOT apply specialized contract transformations
    - Specialized contracts are handled by their own type checks
    """
    
    # Get item types
    types = item.get('@type', [])
    if isinstance(types, str):
        types = [types]
    
    # Apply standard transformations for all documents
    if any(t for t in types if 'E31' in t):  # Any E31 document type
        item = transform_p1_1_has_name(item)
        item = transform_p102_1_has_title(item)
        item = transform_p94i_1_was_created_by(item)
        item = transform_p94i_2_has_enactment_date(item)
        item = transform_p94i_3_has_place_of_enactment(item)
        item = transform_p46i_1_is_contained_in(item)
        item = transform_p3_1_has_editorial_note(item)
    
    # Apply specialized transformations based on specific type
    if 'gmn:E31_2_Sales_Contract' in types:
        item = transform_sales_contract(item)
    
    elif 'gmn:E31_3_Arbitration_Agreement' in types:
        item = transform_arbitration_agreement(item)
    
    elif 'gmn:E31_7_Donation_Contract' in types:
        item = transform_donation_contract(item)
    
    elif 'gmn:E31_8_Dowry_Contract' in types:
        item = transform_dowry_contract(item)
    
    # Note: E31_1_Contract has no 'elif' branch because it only uses
    # the standard transformations applied above
    
    return item
```

## Specialized Contract Transformations

For comparison, here's how specialized contract types add their own transformations:

### Sales Contract Transformations (E31.2)

```python
def transform_sales_contract(data):
    """
    Transform sales contract specific properties.
    
    Only applies to: gmn:E31_2_Sales_Contract
    
    Transforms:
    - P70.14 indicates seller
    - P70.15 indicates buyer  
    - P70.16 documents sale price amount
    - P70.17 documents sale price currency
    """
    data = transform_p70_14_indicates_seller(data)
    data = transform_p70_15_indicates_buyer(data)
    data = transform_p70_16_documents_sale_price(data)
    return data


def transform_p70_14_indicates_seller(data):
    """Transform P70.14 to CIDOC-CRM structure."""
    # Creates E8_Acquisition with P23_transferred_title_from
    pass
```

### Donation Contract Transformations (E31.7)

```python
def transform_donation_contract(data):
    """
    Transform donation contract specific properties.
    
    Only applies to: gmn:E31_7_Donation_Contract
    
    Transforms:
    - P70.32 indicates donor
    - P70.22 indicates receiving party
    - P70.33 indicates object of donation
    """
    data = transform_p70_32_indicates_donor(data)
    data = transform_p70_22_indicates_receiving_party(data)
    data = transform_p70_33_indicates_object_of_donation(data)
    return data


def transform_p70_32_indicates_donor(data):
    """Transform P70.32 to CIDOC-CRM structure."""
    # Creates E8_Acquisition with P23_transferred_title_from
    pass
```

### Dowry Contract Transformations (E31.8)

```python
def transform_dowry_contract(data):
    """
    Transform dowry contract specific properties.
    
    Only applies to: gmn:E31_8_Dowry_Contract
    
    Transforms:
    - P70.32 indicates donor (shared with donations)
    - P70.22 indicates receiving party (shared)
    - P70.34 indicates object of dowry (unique)
    """
    data = transform_p70_32_indicates_donor(data)
    data = transform_p70_22_indicates_receiving_party(data)
    data = transform_p70_34_indicates_object_of_dowry(data)
    return data


def transform_p70_34_indicates_object_of_dowry(data):
    """Transform P70.34 to CIDOC-CRM structure."""
    # Creates E8_Acquisition with P24_transferred_title_of
    pass
```

## Transformation Example

### Input: General Contract (E31_1_Contract)

```json
{
    "@id": "http://example.org/contract/misc001",
    "@type": "gmn:E31_1_Contract",
    "gmn:P1_1_has_name": "Unclassified contract from 1450",
    "gmn:P94i_1_was_created_by": {
        "@id": "http://example.org/person/notary_giovanni"
    },
    "gmn:P94i_2_has_enactment_date": "1450-05-20",
    "gmn:P94i_3_has_place_of_enactment": {
        "@id": "http://example.org/place/genoa"
    },
    "gmn:P46i_1_is_contained_in": {
        "@id": "http://example.org/register/1450_may"
    }
}
```

### Output: CIDOC-CRM Compliant

```json
{
    "@id": "http://example.org/contract/misc001",
    "@type": "gmn:E31_1_Contract",
    "cidoc:P1_is_identified_by": {
        "@id": "http://example.org/contract/misc001/appellation/abc123",
        "@type": "cidoc:E41_Appellation",
        "cidoc:P2_has_type": {
            "@id": "http://vocab.getty.edu/page/aat/300404650",
            "@type": "cidoc:E55_Type"
        },
        "cidoc:P190_has_symbolic_content": "Unclassified contract from 1450"
    },
    "cidoc:P94i_was_created_by": {
        "@id": "http://example.org/contract/misc001/creation",
        "@type": "cidoc:E65_Creation",
        "cidoc:P14_carried_out_by": {
            "@id": "http://example.org/person/notary_giovanni"
        },
        "cidoc:P4_has_time-span": {
            "@id": "http://example.org/contract/misc001/creation/timespan",
            "@type": "cidoc:E52_Time-Span",
            "cidoc:P82_at_some_time_within": "1450-05-20"
        },
        "cidoc:P7_took_place_at": {
            "@id": "http://example.org/place/genoa"
        }
    },
    "cidoc:P46i_forms_part_of": {
        "@id": "http://example.org/register/1450_may"
    }
}
```

**Note**: Only standard transformations applied - no specialized contract properties to transform.

## Creating New Contract Type Transformations

If you need to add a NEW specialized contract type, follow this pattern:

### Step 1: Define Transformation Functions for New Properties

```python
def transform_p70_xx_your_new_property(data):
    """
    Transform P70.XX your new property to full CIDOC-CRM structure.
    
    For your new contract type: gmn:E31_X_YourNewContract
    
    Input: gmn:P70_XX_your_new_property <resource>
    Output: cidoc:P70_documents > E7_Activity > [appropriate path]
    """
    if 'gmn:P70_XX_your_new_property' not in data:
        return data
    
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    property_values = data['gmn:P70_XX_your_new_property']
    
    # Create the documented activity
    activity_uri = f"{subject_uri}/activity"
    activity = {
        '@id': activity_uri,
        '@type': 'cidoc:E7_Activity',  # or E8_Acquisition, as appropriate
        # Add appropriate properties based on your needs
    }
    
    # Add P70_documents link
    if 'cidoc:P70_documents' not in data:
        data['cidoc:P70_documents'] = []
    data['cidoc:P70_documents'].append(activity)
    
    # Remove shortcut property
    del data['gmn:P70_XX_your_new_property']
    
    return data
```

### Step 2: Create Main Transformation Function for New Type

```python
def transform_your_new_contract(data):
    """
    Transform all properties specific to your new contract type.
    
    Applies to: gmn:E31_X_YourNewContract
    """
    data = transform_p70_xx_your_new_property(data)
    # Add other property transformations as needed
    return data
```

### Step 3: Add to Main Transform Function

```python
def transform_item(item):
    """Main transformation function."""
    
    types = item.get('@type', [])
    if isinstance(types, str):
        types = [types]
    
    # Standard document transformations (always applied)
    if any(t for t in types if 'E31' in t):
        item = transform_p1_1_has_name(item)
        # ... other standard transformations
    
    # Specialized transformations
    if 'gmn:E31_2_Sales_Contract' in types:
        item = transform_sales_contract(item)
    # ... other specialized types
    
    # Add your new type here
    elif 'gmn:E31_X_YourNewContract' in types:
        item = transform_your_new_contract(item)
    
    return item
```

## Testing Transformations

### Test General Contract Transformation

```python
def test_general_contract_transformation():
    """Test that general contracts are transformed correctly."""
    
    input_data = {
        '@id': 'http://example.org/contract/test001',
        '@type': 'gmn:E31_1_Contract',
        'gmn:P1_1_has_name': 'Test Contract',
        'gmn:P94i_2_has_enactment_date': '1450-01-01'
    }
    
    output_data = transform_item(input_data)
    
    # Check that standard transformations were applied
    assert 'cidoc:P1_is_identified_by' in output_data
    assert 'cidoc:P94i_was_created_by' in output_data
    
    # Check that no specialized properties were added
    # (E31_1_Contract doesn't have specialized properties)
    
    print("✓ General contract transformation test passed")


def test_specialized_contract_transformation():
    """Test that specialized contracts get their specific transformations."""
    
    input_data = {
        '@id': 'http://example.org/contract/sale001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P1_1_has_name': 'Sale Contract',
        'gmn:P70_14_indicates_seller': {'@id': 'http://example.org/person/seller'}
    }
    
    output_data = transform_item(input_data)
    
    # Check standard transformations
    assert 'cidoc:P1_is_identified_by' in output_data
    
    # Check specialized transformations
    assert 'cidoc:P70_documents' in output_data
    # Further validation of E8_Acquisition structure...
    
    print("✓ Specialized contract transformation test passed")
```

## Summary

### Key Points

1. **E31_1_Contract uses existing transformations** - no new functions needed
2. **Standard document transformations apply** to E31_1_Contract
3. **Specialized contract types add their own transformations** for specialized properties
4. **No modifications needed** to gmn_to_cidoc_transform.py for E31_1_Contract

### Transformation Coverage

| Contract Type | Standard Transforms | Specialized Transforms |
|--------------|-------------------|----------------------|
| E31_1_Contract | ✓ | ❌ (none needed) |
| E31_2_Sales_Contract | ✓ | ✓ (seller, buyer, price) |
| E31_3_Arbitration | ✓ | ✓ (parties, arbitrator) |
| E31_4_Cession | ✓ | ✓ (conceding, receiving) |
| E31_7_Donation | ✓ | ✓ (donor, object) |
| E31_8_Dowry | ✓ | ✓ (donor, object of dowry) |

### For More Information

- **Transformation Script**: gmn_to_cidoc_transform.py
- **Specialized Transformations**: See individual contract type documentation
- **Testing**: Run transformation script with test data
- **CIDOC-CRM Compliance**: Verify output against CIDOC-CRM specification

## References

- **Main Script**: gmn_to_cidoc_transform.py
- **Documentation**: contract-documentation.md
- **Implementation Guide**: contract-implementation-guide.md
- **Specialized Types**: 
  - Sales: See main transformation script
  - Donation: See donation transformation documentation
  - Dowry: See dowry transformation documentation
  - Arbitration: See arbitration transformation documentation

---

**Note**: This is a reference file, not an additions file. E31_1_Contract transformation is already complete using existing standard document transformation functions. No new Python code needs to be added.
