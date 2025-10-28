# Implementation Guide: P70.20 Documents Dispute Subject
## GMN Ontology Property

**Property:** `gmn:P70_20_documents_dispute_subject`  
**Version:** 1.0  
**Last Updated:** October 28, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Ontology Implementation](#step-1-ontology-implementation)
4. [Step 2: Transformation Script Implementation](#step-2-transformation-script-implementation)
5. [Step 3: Pipeline Integration](#step-3-pipeline-integration)
6. [Step 4: Testing](#step-4-testing)
7. [Step 5: Documentation](#step-5-documentation)
8. [Troubleshooting](#troubleshooting)
9. [Validation Procedures](#validation-procedures)

---

## Overview

This guide provides complete step-by-step instructions for implementing the `gmn:P70_20_documents_dispute_subject` property, which links arbitration agreements to the subject matter of disputes.

**What You'll Implement:**
- Property definition in TTL ontology
- Python transformation function
- Integration with transformation pipeline
- Test cases and validation

**Estimated Time:** 30-45 minutes

---

## Prerequisites

### Required Files
- ✅ `gmn_ontology.ttl` - Main ontology file
- ✅ `gmn_to_cidoc_transform.py` - Transformation script
- ✅ Test data with arbitration agreements

### Required Knowledge
- Basic TTL/RDF syntax
- Python programming
- JSON-LD data structures
- Understanding of CIDOC-CRM patterns

### Dependencies
- Python 3.7+
- UUID module (standard library)
- JSON processing capability

---

## Step 1: Ontology Implementation

### 1.1 Locate Insertion Point

Open `gmn_ontology.ttl` and find the arbitration agreement section:

```bash
# Search for the arbitration properties section
grep -n "P70.19 documents arbitrator" gmn_ontology.ttl
```

The P70.20 property should be defined immediately after P70.19.

### 1.2 Verify Property Definition

Check if the property already exists:

```bash
grep "P70_20_documents_dispute_subject" gmn_ontology.ttl
```

### 1.3 Add Property Definition

If not present, add the following TTL definition:

```turtle
# Property: P70.20 documents dispute subject
gmn:P70_20_documents_dispute_subject
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.20 documents dispute subject"@en ;
    rdfs:comment "Simplified property for associating an arbitration agreement with the subject matter of the dispute being arbitrated. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity. The E7_Activity should be typed as an arbitration agreement (AAT 300417271). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The dispute subject can be any entity - a property (E18_Physical_Thing), a legal right (E72_Legal_Object), a debt, a contract claim, or any other matter in contention."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E1_CRM_Entity ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-18"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P16_used_specific_object .
```

### 1.4 Validate TTL Syntax

Validate the ontology file after adding the property:

```bash
# Using rapper (if available)
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Using Python rdflib
python3 -c "from rdflib import Graph; g = Graph(); g.parse('gmn_ontology.ttl', format='turtle'); print('Valid!')"
```

**Expected Result:** No syntax errors

### 1.5 Commit Changes

```bash
git add gmn_ontology.ttl
git commit -m "Add P70.20 documents dispute subject property to ontology"
```

---

## Step 2: Transformation Script Implementation

### 2.1 Locate Insertion Point

Open `gmn_to_cidoc_transform.py` and find the arbitration transformation section:

```python
# Search for existing arbitration functions
# Should be near transform_p70_18 and transform_p70_19
```

### 2.2 Add Constant Definition

At the top of the file with other AAT constants, verify:

```python
# AAT vocabulary URIs
AAT_ARBITRATION = 'http://vocab.getty.edu/page/aat/300417271'
```

### 2.3 Add Transformation Function

Insert the following function after `transform_p70_19_documents_arbitrator`:

```python
def transform_p70_20_documents_dispute_subject(data):
    """
    Transform gmn:P70_20_documents_dispute_subject to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity
    
    This function:
    1. Locates or creates the shared E7_Activity node (arbitration activity)
    2. Adds the dispute subject(s) to the activity's P16_used_specific_object property
    3. Removes the shortcut property from the document
    
    The E7_Activity is shared with P70.18 and P70.19 properties, representing
    one unified arbitration process.
    
    Args:
        data (dict): The arbitration agreement document in JSON-LD format
        
    Returns:
        dict: The transformed document with CIDOC-CRM compliant structure
    """
    # Check if the shortcut property exists
    if 'gmn:P70_20_documents_dispute_subject' not in data:
        return data
    
    # Extract the dispute subjects
    subjects = data['gmn:P70_20_documents_dispute_subject']
    if not isinstance(subjects, list):
        subjects = [subjects]
    
    # Get or generate document URI
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Find existing E7_Activity or create new one
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        # Create new E7_Activity for arbitration
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    # Get reference to the activity (shared with P70.18 and P70.19)
    activity = data['cidoc:P70_documents'][0]
    
    # Initialize P16_used_specific_object if not present
    if 'cidoc:P16_used_specific_object' not in activity:
        activity['cidoc:P16_used_specific_object'] = []
    
    # Add each dispute subject to the activity
    for subject_obj in subjects:
        if isinstance(subject_obj, dict):
            # Subject is already a dictionary (may have @id and @type)
            subject_data = subject_obj.copy()
            if '@type' not in subject_data:
                subject_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            # Subject is a URI string
            subject_uri_str = str(subject_obj)
            subject_data = {
                '@id': subject_uri_str,
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    # Remove the shortcut property
    del data['gmn:P70_20_documents_dispute_subject']
    
    return data
```

### 2.4 Validate Python Syntax

Test the function syntax:

```python
python3 -m py_compile gmn_to_cidoc_transform.py
```

**Expected Result:** No syntax errors

---

## Step 3: Pipeline Integration

### 3.1 Locate Transformation Pipeline

Find the main transformation function or pipeline:

```python
def transform_document(data):
    """Main transformation pipeline"""
    # ... existing transformations ...
```

### 3.2 Add Function Call

Add the transformation call with other arbitration property transformations:

```python
def transform_document(data):
    """Main transformation pipeline"""
    
    # ... existing transformations ...
    
    # Arbitration Agreement transformations
    if data.get('@type') == 'gmn:E31_3_Arbitration_Agreement':
        data = transform_p70_18_documents_disputing_party(data)
        data = transform_p70_19_documents_arbitrator(data)
        data = transform_p70_20_documents_dispute_subject(data)  # ADD THIS LINE
    
    # ... remaining transformations ...
    
    return data
```

### 3.3 Verify Import Statements

Ensure UUID is imported at the top of the file:

```python
from uuid import uuid4
```

### 3.4 Test Integration

Run a simple integration test:

```python
# Test with minimal data
test_data = {
    '@type': 'gmn:E31_3_Arbitration_Agreement',
    '@id': 'http://example.org/arb/001',
    'gmn:P70_20_documents_dispute_subject': [
        {'@id': 'http://example.org/property/house1'}
    ]
}

result = transform_document(test_data)
print(json.dumps(result, indent=2))
```

**Expected Output:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "@id": "http://example.org/arb/001",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/arb/001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P16_used_specific_object": [{
      "@id": "http://example.org/property/house1",
      "@type": "cidoc:E1_CRM_Entity"
    }]
  }]
}
```

---

## Step 4: Testing

### 4.1 Create Test Cases

Create a test file `test_p70_20.json`:

```json
[
  {
    "test_name": "Single dispute subject",
    "input": {
      "@type": "gmn:E31_3_Arbitration_Agreement",
      "@id": "http://example.org/arb/test001",
      "gmn:P70_20_documents_dispute_subject": [
        {"@id": "http://example.org/property/building123"}
      ]
    },
    "expected_properties": [
      "cidoc:P70_documents",
      "cidoc:P16_used_specific_object"
    ]
  },
  {
    "test_name": "Multiple dispute subjects",
    "input": {
      "@type": "gmn:E31_3_Arbitration_Agreement",
      "@id": "http://example.org/arb/test002",
      "gmn:P70_20_documents_dispute_subject": [
        {"@id": "http://example.org/debts/debt_xyz"},
        {"@id": "http://example.org/ships/ship_santa_maria"}
      ]
    },
    "expected_count": 2
  },
  {
    "test_name": "Integration with P70.18 and P70.19",
    "input": {
      "@type": "gmn:E31_3_Arbitration_Agreement",
      "@id": "http://example.org/arb/test003",
      "gmn:P70_18_documents_disputing_party": [
        {"@id": "http://example.org/persons/party1"}
      ],
      "gmn:P70_19_documents_arbitrator": [
        {"@id": "http://example.org/persons/arbitrator1"}
      ],
      "gmn:P70_20_documents_dispute_subject": [
        {"@id": "http://example.org/property/land"}
      ]
    },
    "expected_shared_activity": true
  }
]
```

### 4.2 Run Test Script

Create and run `test_transformation.py`:

```python
import json
from gmn_to_cidoc_transform import transform_document

def run_tests():
    with open('test_p70_20.json', 'r') as f:
        tests = json.load(f)
    
    for test in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test['test_name']}")
        print('='*60)
        
        result = transform_document(test['input'].copy())
        
        # Check expected properties exist
        if 'expected_properties' in test:
            for prop in test['expected_properties']:
                if prop not in str(result):
                    print(f"❌ FAIL: Missing {prop}")
                else:
                    print(f"✅ PASS: Found {prop}")
        
        # Check count of subjects
        if 'expected_count' in test:
            activity = result.get('cidoc:P70_documents', [{}])[0]
            subjects = activity.get('cidoc:P16_used_specific_object', [])
            if len(subjects) == test['expected_count']:
                print(f"✅ PASS: Correct count ({test['expected_count']})")
            else:
                print(f"❌ FAIL: Expected {test['expected_count']}, got {len(subjects)}")
        
        # Check shared activity
        if test.get('expected_shared_activity'):
            activity = result.get('cidoc:P70_documents', [{}])[0]
            has_p14 = 'cidoc:P14_carried_out_by' in activity
            has_p16 = 'cidoc:P16_used_specific_object' in activity
            if has_p14 and has_p16:
                print("✅ PASS: Shared activity structure")
            else:
                print("❌ FAIL: Not sharing activity properly")
        
        print(f"\nTransformed output:")
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    run_tests()
```

Run tests:

```bash
python3 test_transformation.py
```

### 4.3 Validation Checks

Verify the following for each test:

- [ ] `gmn:P70_20_documents_dispute_subject` is removed
- [ ] `cidoc:P70_documents` array exists
- [ ] E7_Activity has correct type (AAT 300417271)
- [ ] `cidoc:P16_used_specific_object` contains subjects
- [ ] Each subject has `@type` of `cidoc:E1_CRM_Entity`
- [ ] Activity is shared with P70.18 and P70.19
- [ ] No duplicate subjects added

### 4.4 Real Data Testing

Test with actual arbitration agreement data:

```python
# Load real arbitration agreement
with open('real_arbitration_data.json', 'r') as f:
    real_data = json.load(f)

# Transform
result = transform_document(real_data)

# Validate structure
assert 'cidoc:P70_documents' in result
assert 'gmn:P70_20_documents_dispute_subject' not in result

print("✅ Real data transformation successful")
```

---

## Step 5: Documentation

### 5.1 Update Main Documentation

Add to your main documentation file:

```markdown
### gmn:P70_20_documents_dispute_subject

**Label:** P70.20 documents dispute subject

**Domain:** gmn:E31_3_Arbitration_Agreement

**Range:** cidoc:E1_CRM_Entity

**Definition:** Simplified property for associating an arbitration agreement 
with the subject matter of the dispute being arbitrated.

**Full CIDOC-CRM Path:**
E31_Document → P70_documents → E7_Activity → P16_used_specific_object → E1_CRM_Entity

**Usage:** Use this property to indicate what the dispute is about. Common 
subjects include physical property, legal rights, debts, contract claims, 
or any other matter in contention.

**Example:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/property/building123"},
    {"@id": "http://example.org/debts/debt_xyz"}
  ]
}
```
```

