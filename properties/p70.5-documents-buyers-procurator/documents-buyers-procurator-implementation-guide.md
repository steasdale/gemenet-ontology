# Implementation Guide: P70.5 Documents Buyer's Procurator
## Step-by-Step Instructions for gmn:P70_5_documents_buyers_procurator

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Ontology Implementation](#ontology-implementation)
4. [Transformation Script Implementation](#transformation-script-implementation)
5. [Testing Procedures](#testing-procedures)
6. [Documentation Updates](#documentation-updates)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides complete instructions for implementing the `gmn:P70_5_documents_buyers_procurator` property in the GMN ontology system. This property documents procurators (legal representatives) acting on behalf of buyers in sales contracts.

### What You'll Implement

1. **Ontology Definition** - TTL property declaration
2. **Transformation Function** - Python code for CIDOC-CRM conversion
3. **Pipeline Integration** - Connection to main transformation flow
4. **Documentation** - Examples and usage guidance

### Expected Time

- Ontology addition: 5 minutes
- Transformation code: 15 minutes
- Testing: 20 minutes
- Documentation: 10 minutes
- **Total: ~50 minutes**

---

## Prerequisites

### Required Files

- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script

### Required Knowledge

- Basic understanding of RDF/TTL syntax
- Python programming fundamentals
- CIDOC-CRM concepts (E7_Activity, P14_carried_out_by, P17_was_motivated_by)
- JSON-LD structure

### Existing Dependencies

The transformation uses the generic `transform_procurator_property()` function, which should already exist for P70.4 (seller's procurator). If not present, you'll need to implement it (covered below).

---

## Ontology Implementation

### Step 1: Locate Insertion Point

Open `gmn_ontology.ttl` and find the sales contract properties section. Look for existing P70 properties (around line 800-900, after P70.4).

### Step 2: Add Property Definition

Insert the following TTL definition:

```turtle
# Property: P70.5 documents buyer's procurator
gmn:P70_5_documents_buyers_procurator
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.5 documents buyer's procurator"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the procurator (legal representative) for the buyer. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (procurator), with P17_was_motivated_by linking to the buyer (E21_Person). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The transformation creates an E7_Activity node that explicitly links the procurator to the buyer they represent via P17_was_motivated_by."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P17_was_motivated_by .
```

### Step 3: Verify Ontology Structure

Check that:
- [ ] Property URI follows naming convention (gmn:P70_5_documents_buyers_procurator)
- [ ] Label includes property number (P70.5)
- [ ] Comment explains transformation path
- [ ] Domain is gmn:E31_2_Sales_Contract
- [ ] Range is cidoc:E21_Person
- [ ] Superproperty is cidoc:P70_documents
- [ ] Created date is present
- [ ] See-also references are included

### Step 4: Validate TTL Syntax

```bash
# Use rapper or similar tool to validate
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Or use online validator
# Upload to: http://www.easyrdf.org/converter
```

---

## Transformation Script Implementation

### Step 5: Verify Generic Function Exists

Open `gmn_to_cidoc_transform.py` and search for `transform_procurator_property`. This generic function should already exist (used for P70.4). If not found, add it:

```python
def transform_procurator_property(data, property_name, motivated_by_property):
    """
    Generic function to transform procurator properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    
    Args:
        data: Item data dictionary
        property_name: The GMN property to transform (e.g., 'gmn:P70_5_documents_buyers_procurator')
        motivated_by_property: The CIDOC property linking to principal (e.g., 'cidoc:P22_transferred_title_to')
    
    Returns:
        Transformed data dictionary
    """
    if property_name not in data:
        return data
    
    procurators = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create acquisition if it doesn't exist
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P9_consists_of if needed
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Get the motivated_by person (seller or buyer)
    motivated_by_uri = None
    if motivated_by_property in acquisition:
        motivated_by_list = acquisition[motivated_by_property]
        if isinstance(motivated_by_list, list) and len(motivated_by_list) > 0:
            if isinstance(motivated_by_list[0], dict):
                motivated_by_uri = motivated_by_list[0].get('@id')
            else:
                motivated_by_uri = str(motivated_by_list[0])
    
    # Process each procurator
    for procurator_obj in procurators:
        if isinstance(procurator_obj, dict):
            procurator_uri = procurator_obj.get('@id', '')
            procurator_data = procurator_obj.copy()
        else:
            procurator_uri = str(procurator_obj)
            procurator_data = {
                '@id': procurator_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique activity URI
        activity_hash = str(hash(procurator_uri + property_name))[-8:]
        activity_uri = f"{subject_uri}/activity/procurator_{activity_hash}"
        
        # Create activity structure
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [procurator_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_AGENT,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Link to motivated_by person if available
        if motivated_by_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': motivated_by_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove simplified property
    del data[property_name]
    return data
```

### Step 6: Add Specific Transformation Function

Add the following function after the generic `transform_procurator_property` function:

```python
def transform_p70_5_documents_buyers_procurator(data):
    """Transform gmn:P70_5_documents_buyers_procurator to full CIDOC-CRM structure."""
    return transform_procurator_property(data, 'gmn:P70_5_documents_buyers_procurator', 
                                        'cidoc:P22_transferred_title_to')
```

### Step 7: Verify AAT Constant

Check that the AAT_AGENT constant is defined at the top of the file:

```python
# AAT vocabulary URIs for roles
AAT_AGENT = "http://vocab.getty.edu/aat/300411835"  # Agents (people in legal context)
AAT_GUARANTOR = "http://vocab.getty.edu/aat/300203988"  # Guarantors
```

If not present, add it near other AAT constants (typically around line 20-30).

### Step 8: Integrate into Main Pipeline

Locate the main transformation function (likely `transform_item` or similar). Add the transformation call in the appropriate section, after buyer transformation (P70.2) and before guarantor transformation (P70.7):

```python
def transform_item(item, include_internal=False):
    """
    Transform a single item from GMN shorthand to full CIDOC-CRM.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    
    Returns:
        Transformed item dictionary
    """
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)  # ADD THIS LINE
    item = transform_p70_6_documents_sellers_guarantor(item)
    item = transform_p70_7_documents_buyers_guarantor(item)
    # ... continue with other transformations ...
```

### Step 9: Import Required Modules

Ensure the uuid module is imported at the top of the file:

```python
from uuid import uuid4
```

---

## Testing Procedures

### Step 10: Create Test Data

Create a test file `test_buyers_procurator.json`:

```json
{
  "@context": {
    "gmn": "https://w3id.org/genoa-maritime-notarial/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "https://example.org/contract/test_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [{
    "@id": "https://example.org/person/buyer_001",
    "@type": "cidoc:E21_Person",
    "gmn:P1_1_has_name": "Giovanni de Marini"
  }],
  "gmn:P70_5_documents_buyers_procurator": [{
    "@id": "https://example.org/person/procurator_001",
    "@type": "cidoc:E21_Person",
    "gmn:P1_1_has_name": "Oberto Spinola"
  }]
}
```

### Step 11: Run Transformation Test

```python
# Test script
import json
from gmn_to_cidoc_transform import transform_item

# Load test data
with open('test_buyers_procurator.json', 'r') as f:
    test_data = json.load(f)

# Transform
transformed = transform_item(test_data)

# Output
print(json.dumps(transformed, indent=2))
```

### Step 12: Verify Transformation Output

Check that the output contains:

1. **E8_Acquisition created**:
```json
"cidoc:P70_documents": [{
  "@id": "https://example.org/contract/test_001/acquisition",
  "@type": "cidoc:E8_Acquisition"
}]
```

2. **Buyer linked via P22**:
```json
"cidoc:P22_transferred_title_to": [{
  "@id": "https://example.org/person/buyer_001",
  "@type": "cidoc:E21_Person"
}]
```

3. **E7_Activity created**:
```json
"cidoc:P9_consists_of": [{
  "@id": "https://example.org/contract/test_001/activity/procurator_[hash]",
  "@type": "cidoc:E7_Activity"
}]
```

4. **Procurator linked via P14**:
```json
"cidoc:P14_carried_out_by": [{
  "@id": "https://example.org/person/procurator_001",
  "@type": "cidoc:E21_Person"
}]
```

5. **Role specified via P14.1**:
```json
"cidoc:P14.1_in_the_role_of": {
  "@id": "http://vocab.getty.edu/aat/300411835",
  "@type": "cidoc:E55_Type"
}
```

6. **Buyer linked via P17**:
```json
"cidoc:P17_was_motivated_by": {
  "@id": "https://example.org/person/buyer_001",
  "@type": "cidoc:E21_Person"
}
```

7. **Original property removed**:
   - `gmn:P70_5_documents_buyers_procurator` should NOT appear in output

### Step 13: Test Edge Cases

#### Test 1: Multiple Procurators

```json
{
  "@id": "https://example.org/contract/test_002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [{
    "@id": "https://example.org/person/buyer_002"
  }],
  "gmn:P70_5_documents_buyers_procurator": [
    {"@id": "https://example.org/person/procurator_001"},
    {"@id": "https://example.org/person/procurator_002"}
  ]
}
```

**Expected:** Two separate E7_Activity instances created, each linking to the same buyer.

#### Test 2: No Buyer Present

```json
{
  "@id": "https://example.org/contract/test_003",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_5_documents_buyers_procurator": [{
    "@id": "https://example.org/person/procurator_001"
  }]
}
```

**Expected:** Activity created without P17_was_motivated_by (no buyer to link to).

#### Test 3: Empty Procurator List

```json
{
  "@id": "https://example.org/contract/test_004",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_5_documents_buyers_procurator": []
}
```

**Expected:** Property removed, no activities created.

### Step 14: Integration Testing

Test with complete contract:

```json
{
  "@id": "https://example.org/contract/complete_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [{
    "@id": "https://example.org/person/seller_001"
  }],
  "gmn:P70_2_documents_buyer": [{
    "@id": "https://example.org/person/buyer_001"
  }],
  "gmn:P70_3_documents_transfer_of": [{
    "@id": "https://example.org/property/house_001"
  }],
  "gmn:P70_4_documents_sellers_procurator": [{
    "@id": "https://example.org/person/seller_procurator_001"
  }],
  "gmn:P70_5_documents_buyers_procurator": [{
    "@id": "https://example.org/person/buyer_procurator_001"
  }]
}
```

**Expected:** 
- One E8_Acquisition
- Seller linked via P23_transferred_title_from
- Buyer linked via P22_transferred_title_to
- Property linked via P24_transferred_title_of
- Two E7_Activities in P9_consists_of (one for each procurator)
- Each activity properly linked to respective principal party

---

## Documentation Updates

### Step 15: Add Property Description

Add to your main documentation file (e.g., `correspondence-documentation.md` or similar):

```markdown
### P70.5 documents buyer's procurator

**URI:** `gmn:P70_5_documents_buyers_procurator`  
**Label:** "P70.5 documents buyer's procurator"  
**Domain:** `gmn:E31_2_Sales_Contract`  
**Range:** `cidoc:E21_Person`

Documents the procurator (legal representative) acting on behalf of the buyer in a sales contract. The procurator has legal authority to act for the buyer and make binding decisions in the transaction.

**CIDOC-CRM Transformation:**
```
E31_Document → P70_documents → E8_Acquisition → P9_consists_of → E7_Activity
  → P14_carried_out_by → E21_Person (procurator)
  → P14.1_in_the_role_of → E55_Type (AAT: agent)
  → P17_was_motivated_by → E21_Person (buyer)
```

**Example:**
```json
{
  "@id": "contract123",
  "gmn:P70_5_documents_buyers_procurator": [{
    "@id": "person456",
    "gmn:P1_1_has_name": "Oberto Spinola"
  }]
}
```
```

### Step 16: Add Historical Context

```markdown
#### Historical Usage: Procurators in Genoese Contracts

Procurators (Latin: *procurator*, Italian: *procuratore*) were essential in medieval commercial transactions. In Genoa, buyers commonly appointed procurators for several reasons:

- **Absence:** Buyers conducting business elsewhere needed representation
- **Illness:** Incapacity prevented personal appearance before the notary
- **Social Status:** High-status individuals might use agents for routine transactions
- **Professional Management:** Merchants employed professional agents
- **Family Affairs:** Family members represented relatives in property transactions

The procurator held legal power of attorney (*procura*) documented in separate instruments, enabling them to bind their principals to contracts.
```

---

## Troubleshooting

### Common Issues

#### Issue 1: AttributeError - 'str' object has no attribute 'get'

**Cause:** Procurator value is a string URI, not a dictionary.

**Solution:** The transformation function handles both formats. Ensure this section is present:

```python
if isinstance(procurator_obj, dict):
    procurator_uri = procurator_obj.get('@id', '')
    procurator_data = procurator_obj.copy()
else:
    procurator_uri = str(procurator_obj)
    procurator_data = {
        '@id': procurator_uri,
        '@type': 'cidoc:E21_Person'
    }
```

#### Issue 2: NameError - AAT_AGENT is not defined

**Cause:** AAT constant not defined or not imported.

**Solution:** Add constant at module level:

```python
AAT_AGENT = "http://vocab.getty.edu/aat/300411835"
```

#### Issue 3: KeyError - 'cidoc:P22_transferred_title_to'

**Cause:** Buyer not transformed before procurator transformation.

**Solution:** Ensure transformation order in pipeline:
```python
item = transform_p70_2_documents_buyer(item)  # MUST come before
item = transform_p70_5_documents_buyers_procurator(item)  # procurator transformation
```

#### Issue 4: Multiple acquisitions created

**Cause:** Acquisition check failing.

**Solution:** Verify acquisition check logic:

```python
if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
    # Create new acquisition
```

#### Issue 5: Activity URIs not unique

**Cause:** Hash collision or improper URI generation.

**Solution:** Verify hash generation includes both procurator URI and property name:

```python
activity_hash = str(hash(procurator_uri + property_name))[-8:]
```

### Validation Checklist

After implementation, verify:

- [ ] TTL syntax is valid
- [ ] Property appears in ontology correctly
- [ ] Transformation function executes without errors
- [ ] E8_Acquisition is created or reused properly
- [ ] E7_Activity receives unique URI
- [ ] P14_carried_out_by links to procurator
- [ ] P14.1_in_the_role_of specifies agent role
- [ ] P17_was_motivated_by links to buyer (when present)
- [ ] Original simplified property is removed
- [ ] Multiple procurators create multiple activities
- [ ] Function integrated in main pipeline
- [ ] Documentation is updated

---

## Next Steps

1. **Deploy to Production**
   - Merge changes to main branch
   - Update production ontology file
   - Deploy transformation script

2. **Update Data Entry Tools**
   - Add P70.5 to data entry forms
   - Provide dropdown or autocomplete for procurators
   - Include validation rules

3. **Train Users**
   - Document when to use procurator vs. buyer
   - Explain difference from guarantor (P70.7) and payment provider (P70.9)
   - Provide historical examples

4. **Monitor Usage**
   - Track property usage statistics
   - Collect user feedback
   - Identify additional use cases

---

## Additional Resources

- **CIDOC-CRM Specification:** http://www.cidoc-crm.org/
- **Getty AAT:** http://vocab.getty.edu/aat/
- **RDF/TTL Tutorial:** https://www.w3.org/TR/turtle/
- **JSON-LD Spec:** https://www.w3.org/TR/json-ld/

---

**Implementation Guide Version:** 1.0  
**Last Updated:** 2025-10-27  
**Property Version:** 1.0 (created 2025-10-17)
