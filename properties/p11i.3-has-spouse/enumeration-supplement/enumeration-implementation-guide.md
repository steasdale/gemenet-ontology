# Marriage Enumeration - Implementation Guide (Option 2)

## Overview

This guide provides step-by-step instructions for adding marriage enumeration support using the E13_Attribute_Assignment approach to your GMN ontology.

**Prerequisites**: Base has-spouse package must be implemented first.

**Estimated time**: 30 minutes

---

## Table of Contents

1. [Prerequisites Check](#prerequisites-check)
2. [Step 1: Add New Properties to Ontology](#step-1-add-new-properties-to-ontology)
3. [Step 2: Replace Transformation Function](#step-2-replace-transformation-function)
4. [Step 3: Testing](#step-3-testing)
5. [Step 4: Update Documentation](#step-4-update-documentation)
6. [Troubleshooting](#troubleshooting)
7. [Validation](#validation)

---

## Prerequisites Check

Before beginning, verify:

- [ ] Base `gmn:P11i_3_has_spouse` property is defined in ontology
- [ ] Base transformation function exists in `gmn_to_cidoc_transform.py`
- [ ] Python environment has `uuid` module
- [ ] Understanding of E13_Attribute_Assignment class
- [ ] Backup of current files created

---

## Step 1: Add New Properties to Ontology

### Location
Open `gmn_ontology.ttl` and locate the `gmn:P11i_3_has_spouse` property definition.

### Action
Add the following two new property definitions immediately after `gmn:P11i_3_has_spouse`:

```turtle
# Property: marriage number for subject
gmn:marriage_number_for_subject
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "marriage number for subject"@en ;
    rdfs:comment "Ordinal number indicating which marriage this is for the subject person (the person who has the has_spouse property). Values are positive integers: 1 for first marriage, 2 for second marriage, etc. This property is used within the object of gmn:P11i_3_has_spouse to indicate the marriage enumeration. When transformed to CIDOC-CRM, this creates an E13_Attribute_Assignment that assigns the ordinal number to the subject person's participation in the marriage event."@en ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range xsd:integer ;
    dcterms:created "2025-10-27"^^xsd:date ;
    rdfs:seeAlso cidoc:P140i_was_attributed_by, cidoc:P141_assigned .

# Property: marriage number for spouse
gmn:marriage_number_for_spouse
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "marriage number for spouse"@en ;
    rdfs:comment "Ordinal number indicating which marriage this is for the spouse (the person being referenced as the spouse). Values are positive integers: 1 for first marriage, 2 for second marriage, etc. This property is used within the object of gmn:P11i_3_has_spouse to indicate the marriage enumeration. When transformed to CIDOC-CRM, this creates an E13_Attribute_Assignment that assigns the ordinal number to the spouse's participation in the marriage event."@en ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range xsd:integer ;
    dcterms:created "2025-10-27"^^xsd:date ;
    rdfs:seeAlso cidoc:P140i_was_attributed_by, cidoc:P141_assigned .
```

### Placement
Insert these properties right after `gmn:P11i_3_has_spouse` but before `gmn:P22_1_has_owner`.

### Validation
```bash
rapper -i turtle gmn_ontology.ttl -o turtle > /dev/null
```

If no errors, proceed to next step.

---

## Step 2: Replace Transformation Function

### Location
Open `gmn_to_cidoc_transform.py` and locate the existing `transform_p11i_3_has_spouse()` function.

### Action
Replace the entire function with this enhanced version:

```python
def transform_p11i_3_has_spouse(data):
    """
    Transform gmn:P11i_3_has_spouse to full CIDOC-CRM structure with optional enumeration:
    P11i_participated_in > E5_Event (marriage) > P11_had_participant > E21_Person
    
    When marriage enumeration is provided (gmn:marriage_number_for_subject or 
    gmn:marriage_number_for_spouse), creates E13_Attribute_Assignment nodes using:
    P140i_was_attributed_by > E13_Attribute_Assignment > P141_assigned > integer
    
    Args:
        data: Dictionary representing a JSON-LD entity with potential spouse information
    
    Returns:
        Dictionary with transformed CIDOC-CRM compliant structure
    """
    if 'gmn:P11i_3_has_spouse' not in data:
        return data
    
    spouses = data['gmn:P11i_3_has_spouse']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    for spouse_obj in spouses:
        # Handle both dictionary and string formats
        if isinstance(spouse_obj, dict):
            spouse_uri = spouse_obj.get('@id', '')
            spouse_data = spouse_obj.copy()
            
            # Extract enumeration data if present
            subject_marriage_num = spouse_obj.get('gmn:marriage_number_for_subject')
            spouse_marriage_num = spouse_obj.get('gmn:marriage_number_for_spouse')
            
            # Remove enumeration properties from spouse_data as they're not person attributes
            spouse_data.pop('gmn:marriage_number_for_subject', None)
            spouse_data.pop('gmn:marriage_number_for_spouse', None)
        else:
            spouse_uri = str(spouse_obj)
            spouse_data = {
                '@id': spouse_uri,
                '@type': 'cidoc:E21_Person'
            }
            subject_marriage_num = None
            spouse_marriage_num = None
        
        # Generate unique event URI using hash
        event_hash = str(hash(spouse_uri + 'marriage'))[-8:]
        event_uri = f"{subject_uri}/event/marriage_{event_hash}"
        
        # Create base marriage event structure
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P2_has_type': {
                '@id': AAT_MARRIAGE,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P11_had_participant': [spouse_data]
        }
        
        # Add E13_Attribute_Assignment nodes for marriage enumeration if provided
        if subject_marriage_num is not None or spouse_marriage_num is not None:
            event['cidoc:P140i_was_attributed_by'] = []
            
            # Create attribution for subject's marriage number
            if subject_marriage_num is not None:
                subject_hash = str(hash(subject_uri))[-8:]
                subject_attr_uri = f"{event_uri}/attribution_{subject_hash}"
                
                subject_attribution = {
                    '@id': subject_attr_uri,
                    '@type': 'cidoc:E13_Attribute_Assignment',
                    'cidoc:P140_assigned_attribute_to': {
                        '@id': subject_uri,
                        '@type': 'cidoc:E21_Person'
                    },
                    'cidoc:P141_assigned': {
                        '@value': str(subject_marriage_num),
                        '@type': 'xsd:integer'
                    },
                    'cidoc:P177_assigned_property_of_type': {
                        '@id': 'cidoc:P11_had_participant'
                    }
                }
                event['cidoc:P140i_was_attributed_by'].append(subject_attribution)
            
            # Create attribution for spouse's marriage number
            if spouse_marriage_num is not None:
                spouse_hash = str(hash(spouse_uri))[-8:]
                spouse_attr_uri = f"{event_uri}/attribution_{spouse_hash}"
                
                spouse_attribution = {
                    '@id': spouse_attr_uri,
                    '@type': 'cidoc:E13_Attribute_Assignment',
                    'cidoc:P140_assigned_attribute_to': {
                        '@id': spouse_uri,
                        '@type': 'cidoc:E21_Person'
                    },
                    'cidoc:P141_assigned': {
                        '@value': str(spouse_marriage_num),
                        '@type': 'xsd:integer'
                    },
                    'cidoc:P177_assigned_property_of_type': {
                        '@id': 'cidoc:P11_had_participant'
                    }
                }
                event['cidoc:P140i_was_attributed_by'].append(spouse_attribution)
        
        data['cidoc:P11i_participated_in'].append(event)
    
    del data['gmn:P11i_3_has_spouse']
    return data
```

### Important Notes

1. **Backward Compatibility**: This function handles marriages without enumeration
2. **Optional Properties**: Both enumeration properties are optional
3. **Cleanup**: Enumeration properties are removed from spouse_data before adding to event

### No Pipeline Changes Needed
The function registration in `transform_item()` remains the same - no changes needed there.

---

## Step 3: Testing

### Test Case 1: Marriage with Full Enumeration

**Input**: Create `test_enumeration_full.json`
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "person:giovanni",
  "@type": "cidoc:E21_Person",
  "rdfs:label": "Giovanni",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:maria",
      "@type": "cidoc:E21_Person",
      "rdfs:label": "Maria",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 1
    }
  ]
}
```

**Run**:
```bash
python gmn_to_cidoc_transform.py test_enumeration_full.json output_full.json
```

**Expected Output**: Should contain:
- E5_Event with marriage type
- Two E13_Attribute_Assignment nodes
- One with P141_assigned = "2" for Giovanni
- One with P141_assigned = "1" for Maria

### Test Case 2: Marriage with Partial Enumeration

**Input**: `test_enumeration_partial.json`
```json
{
  "@id": "person:paolo",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:francesca",
      "gmn:marriage_number_for_subject": 1
    }
  ]
}
```

**Expected**: Only one E13_Attribute_Assignment for the subject.

### Test Case 3: Marriage without Enumeration (Backward Compatibility)

**Input**: `test_no_enumeration.json`
```json
{
  "@id": "person:lorenzo",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {"@id": "person:clarice"}
  ]
}
```

**Expected**: Simple marriage event with no P140i_was_attributed_by property.

### Test Case 4: Multiple Marriages with Different Enumerations

**Input**: `test_multiple_marriages.json`
```json
{
  "@id": "person:cosimo",
  "@type": "cidoc:E21_Person",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:first_wife",
      "gmn:marriage_number_for_subject": 1,
      "gmn:marriage_number_for_spouse": 1
    },
    {
      "@id": "person:second_wife",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 1
    }
  ]
}
```

**Expected**: Two separate marriage events, each with appropriate attributions.

### Automated Test Script

Create `test_enumeration.py`:

```python
import json
from gmn_to_cidoc_transform import transform_p11i_3_has_spouse

