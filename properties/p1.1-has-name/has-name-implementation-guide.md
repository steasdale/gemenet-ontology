# GMN P1.1 has_name Property - Implementation Guide

**Version:** 1.0  
**Date:** October 26, 2025  
**Estimated Time:** 2 hours (including testing)

## Introduction

This guide provides step-by-step instructions for implementing and verifying the `gmn:P1_1_has_name` property in your GMN ontology system. The property is already implemented in the current codebase, so this guide focuses on verification, testing, and integration.

## Prerequisites

Before starting implementation:

- [ ] Access to gmn_ontology.ttl file
- [ ] Access to gmn_to_cidoc_transform.py file
- [ ] Python 3.6+ installed
- [ ] RDF/TTL validation tools (optional but recommended)
- [ ] Test environment for validation
- [ ] Backup of current files

## Implementation Overview

### Current Status

✅ **Property Definition:** Already exists in gmn_ontology.ttl (created 2025-10-16, modified 2025-10-17)  
✅ **Transformation Code:** Already exists in gmn_to_cidoc_transform.py  
✅ **AAT Constants:** Already defined in transformation script

**This guide will help you:**
1. Verify the existing implementation
2. Test the transformation functionality
3. Integrate with your data entry workflows
4. Update documentation and training materials

---

## Phase 1: Pre-Implementation Verification

### Step 1.1: Backup Current System

Create backups of all files before making any changes:

```bash
# Navigate to your project directory
cd /path/to/gmn/project

# Create backup directory with timestamp
mkdir -p backups/$(date +%Y%m%d)

# Backup ontology file
cp gmn_ontology.ttl backups/$(date +%Y%m%d)/gmn_ontology.ttl.bak

# Backup transformation script
cp gmn_to_cidoc_transform.py backups/$(date +%Y%m%d)/gmn_to_cidoc_transform.py.bak

# Verify backups
ls -lh backups/$(date +%Y%m%d)/
```

### Step 1.2: Verify File Access

Check that you have read/write access to necessary files:

```bash
# Check ontology file
ls -l gmn_ontology.ttl

# Check transformation script
ls -l gmn_to_cidoc_transform.py

# Check file permissions
test -r gmn_ontology.ttl && echo "✓ Can read ontology"
test -w gmn_ontology.ttl && echo "✓ Can write ontology"
test -r gmn_to_cidoc_transform.py && echo "✓ Can read script"
test -w gmn_to_cidoc_transform.py && echo "✓ Can write script"
```

---

## Phase 2: Verify Ontology Definition

### Step 2.1: Locate Property in Ontology

Open `gmn_ontology.ttl` and locate the P1.1 has_name property:

```bash
# Search for the property definition
grep -n "P1_1_has_name" gmn_ontology.ttl
```

The property should be around line 280 and look like this:

```turtle
# Property: P1.1 has name
gmn:P1_1_has_name 
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P1.1 has name"@en ;
    rdfs:comment "Simplified property for expressing the name of any entity in the database (persons, places, things, contracts, etc.). Represents the full CIDOC-CRM path: E1_CRM_Entity > P1_is_identified_by > E41_Appellation > P2_has_type <http://vocab.getty.edu/aat/300404650> > P190_has_symbolic_content. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The appellation type is automatically set to AAT 300404650 (names)."@en ;
    rdfs:subPropertyOf cidoc:P1_is_identified_by ;
    rdfs:domain cidoc:E1_CRM_Entity ;
    rdfs:range cidoc:E62_String ;
    dcterms:created "2025-10-16"^^xsd:date ;
    dcterms:modified "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P1_is_identified_by, cidoc:P190_has_symbolic_content, aat:300404650 ;
    owl:equivalentProperty [
        a owl:Restriction ;
        owl:onProperty cidoc:P1_is_identified_by ;
        owl:allValuesFrom [
            a owl:Restriction ;
            owl:onProperty cidoc:P190_has_symbolic_content ;
            owl:hasValue cidoc:E62_String
        ]
    ] ;
    gmn:hasImplicitType aat:300404650 .
```

### Step 2.2: Validate Property Definition

✅ **Verification Checklist:**

- [ ] Property URI is `gmn:P1_1_has_name`
- [ ] Property type is `owl:DatatypeProperty`
- [ ] Label is "P1.1 has name"
- [ ] Domain is `cidoc:E1_CRM_Entity`
- [ ] Range is `cidoc:E62_String`
- [ ] Has `rdfs:subPropertyOf cidoc:P1_is_identified_by`
- [ ] Has `gmn:hasImplicitType aat:300404650`
- [ ] Created date is present
- [ ] Modified date is present

