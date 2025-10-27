# Implementation Guide: P70.13 Documents Referenced Place
## GMN Ontology Property

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Ontology Implementation](#ontology-implementation)
4. [Transform Script Implementation](#transform-script-implementation)
5. [Testing Procedures](#testing-procedures)
6. [Integration Steps](#integration-steps)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides step-by-step instructions for implementing the `gmn:P70_13_documents_referenced_place` property across the GMN ontology stack.

**Implementation Scope**:
- Add property definition to GMN ontology (TTL file)
- Add transformation function to Python script
- Update documentation
- Test and validate

**Estimated Time**: 30-45 minutes

**Difficulty**: Low

---

## Prerequisites

### Required Access
- [ ] Write access to `gmn_ontology.ttl`
- [ ] Write access to `gmn_to_cidoc_transform.py`
- [ ] Write access to documentation files

### Required Knowledge
- Basic understanding of RDF/Turtle syntax
- Python programming (basic level)
- Understanding of CIDOC-CRM property structure
- Familiarity with JSON-LD format

### Required Tools
- Text editor with TTL syntax support
- Python 3.7+ environment
- RDF validation tool (optional but recommended)
- Git for version control

---

## Ontology Implementation

### Step 1: Locate Insertion Point

Open `gmn_ontology.ttl` and locate the P70 property section. Find the P70.12 property definition:

```turtle
# Property: P70.12 documents payment through organization
gmn:P70_12_documents_payment_through_organization
    a owl:ObjectProperty ;
    ...
```

The P70.13 property should be added **immediately after** P70.12.

### Step 2: Add Property Definition

Insert the following TTL code:

```turtle
# Property: P70.13 documents referenced place
gmn:P70_13_documents_referenced_place
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.13 documents referenced place"@en ;
    rdfs:comment "Simplified property for associating a sales contract with any place referenced or mentioned in the document text. This captures places that appear in the contract narrative such as neighboring properties used for boundary descriptions, landmarks referenced for location, districts or parishes mentioned, or any other geographic locations named in the contract text. Unlike P94i_3_has_place_of_enactment which indicates where the contract was created, this property represents places mentioned within the contract content. Represents the direct CIDOC-CRM relationship: E31_Document > P67_refers_to > E53_Place. This acknowledges that the place is textually present in the document without implying it is the location of the transaction or the contract's creation."@en ;
    rdfs:subPropertyOf cidoc:P67_refers_to ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E53_Place ;
    dcterms:created "2025-10-27"^^xsd:date ;
    rdfs:seeAlso cidoc:P67_refers_to .
```

### Step 3: Verify TTL Syntax

**Manual Verification Checklist**:
- [ ] Property URI follows naming convention: `gmn:P70_13_documents_referenced_place`
- [ ] Label uses proper numbering: "P70.13 documents referenced place"
- [ ] Comment is enclosed in quotes and ends with `@en`
- [ ] Domain is `gmn:E31_2_Sales_Contract`
- [ ] Range is `cidoc:E53_Place`
- [ ] Date format is correct: `"2025-10-27"^^xsd:date`
- [ ] All lines end with semicolon except last (period)

**Automated Validation** (if available):
```bash
rapper -i turtle gmn_ontology.ttl -o ntriples > /dev/null
```

If validation passes, you should see no error messages.

### Step 4: Commit Changes

```bash
git add gmn_ontology.ttl
git commit -m "Add P70.13 documents_referenced_place property

- Captures places mentioned in contract text
- Distinct from place of contract creation
- Maps to CIDOC-CRM P67_refers_to > E53_Place"
```

---

## Transform Script Implementation

### Step 1: Locate Insertion Point

Open `gmn_to_cidoc_transform.py` and find the transformation function section. Locate:

```python
def transform_p70_12_documents_payment_through_organization(data):
    """
    Transform gmn:P70_12_documents_payment_through_organization...
    """
```

The P70.13 function should be added **immediately after** the P70.12 function.

### Step 2: Add Transformation Function

Insert the following Python code:

```python
def transform_p70_13_documents_referenced_place(data):
    """
    Transform gmn:P70_13_documents_referenced_place to full CIDOC-CRM structure:
    P67_refers_to > E53_Place
    """
    if 'gmn:P70_13_documents_referenced_place' not in data:
        return data
    
    places = data['gmn:P70_13_documents_referenced_place']
    
    # Ensure places is a list
    if not isinstance(places, list):
        places = [places]
    
    # Initialize P67_refers_to if not present
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    # Process each place
    for place_obj in places:
        if isinstance(place_obj, dict):
            # Place is already an object
            place_data = place_obj.copy()
            # Ensure it has the correct type
            if '@type' not in place_data:
                place_data['@type'] = 'cidoc:E53_Place'
        else:
            # Place is just a URI string
            place_uri = str(place_obj)
            place_data = {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        
        # Add to P67_refers_to
        data['cidoc:P67_refers_to'].append(place_data)
    
    # Remove the simplified property
    del data['gmn:P70_13_documents_referenced_place']
    
    return data
```

### Step 3: Add to Main Transform Pipeline

Locate the main transformation function (usually named `transform_item` or similar). Find the section with other P70 transformations:

```python
# Sales contract properties (P70.1-P70.17)
item = transform_p70_1_documents_seller(item)
item = transform_p70_2_documents_buyer(item)
# ... other transformations ...
item = transform_p70_12_documents_payment_through_organization(item)
```

Add the new transformation call in sequence:

```python
item = transform_p70_13_documents_referenced_place(item)
```

**Complete section should look like**:
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
item = transform_p70_11_documents_referenced_person(item)
item = transform_p70_12_documents_payment_through_organization(item)
item = transform_p70_13_documents_referenced_place(item)
item = transform_p70_14_documents_referenced_object(item)
item = transform_p70_15_documents_witness(item)
item = transform_p70_16_documents_sale_price_amount(item)
item = transform_p70_17_documents_sale_price_currency(item)
```

### Step 4: Verify Python Syntax

```bash
python -m py_compile gmn_to_cidoc_transform.py
```

If successful, no output will be displayed.

### Step 5: Commit Changes

```bash
git add gmn_to_cidoc_transform.py
git commit -m "Add P70.13 referenced place transformation

- Transforms to P67_refers_to with E53_Place
- Handles both URI strings and place objects
- Supports multiple place references"
```

---

## Testing Procedures

### Unit Test 1: Single Place URI

**Input Data**:
```json
{
  "@id": "contract:test001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_13_documents_referenced_place": "place:rialto"
}
```

**Expected Output**:
```json
{
  "@id": "contract:test001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "place:rialto",
      "@type": "cidoc:E53_Place"
    }
  ]
}
```

**Test Script**:
```python
def test_single_place_uri():
    input_data = {
        "@id": "contract:test001",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_13_documents_referenced_place": "place:rialto"
    }
    
    result = transform_p70_13_documents_referenced_place(input_data)
    
    assert 'gmn:P70_13_documents_referenced_place' not in result
    assert 'cidoc:P67_refers_to' in result
    assert len(result['cidoc:P67_refers_to']) == 1
    assert result['cidoc:P67_refers_to'][0]['@id'] == "place:rialto"
    assert result['cidoc:P67_refers_to'][0]['@type'] == "cidoc:E53_Place"
    
    print("✓ Test 1 passed: Single place URI")
```

### Unit Test 2: Multiple Places

**Input Data**:
```json
{
  "@id": "contract:test002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_13_documents_referenced_place": [
    "place:san_polo",
    "place:grand_canal"
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
      "@id": "place:san_polo",
      "@type": "cidoc:E53_Place"
    },
    {
      "@id": "place:grand_canal",
      "@type": "cidoc:E53_Place"
    }
  ]
}
```

**Test Script**:
```python
def test_multiple_places():
    input_data = {
        "@id": "contract:test002",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_13_documents_referenced_place": [
            "place:san_polo",
            "place:grand_canal"
        ]
    }
    
    result = transform_p70_13_documents_referenced_place(input_data)
    
    assert 'gmn:P70_13_documents_referenced_place' not in result
    assert 'cidoc:P67_refers_to' in result
    assert len(result['cidoc:P67_refers_to']) == 2
    
    print("✓ Test 2 passed: Multiple places")
