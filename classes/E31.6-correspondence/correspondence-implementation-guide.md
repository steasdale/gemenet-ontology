# E31.6 Correspondence - Implementation Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Update Ontology File](#step-1-update-ontology-file)
3. [Step 2: Update Transformation Script](#step-2-update-transformation-script)
4. [Step 3: Update Documentation](#step-3-update-documentation)
5. [Step 4: Testing](#step-4-testing)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before beginning implementation, ensure you have:

- [ ] Access to `gmn_ontology.ttl`
- [ ] Access to `gmn_to_cidoc_transform_script.py`
- [ ] Access to `documentation note.txt`
- [ ] Understanding of existing GMN property patterns
- [ ] Familiarity with CIDOC-CRM P70_documents pattern
- [ ] Python 3.x environment for testing

**Estimated Time**: 90 minutes total

---

## Step 1: Update Ontology File

**File**: `gmn_ontology.ttl`  
**Time**: 15 minutes

### 1.1 Locate the Classes Section

Find the section in your ontology file labeled:
```turtle
#######################
# Classes (Alphabetical)
#######################
```

### 1.2 Add E31.6 Correspondence Class

Insert the following after the existing E31 document classes (around line 50-80):

```turtle
# Class: E31.6 Correspondence
gmn:E31_6_Correspondence
    a owl:Class ;
    rdfs:subClassOf cidoc:E31_Document ;
    rdfs:label "E31.6 Correspondence"@en ;
    rdfs:comment "A specialized type of E31_Document representing letters and other forms of written correspondence. These are documents written by one party from one location and sent to another party at a different location. Correspondence documents capture communication events between individuals or groups, including the sender, recipient, origin location, destination location, and any events or parties described within the letter's content. This class extends E31_Document to capture the specific structure and participants involved in epistolary communication."@en ;
    dcterms:created "2025-10-18"^^xsd:date .
```

**✓ Checkpoint**: Validate TTL syntax using an RDF validator or your IDE.

### 1.3 Locate the Properties Section

Find the section labeled:
```turtle
#############################
# Properties (Alphabetical) # 
#############################
```

### 1.4 Add Property Definitions

Add all six property definitions. The complete code is in `ttl_additions.txt`. Insert them in numerical order around the P70 properties section.

**Key properties to add**:
- P70.26 indicates sender
- P70.27 has address of origin
- P70.28 indicates recipient
- P70.29 indicates holder of item
- P70.30 refers to described event
- P70.31 has address of destination

**✓ Checkpoint**: Verify all properties have correct:
- Domain declarations
- Range declarations
- rdfs:subPropertyOf cidoc:P70_documents
- Proper comments

### 1.5 Update CLASS HIERARCHY Documentation

Find the CLASS HIERARCHY section at the bottom of your ontology and update it:

```turtle
CLASS HIERARCHY:

cidoc:E31_Document
  ├─ gmn:E31_1_Contract (general notarial contracts)
  │   ├─ gmn:E31_2_Sales_Contract (specialized for sales)
  │   ├─ gmn:E31_3_Arbitration_Agreement
  │   ├─ gmn:E31_4_Cession_of_Rights_Contract
  │   └─ gmn:E31_7_Donation_Contract
  ├─ gmn:E31_5_Declaration
  └─ gmn:E31_6_Correspondence
```

**✓ Checkpoint**: Save the file and validate the entire TTL document.

---

## Step 2: Update Transformation Script

**File**: `gmn_to_cidoc_transform_script.py`  
**Time**: 30 minutes

### 2.1 Add AAT Constant

Locate the AAT constants section at the top of the script (around lines 20-40) and add:

```python
AAT_CORRESPONDENCE = "http://vocab.getty.edu/page/aat/300026877"
```

**Location**: After `AAT_DECLARATION` and before the function definitions.

**✓ Checkpoint**: Verify constant follows naming convention.

### 2.2 Add Transformation Functions

Copy all six transformation functions from `python_additions.txt` and add them to your script.

**Recommended location**: After the existing P70 transformation functions (around line 800-1200).

**Functions to add**:
1. `transform_p70_26_indicates_sender(data)`
2. `transform_p70_27_has_address_of_origin(data)`
3. `transform_p70_28_indicates_recipient(data)`
4. `transform_p70_29_indicates_holder_of_item(data)`
5. `transform_p70_30_refers_to_described_event(data)`
6. `transform_p70_31_has_address_of_destination(data)`

**✓ Checkpoint**: Ensure each function has:
- Proper docstring
- Input validation
- Activity reuse logic
- Proper return statement

### 2.3 Update transform_item() Function

Locate the `transform_item(item, include_internal=False)` function.

Find the section with correspondence property transformations (if it exists) or create a new section after declaration properties:

```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    
    # ... existing transformations ...
    
    # Correspondence properties (P70.26-P70.31)
    item = transform_p70_26_indicates_sender(item)
    item = transform_p70_27_has_address_of_origin(item)
    item = transform_p70_28_indicates_recipient(item)
    item = transform_p70_29_indicates_holder_of_item(item)
    item = transform_p70_30_refers_to_described_event(item)
    item = transform_p70_31_has_address_of_destination(item)
    
    # ... rest of transformations ...
    
    return item
```

**Recommended order**: Add these after declaration transformations and before donation transformations.

**✓ Checkpoint**: Verify all six function calls are present and properly ordered.

### 2.4 Update Script Documentation

Update the module docstring at the top of the script:

```python
"""
Transform GMN shortcut properties to full CIDOC-CRM compliant structure.

This script reads JSON-LD export from Omeka-S and transforms custom shortcut
properties (like gmn:P1_1_has_name) into their full CIDOC-CRM equivalents.

Updated to reflect expanded class hierarchy including:
- gmn:E31_1_Contract (general contract class)
- gmn:E31_2_Sales_Contract (specialized sales contract)
- gmn:E31_3_Arbitration_Agreement
- gmn:E31_4_Cession_of_Rights_Contract
- gmn:E31_5_Declaration
- gmn:E31_6_Correspondence
- gmn:E31_7_Donation_Contract
"""
```

**✓ Checkpoint**: Save the script and run Python syntax check: `python -m py_compile gmn_to_cidoc_transform_script.py`

---

## Step 3: Update Documentation

**File**: `documentation note.txt`  
**Time**: 15 minutes

### 3.1 Add Transformation Examples

Copy the example transformations from `documentation_additions.txt` to your documentation file.

**Location**: Add in the examples section, after the existing P70 property examples.

### 3.2 Update Class Hierarchy Table

Update your CLASS HIERARCHY section to include E31.6:

```
cidoc:E31_Document
  ├─ gmn:E31_1_Contract (general notarial contracts)
  │   ├─ gmn:E31_2_Sales_Contract (specialized for sales)
  │   ├─ gmn:E31_3_Arbitration_Agreement
  │   ├─ gmn:E31_4_Cession_of_Rights_Contract
  │   └─ gmn:E31_7_Donation_Contract
  ├─ gmn:E31_5_Declaration
  └─ gmn:E31_6_Correspondence
```

### 3.3 Update Property Distribution Table

If you have a property distribution table, add Correspondence properties:

```
Properties on gmn:E31_6_Correspondence:
- P70.26 indicates sender
- P70.27 has address of origin
- P70.28 indicates recipient
- P70.29 indicates holder of item
- P70.31 has address of destination

Properties on cidoc:E31_Document (all document types):
- P70.30 refers to described event
- P70.11 documents referenced person
- [other universal properties...]
```

**✓ Checkpoint**: Verify examples match the transformation output format.

---

## Step 4: Testing

**Time**: 30 minutes

### 4.1 Create Test Data

Create a test JSON-LD file with correspondence properties:

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/correspondence/letter001",
  "@type": "gmn:E31_6_Correspondence",
  "gmn:P70_26_indicates_sender": {
    "@id": "http://example.org/persons/john_merchant"
  },
  "gmn:P70_27_has_address_of_origin": {
    "@id": "http://example.org/places/venice"
  },
  "gmn:P70_28_indicates_recipient": {
    "@id": "http://example.org/persons/maria_trader"
  },
  "gmn:P70_31_has_address_of_destination": {
    "@id": "http://example.org/places/cairo"
  },
  "gmn:P70_29_indicates_holder_of_item": {
    "@id": "http://example.org/persons/carlo_porter"
  },
  "gmn:P70_30_refers_to_described_event": {
    "@id": "http://example.org/events/cargo_arrival"
  }
}
```

Save as `test_correspondence.json`

### 4.2 Run Transformation

```bash
python gmn_to_cidoc_transform_script.py test_correspondence.json output_correspondence.json
```

### 4.3 Validate Output Structure

Check the output for:

**1. Correspondence Activity Created**:
```json
"cidoc:P70_documents": [{
  "@id": "http://example.org/correspondence/letter001/correspondence",
  "@type": "cidoc:E7_Activity",
  "cidoc:P2_has_type": {
    "@id": "http://vocab.getty.edu/page/aat/300026877"
  }
}]
```

**2. Sender Linked**:
```json
"cidoc:P14_carried_out_by": [{
  "@id": "http://example.org/persons/john_merchant",
  "@type": "cidoc:E39_Actor"
}]
```

**3. Origin and Destination**:
```json
"cidoc:P7_took_place_at": {
  "@id": "http://example.org/places/venice",
  "@type": "cidoc:E53_Place"
},
"cidoc:P26_moved_to": {
  "@id": "http://example.org/places/cairo",
  "@type": "cidoc:E53_Place"
}
```

**4. Recipient Linked**:
```json
"cidoc:P01_has_domain": [{
  "@id": "http://example.org/persons/maria_trader",
  "@type": "cidoc:E39_Actor"
}]
```

**5. Nested Holding Activity**:
```json
"cidoc:P16_used_specific_object": [{
  "@id": "http://example.org/correspondence/letter001/holding_activity_0",
  "@type": "cidoc:E7_Activity",
  "cidoc:P2_has_type": {
    "@id": "http://vocab.getty.edu/page/aat/300077993"
  },
  "cidoc:P14_carried_out_by": {
    "@id": "http://example.org/persons/carlo_porter",
    "@type": "cidoc:E39_Actor"
  }
}]
```

**6. Event Reference**:
```json
"cidoc:P16_used_specific_object": [{
  "@id": "http://example.org/events/cargo_arrival",
  "@type": "cidoc:E5_Event"
}]
```

**✓ Checkpoint**: All six correspondence properties should be transformed correctly.

### 4.4 Test Edge Cases

Create and test these scenarios:

**Test 1: Minimal Correspondence** (sender and recipient only)
```json
{
  "@id": "http://example.org/correspondence/letter002",
  "@type": "gmn:E31_6_Correspondence",
  "gmn:P70_26_indicates_sender": {"@id": "http://example.org/persons/john"},
  "gmn:P70_28_indicates_recipient": {"@id": "http://example.org/persons/maria"}
}
```

**Expected**: Single correspondence activity with P14 and P01 properties only.

**Test 2: Multiple Holders**
```json
{
  "@id": "http://example.org/correspondence/letter003",
  "@type": "gmn:E31_6_Correspondence",
  "gmn:P70_26_indicates_sender": {"@id": "http://example.org/persons/john"},
  "gmn:P70_28_indicates_recipient": {"@id": "http://example.org/persons/maria"},
  "gmn:P70_29_indicates_holder_of_item": [
    {"@id": "http://example.org/persons/holder1"},
    {"@id": "http://example.org/persons/holder2"}
  ]
}
```

**Expected**: Two separate holding activities (holding_activity_0 and holding_activity_1).

**Test 3: P70.30 with Non-Correspondence Document**
```json
{
  "@id": "http://example.org/documents/report001",
  "@type": "cidoc:E31_Document",
  "gmn:P70_30_refers_to_described_event": {"@id": "http://example.org/events/meeting"}
}
```

**Expected**: Works correctly since P70.30 domain is E31_Document.

**✓ Checkpoint**: All edge cases transform without errors.

### 4.5 Validation Checklist

- [ ] All six properties transform correctly
- [ ] Shared correspondence activity created properly
- [ ] No duplicate activities for same correspondence
- [ ] URIs follow expected pattern
- [ ] Nested structures (holding, events) created correctly
- [ ] No Python errors or warnings
- [ ] Output validates as proper JSON-LD
- [ ] RDF graph can be parsed

---

## Troubleshooting

### Issue: "KeyError: 'gmn:P70_26_indicates_sender'"

**Cause**: Transformation function called but property not in data.

**Solution**: Each function checks `if property not in data: return data` at the start. Verify this check exists.

### Issue: Multiple correspondence activities created

**Cause**: Activity reuse logic not finding existing activity.

**Solution**: Verify the activity search logic:
```python
for activity in data['cidoc:P70_documents']:
    if isinstance(activity, dict) and activity.get('@id', '').endswith('/correspondence'):
        existing_activity = activity
        break
```

### Issue: Wrong AAT type on holding activity

**Cause**: Incorrect AAT URI.

**Solution**: Verify `AAT_HOLDING = "http://vocab.getty.edu/page/aat/300077993"` (if you added this constant, otherwise use the literal in the function).

### Issue: P70.30 not working with correspondence

**Cause**: Activity type mismatch.

**Solution**: P70.30 should work with any activity. Check that it's using the first available activity from `cidoc:P70_documents`.

### Issue: Nested holding activity not appearing

**Cause**: P16_used_specific_object not initialized.

**Solution**: Verify:
```python
if 'cidoc:P16_used_specific_object' not in existing_activity:
    existing_activity['cidoc:P16_used_specific_object'] = []
```

### Issue: Properties not being removed after transformation

**Cause**: Missing `del data['gmn:property_name']` statement.

**Solution**: Each function must end with deleting the shortcut property.

---

## Post-Implementation Checklist

- [ ] All files saved and backed up
- [ ] Test suite passes
- [ ] Documentation updated
- [ ] Team notified of new class/properties
- [ ] Example correspondence created in database
- [ ] Training materials updated (if applicable)
- [ ] Version control committed

---

## Next Steps

1. Begin using E31.6 Correspondence in data entry
2. Monitor transformation logs for errors
3. Collect feedback from users
4. Consider creating additional helper properties if needed

---

## Support Resources

- **Ontology Documentation**: See `ontology_documentation.md`
- **CIDOC-CRM Reference**: http://www.cidoc-crm.org/
- **AAT Browser**: http://vocab.getty.edu/

---

## Implementation Complete

Once all steps are completed and tests pass, your E31.6 Correspondence implementation is ready for production use.

**Version**: 1.0  
**Date**: 2025-10-18
