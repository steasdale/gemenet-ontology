# Has Spouse Property - Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the `gmn:P11i_3_has_spouse` property in your GMN ontology and transformation pipeline.

**Estimated implementation time**: 25 minutes

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Update Ontology File](#step-1-update-ontology-file)
3. [Step 2: Add Transformation Function](#step-2-add-transformation-function)
4. [Step 3: Register in Pipeline](#step-3-register-in-pipeline)
5. [Step 4: Testing](#step-4-testing)
6. [Troubleshooting](#troubleshooting)
7. [Validation](#validation)

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script

### Required Knowledge
- Basic understanding of RDF/Turtle syntax
- Familiarity with Python
- Understanding of CIDOC-CRM event modeling
- JSON-LD format knowledge

### Tools
- Text editor with Turtle syntax support (recommended)
- Python 3.7+ with `uuid` module
- JSON validation tool (optional)

---

## Step 1: Update Ontology File

### Location
Open `gmn_ontology.ttl` and locate the section with other P11i properties (approximately lines 300-400).

### Action
Insert the following TTL definition:

```turtle
# Property: P11i.3 has spouse
gmn:P11i_3_has_spouse
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P11i.3 has spouse"@en ;
    rdfs:comment "Simplified property for expressing a spousal relationship between two persons. Represents the full CIDOC-CRM path: E21_Person > P11i_participated_in > E5_Event > P2_has_type <http://vocab.getty.edu/aat/300055475> > P11_had_participant > E21_Person. This property captures marriage relationships through a marriage event. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The event type is automatically set to AAT 300055475 (marriages)."@en ;
    rdfs:subPropertyOf cidoc:P11i_participated_in ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P11i_participated_in, cidoc:P11_had_participant, aat:300055475 ;
    gmn:hasImplicitType aat:300055475 .
```

### Placement Tips
- Insert after `gmn:P11i_2_latest_attestation_date`
- Insert before `gmn:P22_1_has_owner`
- Maintain consistent indentation (4 spaces)
- Ensure blank line before and after the definition

### Validation
After adding, validate the Turtle syntax:
```bash
rapper -i turtle gmn_ontology.ttl > /dev/null
```

---

## Step 2: Add Transformation Function

### Location
Open `gmn_to_cidoc_transform.py` and locate the section with other transformation functions (around line 200-500).

### Action
Insert the following function after `transform_p11i_2_latest_attestation_date()`:

```python
def transform_p11i_3_has_spouse(data):
    """
    Transform gmn:P11i_3_has_spouse to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event (marriage) > P11_had_participant > E21_Person
    """
    if 'gmn:P11i_3_has_spouse' not in data:
        return data
    
    spouses = data['gmn:P11i_3_has_spouse']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    for spouse_obj in spouses:
        if isinstance(spouse_obj, dict):
            spouse_uri = spouse_obj.get('@id', '')
            spouse_data = spouse_obj.copy()
        else:
            spouse_uri = str(spouse_obj)
            spouse_data = {
                '@id': spouse_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        event_hash = str(hash(spouse_uri + 'marriage'))[-8:]
        event_uri = f"{subject_uri}/event/marriage_{event_hash}"
        
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P2_has_type': {
                '@id': AAT_MARRIAGE,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P11_had_participant': [spouse_data]
        }
        
        data['cidoc:P11i_participated_in'].append(event)
    
    del data['gmn:P11i_3_has_spouse']
    return data
```

### Required Constants
Ensure the following constant is defined at the top of the file (around line 20-30):

```python
AAT_MARRIAGE = "http://vocab.getty.edu/aat/300055475"
```

### Code Explanation

#### Input Validation
```python
if 'gmn:P11i_3_has_spouse' not in data:
    return data
```
Returns unchanged data if property not present.

#### Subject URI Extraction
```python
subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
```
Gets the person's URI or generates a UUID if missing.

#### Container Initialization
```python
if 'cidoc:P11i_participated_in' not in data:
    data['cidoc:P11i_participated_in'] = []
```
Creates the participation container if it doesn't exist.

#### Spouse Processing Loop
```python
for spouse_obj in spouses:
    if isinstance(spouse_obj, dict):
        spouse_uri = spouse_obj.get('@id', '')
        spouse_data = spouse_obj.copy()
    else:
        spouse_uri = str(spouse_obj)
        spouse_data = {
            '@id': spouse_uri,
            '@type': 'cidoc:E21_Person'
        }
```
Handles both dictionary and string spouse representations.

#### Event URI Generation
```python
event_hash = str(hash(spouse_uri + 'marriage'))[-8:]
event_uri = f"{subject_uri}/event/marriage_{event_hash}"
```
Creates a consistent, unique URI for the marriage event.

#### Event Construction
```python
event = {
    '@id': event_uri,
    '@type': 'cidoc:E5_Event',
    'cidoc:P2_has_type': {
        '@id': AAT_MARRIAGE,
        '@type': 'cidoc:E55_Type'
    },
    'cidoc:P11_had_participant': [spouse_data]
}
```
Builds the complete marriage event structure.

#### Cleanup
```python
del data['gmn:P11i_3_has_spouse']
```
Removes the simplified property after transformation.

---

## Step 3: Register in Pipeline

### Location
Find the `transform_item()` function (around line 700-900).

### Action
Add the function call in the appropriate section:

```python
def transform_item(item, include_internal=False):
    """Transform a single JSON-LD item."""
    
    # ... existing transformations ...
    
    # Person attestation and relationship properties
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)
    item = transform_p11i_3_has_spouse(item)  # <-- ADD THIS LINE
    
    # Property ownership and occupation
    item = transform_p22_1_has_owner(item)
    # ... rest of function ...
```

### Placement
Insert after `transform_p11i_2_latest_attestation_date(item)` and before `transform_p22_1_has_owner(item)`.

---

## Step 4: Testing

### Test Data Preparation

Create a test file `test_has_spouse.json`:

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/",
    "aat": "http://vocab.getty.edu/aat/"
  },
  "@id": "person:alice",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:bob",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

### Run Transformation

```bash
python gmn_to_cidoc_transform.py test_has_spouse.json output_spouse.json
```

### Expected Output

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "aat": "http://vocab.getty.edu/aat/"
  },
  "@id": "person:alice",
  "@type": "cidoc:E21_Person",
  "cidoc:P11i_participated_in": [
    {
      "@id": "person:alice/event/marriage_a1b2c3d4",
      "@type": "cidoc:E5_Event",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300055475",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P11_had_participant": [
        {
          "@id": "person:bob",
          "@type": "cidoc:E21_Person"
        }
      ]
    }
  ]
}
```

### Test Cases

#### Test Case 1: Single Spouse (Dictionary Format)
```json
{
  "@id": "person:001",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {"@id": "person:002", "@type": "cidoc:E21_Person"}
  ]
}
```
**Expected**: Creates one marriage event with proper typing.

#### Test Case 2: Multiple Spouses
```json
{
  "@id": "person:001",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {"@id": "person:002", "@type": "cidoc:E21_Person"},
    {"@id": "person:003", "@type": "cidoc:E21_Person"}
  ]
}
```
**Expected**: Creates two separate marriage events, each properly typed.

#### Test Case 3: String Format (URI only)
```json
{
  "@id": "person:001",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": ["person:002"]
}
```
**Expected**: Creates marriage event and infers E21_Person type for spouse.

#### Test Case 4: Mixed with Other Participations
```json
{
  "@id": "person:001",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_1_earliest_attestation_date": ["1450-01-01"],
  "gmn:P11i_3_has_spouse": [{"@id": "person:002"}]
}
```
**Expected**: Both transformations applied correctly, P11i_participated_in array contains both events.

#### Test Case 5: No Spouse Property
```json
{
  "@id": "person:001",
  "@type": "cidoc:E21_Person"
}
```
**Expected**: No changes, data returned as-is.

---

## Troubleshooting

### Common Issues

#### Issue 1: "NameError: name 'AAT_MARRIAGE' is not defined"

**Cause**: The AAT_MARRIAGE constant is not defined.

**Solution**: Add to top of file:
```python
AAT_MARRIAGE = "http://vocab.getty.edu/aat/300055475"
```

#### Issue 2: "TypeError: unhashable type: 'dict'"

**Cause**: Trying to hash a dictionary object.

**Solution**: Verify you're extracting the URI string before hashing:
```python
spouse_uri = spouse_obj.get('@id', '')  # Extracts string
event_hash = str(hash(spouse_uri + 'marriage'))[-8:]  # Hashes string
```

#### Issue 3: Duplicate Events Created

**Cause**: The same spouse appears multiple times in the input.

**Solution**: This is expected behavior. Each entry creates a separate event. To deduplicate:
```python
# Add before processing
spouses = list({spouse.get('@id') if isinstance(spouse, dict) else spouse: spouse 
                for spouse in spouses}.values())
```

#### Issue 4: Missing @id in Output

**Cause**: Spouse object doesn't have an @id field.

**Solution**: The code handles this by skipping (spouse_uri will be empty string). Add validation:
```python
if not spouse_uri:
    continue  # Skip entries without URI
```

#### Issue 5: Invalid JSON-LD Output

**Cause**: Incorrect structure or missing required fields.

**Solution**: Validate output with JSON-LD processor:
```bash
jsonld format output_spouse.json
```

---

## Validation

### Ontology Validation

```bash
# Validate Turtle syntax
rapper -i turtle gmn_ontology.ttl -o turtle > /dev/null

# Check for property definition
grep -A 10 "P11i_3_has_spouse" gmn_ontology.ttl
```

### Python Code Validation

```bash
# Check Python syntax
python -m py_compile gmn_to_cidoc_transform.py

# Run unit tests (if available)
python -m pytest test_transformations.py -k spouse
```

### Transformation Validation

```bash
# Transform test file
python gmn_to_cidoc_transform.py test_has_spouse.json output.json

# Validate output JSON-LD
jsonld format output.json

# Check for required elements
grep -c "P11i_participated_in" output.json  # Should be > 0
grep -c "300055475" output.json  # Should be > 0
grep -c "E5_Event" output.json  # Should be > 0
```

### Semantic Validation Checklist

- [ ] Marriage events are properly typed with AAT 300055475
- [ ] Spouse person entities have @id and @type
- [ ] Event URIs are unique and consistent
- [ ] P11i_participated_in array is properly structured
- [ ] P11_had_participant contains spouse data
- [ ] Original gmn:P11i_3_has_spouse property is removed

---

## Post-Implementation

### Documentation Update

After successful implementation, update your project documentation to include:

1. Property definition and usage
2. Transformation rules
3. Examples
4. Related properties

See `has-spouse-doc-note.txt` for ready-to-paste documentation text.

### Data Migration

If you have existing data using this property:

```bash
# Backup existing data
cp data.json data.json.backup

# Run transformation
python gmn_to_cidoc_transform.py data.json data_transformed.json

# Validate
python validate_cidoc.py data_transformed.json
```

### Performance Considerations

For large datasets:

- The transformation is O(n) where n = number of spouse entries
- Each spouse creates one marriage event
- URI hashing is fast and consistent
- Consider batch processing for >10,000 entries

---

## Next Steps

1. ✅ Implement related properties:
   - `gmn:P96_1_has_mother`
   - `gmn:P97_1_has_father`

2. ✅ Add inverse relationship handling (optional):
   - Consider bidirectional spouse relationships
   - Implement consistency checks

3. ✅ Enhance with additional attributes (optional):
   - Marriage date (via E52_Time-Span)
   - Marriage place (via E53_Place)
   - Marriage type qualifiers

4. ✅ Integration testing:
   - Test with full dataset
   - Verify compatibility with other transformations
   - Performance benchmarking

---

## Support and Resources

### Documentation
- Main GMN documentation
- CIDOC-CRM specification: http://www.cidoc-crm.org/
- AAT marriage concept: http://vocab.getty.edu/aat/300055475

### Code Examples
- See `has-spouse-transform.py` for complete function
- See `has-spouse-documentation.md` for semantic details

### Questions?
- Review this guide's troubleshooting section
- Check the main README for common issues
- Consult CIDOC-CRM documentation for semantic questions

---

**Implementation Guide Version**: 1.0  
**Last Updated**: 2025-10-27  
**Property**: gmn:P11i_3_has_spouse
