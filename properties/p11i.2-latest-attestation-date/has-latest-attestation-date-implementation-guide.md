# Implementation Guide: gmn:P11i_2_latest_attestation_date
## Step-by-Step Instructions for Latest Attestation Date Property

**Status**: ✅ Already Fully Implemented  
**Last Updated**: October 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Current Implementation Status](#current-implementation-status)
3. [Ontology Definition](#ontology-definition)
4. [Python Transformation Function](#python-transformation-function)
5. [Integration Points](#integration-points)
6. [Testing Procedures](#testing-procedures)
7. [Usage Examples](#usage-examples)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### Purpose

This guide provides technical implementation details for the `gmn:P11i_2_latest_attestation_date` property. Since the property is **already fully implemented**, this guide serves as:

- Reference documentation for developers
- Testing procedures for quality assurance
- Maintenance guidance for future updates
- Integration examples for new features

### Key Information

- **Property IRI**: `gmn:P11i_2_latest_attestation_date`
- **Type**: `owl:DatatypeProperty`
- **Domain**: `cidoc:E21_Person`
- **Range**: `xsd:date`
- **Super Property**: `cidoc:P11i_participated_in`

---

## Current Implementation Status

### ✅ Completed Components

1. **Ontology Definition** (in `gmn_ontology.ttl`)
   - Lines 143-152
   - Fully documented with rdfs:label and rdfs:comment
   - Includes proper domain, range, and super property declarations
   - Has dcterms:created date and rdfs:seeAlso references

2. **Transformation Function** (in `gmn_to_cidoc_transform.py`)
   - Function: `transform_p11i_2_latest_attestation_date(data)`
   - Lines approximately 300-350 (varies with updates)
   - Handles single and multiple dates
   - Creates proper CIDOC-CRM event structure
   - Includes URI generation and hashing

3. **Pipeline Integration** (in `gmn_to_cidoc_transform.py`)
   - Called in main `transform_item()` function
   - Positioned logically with other person attestation properties
   - Executes before editorial notes (to preserve data flow)

### 📋 Verification Checklist

Run through this checklist to verify the implementation:

- [ ] Ontology file contains property definition
- [ ] Property has correct RDF type declarations
- [ ] Domain and range are properly specified
- [ ] Super property relationship is declared
- [ ] Transformation function exists and is named correctly
- [ ] Function is called in the main transformation pipeline
- [ ] Function handles edge cases (missing data, multiple dates)
- [ ] Generated URIs are stable and deterministic
- [ ] Output structure matches CIDOC-CRM specification

---

## Ontology Definition

### Location

File: `gmn_ontology.ttl`  
Lines: 143-152

### Current Definition

```turtle
# Property: P11i.2 latest attestation date
gmn:P11i_2_latest_attestation_date
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P11i.2 latest attestation date"@en ;
    rdfs:comment "Simplified property for expressing the latest date at which a person is documented or attested to have been alive in historical sources. Represents the full CIDOC-CRM path: E21_Person > P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82b_end_of_the_end. This property captures the last known documentary evidence of a person's existence. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P11i_participated_in ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range xsd:date ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P11i_participated_in, cidoc:P4_has_time-span, cidoc:P82b_end_of_the_end .
```

### Key Components Explained

1. **Type Declarations**
   ```turtle
   a owl:DatatypeProperty ;
   a rdf:Property ;
   ```
   - Declares the property as both OWL and RDF property types
   - DatatypeProperty indicates the range is a literal (date) not an object

2. **Label and Comment**
   ```turtle
   rdfs:label "P11i.2 latest attestation date"@en ;
   rdfs:comment "Simplified property for expressing the latest date..."@en ;
   ```
   - Human-readable label for display
   - Detailed comment explaining purpose and transformation path

3. **Domain and Range**
   ```turtle
   rdfs:domain cidoc:E21_Person ;
   rdfs:range xsd:date ;
   ```
   - Domain: Can only be used with E21_Person entities
   - Range: Values must be xsd:date literals

4. **Super Property**
   ```turtle
   rdfs:subPropertyOf cidoc:P11i_participated_in ;
   ```
   - Establishes relationship to parent CIDOC-CRM property
   - Enables property hierarchy reasoning

5. **Metadata**
   ```turtle
   dcterms:created "2025-10-16"^^xsd:date ;
   rdfs:seeAlso cidoc:P11i_participated_in, cidoc:P4_has_time-span, cidoc:P82b_end_of_the_end ;
   ```
   - Creation date for provenance
   - Related properties for reference

### Modification Instructions (If Needed)

If you need to modify the ontology definition:

1. Open `gmn_ontology.ttl` in a text editor
2. Locate lines 143-152
3. Make changes carefully, preserving TTL syntax
4. Validate the TTL file using a validator (e.g., `rapper` or online tools)
5. Test with sample data before committing changes

---

## Python Transformation Function

### Location

File: `gmn_to_cidoc_transform.py`  
Function: `transform_p11i_2_latest_attestation_date(data)`

### Complete Function Code

```python
def transform_p11i_2_latest_attestation_date(data):
    """
    Transform gmn:P11i_2_latest_attestation_date to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82b_end_of_the_end
    """
    if 'gmn:P11i_2_latest_attestation_date' not in data:
        return data
    
    dates = data['gmn:P11i_2_latest_attestation_date']
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
        
        event_hash = str(hash(date_value + 'latest'))[-8:]
        event_uri = f"{subject_uri}/event/latest_{event_hash}"
        timespan_uri = f"{event_uri}/timespan"
        
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82b_end_of_the_end': date_value
            }
        }
        
        data['cidoc:P11i_participated_in'].append(event)
    
    del data['gmn:P11i_2_latest_attestation_date']
    return data
```

### Function Flow Explanation

#### Step 1: Check for Property Presence

```python
if 'gmn:P11i_2_latest_attestation_date' not in data:
    return data
```

- Early return if the property doesn't exist
- Prevents unnecessary processing
- Safe for records without this property

#### Step 2: Extract Date Values

```python
dates = data['gmn:P11i_2_latest_attestation_date']
subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
```

- Gets the date value(s) from the data
- Retrieves the subject URI or generates a UUID fallback
- Prepares for event creation

#### Step 3: Initialize Target Structure

```python
if 'cidoc:P11i_participated_in' not in data:
    data['cidoc:P11i_participated_in'] = []
```

- Creates the P11i_participated_in array if it doesn't exist
- Allows multiple events (earliest, latest, other attestations) to coexist

#### Step 4: Process Each Date

```python
for date_obj in dates:
    if isinstance(date_obj, dict):
        date_value = date_obj.get('@value', '')
    else:
        date_value = str(date_obj)
    
    if not date_value:
        continue
```

- Handles both simple string dates and JSON-LD date objects
- Extracts the actual date value
- Skips empty or null dates

#### Step 5: Generate Unique URIs

```python
event_hash = str(hash(date_value + 'latest'))[-8:]
event_uri = f"{subject_uri}/event/latest_{event_hash}"
timespan_uri = f"{event_uri}/timespan"
```

- Creates deterministic hash from date value + 'latest'
- Generates unique event URI (prevents collisions with earliest attestation)
- Creates timespan URI as child of event URI
- URIs are stable: same input always produces same output

#### Step 6: Build CIDOC-CRM Structure

```python
event = {
    '@id': event_uri,
    '@type': 'cidoc:E5_Event',
    'cidoc:P4_has_time-span': {
        '@id': timespan_uri,
        '@type': 'cidoc:E52_Time-Span',
        'cidoc:P82b_end_of_the_end': date_value
    }
}
```

- Creates nested JSON-LD structure
- E5_Event represents the attestation event
- E52_Time-Span holds the temporal information
- P82b_end_of_the_end is specifically the "latest" bound

#### Step 7: Add to Output and Clean Up

```python
data['cidoc:P11i_participated_in'].append(event)

del data['gmn:P11i_2_latest_attestation_date']
return data
```

- Appends the event to the P11i_participated_in array
- Removes the simplified property (transformation complete)
- Returns the modified data structure

### Key Design Decisions

1. **Hash Suffix**: Uses 'latest' (vs 'earliest') to ensure unique event URIs
2. **Array Structure**: Allows multiple attestations per person
3. **Nested Objects**: Creates inline timespan (not separate top-level entity)
4. **Date Format**: Preserves input date format (no conversion)
5. **Error Handling**: Gracefully skips empty or invalid dates

---

## Integration Points

### Main Transformation Pipeline

The function is called in `transform_item()` within the person attestation section:

```python
def transform_item(data, include_internal=False):
    """Transform a single JSON-LD item from GMN to CIDOC-CRM format."""
    
    # ... earlier transformations ...
    
    # Person attestation and relationship properties
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)  # ← Called here
    item = transform_p11i_3_has_spouse(item)
    
    # ... later transformations ...
```

### Integration Order

The transformation is positioned:

- **After** earliest attestation date (logical pairing)
- **Before** spouse relationships (which also use P11i_participated_in)
- **With** other person-focused properties

This ordering ensures:
- Related properties are processed together
- Event arrays are built incrementally
- No conflicts with other transformations

### Dependencies

Required imports:

```python
from uuid import uuid4
import json
```

Required context in JSON-LD:

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  }
}
```

---

## Testing Procedures

### Unit Testing

#### Test 1: Single Date Transformation

**Input:**
```json
{
  "@id": "person:p001",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_2_latest_attestation_date": "1595-08-20"
}
```

**Expected Output:**
```json
{
  "@id": "person:p001",
  "@type": "cidoc:E21_Person",
  "cidoc:P11i_participated_in": [
    {
      "@id": "person:p001/event/latest_12345678",
      "@type": "cidoc:E5_Event",
      "cidoc:P4_has_time-span": {
        "@id": "person:p001/event/latest_12345678/timespan",
        "@type": "cidoc:E52_Time-Span",
        "cidoc:P82b_end_of_the_end": "1595-08-20"
      }
    }
  ]
}
```

**Test Code:**
```python
def test_single_date():
    input_data = {
        "@id": "person:p001",
        "@type": "cidoc:E21_Person",
        "gmn:P11i_2_latest_attestation_date": ["1595-08-20"]
    }
    result = transform_p11i_2_latest_attestation_date(input_data)
    
    assert "gmn:P11i_2_latest_attestation_date" not in result
    assert "cidoc:P11i_participated_in" in result
    assert len(result["cidoc:P11i_participated_in"]) == 1
    
    event = result["cidoc:P11i_participated_in"][0]
    assert event["@type"] == "cidoc:E5_Event"
    assert "cidoc:P4_has_time-span" in event
    
    timespan = event["cidoc:P4_has_time-span"]
    assert timespan["@type"] == "cidoc:E52_Time-Span"
    assert timespan["cidoc:P82b_end_of_the_end"] == "1595-08-20"
    
    print("✓ Single date test passed")
```

#### Test 2: Multiple Dates

**Input:**
```json
{
  "@id": "person:p002",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_2_latest_attestation_date": ["1590-03-15", "1595-08-20"]
}
```

**Expected Behavior:**
- Both dates create separate events
- Each event has unique URI (different hash)
- Both events added to P11i_participated_in array

**Test Code:**
```python
def test_multiple_dates():
    input_data = {
        "@id": "person:p002",
        "@type": "cidoc:E21_Person",
        "gmn:P11i_2_latest_attestation_date": ["1590-03-15", "1595-08-20"]
    }
    result = transform_p11i_2_latest_attestation_date(input_data)
    
    assert len(result["cidoc:P11i_participated_in"]) == 2
    
    # Check that URIs are different
    uri1 = result["cidoc:P11i_participated_in"][0]["@id"]
    uri2 = result["cidoc:P11i_participated_in"][1]["@id"]
    assert uri1 != uri2
    
    print("✓ Multiple dates test passed")
```

#### Test 3: JSON-LD Date Object

**Input:**
```json
{
  "@id": "person:p003",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_2_latest_attestation_date": [
    {
      "@value": "1595-08-20",
      "@type": "xsd:date"
    }
  ]
}
```

**Test Code:**
```python
def test_jsonld_date_object():
    input_data = {
        "@id": "person:p003",
        "@type": "cidoc:E21_Person",
        "gmn:P11i_2_latest_attestation_date": [
            {"@value": "1595-08-20", "@type": "xsd:date"}
        ]
    }
    result = transform_p11i_2_latest_attestation_date(input_data)
    
    timespan = result["cidoc:P11i_participated_in"][0]["cidoc:P4_has_time-span"]
    assert timespan["cidoc:P82b_end_of_the_end"] == "1595-08-20"
    
    print("✓ JSON-LD date object test passed")
```

#### Test 4: Missing Property

**Input:**
```json
{
  "@id": "person:p004",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Test Person"
}
```

**Expected Behavior:**
- Function returns data unchanged
- No error raised
- No P11i_participated_in array created

**Test Code:**
```python
def test_missing_property():
    input_data = {
        "@id": "person:p004",
        "@type": "cidoc:E21_Person",
        "gmn:P1_1_has_name": "Test Person"
    }
    result = transform_p11i_2_latest_attestation_date(input_data)
    
    assert "cidoc:P11i_participated_in" not in result
    assert result == input_data  # Unchanged
    
    print("✓ Missing property test passed")
```

#### Test 5: Empty Date Value

**Input:**
```json
{
  "@id": "person:p005",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_2_latest_attestation_date": [""]
}
```

**Expected Behavior:**
- Empty date is skipped
- No event created
- Property is removed from output

**Test Code:**
```python
def test_empty_date():
    input_data = {
        "@id": "person:p005",
        "@type": "cidoc:E21_Person",
        "gmn:P11i_2_latest_attestation_date": [""]
    }
    result = transform_p11i_2_latest_attestation_date(input_data)
    
    assert "gmn:P11i_2_latest_attestation_date" not in result
    # P11i_participated_in array created but empty
    assert len(result.get("cidoc:P11i_participated_in", [])) == 0
    
    print("✓ Empty date test passed")
```

#### Test 6: Coexistence with Earliest Attestation

**Input:**
```json
{
  "@id": "person:p006",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_1_earliest_attestation_date": ["1580-01-10"],
  "gmn:P11i_2_latest_attestation_date": ["1595-08-20"]
}
```

**Expected Behavior:**
- Both properties create events
- Events have different URIs (earliest_xxx vs latest_xxx)
- Both events in same P11i_participated_in array

**Test Code:**
```python
def test_coexistence_with_earliest():
    input_data = {
        "@id": "person:p006",
        "@type": "cidoc:E21_Person",
        "gmn:P11i_1_earliest_attestation_date": ["1580-01-10"],
        "gmn:P11i_2_latest_attestation_date": ["1595-08-20"]
    }
    # Transform both properties
    result = transform_p11i_1_earliest_attestation_date(input_data)
    result = transform_p11i_2_latest_attestation_date(result)
    
    assert len(result["cidoc:P11i_participated_in"]) == 2
    
    # Check that one uses P82a and one uses P82b
    timespans = [e["cidoc:P4_has_time-span"] for e in result["cidoc:P11i_participated_in"]]
    has_earliest = any("cidoc:P82a_begin_of_the_begin" in ts for ts in timespans)
    has_latest = any("cidoc:P82b_end_of_the_end" in ts for ts in timespans)
    
    assert has_earliest and has_latest
    
    print("✓ Coexistence test passed")
```

### Integration Testing

#### Test 7: Full Person Record Transformation

**Input:** Complete person record with multiple properties

```json
{
  "@id": "person:lorenzo_giustiniani",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Lorenzo Giustiniani",
  "gmn:P11i_1_earliest_attestation_date": ["1580-01-10"],
  "gmn:P11i_2_latest_attestation_date": ["1595-08-20"],
  "gmn:P11i_3_has_spouse": [{"@id": "person:maria_corner"}]
}
```

**Test Procedure:**

1. Run full transformation: `transform_item(input_data)`
2. Verify all simplified properties are removed
3. Verify P11i_participated_in contains 3 events (earliest, latest, marriage)
4. Check event types and structures are correct
5. Validate no data loss

#### Test 8: Round-Trip Test

**Procedure:**

1. Start with GMN simplified data
2. Transform to CIDOC-CRM
3. Query the CIDOC-CRM output for latest attestation info
4. Verify you can extract the same date value

**SPARQL Query for Verification:**

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?latestDate WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P11i_participated_in ?event .
  ?event cidoc:P4_has_time-span ?timespan .
  ?timespan cidoc:P82b_end_of_the_end ?latestDate .
}
```

### Performance Testing

#### Test 9: Bulk Transformation

**Test Scenario:** Transform 1000 person records with latest attestation dates

```python
def test_bulk_transformation():
    import time
    
    # Generate 1000 test records
    test_data = []
    for i in range(1000):
        test_data.append({
            "@id": f"person:p{i:04d}",
            "@type": "cidoc:E21_Person",
            "gmn:P11i_2_latest_attestation_date": [f"159{i%10}-0{(i%9)+1}-{(i%28)+1:02d}"]
        })
    
    start_time = time.time()
    
    results = [transform_p11i_2_latest_attestation_date(item) for item in test_data]
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"✓ Bulk transformation: {len(results)} records in {elapsed:.3f}s")
    print(f"  Average: {elapsed/len(results)*1000:.2f}ms per record")
    
    # Performance threshold: should complete in < 1 second
    assert elapsed < 1.0
```

### Validation Testing

#### Test 10: TTL Output Validation

**Procedure:**

1. Transform sample data
2. Serialize to TTL format
3. Validate using `rapper` or similar tool
4. Verify compliance with CIDOC-CRM schema

```bash
# After generating output.ttl
rapper -i turtle -o ntriples output.ttl > /dev/null

# If rapper succeeds with no errors, TTL is valid
echo "✓ TTL validation passed"
```

---

## Usage Examples

### Example 1: Basic Person with Latest Attestation

**Use Case:** A person whose last appearance in records was a specific date

**Input Data (GMN):**

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "person:francesco_corner",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Francesco Corner",
      "gmn:P11i_2_latest_attestation_date": "1592-06-15"
    }
  ]
}
```

**Command:**

```bash
python gmn_to_cidoc_transform.py input.json output.json
```

**Output Data (CIDOC-CRM):**

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "person:francesco_corner",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": {
        "@id": "person:francesco_corner/appellation",
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Francesco Corner"
      },
      "cidoc:P11i_participated_in": [
        {
          "@id": "person:francesco_corner/event/latest_45678901",
          "@type": "cidoc:E5_Event",
          "cidoc:P4_has_time-span": {
            "@id": "person:francesco_corner/event/latest_45678901/timespan",
            "@type": "cidoc:E52_Time-Span",
            "cidoc:P82b_end_of_the_end": "1592-06-15"
          }
        }
      ]
    }
  ]
}
```

