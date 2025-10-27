# GMN Ontology P22.1 Has Owner Property
## Implementation Guide

This guide provides step-by-step instructions for implementing the `gmn:P22_1_has_owner` property in the GMN ontology and transformation pipeline.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Ontology Implementation](#phase-1-ontology-implementation)
4. [Phase 2: Transformation Script Implementation](#phase-2-transformation-script-implementation)
5. [Phase 3: Testing](#phase-3-testing)
6. [Phase 4: Documentation](#phase-4-documentation)
7. [Troubleshooting](#troubleshooting)

---

## Overview

### What You'll Implement

The `gmn:P22_1_has_owner` property allows simplified expression of ownership relationships, which are then transformed to full CIDOC-CRM compliant structures during export.

**Shortcut Property**:
```turtle
<building001> gmn:P22_1_has_owner <person_giovanni> .
```

**Transforms To**:
```turtle
<building001> cidoc:P24i_changed_ownership_through <building001/acquisition/ownership_a1b2c3d4> .

<building001/acquisition/ownership_a1b2c3d4> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to <person_giovanni> .
```

### Implementation Time

- Ontology changes: ~5 minutes
- Transformation code: ~10 minutes
- Testing: ~15 minutes
- Documentation: ~10 minutes
- **Total**: ~40 minutes

---

## Prerequisites

### Required Files

1. `gmn_ontology.ttl` - Main ontology file
2. `gmn_to_cidoc_transform.py` - Transformation script
3. Documentation file (markdown or text)

### Required Tools

- Text editor or IDE
- Python 3.7+
- RDF validator (optional but recommended)
- JSON-LD test files

### Knowledge Requirements

- Basic understanding of RDF/Turtle syntax
- Basic Python programming
- Understanding of CIDOC-CRM acquisition events
- Familiarity with the GMN ontology structure

---

## Phase 1: Ontology Implementation

### Step 1.1: Locate the Property Section

Open `gmn_ontology.ttl` and find the simplified properties section. Look for similar properties like `gmn:P53_1_has_occupant` or other P-numbered properties.

### Step 1.2: Add Property Definition

Add the following TTL code to your ontology file:

```turtle
# Property: P22.1 has owner
gmn:P22_1_has_owner
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P22.1 has owner"@en ;
    rdfs:comment "Simplified property for expressing ownership of a building or moveable property by a person. Represents the full CIDOC-CRM path: E22_Human-Made_Object > P24i_changed_ownership_through > E8_Acquisition > P22_transferred_title_to > E21_Person. This property captures ownership relationships through acquisition events. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Applies to both buildings (E22.1) and moveable property (E22.2)."@en ;
    rdfs:subPropertyOf cidoc:P24i_changed_ownership_through ;
    rdfs:domain cidoc:E22_Human-Made_Object ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P24i_changed_ownership_through, cidoc:P22_transferred_title_to .
```

### Step 1.3: Verify Property Components

Check that each component is correct:

| Component | Value | Purpose |
|-----------|-------|---------|
| **IRI** | `gmn:P22_1_has_owner` | Unique identifier |
| **Type** | `owl:ObjectProperty` | Links objects to objects |
| **Label** | "P22.1 has owner"@en | Human-readable name |
| **Subproperty** | `cidoc:P24i_changed_ownership_through` | CIDOC-CRM alignment |
| **Domain** | `cidoc:E22_Human-Made_Object` | Source: buildings/property |
| **Range** | `cidoc:E21_Person` | Target: person owners |
| **Comment** | Full documentation | Explains purpose and usage |

### Step 1.4: Validate Ontology

If using a validator:

```bash
# Using rapper (if installed)
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Or open in Protégé and check for errors
```

Look for:
- ✅ No syntax errors
- ✅ Property appears in class hierarchy
- ✅ Domain and range are correctly set
- ✅ Subproperty relationship is valid

---

## Phase 2: Transformation Script Implementation

### Step 2.1: Locate Transform Functions

Open `gmn_to_cidoc_transform.py` and find the transformation functions section. Look for similar functions like `transform_p53_1_has_occupant()`.

### Step 2.2: Add the Transform Function

Add this function after the other property transformation functions (around line 1983 in the current script):

```python
def transform_p22_1_has_owner(data):
    """
    Transform gmn:P22_1_has_owner to full CIDOC-CRM structure:
    P24i_changed_ownership_through > E8_Acquisition > P22_transferred_title_to > E21_Person
    """
    if 'gmn:P22_1_has_owner' not in data:
        return data
    
    owners = data['gmn:P22_1_has_owner']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P24i_changed_ownership_through' not in data:
        data['cidoc:P24i_changed_ownership_through'] = []
    
    for owner_obj in owners:
        if isinstance(owner_obj, dict):
            owner_uri = owner_obj.get('@id', '')
            owner_data = owner_obj.copy()
        else:
            owner_uri = str(owner_obj)
            owner_data = {
                '@id': owner_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition_hash = str(hash(owner_uri + 'ownership'))[-8:]
        acquisition_uri = f"{subject_uri}/acquisition/ownership_{acquisition_hash}"
        
        acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition',
            'cidoc:P22_transferred_title_to': [owner_data]
        }
        
        data['cidoc:P24i_changed_ownership_through'].append(acquisition)
    
    del data['gmn:P22_1_has_owner']
    return data
```

### Step 2.3: Add to Transform Pipeline

Find the `transform_item()` function and add the function call in the appropriate location. It should be called after other property transformations but before editorial notes:

```python
def transform_item(item, include_internal=False):
    """Transform a single item."""
    
    # ... existing transformations ...
    
    # Person attestation and relationship properties
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)
    item = transform_p11i_3_has_spouse(item)
    
    # Property ownership and occupation
    item = transform_p22_1_has_owner(item)  # ← ADD THIS LINE
    item = transform_p53_1_has_occupant(item)
    
    # ... rest of transformations ...
    
    return item
```

### Step 2.4: Code Walkthrough

Let's understand what each part does:

#### Part 1: Check for Property
```python
if 'gmn:P22_1_has_owner' not in data:
    return data
```
- Returns unchanged data if property not present
- Efficient: no processing if not needed

#### Part 2: Get Owners and Subject
```python
owners = data['gmn:P22_1_has_owner']
subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
```
- Extracts the list of owners
- Gets or creates URI for the subject (building/property)

#### Part 3: Initialize Acquisition Array
```python
if 'cidoc:P24i_changed_ownership_through' not in data:
    data['cidoc:P24i_changed_ownership_through'] = []
```
- Creates array for acquisitions if it doesn't exist
- Allows multiple ownership events

#### Part 4: Process Each Owner
```python
for owner_obj in owners:
    if isinstance(owner_obj, dict):
        owner_uri = owner_obj.get('@id', '')
        owner_data = owner_obj.copy()
    else:
        owner_uri = str(owner_obj)
        owner_data = {
            '@id': owner_uri,
            '@type': 'cidoc:E21_Person'
        }
```
- Handles both dictionary objects and simple URI strings
- Ensures owner data has correct type

#### Part 5: Generate Unique Acquisition URI
```python
acquisition_hash = str(hash(owner_uri + 'ownership'))[-8:]
acquisition_uri = f"{subject_uri}/acquisition/ownership_{acquisition_hash}"
```
- Creates unique hash for each owner-property pair
- Ensures consistent URIs across transformations
- Format: `<object_uri>/acquisition/ownership_<hash>`

#### Part 6: Create Acquisition Event
```python
acquisition = {
    '@id': acquisition_uri,
    '@type': 'cidoc:E8_Acquisition',
    'cidoc:P22_transferred_title_to': [owner_data]
}

data['cidoc:P24i_changed_ownership_through'].append(acquisition)
```
- Creates CIDOC-CRM compliant acquisition event
- Links acquisition to owner via P22

#### Part 7: Clean Up
```python
del data['gmn:P22_1_has_owner']
return data
```
- Removes shortcut property
- Returns transformed data

---

## Phase 3: Testing

### Step 3.1: Create Test Data Files

Create test files for different scenarios:

#### Test 1: Single Owner (Building)
**File**: `test_single_owner_building.json`

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/building001",
  "@type": "gmn:E22_1_Building",
  "gmn:P22_1_has_owner": [
    {
      "@id": "http://example.org/person/giovanni",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

#### Test 2: Multiple Owners (Building)
**File**: `test_multiple_owners.json`

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/building002",
  "@type": "gmn:E22_1_Building",
  "gmn:P22_1_has_owner": [
    {
      "@id": "http://example.org/person/giovanni",
      "@type": "cidoc:E21_Person"
    },
    {
      "@id": "http://example.org/person/francesco",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

#### Test 3: Moveable Property Owner
**File**: `test_moveable_property.json`

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/property001",
  "@type": "gmn:E22_2_Moveable_Property",
  "gmn:P22_1_has_owner": [
    "http://example.org/person/maria"
  ]
}
```

### Step 3.2: Run Transformations

```bash
# Test single owner
python gmn_to_cidoc_transform.py test_single_owner_building.json output1.json

# Test multiple owners
python gmn_to_cidoc_transform.py test_multiple_owners.json output2.json

# Test moveable property
python gmn_to_cidoc_transform.py test_moveable_property.json output3.json
```

### Step 3.3: Verify Expected Outputs

#### Expected Output 1: Single Owner
```json
{
  "@context": {...},
  "@id": "http://example.org/building001",
  "@type": "gmn:E22_1_Building",
  "cidoc:P24i_changed_ownership_through": [
    {
      "@id": "http://example.org/building001/acquisition/ownership_a1b2c3d4",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "http://example.org/person/giovanni",
          "@type": "cidoc:E21_Person"
        }
      ]
    }
  ]
}
```

#### Expected Output 2: Multiple Owners
```json
{
  "@id": "http://example.org/building002",
  "@type": "gmn:E22_1_Building",
  "cidoc:P24i_changed_ownership_through": [
    {
      "@id": "http://example.org/building002/acquisition/ownership_hash1",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "http://example.org/person/giovanni",
          "@type": "cidoc:E21_Person"
        }
      ]
    },
    {
      "@id": "http://example.org/building002/acquisition/ownership_hash2",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "http://example.org/person/francesco",
          "@type": "cidoc:E21_Person"
        }
      ]
    }
  ]
}
```

### Step 3.4: Validation Checklist

For each test output, verify:

- [ ] ✅ `gmn:P22_1_has_owner` property is removed
- [ ] ✅ `cidoc:P24i_changed_ownership_through` property is present
- [ ] ✅ E8_Acquisition events are created
- [ ] ✅ Each acquisition has `@type: cidoc:E8_Acquisition`
- [ ] ✅ Each acquisition has unique URI with hash
- [ ] ✅ `cidoc:P22_transferred_title_to` links to owners
- [ ] ✅ Owner objects have `@type: cidoc:E21_Person`
- [ ] ✅ Multiple owners each get separate acquisitions
- [ ] ✅ No duplicate acquisitions
- [ ] ✅ JSON structure is valid

### Step 3.5: Edge Case Testing

Test these scenarios:

#### No Owners
```json
{
  "@id": "http://example.org/building003",
  "@type": "gmn:E22_1_Building"
}
```
**Expected**: No transformation occurs, data unchanged

#### Owner as String URI
```json
{
  "@id": "http://example.org/building004",
  "@type": "gmn:E22_1_Building",
  "gmn:P22_1_has_owner": ["http://example.org/person/antonio"]
}
```
**Expected**: URI is wrapped in proper object structure

#### Owner with Additional Properties
```json
{
  "@id": "http://example.org/building005",
  "@type": "gmn:E22_1_Building",
  "gmn:P22_1_has_owner": [
    {
      "@id": "http://example.org/person/lucia",
      "@type": "cidoc:E21_Person",
      "gmn:P1_2_has_name_from_source": "Lucia Spinola"
    }
  ]
}
```
**Expected**: Additional properties preserved in owner object

---

## Phase 4: Documentation

### Step 4.1: Update Property Reference

Add to your property reference table:

| Property | Label | Domain | Range | Transforms To |
|----------|-------|--------|-------|---------------|
| `gmn:P22_1_has_owner` | "P22.1 has owner" | E22_Human-Made_Object | E21_Person | P24i > E8_Acquisition > P22 |

### Step 4.2: Add Usage Section

Add a section to your documentation:

```markdown
## P22.1 Has Owner

### Purpose
Express ownership of buildings or moveable property by persons.

### Usage
```turtle
<building001> a gmn:E22_1_Building ;
    gmn:P22_1_has_owner <person_giovanni> , <person_francesco> .
```

### Transformation
Creates separate E8_Acquisition events for each owner:
```turtle
<building001> cidoc:P24i_changed_ownership_through 
    <building001/acquisition/ownership_a1b2c3d4> ,
    <building001/acquisition/ownership_e5f6g7h8> .
```

### Step 4.3: Document Related Properties

Note relationships with:
- P53.1 Has Occupant (for residence vs. ownership)
- P70.1 Documents Seller (for sales transactions)
- P70.2 Documents Buyer (for sales transactions)
- P70.3 Documents Transfer Of (for property transfers)

---

## Troubleshooting

### Issue 1: Property Not Transforming

**Symptom**: `gmn:P22_1_has_owner` still in output

**Possible Causes**:
1. Function not called in `transform_item()`
2. Function name misspelled
3. Property key mismatch

**Solution**:
```python
# Check function is called
item = transform_p22_1_has_owner(item)

# Check property key exactly matches
if 'gmn:P22_1_has_owner' not in data:  # Must match exactly
```

### Issue 2: No Acquisition Created

**Symptom**: No `cidoc:P24i_changed_ownership_through` in output

**Possible Causes**:
1. Empty owners list
2. Exception in processing
3. Logic error in function

**Debug**:
```python
# Add debug prints
owners = data['gmn:P22_1_has_owner']
print(f"Processing {len(owners)} owners")

for owner_obj in owners:
    print(f"Owner: {owner_obj}")
```

### Issue 3: Duplicate Acquisitions

**Symptom**: Same acquisition appears multiple times

**Possible Causes**:
1. Function called multiple times
2. Hash collision
3. Data duplication

**Solution**:
- Verify function called only once in pipeline
- Check that hash generation is deterministic
- Examine input data for duplicates

### Issue 4: Invalid JSON Output

**Symptom**: JSON parsing errors

**Possible Causes**:
1. Unclosed brackets
2. Missing commas
3. Invalid structure

**Solution**:
```bash
# Validate JSON
python -m json.tool output.json

# Or use jq
jq . output.json
```

### Issue 5: Owner Type Missing

**Symptom**: Owner objects lack `@type`

**Possible Causes**:
1. Type not set in string URI conversion
2. Existing type overwritten

**Solution**:
```python
# Ensure type is set
if '@type' not in owner_data:
    owner_data['@type'] = 'cidoc:E21_Person'
```

### Issue 6: URI Hash Collisions

**Symptom**: Two different owners get same acquisition URI

**Possible Causes**:
1. Weak hash function
2. Same owner listed twice
3. Hash truncation too aggressive

**Solution**:
```python
# Use longer hash
acquisition_hash = str(hash(owner_uri + 'ownership'))[-12:]  # 12 chars instead of 8
```

---

## Verification Checklist

Before considering implementation complete:

### Ontology
- [ ] Property added to `gmn_ontology.ttl`
- [ ] No syntax errors in TTL file
- [ ] Property appears in RDF validators
- [ ] All metadata complete (label, comment, domain, range)
- [ ] Subproperty relationship correct

### Transformation
- [ ] Function added to `gmn_to_cidoc_transform.py`
- [ ] Function called in `transform_item()` pipeline
- [ ] No Python syntax errors
- [ ] Import statements correct (uuid4)
- [ ] Function handles all data types (dict, string)

### Testing
- [ ] Single owner test passes
- [ ] Multiple owners test passes
- [ ] Moveable property test passes
- [ ] Edge cases handled
- [ ] No errors in output
- [ ] URIs are unique and valid

### Documentation
- [ ] Property documented in main docs
- [ ] Examples provided
- [ ] Transformation explained
- [ ] Related properties noted
- [ ] Usage guidelines clear

---

## Next Steps

After successful implementation:

1. **Integration**: Test with real project data
2. **Performance**: Monitor transformation speed with large datasets
3. **Enhancement**: Consider adding optional time-spans to acquisitions
4. **Training**: Document for other team members
5. **Maintenance**: Plan for future updates or refinements

---

## Additional Resources

- **CIDOC-CRM P24i Property**: http://www.cidoc-crm.org/Property/P24i-changed-ownership-through
- **CIDOC-CRM E8 Class**: http://www.cidoc-crm.org/Entity/E8-Acquisition
- **CIDOC-CRM P22 Property**: http://www.cidoc-crm.org/Property/P22-transferred-title-to

---

**Implementation Guide Version**: 1.0  
**Last Updated**: October 2025  
**Property**: gmn:P22_1_has_owner
