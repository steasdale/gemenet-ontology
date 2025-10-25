# Dowry Contract Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the new gmn:E31_8_Dowry_Contract class in the Genoese Merchant Networks ontology and transformation script.

## What is a Dowry Contract?

A dowry contract is a specialized type of notarial contract that records the transfer of property (dowry) from a donor (typically a parent or family member) to a person receiving the dowry (typically the bride or the couple), usually in the context of marriage arrangements.

Like all notarial contracts in this ontology, dowry contracts model the transfer of rights: the donor agrees or obliges themselves to transfer an object of dowry to the person receiving the dowry.

## Key Design Decisions

1. **Reuses existing properties**: The dowry contract reuses `gmn:P70_32_indicates_donor` (from donations) rather than creating a new donor property, as requested.

2. **Shares receiving party property**: Uses `gmn:P70_22_indicates_receiving_party` which is already shared across cessions, declarations, and donations.

3. **New object property**: Creates `gmn:P70_34_indicates_object_of_dowry` to distinguish dowry objects from donation objects (P70.33).

4. **Uses E8_Acquisition**: Like sales and donations, dowry contracts use E8_Acquisition to model the property transfer.

## Implementation Steps

### Step 1: Update the Ontology File (gmn_ontology.ttl)

#### 1.1 Add the new class

Add this class definition to the "Classes (Alphabetical)" section:

```turtle
# Class: E31.8 Dowry Contract
gmn:E31_8_Dowry_Contract
    a owl:Class ;
    rdfs:subClassOf gmn:E31_1_Contract ;
    rdfs:label "E31.8 Dowry Contract"@en ;
    rdfs:comment "Specialized class that describes dowry contract documents. This is a specialized type of gmn:E31_1_Contract used to represent legal documents that record the transfer of property (dowry) from a donor to a person receiving the dowry, typically in the context of marriage arrangements. Like all notarial contracts in this ontology, dowry contracts model the transfer of rights: the donor agrees or obliges themselves to transfer an object of dowry to the person receiving the dowry. Dowry contracts typically include information about the donor (often a parent or family member), the recipient (often the spouse or the couple), the property being transferred as dowry, any conditions attached to the transfer, date of transaction, and witnessing notaries. Instances of this class represent the physical or conceptual document itself, while the actual transfer of ownership is modeled through E8_Acquisition events that the document documents (via P70_documents)."@en ;
    dcterms:created "2025-10-25"^^xsd:date ;
    rdfs:seeAlso gmn:E31_1_Contract, cidoc:E8_Acquisition, cidoc:P70_documents .
```

#### 1.2 Update P70.32 domain

Find the `gmn:P70_32_indicates_donor` property and replace its `rdfs:domain` statement with:

```turtle
gmn:P70_32_indicates_donor
    # ... keep all existing property definitions ...
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_7_Donation_Contract
            gmn:E31_8_Dowry_Contract
        )
    ] ;
    dcterms:modified "2025-10-25"^^xsd:date ;
    # ... keep remaining property definitions ...
```

Also update its comment to mention dowries:

```turtle
    rdfs:comment "Simplified property for associating a donation or dowry contract with the person or entity named as the donor. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P23_transferred_title_from > E39_Actor. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. In donation contracts, the donor is the party voluntarily transferring ownership of property without expectation of payment. In dowry contracts, the donor is the party (often a parent or family member) transferring property as part of a marriage arrangement."@en ;
```

#### 1.3 Update P70.22 domain

Find the `gmn:P70_22_indicates_receiving_party` property and replace its `rdfs:domain` statement with:

```turtle
gmn:P70_22_indicates_receiving_party
    # ... keep all existing property definitions ...
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_4_Cession_of_Rights_Contract
            gmn:E31_5_Declaration
            gmn:E31_7_Donation_Contract
            gmn:E31_8_Dowry_Contract
        )
    ] ;
    dcterms:modified "2025-10-25"^^xsd:date ;
    # ... keep remaining property definitions ...
```

Also update its comment to mention dowries:

