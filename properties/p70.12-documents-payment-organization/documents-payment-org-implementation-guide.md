# GMN Ontology: P70.12 Documents Payment Through Organization
## Implementation Guide

This guide provides step-by-step instructions for implementing the `gmn:P70_12_documents_payment_through_organization` property in the GMN ontology and transformation pipeline.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Ontology Updates](#phase-1-ontology-updates)
4. [Phase 2: Transformation Script Updates](#phase-2-transformation-script-updates)
5. [Phase 3: Documentation Updates](#phase-3-documentation-updates)
6. [Phase 4: Testing](#phase-4-testing)
7. [Troubleshooting](#troubleshooting)

---

## Overview

### What You're Implementing

The `gmn:P70_12_documents_payment_through_organization` property enables sales contracts to reference organizations (typically banks or financial institutions) through which payment is made or facilitated.

### Implementation Scope

- **Ontology file:** Add property definition to `gmn_ontology.ttl`
- **Transformation script:** Add function to `gmn_to_cidoc_transform.py`
- **Documentation:** Add examples and tables to main documentation files

### Estimated Time
- **Total:** 1-2 hours
- **Ontology:** 15 minutes
- **Transformation:** 30 minutes
- **Testing:** 30-45 minutes
- **Documentation:** 15-30 minutes

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script
- Project documentation files (correspondence, donation, dowry docs)

### Required Knowledge
- Basic understanding of RDF/TTL syntax
- Python programming fundamentals
- CIDOC-CRM concepts (particularly P67_refers_to)
- Understanding of E74_Group class

### Development Environment
- Text editor with TTL syntax support
- Python 3.x environment
- Git for version control
- TTL validator (optional but recommended)

---

## Phase 1: Ontology Updates

### Step 1.1: Locate the Property Definition Section

Open `gmn_ontology.ttl` and find the section containing P70 property definitions. Look for:

```turtle
# Property: P70.11 documents referenced person
gmn:P70_11_documents_referenced_person
    a owl:ObjectProperty ;
    ...
```

The P70.12 property should be added immediately after P70.11.

### Step 1.2: Add the Property Definition

Insert the following TTL code:

```turtle
# Property: P70.12 documents payment through organization
gmn:P70_12_documents_payment_through_organization
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.12 documents payment through organization"@en ;
    rdfs:comment "Simplified property for associating a sales contract with an organization (typically a bank) through which payment for the transaction is made or facilitated. This captures financial institutions that serve as intermediaries in the payment process, such as banks holding deposits, making transfers, or providing credit facilities for the transaction. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E74_Group, where the E7_Activity represents the payment facilitation activity. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The organization facilitates the financial aspects of the transaction without being a principal party (buyer/seller) or individual agent (procurator/guarantor)."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E74_Group ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

### Step 1.3: Validate the TTL Syntax

Run a TTL validator to check for syntax errors:

```bash
# Using rapper (if installed)
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Or use an online validator like:
# http://ttl.summerofcode.be/
```

### Step 1.4: Commit Changes

```bash
git add gmn_ontology.ttl
git commit -m "Add P70.12 documents payment through organization property"
```

---

## Phase 2: Transformation Script Updates

### Step 2.1: Locate the Transformation Function Section

Open `gmn_to_cidoc_transform.py` and find the P70.11 transformation function:

```python
def transform_p70_11_documents_referenced_person(data):
    """
    Transform gmn:P70_11_documents_referenced_person to full CIDOC-CRM structure:
    P67_refers_to > E21_Person
    """
    ...
```

The P70.12 function should be added immediately after this function.

### Step 2.2: Add the Transformation Function

Insert the following Python code:

```python
def transform_p70_12_documents_payment_through_organization(data):
    """
    Transform gmn:P70_12_documents_payment_through_organization to full CIDOC-CRM structure:
    P67_refers_to > E74_Group
    """
    if 'gmn:P70_12_documents_payment_through_organization' not in data:
        return data
    
    organizations = data['gmn:P70_12_documents_payment_through_organization']
    
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    for org_obj in organizations:
        if isinstance(org_obj, dict):
            org_data = org_obj.copy()
            if '@type' not in org_data:
                org_data['@type'] = 'cidoc:E74_Group'
        else:
            org_uri = str(org_obj)
            org_data = {
                '@id': org_uri,
                '@type': 'cidoc:E74_Group'
            }
        
        data['cidoc:P67_refers_to'].append(org_data)
    
    del data['gmn:P70_12_documents_payment_through_organization']
    return data
```

### Step 2.3: Add Function Call to Pipeline

Locate the `transform_gmn_to_cidoc()` function and find the section with P70 property transformations:

```python
def transform_gmn_to_cidoc(item, include_internal=False):
    """
    Transform GMN shortcut properties to full CIDOC-CRM structure.
    ...
    """
    # ... earlier transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)
    item = transform_p70_7_documents_buyers_guarantor(item)
    item = transform_p70_8_documents_broker(item)
    item = transform_p70_9_documents_payment_provider_for_buyer(item)
    item = transform_p70_10_documents_payment_recipient_for_seller(item)
    item = transform_p70_11_documents_referenced_person(item)
    item = transform_p70_12_documents_payment_through_organization(item)  # ADD THIS LINE
    item = transform_p70_13_documents_referenced_place(item)
    # ... rest of pipeline ...
```

**Critical:** Ensure the function call is in the correct position (after P70.11, before P70.13).

### Step 2.4: Verify Import Statements

Check that necessary imports are present at the top of the file:

```python
import json
from copy import deepcopy
from typing import Dict, Any, List, Union
```

### Step 2.5: Test the Function in Isolation

Create a test script to verify the function works correctly:

```python
# test_p70_12.py
from gmn_to_cidoc_transform import transform_p70_12_documents_payment_through_organization

# Test 1: Organization URI reference
test_data_1 = {
    '@id': 'http://example.org/contract/001',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_12_documents_payment_through_organization': [
        'http://example.org/organization/banco_san_giorgio'
    ]
}

result_1 = transform_p70_12_documents_payment_through_organization(test_data_1)
print("Test 1 - URI reference:")
print(json.dumps(result_1, indent=2))
print()

# Test 2: Inline organization data
test_data_2 = {
    '@id': 'http://example.org/contract/002',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_12_documents_payment_through_organization': [
        {
            '@id': 'http://example.org/organization/banco_san_giorgio',
            'cidoc:P1_is_identified_by': {
                '@type': 'cidoc:E41_Appellation',
                'cidoc:P190_has_symbolic_content': 'Banco di San Giorgio'
            }
        }
    ]
}

result_2 = transform_p70_12_documents_payment_through_organization(test_data_2)
print("Test 2 - Inline data:")
print(json.dumps(result_2, indent=2))
print()

# Test 3: Multiple organizations
test_data_3 = {
    '@id': 'http://example.org/contract/003',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_12_documents_payment_through_organization': [
        'http://example.org/organization/banco_san_giorgio',
        'http://example.org/organization/casa_credito_genova'
    ]
}

result_3 = transform_p70_12_documents_payment_through_organization(test_data_3)
print("Test 3 - Multiple organizations:")
print(json.dumps(result_3, indent=2))
```

Run the test:

```bash
python test_p70_12.py
```

---

## Phase 3: Documentation Updates

### Step 3.1: Update Main Documentation Files

The property should be documented in:
- **correspondence-documentation.md** (if applicable)
- **donation-documentation.md** (if applicable)
- **dowry-documentation.md** (if applicable)
- Any sales contract documentation files

### Step 3.2: Add Property Description

Add a section describing the property:

```markdown
### P70.12 documents payment through organization

**URI:** `http://www.genoesemerchantnetworks.com/ontology#P70_12_documents_payment_through_organization`

**Label:** P70.12 documents payment through organization

**Definition:** Simplified property for associating a sales contract with an organization (typically a bank) through which payment for the transaction is made or facilitated.

**Domain:** gmn:E31_2_Sales_Contract

**Range:** cidoc:E74_Group

**Superproperty:** cidoc:P70_documents

**Full CIDOC-CRM Path:**
```
E31_Document 
  → P70_documents 
    → E8_Acquisition 
      → P9_consists_of 
        → E7_Activity (payment facilitation)
          → P14_carried_out_by 
            → E74_Group
```

**Note:** Current implementation uses P67_refers_to for referenced organizations.

**Cardinality:** Zero or many (multiple organizations may be involved)

**Usage Notes:**

- Captures financial institutions that serve as payment intermediaries
- Includes banks holding deposits, making transfers, or providing credit
- Distinct from individual payment providers (P70.9) and recipients (P70.10)
- Organizations are referenced but not active transaction participants

**Example:**
```turtle
:contract_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_12_documents_payment_through_organization :banco_san_giorgio .
```
```

### Step 3.3: Add to Property Index/Table

If your documentation includes a property index, add an entry:

```
| Property | Label | Domain | Range |
|----------|-------|--------|-------|
| ... | ... | ... | ... |
| gmn:P70_12 | documents payment through organization | E31_2_Sales_Contract | E74_Group |
| ... | ... | ... | ... |
```

---

## Phase 4: Testing

### Step 4.1: Create Test Data Files

Create comprehensive test cases:

```json
// test_p70_12_complete.json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@graph": [
    {
      "@id": "http://example.org/contract/test_001",
      "@type": "gmn:E31_2_Sales_Contract",
      "gmn:P70_1_documents_seller": {
        "@id": "http://example.org/person/giovanni_doria",
        "@type": "cidoc:E21_Person"
      },
      "gmn:P70_2_documents_buyer": {
        "@id": "http://example.org/person/pietro_spinola",
        "@type": "cidoc:E21_Person"
      },
      "gmn:P70_12_documents_payment_through_organization": [
        {
          "@id": "http://example.org/organization/banco_san_giorgio",
          "@type": "cidoc:E74_Group",
          "cidoc:P1_is_identified_by": {
            "@type": "cidoc:E41_Appellation",
            "cidoc:P190_has_symbolic_content": "Banco di San Giorgio"
          }
        }
      ]
    },
    {
      "@id": "http://example.org/contract/test_002",
      "@type": "gmn:E31_2_Sales_Contract",
      "gmn:P70_12_documents_payment_through_organization": [
        "http://example.org/organization/banco_san_giorgio",
        "http://example.org/organization/casa_credito_genova"
      ]
    }
  ]
}
```

### Step 4.2: Run Transformation

```python
# test_transformation.py
import json
from gmn_to_cidoc_transform import transform_gmn_to_cidoc