def test_full_enumeration():
    data = {
        "@id": "person:test",
        "gmn:P11i_3_has_spouse": [
            {
                "@id": "person:spouse",
                "gmn:marriage_number_for_subject": 2,
                "gmn:marriage_number_for_spouse": 1
            }
        ]
    }
    result = transform_p11i_3_has_spouse(data)
    
    # Verify event exists
    assert 'cidoc:P11i_participated_in' in result
    event = result['cidoc:P11i_participated_in'][0]
    
    # Verify attributions exist
    assert 'cidoc:P140i_was_attributed_by' in event
    attrs = event['cidoc:P140i_was_attributed_by']
    assert len(attrs) == 2
    
    # Verify values
    nums = [attr['cidoc:P141_assigned']['@value'] for attr in attrs]
    assert '2' in nums and '1' in nums
    
    print("✓ Full enumeration test passed")

def test_no_enumeration():
    data = {
        "@id": "person:test",
        "gmn:P11i_3_has_spouse": [{"@id": "person:spouse"}]
    }
    result = transform_p11i_3_has_spouse(data)
    
    event = result['cidoc:P11i_participated_in'][0]
    assert 'cidoc:P140i_was_attributed_by' not in event
    
    print("✓ No enumeration test passed")

if __name__ == "__main__":
    test_full_enumeration()
    test_no_enumeration()
    print("\n✓ All tests passed!")