### Step 2.3: Validate TTL Syntax

Use an RDF validator to check syntax (optional but recommended):

```bash
# Using rapper (install with: apt-get install raptor2-utils)
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# If successful, you'll see: "rapper: Parsing returned 0 triples"
```

---

## Phase 3: Verify Transformation Code

### Step 3.1: Locate AAT Constant

Open `gmn_to_cidoc_transform.py` and verify the AAT constant (around line 23):

```python
# Getty AAT URI constants
AAT_NAME = "http://vocab.getty.edu/page/aat/300404650"
```

✅ **Verification:**
- [ ] Constant is defined
- [ ] URI is correct (AAT 300404650 for "names")
- [ ] No typos in the URL

### Step 3.2: Locate Transformation Function

Find the `transform_p1_1_has_name` function (around line 49):

```python
def transform_p1_1_has_name(data):
    """Transform gmn:P1_1_has_name to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_1_has_name', AAT_NAME)
```

✅ **Verification:**
- [ ] Function is defined
- [ ] Function name is correct
- [ ] Calls `transform_name_property` with correct parameters
- [ ] Uses correct property name string
- [ ] Uses AAT_NAME constant

### Step 3.3: Verify Generic Transform Function

Locate the `transform_name_property` function (around line 31):

```python
def transform_name_property(data, property_name, aat_type_uri):
    """
    Generic function to transform name shortcut properties to full CIDOC-CRM structure.
    
    Args:
        data: The item data dictionary
        property_name: The shortcut property name (e.g., 'gmn:P1_1_has_name')
        aat_type_uri: The AAT URI for the type of name
    
    Returns:
        Modified data dictionary
    """
    if property_name not in data:
        return data
    
    names = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P1_is_identified_by' not in data:
        data['cidoc:P1_is_identified_by'] = []
    
    for name_obj in names:
        if isinstance(name_obj, dict):
            name_value = name_obj.get('@value', '')
        else:
            name_value = str(name_obj)
        
        if not name_value:
            continue
        
        appellation_uri = generate_appellation_uri(subject_uri, name_value, property_name)
        
        appellation = {
            '@id': appellation_uri,
            '@type': 'cidoc:E41_Appellation',
            'cidoc:P2_has_type': {
                '@id': aat_type_uri,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P190_has_symbolic_content': name_value
        }
        
        data['cidoc:P1_is_identified_by'].append(appellation)
    
    del data[property_name]
    return data
```

✅ **Verification:**
- [ ] Function handles both dict and string inputs
- [ ] Creates unique appellation URI
- [ ] Sets correct AAT type
- [ ] Removes shortcut property after transformation
- [ ] Handles multiple names correctly

### Step 3.4: Verify Function is Registered

Check that the transform function is in the TRANSFORMERS list:

```bash
# Search for transform_p1_1_has_name in TRANSFORMERS list
grep -A 20 "TRANSFORMERS = " gmn_to_cidoc_transform.py | grep "transform_p1_1_has_name"
```

You should see:
```python
TRANSFORMERS = [
    # ... other transformers ...
    transform_p1_1_has_name,
    # ... other transformers ...
]
```

---

## Phase 4: Testing

### Step 4.1: Create Test Data

Create a test JSON-LD file (`test_p1_1_has_name.json`):

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#"
  },
  "@graph": [
    {
      "@id": "http://example.org/test/person1",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": [
        {"@value": "Giovanni Spinola"}
      ]
    },
    {
      "@id": "http://example.org/test/place1",
      "@type": "cidoc:E53_Place",
      "gmn:P1_1_has_name": [
        {"@value": "Genoa"}
      ]
    },
    {
      "@id": "http://example.org/test/contract1",
      "@type": "gmn:E31_2_Sales_Contract",
      "gmn:P1_1_has_name": [
        {"@value": "Sale of Building on Via San Lorenzo"}
      ]
    }
  ]
}
```

### Step 4.2: Run Transformation

Execute the transformation script:

```bash
# Run transformation
python3 gmn_to_cidoc_transform.py test_p1_1_has_name.json output_test.json

