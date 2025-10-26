# has_name_from_source Property Implementation Guide

**Implementation Guide for**: `gmn:P1_2_has_name_from_source`  
**Version**: 1.0  
**Last Updated**: October 26, 2025

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Implementation Overview](#implementation-overview)
3. [Step 1: Update Ontology File](#step-1-update-ontology-file)
4. [Step 2: Update Transformation Script](#step-2-update-transformation-script)
5. [Step 3: Validate Changes](#step-3-validate-changes)
6. [Step 4: Test Implementation](#step-4-test-implementation)
7. [Step 5: Deploy to Production](#step-5-deploy-to-production)
8. [Troubleshooting](#troubleshooting)
9. [Verification Checklist](#verification-checklist)

## Prerequisites

Before implementing the `has_name_from_source` property, ensure you have:

- [ ] Access to the GMN ontology file (`gmn_ontology.ttl`)
- [ ] Access to the transformation script (`gmn_to_cidoc_transform.py`)
- [ ] Python 3.7 or higher installed
- [ ] RDF libraries installed (`rdflib` for validation)
- [ ] Text editor or IDE for editing files
- [ ] Git access for version control (recommended)
- [ ] Test environment for validation before production deployment

## Implementation Overview

The implementation consists of two main components:

1. **Ontology Definition**: Add the property definition to `gmn_ontology.ttl`
2. **Transformation Logic**: Add the transformation function to `gmn_to_cidoc_transform.py`

**Estimated Time**: 2-3 hours (including testing)

**Difficulty Level**: Intermediate

## Step 1: Update Ontology File

### 1.1 Locate the Ontology File

Open `gmn_ontology.ttl` in your text editor. This file contains all property and class definitions for the GMN ontology.

### 1.2 Find the Insertion Point

The property should be added in the name properties section, specifically between `P1_1_has_name` and `P1_3_has_patrilineal_name`. Look for this location:

```turtle
# Property: P1.1 has name
gmn:P1_1_has_name 
    a owl:DatatypeProperty ;
    ...
    gmn:hasImplicitType aat:300404650 .

# INSERT P1_2_has_name_from_source HERE

# Property: P1.3 has patrilineal name
gmn:P1_3_has_patrilineal_name 
    a owl:DatatypeProperty ;
    ...
```

### 1.3 Add the Property Definition

Insert the following TTL block at the identified location:

```turtle
# Property: P1.2 has name from source
gmn:P1_2_has_name_from_source 
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P1.2 has name from source"@en ;
    rdfs:comment "Simplified property for expressing the name of a person as found in historical sources. Represents the full CIDOC-CRM path: P1_is_identified_by > E41_Appellation > P2_has_type <http://vocab.getty.edu/aat/300456607> > P190_has_symbolic_content. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The appellation type is automatically set to AAT 300456607 (names found in historical sources)."@en ;
    rdfs:subPropertyOf cidoc:P1_is_identified_by ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E62_String ;
    dcterms:created "2025-10-26"^^xsd:date ;
    rdfs:seeAlso cidoc:P1_is_identified_by, cidoc:P190_has_symbolic_content, aat:300456607 ;
    owl:equivalentProperty [
        a owl:Restriction ;
        owl:onProperty cidoc:P1_is_identified_by ;
        owl:allValuesFrom [
            a owl:Restriction ;
            owl:onProperty cidoc:P190_has_symbolic_content ;
            owl:hasValue cidoc:E62_String
        ]
    ] ;
    gmn:hasImplicitType aat:300456607 .
```

### 1.4 Line-by-Line Explanation

**Line 1-2**: Property URI and declaration
```turtle
# Property: P1.2 has name from source
gmn:P1_2_has_name_from_source 
```
- Human-readable comment identifying the property
- Property URI using the GMN namespace

**Line 3-4**: Property types
```turtle
    a owl:DatatypeProperty ;
    a rdf:Property ;
```
- Declares this as an OWL datatype property (links to literal values)
- Also declares as an RDF property for compatibility

**Line 5**: Label
```turtle
    rdfs:label "P1.2 has name from source"@en ;
```
- Human-readable label in English
- Used in user interfaces and documentation

**Line 6**: Comment/Description
```turtle
    rdfs:comment "Simplified property for expressing the name of a person as found in historical sources. Represents the full CIDOC-CRM path: P1_is_identified_by > E41_Appellation > P2_has_type <http://vocab.getty.edu/aat/300456607> > P190_has_symbolic_content. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The appellation type is automatically set to AAT 300456607 (names found in historical sources)."@en ;
```
- Detailed description of the property's purpose
- Explains the CIDOC-CRM equivalence
- Notes automatic transformation behavior

**Line 7**: Subproperty relationship
```turtle
    rdfs:subPropertyOf cidoc:P1_is_identified_by ;
```
- Declares this property as a specialization of CIDOC-CRM's P1
- Enables reasoning and inference

**Line 8-9**: Domain and range
```turtle
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E62_String ;
```
- Domain: This property applies to persons (E21_Person)
- Range: The value is a string (E62_String)

**Line 10**: Creation date
```turtle
    dcterms:created "2025-10-26"^^xsd:date ;
```
- Documents when the property was added to the ontology
- Uses Dublin Core terms vocabulary

**Line 11**: Related properties
```turtle
    rdfs:seeAlso cidoc:P1_is_identified_by, cidoc:P190_has_symbolic_content, aat:300456607 ;
```
- Links to related CIDOC-CRM properties
- Links to the AAT term for reference

**Line 12-19**: OWL equivalence
```turtle
    owl:equivalentProperty [
        a owl:Restriction ;
        owl:onProperty cidoc:P1_is_identified_by ;
        owl:allValuesFrom [
            a owl:Restriction ;
            owl:onProperty cidoc:P190_has_symbolic_content ;
            owl:hasValue cidoc:E62_String
        ]
    ] ;
```
- Formal OWL definition of the equivalence to CIDOC-CRM structure
- Enables automated reasoning about property relationships

**Line 20**: Implicit type
```turtle
    gmn:hasImplicitType aat:300456607 .
```
- Specifies the AAT type automatically applied during transformation
- Custom GMN property for documenting transformation behavior

### 1.5 Save the Ontology File

After adding the property definition:

1. Save the file
2. Make a backup copy (recommended)
3. Commit to version control with a clear message: "Add P1_2_has_name_from_source property"

## Step 2: Update Transformation Script

### 2.1 Locate the Transformation Script

Open `gmn_to_cidoc_transform.py` in your text editor.

### 2.2 Verify Required Constants

Check that the AAT constant for names from sources is defined at the top of the file. Look for:

```python
AAT_NAME_FROM_SOURCE = "http://vocab.getty.edu/page/aat/300456607"
```

**Location**: Near the top of the file, with other AAT constants (around line 23).

**If missing**, add it alongside other AAT constants:

```python
AAT_NAME = "http://vocab.getty.edu/page/aat/300404650"
AAT_NAME_FROM_SOURCE = "http://vocab.getty.edu/page/aat/300456607"  # Add this line
AAT_PATRONYMIC = "http://vocab.getty.edu/page/aat/300404651"
```

### 2.3 Add the Transformation Function

Find the section with name transformation functions (around line 96-110). Add the new function:

```python
def transform_p1_2_has_name_from_source(data):
    """Transform gmn:P1_2_has_name_from_source to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_2_has_name_from_source', AAT_NAME_FROM_SOURCE)
```

**Placement**: Insert between `transform_p1_1_has_name` and `transform_p1_3_has_patrilineal_name`.

**Expected location**:
```python
def transform_p1_1_has_name(data):
    """Transform gmn:P1_1_has_name to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_1_has_name', AAT_NAME)


def transform_p1_2_has_name_from_source(data):  # NEW FUNCTION
    """Transform gmn:P1_2_has_name_from_source to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_2_has_name_from_source', AAT_NAME_FROM_SOURCE)


def transform_p1_3_has_patrilineal_name(data):
    """Transform gmn:P1_3_has_patrilineal_name to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_3_has_patrilineal_name', AAT_PATRONYMIC)
```

### 2.4 Function Explanation

**Function signature**:
```python
def transform_p1_2_has_name_from_source(data):
```
- Takes a data dictionary representing an item (typically a person)
- Returns the modified data dictionary

**Docstring**:
```python
    """Transform gmn:P1_2_has_name_from_source to full CIDOC-CRM structure."""
```
- Documents the function's purpose
- Follows Python documentation standards

**Implementation**:
```python
    return transform_name_property(data, 'gmn:P1_2_has_name_from_source', AAT_NAME_FROM_SOURCE)
```
- Delegates to the generic `transform_name_property` helper function
- Passes the property name to transform
- Passes the AAT type URI to apply

### 2.5 Integrate into Transformation Pipeline

Find the main transformation function (typically `transform_item` or similar) and add the call to the new function. Look for the section where other name properties are transformed:

```python
def transform_item(item):
    """Transform a single item from Omeka-S format to CIDOC-CRM."""
    # ... other transformations ...
    
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)  # ADD THIS LINE
    item = transform_p1_3_has_patrilineal_name(item)
    
    # ... more transformations ...
    return item
```

**Location**: Look for where other `transform_p1_*` functions are called (around line 2409).

### 2.6 Save the Script

After making changes:

1. Save the file
2. Make a backup copy (recommended)
3. Commit to version control: "Add transform_p1_2_has_name_from_source function"

## Step 3: Validate Changes

### 3.1 Validate Ontology Syntax

Use an RDF validator to check the TTL syntax:

```bash
# Using rapper (part of Raptor RDF Syntax Library)
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Using rdflib in Python
python -c "from rdflib import Graph; g = Graph(); g.parse('gmn_ontology.ttl', format='turtle'); print('Valid!')"
```

**Expected output**: No errors or "Valid!" message

**If errors occur**:
- Check for missing semicolons or periods
- Verify all URIs are properly formatted
- Ensure all prefixes are defined
- Check for unclosed quotes or brackets

### 3.2 Validate Python Syntax

Check the Python script for syntax errors:

```bash
# Basic syntax check
python -m py_compile gmn_to_cidoc_transform.py

# More thorough check with pylint (if installed)
pylint gmn_to_cidoc_transform.py
```

**Expected output**: No syntax errors

**If errors occur**:
- Check for proper indentation
- Verify function is properly defined
- Ensure all parentheses and brackets are balanced
- Check for typos in function or variable names

### 3.3 Validate Constant Definition

Verify the AAT constant is accessible:

```python
# In Python interactive shell or script
from gmn_to_cidoc_transform import AAT_NAME_FROM_SOURCE
print(AAT_NAME_FROM_SOURCE)
# Should output: http://vocab.getty.edu/page/aat/300456607
```

## Step 4: Test Implementation

### 4.1 Create Test Data

Create a test file `test_name_from_source.json` with sample data:

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/ontology/",
    "aat": "http://vocab.getty.edu/page/aat/"
  },
  "@id": "http://example.org/person/test_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_2_has_name_from_source": [
    {"@value": "Iohannes Spinula"},
    {"@value": "Iohanes de Spinola"}
  ]
}
```

### 4.2 Run Transformation Test

Create a test script `test_transform.py`:

```python
import json
from gmn_to_cidoc_transform import transform_p1_2_has_name_from_source

# Load test data
with open('test_name_from_source.json', 'r') as f:
    test_data = json.load(f)

print("Input data:")
print(json.dumps(test_data, indent=2))

# Transform
result = transform_p1_2_has_name_from_source(test_data)

print("\nOutput data:")
print(json.dumps(result, indent=2))

# Verify transformation
assert 'cidoc:P1_is_identified_by' in result, "P1_is_identified_by not found"
assert 'gmn:P1_2_has_name_from_source' not in result, "Original property not removed"
assert len(result['cidoc:P1_is_identified_by']) == 2, "Should have 2 appellations"

for app in result['cidoc:P1_is_identified_by']:
    assert app['@type'] == 'cidoc:E41_Appellation', "Wrong appellation type"
    assert 'cidoc:P2_has_type' in app, "Missing type link"
    assert app['cidoc:P2_has_type']['@id'] == 'http://vocab.getty.edu/page/aat/300456607', "Wrong AAT type"
    assert 'cidoc:P190_has_symbolic_content' in app, "Missing name content"

print("\nAll tests passed!")
```

Run the test:

```bash
python test_transform.py
```

### 4.3 Expected Output

The test should produce output like:

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/ontology/",
    "aat": "http://vocab.getty.edu/page/aat/"
  },
  "@id": "http://example.org/person/test_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://example.org/appellation/...",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300456607",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Iohannes Spinula"
    },
    {
      "@id": "http://example.org/appellation/...",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300456607",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Iohanes de Spinola"
    }
  ]
}
```

### 4.4 Validate Output Structure

Check that the output meets requirements:

- [ ] Original property `gmn:P1_2_has_name_from_source` is removed
- [ ] `cidoc:P1_is_identified_by` array is present
- [ ] Each appellation has `@type` = `cidoc:E41_Appellation`
- [ ] Each appellation has `cidoc:P2_has_type` with AAT 300456607
- [ ] Each appellation has `cidoc:P190_has_symbolic_content` with the name
- [ ] Appellation URIs are unique and valid

### 4.5 Test Edge Cases

Create additional tests for edge cases:

```python
# Test: Empty name
test_empty = {
    "@id": "person/test",
    "@type": "cidoc:E21_Person",
    "gmn:P1_2_has_name_from_source": [{"@value": ""}]
}

# Test: Special characters
test_special = {
    "@id": "person/test",
    "@type": "cidoc:E21_Person",
    "gmn:P1_2_has_name_from_source": [{"@value": "Iohannes q. Petri de Nigro"}]
}

# Test: Unicode characters
test_unicode = {
    "@id": "person/test",
    "@type": "cidoc:E21_Person",
    "gmn:P1_2_has_name_from_source": [{"@value": "João de Évora"}]
}

# Test: Mixed with other properties
test_mixed = {
    "@id": "person/test",
    "@type": "cidoc:E21_Person",
    "gmn:P1_1_has_name": [{"@value": "John Spinola"}],
    "gmn:P1_2_has_name_from_source": [{"@value": "Iohannes Spinula"}],
    "gmn:P1_3_has_patrilineal_name": [{"@value": "Iohannes Spinula q. Antonii"}]
}
```

Run each test and verify correct behavior.

## Step 5: Deploy to Production

### 5.1 Pre-Deployment Checklist

Before deploying to production:

- [ ] All tests pass successfully
- [ ] Ontology validates without errors
- [ ] Python script has no syntax errors
- [ ] Documentation is updated
- [ ] Changes are committed to version control
- [ ] Backup of current production files created

### 5.2 Deployment Steps

1. **Create backup**:
```bash
cp gmn_ontology.ttl gmn_ontology.ttl.backup.$(date +%Y%m%d)
cp gmn_to_cidoc_transform.py gmn_to_cidoc_transform.py.backup.$(date +%Y%m%d)
```

2. **Deploy ontology file**:
```bash
# Copy to production location
cp gmn_ontology.ttl /path/to/production/gmn_ontology.ttl
```

3. **Deploy transformation script**:
```bash
# Copy to production location
cp gmn_to_cidoc_transform.py /path/to/production/gmn_to_cidoc_transform.py
```

4. **Restart services** (if applicable):
```bash
# Restart Omeka-S or transformation service
sudo systemctl restart omeka-s
# Or restart transformation service
sudo systemctl restart gmn-transform-service
```

### 5.3 Post-Deployment Validation

After deployment:

1. **Verify ontology is accessible**:
   - Check that Omeka-S can load the ontology
   - Verify the property appears in resource templates

2. **Test with real data**:
   - Create a test person record in Omeka-S
   - Add a name using `gmn:P1_2_has_name_from_source`
   - Run transformation pipeline
   - Verify output is correct

3. **Monitor for errors**:
   - Check application logs
   - Watch for transformation errors
   - Monitor user feedback

### 5.4 Update Omeka-S Resource Templates

If using Omeka-S, update resource templates to include the new property:

1. Log in to Omeka-S admin interface
2. Navigate to Resource Templates
3. Edit the "Person" template (or relevant template)
4. Add property: `gmn:P1_2_has_name_from_source`
5. Configure property settings:
   - Label: "Name from Source"
   - Data type: Text
   - Description: "Name of person as found in historical source documents"
6. Save template

### 5.5 User Training

Provide guidance to data entry users:

1. Distribute documentation
2. Provide example records
3. Demonstrate proper usage
4. Clarify distinction from `P1_1_has_name`
5. Answer questions

## Troubleshooting

### Issue: Ontology Won't Load

**Symptoms**:
- RDF parser reports errors
- Omeka-S can't load the ontology
- Validation tools report syntax errors

**Solutions**:
1. Check for missing or extra semicolons
2. Verify all prefixes are defined
3. Ensure URIs are properly formatted
4. Look for unclosed quotes or brackets
5. Use an RDF validator with detailed error messages

### Issue: Transformation Not Working

**Symptoms**:
- Property not being transformed
- Original property remains in output
- No E41_Appellation structures created

**Solutions**:
1. Verify function is being called in transformation pipeline
2. Check that constant `AAT_NAME_FROM_SOURCE` is defined
3. Ensure property name in function matches ontology
4. Verify `transform_name_property` function exists and works
5. Check input data format is correct

### Issue: Wrong AAT Type Applied

**Symptoms**:
- E41_Appellation has wrong P2_has_type value
- Type is 300404650 instead of 300456607

**Solutions**:
1. Verify `AAT_NAME_FROM_SOURCE` constant value
2. Check that correct constant is passed to `transform_name_property`
3. Ensure no other code is overwriting the type
4. Verify AAT URI format is correct

### Issue: Invalid URIs Generated

**Symptoms**:
- Appellation URIs cause errors
- RDF validation fails on URI format
- URIs contain invalid characters

**Solutions**:
1. Check `generate_appellation_uri` function
2. Verify URI encoding for special characters
3. Test with various character sets (ASCII, Unicode)
4. Ensure base URI is properly configured
5. Check for proper URL encoding of spaces and special chars

### Issue: Duplicate Appellations

**Symptoms**:
- Multiple identical E41_Appellation instances created
- Same name appears multiple times with different URIs

**Solutions**:
1. Check if transformation is being called multiple times
2. Verify data doesn't already have appellations
3. Check URI generation for uniqueness
4. Ensure deduplication logic (if any) is working

## Verification Checklist

After implementation, verify the following:

### Ontology File

- [ ] Property definition is present in `gmn_ontology.ttl`
- [ ] Property has correct namespace (gmn:)
- [ ] Property has correct URI (P1_2_has_name_from_source)
- [ ] Property type is `owl:DatatypeProperty`
- [ ] Domain is `cidoc:E21_Person`
- [ ] Range is `cidoc:E62_String`
- [ ] Label is present and correct
- [ ] Comment describes purpose clearly
- [ ] `rdfs:subPropertyOf cidoc:P1_is_identified_by` is present
- [ ] `dcterms:created` has correct date
- [ ] `rdfs:seeAlso` references relevant terms
- [ ] `owl:equivalentProperty` structure is correct
- [ ] `gmn:hasImplicitType` is aat:300456607
- [ ] TTL syntax validates without errors

### Transformation Script

- [ ] `AAT_NAME_FROM_SOURCE` constant is defined
- [ ] Constant value is "http://vocab.getty.edu/page/aat/300456607"
- [ ] `transform_p1_2_has_name_from_source` function exists
- [ ] Function has proper docstring
- [ ] Function calls `transform_name_property` correctly
- [ ] Function passes correct property name
- [ ] Function passes correct AAT type
- [ ] Function is called in main transformation pipeline
- [ ] Function is called in correct order (after P1_1, before P1_3)
- [ ] Python syntax validates without errors

### Testing

- [ ] Unit tests pass for single name
- [ ] Unit tests pass for multiple names
- [ ] Edge cases handled correctly (empty, special chars, unicode)
- [ ] Integration test with full pipeline succeeds
- [ ] Output structure is valid CIDOC-CRM
- [ ] Original property is removed after transformation
- [ ] E41_Appellation structures are created correctly
- [ ] P2_has_type links to correct AAT term
- [ ] P190_has_symbolic_content contains name value
- [ ] Appellation URIs are unique and valid

### Documentation

- [ ] README.md is updated
- [ ] Property appears in property listing
- [ ] Examples demonstrate usage
- [ ] Transformation explained
- [ ] User guide updated (if applicable)

### Deployment

- [ ] Backups created before deployment
- [ ] Files deployed to production
- [ ] Services restarted (if needed)
- [ ] Post-deployment tests pass
- [ ] Omeka-S recognizes property
- [ ] Resource templates updated
- [ ] Users notified of new property

## Next Steps

After successful implementation:

1. **Monitor Usage**: Track how the property is being used in production
2. **Collect Feedback**: Gather user experiences and suggestions
3. **Document Examples**: Create real-world examples from actual data
4. **Train Users**: Provide ongoing support and training
5. **Iterate**: Make improvements based on feedback and usage patterns

## Support

For additional help:

- Review the complete semantic documentation in `has-name-from-source-documentation.md`
- Check code examples in `has-name-from-source-transform.py`
- Consult TTL definitions in `has-name-from-source-ontology.ttl`
- Contact the GMN ontology maintainer with questions

---

**Implementation complete!** Remember to update documentation and notify users of the new property availability.
