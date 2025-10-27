# GMN P70.2 Documents Buyer: Implementation Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Implementation Steps](#implementation-steps)
4. [Testing Procedures](#testing-procedures)
5. [Troubleshooting](#troubleshooting)
6. [Examples](#examples)

---

## Overview

This guide provides step-by-step instructions for implementing the `gmn:P70_2_documents_buyer` property in the GMN ontology and transformation pipeline. The property simplifies the documentation of buyers in sales contracts by providing a direct relationship that transforms into the full CIDOC-CRM acquisition structure.

**Implementation Time:** Approximately 30-40 minutes  
**Difficulty Level:** Intermediate  
**Required Files:** `gmn_ontology.ttl`, `gmn_to_cidoc_transform.py`

---

## Prerequisites

### Required Knowledge
- Basic understanding of RDF/OWL ontology structure
- Familiarity with CIDOC-CRM conceptual model
- Python programming (intermediate level)
- JSON-LD data structure concepts

### Required Tools
- Text editor with TTL/Python syntax support
- RDF validation tool (optional but recommended)
- Python 3.7 or higher
- Access to GMN ontology and transformation files

### Dependencies
```python
from uuid import uuid4
```

---

## Implementation Steps

### Step 1: Add Ontology Definition

#### 1.1 Open the Ontology File
Open `gmn_ontology.ttl` in your text editor.

#### 1.2 Locate the P70 Properties Section
Find the section containing other P70 properties (typically after P70.1 documents seller).

#### 1.3 Add the Property Definition
Insert the following TTL code:

```turtle
# Property: P70.2 documents buyer
gmn:P70_2_documents_buyer
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.2 documents buyer"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the buyer. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P22_transferred_title_to > E21_Person. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The buyer is the party receiving ownership of the property being sold."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P22_transferred_title_to .
```

#### 1.4 Verify Formatting
- Ensure proper indentation (4 spaces)
- Check that all lines end with `;` except the last (which ends with `.`)
- Verify namespace prefixes are defined (`gmn:`, `cidoc:`, `rdfs:`, `owl:`, `dcterms:`)

#### 1.5 Validate the Ontology
Run your RDF validator or use an online tool to check syntax:
```bash
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null
```

---

### Step 2: Implement Transformation Function

#### 2.1 Open the Transformation Script
Open `gmn_to_cidoc_transform.py` in your text editor.

#### 2.2 Locate the P70 Transformation Functions
Find the section with other P70 transformation functions (after `transform_p70_1_documents_seller`).

#### 2.3 Add the Transformation Function
Insert the following Python code:

```python
def transform_p70_2_documents_buyer(data):
    """
    Transform gmn:P70_2_documents_buyer to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P22_transferred_title_to > E21_Person
    """
    if 'gmn:P70_2_documents_buyer' not in data:
        return data
    
    buyers = data['gmn:P70_2_documents_buyer']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create or get E8_Acquisition node
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P22_transferred_title_to array if needed
    if 'cidoc:P22_transferred_title_to' not in acquisition:
        acquisition['cidoc:P22_transferred_title_to'] = []
    
    # Process each buyer
    for buyer_obj in buyers:
        if isinstance(buyer_obj, dict):
            buyer_data = buyer_obj.copy()
            if '@type' not in buyer_data:
                buyer_data['@type'] = 'cidoc:E21_Person'
        else:
            buyer_uri = str(buyer_obj)
            buyer_data = {
                '@id': buyer_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P22_transferred_title_to'].append(buyer_data)
    
    # Remove original GMN property
    del data['gmn:P70_2_documents_buyer']
    return data
```

#### 2.4 Code Explanation

**Lines 1-3:** Function signature and docstring documenting the transformation path.

**Lines 4-5:** Early return if property not present (no transformation needed).

**Lines 7-8:** Extract buyers array and get document URI (generate if missing).

**Lines 10-16:** Create E8_Acquisition node if none exists. This node is shared by all P70 acquisition properties.

**Line 18:** Get reference to the acquisition node.

**Lines 20-22:** Initialize P22_transferred_title_to array if not present.

**Lines 24-35:** Loop through buyers:
- If buyer is a dictionary (full object), copy it and ensure it has @type
- If buyer is a string (URI reference), create minimal object structure
- Add properly formatted buyer to acquisition's P22_transferred_title_to array

**Lines 37-39:** Remove the original GMN property and return transformed data.

---

### Step 3: Integrate with Transform Pipeline

#### 3.1 Locate the transform_item Function
Find the `transform_item()` function (typically near the end of the file).

#### 3.2 Add Function Call
Add the transformation call in the P70 properties section:

```python
def transform_item(item, include_internal=False):
    """
    Transform a GMN item to full CIDOC-CRM structure.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM.
    
    Returns:
        Transformed item dictionary
    """
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)  # ADD THIS LINE
    item = transform_p70_3_documents_transfer_of(item)
    # ... rest of P70 transformations ...
```

#### 3.3 Verify Import Statements
Ensure `uuid4` is imported at the top of the file:

```python
from uuid import uuid4
```

---

### Step 4: Update Documentation

#### 4.1 Add Property Description
Add the following to your main documentation file in the sales contract properties section:

```markdown
#### P70.2 documents buyer

**GMN Property:** `gmn:P70_2_documents_buyer`  
**Label:** "P70.2 documents buyer"  
**Domain:** `gmn:E31_2_Sales_Contract`  
**Range:** `cidoc:E21_Person`

Simplified property for associating a sales contract with the person named as 
the buyer. The buyer is the party receiving ownership of the property being sold.

**CIDOC-CRM Transformation Path:**
```
E31_Document
  └─ P70_documents
      └─ E8_Acquisition
          └─ P22_transferred_title_to
              └─ E21_Person
```

**Multiple Values:** Supported (for joint purchases by multiple buyers)
```

#### 4.2 Add to Property Reference Table
Add row to your property reference table:

| GMN Property | Label | CIDOC Path | Domain | Range |
|--------------|-------|------------|--------|-------|
| gmn:P70_2_documents_buyer | P70.2 documents buyer | P70→E8→P22→E21 | E31_2_Sales_Contract | E21_Person |

---

## Testing Procedures

### Test 1: Single Buyer

#### Input Data
```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "contract001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "person001",
      "gmn:P1_1_has_name": "Giovanni Rossi"
    }
  ]
}
```

#### Expected Output
```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "contract001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "contract001/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "person001",
          "@type": "cidoc:E21_Person",
          "gmn:P1_1_has_name": "Giovanni Rossi"
        }
      ]
    }
  ]
}
```

#### Verification Steps
1. ✓ E8_Acquisition node created with correct URI
2. ✓ P22_transferred_title_to array present
3. ✓ Buyer has correct @type (cidoc:E21_Person)
4. ✓ Buyer properties preserved (name, etc.)
5. ✓ Original gmn:P70_2_documents_buyer removed

---

### Test 2: Multiple Buyers (Joint Purchase)

#### Input Data
```json
{
  "@id": "contract002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "person002",
      "gmn:P1_1_has_name": "Marco Bianchi"
    },
    {
      "@id": "person003",
      "gmn:P1_1_has_name": "Paolo Verdi"
    }
  ]
}
```

#### Expected Output
```json
{
  "@id": "contract002",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "contract002/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "person002",
          "@type": "cidoc:E21_Person",
          "gmn:P1_1_has_name": "Marco Bianchi"
        },
        {
          "@id": "person003",
          "@type": "cidoc:E21_Person",
          "gmn:P1_1_has_name": "Paolo Verdi"
        }
      ]
    }
  ]
}
```

#### Verification Steps
1. ✓ Both buyers present in P22_transferred_title_to array
2. ✓ Each buyer properly typed as E21_Person
3. ✓ Order of buyers preserved
4. ✓ All buyer properties maintained

---

### Test 3: Integration with Other P70 Properties

#### Input Data
```json
{
  "@id": "contract003",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [
    {
      "@id": "person004",
      "gmn:P1_1_has_name": "Antonio Neri"
    }
  ],
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "person005",
      "gmn:P1_1_has_name": "Francesco Giusti"
    }
  ],
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "house001",
      "@type": "gmn:E22_1_Building"
    }
  ]
}
```

#### Expected Output
```json
{
  "@id": "contract003",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "contract003/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P23_transferred_title_from": [
        {
          "@id": "person004",
          "@type": "cidoc:E21_Person",
          "gmn:P1_1_has_name": "Antonio Neri"
        }
      ],
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "person005",
          "@type": "cidoc:E21_Person",
          "gmn:P1_1_has_name": "Francesco Giusti"
        }
      ],
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "house001",
          "@type": "gmn:E22_1_Building"
        }
      ]
    }
  ]
}
```

#### Verification Steps
1. ✓ Single E8_Acquisition node contains all three relationships
2. ✓ P23_transferred_title_from contains seller
3. ✓ P22_transferred_title_to contains buyer
4. ✓ P24_transferred_title_of contains property
5. ✓ All original GMN properties removed

---

### Test 4: URI Reference Only

#### Input Data
```json
{
  "@id": "contract004",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [
    "person006"
  ]
}
```

#### Expected Output
```json
{
  "@id": "contract004",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "contract004/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "person006",
          "@type": "cidoc:E21_Person"
        }
      ]
    }
  ]
}
```

#### Verification Steps
1. ✓ String URI converted to object structure
2. ✓ E21_Person type automatically assigned
3. ✓ Minimal valid CIDOC structure created

---

## Troubleshooting

### Issue 1: Property Not Transforming

**Symptom:** Original `gmn:P70_2_documents_buyer` remains in output

**Possible Causes:**
1. Transformation function not called in `transform_item()`
2. Function placed after other code that modifies data structure
3. Property name mismatch (check spelling, case)

**Solutions:**
1. Verify function is called: `item = transform_p70_2_documents_buyer(item)`
2. Ensure function is called before any code that depends on the transformed structure
3. Check property name matches exactly: `'gmn:P70_2_documents_buyer'`

---

### Issue 2: Multiple E8_Acquisition Nodes Created

**Symptom:** Each P70 property creates its own acquisition node

**Cause:** Transformation functions not properly checking for existing acquisition

**Solution:**
Ensure this check exists in ALL P70 transformation functions:
```python
if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
    # Create new acquisition
else:
    # Use existing acquisition
```

---

### Issue 3: Buyer Properties Lost

**Symptom:** Only buyer URI appears, other properties missing

**Cause:** Not using `.copy()` when handling dictionary objects

**Solution:**
Verify this line in transformation function:
```python
buyer_data = buyer_obj.copy()  # Must use .copy()!
```

---

### Issue 4: Type Error with Mixed Input

**Symptom:** Error when processing arrays with both strings and objects

**Cause:** Not checking object type before processing

**Solution:**
Ensure proper type checking:
```python
for buyer_obj in buyers:
    if isinstance(buyer_obj, dict):
        # Handle object
    else:
        # Handle string URI
```

---

### Issue 5: UUID Import Error

**Symptom:** `NameError: name 'uuid4' is not defined`

**Cause:** Missing import statement

**Solution:**
Add to imports at top of file:
```python
from uuid import uuid4
```

---

## Examples

### Example 1: Historical Venetian Contract

**Scenario:** 1548 property sale in Venice

**Input:**
```json
{
  "@id": "ASV_NT_1548_05_12",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P94i_2_has_enactment_date": "1548-05-12",
  "gmn:P70_1_documents_seller": [
    {
      "@id": "person_giovanni_marcello",
      "gmn:P1_1_has_name": "Giovanni Marcello"
    }
  ],
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "person_pietro_grimani",
      "gmn:P1_1_has_name": "Pietro Grimani",
      "gmn:P1_3_has_patrilineal_name": "Grimani"
    }
  ],
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "building_san_polo_1548",
      "@type": "gmn:E22_1_Building",
      "cidoc:P3_has_note": "House in San Polo parish"
    }
  ]
}
```

**Output Shows:**
- Single E8_Acquisition documenting the transaction
- Seller (Marcello) in P23_transferred_title_from
- Buyer (Grimani) in P22_transferred_title_to
- Building in P24_transferred_title_of
- All participant details preserved

---

### Example 2: Joint Purchase by Siblings

**Scenario:** Two brothers jointly purchasing property

**Input:**
```json
{
  "@id": "contract_joint_purchase_1565",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P94i_2_has_enactment_date": "1565-08-22",
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "person_marco_contarini",
      "gmn:P1_1_has_name": "Marco Contarini",
      "gmn:P1_3_has_patrilineal_name": "Contarini"
    },
    {
      "@id": "person_alvise_contarini",
      "gmn:P1_1_has_name": "Alvise Contarini",
      "gmn:P1_3_has_patrilineal_name": "Contarini"
    }
  ]
}
```

**Output Shows:**
- Both brothers in P22_transferred_title_to array
- Each properly typed as E21_Person
- Family relationship inferable from shared patrilineal name

---

### Example 3: Buyer with Procurator

**Scenario:** Buyer acting through legal representative

**Input:**
```json
{
  "@id": "contract_with_procurator",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "person_lorenzo_morosini",
      "gmn:P1_1_has_name": "Lorenzo Morosini"
    }
  ],
  "gmn:P70_5_documents_buyers_procurator": [
    {
      "@id": "person_andrea_venier",
      "gmn:P1_1_has_name": "Andrea Venier"
    }
  ]
}
```

**Output Shows:**
- Buyer (Morosini) in P22_transferred_title_to
- Procurator (Venier) in separate E7_Activity with P17_was_motivated_by linking to buyer
- Clear distinction between principal and representative

---

## Next Steps

After successful implementation:

1. **Test thoroughly** with historical data samples
2. **Document edge cases** encountered in your data
3. **Update property statistics** in documentation
4. **Train data entry team** on proper usage
5. **Monitor transformation logs** for errors

---

## Additional Resources

- **CIDOC-CRM Documentation**: http://www.cidoc-crm.org/
- **P22 Property Specification**: http://www.cidoc-crm.org/Property/P22-transferred-title-to/version-7.1.3
- **E8 Acquisition Class**: http://www.cidoc-crm.org/Entity/E8-Acquisition/version-7.1.3
- **GMN Ontology Full Documentation**: See project documentation
- **Related Implementation Guides**: P70.1 (seller), P70.3 (transfer of)

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-27  
**Author:** GMN Project Team