```

**Run**:
```bash
python test_enumeration.py
```

---

## Step 4: Update Documentation

### Update Main Documentation

Add the following sections from `enumeration-doc-note.txt` to your main documentation:

1. Property table entries for new properties
2. Examples of enumerated marriages
3. SPARQL queries for marriage enumeration
4. Usage guidelines for when to use enumeration

### Update README

Add note about enumeration support:
```markdown
## Optional: Marriage Enumeration

The P11i.3 has spouse property supports optional marriage enumeration to indicate 
which marriage this is for each person (1st, 2nd, 3rd, etc.). See the enumeration 
supplement documentation for details.
```

---

## Troubleshooting

### Issue 1: "KeyError: 'gmn:marriage_number_for_subject'"

**Cause**: Code expects enumeration properties but doesn't handle their absence.

**Solution**: Use `.get()` method with default of `None`:
```python
subject_marriage_num = spouse_obj.get('gmn:marriage_number_for_subject')
```

### Issue 2: Attribution URIs Not Unique

**Cause**: Hash collision or improper URI generation.

**Solution**: Verify hash includes person URI:
```python
subject_hash = str(hash(subject_uri))[-8:]
```

### Issue 3: Enumeration Properties Appear in Spouse Data

**Cause**: Properties not removed before adding spouse to event.

**Solution**: Ensure cleanup:
```python
spouse_data.pop('gmn:marriage_number_for_subject', None)
spouse_data.pop('gmn:marriage_number_for_spouse', None)
```

### Issue 4: Integer Values Stored as Strings

**Cause**: Not converting to string for JSON-LD.

**Solution**: Use `str()` conversion:
```python
'@value': str(subject_marriage_num),
'@type': 'xsd:integer'
```

### Issue 5: No Attribution Nodes Created

**Cause**: Condition check fails when value is 0 or False-like.

**Solution**: Use explicit `is not None` check:
```python
if subject_marriage_num is not None:
```

---

## Validation

### Ontology Validation

```bash
# Validate Turtle syntax
rapper -i turtle gmn_ontology.ttl -o turtle > /dev/null