```

### Unit Test 3: Place Object with Details

**Input Data**:
```json
{
  "@id": "contract:test003",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_13_documents_referenced_place": {
    "@id": "place:rialto_bridge",
    "@type": "cidoc:E53_Place",
    "rdfs:label": "Rialto Bridge",
    "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300008193"
  }
}
```

**Expected Output**:
```json
{
  "@id": "contract:test003",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "place:rialto_bridge",
      "@type": "cidoc:E53_Place",
      "rdfs:label": "Rialto Bridge",
      "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300008193"
    }
  ]
}
```

**Test Script**:
```python
def test_place_object_with_details():
    input_data = {
        "@id": "contract:test003",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_13_documents_referenced_place": {
            "@id": "place:rialto_bridge",
            "@type": "cidoc:E53_Place",
            "rdfs:label": "Rialto Bridge",
            "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300008193"
        }
    }
    
    result = transform_p70_13_documents_referenced_place(input_data)
    
    assert 'gmn:P70_13_documents_referenced_place' not in result
    assert 'cidoc:P67_refers_to' in result
    assert result['cidoc:P67_refers_to'][0]['rdfs:label'] == "Rialto Bridge"
    
    print("✓ Test 3 passed: Place object with details")
```

### Unit Test 4: Missing Property (No Error)

**Input Data**:
```json
{
  "@id": "contract:test004",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": "person:seller123"
}
```

**Expected Output**: Same as input (no changes)

**Test Script**:
```python
def test_missing_property():
    input_data = {
        "@id": "contract:test004",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_1_documents_seller": "person:seller123"
    }
    
    result = transform_p70_13_documents_referenced_place(input_data)
    
    assert result == input_data
    assert 'cidoc:P67_refers_to' not in result
    
    print("✓ Test 4 passed: Missing property handled gracefully")