# View results
cat output_test.json | python3 -m json.tool
```

### Step 4.3: Verify Output Structure

The output should contain structures like:

```json
{
  "@id": "http://example.org/test/person1",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://example.org/test/person1/appellation/12345678",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Giovanni Spinola"
    }
  ]
}
```

✅ **Output Verification:**
- [ ] `gmn:P1_1_has_name` is removed
- [ ] `cidoc:P1_is_identified_by` is present
- [ ] Appellation has `@id` with correct URI pattern
- [ ] Appellation type is `cidoc:E41_Appellation`
- [ ] `P2_has_type` points to AAT 300404650
- [ ] `P190_has_symbolic_content` contains the name value
- [ ] All three test entities transformed correctly

### Step 4.4: Test Edge Cases

Create additional test cases:

**Test 4.4a: Multiple Names**
```json
{
  "@id": "http://example.org/test/person2",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [
    {"@value": "Antonio Doria"},
    {"@value": "Antonius Auria"}
  ]
}
```

Expected: Two separate appellation resources created.

**Test 4.4b: Empty Name**
```json
{
  "@id": "http://example.org/test/person3",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [
    {"@value": ""}
  ]
}
```

Expected: No appellation created, property removed.

**Test 4.4c: No Name Property**
```json
{
  "@id": "http://example.org/test/person4",
  "@type": "cidoc:E21_Person"
}
```

Expected: No changes to the entity.

### Step 4.5: Run Full Test Suite

```bash
# Create test directory
mkdir -p tests/p1_1_has_name