### Example 2: Person with Both Attestation Dates

**Use Case:** Bracketing a person's documented lifespan

**Input Data (GMN):**

```json
{
  "@id": "person:maria_venier",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Maria Venier",
  "gmn:P11i_1_earliest_attestation_date": "1575-03-12",
  "gmn:P11i_2_latest_attestation_date": "1598-11-20"
}
```

**Output (CIDOC-CRM):**

```json
{
  "@id": "person:maria_venier",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": {...},
  "cidoc:P11i_participated_in": [
    {
      "@id": "person:maria_venier/event/earliest_12345678",
      "@type": "cidoc:E5_Event",
      "cidoc:P4_has_time-span": {
        "@id": "person:maria_venier/event/earliest_12345678/timespan",
        "@type": "cidoc:E52_Time-Span",
        "cidoc:P82a_begin_of_the_begin": "1575-03-12"
      }
    },
    {
      "@id": "person:maria_venier/event/latest_87654321",
      "@type": "cidoc:E5_Event",
      "cidoc:P4_has_time-span": {
        "@id": "person:maria_venier/event/latest_87654321/timespan",
        "@type": "cidoc:E52_Time-Span",
        "cidoc:P82b_end_of_the_end": "1598-11-20"
      }
    }
  ]
}
```

**SPARQL Query to Retrieve Lifespan:**

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?name ?earliest ?latest WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by ?app ;
          cidoc:P11i_participated_in ?event1, ?event2 .
  
  ?app cidoc:P190_has_symbolic_content ?name .
  
  ?event1 cidoc:P4_has_time-span ?ts1 .
  ?ts1 cidoc:P82a_begin_of_the_begin ?earliest .
  
  ?event2 cidoc:P4_has_time-span ?ts2 .
  ?ts2 cidoc:P82b_end_of_the_end ?latest .
}
```

### Example 3: Multiple Latest Attestations

**Use Case:** Person appears in records multiple times in final year of documentation

**Input (GMN):**

```json
{
  "@id": "person:lorenzo_giustiniani",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Lorenzo Giustiniani",
  "gmn:P11i_2_latest_attestation_date": [
    "1595-06-10",
    "1595-08-20",
    "1595-12-15"
  ]
}
```

**Output (CIDOC-CRM):**

Creates three separate E5_Event instances, each with its own timespan and date.

**Use Case Justification:**

- Multiple attestations might indicate different documents or events
- Preserves fine-grained temporal information
- Allows researchers to see patterns in documentation
- Each event is independently queryable and citable

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Property Not Being Transformed

**Symptoms:**
- GMN property appears in output
- No P11i_participated_in events created

**Possible Causes:**
1. Function not called in transformation pipeline
2. Property name typo in data
3. Data structure unexpected

**Solutions:**

```python
# Check 1: Verify function is called
def transform_item(data, include_internal=False):
    # ... 
    item = transform_p11i_2_latest_attestation_date(item)  # Must be present
    # ...