```

### Integration Test: Complete Contract

**Input Data**:
```json
{
  "@id": "contract:1458_03_15_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P1_1_has_name": "Sale of house in San Polo",
  "gmn:P70_1_documents_seller": "person:giovanni_rossi",
  "gmn:P70_2_documents_buyer": "person:marco_bianchi",
  "gmn:P70_3_documents_transfer_of": "property:house_123",
  "gmn:P70_13_documents_referenced_place": [
    "place:san_polo_parish",
    "place:grand_canal",
    "place:rialto_market"
  ],
  "gmn:P94i_3_has_place_of_enactment": "place:notary_office"
}
```

**Validation Steps**:
1. Transform the complete contract
2. Verify P70.13 is removed
3. Verify P67_refers_to contains 3 places
4. Verify P94i_3 is transformed separately (place of enactment)
5. Verify no data loss in other properties
6. Check valid CIDOC-CRM structure

**Test Script**:
```python
def test_complete_contract():
    input_data = {
        "@id": "contract:1458_03_15_001",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P1_1_has_name": "Sale of house in San Polo",
        "gmn:P70_13_documents_referenced_place": [
            "place:san_polo_parish",
            "place:grand_canal",
            "place:rialto_market"
        ]
    }
    
    # Run through full transformation pipeline
    result = transform_item(input_data)
    
    # Verify transformations
    assert 'gmn:P70_13_documents_referenced_place' not in result
    assert 'cidoc:P67_refers_to' in result
    assert len(result['cidoc:P67_refers_to']) == 3
    
    # Check each place has correct type
    for place in result['cidoc:P67_refers_to']:
        assert place['@type'] == 'cidoc:E53_Place'
        assert '@id' in place
    
    print("✓ Integration test passed: Complete contract")
```

### Running All Tests

**Complete Test Suite**:
```python
if __name__ == "__main__":
    print("Running P70.13 transformation tests...\n")
    
    test_single_place_uri()
    test_multiple_places()
    test_place_object_with_details()
    test_missing_property()
    test_complete_contract()
    
    print("\n✓ All tests passed successfully!")
```

---

## Integration Steps

### Step 1: Update Documentation

Add property description to main documentation file. See `documents-place-doc-note.txt` for ready-to-copy text.

**Location**: After P70.12 section

**Content**: Copy the property definition, examples, and usage notes

### Step 2: Update Property Index

If your documentation includes a property index or table, add:

| Property | Label | Domain | Range |
|----------|-------|--------|-------|
| gmn:P70_13_documents_referenced_place | P70.13 documents referenced place | gmn:E31_2_Sales_Contract | cidoc:E53_Place |

### Step 3: Deploy to Test Environment

1. Deploy updated ontology file
2. Deploy updated transformation script
3. Run test suite against test database
4. Validate output RDF

### Step 4: Data Migration (if needed)

If existing data uses this property:

```python
# Migration script
def migrate_existing_contracts():
    contracts = get_all_contracts()
    
    for contract in contracts:
        if has_property(contract, 'gmn:P70_13_documents_referenced_place'):
            transformed = transform_p70_13_documents_referenced_place(contract)
            save_contract(transformed)
    
    print(f"Migrated {len(contracts)} contracts")