### 5.2 Update Property Tables

Add row to arbitration properties table:

| Property | Label | Domain | Range | Description |
|----------|-------|--------|-------|-------------|
| P70.18 | documents disputing party | E31_3_Arbitration_Agreement | E39_Actor | Parties involved in the dispute |
| P70.19 | documents arbitrator | E31_3_Arbitration_Agreement | E39_Actor | Arbitrators appointed to resolve dispute |
| **P70.20** | **documents dispute subject** | **E31_3_Arbitration_Agreement** | **E1_CRM_Entity** | **Subject matter being arbitrated** |

### 5.3 Add Usage Examples

Document common usage patterns:

```markdown
#### Example: Property Dispute

```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "@id": "http://example.org/arb/property_dispute_001",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/merchant_a"},
    {"@id": "http://example.org/persons/merchant_b"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_1"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/property/warehouse_genoa"}
  ]
}
```

#### Example: Multiple Subjects

```json
{
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/debts/debt123"},
    {"@id": "http://example.org/contracts/partnership_001"},
    {"@id": "http://example.org/property/shop_location"}
  ]
}
```
```

---

## Troubleshooting

### Issue: Property Not Transforming

**Symptoms:**
- Shortcut property still present after transformation
- No E7_Activity created

**Solutions:**
1. Verify function is called in pipeline
2. Check document type is `gmn:E31_3_Arbitration_Agreement`
3. Ensure property name matches exactly: `gmn:P70_20_documents_dispute_subject`
4. Check for typos in property name

