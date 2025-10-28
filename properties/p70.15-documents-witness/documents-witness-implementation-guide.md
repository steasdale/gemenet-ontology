# GMN P70.15 Documents Witness - Implementation Guide

This guide provides step-by-step instructions for implementing the `gmn:P70_15_documents_witness` property in your GMN ontology and transformation pipeline.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Add Ontology Definition](#step-1-add-ontology-definition)
3. [Step 2: Add Transformation Function](#step-2-add-transformation-function)
4. [Step 3: Register in Pipeline](#step-3-register-in-pipeline)
5. [Step 4: Testing](#step-4-testing)
6. [Step 5: Documentation](#step-5-documentation)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before implementing this property, ensure you have:

- [ ] Access to `gmn_ontology.ttl` file
- [ ] Access to `gmn_to_cidoc_transform.py` file
- [ ] Python 3.7+ installed
- [ ] Understanding of CIDOC-CRM E8_Acquisition and E7_Activity classes
- [ ] Familiarity with the GMN transformation pipeline

---

## Step 1: Add Ontology Definition

### 1.1 Locate the Property Section

Open `gmn_ontology.ttl` and locate the section for Sales Contract properties (around P70.x properties).

### 1.2 Add the Property Definition

Insert the following TTL definition (from `documents-witness-ontology.ttl`):

```turtle
# Property: P70.15 documents witness
gmn:P70_15_documents_witness
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.15 documents witness"@en ;
    rdfs:comment "Simplified property for associating a sales contract with a person who served as a witness to the acquisition. Witnesses were present at the transaction and formally observed the transfer of property, providing legal validation of the event. Unlike referenced persons (P70.11) who are merely mentioned in the text, witnesses actively participated in the acquisition event. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P11_had_participant > E21_Person, with the person's role typed as 'witness' (AAT 300028910). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P11_had_participant .
```

### 1.3 Verify Placement

Ensure the property is placed logically with other P70.x properties (typically between P70.14 and P70.16).

---

## Step 2: Add Transformation Function

### 2.1 Locate the AAT Constants Section

At the top of `gmn_to_cidoc_transform.py`, verify the AAT_WITNESS constant exists:

```python
# AAT Constants
AAT_WITNESS = "http://vocab.getty.edu/page/aat/300028910"
```

If it doesn't exist, add it to the constants section.

### 2.2 Add the Transformation Function

Insert the transformation function (from `documents-witness-transform.py`):

```python
def transform_p70_15_documents_witness(data):
    """
    Transform gmn:P70_15_documents_witness to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (with role)
    """
    if 'gmn:P70_15_documents_witness' not in data:
        return data
    
    witnesses = data['gmn:P70_15_documents_witness']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    for witness_obj in witnesses:
        if isinstance(witness_obj, dict):
            witness_uri = witness_obj.get('@id', '')
            witness_data = witness_obj.copy()
        else:
            witness_uri = str(witness_obj)
            witness_data = {
                '@id': witness_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        activity_hash = str(hash(witness_uri + 'witness'))[-8:]
        activity_uri = f"{subject_uri}/activity/witness_{activity_hash}"
        
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [witness_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_WITNESS,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    del data['gmn:P70_15_documents_witness']
    return data
```

### 2.3 Verify Function Placement

Place this function with other P70.x transformation functions, ideally between `transform_p70_14_documents_referenced_object` and `transform_p70_16_documents_sale_price_amount`.

---

## Step 3: Register in Pipeline

### 3.1 Locate the Main Transform Function

Find the main `transform_gmn_to_cidoc` function or similar entry point in your transformation pipeline.

### 3.2 Add the Function Call

Add the function call in the appropriate location (with other P70.x transformations):

```python
def transform_gmn_to_cidoc(item, include_internal=False):
    """
    Main transformation function.
    """
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    # ... other P70 transformations ...
    item = transform_p70_14_documents_referenced_object(item)
    item = transform_p70_15_documents_witness(item)  # ADD THIS LINE
    item = transform_p70_16_documents_sale_price_amount(item)
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # ... remaining transformations ...
    
    return item
```

---

## Step 4: Testing

### 4.1 Basic Test Case

Create a test file `test_witness.json`:

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "contract001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_15_documents_witness": [
    {
      "@id": "witness_antonio",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

### 4.2 Run the Transformation

```python
# Test script
from gmn_to_cidoc_transform import transform_gmn_to_cidoc
import json

# Load test data
with open('test_witness.json', 'r') as f:
    test_data = json.load(f)

# Transform
result = transform_gmn_to_cidoc(test_data)

# Print result
print(json.dumps(result, indent=2))
```

### 4.3 Expected Output

The output should show:

```json
{
  "@id": "contract001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "contract001/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P9_consists_of": [
        {
          "@id": "contract001/activity/witness_<hash>",
          "@type": "cidoc:E7_Activity",
          "cidoc:P14_carried_out_by": [
            {
              "@id": "witness_antonio",
              "@type": "cidoc:E21_Person"
            }
          ],
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/page/aat/300028910",
            "@type": "cidoc:E55_Type"
          }
        }
      ]
    }
  ]
}
```

### 4.4 Test Multiple Witnesses

Create `test_multiple_witnesses.json`:

```json
{
  "@id": "contract002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_15_documents_witness": [
    "witness_antonio",
    "witness_paolo",
    "witness_giovanni"
  ]
}
```

Run the transformation and verify that three separate E7_Activity nodes are created, each with the witness role.

### 4.5 Validation Checks

- [ ] Property `gmn:P70_15_documents_witness` is removed from output
- [ ] `cidoc:P70_documents` points to an E8_Acquisition
- [ ] E8_Acquisition has `cidoc:P9_consists_of` array
- [ ] Each witness creates a separate E7_Activity
- [ ] Each E7_Activity has `cidoc:P14_carried_out_by` pointing to the witness
- [ ] Each E7_Activity has `cidoc:P14.1_in_the_role_of` with AAT_WITNESS URI
- [ ] Witness persons are typed as `cidoc:E21_Person`

---

## Step 5: Documentation

### 5.1 Update Main Documentation

Add the content from `documents-witness-doc-note.txt` to your main GMN documentation file.

### 5.2 Update Changelog

Document the addition of this property in your project's changelog:

```markdown
## [Version X.X.X] - 2025-10-XX

### Added
- gmn:P70_15_documents_witness property for recording witnesses to acquisitions
- Transformation function to convert witness shortcuts to full CIDOC-CRM structure with role assignment
```

### 5.3 Update API Documentation

If you have API documentation, add examples showing how to use the property.

---

## Troubleshooting

### Issue: Transformation Not Applied

**Symptom:** The `gmn:P70_15_documents_witness` property remains in the output

**Solution:**
- Verify the function is called in the main pipeline
- Check that the function name matches exactly: `transform_p70_15_documents_witness`
- Ensure the property name in the data matches: `gmn:P70_15_documents_witness`

### Issue: Missing AAT_WITNESS Constant

**Symptom:** `NameError: name 'AAT_WITNESS' is not defined`

**Solution:**
- Add the constant at the top of `gmn_to_cidoc_transform.py`:
```python
AAT_WITNESS = "http://vocab.getty.edu/page/aat/300028910"
```

### Issue: No E8_Acquisition Created

**Symptom:** The transformation tries to access `data['cidoc:P70_documents'][0]` but the list is empty

**Solution:**
- The function automatically creates an E8_Acquisition if one doesn't exist
- Check that the condition `if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:` is correctly implemented
- Verify that no other transformation is removing the E8_Acquisition

### Issue: Duplicate Activities

**Symptom:** Multiple E7_Activity nodes are created for the same witness

**Solution:**
- The hash function should prevent duplicates: `str(hash(witness_uri + 'witness'))[-8:]`
- Check that witness URIs are consistent (same witness = same URI)
- If intentionally modeling the same person witnessing multiple times, this is correct behavior

### Issue: Invalid Role Type

**Symptom:** The role is not recognized as a valid AAT concept

**Solution:**
- Verify AAT_WITNESS constant is set to `http://vocab.getty.edu/page/aat/300028910`
- Check that the AAT vocabulary is accessible
- Ensure the `@type` for the role is `cidoc:E55_Type`

---

## Advanced Implementation Notes

### Handling Complex Witness Data

If witness data includes additional properties (name, appellation, etc.), the transformation preserves them:

```python
# Input
{
  "gmn:P70_15_documents_witness": [
    {
      "@id": "witness_antonio",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Antonio Spinola"
      }
    }
  ]
}

# The witness_data preserves all properties via .copy()
```

### Integration with Other Properties

The `gmn:P70_15_documents_witness` property works alongside other acquisition-related properties:

```turtle
<contract> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <seller> ;
    gmn:P70_2_documents_buyer <buyer> ;
    gmn:P70_3_documents_transfer_of <property> ;
    gmn:P70_15_documents_witness <witness1>, <witness2> .
```

All properties are transformed to create a complete E8_Acquisition structure.

---

## Next Steps

After successful implementation:

1. Update your data entry forms/interfaces to support witness input
2. Create validation rules to ensure witnesses are E21_Person instances
3. Consider adding cardinality constraints if needed (e.g., minimum number of witnesses)
4. Update training materials for data entry staff
5. Add witness search/filter capabilities to your query interface

---

## References

- **CIDOC-CRM Specification:** http://www.cidoc-crm.org/
- **AAT Vocabulary (Witness):** http://vocab.getty.edu/page/aat/300028910
- **GMN Ontology Documentation:** See project documentation files
- **Related Properties:** gmn:P70_11_documents_referenced_person

---

## Support

For questions or issues with this implementation, please:
1. Check the troubleshooting section above
2. Review the semantic documentation in `documents-witness-documentation.md`
3. Consult the main GMN ontology documentation
4. Contact the ontology development team

---

**Last Updated:** 2025-10-27  
**Version:** 1.0