```

### Step 5: Production Deployment

1. Create deployment branch
2. Run final validation
3. Merge to main branch
4. Deploy to production
5. Monitor transformation logs
6. Verify data integrity

---

## Troubleshooting

### Problem: TTL Validation Fails

**Symptoms**: RDF parser errors when loading ontology

**Solutions**:
1. Check for missing semicolons or periods
2. Verify quote marks are straight quotes (not curly)
3. Ensure language tags are lowercase (@en not @EN)
4. Validate date format: `"YYYY-MM-DD"^^xsd:date`

**Validation Command**:
```bash
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null
```

### Problem: Python Import Errors

**Symptoms**: `ModuleNotFoundError` or import failures

**Solutions**:
1. Ensure function is defined before being called
2. Check function name spelling
3. Verify indentation (Python requires consistent indentation)

**Test Import**:
```python
python -c "from gmn_to_cidoc_transform import transform_p70_13_documents_referenced_place"
```

### Problem: Type Not Inferred

**Symptoms**: Place objects missing `@type` in output

**Solutions**:
1. Check if type inference logic is present in function
2. Verify the line: `if '@type' not in place_data: place_data['@type'] = 'cidoc:E53_Place'`
3. Test with minimal input

**Debug Code**:
```python
# Add before returning data
print(f"DEBUG: place_data = {json.dumps(place_data, indent=2)}")
```

### Problem: Duplicate P67 References

**Symptoms**: Multiple entries for same place in P67_refers_to

**Solutions**:
1. Check if transformation is called multiple times
2. Verify input data doesn't already have P67_refers_to
3. Consider deduplication logic if needed

**Deduplication Code**:
```python
# Before returning, remove duplicates
seen = set()
unique_refs = []
for ref in data['cidoc:P67_refers_to']:
    ref_id = ref.get('@id')
    if ref_id not in seen:
        seen.add(ref_id)
        unique_refs.append(ref)
data['cidoc:P67_refers_to'] = unique_refs
```

### Problem: Transformation Not Applied

**Symptoms**: GMN property still present after transformation

**Solutions**:
1. Verify function is called in main pipeline
2. Check function order (should be after P70.12)
3. Ensure function returns modified data
4. Check if property name matches exactly

**Debug Pipeline**:
```python
# Add after transformation call
print(f"After P70.13: {'gmn:P70_13_documents_referenced_place' in item}")
```

### Problem: Test Failures

**Symptoms**: Unit tests fail unexpectedly

**Solutions**:
1. Print actual vs expected output
2. Check for whitespace differences
3. Verify test data is valid JSON
4. Run tests individually to isolate issues

**Debug Test**:
```python
import json
print("Expected:")
print(json.dumps(expected, indent=2))
print("\nActual:")
print(json.dumps(result, indent=2))
```

---

## Best Practices

### Code Quality
- ✅ Use descriptive variable names
- ✅ Add docstrings to functions
- ✅ Handle edge cases (None, empty lists)
- ✅ Include error handling where appropriate
- ✅ Follow project coding standards

### Testing
- ✅ Test with real contract data
- ✅ Test boundary conditions
- ✅ Include negative tests (missing properties)
- ✅ Test integration with other properties
- ✅ Validate CIDOC-CRM compliance

### Documentation
- ✅ Document semantic meaning clearly
- ✅ Provide concrete examples
- ✅ Explain differences from similar properties
- ✅ Include use case scenarios
- ✅ Keep documentation in sync with code

### Version Control
- ✅ Commit logical units of work
- ✅ Write descriptive commit messages
- ✅ Create feature branch for changes
- ✅ Request code review before merging
- ✅ Tag releases with version numbers

---

## Checklist Summary

### Ontology File
- [ ] TTL code added after P70.12
- [ ] Syntax validated
- [ ] Committed with descriptive message

### Transform Script
- [ ] Function added after P70.12 transformation
- [ ] Function called in main pipeline
- [ ] Python syntax validated
- [ ] Committed with descriptive message

### Testing
- [ ] Unit tests written and passing
- [ ] Integration tests run successfully
- [ ] Edge cases tested
- [ ] Performance acceptable

### Documentation
- [ ] Property documented
- [ ] Examples added
- [ ] Property index updated
- [ ] Changes committed

### Deployment
- [ ] Deployed to test environment
- [ ] Validated with test data
- [ ] Deployed to production
- [ ] Monitoring in place

---

## Next Steps

After successful implementation:

1. **Monitor Usage**: Track how often the property is used
2. **Gather Feedback**: Collect input from data entry team
3. **Refine Documentation**: Update based on real-world usage
4. **Consider Extensions**: Evaluate if additional place properties needed
5. **Knowledge Sharing**: Brief team on new property

---

## Contact & Support

For implementation questions:
- Review this guide thoroughly
- Check project documentation
- Consult with ontology team lead
- Reference CIDOC-CRM documentation

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-27  
**Author**: GMN Development Team
