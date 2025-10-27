# Implementation Guide: P70.7 Documents Buyer's Guarantor
## Step-by-Step Instructions for Full Implementation

This guide provides detailed, step-by-step instructions for implementing the `gmn:P70_7_documents_buyers_guarantor` property in the GMN ontology and transformation system.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Part 1: Ontology Update](#part-1-ontology-update)
3. [Part 2: Transformation Script Update](#part-2-transformation-script-update)
4. [Part 3: Testing](#part-3-testing)
5. [Part 4: Documentation Update](#part-4-documentation-update)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script
- Project documentation files

### Required Knowledge
- Basic understanding of RDF/Turtle syntax
- Python programming basics
- CIDOC-CRM concepts (E7_Activity, E8_Acquisition, E21_Person)
- Understanding of the guarantor role in historical contracts

### Dependencies
- Python 3.x
- JSON handling capabilities
- UUID generation (from Python's uuid module)

### Verify Existing Implementation
Before starting, verify that related components exist:

```bash
# Check if guarantor helper function exists
grep -n "def transform_guarantor_property" gmn_to_cidoc_transform.py

# Check if AAT_GUARANTOR constant is defined
grep -n "AAT_GUARANTOR" gmn_to_cidoc_transform.py

# Check if seller's guarantor (P70.6) is already implemented
grep -n "P70_6_documents_sellers_guarantor" gmn_to_cidoc_transform.py
```

---

## Part 1: Ontology Update

### Step 1.1: Locate Insertion Point

Open `gmn_ontology.ttl` and find the P70 properties section. The buyer's guarantor property should be inserted after P70.6 (seller's guarantor) and before P70.8 (broker).

```bash
# Find the location
grep -n "P70.6 documents seller's guarantor" gmn_ontology.ttl
grep -n "P70.8 documents broker" gmn_ontology.ttl
```

### Step 1.2: Insert Property Definition

Add the following TTL content after the P70.6 property definition:

```turtle
# Property: P70.7 documents buyer's guarantor
gmn:P70_7_documents_buyers_guarantor
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.7 documents buyer's guarantor"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the guarantor for the buyer. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (guarantor), with P17_was_motivated_by linking to the buyer (E21_Person). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The transformation creates an E7_Activity node that explicitly links the guarantor to the buyer they guarantee via P17_was_motivated_by. Guarantors provide security for the transaction by promising to fulfill obligations if the principal defaults."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P17_was_motivated_by .
```

### Step 1.3: Verify Syntax

Check that the TTL syntax is correct:

```bash
# Use a TTL validator or parser
rapper -i turtle gmn_ontology.ttl > /dev/null

# Or check manually for:
# - Proper semicolons between predicates
# - Period at the end of the property definition
# - Proper spacing and indentation
# - Matching quotes
```

### Step 1.4: Verify Property Placement

Confirm the property appears in the correct sequence:
- P70.6 (seller's guarantor)
- **P70.7 (buyer's guarantor)** ← New property
- P70.8 (broker)

---

## Part 2: Transformation Script Update

### Step 2.1: Verify Dependencies

Ensure the required helper function and constants exist:

```python
# Check if these are already present in gmn_to_cidoc_transform.py:

# AAT Constant (should be near top of file, around line 30)
AAT_GUARANTOR = "http://vocab.getty.edu/page/aat/300025614"

# Generic guarantor transformation function (should be around line 564-629)
def transform_guarantor_property(data, property_name, motivated_by_property):
    """
    Generic function to transform guarantor properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    """
    # ... function body ...
```

**If the helper function is missing**, see the `documents-buyers-guarantor-transform.py` file for the complete implementation to add.

### Step 2.2: Add Transformation Function

Locate the P70.6 transformation function (around line 632-635):

```python
def transform_p70_6_documents_sellers_guarantor(data):
    """Transform gmn:P70_6_documents_sellers_guarantor to full CIDOC-CRM structure."""
    return transform_guarantor_property(data, 'gmn:P70_6_documents_sellers_guarantor', 
                                       'cidoc:P23_transferred_title_from')
```

**Immediately after** this function, add the P70.7 transformation:

```python
def transform_p70_7_documents_buyers_guarantor(data):
    """Transform gmn:P70_7_documents_buyers_guarantor to full CIDOC-CRM structure."""
    return transform_guarantor_property(data, 'gmn:P70_7_documents_buyers_guarantor', 
                                       'cidoc:P22_transferred_title_to')
```

### Step 2.3: Add Function Call to Main Transform

Find the `transform_item()` function (typically around line 2200-2300). Locate the section where P70 properties are transformed:

```python
def transform_item(item, include_internal=False):
    """
    Transform an item with all custom properties to CIDOC-CRM structure.
    """
    # ... earlier transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)
    # ADD THIS LINE:
    item = transform_p70_7_documents_buyers_guarantor(item)
    item = transform_p70_8_documents_broker(item)
    # ... rest of transformations ...
```

### Step 2.4: Verify Integration

Check that the function call is in the correct position:

```bash
# Should show the correct sequence
grep -A 2 "transform_p70_6_documents_sellers_guarantor" gmn_to_cidoc_transform.py
```

Expected output should show:
```
item = transform_p70_6_documents_sellers_guarantor(item)
item = transform_p70_7_documents_buyers_guarantor(item)
item = transform_p70_8_documents_broker(item)
```

---

## Part 3: Testing

### Step 3.1: Create Test Data

Create a test JSON-LD file with a buyer's guarantor:

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/ontology#"
  },
  "@graph": [
    {
      "@id": "http://example.org/contract/test001",
      "@type": "gmn:E31_2_Sales_Contract",
      "gmn:P70_2_documents_buyer": [
        {
          "@id": "http://example.org/person/buyer001",
          "@type": "cidoc:E21_Person"
        }
      ],
      "gmn:P70_7_documents_buyers_guarantor": [
        {
          "@id": "http://example.org/person/guarantor001",
          "@type": "cidoc:E21_Person"
        }
      ]
    }
  ]
}
```

Save this as `test_buyers_guarantor.json`.

### Step 3.2: Run Transformation

```bash
python gmn_to_cidoc_transform.py test_buyers_guarantor.json > test_output.json
```

### Step 3.3: Verify Output Structure

The output should contain:

```json
{
  "@id": "http://example.org/contract/test001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "http://example.org/contract/test001/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "http://example.org/person/buyer001",
          "@type": "cidoc:E21_Person"
        }
      ],
      "cidoc:P9_consists_of": [
        {
          "@id": "http://example.org/contract/test001/activity/guarantor_XXXXXXXX",
          "@type": "cidoc:E7_Activity",
          "cidoc:P14_carried_out_by": [
            {
              "@id": "http://example.org/person/guarantor001",
              "@type": "cidoc:E21_Person"
            }
          ],
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/page/aat/300025614",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P17_was_motivated_by": {
            "@id": "http://example.org/person/buyer001",
            "@type": "cidoc:E21_Person"
          }
        }
      ]
    }
  ]
}
```

### Step 3.4: Verification Checklist

Verify that the output has:

- [ ] **E8_Acquisition node** created under `cidoc:P70_documents`
- [ ] **E7_Activity node** created under `cidoc:P9_consists_of`
- [ ] **Guarantor linked** via `cidoc:P14_carried_out_by`
- [ ] **Role specified** via `cidoc:P14.1_in_the_role_of` pointing to AAT_GUARANTOR
- [ ] **Buyer linked** via `cidoc:P17_was_motivated_by`
- [ ] **Unique activity URI** generated with hash
- [ ] **Original shortcut property removed** (gmn:P70_7_documents_buyers_guarantor should not appear in output)

### Step 3.5: Test Edge Cases

#### Test with Multiple Guarantors

```json
{
  "@id": "http://example.org/contract/test002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "http://example.org/person/buyer001"
    }
  ],
  "gmn:P70_7_documents_buyers_guarantor": [
    {
      "@id": "http://example.org/person/guarantor001"
    },
    {
      "@id": "http://example.org/person/guarantor002"
    }
  ]
}
```

Expected: Two separate E7_Activity nodes, one for each guarantor.

#### Test Without Buyer

```json
{
  "@id": "http://example.org/contract/test003",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_7_documents_buyers_guarantor": [
    {
      "@id": "http://example.org/person/guarantor001"
    }
  ]
}
```

Expected: E7_Activity created but without P17_was_motivated_by property (function should handle this gracefully).

#### Test with URI-only Guarantor

```json
{
  "@id": "http://example.org/contract/test004",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_7_documents_buyers_guarantor": [
    "http://example.org/person/guarantor001"
  ]
}
```

Expected: Guarantor converted to full object with @id and @type.

### Step 3.6: Automated Testing Script

Create a test script `test_p70_7.py`:

```python
#!/usr/bin/env python3
import json
from gmn_to_cidoc_transform import transform_p70_7_documents_buyers_guarantor

