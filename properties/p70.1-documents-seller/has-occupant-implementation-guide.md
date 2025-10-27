# Implementation Guide: gmn:P53_1_has_occupant
## Step-by-Step Instructions for Complete Implementation

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Phase 1: Ontology Definition](#phase-1-ontology-definition)
3. [Phase 2: Transformation Script](#phase-2-transformation-script)
4. [Phase 3: Testing & Validation](#phase-3-testing--validation)
5. [Phase 4: Documentation](#phase-4-documentation)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script
- Project documentation file

### Required Knowledge
- Understanding of CIDOC-CRM basics
- Familiarity with RDF/TTL syntax
- Basic Python programming
- JSON-LD data format

### Tools Needed
- Text editor or IDE
- Python 3.7+
- RDF validation tool (optional but recommended)

---

## Phase 1: Ontology Definition

### Step 1.1: Locate Insertion Point

Open `gmn_ontology.ttl` and find the property definitions section. The `gmn:P53_1_has_occupant` property should be placed after the ownership property (`gmn:P22_1_has_owner`) and before the building border property (`gmn:P122_1_borders_with`).

**Search for:**
```turtle
# Property: P22.1 has owner
gmn:P22_1_has_owner
```

**Insert after** the complete P22.1 definition block.

### Step 1.2: Add Property Definition

Copy the complete TTL definition from `has-occupant-ontology.ttl` and insert it into your ontology file:

```turtle
# Property: P53.1 has occupant
gmn:P53_1_has_occupant
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P53.1 has occupant"@en ;
    rdfs:comment "Simplified property for expressing occupation/residence in a building by a person who is not the owner. Represents the full CIDOC-CRM path: E22_Human-Made_Object > P53i_is_former_or_current_location_of > E9_Move > P25_moved > E21_Person. This property captures residence/occupation relationships through move events. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. This is distinct from ownership."@en ;
    rdfs:subPropertyOf cidoc:P53i_is_former_or_current_location_of ;
    rdfs:domain gmn:E22_1_Building ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P53i_is_former_or_current_location_of, cidoc:P25_moved .
```

### Step 1.3: Verify Definition

Check the following:
- [ ] Property has both `owl:ObjectProperty` and `rdf:Property` types
- [ ] Label and comment are present and descriptive
- [ ] `rdfs:subPropertyOf` correctly references parent CIDOC-CRM property
- [ ] Domain is `gmn:E22_1_Building`
- [ ] Range is `cidoc:E21_Person`
- [ ] Created date is present
- [ ] `rdfs:seeAlso` references related properties

### Step 1.4: Validate Ontology

Run your ontology through a validator:
```bash
# Example using rapper (if available)
rapper -i turtle -o turtle gmn_ontology.ttl > /dev/null
```

If validation succeeds, proceed to Phase 2.

---

## Phase 2: Transformation Script

### Step 2.1: Add Transformation Function

Open `gmn_to_cidoc_transform.py` and locate the section with property transformation functions. Add the following function after `transform_p22_1_has_owner()`:

```python
def transform_p53_1_has_occupant(data):
    """
    Transform gmn:P53_1_has_occupant to full CIDOC-CRM structure:
    P53_has_former_or_current_location > E21_Person
    
    The building's location serves as a place where persons reside.
    """
    if 'gmn:P53_1_has_occupant' not in data:
        return data
    
    occupants = data['gmn:P53_1_has_occupant']
    
    # Initialize CIDOC-CRM property if not present
    if 'cidoc:P53_has_former_or_current_location' not in data:
        data['cidoc:P53_has_former_or_current_location'] = []
    
    # Process each occupant
    for occupant_obj in occupants:
        if isinstance(occupant_obj, dict):
            occupant_data = occupant_obj.copy()
            if '@type' not in occupant_data:
                occupant_data['@type'] = 'cidoc:E21_Person'
        else:
            # Handle URI string format
            occupant_uri = str(occupant_obj)
            occupant_data = {
                '@id': occupant_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        data['cidoc:P53_has_former_or_current_location'].append(occupant_data)
    
    # Remove shortcut property
    del data['gmn:P53_1_has_occupant']
    return data
```

### Step 2.2: Add Function to Transformation Pipeline

Locate the `transform_item()` function (usually near the end of the file) and add the function call in the appropriate section:

**Find this section:**
```python
    # Property ownership and occupation
    item = transform_p22_1_has_owner(item)
```

**Add this line after it:**
```python
    item = transform_p53_1_has_occupant(item)
```

**Complete context:**
```python
    # Property ownership and occupation
    item = transform_p22_1_has_owner(item)
    item = transform_p53_1_has_occupant(item)
    
    # Family relationships
    item = transform_p96_1_has_mother(item)
```

### Step 2.3: Verify Integration

Check that:
- [ ] Function is properly indented (4-space indentation)
- [ ] Function includes complete docstring
- [ ] Function handles both dict and string input formats
- [ ] Function properly deletes the shortcut property
- [ ] Function call is in the correct position in pipeline

---

## Phase 3: Testing & Validation

### Step 3.1: Create Test Data

Create a test JSON-LD file (`test_occupant.json`):

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@graph": [
    {
      "@id": "http://example.org/building/palace_medici",
      "@type": "gmn:E22_1_Building",
      "gmn:P1_1_has_name": [{"@value": "Palazzo Medici"}],
      "gmn:P53_1_has_occupant": [
        {"@id": "http://example.org/person/lorenzo_medici", "@type": "cidoc:E21_Person"}
      ]
    },
    {
      "@id": "http://example.org/person/lorenzo_medici",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": [{"@value": "Lorenzo de' Medici"}]
    }
  ]
}
```

### Step 3.2: Run Transformation

Execute the transformation script:

```bash
python3 gmn_to_cidoc_transform.py test_occupant.json test_occupant_output.json
```

### Step 3.3: Verify Output

Open `test_occupant_output.json` and verify:

**Expected output structure:**
```json
{
  "@id": "http://example.org/building/palace_medici",
  "@type": "gmn:E22_1_Building",
  "cidoc:P1_is_identified_by": [...],
  "cidoc:P53_has_former_or_current_location": [
    {
      "@id": "http://example.org/person/lorenzo_medici",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Verification checklist:**
- [ ] `gmn:P53_1_has_occupant` property has been removed
- [ ] `cidoc:P53_has_former_or_current_location` property is present
- [ ] Occupant data structure is preserved
- [ ] Person type is correctly set to `cidoc:E21_Person`
- [ ] All other building properties remain intact

### Step 3.4: Test Multiple Occupants

Create test data with multiple occupants:

```json
{
  "@id": "http://example.org/building/house_martelli",
  "@type": "gmn:E22_1_Building",
  "gmn:P1_1_has_name": [{"@value": "Casa Martelli"}],
  "gmn:P53_1_has_occupant": [
    {"@id": "http://example.org/person/niccolo_martelli"},
    {"@id": "http://example.org/person/maria_martelli"}
  ]
}
```

Run transformation and verify that both occupants appear in the output.

### Step 3.5: Test Edge Cases

**Test Case 1: Empty Occupant List**
```json
{
  "@id": "http://example.org/building/vacant",
  "@type": "gmn:E22_1_Building",
  "gmn:P53_1_has_occupant": []
}
```
Expected: Property should be removed, no errors.

**Test Case 2: No Occupant Property**
```json
{
  "@id": "http://example.org/building/warehouse",
  "@type": "gmn:E22_1_Building",
  "gmn:P1_1_has_name": [{"@value": "Warehouse"}]
}
```
Expected: Data passes through unchanged, no errors.

**Test Case 3: String URI Format**
```json
{
  "@id": "http://example.org/building/shop",
  "@type": "gmn:E22_1_Building",
  "gmn:P53_1_has_occupant": [
    "http://example.org/person/merchant_giovanni"
  ]
}
```
Expected: Transformation creates proper structure with @id and @type.

---

## Phase 4: Documentation

### Step 4.1: Add to Main Documentation

Open your project documentation file and add a section for the occupant property. Use the content from `has-occupant-doc-note.txt` as a template.

**Recommended location:** After the ownership property section, before border relationships.

### Step 4.2: Include Examples

Add practical examples showing:
- Single occupant in a palace
- Multiple occupants in a shared house
- Temporal changes in occupancy (if using time-spans)
- Distinction between owner and occupant

### Step 4.3: Add Usage Guidelines

Document when to use `gmn:P53_1_has_occupant`:
- ✅ For residents who are not owners
- ✅ For tenants and renters
- ✅ For family members living in a property they don't own
- ❌ Not for property owners (use `gmn:P22_1_has_owner`)
- ❌ Not for temporary visitors

### Step 4.4: Cross-Reference Related Properties

Create links or references to:
- `gmn:P22_1_has_owner` (ownership)
- `cidoc:P74_has_current_or_former_residence` (person-centric residence)
- `cidoc:P53i_is_former_or_current_location_of` (parent property)

---

## Troubleshooting

### Issue 1: Property Not Being Transformed

**Symptoms:** The `gmn:P53_1_has_occupant` property appears in output unchanged.

**Solutions:**
1. Verify function is called in `transform_item()` pipeline
2. Check function name spelling matches exactly
3. Ensure data contains the property with correct namespace prefix
4. Verify function is not returning early due to conditional

**Debug steps:**
```python
# Add debug print at start of function
def transform_p53_1_has_occupant(data):
    print(f"DEBUG: Processing occupant for {data.get('@id', 'unknown')}")
    if 'gmn:P53_1_has_occupant' not in data:
        print("DEBUG: No occupant property found")
        return data
    print(f"DEBUG: Found {len(data['gmn:P53_1_has_occupant'])} occupants")
    # ... rest of function
```

### Issue 2: Multiple Occupants Not All Appearing

**Symptoms:** Only first occupant is in output, or some occupants are missing.

**Solutions:**
1. Verify loop iterates over all items in the list
2. Check that `append()` is used (not assignment with `=`)
3. Ensure initialization of output list happens before loop
4. Verify occupant data structure is correct in input

### Issue 3: Type Information Lost

**Symptoms:** Occupants in output missing `@type` field.

**Solutions:**
1. Check conditional that adds `@type` when missing
2. Verify `occupant_data.copy()` is used to avoid modifying original
3. Ensure `cidoc:E21_Person` type is correctly specified

### Issue 4: Validation Errors in Ontology

**Symptoms:** Ontology validator reports errors after adding property.

**Common causes:**
- Missing semicolon at end of previous property definition
- Incorrect namespace prefix (`gmn:` vs `cidoc:`)
- Malformed URI in `rdfs:seeAlso`
- Missing period at end of property definition block

**Solution:**
```turtle
# Correct format
gmn:P22_1_has_owner
    a owl:ObjectProperty ;
    rdfs:label "P22.1 has owner"@en ;
    ...
    rdfs:seeAlso cidoc:P24i_changed_ownership_through .  # ← period here

# Property: P53.1 has occupant  # ← new property starts here
gmn:P53_1_has_occupant
    ...
```

### Issue 5: JSON Parse Errors

**Symptoms:** Script fails with JSON parsing errors.

**Solutions:**
1. Validate input JSON syntax (use https://jsonlint.com or similar)
2. Check for trailing commas in JSON arrays
3. Verify proper nesting of brackets and braces
4. Ensure UTF-8 encoding for non-ASCII characters

---

## Performance Considerations

### Large Datasets

For buildings with many occupants or datasets with thousands of buildings:

1. **Memory usage:** The transformation loads entire JSON into memory. For very large files, consider batch processing.

2. **Processing time:** Each occupant requires individual processing. Monitor performance with:
   ```python
   import time
   start = time.time()
   result = transform_item(data)
   print(f"Processed in {time.time() - start:.3f} seconds")
   ```

3. **Optimization:** If processing many buildings, the current implementation is efficient (O(n) complexity).

---

## Next Steps

After successful implementation:

1. **Deploy to production:** Update production ontology and transformation script
2. **Train data entry personnel:** Document the new property in user guides
3. **Update data entry forms:** Add occupant field to building entry forms
4. **Migrate existing data:** If needed, identify and tag occupants in historical data
5. **Monitor usage:** Track how the property is used to identify any issues

---

## Support and Resources

- **Ontology Questions:** Review CIDOC-CRM documentation for P53 and related properties
- **Implementation Issues:** Check transformation script logs and error messages
- **Data Questions:** Consult historical sources to distinguish owners from occupants
- **Technical Support:** Refer to project documentation and team resources

---

**Version:** 1.0  
**Last Updated:** 2025-10-27  
**Implementation Status:** Ready for production use