# Check 2: Verify property name in data
print(data.keys())  # Should include 'gmn:P11i_2_latest_attestation_date'

# Check 3: Verify data structure
print(type(data['gmn:P11i_2_latest_attestation_date']))  # Should be list
```

#### Issue 2: Invalid Date Format

**Symptoms:**
- Dates not formatted correctly in output
- Validation errors when querying

**Solution:**

Ensure dates are in ISO 8601 format: `YYYY-MM-DD`

```python
# Valid formats
"1595-08-20"           # Full date
"1595-08"              # Year-month
"1595"                 # Year only

# Invalid formats
"20/08/1595"           # Wrong delimiter
"Aug 20, 1595"         # Text format
"1595/08/20"           # Wrong order
```

#### Issue 3: URI Collisions

**Symptoms:**
- Same URI generated for different events
- Data overwritten

**Solution:**

The hash function prevents collisions by:
- Including the date value in the hash input
- Including 'latest' string (vs 'earliest')
- Using last 8 characters of hash

If collisions persist:

```python
# Increase hash length
event_hash = str(hash(date_value + 'latest'))[-12:]  # Use 12 chars instead of 8
```

#### Issue 4: Empty P11i_participated_in Array

**Symptoms:**
- Property transformed but array is empty
- No events created

**Possible Causes:**
- All date values were empty strings
- Date objects missing '@value' key

**Debug Code:**

```python
def transform_p11i_2_latest_attestation_date_debug(data):
    if 'gmn:P11i_2_latest_attestation_date' not in data:
        print("DEBUG: Property not present")
        return data
    
    dates = data['gmn:P11i_2_latest_attestation_date']
    print(f"DEBUG: Found {len(dates)} date values")
    
    for i, date_obj in enumerate(dates):
        print(f"DEBUG: Date {i}: {date_obj} (type: {type(date_obj)})")
        
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
            print(f"DEBUG: Extracted value: '{date_value}'")
        else:
            date_value = str(date_obj)
        
        if not date_value:
            print(f"DEBUG: Date {i} is empty, skipping")
            continue
    
    # ... rest of function ...
