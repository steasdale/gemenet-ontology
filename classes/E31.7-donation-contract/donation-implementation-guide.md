# Donation Contract Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the gmn:E31_7_Donation_Contract class in the Genoese Merchant Networks ontology. The donation contract models the gratuitous transfer of property from a donor to a donee without expectation of payment.

## Design Decisions

### Why use E8_Acquisition?
Donation contracts, like sales contracts, involve the transfer of ownership rights over physical property. E8_Acquisition is the appropriate CIDOC-CRM class for modeling such transfers, maintaining consistency across all property transfer contract types in the ontology.

### Why reuse P70.22 (indicates receiving party)?
The semantic meaning of "receiving party" is consistent across donation, cession, and declaration contexts. Rather than creating donation-specific properties, we leverage the existing P70.22 property which:
- Already handles E8_Acquisition contexts (for cessions)
- Reduces ontology complexity
- Maintains semantic consistency
- Follows the DRY (Don't Repeat Yourself) principle

### Why create separate P70.32 and P70.33?
While we reuse P70.22 for the receiving party, we create specific properties for the donor and object of donation to:
1. Make the data model clearer and more explicit
2. Improve data entry clarity in Omeka-S
3. Maintain semantic precision at the source level
4. Allow for future distinctions if needed

## Implementation Steps

### Step 1: Update gmn_ontology.ttl

You need to make **4 changes** to the ontology file:

#### Change 1: Add E31_7_Donation_Contract Class

Insert this class definition in the Classes section (alphabetically after E31_6_Correspondence):

```turtle
# Class: E31.7 Donation Contract
gmn:E31_7_Donation_Contract
    a owl:Class ;
    rdfs:subClassOf gmn:E31_1_Contract ;
    rdfs:label "E31.7 Donation Contract"@en ;
    rdfs:comment "Specialized class that describes donation contract documents. This is a specialized type of gmn:E31_1_Contract used to represent legal documents that record the gratuitous transfer of property (both real estate and moveable property) from a donor to a donee (recipient). Unlike sales contracts where transfer occurs in exchange for payment, donation contracts document voluntary transfers without expectation of compensation, though they may include conditions or stipulations. Like all notarial contracts in this ontology, donation contracts model the transfer of rights: the donor agrees or obliges themselves to transfer an object of donation to the person receiving the donation. Donation contracts typically include information about the donor, donee, property being donated, any conditions attached to the donation, date of transaction, and witnessing notaries. Instances of this class represent the physical or conceptual document itself, while the actual transfer of ownership is modeled through E8_Acquisition events that the document documents (via P70_documents)."@en ;
    dcterms:created "2025-10-19"^^xsd:date ;
    rdfs:seeAlso gmn:E31_1_Contract, cidoc:E8_Acquisition, cidoc:P70_documents .
```

#### Change 2: Update P70.22 Domain

Find the existing P70.22 property definition and replace it with this updated version:

```turtle
# Property: P70.22 indicates receiving party
gmn:P70_22_indicates_receiving_party
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.22 indicates receiving party"@en ;
    rdfs:comment "Simplified property for associating a document with the person or entity receiving something in the documented activity. In cession of rights contracts, this is the party receiving the ceded rights. In declarations, this is the party to whom the declaration is addressed or directed. In donation contracts, this is the donee receiving the donated property. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P01_has_domain > E39_Actor (using the inverse P01i_is_domain_of for declarations) OR E31_Document > P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor (for cessions and donations, where the receiving party acquires ownership or rights). The E7_Activity or E8_Acquisition should be typed appropriately (AAT 300417639 for cessions, AAT 300027623 for declarations, or appropriate type for donations). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_4_Cession_of_Rights_Contract
            gmn:E31_5_Declaration
            gmn:E31_7_Donation_Contract
        )
    ] ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-18"^^xsd:date ;
    dcterms:modified "2025-10-19"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P22_transferred_title_to, cidoc:P01_has_domain .
```

#### Change 3: Add P70.32 Property

Insert this property definition in the Properties section (after P70.31):

```turtle
# Property: P70.32 indicates donor
gmn:P70_32_indicates_donor
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.32 indicates donor"@en ;
    rdfs:comment "Simplified property for associating a donation contract with the person or entity named as the donor. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P23_transferred_title_from > E39_Actor. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The donor is the party voluntarily transferring ownership of the property being donated without expectation of payment."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_7_Donation_Contract ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-19"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P23_transferred_title_from .
```

#### Change 4: Add P70.33 Property

Insert this property definition immediately after P70.32:

```turtle
# Property: P70.33 indicates object of donation
gmn:P70_33_indicates_object_of_donation
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.33 indicates object of donation"@en ;
    rdfs:comment "Simplified property for associating a donation contract with the physical thing (property or object) being donated. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The range includes buildings (gmn:E22_1_Building) and moveable property (gmn:E22_2_Moveable_Property) that are being transferred as gifts."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_7_Donation_Contract ;
    rdfs:range cidoc:E18_Physical_Thing ;
    dcterms:created "2025-10-19"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P24_transferred_title_of .
```

### Step 2: Update gmn_to_cidoc_transform.py

You need to make **3 changes** to the transformation script:

#### Change 1: Add transform_p70_32_indicates_donor() Function

Add this function after the correspondence transformation functions (around line 1800):

```python
def transform_p70_32_indicates_donor(data):
    """
    Transform gmn:P70_32_indicates_donor to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P23_transferred_title_from > E39_Actor
    """
    if 'gmn:P70_32_indicates_donor' not in data:
        return data
    
    donors = data['gmn:P70_32_indicates_donor']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P23_transferred_title_from' not in acquisition:
        acquisition['cidoc:P23_transferred_title_from'] = []
    
    for donor_obj in donors:
        if isinstance(donor_obj, dict):
            donor_data = donor_obj.copy()
            if '@type' not in donor_data:
                donor_data['@type'] = 'cidoc:E39_Actor'
        else:
            donor_uri = str(donor_obj)
            donor_data = {
                '@id': donor_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        acquisition['cidoc:P23_transferred_title_from'].append(donor_data)
    
    del data['gmn:P70_32_indicates_donor']
    return data
```

#### Change 2: Add transform_p70_33_indicates_object_of_donation() Function

Add this function immediately after transform_p70_32_indicates_donor():

```python
def transform_p70_33_indicates_object_of_donation(data):
    """
    Transform gmn:P70_33_indicates_object_of_donation to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing
    """
    if 'gmn:P70_33_indicates_object_of_donation' not in data:
        return data
    
    objects = data['gmn:P70_33_indicates_object_of_donation']
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
    
    del data['gmn:P70_33_indicates_object_of_donation']
    return data
```

#### Change 3: Update transform_p70_22_indicates_receiving_party() Function

Find the existing transform_p70_22_indicates_receiving_party() function and update the document type detection section to include donations:

```python
def transform_p70_22_indicates_receiving_party(data):
    """
    Transform gmn:P70_22_indicates_receiving_party to full CIDOC-CRM structure.
    For cessions: P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    For declarations: P70_documents > E7_Activity > P01_has_domain > E39_Actor
    For donations: P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
    """
    if 'gmn:P70_22_indicates_receiving_party' not in data:
        return data
    
    receiving_parties = data['gmn:P70_22_indicates_receiving_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    item_type = data.get('@type', '')
    
    # Determine document type
    is_cession = 'gmn:E31_4_Cession_of_Rights_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_4_Cession_of_Rights_Contract'
    is_declaration = 'gmn:E31_5_Declaration' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_5_Declaration'
    is_donation = 'gmn:E31_7_Donation_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_7_Donation_Contract'
    
    if is_donation:
        # For donations, use E8_Acquisition
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            acquisition_uri = f"{subject_uri}/acquisition"
            data['cidoc:P70_documents'] = [{
                '@id': acquisition_uri,
                '@type': 'cidoc:E8_Acquisition'
            }]
        
        acquisition = data['cidoc:P70_documents'][0]
        
        if 'cidoc:P22_transferred_title_to' not in acquisition:
            acquisition['cidoc:P22_transferred_title_to'] = []
        
        for party_obj in receiving_parties:
            if isinstance(party_obj, dict):
                party_data = party_obj.copy()
                if '@type' not in party_data:
                    party_data['@type'] = 'cidoc:E39_Actor'
            else:
                party_uri = str(party_obj)
                party_data = {
                    '@id': party_uri,
                    '@type': 'cidoc:E39_Actor'
                }
            
            acquisition['cidoc:P22_transferred_title_to'].append(party_data)
    
    elif is_declaration:
        # [Existing declaration code...]
    
    elif is_cession:
        # [Existing cession code...]
    
    del data['gmn:P70_22_indicates_receiving_party']
    return data
```

#### Change 4: Update transform_item() Function

In the transform_item() function, add the two new transformation functions after the correspondence transformations (around line 2200):

```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    # ... existing transformations ...
    
    # Correspondence properties (P70.26-P70.31)
    item = transform_p70_26_indicates_sender(item)
    item = transform_p70_27_has_address_of_origin(item)
    item = transform_p70_28_indicates_addressee(item)
    item = transform_p70_29_describes_subject(item)
    item = transform_p70_30_mentions_person(item)
    item = transform_p70_31_has_address_of_destination(item)
    
    # Donation properties (P70.32-P70.33)
    item = transform_p70_32_indicates_donor(item)
    item = transform_p70_33_indicates_object_of_donation(item)
    
    # ... rest of transformations ...
    return item
```

#### Change 5: Update main() Help Text

Update the help text in the main() function to include E31_7:

```python
def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python gmn_to_cidoc_transform_script.py <input_file.json> <output_file.json> [--include-internal]")
        print("\nOptions:")
        print("  --include-internal    Include editorial notes in output (default: exclude)")
        print("\nExamples:")
        print("  python gmn_to_cidoc_transform_script.py omeka_export.json public_output.json")
        print("  python gmn_to_cidoc_transform_script.py omeka_export.json full_output.json --include-internal")
        print("\nSupported contract types:")
        print("  - gmn:E31_1_Contract (general contracts)")
        print("  - gmn:E31_2_Sales_Contract")
        print("  - gmn:E31_4_Cession_of_Rights_Contract")
        print("  - gmn:E31_5_Declaration")
        print("  - gmn:E31_6_Correspondence")
        print("  - gmn:E31_7_Donation_Contract")
        sys.exit(1)
```

### Step 3: Update documentation_note.txt

Add the transformation examples and update the tables. See donation_contract_documentation_additions.txt for the complete content to add.

## Testing

### Test Data Example

Create a test JSON file with a donation contract:

```json
{
  "@id": "http://example.com/donations/donation001",
  "@type": "gmn:E31_7_Donation_Contract",
  "gmn:P1_1_has_name": "Donation of palazzo to monastery",
  "gmn:P70_32_indicates_donor": {
    "@id": "http://example.com/persons/giovanni_merchant",
    "@type": "cidoc:E21_Person"
  },
  "gmn:P70_22_indicates_receiving_party": {
    "@id": "http://example.com/groups/san_lorenzo_monastery",
    "@type": "cidoc:E74_Group"
  },
  "gmn:P70_33_indicates_object_of_donation": {
    "@id": "http://example.com/buildings/palazzo_spinola",
    "@type": "gmn:E22_1_Building"
  },
  "gmn:P94i_2_has_enactment_date": "1445-03-15"
}
```

### Run Transformation

```bash
python gmn_to_cidoc_transform.py test_donation.json output_donation.json
```

### Verify Output

Check that the output contains:
- An E8_Acquisition event
- P23_transferred_title_from linking to the donor
- P22_transferred_title_to linking to the receiving party
- P24_transferred_title_of linking to the donated object

## Summary of Changes

### Files Modified: 3

1. **gmn_ontology.ttl**
   - Added E31_7_Donation_Contract class
   - Added P70.32_indicates_donor property
   - Added P70.33_indicates_object_of_donation property
   - Updated P70.22_indicates_receiving_party domain

2. **gmn_to_cidoc_transform.py**
   - Added transform_p70_32_indicates_donor() function
   - Added transform_p70_33_indicates_object_of_donation() function
   - Updated transform_p70_22_indicates_receiving_party() function
   - Updated transform_item() function
   - Updated main() help text

3. **documentation_note.txt**
   - Added transformation examples for P70.32, P70.33
   - Updated class hierarchy
   - Updated property domain distribution table
   - Added donation contracts to comparison table

### Total Changes
- **Classes**: 1 added
- **Properties**: 2 added, 1 modified
- **Functions**: 2 added, 2 modified
- **Lines of code**: ~150 added

## Design Rationale

### Why reuse P70.22 instead of creating P70.34?

The semantic meaning of "receiving party" is identical in both donations and cessions - someone receiving transferred property or rights. The context (gift vs. rights transfer) is captured by the document type, not by different property names.

### Why create P70.33 instead of reusing P70.3?

While P70.3 (documents transfer of) could theoretically be reused, having a donation-specific property:
- Makes data entry clearer and more explicit
- Allows for future distinctions if needed
- Maintains semantic precision at the source level
- Improves data model documentation

## Support Information

If you encounter issues during implementation:

1. **Ontology validation**: Use an RDF validator to check syntax
2. **Transformation testing**: Test with small sample files first
3. **CIDOC-CRM compliance**: Verify output against CIDOC-CRM specification
4. **Property domains**: Ensure all property domains are correctly updated

## Next Steps

After implementation:
1. Test with sample data
2. Update any documentation or training materials
3. Notify Omeka-S administrators to add the new class to resource templates
4. Create example records in Omeka-S for reference
5. Update any data entry guidelines for users