def test_basic_transformation():
    """Test basic buyer's guarantor transformation."""
    input_data = {
        "@id": "http://example.org/contract/test001",
        "gmn:P70_7_documents_buyers_guarantor": [
            {
                "@id": "http://example.org/person/guarantor001",
                "@type": "cidoc:E21_Person"
            }
        ],
        "cidoc:P70_documents": [{
            "@id": "http://example.org/contract/test001/acquisition",
            "@type": "cidoc:E8_Acquisition",
            "cidoc:P22_transferred_title_to": [{
                "@id": "http://example.org/person/buyer001"
            }]
        }]
    }
    
    result = transform_p70_7_documents_buyers_guarantor(input_data)
    
    # Verify shortcut property removed
    assert "gmn:P70_7_documents_buyers_guarantor" not in result
    
    # Verify E7_Activity created
    acquisition = result["cidoc:P70_documents"][0]
    assert "cidoc:P9_consists_of" in acquisition
    assert len(acquisition["cidoc:P9_consists_of"]) > 0
    
    # Verify activity structure
    activity = acquisition["cidoc:P9_consists_of"][0]
    assert activity["@type"] == "cidoc:E7_Activity"
    assert "cidoc:P14_carried_out_by" in activity
    assert "cidoc:P17_was_motivated_by" in activity
    assert activity["cidoc:P17_was_motivated_by"]["@id"] == "http://example.org/person/buyer001"
    
    print("✓ Basic transformation test passed")