### Issue: Activity Not Shared

**Symptoms:**
- Multiple E7_Activity nodes created
- P14 and P16 in separate activities

**Solutions:**
1. Ensure P70.18, P70.19, and P70.20 all check for existing activity
2. Verify all functions use `data['cidoc:P70_documents'][0]`
3. Check transformation order - all three should run on same document
4. Review activity creation logic

### Issue: Missing @type on Subjects

**Symptoms:**
- Subjects in P16 array lack `@type` property
- Validation warnings about untyped entities

**Solutions:**
1. Check subject creation logic in transformation function
2. Ensure `cidoc:E1_CRM_Entity` is added when @type is missing
3. Verify entity typing for known types (E18, E72, etc.)

### Issue: Duplicate Subjects

**Symptoms:**
- Same subject appears multiple times in P16 array

**Solutions:**
1. Add duplicate check before appending:
```python
# Before appending subject
existing_ids = [s.get('@id') for s in activity['cidoc:P16_used_specific_object']]
if subject_data.get('@id') not in existing_ids:
    activity['cidoc:P16_used_specific_object'].append(subject_data)
```

### Issue: Transformation Order Problems

**Symptoms:**
- Inconsistent results depending on property order
- Sometimes works, sometimes doesn't

**Solutions:**
1. Ensure all three functions (P70.18, P70.19, P70.20) handle all cases:
   - Creating new activity
   - Using existing activity
   - Initializing arrays