```

#### Issue 5: JSON-LD Context Missing

**Symptoms:**
- Properties not recognized
- Transformation skipped

**Solution:**

Ensure proper JSON-LD context:

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [...]
}
```

---

## Maintenance Notes

### When to Update This Implementation

Update the transformation function if:

1. **CIDOC-CRM Updates**: New version changes E5_Event or time-span modeling
2. **Performance Issues**: Need to optimize for large datasets
3. **New Requirements**: Additional metadata needs to be captured
4. **Bug Fixes**: Discovered edge cases or errors

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-16 | Initial implementation |

### Related Documentation

- See `has-earliest-attestation-date-documentation.md` for the companion property
- See CIDOC-CRM specification for E5_Event and E52_Time-Span
- See `gmn-ontology-documentation.md` for overall ontology structure

---

## Summary

This implementation guide has covered:

- ✅ Current implementation status (fully implemented)
- ✅ Ontology definition details
- ✅ Python transformation function breakdown
- ✅ Integration points in the pipeline
- ✅ Comprehensive testing procedures
- ✅ Usage examples and SPARQL queries
- ✅ Troubleshooting common issues

**Next Steps:**

1. Run the test suite to verify implementation
2. Review usage examples for your specific use case
3. Consult the Ontology Documentation for semantic details
4. Check the Document Additions file for examples to include in project docs

---

**For additional support:** Refer to the other files in this deliverables package or consult the CIDOC-CRM specification.
