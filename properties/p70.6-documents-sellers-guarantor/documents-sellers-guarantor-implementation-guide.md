# P70.6 Documents Seller's Guarantor - Implementation Guide

This guide provides detailed step-by-step instructions for implementing the `gmn:P70_6_documents_sellers_guarantor` property in your GMN ontology system.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Update Ontology Definition](#step-1-update-ontology-definition)
3. [Step 2: Update Transformation Script](#step-2-update-transformation-script)
4. [Step 3: Update Documentation](#step-3-update-documentation)
5. [Step 4: Testing and Validation](#step-4-testing-and-validation)
6. [Troubleshooting](#troubleshooting)
7. [Rollback Procedures](#rollback-procedures)

---

## Prerequisites

Before beginning implementation, ensure you have:

- [ ] Access to the `gmn_ontology.ttl` file
- [ ] Access to the `gmn_to_cidoc_transform.py` script
- [ ] A TTL syntax validator
- [ ] Python 3.7 or higher
- [ ] Required Python packages: `rdflib`, `uuid`
- [ ] Test dataset with sales contract data
- [ ] Backup of all files to be modified

---

## Step 1: Update Ontology Definition

### 1.1 Open the Ontology File

Open `gmn_ontology.ttl` in your text editor.

### 1.2 Locate the Sales Contract Properties Section

Find the section with other P70 properties, specifically after P70.5 (buyer's procurator) and before P70.7 (buyer's guarantor).

### 1.3 Add the Property Definition

Insert the following TTL code:

```turtle
# Property: P70.6 documents seller's guarantor
gmn:P70_6_documents_sellers_guarantor
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.6 documents seller's guarantor"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the guarantor for the seller. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (guarantor), with P17_was_motivated_by linking to the seller (E21_Person). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The transformation creates an E7_Activity node that explicitly links the guarantor to the seller they guarantee via P17_was_motivated_by. Guarantors provide security for the transaction by promising to fulfill obligations if the principal defaults."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P17_was_motivated_by .
```

### 1.4 Validate the Syntax

Run your TTL validator to ensure no syntax errors:

```bash
# Example using rapper
rapper -i turtle -o turtle gmn_ontology.ttl > /dev/null
```

If validation succeeds, proceed to the next step.

### 1.5 Commit the Changes

```bash
git add gmn_ontology.ttl
git commit -m "Add P70.6 documents seller's guarantor property"
```

---

## Step 2: Update Transformation Script

### 2.1 Open the Transformation Script

Open `gmn_to_cidoc_transform.py` in your code editor.

### 2.2 Add or Verify AAT Constant

Check if the AAT_GUARANTOR constant exists at the top of the file (around line 20-40). If not, add it:

```python
# AAT Concept URIs
AAT_NOTARY = 'http://vocab.getty.edu/aat/300025631'
AAT_PROCURATOR = 'http://vocab.getty.edu/aat/300266886'
AAT_GUARANTOR = 'http://vocab.getty.edu/aat/300379835'
AAT_BROKER = 'http://vocab.getty.edu/aat/300025234'
# ... other AAT constants
```

### 2.3 Add or Verify Helper Function

Check if the `transform_guarantor_property()` helper function exists. If not, add it after the procurator helper function:

```python
def transform_guarantor_property(data, property_name, motivated_by_property):
    """
    Generic function to transform guarantor properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    
    Args:
        data: The item data dictionary
        property_name: The GMN guarantor property to transform
        motivated_by_property: The CIDOC property linking to the principal (P22 or P23)
    
    Returns:
        Transformed data dictionary
    """
    if property_name not in data:
        return data
    
    guarantors = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure acquisition node exists
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Ensure P9_consists_of exists
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Get the motivated-by URI (seller or buyer)
    motivated_by_uri = None
    if motivated_by_property in acquisition:
        motivated_by_list = acquisition[motivated_by_property]
        if isinstance(motivated_by_list, list) and len(motivated_by_list) > 0:
            if isinstance(motivated_by_list[0], dict):
                motivated_by_uri = motivated_by_list[0].get('@id')
            else:
                motivated_by_uri = str(motivated_by_list[0])
    
    # Process each guarantor
    for guarantor_obj in guarantors:
        if isinstance(guarantor_obj, dict):
            guarantor_uri = guarantor_obj.get('@id', '')
            guarantor_data = guarantor_obj.copy()
        else:
            guarantor_uri = str(guarantor_obj)
            guarantor_data = {
                '@id': guarantor_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Create unique activity URI
        activity_hash = str(hash(guarantor_uri + property_name))[-8:]
        activity_uri = f"{subject_uri}/activity/guarantor_{activity_hash}"
        
        # Build activity node
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [guarantor_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_GUARANTOR,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add motivation if available
        if motivated_by_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': motivated_by_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove the original property
    del data[property_name]
    return data
```

### 2.4 Add the Transformation Function

Add the specific function for P70.6 after the helper function:

```python
def transform_p70_6_documents_sellers_guarantor(data):
    """
    Transform gmn:P70_6_documents_sellers_guarantor to full CIDOC-CRM structure.
    
    Creates an E7_Activity that links the guarantor to the seller via P17_was_motivated_by.
    
    Args:
        data: Item data dictionary
    
    Returns:
        Transformed item dictionary
    """
    return transform_guarantor_property(
        data, 
        'gmn:P70_6_documents_sellers_guarantor', 
        'cidoc:P23_transferred_title_from'
    )
```

### 2.5 Add Function Call to Pipeline

Locate the `transform_item()` function and add the function call in the appropriate sequence (after P70.5, before P70.7):

```python
def transform_item(item, include_internal=False):
    """
    Transform a single item from GMN format to CIDOC-CRM format.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    
    Returns:
        Transformed item dictionary
    """
    # ... previous transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)  # ADD THIS LINE
    item = transform_p70_7_documents_buyers_guarantor(item)
    # ... remaining transformations ...
    
    return item
```

### 2.6 Save and Verify

Save the file and verify the Python syntax:

```bash
python3 -m py_compile gmn_to_cidoc_transform.py
```

If no errors, proceed to testing.

---

## Step 3: Update Documentation

### 3.1 Locate Documentation File

Open your main documentation file (e.g., `sales_contract_documentation.md` or similar).

### 3.2 Add Property to Table

Find the property reference table and add P70.6:

```markdown
| Property | Label | Domain | Range | Role |
|----------|-------|--------|-------|------|
| P70.4 | documents seller's procurator | Sales Contract | Person | Seller's legal rep |
| P70.5 | documents buyer's procurator | Sales Contract | Person | Buyer's legal rep |
| **P70.6** | **documents seller's guarantor** | **Sales Contract** | **Person** | **Seller's guarantor** |
| P70.7 | documents buyer's guarantor | Sales Contract | Person | Buyer's guarantor |
```

### 3.3 Add Property Description Section

Add a dedicated section for the property (copy from `documents-sellers-guarantor-doc-note.txt`).

### 3.4 Add Examples

Include usage examples and transformation patterns from the doc-note file.

---

## Step 4: Testing and Validation

### 4.1 Create Test Data

Create a test JSON-LD file with seller's guarantor data:

```json
{
  "@context": {
    "gmn": "http://w3id.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contract/test001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": {
    "@id": "http://example.org/person/seller001",
    "@type": "cidoc:E21_Person"
  },
  "gmn:P70_6_documents_sellers_guarantor": [
    {
      "@id": "http://example.org/person/guarantor001",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

### 4.2 Run Transformation

Execute the transformation script:

```python
from gmn_to_cidoc_transform import transform_item
import json

with open('test_data.json', 'r') as f:
    test_data = json.load(f)

transformed = transform_item(test_data)

with open('test_output.json', 'w') as f:
    json.dump(transformed, f, indent=2)
```

### 4.3 Validate Output Structure

Verify the output contains:

1. **E8_Acquisition node** with @type: cidoc:E8_Acquisition
2. **E7_Activity node** with:
   - @type: cidoc:E7_Activity
   - cidoc:P14_carried_out_by pointing to guarantor
   - cidoc:P14.1_in_the_role_of pointing to AAT:300379835
   - cidoc:P17_was_motivated_by pointing to seller
3. **No GMN property** - gmn:P70_6_documents_sellers_guarantor should be removed

### 4.4 Test Edge Cases

Test with:
- Multiple guarantors for one seller
- Contract with no seller defined
- Contract with seller but no seller's guarantor
- Guarantor as both object reference and URI string

### 4.5 Integration Testing

Run the transformation on your full dataset and verify:
- No errors or exceptions
- All guarantor relationships preserved
- E7_Activity nodes properly linked
- URI generation is consistent

### 4.6 Performance Testing

For large datasets, measure:
- Transformation time
- Memory usage
- Output file size

---

## Troubleshooting

### Issue: Property Not Transforming

**Symptom:** GMN property still appears in output

**Possible Causes:**
- Function not called in pipeline
- Property name mismatch
- Conditional logic preventing transformation

**Solution:**
```python
# Add debug print in function
def transform_p70_6_documents_sellers_guarantor(data):
    print(f"Processing P70.6, found: {property_name in data}")
    # ... rest of function
```

### Issue: Missing E7_Activity Nodes

**Symptom:** Guarantor appears directly in acquisition

**Possible Causes:**
- Helper function not creating activity
- P9_consists_of not initialized

**Solution:**
- Verify helper function logic
- Check P9_consists_of initialization
- Ensure acquisition node exists

### Issue: P17_was_motivated_by Missing

**Symptom:** Activity has guarantor but no link to seller

**Possible Causes:**
- Seller not defined before guarantor transformation
- Wrong motivated_by_property parameter
- Seller URI extraction failing

**Solution:**
```python
# Add debug logging
motivated_by_uri = None
if motivated_by_property in acquisition:
    print(f"Found {motivated_by_property}")
    motivated_by_list = acquisition[motivated_by_property]
    print(f"Motivated by list: {motivated_by_list}")
    # ... continue extraction
```

### Issue: AAT Constant Not Found

**Symptom:** NameError: name 'AAT_GUARANTOR' is not defined

**Solution:**
- Add the constant at module level
- Verify spelling matches function usage
- Check import statements

### Issue: Invalid TTL Syntax

**Symptom:** Parser error when loading ontology

**Solution:**
- Run TTL validator
- Check for missing periods, commas
- Verify namespace prefixes are defined
- Ensure proper escaping of quotes in comments

---

## Rollback Procedures

If issues arise, follow these rollback steps:

### Rollback Ontology

```bash
git checkout HEAD~1 -- gmn_ontology.ttl
```

### Rollback Transformation Script

```bash
git checkout HEAD~1 -- gmn_to_cidoc_transform.py
```

### Rollback Documentation

```bash
git checkout HEAD~1 -- [your_documentation_file]
```

### Full Rollback

```bash
git revert [commit_hash]
git push
```

---

## Post-Implementation Checklist

- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Documentation updated and reviewed
- [ ] Code reviewed by peer
- [ ] Test data validated
- [ ] Performance benchmarks acceptable
- [ ] Rollback procedures tested
- [ ] Changes committed to version control
- [ ] Deployment to staging successful
- [ ] User acceptance testing completed
- [ ] Production deployment scheduled

---

## Next Steps

After successful implementation of P70.6:

1. Consider implementing P70.7 (buyer's guarantor) using the same pattern
2. Update any UI forms or data entry interfaces
3. Update SPARQL query examples
4. Train users on the new property
5. Monitor production logs for issues

---

## Support and Questions

For implementation support:
- Review the semantic documentation in `documents-sellers-guarantor-documentation.md`
- Check similar implementations (P70.7, P70.4, P70.5)
- Consult CIDOC-CRM documentation for E7_Activity patterns
- Reference the Getty AAT for guarantor concept details

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-27  
**Implementation Time Estimate:** 45-60 minutes
