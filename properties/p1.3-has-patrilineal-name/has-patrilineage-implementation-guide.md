# P1.3 Has Patrilineal Name - Implementation Guide

## Introduction

This guide provides step-by-step instructions for implementing the `gmn:P1_3_has_patrilineal_name` property in your Genoese Merchant Networks (GMN) ontology and transformation system. The implementation is already complete in the project files, but this guide documents the process for reference, validation, or replication.

## Prerequisites

Before beginning implementation, ensure you have:

- Access to the GMN ontology file (`gmn_ontology.ttl`)
- Access to the transformation script (`gmn_to_cidoc_transform.py`)
- Python 3.x environment with required dependencies
- RDF validation tools (optional but recommended)
- Understanding of CIDOC-CRM and Turtle/RDF syntax

## Implementation Overview

The implementation consists of three main components:

1. **Ontology Definition**: Add the property definition to the TTL file
2. **Transformation Function**: Add Python code to transform the shortcut to full CIDOC-CRM
3. **Integration**: Connect the transformation function to the main processing pipeline

## Step-by-Step Implementation

### Step 1: Add Property Definition to Ontology

**File**: `gmn_ontology.ttl`  
**Location**: After other P1.x properties (around line 187-208)

#### 1.1 Open the Ontology File

```bash
# Navigate to the ontology file
cd /path/to/project
nano gmn_ontology.ttl
```

#### 1.2 Locate the Insertion Point

Find the section with other name properties (P1.1, P1.2, etc.). The property should be added after `P1_2_has_name_from_source` and before `P1_4_has_loconym`.

#### 1.3 Add the Property Definition

Insert the following TTL code:

```turtle
# Property: P1.3 has patrilineal name
gmn:P1_3_has_patrilineal_name 
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P1.3 has patrilineal name"@en ;
    rdfs:comment "Simplified property for expressing the patrilineal name of a person, which includes their given name followed by their patronymic ancestry (e.g., 'Giacomo Spinola q. Antonio' meaning 'Giacomo Spinola, son of the late Antonio'). This naming pattern is common in medieval and early modern Italian contexts where 'q.' (quondam) indicates a deceased father or ancestor. Represents the full CIDOC-CRM path: P1_is_identified_by > E41_Appellation > P2_has_type <http://vocab.getty.edu/aat/300404651> > P190_has_symbolic_content. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The appellation type is automatically set to AAT 300404651 (patronymics)."@en ;
    rdfs:subPropertyOf cidoc:P1_is_identified_by ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E62_String ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P1_is_identified_by, cidoc:P190_has_symbolic_content, aat:300404651 ;
    owl:equivalentProperty [
        a owl:Restriction ;
        owl:onProperty cidoc:P1_is_identified_by ;
        owl:allValuesFrom [
            a owl:Restriction ;
            owl:onProperty cidoc:P190_has_symbolic_content ;
            owl:hasValue cidoc:E62_String
        ]
    ] ;
    gmn:hasImplicitType aat:300404651 .
```

#### 1.4 Validate the Syntax

```bash
# Use rapper or another RDF validator
rapper -i turtle gmn_ontology.ttl > /dev/null
```

If there are no errors, the syntax is valid.

### Step 2: Add AAT Constant (if not already present)

**File**: `gmn_to_cidoc_transform.py`  
**Location**: Near the top of the file with other constants (around line 24)

#### 2.1 Check for Existing Constant

Search for the AAT_PATRONYMIC constant:

```bash
grep "AAT_PATRONYMIC" gmn_to_cidoc_transform.py
```

#### 2.2 Add Constant if Missing

If the constant doesn't exist, add it near other AAT constants:

```python
# AAT Type URIs
AAT_PATRONYMIC = "http://vocab.getty.edu/page/aat/300404651"
```

### Step 3: Implement Transformation Function

**File**: `gmn_to_cidoc_transform.py`  
**Location**: After other name transformation functions (around line 106-108)

#### 3.1 Add the Transformation Function

Insert the following code:

```python
def transform_p1_3_has_patrilineal_name(data):
    """Transform gmn:P1_3_has_patrilineal_name to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_3_has_patrilineal_name', AAT_PATRONYMIC)
```

**Note**: This function leverages the existing `transform_name_property` helper function, which handles the generic name transformation pattern.

#### 3.2 Verify Helper Function Exists

Ensure the `transform_name_property` function exists in the file:

```bash
grep "def transform_name_property" gmn_to_cidoc_transform.py
```

This function should exist around line 48-93 and handles the generic transformation logic for all name properties.

### Step 4: Integrate into Processing Pipeline