def test_multiple_guarantors():
    """Test transformation with multiple guarantors."""
    input_data = {
        "@id": "http://example.org/contract/test002",
        "gmn:P70_7_documents_buyers_guarantor": [
            {"@id": "http://example.org/person/guarantor001"},
            {"@id": "http://example.org/person/guarantor002"}
        ],
        "cidoc:P70_documents": [{
            "@id": "http://example.org/contract/test002/acquisition",
            "@type": "cidoc:E8_Acquisition",
            "cidoc:P22_transferred_title_to": [{
                "@id": "http://example.org/person/buyer001"
            }]
        }]
    }
    
    result = transform_p70_7_documents_buyers_guarantor(input_data)
    
    acquisition = result["cidoc:P70_documents"][0]
    assert len(acquisition["cidoc:P9_consists_of"]) == 2
    
    print("✓ Multiple guarantors test passed")

def test_without_buyer():
    """Test transformation when buyer is not present."""
    input_data = {
        "@id": "http://example.org/contract/test003",
        "gmn:P70_7_documents_buyers_guarantor": [
            {"@id": "http://example.org/person/guarantor001"}
        ]
    }
    
    result = transform_p70_7_documents_buyers_guarantor(input_data)
    
    # Should still create E7_Activity but without P17
    acquisition = result["cidoc:P70_documents"][0]
    activity = acquisition["cidoc:P9_consists_of"][0]
    assert "cidoc:P14_carried_out_by" in activity
    assert "cidoc:P17_was_motivated_by" not in activity or \
           activity.get("cidoc:P17_was_motivated_by") is None
    
    print("✓ Without buyer test passed")

if __name__ == "__main__":
    test_basic_transformation()
    test_multiple_guarantors()
    test_without_buyer()
    print("\n✅ All tests passed!")
```

Run the tests:

```bash
python test_p70_7.py
```

---

## Part 4: Documentation Update

### Step 4.1: Update Property Table

Add an entry to your main documentation's property table:

| Property | Label | Domain | Range | Description |
|----------|-------|--------|-------|-------------|
| gmn:P70_7_documents_buyers_guarantor | P70.7 documents buyer's guarantor | gmn:E31_2_Sales_Contract | cidoc:E21_Person | Links contract to person guaranteeing the buyer's obligations |

### Step 4.2: Add Detailed Description

In your documentation's P70 properties section, add:

```markdown
#### P70.7 documents buyer's guarantor

**Purpose**: Associates a sales contract with the person(s) serving as guarantor for the buyer.

**CIDOC-CRM Path**:
```
E31_Document 
  → P70_documents → E8_Acquisition 
    → P9_consists_of → E7_Activity
      → P14_carried_out_by → E21_Person (guarantor)
      → P14.1_in_the_role_of → E55_Type (AAT: guarantor)
      → P17_was_motivated_by → E21_Person (buyer)
```

**Use Cases**:
- Recording persons who provide security for the buyer's obligations
- Documenting financial backing arrangements in historical contracts
- Linking guarantors to the specific party they guarantee

**Historical Context**: Guarantors were commonly required in real estate transactions when the buyer's financial standing was uncertain or when the transaction involved significant value. The guarantor promised to fulfill the buyer's obligations if the buyer defaulted.