with open('test_p70_12_complete.json', 'r') as f:
    test_data = json.load(f)

for item in test_data['@graph']:
    print(f"Original: {item['@id']}")
    print(json.dumps(item, indent=2))
    
    transformed = transform_gmn_to_cidoc(item)
    
    print(f"\nTransformed: {item['@id']}")
    print(json.dumps(transformed, indent=2))
    print("\n" + "="*80 + "\n")
```

### Step 4.3: Verify Transformation Results

Check that the output includes:

1. **P67_refers_to property created:**
   ```json
   "cidoc:P67_refers_to": [...]
   ```

2. **E74_Group type preserved:**
   ```json
   {
     "@id": "...",
     "@type": "cidoc:E74_Group",
     ...
   }
   ```

3. **Original property removed:**
   - `gmn:P70_12_documents_payment_through_organization` should not appear in output

4. **Additional organization data preserved:**
   - Names, identifiers, and other properties should remain intact

### Step 4.4: Test Edge Cases

Test these scenarios:

1. **Empty organization list:**
   ```json
   "gmn:P70_12_documents_payment_through_organization": []
   ```

2. **Single organization:**
   ```json
   "gmn:P70_12_documents_payment_through_organization": [
     "http://example.org/organization/banco"
   ]
   ```

3. **Multiple organizations:**
   ```json
   "gmn:P70_12_documents_payment_through_organization": [
     "http://example.org/org1",
     "http://example.org/org2"
   ]
   ```

4. **Mixed URI and object references:**
   ```json
   "gmn:P70_12_documents_payment_through_organization": [
     "http://example.org/org1",
     {
       "@id": "http://example.org/org2",
       "cidoc:P1_is_identified_by": {...}
     }
   ]
   ```

5. **Organization with existing P67_refers_to:**
   Test that organizations are appended to existing P67 list

### Step 4.5: Validate Against CIDOC-CRM

Verify that:
- E74_Group is a valid CIDOC-CRM class
- P67_refers_to is correctly applied to E31_Document domain
- All property paths are valid according to CIDOC-CRM specifications

---

## Troubleshooting

### Issue: TTL Syntax Error

**Symptom:** Validator reports parsing errors

**Solution:**
- Check for missing semicolons or periods
- Verify all IRIs are properly enclosed in angle brackets
- Ensure all string literals have language tags (`@en`)
- Check that prefixes are correctly defined

### Issue: Transformation Function Not Called

**Symptom:** GMN property still present in output

**Solution:**
- Verify function is added to `transform_gmn_to_cidoc()` pipeline
- Check function name spelling matches exactly
- Ensure function is called in correct order
- Add debug print statements to verify execution

### Issue: TypeError in Transformation

**Symptom:** Python raises TypeError when processing organizations

**Solution:**
- Check that organizations variable is always treated as a list
- Verify proper handling of both dict and string formats
- Add type checking with `isinstance()` calls
- Handle edge case of single value vs. list

### Issue: E74_Group Type Not Added

**Symptom:** Organizations missing @type after transformation

**Solution:**
- Check the type assignment logic: `org_data['@type'] = 'cidoc:E74_Group'`
- Verify it's applied in both URI and dict branches
- Test with debug output to see intermediate values

### Issue: Existing P67_refers_to Overwritten

**Symptom:** Previous P67_refers_to values disappear

**Solution:**
- Check initialization: `if 'cidoc:P67_refers_to' not in data:`
- Ensure `.append()` is used, not assignment
- Verify no code deletes P67_refers_to elsewhere

### Issue: Organizations Not Appearing in Output

**Symptom:** P67_refers_to is empty or missing

**Solution:**
- Add debug print before and after transformation
- Check that organizations list is not empty
- Verify proper iteration over organizations
- Test with simple minimal example first

---

## Validation Checklist

Before considering implementation complete, verify:

- [ ] TTL definition added to ontology file
- [ ] TTL syntax validates without errors
- [ ] Transformation function added to script
- [ ] Function called in correct position in pipeline
- [ ] Function handles URI references correctly
- [ ] Function handles inline object data correctly
- [ ] Function handles multiple organizations
- [ ] Function preserves additional organization properties
- [ ] E74_Group type is correctly applied
- [ ] P67_refers_to relationship is created
- [ ] Original property is removed after transformation
- [ ] Documentation updated with examples
- [ ] All tests pass successfully
- [ ] Changes committed to version control

---

## Next Steps

After successful implementation:

1. **Update Related Properties:**
   - Review P70.11 (referenced persons)
   - Review P70.13 (referenced places)
   - Ensure consistent reference handling

2. **Data Migration:**
   - Plan migration for existing data
   - Create data entry guidelines
   - Train catalogers on new property

3. **Performance Testing:**
   - Test with large datasets
   - Profile transformation performance
   - Optimize if necessary

4. **Integration Testing:**
   - Test with full transformation pipeline
   - Verify integration with other P70 properties
   - Test round-trip data preservation

---

## Support Resources

- **CIDOC-CRM Documentation:** http://www.cidoc-crm.org/
- **E74_Group Definition:** CIDOC-CRM specification section for social entities
- **P67_refers_to Definition:** CIDOC-CRM specification section for reference properties
- **GMN Project Documentation:** [Project documentation location]
- **Issue Tracker:** [Project issue tracker URL]

---

*Implementation Guide Version 1.0 - Created 2025-10-27*
