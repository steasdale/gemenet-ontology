# Implementation Guide: gmn:P70_8_documents_broker

## Complete Step-by-Step Implementation Instructions

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Ontology Implementation](#ontology-implementation)
4. [Transformation Code Implementation](#transformation-code-implementation)
5. [Integration Steps](#integration-steps)
6. [Testing Procedures](#testing-procedures)
7. [Validation](#validation)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides complete instructions for implementing the `gmn:P70_8_documents_broker` property in both the GMN ontology file and the transformation script. The property enables simplified data entry for broker information while ensuring CIDOC-CRM compliance through automatic transformation.

**Implementation Time**: Approximately 30-45 minutes
**Difficulty Level**: Intermediate
**Prerequisites**: Basic knowledge of RDF/TTL and Python

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main GMN ontology file
- `gmn_to_cidoc_transform.py` - Transformation script

### Required Tools
- Text editor with TTL syntax support
- Python 3.8 or higher
- RDF validator (e.g., Jena riot)
- pytest for testing (optional but recommended)

### Required Knowledge
- Basic RDF/TTL syntax
- Python programming
- Understanding of CIDOC-CRM E8_Acquisition
- Familiarity with P14_carried_out_by property

---

## Ontology Implementation

### Step 1: Locate the Insertion Point

Open `gmn_ontology.ttl` and find the section with P70 subproperties. Look for the existing broker-related properties or the guarantor properties (P70.6 and P70.7). The new property should be inserted after P70.7.

### Step 2: Add the Property Definition

Insert the following TTL code:

```turtle
# Property: P70.8 documents broker
gmn:P70_8_documents_broker
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.8 documents broker"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the broker who facilitated the transaction. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P14_carried_out_by > E21_Person. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Unlike procurators and guarantors who act for one party, brokers facilitate the transaction between both parties, arranging the sale and often receiving a commission."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

### Step 3: Verify Property Placement

Ensure the property is:
1. Located in the P70 subproperties section
2. Numbered sequentially (P70.8 follows P70.7)
3. Properly indented for readability
4. Has correct prefix declarations at the top of the file

### Step 4: Validate Ontology Syntax

Run validation:

```bash
# Using Apache Jena riot
riot --validate gmn_ontology.ttl

# Or using rapper
rapper -i turtle -o turtle gmn_ontology.ttl > /dev/null
```

Expected output: No syntax errors

### Step 5: Update Ontology Metadata

If your ontology has version tracking, update:
- Version number (e.g., 1.8.0 → 1.9.0)
- Last modified date
- Changelog entry

Example:
```turtle
gmn:ontology
    owl:versionInfo "1.9.0" ;
    dcterms:modified "2025-10-27"^^xsd:date ;
    rdfs:comment "Added P70.8 documents broker property" .
```

---

## Transformation Code Implementation

### Step 1: Locate the Constants Section

Open `gmn_to_cidoc_transform.py` and find the AAT constants section near the top. Verify that `AAT_BROKER` is defined:

```python
# Getty AAT URI constants
AAT_BROKER = "http://vocab.getty.edu/page/aat/300025234"
```

If not present, add it after the other AAT constants.

### Step 2: Add the Transformation Function

Locate the section with other P70 transformation functions (likely after `transform_p70_7_documents_buyers_guarantor`). Insert the following function:

```python
def transform_p70_8_documents_broker(data):
    """
    Transform gmn:P70_8_documents_broker to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P14_carried_out_by > E21_Person (with role)
    
    Args:
        data: Dictionary containing the item data with potential gmn:P70_8_documents_broker property
    
    Returns:
        Transformed data dictionary with broker information expanded to CIDOC-CRM structure
    
    Example transformation:
        Input:
            {
                "@id": "contract_001",
                "gmn:P70_8_documents_broker": [
                    {"@id": "person_giovanni", "rdfs:label": "Giovanni broker"}
                ]
            }
        
        Output:
            {
                "@id": "contract_001",
                "cidoc:P70_documents": [{
                    "@id": "contract_001/acquisition",
                    "@type": "cidoc:E8_Acquisition",
                    "cidoc:P14_carried_out_by": [{
                        "@id": "person_giovanni",
                        "@type": "cidoc:E21_Person",
                        "rdfs:label": "Giovanni broker",
                        "cidoc:P14.1_in_the_role_of": {
                            "@id": "http://vocab.getty.edu/page/aat/300025234",
                            "@type": "cidoc:E55_Type"
                        }
                    }]
                }]
            }
    """
    # Check if the property exists in the data
    if 'gmn:P70_8_documents_broker' not in data:
        return data
    
    # Extract broker information
    brokers = data['gmn:P70_8_documents_broker']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure P70_documents acquisition exists
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    # Get reference to the acquisition
    acquisition = data['cidoc:P70_documents'][0]
    
    # Ensure P14_carried_out_by list exists
    if 'cidoc:P14_carried_out_by' not in acquisition:
        acquisition['cidoc:P14_carried_out_by'] = []
    
    # Process each broker
    for broker_obj in brokers:
        # Handle both dictionary and string URI formats
        if isinstance(broker_obj, dict):
            broker_data = broker_obj.copy()
            # Ensure type is set
            if '@type' not in broker_data:
                broker_data['@type'] = 'cidoc:E21_Person'
        else:
            # String URI case
            broker_uri = str(broker_obj)
            broker_data = {
                '@id': broker_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add broker role from Getty AAT
        broker_data['cidoc:P14.1_in_the_role_of'] = {
            '@id': AAT_BROKER,
            '@type': 'cidoc:E55_Type'
        }
        
        # Add broker to acquisition
        acquisition['cidoc:P14_carried_out_by'].append(broker_data)
    
    # Remove the simplified property
    del data['gmn:P70_8_documents_broker']
    
    return data
```

### Step 3: Integrate into Main Transformation Pipeline

Find the `transform_item()` or main transformation function. Add the broker transformation call in the appropriate location (with other P70 transformations):

```python
def transform_item(item, include_internal=False):
    """Transform all shortcut properties in an item to CIDOC-CRM structure."""
    
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)
    item = transform_p70_7_documents_buyers_guarantor(item)
    item = transform_p70_8_documents_broker(item)  # ← ADD THIS LINE
    item = transform_p70_9_documents_payment_provider_for_buyer(item)
    # ... remaining transformations ...
    
    return item
```

### Step 4: Add Import Statements (if needed)

Ensure required imports are present at the top of the file:

```python
import json
import sys
from uuid import uuid4
```

---

## Integration Steps

### Step 1: Backup Existing Files

```bash
# Backup ontology
cp gmn_ontology.ttl gmn_ontology.ttl.backup

# Backup transformation script
cp gmn_to_cidoc_transform.py gmn_to_cidoc_transform.py.backup
```

### Step 2: Apply Changes

1. Add TTL code to `gmn_ontology.ttl`
2. Add Python code to `gmn_to_cidoc_transform.py`
3. Save both files

### Step 3: Validate Syntax

```bash
# Validate TTL
riot --validate gmn_ontology.ttl

# Validate Python
python3 -m py_compile gmn_to_cidoc_transform.py
```

---

## Testing Procedures

### Test 1: Single Broker

Create test file `test_single_broker.json`:

```json
{
    "@context": {
        "gmn": "http://example.org/gmn#",
        "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
    },
    "@id": "http://example.org/contract/001",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_8_documents_broker": [
        {
            "@id": "http://example.org/person/giovanni_broker",
            "@type": "cidoc:E21_Person",
            "rdfs:label": "Giovanni Sensale"
        }
    ]
}
```

Run transformation:

```bash
python3 gmn_to_cidoc_transform.py test_single_broker.json output_single.json
```

Expected output in `output_single.json`:

```json
{
    "@context": { ... },
    "@id": "http://example.org/contract/001",
    "@type": "gmn:E31_2_Sales_Contract",
    "cidoc:P70_documents": [{
        "@id": "http://example.org/contract/001/acquisition",
        "@type": "cidoc:E8_Acquisition",
        "cidoc:P14_carried_out_by": [{
            "@id": "http://example.org/person/giovanni_broker",
            "@type": "cidoc:E21_Person",
            "rdfs:label": "Giovanni Sensale",
            "cidoc:P14.1_in_the_role_of": {
                "@id": "http://vocab.getty.edu/page/aat/300025234",
                "@type": "cidoc:E55_Type"
            }
        }]
    }]
}
```

### Test 2: Multiple Brokers

Create test file `test_multiple_brokers.json`:

```json
{
    "@context": {
        "gmn": "http://example.org/gmn#",
        "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
    },
    "@id": "http://example.org/contract/002",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_8_documents_broker": [
        {
            "@id": "http://example.org/person/giovanni_broker",
            "rdfs:label": "Giovanni Sensale"
        },
        {
            "@id": "http://example.org/person/marco_broker",
            "rdfs:label": "Marco Broker"
        }
    ]
}
```

Run transformation and verify both brokers are included in `cidoc:P14_carried_out_by` array.

### Test 3: Integration with Existing Properties

Create test file `test_integration.json`:

```json
{
    "@context": {
        "gmn": "http://example.org/gmn#",
        "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
    },
    "@id": "http://example.org/contract/003",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_1_documents_seller": [
        {"@id": "http://example.org/person/seller", "rdfs:label": "Pietro Seller"}
    ],
    "gmn:P70_2_documents_buyer": [
        {"@id": "http://example.org/person/buyer", "rdfs:label": "Antonio Buyer"}
    ],
    "gmn:P70_8_documents_broker": [
        {"@id": "http://example.org/person/broker", "rdfs:label": "Giovanni Broker"}
    ]
}
```

Verify all properties transform correctly and broker is added to acquisition structure.

### Test 4: Edge Cases

Test with:
- No broker property (should pass through unchanged)
- Empty broker array (should handle gracefully)
- Broker with only URI (no label)
- Multiple contracts in one file

---

## Validation

### Validation Checklist

- [ ] TTL syntax is valid (no parser errors)
- [ ] Python code compiles without errors
- [ ] Single broker transformation works correctly
- [ ] Multiple brokers transformation works correctly
- [ ] Broker role URI is correct (AAT 300025234)
- [ ] Integration with existing properties works
- [ ] No data loss during transformation
- [ ] Output is valid JSON-LD
- [ ] CIDOC-CRM structure is correct

### CIDOC-CRM Compliance Check

Verify the transformed output matches this pattern:

```
E31_Document (Sales Contract)
  └─ P70_documents
      └─ E8_Acquisition
          └─ P14_carried_out_by
              └─ E21_Person (Broker)
                  └─ P14.1_in_the_role_of
                      └─ E55_Type (Broker role from AAT)
```

### AAT URI Verification

Verify the broker role URI:
- URI: http://vocab.getty.edu/page/aat/300025234
- Term: "brokers (people)"
- Valid: Yes (check at vocab.getty.edu)

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: TTL Parsing Error

**Symptom**: Validator reports syntax error in TTL file

**Solutions**:
- Check for missing semicolons or periods
- Verify prefix declarations (gmn:, cidoc:, dcterms:)
- Ensure proper indentation
- Check for smart quotes (use straight quotes)

#### Issue 2: Property Not Transforming

**Symptom**: Input property still present in output, not transformed

**Solutions**:
- Verify function is called in `transform_item()`
- Check property name spelling exactly matches
- Ensure function is defined before it's called
- Add debug print statements to trace execution

#### Issue 3: Multiple Brokers Not All Included

**Symptom**: Only first broker appears in output

**Solutions**:
- Verify loop iterates through all brokers
- Check that `append()` is used, not assignment
- Ensure broker array is properly initialized

#### Issue 4: Missing Role Information

**Symptom**: Broker appears but without role specification

**Solutions**:
- Verify AAT_BROKER constant is defined
- Check P14.1_in_the_role_of is added to broker_data
- Ensure AAT URI is correct (300025234)

#### Issue 5: Acquisition Not Created

**Symptom**: No E8_Acquisition in output

**Solutions**:
- Check acquisition creation logic in function
- Verify P70_documents initialization
- Ensure acquisition URI is generated correctly

### Debug Mode

Add debug output to transformation function:

```python
def transform_p70_8_documents_broker(data):
    print(f"DEBUG: Processing broker property")
    print(f"DEBUG: Input data keys: {data.keys()}")
    
    if 'gmn:P70_8_documents_broker' not in data:
        print(f"DEBUG: No broker property found")
        return data
    
    brokers = data['gmn:P70_8_documents_broker']
    print(f"DEBUG: Found {len(brokers)} broker(s)")
    
    # ... rest of function ...
    
    print(f"DEBUG: Output data keys: {data.keys()}")
    return data
```

---

## Post-Implementation Steps

### Step 1: Documentation Updates

Update the following documentation:
- Main GMN ontology documentation
- Transformation script README
- User guide for data entry
- API documentation (if applicable)

### Step 2: Training

If needed, provide training on:
- When to use the broker property
- Difference between broker, procurator, and guarantor
- How to identify brokers in historical documents
- Data entry best practices

### Step 3: Monitoring

After deployment:
- Monitor transformation logs for errors
- Review transformed output samples
- Collect user feedback
- Track usage statistics

---

## Success Criteria

Implementation is successful when:
1. ✅ TTL validates without errors
2. ✅ Python code runs without exceptions
3. ✅ Single broker transforms correctly
4. ✅ Multiple brokers transform correctly
5. ✅ Broker role is properly assigned
6. ✅ Integration with other properties works
7. ✅ Output validates against CIDOC-CRM
8. ✅ Documentation is complete
9. ✅ Tests pass consistently
10. ✅ No data loss during transformation

---

## Additional Resources

### CIDOC-CRM References
- P70_documents: http://www.cidoc-crm.org/Property/p70-documents/version-7.1.3
- P14_carried_out_by: http://www.cidoc-crm.org/Property/p14-carried-out-by/version-7.1.3
- E8_Acquisition: http://www.cidoc-crm.org/Entity/e8-acquisition/version-7.1.3

### Getty AAT References
- AAT 300025234 (brokers): http://vocab.getty.edu/page/aat/300025234

### Related GMN Documentation
- P70 subproperties overview
- Sales contract modeling guide
- Transformation pipeline documentation

---

## Version History

- **1.0** (2025-10-27): Initial implementation guide
- Property created: 2025-10-17
- Last tested: 2025-10-27

---

## Contact

For implementation support:
- Review this guide carefully
- Check troubleshooting section
- Consult CIDOC-CRM documentation
- Review existing similar properties (P70.4-P70.7)
