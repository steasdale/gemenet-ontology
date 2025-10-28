# Implementation Guide: P70.23 Indicates Object of Cession

This guide provides step-by-step instructions for implementing the `gmn:P70_23_indicates_object_of_cession` property in the GMN ontology and transformation pipeline.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Add TTL Definition](#step-1-add-ttl-definition)
4. [Step 2: Add Transformation Function](#step-2-add-transformation-function)
5. [Step 3: Register in Pipeline](#step-3-register-in-pipeline)
6. [Step 4: Update Documentation](#step-4-update-documentation)
7. [Step 5: Testing](#step-5-testing)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The `P70.23_indicates_object_of_cession` property is a convenience property for associating cession of rights contracts with the legal objects being transferred. It transforms into the full CIDOC-CRM structure using E7_Activity and P16_used_specific_object.

**Transformation Pattern:**
```
GMN Shortcut: E31_4_Cession_of_Rights_Contract -P70.23-> E72_Legal_Object

CIDOC-CRM: E31_Document -P70-> E7_Activity -P16-> E72_Legal_Object
```

---

## Prerequisites

Before implementing this property, ensure:
- [ ] You have access to `gmn_ontology.ttl`
- [ ] You have access to `gmn_to_cidoc_transform.py`
- [ ] Python environment is set up with required libraries
- [ ] You understand CIDOC-CRM basic structure
- [ ] Related properties (P70.21, P70.22) are already implemented

---

## Step 1: Add TTL Definition

### Location
Open `gmn_ontology.ttl` and locate the cession properties section, after `gmn:P70_22_indicates_receiving_party`.

### Code to Add

```turtle
# Property: P70.23 indicates object of cession
gmn:P70_23_indicates_object_of_cession
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.23 indicates object of cession"@en ;
    rdfs:comment "Simplified property for associating a cession of rights contract with the legal rights, claims, or obligations being transferred. This can include rights to collect debts, rights to use property (usufruct), rights of ownership over some object, claims arising from other contracts, inheritance rights, or any other legal interests. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P16_used_specific_object > E72_Legal_Object. The E7_Activity should be typed as a cession/transfer of rights (AAT 300417639). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The range is E72_Legal_Object, which encompasses rights, obligations, and legal claims."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_4_Cession_of_Rights_Contract ;
    rdfs:range cidoc:E72_Legal_Object ;
    dcterms:created "2025-10-18"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P16_used_specific_object .
```

### Verification
After adding, verify the TTL syntax:
```bash
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null
```

If no errors appear, the syntax is correct.

---

## Step 2: Add Transformation Function

### Location
Open `gmn_to_cidoc_transform.py` and add the function after `transform_p70_22_indicates_receiving_party()`.

### Code to Add

```python
def transform_p70_23_indicates_object_of_cession(data):
    """
    Transform gmn:P70_23_indicates_object_of_cession to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E72_Legal_Object
    
    Args:
        data: Dictionary containing the entity data with JSON-LD structure
        
    Returns:
        Transformed dictionary with CIDOC-CRM compliant structure
        
    Example:
        Input:
        {
            '@id': 'cession001',
            '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
            'gmn:P70_23_indicates_object_of_cession': {'@id': 'debt_claim'}
        }
        
        Output:
        {
            '@id': 'cession001',
            '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
            'cidoc:P70_documents': [{
                '@id': 'cession001/cession',
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': 'http://vocab.getty.edu/aat/300417639',
                    '@type': 'cidoc:E55_Type'
                },
                'cidoc:P16_used_specific_object': [{'@id': 'debt_claim', '@type': 'cidoc:E72_Legal_Object'}]
            }]
        }
    """
    if 'gmn:P70_23_indicates_object_of_cession' not in data:
        return data
    
    rights = data['gmn:P70_23_indicates_object_of_cession']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure P70_documents exists with cession activity
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/cession"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_TRANSFER_OF_RIGHTS,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    # Initialize P16_used_specific_object if not present
    if 'cidoc:P16_used_specific_object' not in activity:
        activity['cidoc:P16_used_specific_object'] = []
    
    # Handle different input formats
    if not isinstance(rights, list):
        rights = [rights]
    
    # Add each legal object to the activity
    for rights_obj in rights:
        if isinstance(rights_obj, dict):
            rights_data = rights_obj.copy()
            if '@type' not in rights_data:
                rights_data['@type'] = 'cidoc:E72_Legal_Object'
        else:
            # Handle URI reference
            rights_uri = str(rights_obj)
            rights_data = {
                '@id': rights_uri,
                '@type': 'cidoc:E72_Legal_Object'
            }
        
        activity['cidoc:P16_used_specific_object'].append(rights_data)
    
    # Remove the shortcut property
    del data['gmn:P70_23_indicates_object_of_cession']
    return data
```

### Constants Check
Ensure the constant `AAT_TRANSFER_OF_RIGHTS` is defined at the top of the file:

```python
# Getty AAT URIs for activity types
AAT_TRANSFER_OF_RIGHTS = 'http://vocab.getty.edu/aat/300417639'
```

---

## Step 3: Register in Pipeline

### Location
In the `transform_item()` function, add the transformation call in the cession properties section.

### Find This Section
```python
# Cession properties (P70.21-P70.23)
item = transform_p70_21_indicates_conceding_party(item)
item = transform_p70_22_indicates_receiving_party(item)
```

### Add This Line
```python
# Cession properties (P70.21-P70.23)
item = transform_p70_21_indicates_conceding_party(item)
item = transform_p70_22_indicates_receiving_party(item)
item = transform_p70_23_indicates_object_of_cession(item)
```

### Verification
Ensure the function is called in the correct order, after P70.22.

---

## Step 4: Update Documentation

### Main Documentation File
Add the content from `indicates-cession-object-doc-note.txt` to your main documentation file.

**Suggested Location**: In the "Cession of Rights Contracts" section, after the discussion of P70.21 and P70.22.

### Key Points to Include
1. Property definition and purpose
2. Transformation pattern diagram
3. Examples with different types of legal objects
4. Comparison with related properties
5. Usage guidelines

---

## Step 5: Testing

### Basic Test Case

Create a test file `test_p70_23.py`:

```python
import json
from gmn_to_cidoc_transform import transform_p70_23_indicates_object_of_cession

def test_basic_transformation():
    """Test basic transformation of object of cession"""
    input_data = {
        '@id': 'http://example.org/cession001',
        '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
        'gmn:P70_23_indicates_object_of_cession': {
            '@id': 'http://example.org/debt_claim',
            '@type': 'cidoc:E72_Legal_Object'
        }
    }
    
    result = transform_p70_23_indicates_object_of_cession(input_data)
    
    # Verify structure
    assert 'cidoc:P70_documents' in result
    assert len(result['cidoc:P70_documents']) == 1
    
    activity = result['cidoc:P70_documents'][0]
    assert activity['@type'] == 'cidoc:E7_Activity'
    assert 'cidoc:P16_used_specific_object' in activity
    assert len(activity['cidoc:P16_used_specific_object']) == 1
    
    legal_obj = activity['cidoc:P16_used_specific_object'][0]
    assert legal_obj['@id'] == 'http://example.org/debt_claim'
    assert legal_obj['@type'] == 'cidoc:E72_Legal_Object'
    
    print("✓ Basic transformation test passed")

def test_multiple_objects():
    """Test transformation with multiple legal objects"""
    input_data = {
        '@id': 'http://example.org/cession002',
        '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
        'gmn:P70_23_indicates_object_of_cession': [
            {'@id': 'http://example.org/debt_claim_1'},
            {'@id': 'http://example.org/usufruct_right'}
        ]
    }
    
    result = transform_p70_23_indicates_object_of_cession(input_data)
    
    activity = result['cidoc:P70_documents'][0]
    assert len(activity['cidoc:P16_used_specific_object']) == 2
    
    print("✓ Multiple objects test passed")

def test_uri_reference():
    """Test transformation with simple URI reference"""
    input_data = {
        '@id': 'http://example.org/cession003',
        '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
        'gmn:P70_23_indicates_object_of_cession': 'http://example.org/inheritance_right'
    }
    
    result = transform_p70_23_indicates_object_of_cession(input_data)
    
    activity = result['cidoc:P70_documents'][0]
    legal_obj = activity['cidoc:P16_used_specific_object'][0]
    assert legal_obj['@id'] == 'http://example.org/inheritance_right'
    assert legal_obj['@type'] == 'cidoc:E72_Legal_Object'
    
    print("✓ URI reference test passed")

def test_shared_activity():
    """Test that function reuses existing activity"""
    input_data = {
        '@id': 'http://example.org/cession004',
        '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
        'cidoc:P70_documents': [{
            '@id': 'http://example.org/cession004/cession',
            '@type': 'cidoc:E7_Activity'
        }],
        'gmn:P70_23_indicates_object_of_cession': {
            '@id': 'http://example.org/debt_claim'
        }
    }
    
    result = transform_p70_23_indicates_object_of_cession(input_data)
    
    # Should still have only one activity
    assert len(result['cidoc:P70_documents']) == 1
    assert result['cidoc:P70_documents'][0]['@id'] == 'http://example.org/cession004/cession'
    
    print("✓ Shared activity test passed")

if __name__ == '__main__':
    test_basic_transformation()
    test_multiple_objects()
    test_uri_reference()
    test_shared_activity()
    print("\n✓ All tests passed!")
```

### Run Tests
```bash
python test_p70_23.py
```

### Integration Test

Test with a complete cession contract:

```python
def test_complete_cession():
    """Test transformation with all cession properties"""
    input_data = {
        '@id': 'http://example.org/cession_complete',
        '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
        'gmn:P70_21_indicates_conceding_party': {
            '@id': 'http://example.org/giovanni',
            '@type': 'cidoc:E21_Person'
        },
        'gmn:P70_22_indicates_receiving_party': {
            '@id': 'http://example.org/marco',
            '@type': 'cidoc:E21_Person'
        },
        'gmn:P70_23_indicates_object_of_cession': {
            '@id': 'http://example.org/debt_claim',
            '@type': 'cidoc:E72_Legal_Object'
        }
    }
    
    from gmn_to_cidoc_transform import transform_item
    result = transform_item(input_data)
    
    # Verify all properties are on the same activity
    activity = result['cidoc:P70_documents'][0]
    assert 'cidoc:P14_carried_out_by' in activity  # From P70.21
    assert 'cidoc:P16_used_specific_object' in activity  # From P70.23
    
    print("✓ Complete cession test passed")
```

---

## Troubleshooting

### Issue: Function Not Called

**Symptom**: Property not being transformed

**Solution**: Check that the function is registered in `transform_item()`:
```python
item = transform_p70_23_indicates_object_of_cession(item)
```

### Issue: Missing AAT Constant

**Symptom**: `NameError: name 'AAT_TRANSFER_OF_RIGHTS' is not defined`

**Solution**: Add the constant at the top of the file:
```python
AAT_TRANSFER_OF_RIGHTS = 'http://vocab.getty.edu/aat/300417639'
```

### Issue: Activity Not Shared

**Symptom**: Multiple E7_Activity nodes created for the same contract

**Solution**: Ensure the function checks for existing activity:
```python
if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
    # Create new activity
```

### Issue: Wrong Type Assignment

**Symptom**: Legal object not typed as E72_Legal_Object

**Solution**: Check the type assignment logic:
```python
if '@type' not in rights_data:
    rights_data['@type'] = 'cidoc:E72_Legal_Object'
```

### Issue: List Handling Error

**Symptom**: Error when property has multiple values

**Solution**: Ensure list normalization:
```python
if not isinstance(rights, list):
    rights = [rights]
```

---

## Validation Checklist

After implementation, verify:

- [ ] TTL syntax is valid (use rapper or similar tool)
- [ ] Function is defined in transformation script
- [ ] Function is called in transform_item()
- [ ] All test cases pass
- [ ] Documentation is updated
- [ ] Activity is properly typed (AAT 300417639)
- [ ] Activity is shared with P70.21 and P70.22
- [ ] Multiple objects can be handled
- [ ] Both URI and object references work

---

## Next Steps

After successful implementation:

1. Test with real data samples
2. Update user documentation
3. Add examples to training materials
4. Monitor for edge cases
5. Consider adding validation rules

---

## Reference Files

- **TTL Code**: `indicates-cession-object-ontology.ttl`
- **Python Code**: `indicates-cession-object-transform.py`
- **Documentation**: `indicates-cession-object-documentation.md`
- **Examples**: `indicates-cession-object-doc-note.txt`

---

**Implementation Date**: 2025-10-28  
**Version**: 1.0  
**Status**: Ready for Production
