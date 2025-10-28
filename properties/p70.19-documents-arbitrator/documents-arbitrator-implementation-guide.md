# GMN P70.19 Documents Arbitrator - Implementation Guide

This guide provides step-by-step instructions for implementing the `gmn:P70_19_documents_arbitrator` property in the GMN ontology and transformation pipeline.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Implementation Overview](#implementation-overview)
3. [Step 1: Update Ontology File](#step-1-update-ontology-file)
4. [Step 2: Update Transformation Script](#step-2-update-transformation-script)
5. [Step 3: Update Main Pipeline](#step-3-update-main-pipeline)
6. [Step 4: Testing](#step-4-testing)
7. [Step 5: Documentation Updates](#step-5-documentation-updates)
8. [Troubleshooting](#troubleshooting)
9. [Validation Checklist](#validation-checklist)

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script
- Access to test data

### Required Knowledge
- Understanding of CIDOC-CRM P70_documents pattern
- Familiarity with arbitration agreement context
- Basic Python programming
- RDF/Turtle syntax
- JSON-LD format

### Required Tools
- Text editor or IDE
- RDF validator (optional but recommended)
- Python 3.x environment
- JSON validator

---

## Implementation Overview

### What You'll Implement

1. **Ontology Definition** - Add property definition to TTL file
2. **Transformation Function** - Add Python function to handle property transformation
3. **Pipeline Integration** - Connect function to main transformation pipeline
4. **Testing** - Verify correct behavior with test data

### Expected Outcome

After implementation:
- Arbitration agreements can link to arbitrators via `gmn:P70_19_documents_arbitrator`
- Property automatically transforms to full CIDOC-CRM structure
- Arbitrators appear as P14_carried_out_by in E7_Activity
- Integration with P70.18 and P70.20 works seamlessly

---

## Step 1: Update Ontology File

### 1.1 Locate the Arbitration Properties Section

Open `gmn_ontology.ttl` and find the arbitration properties section:

```turtle
# Property: P70.18 documents disputing party
gmn:P70_18_documents_disputing_party
    a owl:ObjectProperty ;
    ...

# Property: P70.19 documents arbitrator
# <-- INSERT HERE
```

### 1.2 Add Property Definition

Insert the following TTL snippet:

```turtle
# Property: P70.19 documents arbitrator
gmn:P70_19_documents_arbitrator
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.19 documents arbitrator"@en ;
    rdfs:comment "Simplified property for associating an arbitration agreement with the person or persons appointed to resolve the dispute. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor. The E7_Activity should be typed as an arbitration agreement (AAT 300417271). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Arbitrators are the neutral third parties who will hear the dispute and render a binding decision."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-18"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

### 1.3 Verify Syntax

**Option A: Use RDF Validator**
```bash
rapper -i turtle -c gmn_ontology.ttl
```

**Option B: Manual Check**
- Ensure proper indentation
- Check all semicolons and periods
- Verify all URIs are correctly formatted
- Confirm dates are in ISO format

### 1.4 Save and Commit

```bash
# Save the file
# If using version control:
git add gmn_ontology.ttl
git commit -m "Add P70.19 documents arbitrator property definition"
```

---

## Step 2: Update Transformation Script

### 2.1 Locate the Arbitration Functions Section

Open `gmn_to_cidoc_transform.py` and find:

```python
def transform_p70_18_documents_disputing_party(data):
    """
    Transform gmn:P70_18_documents_disputing_party to full CIDOC-CRM structure
    """
    ...

# INSERT NEW FUNCTION HERE

def transform_p70_20_documents_dispute_subject(data):
    """
    Transform gmn:P70_20_documents_dispute_subject to full CIDOC-CRM structure
    """
    ...
```

### 2.2 Add Transformation Function

Insert the following Python function:

```python
def transform_p70_19_documents_arbitrator(data):
    """
    Transform gmn:P70_19_documents_arbitrator to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    This function handles arbitrators appointed to resolve disputes in
    arbitration agreements. Arbitrators are modeled as active principals
    who carry out the arbitration process.
    
    The function:
    1. Checks if the property exists in the data
    2. Locates or creates the shared E7_Activity node
    3. Adds arbitrators to P14_carried_out_by
    4. Removes the shortcut property
    
    Args:
        data: Dictionary containing the document data
        
    Returns:
        Modified data dictionary with CIDOC-CRM compliant structure
    """
    # Check if property exists
    if 'gmn:P70_19_documents_arbitrator' not in data:
        return data
    
    # Get arbitrator values (could be list or single value)
    arbitrators = data['gmn:P70_19_documents_arbitrator']
    if not isinstance(arbitrators, list):
        arbitrators = [arbitrators]
    
    # Get document URI for creating activity URI
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Find or create E7_Activity
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        # Create new activity with arbitration typing
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,  # AAT 300417271
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    # Get the activity (first in array)
    activity = data['cidoc:P70_documents'][0]
    
    # Ensure P14_carried_out_by array exists
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    # Add each arbitrator to P14_carried_out_by
    for arbitrator_obj in arbitrators:
        if isinstance(arbitrator_obj, dict):
            # Already a structured object, copy and ensure type
            arbitrator_data = arbitrator_obj.copy()
            if '@type' not in arbitrator_data:
                arbitrator_data['@type'] = 'cidoc:E39_Actor'
        else:
            # Just a URI string, create structure
            arbitrator_uri = str(arbitrator_obj)
            arbitrator_data = {
                '@id': arbitrator_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add to activity
        activity['cidoc:P14_carried_out_by'].append(arbitrator_data)
    
    # Remove shortcut property
    del data['gmn:P70_19_documents_arbitrator']
    
    return data
```

### 2.3 Verify AAT Constant

Check that the AAT constant is defined at the top of the file:

```python
# AAT Constants
AAT_ARBITRATION = 'http://vocab.getty.edu/page/aat/300417271'
```

If not present, add it to the constants section.

### 2.4 Add Necessary Imports

Verify these imports exist at the top of the file:

```python
from uuid import uuid4
import json
```

---

## Step 3: Update Main Pipeline

### 3.1 Locate the Transform Pipeline Function

Find the main transformation pipeline function:

```python
def transform_gmn_to_cidoc(data):
    """Main transformation pipeline"""
    
    # ... existing transformations ...
    
    # Arbitration agreement properties
    data = transform_p70_18_documents_disputing_party(data)
    # INSERT CALL HERE
    data = transform_p70_20_documents_dispute_subject(data)
    
    # ... more transformations ...
    
    return data
```

### 3.2 Add Function Call

Insert the function call in the correct position:

```python
    # Arbitration agreement properties
    data = transform_p70_18_documents_disputing_party(data)
    data = transform_p70_19_documents_arbitrator(data)
    data = transform_p70_20_documents_dispute_subject(data)
```

**Important:** The order matters for shared activity coordination. Keep arbitration properties together.

### 3.3 Save Changes

```bash
# Save the file
# If using version control:
git add gmn_to_cidoc_transform.py
git commit -m "Add P70.19 documents arbitrator transformation"
```

---

## Step 4: Testing

### 4.1 Create Test Data

Create a test file `test_arbitrator.json`:

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [{
    "@value": "Arbitration Agreement - Merchant Dispute"
  }],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/merchant_a"},
    {"@id": "http://example.org/persons/merchant_b"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_1"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/debts/debt_001"}
  ]
}
```

### 4.2 Run Transformation

```python
# Test script
import json
from gmn_to_cidoc_transform import transform_gmn_to_cidoc

# Load test data
with open('test_arbitrator.json', 'r') as f:
    test_data = json.load(f)

# Run transformation
result = transform_gmn_to_cidoc(test_data)

# Pretty print result
print(json.dumps(result, indent=2))
```

### 4.3 Expected Output

Verify the output contains:

```json
{
  "@id": "http://example.org/contracts/arb001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P14_carried_out_by": [
      {
        "@id": "http://example.org/persons/merchant_a",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/merchant_b",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/arbitrator_1",
        "@type": "cidoc:E39_Actor"
      }
    ],
    "cidoc:P16_used_specific_object": [
      {
        "@id": "http://example.org/debts/debt_001",
        "@type": "cidoc:E1_CRM_Entity"
      }
    ]
  }]
}
```

### 4.4 Verify Key Elements

Check that:
- [ ] Single E7_Activity created (not multiple)
- [ ] Activity has AAT 300417271 typing
- [ ] Arbitrator appears in P14_carried_out_by
- [ ] Disputing parties also in P14_carried_out_by
- [ ] Dispute subject in P16_used_specific_object
- [ ] Original GMN properties removed

### 4.5 Test Multiple Arbitrators

Test with multiple arbitrators:

```json
{
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_1"},
    {"@id": "http://example.org/persons/arbitrator_2"},
    {"@id": "http://example.org/persons/arbitrator_3"}
  ]
}
```

Verify all arbitrators appear in P14_carried_out_by.

### 4.6 Test Edge Cases

**Test Case 1: Arbitrator Only**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_1"}
  ]
}
```
Should create activity with just the arbitrator.

**Test Case 2: String URI (not object)**
```json
{
  "gmn:P70_19_documents_arbitrator": "http://example.org/persons/arbitrator_1"
}
```
Should handle string URI correctly.

**Test Case 3: Activity Pre-exists from P70.18**
Run transformation on data that already has P70_documents from P70.18. Verify arbitrator added to existing activity.

---

## Step 5: Documentation Updates

### 5.1 Update Main Documentation

Add to your main GMN documentation:

#### Property Table Entry

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `gmn:P70_19_documents_arbitrator` | `gmn:E31_3_Arbitration_Agreement` | `cidoc:E39_Actor` | Links arbitration agreement to appointed arbitrator(s) |

#### Usage Example

```markdown
### Arbitration Agreement with Arbitrator

An arbitration agreement appointing Giovanni Rossi as arbitrator:

**GMN Representation:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "person:merchant_1"},
    {"@id": "person:merchant_2"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "person:giovanni_rossi"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "property:warehouse_5"}
  ]
}
```

**CIDOC-CRM Output:**
All actors (disputing parties and arbitrator) appear as P14_carried_out_by in the arbitration activity.
```

### 5.2 Update Schema Documentation

Add property specification to schema docs:

```markdown
## gmn:P70_19_documents_arbitrator

**URI:** `http://www.genoesemerchantnetworks.com/ontology#P70_19_documents_arbitrator`

**Label:** P70.19 documents arbitrator

**Definition:** Simplified property for associating an arbitration agreement with the person or persons appointed to resolve the dispute.

**Domain:** gmn:E31_3_Arbitration_Agreement
**Range:** cidoc:E39_Actor
**Superproperty:** cidoc:P70_documents

**Cardinality:** 1..*

**Transformation:** Expands to E31 → P70 → E7 → P14 → E39

**Related Properties:**
- gmn:P70_18_documents_disputing_party
- gmn:P70_20_documents_dispute_subject
```

---

## Troubleshooting

### Issue: Multiple Activities Created

**Symptom:** Each arbitration property creates separate E7_Activity nodes

**Cause:** Properties processed independently without checking for existing activity

**Solution:**
1. Verify each transformation function checks for existing `cidoc:P70_documents`
2. Ensure all functions reuse the first activity in the array
3. Check function call order in pipeline

### Issue: Arbitrators Not Appearing

**Symptom:** Transformation runs but arbitrators missing from output

**Cause:** Function not called in pipeline or data format issue

**Solution:**
1. Verify function is called in `transform_gmn_to_cidoc()`
2. Check function call order
3. Verify input data format matches expected structure
4. Add debug print statements to track execution

### Issue: Type Validation Errors

**Symptom:** RDF validator complains about types

**Cause:** Domain/range mismatch or missing type declarations

**Solution:**
1. Verify arbitrator entities are properly typed as E39_Actor
2. Check document is typed as E31_3_Arbitration_Agreement
3. Ensure E7_Activity has proper typing

### Issue: AAT Constant Not Found

**Symptom:** NameError for AAT_ARBITRATION

**Cause:** Constant not defined

**Solution:**
Add to constants section:
```python
AAT_ARBITRATION = 'http://vocab.getty.edu/page/aat/300417271'
```

### Issue: UUID Import Error

**Symptom:** NameError for uuid4

**Cause:** Missing import

**Solution:**
Add to imports:
```python
from uuid import uuid4
```

---

## Validation Checklist

### Ontology Validation
- [ ] TTL file parses without errors
- [ ] Property has correct URI
- [ ] Domain is gmn:E31_3_Arbitration_Agreement
- [ ] Range is cidoc:E39_Actor
- [ ] Superproperty is cidoc:P70_documents
- [ ] Comment describes full CIDOC path
- [ ] Dates are correct

### Transformation Validation
- [ ] Function exists in script
- [ ] Function is called in pipeline
- [ ] AAT constant defined
- [ ] Imports present
- [ ] Handles list and single values
- [ ] Creates activity if needed
- [ ] Reuses existing activity
- [ ] Adds to P14_carried_out_by
- [ ] Removes GMN property
- [ ] Returns modified data

### Integration Validation
- [ ] Works with P70.18 (disputing parties)
- [ ] Works with P70.20 (dispute subject)
- [ ] All use same E7_Activity
- [ ] No duplicate activities
- [ ] Order of execution correct

### Output Validation
- [ ] E7_Activity created
- [ ] Activity has AAT typing
- [ ] Arbitrators in P14_carried_out_by
- [ ] GMN property removed
- [ ] JSON-LD valid
- [ ] Structure matches CIDOC-CRM

### Documentation Validation
- [ ] Property documented in main docs
- [ ] Examples provided
- [ ] Usage notes clear
- [ ] Related properties linked
- [ ] SPARQL examples work

---

## Success Criteria

Implementation is complete and correct when:

1. **Ontology is Valid**
   - TTL parses without errors
   - Property properly defined with all metadata

2. **Transformation Works**
   - Function processes data correctly
   - Creates or reuses E7_Activity appropriately
   - Integrates with other arbitration properties

3. **Output is Correct**
   - CIDOC-CRM compliant structure
   - Proper typing and relationships
   - No data loss

4. **Tests Pass**
   - All test cases produce expected output
   - Edge cases handled
   - Integration verified

5. **Documentation Complete**
   - Property documented
   - Examples provided
   - Usage clear

---

## Next Steps

After successful implementation:

1. **Deploy to Production**
   - Merge changes to main branch
   - Deploy updated ontology and scripts
   - Update production documentation

2. **Monitor Usage**
   - Track property usage in real data
   - Watch for unexpected patterns
   - Collect user feedback

3. **Future Enhancements**
   - Consider adding role typing (P14.1_in_the_role_of)
   - Explore arbitration award linkage
   - Investigate timespan properties

---

*For questions or issues, refer to the main documentation or semantic specification in `documents-arbitrator-documentation.md`.*