**File**: `gmn_to_cidoc_transform.py`  
**Location**: Main processing function (around line 2410)

#### 4.1 Find the Main Processing Loop

Locate the main function where all transformations are applied to each item. This is typically in a function that processes JSON-LD data.

#### 4.2 Add Function Call

Insert the transformation call in the appropriate location:

```python
# Transform P1.3 has patrilineal name
item = transform_p1_3_has_patrilineal_name(item)
```

**Best Practice**: Place this call with other P1.x name transformations to keep related functions together.

### Step 5: Testing the Implementation

#### 5.1 Create Test Data

Create a test file `test_patrilineal.json` with sample data:

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "https://genoese-merchants.org/ontology#"
  },
  "@graph": [
    {
      "@id": "https://example.org/person/giacomo_spinola",
      "@type": "cidoc:E21_Person",
      "gmn:P1_3_has_patrilineal_name": [
        {
          "@value": "Giacomo Spinola q. Antonio"
        }
      ]
    }
  ]
}
```

#### 5.2 Run the Transformation

```python
# In Python interpreter or test script
import json
from gmn_to_cidoc_transform import transform_p1_3_has_patrilineal_name

# Load test data
with open('test_patrilineal.json', 'r') as f:
    data = json.load(f)

# Transform
for item in data['@graph']:
    item = transform_p1_3_has_patrilineal_name(item)

# Print result
print(json.dumps(data, indent=2))
```

#### 5.3 Verify Expected Output

The output should include:

```json
{
  "@id": "https://example.org/person/giacomo_spinola",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "https://example.org/person/giacomo_spinola/appellation/patrilineal/...",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Giacomo Spinola q. Antonio"
    }
  ]
}
```

### Step 6: Validation Testing

#### 6.1 Test Multiple Names

Test with a person having multiple types of names:

```json
{
  "@id": "https://example.org/person/giovanni_doria",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [{"@value": "Giovanni Doria"}],
  "gmn:P1_3_has_patrilineal_name": [{"@value": "Giovanni Doria q. Luca"}],
  "gmn:P1_4_has_loconym": [{"@id": "https://example.org/place/genoa"}]
}
```

Verify that all three properties transform correctly and create separate appellations.

#### 6.2 Test Edge Cases

**Empty String**:
```json
{
  "gmn:P1_3_has_patrilineal_name": [{"@value": ""}]
}
```
Should be handled gracefully (no appellation created).

**Special Characters**:
```json
{
  "gmn:P1_3_has_patrilineal_name": [{"@value": "Bartolomeo de' Medici q. Lorenzo"}]
}
```
Should preserve special characters like apostrophes.

**Multiple Patronymics**:
```json
{
  "gmn:P1_3_has_patrilineal_name": [
    {"@value": "Giovanni q. Antonio"},
    {"@value": "Giovanni q. Marco"}
  ]
}
```
Should create two separate appellations.

#### 6.3 CIDOC-CRM Validation

Validate the output against CIDOC-CRM specifications:

1. **Property Path**: Verify `P1_is_identified_by` → `E41_Appellation` structure
2. **Type Assignment**: Verify `P2_has_type` points to AAT:300404651
3. **Content**: Verify `P190_has_symbolic_content` contains the original string

### Step 7: Integration Testing

#### 7.1 Full Pipeline Test

Run the entire transformation pipeline with real data:

```bash
python gmn_to_cidoc_transform.py input_file.json output_file.json
```

#### 7.2 Check Log Output

Review logs for any warnings or errors related to the patrilineal property.

#### 7.3 Sample Data Validation

Process a sample of production data and manually verify several records.

### Step 8: Omeka-S Configuration

#### 8.1 Update Resource Templates

If using Omeka-S for data entry:

1. Log in to Omeka-S admin interface
2. Navigate to Resource Templates
3. Edit the "Person" resource template
4. Add the `gmn:P1_3_has_patrilineal_name` property
5. Set appropriate data entry guidance
6. Save the template

#### 8.2 Configure Property Settings

- **Label**: "Patrilineal Name"
- **Description**: "Full name including patronymic (e.g., 'Giacomo Spinola q. Antonio')"
- **Required**: No
- **Multiple Values**: Yes
- **Data Type**: Text (literal)

### Step 9: Documentation Updates

#### 9.1 Update User Guide

Add examples to your user documentation showing:
- When to use this property
- How to format patrilineal names
- Common patterns (q., quondam, etc.)

#### 9.2 Add to Data Entry Manual

Include:
- Definition of patronymic naming
- Examples from historical sources
- Guidelines for handling variations
- Instructions for edge cases

### Step 10: Deployment

#### 10.1 Version Control

```bash
git add gmn_ontology.ttl gmn_to_cidoc_transform.py
git commit -m "Add P1_3_has_patrilineal_name property and transformation"
git push origin main
```

#### 10.2 Deploy to Production

Follow your standard deployment procedures:
1. Deploy updated ontology file
2. Deploy updated transformation script
3. Restart any running services
4. Monitor logs for issues

#### 10.3 Notify Stakeholders

Inform relevant parties:
- Data entry personnel
- System administrators
- End users accessing the data

## Troubleshooting

### Issue: Property Not Found During Transformation

**Symptoms**: Property value not being transformed  
**Cause**: Property name mismatch  
**Solution**: 
```python
# Verify exact property name in data
print(data.keys())
# Ensure it matches 'gmn:P1_3_has_patrilineal_name' exactly
```

### Issue: AAT URI Not Resolving

**Symptoms**: Type URI appears broken in output  
**Cause**: Constant not defined or incorrect URI  
**Solution**:
```python
# Verify constant
print(AAT_PATRONYMIC)
# Should output: "http://vocab.getty.edu/page/aat/300404651"
```

### Issue: Multiple Appellations Conflicting

**Symptoms**: Person has too many appellations  
**Cause**: This is expected behavior  
**Solution**: A person can have multiple appellations of different types. Each type (name, patronymic, loconym) should create a separate appellation.

### Issue: Special Characters Not Preserved

**Symptoms**: Apostrophes or accents lost  
**Cause**: Encoding issue  
**Solution**: Ensure UTF-8 encoding throughout pipeline:
```python
with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### Issue: Transformation Function Not Called