# Run all tests
for test_file in tests/p1_1_has_name/*.json; do
    echo "Testing: $test_file"
    python3 gmn_to_cidoc_transform.py "$test_file" "output_$(basename $test_file)"
    echo "---"
done

# Validate all outputs
for output_file in output_*.json; do
    echo "Validating: $output_file"
    python3 -m json.tool "$output_file" > /dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"
done
```

---

## Phase 5: Integration with Data Entry

### Step 5.1: Update Omeka-S Resource Templates

If using Omeka-S for data entry:

1. Navigate to Omeka-S admin interface
2. Go to Resource Templates
3. Select templates for entities that will use names (Person, Place, Contract, etc.)
4. Add `gmn:P1_1_has_name` property to the template
5. Configure property settings:
   - **Label:** "Name"
   - **Comment:** "General name for this entity"
   - **Type:** Literal (text)
   - **Required:** Optional or Required (based on your needs)
   - **Private:** No

### Step 5.2: Create Data Entry Guidelines

Document when to use `gmn:P1_1_has_name` vs. other name properties:

```markdown
## Name Property Selection Guide

### Use gmn:P1_1_has_name when:
- Entering a general, modern name for cataloging
- Creating a display name for an entity
- The name doesn't fit specialized categories
- You need a simple, universal naming field

### Use specialized properties for:
- Historical source names → gmn:P1_2_has_name_from_source
- Patronymic names → gmn:P1_3_has_patrilineal_name
- Place-based names → gmn:P1_4_has_loconym
- Document titles → gmn:P102_1_has_title
```

### Step 5.3: Train Data Entry Staff

Conduct training session covering:

1. **When to use the property** - Review selection guide
2. **How to enter names** - Demonstrate in Omeka-S or data entry interface
3. **Transformation process** - Explain what happens behind the scenes
4. **Quality control** - Show how to verify correct usage

---

## Phase 6: Update Documentation

### Step 6.1: Add to Main Documentation

Add usage examples to your main documentation file. Use the content from `has-name-doc-note.txt`.

### Step 6.2: Update Property Reference Table

Add or update entry in your property reference documentation:

| Property | Domain | Range | AAT Type | Use Case |
|----------|--------|-------|----------|----------|
| gmn:P1_1_has_name | E1_CRM_Entity | String | 300404650 | General names for any entity |

### Step 6.3: Create Quick Reference Card

Create a one-page reference for data entry staff showing:
- Property URI and label
- When to use it
- Example usage
- Common mistakes to avoid

---

## Phase 7: Monitoring and Maintenance

### Step 7.1: Set Up Monitoring

Create a script to monitor usage of the property:

```bash
#!/bin/bash
# monitor_p1_1_usage.sh

echo "P1.1 has_name Usage Report"
echo "=========================="
echo "Date: $(date)"
echo ""

# Count occurrences in JSON-LD exports
echo "Occurrences in data: $(grep -c 'P1_1_has_name' export_*.json)"

# Count successful transformations
echo "Successful transformations: $(grep -c 'P1_is_identified_by' transformed_*.json)"

# Check for errors in logs
echo "Transformation errors: $(grep -c 'ERROR.*P1_1_has_name' transformation.log)"
```

### Step 7.2: Regular Validation

Schedule regular validation checks:

```bash
# Weekly validation cron job
0 2 * * 1 /path/to/validate_p1_1_has_name.sh >> /var/log/gmn_validation.log 2>&1
```

### Step 7.3: Handle Issues

Common issues and solutions:

| Issue | Cause | Solution |
|-------|-------|----------|
| Names not transforming | Function not in TRANSFORMERS list | Add function to list |
| Invalid URIs | Missing @id in entity | Ensure all entities have @id |
| Duplicate appellations | Same name entered twice | Check data entry for duplicates |
| Wrong AAT type | AAT_NAME constant incorrect | Verify constant value |

---

## Phase 8: Quality Assurance

### Step 8.1: Validate Sample Data

Pull a sample of transformed data and manually verify:

```bash
# Extract sample
python3 -c "
import json
import random

with open('transformed_data.json') as f:
    data = json.load(f)

# Sample 10 random entities with P1_is_identified_by
sample = random.sample([e for e in data['@graph'] if 'cidoc:P1_is_identified_by' in e], 10)

with open('validation_sample.json', 'w') as f:
    json.dump({'@graph': sample}, f, indent=2)
"

# Review sample manually
cat validation_sample.json | less
```

### Step 8.2: Check CIDOC-CRM Compliance

Verify that transformed data complies with CIDOC-CRM:

✅ **Compliance Checklist:**
- [ ] E41_Appellation resources have valid URIs
- [ ] P2_has_type points to E55_Type
- [ ] P190_has_symbolic_content contains string values
- [ ] P1_is_identified_by connects entities to appellations
- [ ] No orphaned shortcut properties remain

### Step 8.3: Performance Testing

Test transformation performance with large datasets:

```bash
# Time transformation of large file
time python3 gmn_to_cidoc_transform.py large_export.json large_output.json

# Monitor memory usage
/usr/bin/time -v python3 gmn_to_cidoc_transform.py large_export.json large_output.json
```

---

## Troubleshooting Guide

### Problem: Property Not Found in Ontology

**Symptoms:**
- grep command returns no results
- Property not visible in ontology viewer

**Solutions:**
1. Check file path: `ls -l gmn_ontology.ttl`
2. Check for typos in property name
3. Verify you're looking at the correct version of the file
4. Search case-insensitively: `grep -i "p1.*has.*name" gmn_ontology.ttl`

### Problem: Transformation Not Working

**Symptoms:**
- Shortcut property still present in output
- No P1_is_identified_by created

**Solutions:**
1. Verify function is in TRANSFORMERS list
2. Check function name spelling
3. Test transformation function independently:
```python
# test_transform.py
from gmn_to_cidoc_transform import transform_p1_1_has_name

test_data = {
    '@id': 'http://test.com/person1',
    'gmn:P1_1_has_name': [{'@value': 'Test Name'}]
}

result = transform_p1_1_has_name(test_data)
print(json.dumps(result, indent=2))
```

### Problem: Invalid URIs Generated

**Symptoms:**
- URIs contain spaces or invalid characters
- URIs don't follow expected pattern

**Solutions:**
1. Check entity @id values for validity
2. Verify name values don't contain special characters
3. Review generate_appellation_uri function
4. Test URI generation:
```python
from gmn_to_cidoc_transform import generate_appellation_uri

test_uri = generate_appellation_uri(
    "http://example.org/person1",
    "Test Name",
    "gmn:P1_1_has_name"
)
print(test_uri)  # Should be valid URI
```

### Problem: Wrong AAT Type

**Symptoms:**
- P2_has_type points to wrong AAT concept
- AAT URI is malformed

**Solutions:**
1. Verify AAT_NAME constant: `grep "AAT_NAME =" gmn_to_cidoc_transform.py`
2. Check for typos in the AAT URI
3. Verify AAT 300404650 is correct concept for "names"

---

## Post-Implementation Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Staff trained
- [ ] Omeka-S templates configured
- [ ] Monitoring in place
- [ ] Sample data validated
- [ ] Performance acceptable
- [ ] Backup strategy confirmed
- [ ] Rollback plan documented

---

## Next Steps

After successful implementation:

1. **Monitor Usage** - Track how often the property is used
2. **Gather Feedback** - Get input from data entry staff
3. **Refine Guidelines** - Update usage guidelines based on real-world use
4. **Extend Testing** - Add more edge cases as they're discovered
5. **Document Patterns** - Note common usage patterns for future reference

---

## Conclusion

The `gmn:P1_1_has_name` property is already implemented and ready to use. This guide has walked you through verification, testing, and integration steps to ensure smooth operation in your environment.

For questions or issues, consult:
- has-name-documentation.md for semantic details
- has-name-ontology.ttl for property definition
- has-name-transform.py for transformation code
- has-name-doc-note.txt for documentation examples

**Implementation Status:** ✅ Complete and Ready for Use
