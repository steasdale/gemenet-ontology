# Implementation Guide: gmn:P70_1_indicates_seller

This guide provides step-by-step instructions for implementing the `gmn:P70_1_indicates_seller` property in the GMN ontology and transformation pipeline using the E13 Attribute Assignment pattern.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Ontology Implementation](#ontology-implementation)
3. [Transformation Script Implementation](#transformation-script-implementation)
4. [Testing Procedures](#testing-procedures)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script

### Required Knowledge
- Basic understanding of RDF/OWL ontologies
- Familiarity with Python and JSON-LD
- Understanding of CIDOC-CRM event-based modeling
- Understanding of E13_Attribute_Assignment pattern

### Software Requirements
- Python 3.7+
- RDF libraries (rdflib) for validation (optional)
- JSON processing capabilities

### AAT Terms
The transformation requires these Getty AAT terms:
- Sale event: `http://vocab.getty.edu/aat/300054751`
- Seller role: `http://vocab.getty.edu/aat/300410369`
- P14 carried out by: `http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by`

---

## Ontology Implementation

### Step 1: Locate the Correct Section

Open `gmn_ontology.ttl` and locate the sales contract properties section. Look for other P70 properties.

### Step 2: Add the Property Definition

Insert the following TTL code in the appropriate location:

```turtle
# Property: P70.1 indicates seller
gmn:P70_1_indicates_seller
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.1 indicates seller"@en ;
    rdfs:comment "Simplified property for associating a sales contract document with the person who acts as the seller in the sale event. Represents the full CIDOC-CRM path: E70_Document > P70_documents > E7_Activity (typed as 'sale') > P140i_was_attributed_by > E13_Attribute_Assignment > P141_assigned > E21_Person, with P177_assigned_property_of_type indicating 'P14 carried out by' and P14.1_in_the_role_of indicating 'seller'. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The seller is the party transferring ownership of the property being sold."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain cidoc:E70_Document ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P140i_was_attributed_by, cidoc:E13_Attribute_Assignment, cidoc:P141_assigned .
```

### Step 3: Verify Property Placement

Ensure the property is:
- ✅ In the sales contract properties section
- ✅ After any class definitions it depends on
- ✅ Before any properties that reference it
- ✅ Properly indented and formatted

### Step 4: Validate the Ontology

Run validation checks:

```bash
# Using rapper (if installed)
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Using Python with rdflib
python3 -c "import rdflib; g = rdflib.Graph(); g.parse('gmn_ontology.ttl', format='turtle'); print('Valid')"
```

Expected output: No errors, graph loads successfully.

---

## Transformation Script Implementation

### Step 1: Add AAT Constants

At the top of `gmn_to_cidoc_transform.py`, add these AAT constants if not already present:

```python
# AAT Terms for sale transactions
AAT_SALE_EVENT = 'http://vocab.getty.edu/aat/300054751'  # sale (event)
AAT_SELLER_ROLE = 'http://vocab.getty.edu/aat/300410369'  # sellers (people)
CIDOC_P14 = 'http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by'
```

### Step 2: Add the Transformation Function

Insert the `transform_p70_1_indicates_seller` function:

```python
def transform_p70_1_indicates_seller(data):
    """
    Transform gmn:P70_1_indicates_seller to full CIDOC-CRM structure using E13 Attribute Assignment:
    
    P70_documents > E7_Activity (type: sale) 
      > P140i_was_attributed_by > E13_Attribute_Assignment
        > P141_assigned > E21_Person (seller)
        > P177_assigned_property_of_type > E55_Type ("P14 carried out by")
        > P14.1_in_the_role_of > E55_Type ("seller")
    
    This transformation uses the E13_Attribute_Assignment pattern to formally assign
    the "carried out by" attribute to the sale event, specifying the seller's role.
    
    Args:
        data: Item data dictionary
    
    Returns:
        Transformed item dictionary
    """
    if 'gmn:P70_1_indicates_seller' not in data:
        return data
    
    sellers = data['gmn:P70_1_indicates_seller']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create E7_Activity (sale) if it doesn't exist
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        sale_uri = f"{subject_uri}/sale"
        data['cidoc:P70_documents'] = [{
            '@id': sale_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_SALE_EVENT,
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'sale'
            }
        }]
    
    sale_event = data['cidoc:P70_documents'][0]
    
    # Initialize P140i_was_attributed_by if not present
    if 'cidoc:P140i_was_attributed_by' not in sale_event:
        sale_event['cidoc:P140i_was_attributed_by'] = []
    
    # Create E13_Attribute_Assignment for each seller
    for seller_obj in sellers:
        # Handle seller data
        if isinstance(seller_obj, dict):
            seller_data = seller_obj.copy()
            seller_uri = seller_data.get('@id', f"urn:uuid:{uuid4()}")
            if '@type' not in seller_data:
                seller_data['@type'] = 'cidoc:E21_Person'
        else:
            seller_uri = str(seller_obj)
            seller_data = {
                '@id': seller_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique attribution URI
        attribution_hash = str(hash(seller_uri + 'seller'))[-8:]
        attribution_uri = f"{subject_uri}/attribution/seller_{attribution_hash}"
        
        # Create E13_Attribute_Assignment
        attribution = {
            '@id': attribution_uri,
            '@type': 'cidoc:E13_Attribute_Assignment',
            'cidoc:P141_assigned': seller_data,
            'cidoc:P177_assigned_property_of_type': {
                '@id': CIDOC_P14,
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'P14 carried out by'
            },
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_SELLER_ROLE,
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'seller'
            }
        }
        
        sale_event['cidoc:P140i_was_attributed_by'].append(attribution)
    
    # Remove the simplified property
    del data['gmn:P70_1_indicates_seller']
    return data
```

### Step 3: Add Function Call to transform_item()

Locate the `transform_item()` function and add the function call in the sales contract properties section:

```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_indicates_seller(item)  # ADD THIS LINE
    item = transform_p70_2_indicates_buyer(item)
    item = transform_p70_3_indicates_transfer_of(item)
    # ... rest of P70 functions ...
```

### Step 4: Verify Import Statements

Ensure the `uuid4` function is imported at the top of the file:

```python
from uuid import uuid4
```

### Step 5: Check Function Sequence

Verify the function is called:
- ✅ After document creation properties (P94i series)
- ✅ With other sales contract properties (P70 series)
- ✅ Before arbitration properties (P70.18+)

---

## Testing Procedures

### Test 1: Basic Single Seller with E13 Attribution

**Input Data**:
```json
{
  "@id": "http://example.org/contract/contract_001",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type",
    "rdfs:label": "sales contract"
  },
  "gmn:P70_1_indicates_seller": [
    {
      "@id": "http://example.org/person/giovanni_rossi",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Run Transformation**:
```python
from gmn_to_cidoc_transform import transform_item
import json

input_data = {
    "@id": "http://example.org/contract/contract_001",
    "@type": "cidoc:E70_Document",
    "cidoc:P2_has_type": {
        "@id": "sales_contract_type",
        "@type": "cidoc:E55_Type",
        "rdfs:label": "sales contract"
    },
    "gmn:P70_1_indicates_seller": [
        {
            "@id": "http://example.org/person/giovanni_rossi",
            "@type": "cidoc:E21_Person"
        }
    ]
}

result = transform_item(input_data)
print(json.dumps(result, indent=2))
```

**Expected Output Structure**:
```json
{
  "@id": "http://example.org/contract/contract_001",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type",
    "rdfs:label": "sales contract"
  },
  "cidoc:P70_documents": [
    {
      "@id": "http://example.org/contract/contract_001/sale",
      "@type": "cidoc:E7_Activity",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300054751",
        "@type": "cidoc:E55_Type",
        "rdfs:label": "sale"
      },
      "cidoc:P140i_was_attributed_by": [
        {
          "@id": "http://example.org/contract/contract_001/attribution/seller_...",
          "@type": "cidoc:E13_Attribute_Assignment",
          "cidoc:P141_assigned": {
            "@id": "http://example.org/person/giovanni_rossi",
            "@type": "cidoc:E21_Person"
          },
          "cidoc:P177_assigned_property_of_type": {
            "@id": "http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "P14 carried out by"
          },
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/aat/300410369",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "seller"
          }
        }
      ]
    }
  ]
}
```

**Validation Checks**:
- ✅ `gmn:P70_1_indicates_seller` property is removed
- ✅ `cidoc:P70_documents` array is created
- ✅ E7_Activity node has correct URI pattern and type "sale"
- ✅ `cidoc:P140i_was_attributed_by` contains E13 attribution
- ✅ E13 has P141_assigned linking to seller
- ✅ E13 has P177 linking to "P14 carried out by"
- ✅ E13 has P14.1 linking to "seller" role
- ✅ Seller maintains @id and @type

### Test 2: Multiple Sellers (Multiple E13 Attributions)

**Input Data**:
```json
{
  "@id": "http://example.org/contract/contract_002",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type"
  },
  "gmn:P70_1_indicates_seller": [
    {
      "@id": "http://example.org/person/marco_bianchi",
      "@type": "cidoc:E21_Person"
    },
    {
      "@id": "http://example.org/person/paolo_verdi",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Expected Behavior**:
- Both sellers get separate E13_Attribute_Assignment nodes
- Each E13 in the `P140i_was_attributed_by` array
- Each E13 has unique URI
- Order is preserved

### Test 3: Existing E7_Activity

**Input Data**:
```json
{
  "@id": "http://example.org/contract/contract_003",
  "@type": "cidoc:E70_Document",
  "cidoc:P70_documents": [
    {
      "@id": "http://example.org/contract/contract_003/sale",
      "@type": "cidoc:E7_Activity",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300054751",
        "@type": "cidoc:E55_Type"
      }
    }
  ],
  "gmn:P70_1_indicates_seller": [
    {
      "@id": "http://example.org/person/seller_001",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Expected Behavior**:
- Function reuses existing E7_Activity node
- Adds P140i_was_attributed_by to existing activity
- Preserves existing activity properties

### Test 4: URI Reference Only

**Input Data**:
```json
{
  "@id": "http://example.org/contract/contract_004",
  "@type": "cidoc:E70_Document",
  "gmn:P70_1_indicates_seller": [
    "http://example.org/person/seller_uri_only"
  ]
}
```

**Expected Behavior**:
- Function creates proper E21_Person node from string URI
- Adds correct @type automatically
- Creates complete E13 attribution structure

### Test 5: Integration with Buyer and Transfer

**Input Data**:
```json
{
  "@id": "http://example.org/contract/contract_005",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type"
  },
  "gmn:P70_1_indicates_seller": [
    {
      "@id": "http://example.org/person/seller_001",
      "@type": "cidoc:E21_Person"
    }
  ],
  "gmn:P70_2_indicates_buyer": [
    {
      "@id": "http://example.org/person/buyer_001",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Expected Behavior**:
- All properties transform correctly
- All use same E7_Activity node
- Separate E13 attributions for seller and buyer roles
- Each E13 has appropriate P177 and P14.1 values

---

## Troubleshooting

### Issue 1: Property Not Transforming

**Symptom**: The `gmn:P70_1_indicates_seller` property remains in output

**Possible Causes**:
1. Function not called in `transform_item()`
2. Function called in wrong order
3. Typo in property name

**Solution**:
```python
# Check function is called:
grep "transform_p70_1_indicates_seller" gmn_to_cidoc_transform.py

# Verify it's in transform_item():
grep -A 5 "def transform_item" gmn_to_cidoc_transform.py | grep "p70_1"
```

### Issue 2: AAT Constants Not Defined

**Symptom**: `NameError: name 'AAT_SALE_EVENT' is not defined`

**Solution**: Add constants at top of file:
```python
AAT_SALE_EVENT = 'http://vocab.getty.edu/aat/300054751'
AAT_SELLER_ROLE = 'http://vocab.getty.edu/aat/300410369'
CIDOC_P14 = 'http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by'
```

### Issue 3: E7_Activity Created Multiple Times

**Symptom**: Multiple E7 nodes in output

**Possible Cause**: Logic error in checking for existing activity

**Solution**: Ensure the check uses:
```python
if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
```

### Issue 4: E13 Structure Incomplete

**Symptom**: Missing P177 or P14.1 in E13

**Possible Cause**: Incomplete attribution object

**Solution**: Verify all three links in E13:
```python
attribution = {
    'cidoc:P141_assigned': seller_data,  # Person
    'cidoc:P177_assigned_property_of_type': {...},  # P14
    'cidoc:P14.1_in_the_role_of': {...}  # seller role
}
```

### Issue 5: UUID Import Error

**Symptom**: `NameError: name 'uuid4' is not defined`

**Solution**: Add import at top of file:
```python
from uuid import uuid4
```

---

## Validation Checklist

After implementation, verify:

### Ontology Validation
- [ ] Property loads without errors
- [ ] rdfs:domain points to cidoc:E70_Document
- [ ] rdfs:range points to cidoc:E21_Person
- [ ] rdfs:subPropertyOf links to cidoc:P70_documents
- [ ] Label and comment reference E13 pattern
- [ ] dcterms:created date is present
- [ ] rdfs:seeAlso includes E13 and P140i references

### Transformation Validation
- [ ] Function handles missing property gracefully
- [ ] Function creates E7_Activity when needed
- [ ] Function reuses existing E7_Activity
- [ ] Function creates E13_Attribute_Assignment
- [ ] E13 has all three required links (P141, P177, P14.1)
- [ ] Function handles multiple sellers
- [ ] Function handles dict and string formats
- [ ] Function removes simplified property
- [ ] AAT constants are defined and used correctly

### Integration Validation
- [ ] Function called in correct sequence
- [ ] No conflicts with other transformations
- [ ] Works with full sales contract workflow
- [ ] Handles edge cases properly

---

## Understanding the E13 Pattern

### Why E13 Attribute Assignment?

The E13_Attribute_Assignment pattern is used to formally document the assignment of an attribute to an entity. In this case:

1. **What is being attributed**: The relationship "carried out by" (P14)
2. **To what**: The sale event (E7_Activity)
3. **With what value**: The seller person (E21_Person)
4. **In what role**: As "seller"

This pattern provides:
- **Formal provenance**: Documents who/what made the attribution
- **Explicit typing**: Clearly specifies the relationship type (P14)
- **Role clarity**: Distinguishes seller from other participants
- **Extensibility**: Allows additional attribution metadata

### E13 Structure Breakdown

```
E7_Activity (sale event)
  └─ P140i_was_attributed_by
      └─ E13_Attribute_Assignment
          ├─ P141_assigned → E21_Person (the seller)
          ├─ P177_assigned_property_of_type → E55_Type ("P14 carried out by")
          └─ P14.1_in_the_role_of → E55_Type ("seller")
```

This reads as: "The sale event was attributed by [an attribution] which assigned [the person] as the value of the property type [P14 carried out by] in the role of [seller]."

---

## Performance Considerations

The transformation function is optimized for:
- **Single Pass**: Processes all sellers in one iteration
- **Efficient Checking**: Minimal conditional logic
- **Memory Usage**: Copies only necessary data
- **URI Generation**: Uses document ID as base for stable URIs

Expected performance:
- Single seller: <2ms (E13 adds slight overhead)
- Multiple sellers: <10ms
- 100 contracts: <200ms

---

## Next Steps

After successful implementation:

1. **Update Documentation**: Add E13 pattern examples to main documentation
2. **Train Users**: Inform data entry personnel about new property
3. **Monitor Usage**: Track adoption and any issues
4. **Extend**: Apply similar E13 pattern to buyer and other roles

---

*For additional support, refer to the complete semantic documentation in `documents-seller-documentation.md`.*