# Check for new properties
grep -c "marriage_number_for" gmn_ontology.ttl
# Should output: 2
```

### Transformation Validation

```bash
# Transform test file
python gmn_to_cidoc_transform.py test_enumeration_full.json output.json

# Verify E13 nodes exist
grep -c "E13_Attribute_Assignment" output.json
# Should be > 0 if enumeration provided

# Verify P141 assignments
grep -c "P141_assigned" output.json
# Should equal number of enumerations
```

### SPARQL Validation

Run this query on your transformed data:

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

# Verify all attributions are properly formed
SELECT ?event ?person ?number
WHERE {
  ?event cidoc:P140i_was_attributed_by ?attr .
  ?attr a cidoc:E13_Attribute_Assignment .
  ?attr cidoc:P140_assigned_attribute_to ?person .
  ?attr cidoc:P141_assigned ?number .
  ?attr cidoc:P177_assigned_property_of_type cidoc:P11_had_participant .
}
```

### Validation Checklist

After implementation:

- [ ] New properties exist in ontology
- [ ] TTL validates without errors
- [ ] Transformation handles enumeration correctly
- [ ] Transformation handles missing enumeration (backward compatible)
- [ ] Attribution URIs are unique
- [ ] P177 correctly references P11_had_participant
- [ ] Values are properly typed as xsd:integer
- [ ] Multiple marriages each get separate attributions
- [ ] SPARQL queries return expected results

---

## Performance Considerations

### Storage Impact
- **Per enumerated marriage**: ~300-400 bytes additional JSON-LD
- **1000 marriages**: ~300-400 KB additional storage

### Query Performance
- Attribution nodes increase query depth
- Use indexed queries for large datasets
- Consider materialized views for common queries

### Optimization Tips
1. Only add enumeration when needed (historical research value)
2. Use batch processing for large transformations
3. Index P140i_was_attributed_by for faster queries
4. Cache transformation results when possible

---

## Next Steps

1. ✅ Test with real historical data
2. ✅ Update project documentation
3. ✅ Train data entry staff on new properties
4. ✅ Create data validation rules
5. ✅ Consider extending to other relationship types

---

## Reference

### Files Modified
1. `gmn_ontology.ttl` - Added 2 new properties
2. `gmn_to_cidoc_transform.py` - Replaced 1 function

### Files Created (Optional)
1. `test_enumeration.py` - Test suite
2. `test_enumeration_full.json` - Test data
3. `test_no_enumeration.json` - Test data

### Time Investment
- Implementation: ~20 minutes
- Testing: ~10 minutes
- Documentation: ~10 minutes (if updating)
- **Total**: ~40 minutes

---

**Implementation Guide Version**: 1.0  
**Date**: 2025-10-27  
**Approach**: E13_Attribute_Assignment (Option 2)
