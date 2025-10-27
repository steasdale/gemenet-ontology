# Implementation Guide: gmn:P11i_1_earliest_attestation_date

## Complete Step-by-Step Instructions for Implementation

This guide provides detailed instructions for implementing the `gmn:P11i_1_earliest_attestation_date` property across all components of the GMN ontology system.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Ontology Implementation](#ontology-implementation)
3. [Transformation Script Implementation](#transformation-script-implementation)
4. [Testing Procedures](#testing-procedures)
5. [Documentation Updates](#documentation-updates)
6. [Deployment Checklist](#deployment-checklist)

---

## Prerequisites

### Required Knowledge
- Basic understanding of CIDOC-CRM ontology structure
- Familiarity with RDF/Turtle syntax
- Python programming (basic level)
- JSON-LD format understanding

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script
- Main project documentation file

### Software Requirements
- Text editor with TTL syntax support
- Python 3.7 or higher
- RDF validator (optional but recommended)
- Git for version control

---

## Ontology Implementation

### Step 1: Locate Insertion Point

1. Open `gmn_ontology.ttl` in your text editor
2. Search for the comment: `# Property: P11i.1 earliest attestation date`
3. If not found, search for: `# Property: P11i.2 latest attestation date` and insert before it
4. Alternative location: After other P11i properties (around line 200-300)

### Step 2: Add Property Definition

Copy the following TTL code and paste it at the insertion point:

```turtle
# Property: P11i.1 earliest attestation date
gmn:P11i_1_earliest_attestation_date
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P11i.1 earliest attestation date"@en ;
    rdfs:comment "Simplified property for expressing the earliest date at which a person is documented or attested to have been alive in historical sources. Represents the full CIDOC-CRM path: E21_Person > P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82a_begin_of_the_begin. This property captures the earliest known documentary evidence of a person's existence. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P11i_participated_in ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range xsd:date ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P11i_participated_in, cidoc:P4_has_time-span, cidoc:P82a_begin_of_the_begin .
```

### Step 3: Verify TTL Syntax

**Manual Verification:**
1. Check for balanced parentheses and brackets
2. Verify all lines end with proper punctuation (`;` or `.`)
3. Ensure prefix declarations exist at file top:
   ```turtle
   @prefix gmn: <http://genoa-medieval-notarial.org/ontology#> .
   @prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
   @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
   @prefix dcterms: <http://purl.org/dc/terms/> .
   ```

**Automated Validation:**
```bash
# Using rapper (if installed)
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Using riot (Apache Jena, if installed)
riot --validate gmn_ontology.ttl
```

### Step 4: Commit Changes

```bash
git add gmn_ontology.ttl
git commit -m "Add P11i.1 earliest attestation date property

- Adds gmn:P11i_1_earliest_attestation_date as DatatypeProperty
- Domain: cidoc:E21_Person
- Range: xsd:date
- Maps to CIDOC-CRM path: P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82a_begin_of_the_begin
- Created: 2025-10-16"
```

---

## Transformation Script Implementation

### Step 1: Locate Insertion Point

1. Open `gmn_to_cidoc_transform.py` in your text editor
2. Search for: `def transform_p11i_2_latest_attestation_date`
3. Insert the new function **before** this function (around line 1450-1500)

### Step 2: Add Transformation Function

Copy the following Python code and paste it at the insertion point:

```python
def transform_p11i_1_earliest_attestation_date(data):
    """
    Transform gmn:P11i_1_earliest_attestation_date to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82a_begin_of_the_begin
    """
    if 'gmn:P11i_1_earliest_attestation_date' not in data:
        return data
    
    dates = data['gmn:P11i_1_earliest_attestation_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    for date_obj in dates:
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
        else:
            date_value = str(date_obj)
        
        if not date_value:
            continue
        
        event_hash = str(hash(date_value + 'earliest'))[-8:]
        event_uri = f"{subject_uri}/event/earliest_{event_hash}"
        timespan_uri = f"{event_uri}/timespan"
        
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82a_begin_of_the_begin': date_value
            }
        }
        
        data['cidoc:P11i_participated_in'].append(event)
    
    del data['gmn:P11i_1_earliest_attestation_date']
    return data
```

### Step 3: Add Function Call to transform_item()

1. Locate the `transform_item()` function (around line 2200-2400)
2. Find the comment: `# Person attestation and relationship properties`
3. Add the function call **first** in this section:

```python
    # Person attestation and relationship properties
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)
    item = transform_p11i_3_has_spouse(item)
```

### Step 4: Verify Python Syntax

**Check for common issues:**
```python
# Verify imports at top of file (should already exist)
from uuid import uuid4

# Check indentation (4 spaces per level)
# Verify function is properly indented at module level
```

**Run syntax check:**
```bash
python3 -m py_compile gmn_to_cidoc_transform.py
```

### Step 5: Commit Changes

```bash
git add gmn_to_cidoc_transform.py
git commit -m "Add P11i.1 earliest attestation date transformation

- Implements transform_p11i_1_earliest_attestation_date() function
- Transforms gmn:P11i_1_earliest_attestation_date to full CIDOC-CRM structure
- Creates E5_Event with E52_Time-Span and P82a_begin_of_the_begin
- Generates stable URIs using hash-based identifiers
- Handles both dict and string date formats
- Integrated into transform_item() function"
```

---

## Testing Procedures

### Test 1: Basic Transformation

**Input JSON-LD:**
```json
{
  "@id": "http://example.org/person/001",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_1_earliest_attestation_date": "1450-03-15"
}
```

**Expected Output:**
```json
{
  "@id": "http://example.org/person/001",
  "@type": "cidoc:E21_Person",
  "cidoc:P11i_participated_in": [
    {
      "@id": "http://example.org/person/001/event/earliest_12345678",
      "@type": "cidoc:E5_Event",
      "cidoc:P4_has_time-span": {
        "@id": "http://example.org/person/001/event/earliest_12345678/timespan",
        "@type": "cidoc:E52_Time-Span",
        "cidoc:P82a_begin_of_the_begin": "1450-03-15"
      }
    }
  ]
}
```

**Run Test:**
```bash
# Create test input file
cat > test_input.json << 'EOF'
{
  "@id": "http://example.org/person/001",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_1_earliest_attestation_date": "1450-03-15"
}
EOF

# Run transformation
python3 gmn_to_cidoc_transform.py test_input.json test_output.json

# Verify output
cat test_output.json
```

### Test 2: Multiple Dates

**Input:**
```json
{
  "@id": "http://example.org/person/002",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_1_earliest_attestation_date": [
    "1450-03-15",
    "1451-07-22"
  ]
}
```

**Expected Behavior:**
- Two separate E5_Event nodes created
- Each with unique URI based on hash
- Both events in `cidoc:P11i_participated_in` array

### Test 3: Date Object Format

**Input:**
```json
{
  "@id": "http://example.org/person/003",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_1_earliest_attestation_date": [
    {
      "@value": "1450-03-15",
      "@type": "xsd:date"
    }
  ]
}
```

**Expected Behavior:**
- Extracts `@value` from date object
- Creates proper CIDOC-CRM structure
- Ignores `@type` annotation (handled at higher level)

### Test 4: Existing P11i_participated_in

**Input:**
```json
{
  "@id": "http://example.org/person/004",
  "@type": "cidoc:E21_Person",
  "cidoc:P11i_participated_in": [
    {
      "@id": "http://example.org/event/marriage",
      "@type": "cidoc:E5_Event"
    }
  ],
  "gmn:P11i_1_earliest_attestation_date": "1450-03-15"
}
```

**Expected Behavior:**
- Preserves existing P11i_participated_in events
- Appends new attestation event
- No duplication or overwriting

### Test 5: Empty/Missing Values

**Input:**
```json
{
  "@id": "http://example.org/person/005",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_1_earliest_attestation_date": ""
}
```

**Expected Behavior:**
- Function returns data unchanged
- No empty events created
- No errors raised

### Test 6: Integration Test

**Complete transformation with multiple properties:**

```bash
# Create comprehensive test file
cat > test_full.json << 'EOF'
{
  "@id": "http://example.org/person/giovanni_rossi",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Giovanni Rossi",
  "gmn:P11i_1_earliest_attestation_date": "1450-03-15",
  "gmn:P11i_2_latest_attestation_date": "1475-11-30"
}
EOF

# Run transformation
python3 gmn_to_cidoc_transform.py test_full.json test_full_output.json

# Verify all properties transformed correctly
python3 -m json.tool test_full_output.json
```

### Automated Test Script

Create `test_p11i_1.py`:

```python
#!/usr/bin/env python3
"""Unit tests for P11i.1 earliest attestation date transformation."""

import json
import sys
from gmn_to_cidoc_transform import transform_p11i_1_earliest_attestation_date

def test_basic():
    """Test basic single date transformation."""
    data = {
        '@id': 'http://example.org/person/001',
        '@type': 'cidoc:E21_Person',
        'gmn:P11i_1_earliest_attestation_date': '1450-03-15'
    }
    result = transform_p11i_1_earliest_attestation_date(data)
    
    assert 'gmn:P11i_1_earliest_attestation_date' not in result
    assert 'cidoc:P11i_participated_in' in result
    assert len(result['cidoc:P11i_participated_in']) == 1
    
    event = result['cidoc:P11i_participated_in'][0]
    assert event['@type'] == 'cidoc:E5_Event'
    assert 'cidoc:P4_has_time-span' in event
    assert event['cidoc:P4_has_time-span']['cidoc:P82a_begin_of_the_begin'] == '1450-03-15'
    
    print("✓ Test basic: PASSED")

def test_multiple_dates():
    """Test multiple dates."""
    data = {
        '@id': 'http://example.org/person/002',
        'gmn:P11i_1_earliest_attestation_date': ['1450-03-15', '1451-07-22']
    }
    result = transform_p11i_1_earliest_attestation_date(data)
    
    assert len(result['cidoc:P11i_participated_in']) == 2
    print("✓ Test multiple dates: PASSED")

def test_date_object():
    """Test date as object with @value."""
    data = {
        '@id': 'http://example.org/person/003',
        'gmn:P11i_1_earliest_attestation_date': [
            {'@value': '1450-03-15', '@type': 'xsd:date'}
        ]
    }
    result = transform_p11i_1_earliest_attestation_date(data)
    
    event = result['cidoc:P11i_participated_in'][0]
    assert event['cidoc:P4_has_time-span']['cidoc:P82a_begin_of_the_begin'] == '1450-03-15'
    print("✓ Test date object: PASSED")

def test_empty_value():
    """Test empty date value."""
    data = {
        '@id': 'http://example.org/person/004',
        'gmn:P11i_1_earliest_attestation_date': ''
    }
    result = transform_p11i_1_earliest_attestation_date(data)
    
    # Should not create any events for empty value
    assert 'cidoc:P11i_participated_in' not in result or len(result['cidoc:P11i_participated_in']) == 0
    print("✓ Test empty value: PASSED")

def test_no_property():
    """Test when property is not present."""
    data = {
        '@id': 'http://example.org/person/005',
        '@type': 'cidoc:E21_Person'
    }
    result = transform_p11i_1_earliest_attestation_date(data)
    
    assert result == data
    print("✓ Test no property: PASSED")

if __name__ == '__main__':
    try:
        test_basic()
        test_multiple_dates()
        test_date_object()
        test_empty_value()
        test_no_property()
        print("\n✓ All tests PASSED")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

**Run tests:**
```bash
chmod +x test_p11i_1.py
./test_p11i_1.py
```

---

## Documentation Updates

### Step 1: Locate Documentation Section

Find one of these sections in your main documentation:
- "Person Properties"
- "Attestation Properties"  
- "Temporal Properties"
- "P11i Properties"

### Step 2: Add Property Description

Insert the content from `has-earliest-attestation-date-doc-note.txt` in the appropriate section.

### Step 3: Update Cross-References

Add links to related properties:
- Link to `gmn:P11i_2_latest_attestation_date`
- Link to `gmn:P11i_3_has_spouse`
- Update any chronological properties index

### Step 4: Update Examples

Add this property to your comprehensive person examples in documentation.

---

## Deployment Checklist

### Pre-Deployment
- [ ] All TTL syntax validated
- [ ] Python syntax check passed
- [ ] Unit tests all pass
- [ ] Integration test successful
- [ ] Code reviewed by team member
- [ ] Documentation updated and reviewed
- [ ] Commit messages are clear and complete

### Deployment
- [ ] Merge to development branch
- [ ] Run full test suite on development
- [ ] Deploy to staging environment
- [ ] Verify staging works correctly
- [ ] Merge to main/production branch
- [ ] Deploy to production
- [ ] Monitor for errors

### Post-Deployment
- [ ] Verify production deployment
- [ ] Test with real data
- [ ] Update project documentation
- [ ] Notify team of changes
- [ ] Update changelog
- [ ] Tag release in version control

---

## Troubleshooting

### Issue: TTL Validation Fails

**Symptoms:**
- Parse errors when loading ontology
- Syntax errors in validation tools

**Solutions:**
1. Check all prefixes are declared
2. Verify line endings (`;` vs `.`)
3. Check for typos in URIs
4. Ensure proper indentation

### Issue: Transformation Function Not Called

**Symptoms:**
- Property not transformed in output
- Original property still present

**Solutions:**
1. Verify function added to `transform_item()`
2. Check function name spelling
3. Ensure proper indentation in `transform_item()`
4. Verify property name matches exactly (case-sensitive)

### Issue: URI Generation Inconsistent

**Symptoms:**
- Different URIs for same date
- Hash changes between runs

**Solutions:**
- This is expected if data structure changes
- Hash includes date value + 'earliest' string
- To make deterministic, remove randomness from subject_uri

### Issue: Date Format Not Recognized

**Symptoms:**
- Empty output
- Missing timespan values

**Solutions:**
1. Ensure dates in ISO 8601 format (YYYY-MM-DD)
2. Check for dict format with `@value` key
3. Verify xsd:date datatype declaration

---

## Performance Considerations

### Optimization Tips

1. **Batch Processing**: Process multiple items in single run
2. **URI Caching**: Cache generated URIs if processing same data multiple times
3. **Validation**: Validate dates before transformation to avoid empty events

### Expected Performance

- **Small datasets** (<100 records): Near instantaneous
- **Medium datasets** (100-10,000 records): <1 second
- **Large datasets** (10,000+ records): 1-10 seconds

---

## Additional Resources

### CIDOC-CRM Documentation
- [P11i participated in](https://cidoc-crm.org/Property/P11i-participated-in/version-7.1.2)
- [E5 Event](https://cidoc-crm.org/Entity/E5-Event/version-7.1.2)
- [E52 Time-Span](https://cidoc-crm.org/Entity/E52-Time-Span/version-7.1.2)

### Python Resources
- [JSON module documentation](https://docs.python.org/3/library/json.html)
- [UUID module documentation](https://docs.python.org/3/library/uuid.html)

### RDF/Turtle Resources
- [W3C Turtle Specification](https://www.w3.org/TR/turtle/)
- [RDF 1.1 Primer](https://www.w3.org/TR/rdf11-primer/)

---

*Implementation Guide v1.0 - Last updated: 2025-10-26*
