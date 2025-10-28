# GMN P70.24 Indicates Declaring Party - Implementation Guide

This guide provides step-by-step instructions for implementing the `gmn:P70_24_indicates_declarant` property across the GMN ontology, transformation pipeline, and documentation.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Ontology Updates](#step-1-ontology-updates)
3. [Step 2: Python Transformation](#step-2-python-transformation)
4. [Step 3: Documentation Updates](#step-3-documentation-updates)
5. [Step 4: Testing](#step-4-testing)
6. [Step 5: Validation](#step-5-validation)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before beginning implementation:

- [ ] Access to `gmn_ontology.ttl` file
- [ ] Access to `gmn_to_cidoc_transform.py` file
- [ ] Python 3.7+ environment
- [ ] Understanding of CIDOC-CRM E7_Activity and P14_carried_out_by
- [ ] Familiarity with declaration documents in GMN

---

## Step 1: Ontology Updates

### 1.1 Locate the Declaration Section

Open `gmn_ontology.ttl` and find the declaration properties section (around line 1100-1200). You should see:

```turtle
# Property: P70.24 indicates party issuing declaration
gmn:P70_24_indicates_declarant
    a owl:ObjectProperty ;
    a rdf:Property ;
```

### 1.2 Verify Property Definition

Ensure the complete property definition is present:

```turtle
# Property: P70.24 indicates party issuing declaration
gmn:P70_24_indicates_declarant
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.24 indicates declarant"@en ;
    rdfs:comment "Simplified property for associating a declaration document with the person or entity making the declaration. The declarant is the party who is formally stating, acknowledging, or asserting something. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor. The E7_Activity should be typed as a declaration (AAT 300027623). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_5_Declaration ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-18"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

### 1.3 Verify Domain and Range

**Critical checks**:
- Domain MUST be `gmn:E31_5_Declaration`
- Range MUST be `cidoc:E39_Actor`
- Superproperty MUST be `cidoc:P70_documents`

### 1.4 Save and Validate

```bash
# Validate TTL syntax
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null
```

If validation passes, you'll see no errors. If there are syntax errors, fix them before proceeding.

---

## Step 2: Python Transformation

### 2.1 Locate the Transformation Script

Open `gmn_to_cidoc_transform.py` and find the declaration transformation section (around line 800-900).

### 2.2 Verify the Transformation Function Exists

The function should already exist in the script. Verify it looks like this:

```python
def transform_p70_24_indicates_declarant(data):
    """
    Transform gmn:P70_24_indicates_declarant to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    """
    if 'gmn:P70_24_indicates_declarant' not in data:
        return data
    
    declarants = data['gmn:P70_24_indicates_declarant']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create or reuse activity
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/declaration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_DECLARATION,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    # Add declarants
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    for declarant_obj in declarants:
        if isinstance(declarant_obj, dict):
            declarant_data = declarant_obj.copy()
            if '@type' not in declarant_data:
                declarant_data['@type'] = 'cidoc:E39_Actor'
        else:
            declarant_uri = str(declarant_obj)
            declarant_data = {
                '@id': declarant_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        activity['cidoc:P14_carried_out_by'].append(declarant_data)
    
    # Remove shortcut property
    del data['gmn:P70_24_indicates_declarant']
    return data
```

### 2.3 Verify AAT Constant

Near the top of the file (around line 20-50), verify the AAT constant exists:

```python
AAT_DECLARATION = 'http://vocab.getty.edu/page/aat/300027623'
```

If it doesn't exist, add it with the other AAT constants.

### 2.4 Add to Transform Pipeline

Find the `transform_item()` function (around line 1200-1400) and verify these lines are present in the declaration properties section:

```python
    # Declaration properties (P70.24-P70.25)
    item = transform_p70_24_indicates_declarant(item)
    item = transform_p70_25_indicates_declaration_subject(item)
```

The position matters - it should be:
- **After** creation properties (P94i_1, P94i_2, P94i_3)
- **After** cession properties (P70.21-P70.23)
- **Before** correspondence properties (P70.26+)

### 2.5 Test the Function in Isolation

Create a test file `test_p70_24.py`:

```python
from gmn_to_cidoc_transform import transform_p70_24_indicates_declarant

# Test case 1: Simple declaration
test_data_1 = {
    '@id': 'http://example.org/declaration001',
    '@type': 'gmn:E31_5_Declaration',
    'gmn:P70_24_indicates_declarant': ['http://example.org/person_marco']
}

result_1 = transform_p70_24_indicates_declarant(test_data_1)
print("Test 1 - Simple declaration:")
print(result_1)
print()

# Test case 2: Multiple declarants
test_data_2 = {
    '@id': 'http://example.org/declaration002',
    '@type': 'gmn:E31_5_Declaration',
    'gmn:P70_24_indicates_declarant': [
        'http://example.org/brother_antonio',
        'http://example.org/brother_giovanni'
    ]
}

result_2 = transform_p70_24_indicates_declarant(test_data_2)
print("Test 2 - Multiple declarants:")
print(result_2)
print()

# Test case 3: No declarant (should return unchanged)
test_data_3 = {
    '@id': 'http://example.org/declaration003',
    '@type': 'gmn:E31_5_Declaration'
}

result_3 = transform_p70_24_indicates_declarant(test_data_3)
print("Test 3 - No declarant:")
print(result_3)
```

Run the test:

```bash
python test_p70_24.py
```

Expected output should show proper transformation with E7_Activity nodes.

---

## Step 3: Documentation Updates

### 3.1 Add to Main Documentation File

Open your main documentation file (e.g., `declaration-documentation.md`) and add the property specification.

**Location**: In the "Declaration Properties" section

**Content to add**:

```markdown
### P70.24 indicates declarant

**Property URI**: `gmn:P70_24_indicates_declarant`

**Label**: "P70.24 indicates declarant" (English)

**Domain**: `gmn:E31_5_Declaration`

**Range**: `cidoc:E39_Actor`

**Superproperty**: `cidoc:P70_documents`

**Definition**: Simplified property for associating a declaration document with the person or entity making the declaration. The declarant is the party who is formally stating, acknowledging, or asserting something.

**CIDOC-CRM Path**:
```
E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
```

**Inverse**: `cidoc:P14i_performed` (from E39_Actor to E7_Activity)

**Quantification**: Many to many (0,n:0,n) - A declaration can have multiple declarants (joint declarations), and an actor can be the declarant in multiple declarations.

**Implicit Activity Type**: AAT 300027623 (declaration)

**Scope Note**: The declarant is the person or organization formally making the statement, acknowledgment, or assertion. This is distinct from P70_22 (receiving party), which can be used for the recipient of the declaration. Multiple declarants indicate joint declarations where all parties are making the same statement together.

**Examples**:
- A debtor declaring a debt owed
- Multiple heirs jointly declaring property rights
- An official making a formal statement
- Business partners declaring contractual obligations
```

### 3.2 Add Usage Examples

In the examples section of your documentation, add:

```markdown
### Example 1: Simple Debt Declaration

**Input (shortcut)**:
```turtle
<debt_declaration_01> a gmn:E31_5_Declaration ;
    gmn:P1_1_has_name "Marco's debt declaration" ;
    gmn:P70_24_indicates_declarant <merchant_marco> ;
    gmn:P70_25_indicates_declaration_subject <debt_500_lire> .
```

**Output (CIDOC-CRM compliant)**:
```turtle
<debt_declaration_01> a gmn:E31_5_Declaration ;
    cidoc:P1_is_identified_by <debt_declaration_01/appellation> ;
    cidoc:P70_documents <debt_declaration_01/declaration> .

<debt_declaration_01/appellation> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Marco's debt declaration" .

<debt_declaration_01/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <merchant_marco> ;
    cidoc:P16_used_specific_object <debt_500_lire> .
```

### Example 2: Joint Declaration

**Input (shortcut)**:
```turtle
<property_declaration_02> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <brother_antonio> ,
                                   <brother_giovanni> ;
    gmn:P70_25_indicates_declaration_subject <family_vineyard> .
```

**Output (CIDOC-CRM compliant)**:
```turtle
<property_declaration_02> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <property_declaration_02/declaration> .

<property_declaration_02/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <brother_antonio> ,
                             <brother_giovanni> ;
    cidoc:P16_used_specific_object <family_vineyard> .
```
```

### 3.3 Update Comparison Tables

Add P70.24 to any property comparison tables in your documentation:

```markdown
| Property | Domain | Range | Purpose |
|----------|--------|-------|---------|
| P70.24 indicates declarant | E31_5_Declaration | E39_Actor | Who makes the declaration |
| P70.25 indicates declaration subject | E31_5_Declaration | E1_CRM_Entity | What is declared |
| P70.22 indicates receiving party | Multiple | E39_Actor | Who receives (optional) |
```

---

## Step 4: Testing

### 4.1 Create Test Data

Create a test file `test_declarations.json`:

```json
[
    {
        "@id": "http://example.org/declaration001",
        "@type": "gmn:E31_5_Declaration",
        "gmn:P1_1_has_name": "Debt acknowledgment by Marco",
        "gmn:P70_24_indicates_declarant": ["http://example.org/merchant_marco"],
        "gmn:P70_25_indicates_declaration_subject": ["http://example.org/debt_500_lire"]
    },
    {
        "@id": "http://example.org/declaration002",
        "@type": "gmn:E31_5_Declaration",
        "gmn:P1_1_has_name": "Joint property declaration",
        "gmn:P70_24_indicates_declarant": [
            "http://example.org/brother_antonio",
            "http://example.org/brother_giovanni"
        ],
        "gmn:P70_25_indicates_declaration_subject": ["http://example.org/family_vineyard"]
    },
    {
        "@id": "http://example.org/declaration003",
        "@type": "gmn:E31_5_Declaration",
        "gmn:P70_24_indicates_declarant": ["http://example.org/notary_pietro"],
        "gmn:P70_25_indicates_declaration_subject": ["http://example.org/legal_fact_01"],
        "gmn:P94i_1_was_created_by": ["http://example.org/notary_pietro"],
        "gmn:P94i_2_has_enactment_date": "1445-06-20"
    }
]
```

### 4.2 Run Transformation Test

```python
import json
from gmn_to_cidoc_transform import transform_item

with open('test_declarations.json', 'r') as f:
    test_data = json.load(f)

for item in test_data:
    print(f"\n{'='*60}")
    print(f"Testing: {item.get('gmn:P1_1_has_name', 'Unnamed')}")
    print(f"{'='*60}")
    
    result = transform_item(item)
    
    print("\nTransformed output:")
    print(json.dumps(result, indent=2))
```

### 4.3 Verify Output Structure

For each transformed declaration, verify:

1. **Activity Created**:
   ```python
   assert 'cidoc:P70_documents' in result
   assert len(result['cidoc:P70_documents']) > 0
   ```

2. **Activity Typed**:
   ```python
   activity = result['cidoc:P70_documents'][0]
   assert 'cidoc:P2_has_type' in activity
   assert activity['cidoc:P2_has_type']['@id'] == 'http://vocab.getty.edu/page/aat/300027623'
   ```

3. **Declarant(s) Added**:
   ```python
   assert 'cidoc:P14_carried_out_by' in activity
   assert len(activity['cidoc:P14_carried_out_by']) > 0
   ```

4. **Shortcut Removed**:
   ```python
   assert 'gmn:P70_24_indicates_declarant' not in result
   ```

### 4.4 Test Edge Cases

Test these scenarios:

**Empty declarant list**:
```json
{
    "@id": "http://example.org/declaration004",
    "@type": "gmn:E31_5_Declaration",
    "gmn:P70_24_indicates_declarant": []
}
```

**Declarant with detailed data**:
```json
{
    "@id": "http://example.org/declaration005",
    "@type": "gmn:E31_5_Declaration",
    "gmn:P70_24_indicates_declarant": [
        {
            "@id": "http://example.org/person_lucia",
            "@type": "cidoc:E21_Person",
            "rdfs:label": "Lucia the merchant"
        }
    ]
}
```

**Integration with P70.25**:
```json
{
    "@id": "http://example.org/declaration006",
    "@type": "gmn:E31_5_Declaration",
    "gmn:P70_25_indicates_declaration_subject": ["http://example.org/subject_first"],
    "gmn:P70_24_indicates_declarant": ["http://example.org/declarant_after"]
}
```

Both properties should share the same activity node.

---

## Step 5: Validation

### 5.1 SPARQL Validation Queries

After loading transformed data into a triple store, run these queries:

**Query 1: Verify all declarants are properly linked**
```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declaration ?activity ?declarant
WHERE {
    ?declaration a gmn:E31_5_Declaration ;
                 cidoc:P70_documents ?activity .
    ?activity cidoc:P14_carried_out_by ?declarant .
}
```

**Query 2: Verify activity typing**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declaration ?activity ?type
WHERE {
    ?declaration cidoc:P70_documents ?activity .
    ?activity a cidoc:E7_Activity ;
              cidoc:P2_has_type ?type .
    FILTER(?type = <http://vocab.getty.edu/page/aat/300027623>)
}
```

**Query 3: Find joint declarations**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declaration (COUNT(?declarant) as ?count)
WHERE {
    ?declaration cidoc:P70_documents ?activity .
    ?activity cidoc:P14_carried_out_by ?declarant .
}
GROUP BY ?declaration
HAVING (COUNT(?declarant) > 1)
```

### 5.2 Check for Common Errors

Run these checks:

1. **No orphaned shortcuts**:
```python
def check_no_shortcuts(data):
    if 'gmn:P70_24_indicates_declarant' in data:
        print("ERROR: Shortcut property not removed")
        return False
    return True
```

2. **Activity properly typed**:
```python
def check_activity_type(data):
    if 'cidoc:P70_documents' in data:
        activity = data['cidoc:P70_documents'][0]
        if 'cidoc:P2_has_type' not in activity:
            print("ERROR: Activity not typed")
            return False
        type_uri = activity['cidoc:P2_has_type']['@id']
        if type_uri != 'http://vocab.getty.edu/page/aat/300027623':
            print("ERROR: Wrong activity type")
            return False
    return True
```

3. **Declarant is E39_Actor**:
```python
def check_declarant_type(data):
    if 'cidoc:P70_documents' in data:
        activity = data['cidoc:P70_documents'][0]
        if 'cidoc:P14_carried_out_by' in activity:
            for declarant in activity['cidoc:P14_carried_out_by']:
                if '@type' in declarant:
                    if 'E39_Actor' not in declarant['@type']:
                        print("ERROR: Declarant not typed as E39_Actor")
                        return False
    return True
```

### 5.3 Integration Testing

Test with real data from your project:

```python
import json
from gmn_to_cidoc_transform import transform_item

# Load your actual declaration documents
with open('real_declarations.json', 'r') as f:
    declarations = json.load(f)

errors = []
for decl in declarations:
    try:
        result = transform_item(decl)
        
        # Run validation checks
        if not check_no_shortcuts(result):
            errors.append(f"Shortcut not removed in {decl['@id']}")
        if not check_activity_type(result):
            errors.append(f"Activity type error in {decl['@id']}")
        if not check_declarant_type(result):
            errors.append(f"Declarant type error in {decl['@id']}")
            
    except Exception as e:
        errors.append(f"Exception in {decl['@id']}: {str(e)}")

if errors:
    print("ERRORS FOUND:")
    for error in errors:
        print(f"  - {error}")
else:
    print("ALL TESTS PASSED!")
```

---

## Troubleshooting

### Problem: Activity not created

**Symptom**: Transformed data has no `cidoc:P70_documents`

**Cause**: Function not called in transform pipeline

**Solution**: 
1. Check that `transform_p70_24_indicates_declarant()` is called in `transform_item()`
2. Verify it's called in the correct order (after creation properties, before correspondence)

### Problem: Multiple activities created

**Symptom**: Each property (P70.24, P70.25) creates separate activities

**Cause**: Functions not checking for existing activity

**Solution**: 
Both functions should check for and reuse existing activity:
```python
if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
    # Create new activity
else:
    # Reuse existing activity
```

### Problem: Wrong activity type

**Symptom**: Activity typed as something other than AAT 300027623

**Cause**: Type being overwritten or AAT constant wrong

**Solution**: 
1. Verify AAT_DECLARATION constant: `AAT_DECLARATION = 'http://vocab.getty.edu/page/aat/300027623'`
2. Ensure type is set when activity is created
3. Check that no other function is overwriting the type

### Problem: Declarant not linked properly

**Symptom**: P14_carried_out_by missing or empty

**Cause**: List handling or appending error

**Solution**: 
1. Ensure declarants are extracted as list: `declarants = data['gmn:P70_24_indicates_declarant']`
2. Initialize list if not present: `if 'cidoc:P14_carried_out_by' not in activity: activity['cidoc:P14_carried_out_by'] = []`
3. Append each declarant: `activity['cidoc:P14_carried_out_by'].append(declarant_data)`

### Problem: Shortcut property still present

**Symptom**: Both gmn:P70_24 and cidoc structures exist

**Cause**: Deletion line missing or failing

**Solution**: 
Ensure this line is at the end of the function:
```python
del data['gmn:P70_24_indicates_declarant']
```

### Problem: URI generation fails

**Symptom**: Activity URI is malformed or duplicate

**Cause**: Subject URI not properly extracted

**Solution**: 
```python
subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
activity_uri = f"{subject_uri}/declaration"
```

Ensure subject has an @id, or uuid4 is imported: `from uuid import uuid4`

---

## Completion Checklist

Before considering implementation complete:

- [ ] Property definition added to ontology
- [ ] Transformation function present and correct
- [ ] Function called in transform pipeline
- [ ] AAT constant defined
- [ ] Documentation updated with examples
- [ ] Unit tests pass (single declarant)
- [ ] Unit tests pass (multiple declarants)
- [ ] Integration tests pass (with P70.25)
- [ ] Edge cases tested
- [ ] SPARQL validation queries run successfully
- [ ] No shortcuts remain in transformed data
- [ ] All activities properly typed
- [ ] Real data tested successfully

---

## Next Steps

After successful implementation:

1. **Update related documentation** for E31_5_Declaration class
2. **Add examples to tutorials** showing declaration usage
3. **Update data entry forms** to include P70.24 field
4. **Train data curators** on proper usage
5. **Monitor transformations** in production
6. **Collect feedback** from users

---

**Implementation Guide Version**: 1.0  
**Last Updated**: October 2025  
**Status**: Ready for Use
