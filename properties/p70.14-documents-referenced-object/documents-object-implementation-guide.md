# Implementation Guide: P70.14 Documents Referenced Object
## GMN Ontology Property Implementation

**Property**: `gmn:P70_14_documents_referenced_object`  
**Version**: 1.0  
**Date**: 2025-10-27

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Update Ontology File](#step-1-update-ontology-file)
4. [Step 2: Update Transformation Script](#step-2-update-transformation-script)
5. [Step 3: Update Main Documentation](#step-3-update-main-documentation)
6. [Step 4: Testing Procedures](#step-4-testing-procedures)
7. [Step 5: Validation](#step-5-validation)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This guide walks you through implementing the `gmn:P70_14_documents_referenced_object` property, which allows sales contracts to reference legal and physical objects mentioned in the document text.

**Implementation Time**: Approximately 30-45 minutes  
**Difficulty Level**: Intermediate  
**Required Skills**: TTL syntax, Python, CIDOC-CRM basics

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script
- Main documentation file (markdown or text)

### Backup Strategy
```bash
# Create backups before starting
cp gmn_ontology.ttl gmn_ontology.ttl.backup
cp gmn_to_cidoc_transform.py gmn_to_cidoc_transform.py.backup
cp main-documentation.md main-documentation.md.backup
```

### Knowledge Requirements
- Understanding of CIDOC-CRM P67_refers_to property
- Familiarity with E1_CRM_Entity as the top-level class
- Basic Python dictionary manipulation
- TTL/RDF syntax

---

## Step 1: Update Ontology File

### 1.1 Locate Insertion Point

Open `gmn_ontology.ttl` and find the P70.13 property definition. The new property should be inserted immediately after P70.13 and before P70.15.

**Search for**:
```turtle
gmn:P70_13_documents_referenced_place
    a owl:ObjectProperty ;
    # ... property definition ...
    rdfs:seeAlso cidoc:P67_refers_to .
```

### 1.2 Add Property Definition

Insert the following TTL code after P70.13:

```turtle
# Property: P70.14 documents referenced object
gmn:P70_14_documents_referenced_object
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.14 documents referenced object"@en ;
    rdfs:comment "Simplified property for associating a sales contract with any object (legal or physical) referenced or mentioned in the document. This includes legal objects (rights, obligations, debts, claims, privileges, servitudes, easements) and physical objects mentioned in the contract. For example, a contract might reference existing debts being settled, water rights attached to a property, or obligations being transferred. Represents the direct CIDOC-CRM relationship: E31_Document > P67_refers_to > E1_CRM_Entity. This acknowledges that the object is mentioned in the document, whether as context, as part of the transaction conditions, or as related obligations."@en ;
    rdfs:subPropertyOf cidoc:P67_refers_to ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E1_CRM_Entity ;
    dcterms:created "2025-10-27"^^xsd:date ;
    rdfs:seeAlso cidoc:P67_refers_to .
```

### 1.3 Verify Syntax

Check that:
- [ ] Property has blank line before and after
- [ ] Semicolons and periods are correctly placed
- [ ] All predicates are properly indented
- [ ] Date is correct (2025-10-27)
- [ ] Comment text is on a single line (or properly escaped)

### 1.4 Save File

Save the ontology file and validate with a TTL parser if available.

---

## Step 2: Update Transformation Script

### 2.1 Locate Insertion Point

Open `gmn_to_cidoc_transform.py` and find the `transform_p70_13_documents_referenced_place()` function.

**Search for**:
```python
def transform_p70_13_documents_referenced_place(data):
    """
    Transform gmn:P70_13_documents_referenced_place to full CIDOC-CRM structure
    """
```

### 2.2 Add Transformation Function

Insert the following function immediately after `transform_p70_13_documents_referenced_place()`:

```python
def transform_p70_14_documents_referenced_object(data):
    """
    Transform gmn:P70_14_documents_referenced_object to full CIDOC-CRM structure:
    P67_refers_to > E1_CRM_Entity
    
    Args:
        data: Document data dictionary containing GMN properties
    
    Returns:
        Transformed data dictionary with CIDOC-CRM compliant structure
    
    Examples:
        Input:
        {
            "@id": "contract:123",
            "gmn:P70_14_documents_referenced_object": ["object:water_right_1"]
        }
        
        Output:
        {
            "@id": "contract:123",
            "cidoc:P67_refers_to": [
                {
                    "@id": "object:water_right_1",
                    "@type": "cidoc:E1_CRM_Entity"
                }
            ]
        }
    """
    # Check if property exists in data
    if 'gmn:P70_14_documents_referenced_object' not in data:
        return data
    
    # Get the list of referenced objects
    objects = data['gmn:P70_14_documents_referenced_object']
    
    # Initialize P67_refers_to array if it doesn't exist
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    # Process each referenced object
    for obj_obj in objects:
        if isinstance(obj_obj, dict):
            # Object is already a dictionary with properties
            obj_data = obj_obj.copy()
            # Add type if not present
            if '@type' not in obj_data:
                obj_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            # Object is a simple URI string
            obj_uri = str(obj_obj)
            obj_data = {
                '@id': obj_uri,
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        # Add to P67_refers_to array
        data['cidoc:P67_refers_to'].append(obj_data)
    
    # Remove the simplified property
    del data['gmn:P70_14_documents_referenced_object']
    
    return data
```

### 2.3 Add Function Call to Pipeline

Find the main transformation function (usually `transform_item()` or similar) and locate the section where P70 properties are transformed.

**Search for**:
```python
item = transform_p70_13_documents_referenced_place(item)
```

**Add immediately after**:
```python
item = transform_p70_14_documents_referenced_object(item)
```

The sequence should look like:
```python
# Transform sales contract properties
item = transform_p70_13_documents_referenced_place(item)
item = transform_p70_14_documents_referenced_object(item)
item = transform_p70_15_documents_witness(item)
```

### 2.4 Verify Integration

Check that:
- [ ] Function is properly indented
- [ ] Function is called in correct sequence
- [ ] No syntax errors introduced
- [ ] Import statements are present (if any new imports needed)

### 2.5 Save File

Save the transformation script.

---

## Step 3: Update Main Documentation

### 3.1 Locate Documentation Section

Find the section documenting P70 properties, specifically after P70.13 and before P70.15.

### 3.2 Add Property Documentation

Insert the documentation content from `documents-object-doc-note.txt`. This typically includes:

- Property definition
- Semantic structure
- Usage examples
- Relationship to other properties

**Basic structure**:
```markdown
### P70.14 documents referenced object

**Property URI**: `gmn:P70_14_documents_referenced_object`

**Label**: "P70.14 documents referenced object" (English)

**Domain**: `gmn:E31_2_Sales_Contract`

**Range**: `cidoc:E1_CRM_Entity`

[... rest of documentation ...]
```

### 3.3 Update Table of Contents

If your documentation has a table of contents, add an entry for P70.14.

### 3.4 Save Documentation

Save the updated documentation file.

---

## Step 4: Testing Procedures

### 4.1 Test Case 1: Simple Object Reference

**Input**:
```json
{
  "@id": "contract:test_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_14_documents_referenced_object": [
    "object:water_right_1"
  ]
}
```

**Expected Output**:
```json
{
  "@id": "contract:test_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "object:water_right_1",
      "@type": "cidoc:E1_CRM_Entity"
    }
  ]
}
```

### 4.2 Test Case 2: Complex Object with Properties

**Input**:
```json
{
  "@id": "contract:test_002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_14_documents_referenced_object": [
    {
      "@id": "object:debt_1",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Outstanding debt to creditor"
    }
  ]
}
```

**Expected Output**:
```json
{
  "@id": "contract:test_002",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "object:debt_1",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Outstanding debt to creditor"
    }
  ]
}
```

### 4.3 Test Case 3: Multiple Objects

**Input**:
```json
{
  "@id": "contract:test_003",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_14_documents_referenced_object": [
    "object:water_right_1",
    {
      "@id": "object:easement_1",
      "@type": "cidoc:E72_Legal_Object"
    },
    "object:well_1"
  ]
}
```

**Expected Output**:
```json
{
  "@id": "contract:test_003",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "object:water_right_1",
      "@type": "cidoc:E1_CRM_Entity"
    },
    {
      "@id": "object:easement_1",
      "@type": "cidoc:E72_Legal_Object"
    },
    {
      "@id": "object:well_1",
      "@type": "cidoc:E1_CRM_Entity"
    }
  ]
}
```

### 4.4 Test Case 4: Existing P67_refers_to

**Input**:
```json
{
  "@id": "contract:test_004",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "place:venice",
      "@type": "cidoc:E53_Place"
    }
  ],
  "gmn:P70_14_documents_referenced_object": [
    "object:privilege_1"
  ]
}
```

**Expected Output**:
```json
{
  "@id": "contract:test_004",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "place:venice",
      "@type": "cidoc:E53_Place"
    },
    {
      "@id": "object:privilege_1",
      "@type": "cidoc:E1_CRM_Entity"
    }
  ]
}
```

### 4.5 Running Tests

```python
# Create test script: test_p70_14.py

from gmn_to_cidoc_transform import transform_p70_14_documents_referenced_object
import json

def run_test(test_name, input_data, expected_output):
    """Run a single test case"""
    print(f"\nTesting: {test_name}")
    result = transform_p70_14_documents_referenced_object(input_data.copy())
    
    if result == expected_output:
        print("✓ PASSED")
        return True
    else:
        print("✗ FAILED")
        print("Expected:", json.dumps(expected_output, indent=2))
        print("Got:", json.dumps(result, indent=2))
        return False

# Run all tests
test_cases = [
    # Add your test cases here
]

passed = sum([run_test(name, input_data, expected) 
              for name, input_data, expected in test_cases])
print(f"\n{passed}/{len(test_cases)} tests passed")
```

---

## Step 5: Validation

### 5.1 CIDOC-CRM Compliance

Verify that transformed output:
- [ ] Uses `cidoc:P67_refers_to` property correctly
- [ ] Objects have appropriate types (E1_CRM_Entity or more specific)
- [ ] All URIs are properly formatted
- [ ] Property structure matches CIDOC-CRM specification

### 5.2 Data Integrity

Check that:
- [ ] Original simplified property is removed after transformation
- [ ] Existing P67_refers_to data is preserved
- [ ] No data loss occurs during transformation
- [ ] Type information is preserved when present

### 5.3 Integration Testing

Run full transformation pipeline:
```python
from gmn_to_cidoc_transform import transform_item

test_contract = {
    "@id": "contract:full_test",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_1_documents_seller": ["person:seller"],
    "gmn:P70_2_documents_buyer": ["person:buyer"],
    "gmn:P70_14_documents_referenced_object": [
        "object:water_right_1"
    ]
}

result = transform_item(test_contract)
print(json.dumps(result, indent=2))
```

### 5.4 Documentation Review

Ensure:
- [ ] All examples in documentation are accurate
- [ ] Property relationships are clearly explained
- [ ] Use cases are comprehensive
- [ ] Cross-references to related properties are correct

---

## Troubleshooting

### Issue 1: Property Not Transforming

**Symptom**: GMN property remains in output, CIDOC property not created

**Solutions**:
1. Verify function is called in main pipeline
2. Check property name spelling exactly matches: `gmn:P70_14_documents_referenced_object`
3. Ensure input data structure is correct (should be array)

### Issue 2: Type Not Added

**Symptom**: Objects in P67_refers_to lack @type

**Solutions**:
1. Check that type-adding logic is executed
2. Verify that simple URIs are properly detected with `isinstance(obj_obj, dict)`
3. Ensure default type assignment is working

### Issue 3: Existing P67_refers_to Overwritten

**Symptom**: Previous P67_refers_to data disappears

**Solutions**:
1. Verify initialization check: `if 'cidoc:P67_refers_to' not in data:`
2. Make sure you're appending, not assigning: `data['cidoc:P67_refers_to'].append(obj_data)`
3. Check that you're not reinitializing the array after it exists

### Issue 4: TTL Syntax Errors

**Symptom**: Ontology file won't parse

**Solutions**:
1. Check semicolons and periods at line ends
2. Verify string literal escaping in rdfs:comment
3. Ensure proper indentation
4. Validate with TTL parser: `rapper -i turtle gmn_ontology.ttl`

### Issue 5: Mixed Types in P67_refers_to

**Symptom**: Different object types (places, objects, persons) conflicting

**Solutions**:
1. This is expected behavior - P67_refers_to can contain multiple entity types
2. Verify that each object retains its specific type (E53_Place, E21_Person, E1_CRM_Entity)
3. Ensure transformation preserves existing types

---

## Post-Implementation Checklist

### Code
- [ ] All functions added and properly placed
- [ ] Function calls integrated into pipeline
- [ ] No syntax errors
- [ ] Code follows project style guidelines

### Documentation
- [ ] Property documented in main documentation
- [ ] Examples are clear and accurate
- [ ] Table of contents updated
- [ ] Cross-references added

### Testing
- [ ] All test cases pass
- [ ] Integration tests successful
- [ ] Edge cases handled
- [ ] No regressions in existing functionality

### Validation
- [ ] CIDOC-CRM compliance verified
- [ ] Output structure correct
- [ ] Data integrity maintained
- [ ] Performance acceptable

---

## Next Steps

After successful implementation:

1. **Version Control**: Commit changes with clear message
   ```bash
   git add gmn_ontology.ttl gmn_to_cidoc_transform.py documentation.md
   git commit -m "Add P70.14 documents_referenced_object property"
   ```

2. **Documentation Update**: Update changelog or release notes

3. **Team Notification**: Inform team members of new property availability

4. **Data Migration**: If needed, update existing data to use new property

5. **Monitor**: Watch for any issues in production use

---

## Additional Resources

- CIDOC-CRM P67 specification: http://www.cidoc-crm.org/Property/P67-refers-to/version-7.1.3
- E1 CRM Entity: http://www.cidoc-crm.org/Entity/E1-CRM-Entity/version-7.1.3
- GMN Ontology documentation: [link to your docs]
- Transformation pipeline documentation: [link to your docs]

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-27  
**Prepared By**: GMN Ontology Team