**Symptoms**: Shortcut property remains in output  
**Cause**: Function not integrated into pipeline  
**Solution**: Verify function is called in main processing loop:
```python
# Add to main loop
item = transform_p1_3_has_patrilineal_name(item)
```

## Performance Considerations

### Optimization Tips

1. **Batch Processing**: Process large datasets in batches
2. **Caching**: Cache AAT URIs to avoid repeated string operations
3. **Validation**: Validate input data before transformation to catch errors early

### Expected Performance

- **Small datasets** (<1000 records): Near-instantaneous
- **Medium datasets** (1000-10000 records): Seconds to minutes
- **Large datasets** (>10000 records): Minutes to hours depending on complexity

## Best Practices

### Data Entry Guidelines

1. **Consistency**: Use consistent formatting (e.g., always use "q." for quondam)
2. **Completeness**: Include as much patronymic information as available in source
3. **Clarity**: Preserve original spelling and orthography from historical sources
4. **Context**: Add additional name properties (P1.1, P1.2) as needed

### Code Maintenance

1. **Comments**: Document any modifications to transformation logic
2. **Testing**: Add unit tests for edge cases
3. **Versioning**: Track changes in version control
4. **Review**: Periodically review transformation output for quality

## Additional Resources

### Documentation

- **CIDOC-CRM Specification**: http://www.cidoc-crm.org/
- **Getty AAT Entry for Patronymics**: http://vocab.getty.edu/page/aat/300404651
- **RDF/OWL Tutorial**: https://www.w3.org/TR/owl-primer/

### Tools

- **RDF Validators**: 
  - Rapper: http://librdf.org/raptor/rapper.html
  - RDF Validator: https://www.w3.org/RDF/Validator/
- **Python RDF Libraries**:
  - rdflib: https://rdflib.readthedocs.io/
  - pyld: https://github.com/digitalbazaar/pyld

### Support

For technical support:
1. Check existing documentation
2. Review error logs
3. Consult with ontology maintainer
4. Contact system administrator

## Summary Checklist

Use this checklist to verify complete implementation:

- [ ] Property definition added to ontology TTL file
- [ ] AAT constant defined in Python script
- [ ] Transformation function implemented
- [ ] Function integrated into processing pipeline
- [ ] Test data created and tested
- [ ] Edge cases validated
- [ ] Full pipeline tested with production data
- [ ] Omeka-S templates updated (if applicable)
- [ ] User documentation updated
- [ ] Changes committed to version control
- [ ] Deployment completed
- [ ] Stakeholders notified

## Conclusion

The `gmn:P1_3_has_patrilineal_name` property implementation follows established patterns in the GMN ontology and provides a user-friendly way to capture important historical naming conventions. By following this guide, you can ensure proper implementation, testing, and deployment of this property in your system.

For questions or issues not covered in this guide, consult the main project documentation or contact the ontology maintainer.

---

**Implementation Guide Version**: 1.0  
**Last Updated**: 2025-10-26  
**Property**: gmn:P1_3_has_patrilineal_name