2. Test with different property combinations
3. Document required transformation order

---

## Validation Procedures

### Syntax Validation

```python
def validate_transformation(result):
    """Validate transformed arbitration agreement structure"""
    
    errors = []
    
    # Check shortcut property removed
    if 'gmn:P70_20_documents_dispute_subject' in result:
        errors.append("Shortcut property not removed")
    
    # Check P70_documents exists
    if 'cidoc:P70_documents' not in result:
        errors.append("cidoc:P70_documents not created")
        return errors
    
    activity = result['cidoc:P70_documents'][0]
    
    # Check activity type
    if '@type' not in activity or activity['@type'] != 'cidoc:E7_Activity':
        errors.append("Activity not typed as E7_Activity")
    
    # Check arbitration typing
    if 'cidoc:P2_has_type' not in activity:
        errors.append("Activity not typed as arbitration")
    elif activity['cidoc:P2_has_type'].get('@id') != AAT_ARBITRATION:
        errors.append("Incorrect arbitration type")
    
    # Check P16 exists
    if 'cidoc:P16_used_specific_object' not in activity:
        errors.append("P16_used_specific_object not created")
        return errors
    
    # Check subjects have types
    for subject in activity['cidoc:P16_used_specific_object']:
        if '@type' not in subject:
            errors.append(f"Subject {subject.get('@id')} missing @type")
    
    return errors

# Usage
errors = validate_transformation(result)
if errors:
    print("❌ Validation failed:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ Validation passed")
```