```turtle
    rdfs:comment "Simplified property for associating a document with the person or entity receiving something in the documented activity. In cession of rights contracts, this is the party receiving the ceded rights. In declarations, this is the party to whom the declaration is addressed or directed. In donation contracts, this is the donee receiving the donated property. In dowry contracts, this is the party (often the spouse or the couple) receiving the dowry property. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P01_has_domain > E39_Actor (using the inverse P01i_is_domain_of for declarations) OR E31_Document > P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor (for cessions, donations, and dowries, where the receiving party acquires ownership or rights). The E7_Activity or E8_Acquisition should be typed appropriately (AAT 300417639 for cessions, AAT 300027623 for declarations, or appropriate type for donations and dowries). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
```

#### 1.4 Add the new property P70.34

Add this property definition to the "Properties (Alphabetical)" section:

```turtle
# Property: P70.34 indicates object of dowry
gmn:P70_34_indicates_object_of_dowry
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.34 indicates object of dowry"@en ;
    rdfs:comment "Simplified property for associating a dowry contract with the physical thing (property or object) being transferred as dowry. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The range includes buildings (gmn:E22_1_Building) and moveable property (gmn:E22_2_Moveable_Property) that are being transferred as dowry, typically in the context of marriage arrangements."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_8_Dowry_Contract ;
    rdfs:range cidoc:E18_Physical_Thing ;
    dcterms:created "2025-10-25"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P24_transferred_title_of .
```

#### 1.5 Update ontology metadata

Update the version info and modified date at the top of the ontology:

```turtle
<http://www.genoesemerchantnetworks.com/ontology> 
    a owl:Ontology ;
    # ... keep existing metadata ...
    dcterms:modified "2025-10-25"^^xsd:date ;
    owl:versionInfo "1.5" ;
    # ... keep remaining metadata ...
```

### Step 2: Update the Transformation Script (gmn_to_cidoc_transform.py)

#### 2.1 Add the transformation function

Add this function after the other P70 transformation functions:

```python
def transform_p70_34_indicates_object_of_dowry(data):
    """
    Transform gmn:P70_34_indicates_object_of_dowry to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing
    """
    if 'gmn:P70_34_indicates_object_of_dowry' not in data:
        return data
    
    objects = data['gmn:P70_34_indicates_object_of_dowry']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P24_transferred_title_of' not in acquisition:
        acquisition['cidoc:P24_transferred_title_of'] = []
    
    for obj_obj in objects:
        if isinstance(obj_obj, dict):
            obj_data = obj_obj.copy()
            if '@type' not in obj_data:
                obj_data['@type'] = 'cidoc:E18_Physical_Thing'
        else:
            obj_uri = str(obj_obj)
            obj_data = {
                '@id': obj_uri,
                '@type': 'cidoc:E18_Physical_Thing'
            }
        
        acquisition['cidoc:P24_transferred_title_of'].append(obj_data)
    
    del data['gmn:P70_34_indicates_object_of_dowry']
    return data
```

#### 2.2 Update transform_p70_22_indicates_receiving_party function

Replace the existing `transform_p70_22_indicates_receiving_party` function with the updated version that includes dowry handling. Find these lines:

```python
is_donation = 'gmn:E31_7_Donation_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_7_Donation_Contract'
```

And change the condition to:

```python
is_donation = 'gmn:E31_7_Donation_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_7_Donation_Contract'
is_dowry = 'gmn:E31_8_Dowry_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_8_Dowry_Contract'
```

Then update the condition that handles donations:

```python
if is_donation or is_dowry:
    # For donations and dowries, use E8_Acquisition
    # ... rest of the code remains the same ...
```

#### 2.3 Update transform_item function

Add the call to the new transformation function in the `transform_item()` function, after the donation properties:

```python
    # Donation properties (P70.32-P70.33)
    item = transform_p70_32_indicates_donor(item)
    item = transform_p70_33_indicates_object_of_donation(item)
    
    # Dowry properties (P70.34)  # ADD THIS
    item = transform_p70_34_indicates_object_of_dowry(item)  # ADD THIS
    
    # Visual representation
    item = transform_p138i_1_has_representation(item)
```

#### 2.4 Update the help text in main()

Update the "Supported contract types" list in the `main()` function:

```python
        print("  - gmn:E31_7_Donation_Contract")
        print("  - gmn:E31_8_Dowry_Contract")  # ADD THIS LINE
```

Also update the module docstring at the top of the file to include dowries:

```python
"""
Transform GMN shortcut properties to full CIDOC-CRM compliant structure.

...

Updated to reflect expanded class hierarchy including:
- gmn:E31_1_Contract (general contract class)
- gmn:E31_2_Sales_Contract (specialized sales contract)
- gmn:E31_3_Arbitration_Agreement
- gmn:E31_4_Cession_of_Rights_Contract
- gmn:E31_5_Declaration
- gmn:E31_6_Correspondence
- gmn:E31_7_Donation_Contract
- gmn:E31_8_Dowry_Contract  # ADD THIS
"""
```

### Step 3: Update Documentation (documentation_note.txt)

Add the transformation examples from `dowry_contract_documentation_additions.txt` to the main documentation file. Include:

1. The updated transformation examples for P70.32 and P70.22
2. The new transformation example for P70.34
3. The complete dowry contract example
4. The updated class hierarchy
5. The updated property domain distribution table
6. The comparison table of transfer contract types

### Step 4: Testing

Test the implementation with sample data:

```json
{
  "@id": "http://example.com/contracts/dowry123",
  "@type": "gmn:E31_8_Dowry_Contract",
  "gmn:P1_1_has_name": "Dowry of Maria Spinola",
  "gmn:P70_32_indicates_donor": {
    "@id": "http://example.com/persons/giacomo_spinola"
  },
  "gmn:P70_22_indicates_receiving_party": {
    "@id": "http://example.com/persons/maria_spinola"
  },
  "gmn:P70_34_indicates_object_of_dowry": [
    {
      "@id": "http://example.com/buildings/house_genoa"
    },
    {
      "@id": "http://example.com/properties/vineyard_albaro"
    }
  ],
  "gmn:P70_16_documents_sale_price_amount": "1500.00",
  "gmn:P70_17_documents_sale_price_currency": {
    "@id": "http://example.com/currencies/lira"
  },
  "gmn:P94i_2_has_enactment_date": "1455-08-12"
}
```

Run the transformation:

```bash
python gmn_to_cidoc_transform.py test_input.json test_output.json
```

Verify that the output includes:
- Proper E8_Acquisition structure
- P23_transferred_title_from for the donor
- P22_transferred_title_to for the receiving party
- P24_transferred_title_of for the dowry objects
- Proper E65_Creation for document creation
- E97_Monetary_Amount for the value

## Summary of Changes

### Files Modified:
1. **gmn_ontology.ttl**: Added class, updated 2 properties, added 1 new property
2. **gmn_to_cidoc_transform.py**: Added 1 transformation function, updated 1 function, updated help text
3. **documentation_note.txt**: Added transformation examples and updated tables

### New Entities:
- **Class**: gmn:E31_8_Dowry_Contract
- **Property**: gmn:P70_34_indicates_object_of_dowry

### Updated Entities:
- **Property**: gmn:P70_32_indicates_donor (expanded domain)
- **Property**: gmn:P70_22_indicates_receiving_party (expanded domain)

## Design Rationale

### Why reuse P70.32 (donor)?
The semantic meaning is identical - a person transferring property either as a gift (donation) or as part of a marriage arrangement (dowry). The distinction is captured by the document type (E31_7 vs E31_8), not by creating different properties for semantically identical relationships.

### Why create a separate P70.34 (object of dowry)?
While the transformation is identical to P70.33 (object of donation), having a separate property:
1. Makes the data model clearer (explicit distinction between donation and dowry objects)
2. Allows for potential future distinctions in handling or constraints
3. Improves data entry clarity in Omeka-S
4. Maintains semantic precision in the source data

### Why use E8_Acquisition?
Dowry contracts, like sales and donations, involve the transfer of ownership rights over physical property. E8_Acquisition is the appropriate CIDOC-CRM class for modeling such transfers, maintaining consistency across all property transfer contract types.

## Additional Notes

- All dowry contracts should be classified as both `cidoc:E31_Document` and `gmn:E31_8_Dowry_Contract`
- The transformation automatically creates URIs for intermediate entities (acquisitions, appellations, etc.)
- Price properties (P70.16-17) are optional but can be used to document the declared value of the dowry
- Multiple objects can be associated with a single dowry using P70.34 multiple times
- The donor in P70.32 can be any E39_Actor (person or group)