**Example**: In a 15th-century Venetian property sale, Giovanni Rossi purchases a house, with his brother Marco Rossi serving as guarantor for the transaction.
```

### Step 4.3: Add Usage Examples

Copy relevant examples from `documents-buyers-guarantor-doc-note.txt` to your documentation.

---

## Troubleshooting

### Issue: Shortcut Property Not Removed

**Symptom**: `gmn:P70_7_documents_buyers_guarantor` still appears in output.

**Cause**: Transformation function not being called, or function not deleting property.

**Solution**:
```python
# Ensure this line is at the end of transform_p70_7_documents_buyers_guarantor:
del data['gmn:P70_7_documents_buyers_guarantor']
return data
```

### Issue: No E7_Activity Created

**Symptom**: Output shows E8_Acquisition but no P9_consists_of with activity.

**Cause**: Helper function not working or not being called correctly.

**Solution**: Verify helper function exists and is being called:
```python
# Debug by adding print statements
print("Before guarantor transform:", json.dumps(data, indent=2))
result = transform_guarantor_property(data, 'gmn:P70_7_documents_buyers_guarantor', 
                                      'cidoc:P22_transferred_title_to')
print("After guarantor transform:", json.dumps(result, indent=2))
```

### Issue: P17_was_motivated_by Missing

**Symptom**: E7_Activity created but P17_was_motivated_by not linking to buyer.

**Cause**: Buyer (P22_transferred_title_to) not present in acquisition node when transformation runs.

**Solution**: Ensure P70.2 (buyer) transformation runs before P70.7:
```python
# Correct order in transform_item():
item = transform_p70_2_documents_buyer(item)  # Must run before guarantor
# ... other properties ...
item = transform_p70_7_documents_buyers_guarantor(item)
```

### Issue: Duplicate E7_Activity Nodes

**Symptom**: Multiple identical activity nodes for same guarantor.

**Cause**: Transformation function called multiple times or guarantor listed multiple times in source.

**Solution**: 
- Check that transformation function is only called once in transform_item()
- Verify source data doesn't have duplicate guarantor entries

### Issue: Wrong AAT URI for Role

**Symptom**: P14.1_in_the_role_of points to wrong AAT concept.

**Cause**: AAT_GUARANTOR constant incorrect or not defined.

**Solution**: Verify constant at top of file:
```python
AAT_GUARANTOR = "http://vocab.getty.edu/page/aat/300025614"
```

### Issue: Activity URI Not Unique

**Symptom**: Multiple guarantors get the same activity URI.

**Cause**: Hash function not properly distinguishing guarantors.

**Solution**: Verify hash generation in helper function:
```python
activity_hash = str(hash(guarantor_uri + property_name))[-8:]
activity_uri = f"{subject_uri}/activity/guarantor_{activity_hash}"
```

---

## Validation Checklist

Before considering implementation complete:

### Code Quality
- [ ] All functions properly documented with docstrings
- [ ] Code follows project style guidelines
- [ ] No hardcoded values (uses constants)
- [ ] Proper error handling for edge cases

### Functional Testing
- [ ] Basic transformation works
- [ ] Multiple guarantors handled correctly
- [ ] Edge cases tested (missing buyer, URI-only guarantor, etc.)
- [ ] Integration with other P70 properties verified
- [ ] No regression in existing transformations

### Documentation
- [ ] Ontology TTL properly formatted and valid
- [ ] Property description clear and accurate
- [ ] Examples provided in documentation
- [ ] Implementation guide complete

### Integration
- [ ] Function called in correct sequence
- [ ] Dependencies verified (helper functions, constants)
- [ ] Works with existing test suite
- [ ] Compatible with data entry workflow

---

## Next Steps

After successful implementation:

1. **Deploy to Test Environment**: Test with real historical data
2. **User Training**: Update data entry guidelines
3. **Monitor Usage**: Track how often property is used
4. **Gather Feedback**: Collect user feedback on usability
5. **Iterate**: Make adjustments based on real-world usage

---

## Additional Resources

- **CIDOC-CRM Specification**: http://www.cidoc-crm.org/
- **Getty AAT**: http://vocab.getty.edu/
- **RDF/Turtle Syntax**: https://www.w3.org/TR/turtle/
- **JSON-LD**: https://json-ld.org/

---

## Summary

This implementation adds a convenient shortcut property for documenting buyer's guarantors in sales contracts while maintaining full CIDOC-CRM compliance through automatic transformation. The property integrates seamlessly with the existing P70 property family and follows established patterns for role-based participation in acquisition events.

**Key Points**:
- Uses generic guarantor transformation helper for consistency
- Creates proper E7_Activity structure with role specification
- Links guarantor to buyer via P17_was_motivated_by
- Supports multiple guarantors per contract
- Handles edge cases gracefully

---

**Implementation Guide Version**: 1.0  
**Last Updated**: 2025-10-27  
**Property**: gmn:P70_7_documents_buyers_guarantor