### SPARQL Validation

Test with SPARQL queries:

```sparql
# Query 1: Find all arbitration subjects
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?subject
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P16_used_specific_object ?subject .
}

# Query 2: Verify shared activity
SELECT ?agreement ?party ?arbitrator ?subject
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by ?party ;
            cidoc:P14_carried_out_by ?arbitrator ;
            cidoc:P16_used_specific_object ?subject .
}
```

### Integration Testing

Create comprehensive integration test:

```python
def integration_test():
    """Test full arbitration agreement transformation"""
    
    # Complete arbitration agreement
    test_data = {
        "@type": "gmn:E31_3_Arbitration_Agreement",
        "@id": "http://example.org/arb/integration_test",
        "gmn:P1_1_has_name": [{"@value": "Property Dispute Arbitration"}],
        "gmn:P94i_2_has_enactment_date": [{"@value": "1450-06-15"}],
        "gmn:P70_18_documents_disputing_party": [
            {"@id": "http://example.org/persons/party1"},
            {"@id": "http://example.org/persons/party2"}
        ],
        "gmn:P70_19_documents_arbitrator": [
            {"@id": "http://example.org/persons/arbitrator"}
        ],
        "gmn:P70_20_documents_dispute_subject": [
            {"@id": "http://example.org/property/building"}
        ]
    }
    
    # Transform
    result = transform_document(test_data)
    
    # Validate
    assert 'cidoc:P70_documents' in result
    activity = result['cidoc:P70_documents'][0]
    
    # Check all properties in one activity
    assert 'cidoc:P14_carried_out_by' in activity
    assert 'cidoc:P16_used_specific_object' in activity
    assert len(activity['cidoc:P14_carried_out_by']) == 3  # 2 parties + 1 arbitrator
    assert len(activity['cidoc:P16_used_specific_object']) == 1
    
    print("✅ Integration test passed")
    return result
```

---

## Best Practices

1. **Always check for existing E7_Activity** before creating new one
2. **Initialize arrays** before appending to avoid errors
3. **Type all entities** with appropriate CIDOC-CRM classes
4. **Test with multiple subjects** to ensure array handling works
5. **Validate shared activity** with other arbitration properties
6. **Document edge cases** in code comments
7. **Use descriptive variable names** for clarity
8. **Add logging** for debugging transformation issues

---

## Next Steps

After successful implementation:

1. ✅ Deploy to production environment
2. ✅ Update API documentation
3. ✅ Train data entry team on property usage
4. ✅ Create data validation rules
5. ✅ Monitor transformation logs
6. ✅ Gather user feedback
7. ✅ Plan related property enhancements

---

## Support and Maintenance

### Logging

Add logging to transformation function:

```python
import logging

def transform_p70_20_documents_dispute_subject(data):
    logger = logging.getLogger(__name__)
    
    if 'gmn:P70_20_documents_dispute_subject' not in data:
        logger.debug("No P70.20 property found")
        return data
    
    logger.info(f"Transforming P70.20 for document: {data.get('@id')}")
    
    # ... transformation logic ...
    
    logger.info(f"Added {len(subjects)} dispute subjects")
    return data
```

### Monitoring

Track transformation metrics:

```python
# Count transformations
transformations_count = 0
subjects_added = 0

# In transformation function
transformations_count += 1
subjects_added += len(subjects)

# Report
print(f"Transformed {transformations_count} agreements")
print(f"Added {subjects_added} total subjects")
```

---

**Implementation Guide Version:** 1.0  
**Last Updated:** October 28, 2025  
**Status:** Production Ready
