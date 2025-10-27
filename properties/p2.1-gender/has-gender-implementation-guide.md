# Has Sex/Gender Property Implementation Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Ontology Review](#ontology-review)
4. [Transformation Implementation](#transformation-implementation)
5. [Testing Procedures](#testing-procedures)
6. [Integration Verification](#integration-verification)
7. [Documentation Updates](#documentation-updates)
8. [Deployment](#deployment)

---

## Introduction

This guide provides step-by-step instructions for implementing the **gmn:P2_1_gender** property transformation in the GMN to CIDOC-CRM conversion system. The property records biological sex characteristics of persons using a controlled vocabulary of Getty AAT terms.

### Implementation Overview

**What's Already Done**:
- ✅ Property defined in ontology (gmn_ontology.ttl, line 223)
- ✅ Controlled vocabulary established (three AAT terms)
- ✅ CIDOC-CRM alignment specified

**What You'll Implement**:
- ⚠️ Transformation function (Python code)
- ⚠️ Integration into main transformation pipeline
- ⚠️ Testing and validation

**Time Required**: 30-40 minutes

---

## Prerequisites

### Required Knowledge
- Basic understanding of RDF/OWL
- Python 3.x proficiency
- Familiarity with JSON-LD format
- Understanding of CIDOC-CRM E21_Person and P2_has_type

### Required Files
- `gmn_ontology.ttl` (contains property definition)
- `gmn_to_cidoc_transform.py` (transformation script to modify)
- Test JSON-LD files with person data

### Development Environment
- Python 3.x installed
- Text editor or IDE
- Access to ontology and transformation script files
- Command line terminal

---

## Ontology Review

### Step 1: Verify Property Definition

The gmn:P2_1_gender property should already exist in your ontology file.

**Location**: `gmn_ontology.ttl`, line 223

**Verification Command**:
```bash
grep -A 17 "gmn:P2_1_gender" gmn_ontology.ttl
```

**Expected Output**:
```turtle
gmn:P2_1_gender
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P2.1 has sex/gender"@en ;
    rdfs:comment "Simplified property for expressing biological characteristics and physiological traits that distinguish the males and females of a species. This is an extension of the CIDOC-CRM path: E21_Person > P2_has_type > E55_Type. The range is restricted to a controlled vocabulary of three Getty AAT terms: male (300189559), female (300189557), and intersex (300417544)."@en ;
    rdfs:subPropertyOf cidoc:P2_has_type ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range [
        a owl:Class ;
        owl:oneOf (
            aat:300189559  # male
            aat:300189557  # female
            aat:300417544  # intersex
        )
    ] ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P2_has_type, aat:300189559, aat:300189557, aat:300417544 .
```

### Step 2: Understand the Controlled Vocabulary

The property uses three Getty AAT terms:

| Value | AAT URI | Description |
|-------|---------|-------------|
| Male | `http://vocab.getty.edu/page/aat/300189559` | Male biological sex |
| Female | `http://vocab.getty.edu/page/aat/300189557` | Female biological sex |
| Intersex | `http://vocab.getty.edu/page/aat/300417544` | Intersex biological characteristics |

**Validation**:
```bash
# Verify AAT URIs in ontology
grep -E "aat:300189559|aat:300189557|aat:300417544" gmn_ontology.ttl
```

### Step 3: Understand CIDOC-CRM Alignment

**Simplified GMN Pattern**:
```
E21_Person --gmn:P2_1_gender--> E55_Type (AAT term)
```

**Full CIDOC-CRM Pattern**:
```
E21_Person --P2_has_type--> E55_Type (AAT term)
```

**Note**: The transformation is straightforward since gmn:P2_1_gender is a subproperty of P2_has_type.

---

## Transformation Implementation

### Step 1: Locate Insertion Point

Open `gmn_to_cidoc_transform.py` and locate the `transform_item` function.

**Find the function**:
```bash
grep -n "^def transform_item" gmn_to_cidoc_transform.py
```

**Expected output**: `2395:def transform_item(item, include_internal=False):`

### Step 2: Create the Transformation Function

Add the following function **after line 2486** (after the group membership transformations and before the editorial notes transformation).

**Code to Add**:

```python
def transform_p2_1_gender(data):
    """
    Transform gmn:P2_1_gender to full CIDOC-CRM structure.
    
    Converts:
        gmn:P2_1_gender → cidoc:P2_has_type
    
    The gmn:P2_1_gender property is a simplified way to record biological sex
    characteristics using a controlled vocabulary of three Getty AAT terms:
    - aat:300189559 (male)
    - aat:300189557 (female) 
    - aat:300417544 (intersex)
    
    This function transforms it to the standard CIDOC-CRM P2_has_type pattern
    with proper E55_Type instances.
    
    Args:
        data: Item data dictionary
        
    Returns:
        Transformed data dictionary
    """
    if 'gmn:P2_1_gender' not in data:
        return data
    
    gender = data['gmn:P2_1_gender']
    
    # Handle both string and object formats
    if isinstance(gender, str):
        gender_uri = gender
    elif isinstance(gender, dict) and '@id' in gender:
        gender_uri = gender['@id']
    else:
        # Invalid format, skip transformation
        return data
    
    # Create the P2_has_type structure with E55_Type
    gender_type = {
        '@id': gender_uri,
        '@type': 'cidoc:E55_Type'
    }
    
    # Initialize cidoc:P2_has_type if it doesn't exist
    if 'cidoc:P2_has_type' not in data:
        data['cidoc:P2_has_type'] = []
    elif not isinstance(data['cidoc:P2_has_type'], list):
        data['cidoc:P2_has_type'] = [data['cidoc:P2_has_type']]
    
    # Add the gender type
    data['cidoc:P2_has_type'].append(gender_type)
    
    # Remove the simplified property
    del data['gmn:P2_1_gender']
    
    return data
```

**Insertion Location**:
```python
# In transform_item function, after line 2486:
    # Group memberships
    item = transform_p107i_1_has_regional_provenance(item)
    item = transform_p107i_2_has_social_category(item)
    item = transform_p107i_3_has_occupation(item)
    
    # Gender (ADD THIS LINE)
    item = transform_p2_1_gender(item)
    
    # Editorial notes (last, with optional inclusion)
    item = transform_p3_1_has_editorial_note(item, include_internal)
```

### Step 3: Integrate into Transform Pipeline

Add the function call in the `transform_item` function after the group membership transformations.

**Location**: After line 2486, before line 2488

**Code to Add**:
```python
    # Gender
    item = transform_p2_1_gender(item)
```

**Complete Context**:
```python
def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    ...
    """
    # ... [earlier transformations] ...
    
    # Group memberships
    item = transform_p107i_1_has_regional_provenance(item)
    item = transform_p107i_2_has_social_category(item)
    item = transform_p107i_3_has_occupation(item)
    
    # Gender
    item = transform_p2_1_gender(item)
    
    # Editorial notes (last, with optional inclusion)
    item = transform_p3_1_has_editorial_note(item, include_internal)
    
    return item
```

### Step 4: Verify Code Syntax

**Check for syntax errors**:
```bash
python -m py_compile gmn_to_cidoc_transform.py
```

**Expected output**: No output (means no syntax errors)

**If errors occur**: Review the code carefully, checking:
- Proper indentation (4 spaces)
- Matching quotes and brackets
- Correct function placement

---

## Testing Procedures

### Test Case 1: Male Gender

**Input JSON-LD**:
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "https://data.geniza.org/ontology/",
    "aat": "http://vocab.getty.edu/page/aat/"
  },
  "@id": "person/p001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Abraham ben Moses",
  "gmn:P2_1_gender": {
    "@id": "aat:300189559"
  }
}
```

**Expected Output**:
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "https://data.geniza.org/ontology/",
    "aat": "http://vocab.getty.edu/page/aat/"
  },
  "@id": "person/p001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "person/p001/appellation/name",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "aat:300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Abraham ben Moses"
    }
  ],
  "cidoc:P2_has_type": [
    {
      "@id": "aat:300189559",
      "@type": "cidoc:E55_Type"
    }
  ]
}
```

**Verification Steps**:
1. `gmn:P2_1_gender` property is removed
2. `cidoc:P2_has_type` array is created
3. Gender type has `@type: "cidoc:E55_Type"`
4. Gender URI is preserved correctly

### Test Case 2: Female Gender

**Input JSON-LD**:
```json
{
  "@id": "person/p002",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Esther bat David",
  "gmn:P2_1_gender": {
    "@id": "aat:300189557"
  }
}
```

**Expected Output**:
```json
{
  "@id": "person/p002",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "person/p002/appellation/name",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "aat:300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Esther bat David"
    }
  ],
  "cidoc:P2_has_type": [
    {
      "@id": "aat:300189557",
      "@type": "cidoc:E55_Type"
    }
  ]
}
```

### Test Case 3: Intersex

**Input JSON-LD**:
```json
{
  "@id": "person/p003",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Person Name",
  "gmn:P2_1_gender": {
    "@id": "aat:300417544"
  }
}
```

**Expected Output**:
```json
{
  "@id": "person/p003",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "person/p003/appellation/name",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "aat:300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Person Name"
    }
  ],
  "cidoc:P2_has_type": [
    {
      "@id": "aat:300417544",
      "@type": "cidoc:E55_Type"
    }
  ]
}
```

### Test Case 4: Missing Gender (No Property)

**Input JSON-LD**:
```json
{
  "@id": "person/p004",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Unknown Person"
}
```

**Expected Output**:
```json
{
  "@id": "person/p004",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "person/p004/appellation/name",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "aat:300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Unknown Person"
    }
  ]
}
```

**Verification**: No `cidoc:P2_has_type` property should be present (unless other types exist)

### Test Case 5: Person with Multiple Types

**Input JSON-LD**:
```json
{
  "@id": "person/p005",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Scholar Name",
  "gmn:P2_1_gender": {
    "@id": "aat:300189559"
  },
  "gmn:P107i_3_has_occupation": "scholar"
}
```

**Expected Output**: Should have both gender type and occupation type in `cidoc:P2_has_type` array

### Running Tests

**Create test file**: `test_gender_input.json`
```json
[
  {
    "@id": "person/p001",
    "@type": "cidoc:E21_Person",
    "gmn:P1_1_has_name": "Abraham ben Moses",
    "gmn:P2_1_gender": {"@id": "aat:300189559"}
  },
  {
    "@id": "person/p002",
    "@type": "cidoc:E21_Person",
    "gmn:P1_1_has_name": "Esther bat David",
    "gmn:P2_1_gender": {"@id": "aat:300189557"}
  },
  {
    "@id": "person/p003",
    "@type": "cidoc:E21_Person",
    "gmn:P1_1_has_name": "Person Name",
    "gmn:P2_1_gender": {"@id": "aat:300417544"}
  },
  {
    "@id": "person/p004",
    "@type": "cidoc:E21_Person",
    "gmn:P1_1_has_name": "Unknown Person"
  }
]
```

**Run transformation**:
```bash
python gmn_to_cidoc_transform.py test_gender_input.json test_gender_output.json
```

**Verify output**:
```bash
# Check that gender types are present
grep -c "P2_has_type" test_gender_output.json

# View formatted output
python -m json.tool test_gender_output.json | less
```

---

## Integration Verification

### Step 1: Verify Function Placement

**Check that the function exists**:
```bash
grep -n "def transform_p2_1_gender" gmn_to_cidoc_transform.py
```

**Expected**: Should show line number where function is defined

### Step 2: Verify Function Call

**Check that the function is called**:
```bash
grep -n "transform_p2_1_gender(item)" gmn_to_cidoc_transform.py
```

**Expected**: Should show line number in `transform_item` function (around line 2488)

### Step 3: Verify Transformation Order

The gender transformation should occur after group memberships but before editorial notes:

```bash
grep -B 3 -A 1 "transform_p2_1_gender" gmn_to_cidoc_transform.py
```

**Expected output**:
```python
    item = transform_p107i_3_has_occupation(item)
    
    # Gender
    item = transform_p2_1_gender(item)
    
    # Editorial notes
```

### Step 4: Test with Real Data

**Run on actual project data**:
```bash
# Backup your data first!
cp your_real_data.json your_real_data_backup.json

# Run transformation
python gmn_to_cidoc_transform.py your_real_data.json output_with_gender.json

# Check for errors
echo $?  # Should output 0 for success
```

---

## Documentation Updates

### Step 1: Update Project Documentation

Add the following section to your main project documentation file:

**Section Title**: "Recording Person Gender"

**Content** (copy from `has-gender-doc-note.txt`):

```markdown
## Recording Person Gender

The GMN ontology provides a standardized way to record biological sex characteristics of persons using the `gmn:P2_1_gender` property.

### Property Details

- **Property**: gmn:P2_1_gender
- **Label**: "P2.1 has sex/gender"
- **Domain**: E21_Person
- **Range**: Controlled vocabulary (three AAT terms)

### Allowed Values

| Term | AAT URI | Description |
|------|---------|-------------|
| Male | aat:300189559 | Male biological sex |
| Female | aat:300189557 | Female biological sex |
| Intersex | aat:300417544 | Intersex biological characteristics |

### Usage Example

```json
{
  "@id": "person/p123",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Person Name",
  "gmn:P2_1_gender": {
    "@id": "aat:300189559"
  }
}
```

### Best Practices

1. **Use AAT URIs**: Always use the full Getty AAT URI, not text labels
2. **Document evidence**: Record gender only when supported by historical documents
3. **Avoid inference**: Don't infer gender from names or roles alone
4. **Optional property**: Not all persons require gender information
5. **Privacy considerations**: Be sensitive to historical and cultural contexts
```

### Step 2: Update Change Log

Add entry to your project change log:

```markdown
### 2025-10-26
- Implemented transformation for gmn:P2_1_gender property
- Added transform_p2_1_gender() function to convert simplified gender property to CIDOC-CRM P2_has_type structure
- Gender values now properly transform to E55_Type instances
- Supports three Getty AAT terms: male (300189559), female (300189557), intersex (300417544)
```

### Step 3: Update README or User Guide

Add to the list of supported properties:

```markdown
#### Person Properties

- `gmn:P1_1_has_name`: Person's name
- `gmn:P1_2_has_name_from_source`: Name as it appears in source
- `gmn:P1_3_has_patrilineal_name`: Patronymic or family name
- `gmn:P2_1_gender`: Biological sex (controlled vocabulary) ← NEW
- `gmn:P11i_1_earliest_attestation_date`: First historical appearance
- `gmn:P11i_2_latest_attestation_date`: Last historical appearance
- ... [other properties]
```

---

## Deployment

### Step 1: Pre-Deployment Checklist

- [ ] All tests pass successfully
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Backup of original files created
- [ ] Team notified of changes

### Step 2: Version Control

**Commit changes**:
```bash
git add gmn_to_cidoc_transform.py
git commit -m "Add transformation for gmn:P2_1_gender property

- Implemented transform_p2_1_gender() function
- Converts simplified gender property to CIDOC-CRM P2_has_type
- Supports AAT terms for male, female, and intersex
- Added comprehensive testing
- Updated documentation"
```

### Step 3: Create Release Notes

**File**: `RELEASE_NOTES.md`

```markdown
## Version X.X (2025-10-26)

### New Features

#### Gender Property Transformation

Added support for transforming the `gmn:P2_1_gender` property:

- **Property**: Converts gmn:P2_1_gender to cidoc:P2_has_type
- **Values**: Supports three Getty AAT terms (male, female, intersex)
- **Compatibility**: Fully CIDOC-CRM compliant
- **Testing**: Comprehensive test suite included

**Impact**: 
- Enables standardized recording of person gender information
- Ensures proper semantic structure in output
- Maintains compatibility with existing data

**Migration**: 
- No data migration needed
- Property already defined in ontology
- New transformation applies automatically
```

### Step 4: Deploy to Production

**Deployment steps**:

1. **Stop any running transformation processes**
   ```bash
   # Stop processes if applicable
   ```

2. **Deploy updated script**
   ```bash
   # Copy to production location
   cp gmn_to_cidoc_transform.py /path/to/production/
   ```

3. **Verify deployment**
   ```bash
   # Run version check or test
   python /path/to/production/gmn_to_cidoc_transform.py --version
   ```

4. **Run smoke test**
   ```bash
   # Test with small sample
   python /path/to/production/gmn_to_cidoc_transform.py sample.json output.json
   ```

5. **Monitor initial runs**
   - Watch for errors in logs
   - Verify output format
   - Check transformation completeness

### Step 5: Team Training

**Training topics**:

1. **When to use the property**
   - Historical evidence requirements
   - Data entry guidelines
   - Validation rules

2. **Controlled vocabulary**
   - Three allowed AAT terms
   - How to look up terms
   - What terms mean

3. **Common issues**
   - Invalid URIs
   - Format errors
   - Missing data handling

**Training materials**: Create from `has-gender-documentation.md`

---

## Troubleshooting

### Common Issues

#### Issue 1: Function Not Found Error

**Error message**:
```
NameError: name 'transform_p2_1_gender' is not defined
```

**Solution**:
1. Verify function is defined before it's called
2. Check function name spelling
3. Ensure no indentation errors

#### Issue 2: Property Not Transforming

**Symptom**: `gmn:P2_1_gender` still present in output

**Solution**:
1. Check that function is called in `transform_item()`
2. Verify `del data['gmn:P2_1_gender']` executes
3. Check for early returns that skip deletion

#### Issue 3: Invalid Type URI

**Error message**: Validation fails on output

**Solution**:
1. Verify AAT URI format is correct
2. Check controlled vocabulary in ontology
3. Ensure URI includes namespace prefix

#### Issue 4: Missing @type Property

**Symptom**: Gender type lacks `@type: "cidoc:E55_Type"`

**Solution**:
1. Check type assignment in function
2. Verify dictionary structure
3. Review JSON-LD context

### Getting Help

If issues persist:

1. **Review logs**: Check transformation script output
2. **Test in isolation**: Run function with minimal input
3. **Compare with examples**: Use test cases provided
4. **Check dependencies**: Ensure Python version compatibility
5. **Validate ontology**: Confirm property definition is correct

---

## Validation Checklist

Use this checklist to verify successful implementation:

### Code Implementation
- [ ] `transform_p2_1_gender()` function created
- [ ] Function placed after line 2486
- [ ] Function called in `transform_item()`
- [ ] Call placed after group membership transforms
- [ ] No syntax errors

### Functionality
- [ ] Male gender transforms correctly
- [ ] Female gender transforms correctly
- [ ] Intersex transforms correctly
- [ ] Missing gender handled gracefully
- [ ] Multiple types work together

### Output Quality
- [ ] `gmn:P2_1_gender` removed from output
- [ ] `cidoc:P2_has_type` array created
- [ ] E55_Type added to gender values
- [ ] AAT URIs preserved correctly
- [ ] JSON-LD structure valid

### Documentation
- [ ] Project documentation updated
- [ ] Change log entry added
- [ ] User guide updated
- [ ] Release notes created
- [ ] Training materials prepared

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Real data tested
- [ ] Edge cases verified
- [ ] Performance acceptable

### Deployment
- [ ] Code reviewed
- [ ] Backed up original files
- [ ] Version control updated
- [ ] Team notified
- [ ] Production deployed

---

## Next Steps

After successful implementation:

1. **Monitor usage**: Track how frequently the property is used
2. **Gather feedback**: Collect input from data entry staff
3. **Refine guidelines**: Update documentation based on real-world use
4. **Plan enhancements**: Consider future improvements (temporal aspects, confidence levels)
5. **Train users**: Ensure all stakeholders understand the new capability

---

## Appendix A: Complete Code Listing

### Full Transform Function

```python
def transform_p2_1_gender(data):
    """
    Transform gmn:P2_1_gender to full CIDOC-CRM structure.
    
    Converts:
        gmn:P2_1_gender → cidoc:P2_has_type
    
    The gmn:P2_1_gender property is a simplified way to record biological sex
    characteristics using a controlled vocabulary of three Getty AAT terms:
    - aat:300189559 (male)
    - aat:300189557 (female) 
    - aat:300417544 (intersex)
    
    This function transforms it to the standard CIDOC-CRM P2_has_type pattern
    with proper E55_Type instances.
    
    Args:
        data: Item data dictionary
        
    Returns:
        Transformed data dictionary
    """
    if 'gmn:P2_1_gender' not in data:
        return data
    
    gender = data['gmn:P2_1_gender']
    
    # Handle both string and object formats
    if isinstance(gender, str):
        gender_uri = gender
    elif isinstance(gender, dict) and '@id' in gender:
        gender_uri = gender['@id']
    else:
        # Invalid format, skip transformation
        return data
    
    # Create the P2_has_type structure with E55_Type
    gender_type = {
        '@id': gender_uri,
        '@type': 'cidoc:E55_Type'
    }
    
    # Initialize cidoc:P2_has_type if it doesn't exist
    if 'cidoc:P2_has_type' not in data:
        data['cidoc:P2_has_type'] = []
    elif not isinstance(data['cidoc:P2_has_type'], list):
        data['cidoc:P2_has_type'] = [data['cidoc:P2_has_type']]
    
    # Add the gender type
    data['cidoc:P2_has_type'].append(gender_type)
    
    # Remove the simplified property
    del data['gmn:P2_1_gender']
    
    return data
```

### Integration Point

```python
def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    ...
    """
    # ... [earlier transformations lines 2408-2486] ...
    
    # Group memberships
    item = transform_p107i_1_has_regional_provenance(item)
    item = transform_p107i_2_has_social_category(item)
    item = transform_p107i_3_has_occupation(item)
    
    # Gender
    item = transform_p2_1_gender(item)
    
    # Editorial notes (last, with optional inclusion)
    item = transform_p3_1_has_editorial_note(item, include_internal)
    
    return item
```

---

## Appendix B: Test Data Files

### Complete Test Input

**File**: `comprehensive_gender_test.json`

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "https://data.geniza.org/ontology/",
    "aat": "http://vocab.getty.edu/page/aat/"
  },
  "@graph": [
    {
      "@id": "person/male-example",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Abraham ben Moses",
      "gmn:P2_1_gender": {"@id": "aat:300189559"},
      "gmn:P107i_3_has_occupation": "merchant"
    },
    {
      "@id": "person/female-example",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Esther bat David",
      "gmn:P2_1_gender": {"@id": "aat:300189557"},
      "gmn:P11i_3_has_spouse": "person/male-example"
    },
    {
      "@id": "person/intersex-example",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Person Name",
      "gmn:P2_1_gender": {"@id": "aat:300417544"}
    },
    {
      "@id": "person/no-gender",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Unknown Person"
    }
  ]
}
```

---

*This implementation guide follows GMN project standards and CIDOC-CRM best practices. For additional support, refer to the other files in this deliverables package.*
