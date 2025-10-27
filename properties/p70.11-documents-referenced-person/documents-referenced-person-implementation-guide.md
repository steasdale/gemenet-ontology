# GMN P70.11 Documents Referenced Person - Implementation Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Ontology Implementation](#ontology-implementation)
3. [Python Transformation Implementation](#python-transformation-implementation)
4. [Testing Procedures](#testing-procedures)
5. [Troubleshooting](#troubleshooting)
6. [Rollback Procedures](#rollback-procedures)

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script

### Required Tools
- Text editor with Turtle/TTL syntax support
- Python 3.8 or higher
- RDFLib library (`pip install rdflib`)
- Access to test data or ability to create test cases

### Knowledge Requirements
- Basic understanding of RDF/Turtle syntax
- Python programming basics
- Understanding of CIDOC-CRM P67_refers_to property
- Familiarity with transformation pipeline

---

## Ontology Implementation

### Step 1: Locate Insertion Point

1. Open `gmn_ontology.ttl` in your text editor
2. Search for `gmn:P70_10_documents_payment_recipient_for_seller`
3. Scroll to the end of that property definition (after the last period)
4. Position cursor for new property insertion

**Location**: Around line 1100 (after P70.10, before P70.12)

### Step 2: Add Property Definition

Copy the following TTL block from `documents-referenced-person-ontology.ttl`:

```turtle
# Property: P70.11 documents referenced person
gmn:P70_11_documents_referenced_person
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.11 documents referenced person"@en ;
    rdfs:comment "Simplified property for associating a sales contract with any person referenced or mentioned in the document text who does not have one of the specified transactional roles. This captures persons who appear in the contract narrative but are not parties to the acquisition: witnesses present at the signing, absent parties whose rights or claims are acknowledged, deceased persons whose estates or relationships are mentioned for context (e.g., 'Giovanni, son of the late Marco'), neighbors or adjacent property owners referenced in property descriptions, previous owners mentioned in provenance statements, or any other individuals named in the contract text. Unlike the other P70 properties which document participation in the E8_Acquisition event, this property represents a direct relationship between the document and the person: E31_Document > P67_refers_to > E21_Person. This acknowledges that the person is textually present in the document without implying their participation in the transaction itself."@en ;
    rdfs:subPropertyOf cidoc:P67_refers_to ;
    rdfs:domain cidoc:E31_Document ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P67_refers_to .
```

### Step 3: Verify Syntax

**Checklist**:
- [ ] Property URI is exactly `gmn:P70_11_documents_referenced_person`
- [ ] Blank line before property definition
- [ ] Property starts with `# Property: P70.11 documents referenced person`
- [ ] All statements end with semicolons except the last (which ends with period)
- [ ] Proper indentation (4 spaces)
- [ ] Domain is `cidoc:E31_Document`
- [ ] Range is `cidoc:E21_Person`
- [ ] Subproperty of `cidoc:P67_refers_to`

### Step 4: Validate Ontology

```bash
# Using rapper (if installed)
rapper -i turtle -o turtle gmn_ontology.ttl > /dev/null

# Using Python with rdflib
python3 << EOF
from rdflib import Graph
g = Graph()
try:
    g.parse('gmn_ontology.ttl', format='turtle')
    print("✓ Ontology is valid")
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

**Expected Output**: No errors, confirmation that ontology is valid

---

## Python Transformation Implementation

### Step 1: Locate Insertion Point

1. Open `gmn_to_cidoc_transform.py`
2. Search for `def transform_p70_10_documents_payment_recipient_for_seller`
3. Scroll to the end of that function (after the `return data` statement)
4. Position cursor after the function for new function insertion

**Location**: Around line 803 (after P70.10 function, before P70.12 function)

### Step 2: Add Transformation Function

Copy the following code from `documents-referenced-person-transform.py`:

```python
def transform_p70_11_documents_referenced_person(data):
    """
    Transform gmn:P70_11_documents_referenced_person to full CIDOC-CRM structure:
    P67_refers_to > E21_Person
    
    This property creates a direct reference from the document to persons mentioned
    in the text who do not have specific transactional roles.
    
    Args:
        data: Document data dictionary with gmn:P70_11 property
        
    Returns:
        Transformed data with cidoc:P67_refers_to
        
    Examples:
        Input:
            {
                '@id': 'contract:001',
                '@type': 'gmn:E31_2_Sales_Contract',
                'gmn:P70_11_documents_referenced_person': [
                    {'@id': 'person:giovanni', '@type': 'cidoc:E21_Person'},
                    'person:marco'
                ]
            }
            
        Output:
            {
                '@id': 'contract:001',
                '@type': 'gmn:E31_2_Sales_Contract',
                'cidoc:P67_refers_to': [
                    {'@id': 'person:giovanni', '@type': 'cidoc:E21_Person'},
                    {'@id': 'person:marco', '@type': 'cidoc:E21_Person'}
                ]
            }
    """
    if 'gmn:P70_11_documents_referenced_person' not in data:
        return data
    
    persons = data['gmn:P70_11_documents_referenced_person']
    
    # Initialize P67_refers_to if it doesn't exist
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    # Process each referenced person
    for person_obj in persons:
        if isinstance(person_obj, dict):
            # Person is already a full object
            person_data = person_obj.copy()
            # Ensure it has E21_Person type
            if '@type' not in person_data:
                person_data['@type'] = 'cidoc:E21_Person'
        else:
            # Person is just a URI string
            person_uri = str(person_obj)
            person_data = {
                '@id': person_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add to P67_refers_to
        data['cidoc:P67_refers_to'].append(person_data)
    
    # Remove simplified property
    del data['gmn:P70_11_documents_referenced_person']
    return data
```

### Step 3: Register Function in Transform Pipeline

1. Search for the `transform_item()` function (around line 2300)
2. Locate the line with `item = transform_p70_10_documents_payment_recipient_for_seller(item)`
3. Add the following line immediately after:

```python
    item = transform_p70_11_documents_referenced_person(item)
```

**Context** (what it should look like):
```python
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
    item = transform_p70_11_documents_referenced_person(item)  # ← ADD THIS LINE
    item = transform_p70_12_documents_payment_through_organization(item)
```

### Step 4: Verify Python Syntax

```bash
# Check for syntax errors
python3 -m py_compile gmn_to_cidoc_transform.py

# Or run a quick import test
python3 << EOF
try:
    import gmn_to_cidoc_transform
    print("✓ Module imports successfully")
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

---

## Testing Procedures

### Test Case 1: Single Referenced Person (URI Only)

**Input Data**:
```json
{
    "@id": "contract:test001",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_11_documents_referenced_person": ["person:giovanni_deceased"]
}
```

**Expected Output**:
```json
{
    "@id": "contract:test001",
    "@type": "gmn:E31_2_Sales_Contract",
    "cidoc:P67_refers_to": [
        {
            "@id": "person:giovanni_deceased",
            "@type": "cidoc:E21_Person"
        }
    ]
}
```

**Test Code**:
```python
from gmn_to_cidoc_transform import transform_p70_11_documents_referenced_person
import json

test_data = {
    "@id": "contract:test001",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_11_documents_referenced_person": ["person:giovanni_deceased"]
}

result = transform_p70_11_documents_referenced_person(test_data)
print(json.dumps(result, indent=2))

# Verify
assert 'gmn:P70_11_documents_referenced_person' not in result
assert 'cidoc:P67_refers_to' in result
assert len(result['cidoc:P67_refers_to']) == 1
assert result['cidoc:P67_refers_to'][0]['@type'] == 'cidoc:E21_Person'
print("✓ Test 1 passed")
```

### Test Case 2: Multiple Referenced Persons (Mixed Format)

**Input Data**:
```json
{
    "@id": "contract:test002",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_11_documents_referenced_person": [
        {
            "@id": "person:marco",
            "@type": "cidoc:E21_Person",
            "rdfs:label": "Marco (neighbor)"
        },
        "person:pietro",
        {
            "@id": "person:antonio",
            "rdfs:label": "Antonio (previous owner)"
        }
    ]
}
```

**Expected Output**:
```json
{
    "@id": "contract:test002",
    "@type": "gmn:E31_2_Sales_Contract",
    "cidoc:P67_refers_to": [
        {
            "@id": "person:marco",
            "@type": "cidoc:E21_Person",
            "rdfs:label": "Marco (neighbor)"
        },
        {
            "@id": "person:pietro",
            "@type": "cidoc:E21_Person"
        },
        {
            "@id": "person:antonio",
            "@type": "cidoc:E21_Person",
            "rdfs:label": "Antonio (previous owner)"
        }
    ]
}
```

**Test Code**:
```python
from gmn_to_cidoc_transform import transform_p70_11_documents_referenced_person
import json

test_data = {
    "@id": "contract:test002",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_11_documents_referenced_person": [
        {
            "@id": "person:marco",
            "@type": "cidoc:E21_Person",
            "rdfs:label": "Marco (neighbor)"
        },
        "person:pietro",
        {
            "@id": "person:antonio",
            "rdfs:label": "Antonio (previous owner)"
        }
    ]
}

result = transform_p70_11_documents_referenced_person(test_data)
print(json.dumps(result, indent=2))

# Verify
assert 'gmn:P70_11_documents_referenced_person' not in result
assert 'cidoc:P67_refers_to' in result
assert len(result['cidoc:P67_refers_to']) == 3
assert all(p['@type'] == 'cidoc:E21_Person' for p in result['cidoc:P67_refers_to'])
print("✓ Test 2 passed")
```

### Test Case 3: No Referenced Persons

**Input Data**:
```json
{
    "@id": "contract:test003",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_1_documents_seller": ["person:seller001"]
}
```

**Expected Output**: Same as input (no changes)

**Test Code**:
```python
from gmn_to_cidoc_transform import transform_p70_11_documents_referenced_person
import json

test_data = {
    "@id": "contract:test003",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_1_documents_seller": ["person:seller001"]
}

result = transform_p70_11_documents_referenced_person(test_data)
print(json.dumps(result, indent=2))

# Verify
assert result == test_data
assert 'cidoc:P67_refers_to' not in result
print("✓ Test 3 passed")
```

### Test Case 4: Integration with Existing P67_refers_to

**Input Data**:
```json
{
    "@id": "contract:test004",
    "@type": "gmn:E31_2_Sales_Contract",
    "cidoc:P67_refers_to": [
        {
            "@id": "place:venice",
            "@type": "cidoc:E53_Place"
        }
    ],
    "gmn:P70_11_documents_referenced_person": ["person:lorenzo"]
}
```

**Expected Output**: Both place and person in P67_refers_to

**Test Code**:
```python
from gmn_to_cidoc_transform import transform_p70_11_documents_referenced_person
import json

test_data = {
    "@id": "contract:test004",
    "@type": "gmn:E31_2_Sales_Contract",
    "cidoc:P67_refers_to": [
        {
            "@id": "place:venice",
            "@type": "cidoc:E53_Place"
        }
    ],
    "gmn:P70_11_documents_referenced_person": ["person:lorenzo"]
}

result = transform_p70_11_documents_referenced_person(test_data)
print(json.dumps(result, indent=2))

# Verify
assert 'gmn:P70_11_documents_referenced_person' not in result
assert len(result['cidoc:P67_refers_to']) == 2
assert any(p['@type'] == 'cidoc:E53_Place' for p in result['cidoc:P67_refers_to'])
assert any(p['@type'] == 'cidoc:E21_Person' for p in result['cidoc:P67_refers_to'])
print("✓ Test 4 passed")
```

### Test Case 5: Full Pipeline Test

**Input Data**:
```json
{
    "@id": "contract:test005",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P1_1_has_name": "Test Contract",
    "gmn:P70_1_documents_seller": ["person:seller"],
    "gmn:P70_11_documents_referenced_person": [
        "person:deceased_father",
        "person:neighbor"
    ]
}
```

**Test Code**:
```python
from gmn_to_cidoc_transform import transform_item
import json

test_data = {
    "@id": "contract:test005",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P1_1_has_name": "Test Contract",
    "gmn:P70_1_documents_seller": ["person:seller"],
    "gmn:P70_11_documents_referenced_person": [
        "person:deceased_father",
        "person:neighbor"
    ]
}

result = transform_item(test_data)
print(json.dumps(result, indent=2))

# Verify P70.11 was transformed
assert 'gmn:P70_11_documents_referenced_person' not in result
assert 'cidoc:P67_refers_to' in result

# Verify other transformations still work
assert 'cidoc:P70_documents' in result  # From P70.1
print("✓ Test 5 (Full Pipeline) passed")
```

### Running All Tests

Create a test file `test_p70_11.py`:

```python
#!/usr/bin/env python3
"""Test suite for P70.11 documents referenced person transformation"""

import json
from gmn_to_cidoc_transform import (
    transform_p70_11_documents_referenced_person,
    transform_item
)

def test_single_person_uri():
    """Test Case 1: Single person as URI"""
    data = {
        "@id": "contract:001",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_11_documents_referenced_person": ["person:giovanni"]
    }
    result = transform_p70_11_documents_referenced_person(data)
    
    assert 'gmn:P70_11_documents_referenced_person' not in result
    assert 'cidoc:P67_refers_to' in result
    assert len(result['cidoc:P67_refers_to']) == 1
    assert result['cidoc:P67_refers_to'][0]['@type'] == 'cidoc:E21_Person'
    print("✓ Test 1: Single person URI - PASSED")

def test_multiple_persons_mixed():
    """Test Case 2: Multiple persons in mixed formats"""
    data = {
        "@id": "contract:002",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_11_documents_referenced_person": [
            {"@id": "person:marco", "@type": "cidoc:E21_Person"},
            "person:pietro",
            {"@id": "person:antonio", "rdfs:label": "Antonio"}
        ]
    }
    result = transform_p70_11_documents_referenced_person(data)
    
    assert 'gmn:P70_11_documents_referenced_person' not in result
    assert len(result['cidoc:P67_refers_to']) == 3
    assert all(p['@type'] == 'cidoc:E21_Person' for p in result['cidoc:P67_refers_to'])
    print("✓ Test 2: Multiple persons mixed - PASSED")

def test_no_referenced_persons():
    """Test Case 3: Document without referenced persons"""
    data = {
        "@id": "contract:003",
        "@type": "gmn:E31_2_Sales_Contract"
    }
    result = transform_p70_11_documents_referenced_person(data)
    
    assert result == data
    assert 'cidoc:P67_refers_to' not in result
    print("✓ Test 3: No referenced persons - PASSED")

def test_existing_p67_refers_to():
    """Test Case 4: Integration with existing P67_refers_to"""
    data = {
        "@id": "contract:004",
        "@type": "gmn:E31_2_Sales_Contract",
        "cidoc:P67_refers_to": [
            {"@id": "place:venice", "@type": "cidoc:E53_Place"}
        ],
        "gmn:P70_11_documents_referenced_person": ["person:lorenzo"]
    }
    result = transform_p70_11_documents_referenced_person(data)
    
    assert len(result['cidoc:P67_refers_to']) == 2
    assert any(p['@type'] == 'cidoc:E53_Place' for p in result['cidoc:P67_refers_to'])
    assert any(p['@type'] == 'cidoc:E21_Person' for p in result['cidoc:P67_refers_to'])
    print("✓ Test 4: Existing P67_refers_to - PASSED")

def test_full_pipeline():
    """Test Case 5: Full transformation pipeline"""
    data = {
        "@id": "contract:005",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_1_documents_seller": ["person:seller"],
        "gmn:P70_11_documents_referenced_person": ["person:deceased", "person:neighbor"]
    }
    result = transform_item(data)
    
    assert 'gmn:P70_11_documents_referenced_person' not in result
    assert 'cidoc:P67_refers_to' in result
    assert 'cidoc:P70_documents' in result
    print("✓ Test 5: Full pipeline - PASSED")

if __name__ == '__main__':
    print("Running P70.11 Test Suite...")
    print("=" * 60)
    
    try:
        test_single_person_uri()
        test_multiple_persons_mixed()
        test_no_referenced_persons()
        test_existing_p67_refers_to()
        test_full_pipeline()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
    except AssertionError as e:
        print(f"✗ TEST FAILED: {e}")
    except Exception as e:
        print(f"✗ ERROR: {e}")
```

Run tests:
```bash
python3 test_p70_11.py
```

---

## Troubleshooting

### Problem: Syntax Error in Ontology

**Symptoms**: Turtle parser fails to load ontology

**Solutions**:
1. Check that all statements except the last end with semicolons
2. Verify the last statement ends with a period
3. Ensure proper indentation (4 spaces)
4. Check that all URIs are properly formatted
5. Validate with: `rapper -i turtle gmn_ontology.ttl`

### Problem: Function Not Found

**Symptoms**: `AttributeError: module has no attribute 'transform_p70_11_documents_referenced_person'`

**Solutions**:
1. Verify function was added to the file
2. Check function name spelling
3. Ensure proper indentation (no extra spaces)
4. Reload the module: `import importlib; importlib.reload(gmn_to_cidoc_transform)`

### Problem: Function Not Being Called

**Symptoms**: GMN property still present in output

**Solutions**:
1. Verify function call was added to `transform_item()`
2. Check that call is in correct order (after P70.10)
3. Ensure proper indentation of function call
4. Verify data has the property to transform

### Problem: Type Not Being Added

**Symptoms**: Person in output missing `@type`

**Solutions**:
1. Check that the type assignment logic is correct
2. Verify that `person_data['@type']` is set in both branches
3. Ensure copied dictionary preserves existing type

### Problem: Duplicate P67_refers_to Entries

**Symptoms**: Same person appears multiple times in output

**Solutions**:
1. Check input data for duplicates
2. Consider adding deduplication logic if needed
3. Verify upstream data quality

---

## Rollback Procedures

### Rolling Back Ontology Changes

1. **If using version control**:
   ```bash
   git checkout gmn_ontology.ttl
   ```

2. **If you have a backup**:
   ```bash
   cp gmn_ontology.ttl.backup gmn_ontology.ttl
   ```

3. **Manual removal**:
   - Open `gmn_ontology.ttl`
   - Search for `gmn:P70_11_documents_referenced_person`
   - Delete the entire property block (from `# Property:` to the final period)
   - Save file

### Rolling Back Python Changes

1. **If using version control**:
   ```bash
   git checkout gmn_to_cidoc_transform.py
   ```

2. **If you have a backup**:
   ```bash
   cp gmn_to_cidoc_transform.py.backup gmn_to_cidoc_transform.py
   ```

3. **Manual removal**:
   - Open `gmn_to_cidoc_transform.py`
   - Remove the `transform_p70_11_documents_referenced_person()` function
   - Remove the function call from `transform_item()`
   - Save file

### Verification After Rollback

```bash
# Test that system still works
python3 -c "import gmn_to_cidoc_transform; print('✓ Module loads')"

# Run existing tests
python3 test_suite.py
```

---

## Post-Implementation Checklist

After completing implementation:

- [ ] Ontology file validates without errors
- [ ] Python module imports without errors
- [ ] All 5 test cases pass
- [ ] Documentation updated with examples
- [ ] Existing tests still pass
- [ ] Committed changes to version control
- [ ] Updated changelog or release notes
- [ ] Informed team of new property availability

---

## Additional Notes

### Performance Considerations
- Function has O(n) complexity where n is number of referenced persons
- No significant performance impact expected
- Handles both URI strings and object dictionaries efficiently

### Future Enhancements
Consider these potential improvements:
- Deduplication of identical person references
- Validation of person URIs
- Integration with person authority records
- Logging of transformation statistics

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**Property**: gmn:P70_11_documents_referenced_person
