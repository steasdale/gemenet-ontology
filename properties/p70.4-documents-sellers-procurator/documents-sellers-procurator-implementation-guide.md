# Implementation Guide: gmn:P70_4_documents_sellers_procurator

This guide provides step-by-step instructions for implementing the `gmn:P70_4_documents_sellers_procurator` property in the GMN ontology and transformation pipeline.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Implementation Steps](#implementation-steps)
4. [Testing Procedures](#testing-procedures)
5. [Troubleshooting](#troubleshooting)

---

## Overview

The `gmn:P70_4_documents_sellers_procurator` property is a shortcut property that simplifies representing seller's procurators in sales contracts. During transformation, it expands to full CIDOC-CRM compliance.

**Implementation Time**: ~30 minutes  
**Difficulty**: Intermediate  
**Files Modified**: 2 (ontology + transformation script)

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script

### Required Knowledge
- Basic understanding of CIDOC-CRM
- Familiarity with RDF/TTL syntax
- Python programming basics
- JSON-LD structure

### Existing Infrastructure
Ensure these components already exist in your transformation script:
- `transform_procurator_property()` helper function (lines ~483-549)
- `AAT_AGENT` constant (line 29)
- Import of `uuid4` from uuid module (line 19)

---

## Implementation Steps

### Step 1: Add Ontology Definition

**File**: `gmn_ontology.ttl`  
**Location**: After the P70.3 property definition (approximately line 320)

#### 1.1 Locate Insertion Point

Find the end of the P70.3 property definition:
```turtle
# Property: P70.3 documents transfer of
gmn:P70_3_documents_transfer_of
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.3 documents transfer of"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the physical thing (property, object, or person) being transferred. [...]"@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E18_Physical_Thing ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P24_transferred_title_of .
```

#### 1.2 Insert Property Definition

Add the following immediately after P70.3:

```turtle
# Property: P70.4 documents seller's procurator
gmn:P70_4_documents_sellers_procurator
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.4 documents seller's procurator"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the procurator (legal representative) for the seller. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (procurator), with P17_was_motivated_by linking to the seller (E21_Person). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The transformation creates an E7_Activity node that explicitly links the procurator to the seller they represent via P17_was_motivated_by."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P17_was_motivated_by .
```

#### 1.3 Verify Syntax

Check that:
- All periods and semicolons are correct
- Prefixes are properly declared at file beginning
- No duplicate property URIs exist

---

### Step 2: Add Transformation Function

**File**: `gmn_to_cidoc_transform.py`  
**Location**: In the Sales Contract transformations section, after `transform_p70_3_documents_transfer_of()`

#### 2.1 Verify Helper Function Exists

Check that the `transform_procurator_property()` function exists (around line 483):

```python
def transform_procurator_property(data, property_name, motivated_by_property):
    """
    Generic function to transform procurator properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    """
    # Function body should already exist
```

If this function doesn't exist, you'll need to add it. See the `documents-sellers-procurator-transform.py` file for the complete code.

#### 2.2 Add Specific Transformation Function

After the `transform_p70_3_documents_transfer_of()` function (around line 480), add:

```python
def transform_p70_4_documents_sellers_procurator(data):
    """Transform gmn:P70_4_documents_sellers_procurator to full CIDOC-CRM structure."""
    return transform_procurator_property(data, 'gmn:P70_4_documents_sellers_procurator', 
                                        'cidoc:P23_transferred_title_from')
```

**Code Explanation**:
- Calls generic helper with property-specific parameters
- Uses `cidoc:P23_transferred_title_from` to link to seller
- Delegates complex logic to reusable function

---

### Step 3: Update Main Transformation Function

**File**: `gmn_to_cidoc_transform.py`  
**Location**: In the `transform_item()` function

#### 3.1 Locate the Sales Contract Section

Find the section where P70 properties are transformed (around line 2190):

```python
# Sales contract properties (P70.1-P70.17)
item = transform_p70_1_documents_seller(item)
item = transform_p70_2_documents_buyer(item)
item = transform_p70_3_documents_transfer_of(item)
```

#### 3.2 Add Function Call

Insert the new transformation call after P70.3:

```python
# Sales contract properties (P70.1-P70.17)
item = transform_p70_1_documents_seller(item)
item = transform_p70_2_documents_buyer(item)
item = transform_p70_3_documents_transfer_of(item)
item = transform_p70_4_documents_sellers_procurator(item)  # <-- ADD THIS LINE
item = transform_p70_5_documents_buyers_procurator(item)
# ... continue with other properties
```

**Important**: The order matters! P70.4 must come after P70.1 (seller) to ensure proper linkage via P17_was_motivated_by.

---

### Step 4: Verify Constants

**File**: `gmn_to_cidoc_transform.py`  
**Location**: Top of file (lines 1-40)

#### 4.1 Check AAT Constants

Verify that the following constant exists:

```python
AAT_AGENT = "http://vocab.getty.edu/page/aat/300025972"
```

This should already be present at line 29.

---

## Testing Procedures

### Test 1: Basic Transformation

#### Test Data (Input)
Create a test JSON-LD file `test_p70_4_basic.json`:

```json
{
  "@context": {
    "gmn": "http://genizah.org/ontology/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [{
    "@id": "contract/test_001",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_1_documents_seller": [{
      "@id": "person/seller_001"
    }],
    "gmn:P70_4_documents_sellers_procurator": [{
      "@id": "person/procurator_001"
    }]
  }]
}
```

#### Run Transformation
```bash
python3 gmn_to_cidoc_transform.py test_p70_4_basic.json output_basic.json
```

#### Expected Output
```json
{
  "@id": "contract/test_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "contract/test_001/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P23_transferred_title_from": [{
      "@id": "person/seller_001",
      "@type": "cidoc:E21_Person"
    }],
    "cidoc:P9_consists_of": [{
      "@id": "contract/test_001/activity/procurator_[hash]",
      "@type": "cidoc:E7_Activity",
      "cidoc:P14_carried_out_by": [{
        "@id": "person/procurator_001",
        "@type": "cidoc:E21_Person"
      }],
      "cidoc:P14.1_in_the_role_of": {
        "@id": "http://vocab.getty.edu/page/aat/300025972",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P17_was_motivated_by": {
        "@id": "person/seller_001",
        "@type": "cidoc:E21_Person"
      }
    }]
  }]
}
```

#### Validation Checklist
- [ ] E8_Acquisition node created
- [ ] E7_Activity node created under P9_consists_of
- [ ] Procurator linked via P14_carried_out_by
- [ ] AAT agent role assigned via P14.1_in_the_role_of
- [ ] Seller linked via P17_was_motivated_by
- [ ] Original gmn:P70_4 property removed

---

### Test 2: Multiple Procurators

#### Test Data
```json
{
  "@id": "contract/test_002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [{"@id": "person/seller_002"}],
  "gmn:P70_4_documents_sellers_procurator": [
    {"@id": "person/procurator_002a"},
    {"@id": "person/procurator_002b"}
  ]
}
```

#### Expected Behavior
- Two separate E7_Activity nodes created
- Each with unique URI (different hash)
- Both link to same seller via P17_was_motivated_by

---

### Test 3: Edge Case - No Seller Defined

#### Test Data
```json
{
  "@id": "contract/test_003",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_4_documents_sellers_procurator": [{"@id": "person/procurator_003"}]
}
```

#### Expected Behavior
- E7_Activity still created
- Procurator linked via P14_carried_out_by
- No P17_was_motivated_by property (graceful degradation)

---

### Test 4: Integration with Other Properties

#### Test Data
```json
{
  "@id": "contract/test_004",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [{"@id": "person/seller_004"}],
  "gmn:P70_2_documents_buyer": [{"@id": "person/buyer_004"}],
  "gmn:P70_4_documents_sellers_procurator": [{"@id": "person/procurator_004"}],
  "gmn:P70_5_documents_buyers_procurator": [{"@id": "person/procurator_005"}]
}
```

#### Expected Behavior
- Single E8_Acquisition with both seller and buyer
- Two E7_Activity nodes (one for each procurator)
- Seller's procurator linked to seller
- Buyer's procurator linked to buyer

---

## Troubleshooting

### Issue 1: "AttributeError: 'dict' object has no attribute 'P70_4'"

**Cause**: Property name incorrect or data structure issue  
**Solution**: Verify property name is exactly `'gmn:P70_4_documents_sellers_procurator'` with correct namespace

### Issue 2: P17_was_motivated_by missing in output

**Cause**: Seller transformation not executed first  
**Solution**: Ensure `transform_p70_1_documents_seller()` is called before P70.4 transformation in `transform_item()`

### Issue 3: Multiple procurators create same URI

**Cause**: Hash function not working correctly  
**Solution**: Check that procurator URIs are distinct and hash calculation is correct (line 527 in transform function)

### Issue 4: Validation errors in output

**Cause**: Malformed JSON-LD structure  
**Solution**: 
1. Check all required properties are present
2. Verify '@id' and '@type' fields in all objects
3. Ensure proper list structure for array properties

### Issue 5: Original gmn:P70_4 not removed

**Cause**: Delete statement not executing  
**Solution**: Verify `del data[property_name]` line exists at end of `transform_procurator_property()` function (line 548)

---

## Validation Commands

### Validate Ontology Syntax
```bash
rapper -i turtle -o turtle gmn_ontology.ttl > /dev/null
```

### Validate JSON-LD Output
```bash
python3 -c "import json; json.load(open('output.json'))"
```

### Check Transformation Coverage
```bash
grep -n "P70_4" gmn_to_cidoc_transform.py
```

---

## Performance Considerations

- **Memory**: Each procurator adds ~200 bytes to output
- **Processing**: Linear O(n) with number of procurators
- **Hash Calculation**: Minimal overhead (~1ms per procurator)

---

## Best Practices

1. **Always transform seller first** to ensure P17 linkage
2. **Use consistent URIs** for person entities across properties
3. **Test with edge cases** before production deployment
4. **Document any customizations** to the generic helper function
5. **Validate output** against CIDOC-CRM spec

---

## Next Steps

After successful implementation:

1. ✅ Update main documentation with new property
2. ✅ Add to data entry guidelines
3. ✅ Train users on proper usage
4. ✅ Monitor transformation logs for errors
5. ✅ Consider similar implementation for P70.5 (buyer's procurator)

---

## Additional Resources

- CIDOC-CRM Documentation: http://www.cidoc-crm.org/
- Getty AAT for "agent": http://vocab.getty.edu/page/aat/300025972
- JSON-LD Specification: https://json-ld.org/spec/latest/json-ld/

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**Tested With**: Python 3.8+, JSON-LD 1.1
