# P70.3 Documents Transfer Of - Implementation Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Ontology Implementation](#ontology-implementation)
3. [Python Transformation Implementation](#python-transformation-implementation)
4. [Testing](#testing)
5. [Integration](#integration)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main GMN ontology file
- `gmn_to_cidoc_transform.py` - Python transformation script

### Required Knowledge
- Basic understanding of RDF/Turtle syntax
- Python programming fundamentals
- CIDOC-CRM ontology structure
- JSON-LD data format

### Required Tools
- RDF validation tool (e.g., Raptor, rdflib)
- Python 3.7 or higher
- JSON-LD processor
- Text editor with syntax highlighting

---

## Ontology Implementation

### Step 1: Locate the Property Section

Open your `gmn_ontology.ttl` file and navigate to the sales contract properties section. Look for:

```turtle
# Property: P70.2 documents buyer
gmn:P70_2_documents_buyer
    a owl:ObjectProperty ;
    ...
```

### Step 2: Add the P70.3 Property Definition

Add the following complete property definition immediately after the P70.2 property:

```turtle
# Property: P70.3 documents transfer of
gmn:P70_3_documents_transfer_of
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.3 documents transfer of"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the physical thing (property, object, or person) being transferred. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The range includes buildings (gmn:E22_1_Building), moveable property (gmn:E22_2_Moveable_Property), and persons (E21_Person, for the historical documentation of enslaved persons or other instances where people were treated as property)."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E18_Physical_Thing ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P24_transferred_title_of .
```

### Step 3: Verify Property Placement

Ensure the property is placed in the correct sequence:
1. P70.1 documents seller
2. P70.2 documents buyer
3. **P70.3 documents transfer of** ← New property
4. P70.4 documents seller's procurator
5. P70.5 documents buyer's procurator

### Step 4: Validate the Ontology

Run validation to ensure proper syntax:

```bash
# Using rapper (Raptor)
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Using rdflib (Python)
python -c "from rdflib import Graph; g = Graph(); g.parse('gmn_ontology.ttl', format='turtle'); print('Valid')"
```

Expected output: No errors, validation successful.

### Step 5: Check Property Metadata

Verify that all required metadata fields are present:
- ✅ Property type declarations (owl:ObjectProperty, rdf:Property)
- ✅ Label with language tag
- ✅ Comment with full CIDOC-CRM path
- ✅ rdfs:subPropertyOf declaration
- ✅ rdfs:domain specification
- ✅ rdfs:range specification
- ✅ dcterms:created date
- ✅ rdfs:seeAlso cross-references

---

## Python Transformation Implementation

### Step 1: Locate the Transformation Section

Open your `gmn_to_cidoc_transform.py` file and find the transform function for P70.2:

```python
def transform_p70_2_documents_buyer(data):
    """
    Transform gmn:P70_2_documents_buyer to full CIDOC-CRM structure
    """
    # ... function body ...
```

### Step 2: Add the P70.3 Transformation Function

Add the following complete function immediately after the P70.2 function:

```python
def transform_p70_3_documents_transfer_of(data):
    """
    Transform gmn:P70_3_documents_transfer_of to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing
    """
    if 'gmn:P70_3_documents_transfer_of' not in data:
        return data
    
    things = data['gmn:P70_3_documents_transfer_of']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create or locate the E8_Acquisition node
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P24_transferred_title_of array if needed
    if 'cidoc:P24_transferred_title_of' not in acquisition:
        acquisition['cidoc:P24_transferred_title_of'] = []
    
    # Process each thing being transferred
    for thing_obj in things:
        if isinstance(thing_obj, dict):
            thing_data = thing_obj.copy()
            # Preserve specific type if provided, default to E18_Physical_Thing
            if '@type' not in thing_data:
                thing_data['@type'] = 'cidoc:E18_Physical_Thing'
        else:
            # Handle URI string reference
            thing_uri = str(thing_obj)
            thing_data = {
                '@id': thing_uri,
                '@type': 'cidoc:E18_Physical_Thing'
            }
        
        acquisition['cidoc:P24_transferred_title_of'].append(thing_data)
    
    # Remove the simplified property
    del data['gmn:P70_3_documents_transfer_of']
    return data
```

### Step 3: Verify Imports

Ensure the required import is present at the top of the file:

```python
from uuid import uuid4
```

### Step 4: Register the Transformation Function

Locate the main transformation registration section (usually near the bottom of the file) and add the P70.3 transformation:

```python
# Sales Contract Properties
transform_functions = [
    # ... other transformations ...
    transform_p70_1_documents_seller,
    transform_p70_2_documents_buyer,
    transform_p70_3_documents_transfer_of,  # ← Add this line
    transform_p70_4_documents_sellers_procurator,
    # ... more transformations ...
]
```

### Step 5: Code Review Checklist

Verify the following in your implementation:

- [ ] Function name matches: `transform_p70_3_documents_transfer_of`
- [ ] Docstring clearly explains the transformation
- [ ] Property key check: `'gmn:P70_3_documents_transfer_of'`
- [ ] Creates or reuses E8_Acquisition node
- [ ] Initializes P24_transferred_title_of array
- [ ] Handles both dict and string inputs
- [ ] Preserves specific types when provided
- [ ] Defaults to E18_Physical_Thing when type not specified
- [ ] Removes the simplified property after transformation
- [ ] Returns the modified data structure

---

## Testing

### Test 1: Single Building Transfer

**Input:**
```json
{
  "@id": "https://example.org/contract/c001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "https://example.org/building/b001",
      "@type": "gmn:E22_1_Building",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "@value": "House on Via Luccoli"
      }
    }
  ]
}
```

**Expected Output:**
```json
{
  "@id": "https://example.org/contract/c001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://example.org/contract/c001/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "https://example.org/building/b001",
          "@type": "gmn:E22_1_Building",
          "cidoc:P1_is_identified_by": {
            "@type": "cidoc:E41_Appellation",
            "@value": "House on Via Luccoli"
          }
        }
      ]
    }
  ]
}
```

**Verification:**
```python
def test_single_building_transfer():
    input_data = {
        "@id": "https://example.org/contract/c001",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_3_documents_transfer_of": [
            {
                "@id": "https://example.org/building/b001",
                "@type": "gmn:E22_1_Building"
            }
        ]
    }
    
    result = transform_p70_3_documents_transfer_of(input_data)
    
    # Verify structure
    assert 'cidoc:P70_documents' in result
    assert len(result['cidoc:P70_documents']) == 1
    
    acquisition = result['cidoc:P70_documents'][0]
    assert acquisition['@type'] == 'cidoc:E8_Acquisition'
    assert 'cidoc:P24_transferred_title_of' in acquisition
    
    things = acquisition['cidoc:P24_transferred_title_of']
    assert len(things) == 1
    assert things[0]['@type'] == 'gmn:E22_1_Building'
    assert things[0]['@id'] == 'https://example.org/building/b001'
    
    # Verify cleanup
    assert 'gmn:P70_3_documents_transfer_of' not in result
    
    print("✅ Test 1 passed: Single building transfer")
```

### Test 2: Multiple Mixed Items

**Input:**
```json
{
  "@id": "https://example.org/contract/c002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "https://example.org/building/b002",
      "@type": "gmn:E22_1_Building"
    },
    {
      "@id": "https://example.org/object/goods001",
      "@type": "gmn:E22_2_Moveable_Property"
    }
  ]
}
```

**Expected Output:**
```json
{
  "@id": "https://example.org/contract/c002",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://example.org/contract/c002/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "https://example.org/building/b002",
          "@type": "gmn:E22_1_Building"
        },
        {
          "@id": "https://example.org/object/goods001",
          "@type": "gmn:E22_2_Moveable_Property"
        }
      ]
    }
  ]
}
```

**Verification:**
```python
def test_multiple_mixed_items():
    input_data = {
        "@id": "https://example.org/contract/c002",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_3_documents_transfer_of": [
            {"@id": "https://example.org/building/b002", "@type": "gmn:E22_1_Building"},
            {"@id": "https://example.org/object/goods001", "@type": "gmn:E22_2_Moveable_Property"}
        ]
    }
    
    result = transform_p70_3_documents_transfer_of(input_data)
    
    acquisition = result['cidoc:P70_documents'][0]
    things = acquisition['cidoc:P24_transferred_title_of']
    
    assert len(things) == 2
    assert things[0]['@type'] == 'gmn:E22_1_Building'
    assert things[1]['@type'] == 'gmn:E22_2_Moveable_Property'
    
    print("✅ Test 2 passed: Multiple mixed items")
```

### Test 3: URI String Reference

**Input:**
```json
{
  "@id": "https://example.org/contract/c003",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_3_documents_transfer_of": [
    "https://example.org/building/b003"
  ]
}
```

**Expected Output:**
```json
{
  "@id": "https://example.org/contract/c003",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://example.org/contract/c003/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "https://example.org/building/b003",
          "@type": "cidoc:E18_Physical_Thing"
        }
      ]
    }
  ]
}
```

**Verification:**
```python
def test_uri_string_reference():
    input_data = {
        "@id": "https://example.org/contract/c003",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_3_documents_transfer_of": [
            "https://example.org/building/b003"
        ]
    }
    
    result = transform_p70_3_documents_transfer_of(input_data)
    
    acquisition = result['cidoc:P70_documents'][0]
    things = acquisition['cidoc:P24_transferred_title_of']
    
    assert len(things) == 1
    assert things[0]['@id'] == 'https://example.org/building/b003'
    assert things[0]['@type'] == 'cidoc:E18_Physical_Thing'
    
    print("✅ Test 3 passed: URI string reference")
```

### Test 4: Integration with Other Properties

**Input:**
```json
{
  "@id": "https://example.org/contract/c004",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [
    {
      "@id": "https://example.org/person/seller001",
      "@type": "cidoc:E21_Person"
    }
  ],
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "https://example.org/person/buyer001",
      "@type": "cidoc:E21_Person"
    }
  ],
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "https://example.org/building/b004",
      "@type": "gmn:E22_1_Building"
    }
  ]
}
```

**Expected Output:**
```json
{
  "@id": "https://example.org/contract/c004",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://example.org/contract/c004/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P23_transferred_title_from": [
        {
          "@id": "https://example.org/person/seller001",
          "@type": "cidoc:E21_Person"
        }
      ],
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "https://example.org/person/buyer001",
          "@type": "cidoc:E21_Person"
        }
      ],
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "https://example.org/building/b004",
          "@type": "gmn:E22_1_Building"
        }
      ]
    }
  ]
}
```

**Verification:**
```python
def test_integration_with_other_properties():
    # Run all three transformations in sequence
    input_data = {
        "@id": "https://example.org/contract/c004",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_1_documents_seller": [{"@id": "https://example.org/person/seller001", "@type": "cidoc:E21_Person"}],
        "gmn:P70_2_documents_buyer": [{"@id": "https://example.org/person/buyer001", "@type": "cidoc:E21_Person"}],
        "gmn:P70_3_documents_transfer_of": [{"@id": "https://example.org/building/b004", "@type": "gmn:E22_1_Building"}]
    }
    
    result = transform_p70_1_documents_seller(input_data)
    result = transform_p70_2_documents_buyer(result)
    result = transform_p70_3_documents_transfer_of(result)
    
    acquisition = result['cidoc:P70_documents'][0]
    
    # All three properties should be on the same acquisition node
    assert 'cidoc:P23_transferred_title_from' in acquisition
    assert 'cidoc:P22_transferred_title_to' in acquisition
    assert 'cidoc:P24_transferred_title_of' in acquisition
    
    print("✅ Test 4 passed: Integration with other properties")
```

### Running All Tests

```python
def run_all_tests():
    print("Starting P70.3 transformation tests...\n")
    
    test_single_building_transfer()
    test_multiple_mixed_items()
    test_uri_string_reference()
    test_integration_with_other_properties()
    
    print("\n✅ All tests passed successfully!")

if __name__ == "__main__":
    run_all_tests()
```

---

## Integration

### Step 1: Update Main Transformation Pipeline

Locate your main transformation orchestration function (typically named `transform_document` or similar):

```python
def transform_document(data):
    """
    Transform GMN simplified properties to full CIDOC-CRM structure.
    """
    # Apply all transformations in sequence
    data = transform_p1_2_has_name_from_source(data)
    data = transform_p11i_1_earliest_attestation_date(data)
    # ... other transformations ...
    data = transform_p70_1_documents_seller(data)
    data = transform_p70_2_documents_buyer(data)
    data = transform_p70_3_documents_transfer_of(data)  # ← Add this line
    data = transform_p70_4_documents_sellers_procurator(data)
    # ... more transformations ...
    
    return data
```

### Step 2: Update Documentation

Add the property to your internal documentation:

1. **Property Registry:** Add P70.3 to the list of implemented properties
2. **Transformation Map:** Document the GMN → CIDOC-CRM mapping
3. **Usage Examples:** Include examples in user guides
4. **API Documentation:** Update API docs if transformation is exposed via API

### Step 3: Update Version Information

Update version metadata in your project:

```python
# In your configuration or constants file
GMN_ONTOLOGY_VERSION = "1.x"
SUPPORTED_PROPERTIES = [
    # ... existing properties ...
    "gmn:P70_3_documents_transfer_of",
]
LAST_UPDATED = "2025-10-27"
```

---

## Troubleshooting

### Issue 1: Property Not Being Transformed

**Symptoms:**
- Input data contains `gmn:P70_3_documents_transfer_of`
- Output data still contains `gmn:P70_3_documents_transfer_of` (not transformed)

**Possible Causes:**
1. Transformation function not registered in pipeline
2. Function name typo in registration
3. Transformation function not being called

**Solutions:**
```python
# Verify function is in transformation list
if 'transform_p70_3_documents_transfer_of' not in [f.__name__ for f in transform_functions]:
    print("⚠️ WARNING: P70.3 transformation not registered!")

# Check if function is being called
import logging
logging.debug(f"Calling transform_p70_3_documents_transfer_of")
```

### Issue 2: Multiple Acquisition Nodes Created

**Symptoms:**
- Output has multiple E8_Acquisition objects in `cidoc:P70_documents` array
- Expected single shared acquisition node

**Possible Cause:**
Transformations running in wrong order or not checking for existing acquisition node

**Solution:**
```python
# Ensure all P70 transformations check for existing acquisition node:
if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
    # Only create if doesn't exist
    acquisition_uri = f"{subject_uri}/acquisition"
    data['cidoc:P70_documents'] = [{
        '@id': acquisition_uri,
        '@type': 'cidoc:E8_Acquisition'
    }]

# Always use the first (shared) acquisition node
acquisition = data['cidoc:P70_documents'][0]
```

### Issue 3: Type Information Lost

**Symptoms:**
- Input specifies `gmn:E22_1_Building`
- Output shows only `cidoc:E18_Physical_Thing`

**Possible Cause:**
Type preservation logic not working correctly

**Solution:**
```python
# Verify this logic in your function:
if isinstance(thing_obj, dict):
    thing_data = thing_obj.copy()  # ← Must use .copy()
    if '@type' not in thing_data:
        thing_data['@type'] = 'cidoc:E18_Physical_Thing'
    # Type is preserved if it exists in input
```

### Issue 4: URI String Not Handled

**Symptoms:**
- Input contains string URI: `"https://example.org/thing"`
- Transformation fails or produces incorrect output

**Possible Cause:**
Missing logic to handle string URIs

**Solution:**
```python
# Ensure you handle both dict and string:
for thing_obj in things:
    if isinstance(thing_obj, dict):
        # Handle dict...
    else:
        # Handle string URI
        thing_uri = str(thing_obj)
        thing_data = {
            '@id': thing_uri,
            '@type': 'cidoc:E18_Physical_Thing'
        }
```

### Issue 5: Property Not Deleted After Transformation

**Symptoms:**
- Both `gmn:P70_3_documents_transfer_of` and `cidoc:P70_documents` present in output
- Data duplication

**Possible Cause:**
Missing deletion statement

**Solution:**
```python
# Add at end of function:
del data['gmn:P70_3_documents_transfer_of']
return data
```

### Debugging Tips

1. **Add Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

def transform_p70_3_documents_transfer_of(data):
    logging.debug("P70.3 transformation started")
    logging.debug(f"Input: {data.get('gmn:P70_3_documents_transfer_of')}")
    # ... transformation logic ...
    logging.debug(f"Output: {data.get('cidoc:P70_documents')}")
    return data
```

2. **Validate Each Step:**
```python
# After each major operation, validate:
assert 'cidoc:P70_documents' in data, "P70_documents should exist"
assert len(data['cidoc:P70_documents']) > 0, "Should have at least one acquisition"
```

3. **Use Pretty Printing:**
```python
import json
print(json.dumps(data, indent=2))
```

---

## Next Steps

After successful implementation:

1. ✅ Run all test cases
2. ✅ Validate with real historical data
3. ✅ Update project documentation
4. ✅ Commit changes to version control
5. ✅ Deploy to staging environment
6. ✅ Monitor transformation logs
7. ✅ Update user training materials

---

## Additional Resources

- **CIDOC-CRM Documentation:** http://www.cidoc-crm.org/
- **E8 Acquisition Specification:** CIDOC-CRM v7.x documentation
- **P24 transferred_title_of:** CIDOC-CRM property definition
- **GMN Ontology Main Documentation:** See project documentation files

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-27  
**Maintainer:** GMN Ontology Project Team
