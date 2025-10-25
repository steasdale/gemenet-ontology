# E31.8 Dowry Contract - Ontology Addition

## Class Definition

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

## Semantic Structure

```
E31_8_Dowry_Contract (the dowry contract document)
  └─ P70_documents
      └─ E8_Acquisition (the dowry transfer)
          ├─ P23_transferred_title_from → E39_Actor (donor)
          ├─ P22_transferred_title_to → E39_Actor (receiving party)
          └─ P24_transferred_title_of → E18_Physical_Thing (object of dowry)
```

## Properties

### P70.32 indicates donor (updated)

```turtle
gmn:P70_32_indicates_donor
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.32 indicates donor"@en ;
    rdfs:comment "Simplified property for associating a donation or dowry contract with the person or entity named as the donor. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P23_transferred_title_from > E39_Actor. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. In donation contracts, the donor is the party voluntarily transferring ownership of property without expectation of payment. In dowry contracts, the donor is the party (often a parent or family member) transferring property as part of a marriage arrangement."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_7_Donation_Contract
            gmn:E31_8_Dowry_Contract
        )
    ] ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-19"^^xsd:date ;
    dcterms:modified "2025-10-25"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P23_transferred_title_from .
```

### P70.22 indicates receiving party (updated)

```turtle
gmn:P70_22_indicates_receiving_party
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.22 indicates receiving party"@en ;
    rdfs:comment "Simplified property for associating a document with the person or entity receiving something in the documented activity. In cession of rights contracts, this is the party receiving the ceded rights. In declarations, this is the party to whom the declaration is addressed or directed. In donation contracts, this is the donee receiving the donated property. In dowry contracts, this is the party (often the spouse or the couple) receiving the dowry property. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P01_has_domain > E39_Actor (using the inverse P01i_is_domain_of for declarations) OR E31_Document > P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor (for cessions, donations, and dowries, where the receiving party acquires ownership or rights). The E7_Activity or E8_Acquisition should be typed appropriately (AAT 300417639 for cessions, AAT 300027623 for declarations, or appropriate type for donations and dowries). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_4_Cession_of_Rights_Contract
            gmn:E31_5_Declaration
            gmn:E31_7_Donation_Contract
            gmn:E31_8_Dowry_Contract
        )
    ] ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-18"^^xsd:date ;
    dcterms:modified "2025-10-25"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P22_transferred_title_to, cidoc:P01_has_domain .
```

### P70.34 indicates object of dowry

```turtle
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

## Transformation Examples

### Example 1: Basic Dowry Contract

**Input (shortcut):**
```turtle
<dowry001> a gmn:E31_8_Dowry_Contract ;
    gmn:P70_32_indicates_donor <father_giovanni> ;
    gmn:P70_22_indicates_receiving_party <bride_maria> ;
    gmn:P70_34_indicates_object_of_dowry <house_genoa> ;
    gmn:P94i_1_was_created_by <notary_antonio> ;
    gmn:P94i_2_has_enactment_date "1450-03-15"^^xsd:date .
```

**Output (CIDOC-CRM compliant):**
```turtle
<dowry001> a gmn:E31_8_Dowry_Contract ;
    cidoc:P70_documents <dowry001/acquisition> ;
    cidoc:P94i_was_created_by <dowry001/creation> .

<dowry001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <father_giovanni> ;
    cidoc:P22_transferred_title_to <bride_maria> ;
    cidoc:P24_transferred_title_of <house_genoa> .

<dowry001/creation> a cidoc:E65_Creation ;
    cidoc:P14_carried_out_by <notary_antonio> ;
    cidoc:P4_has_time-span <dowry001/creation/timespan> .

<dowry001/creation/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1450-03-15"^^xsd:date .
```

### Example 2: Complex Dowry with Multiple Properties

**Input (shortcut):**
```turtle
<dowry002> a gmn:E31_8_Dowry_Contract ;
    gmn:P1_1_has_name "Dowry of Maria Spinola"@en ;
    gmn:P102_1_has_title "Dos data per patrem Marie Spinola"@la ;
    gmn:P70_32_indicates_donor <giacomo_spinola> ;
    gmn:P70_22_indicates_receiving_party <maria_spinola> ;
    gmn:P70_34_indicates_object_of_dowry <house_piazza_banchi> , <vineyard_albaro> ;
    gmn:P70_16_documents_sale_price_amount "1000.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <lira_genovese> ;
    gmn:P94i_1_was_created_by <notary_basso> ;
    gmn:P94i_2_has_enactment_date "1455-06-20"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <genoa> ;
    gmn:P46i_1_is_contained_in <register_1455> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<dowry002> a gmn:E31_8_Dowry_Contract ;
    cidoc:P1_is_identified_by <dowry002/appellation/1> ;
    cidoc:P102_has_title <dowry002/title/1> ;
    cidoc:P70_documents <dowry002/acquisition> ;
    cidoc:P94i_was_created_by <dowry002/creation> ;
    cidoc:P46i_forms_part_of <register_1455> .

<dowry002/appellation/1> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Dowry of Maria Spinola"@en .

<dowry002/title/1> a cidoc:E35_Title ;
    cidoc:P190_has_symbolic_content "Dos data per patrem Marie Spinola"@la .

<dowry002/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <giacomo_spinola> ;
    cidoc:P22_transferred_title_to <maria_spinola> ;
    cidoc:P24_transferred_title_of <house_piazza_banchi> , <vineyard_albaro> ;
    cidoc:P177_assigned_property_of_type <dowry002/acquisition/monetary_amount> .

<dowry002/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P181_has_amount "1000.00"^^xsd:decimal ;
    cidoc:P180_has_currency <lira_genovese> .

<dowry002/creation> a cidoc:E65_Creation ;
    cidoc:P14_carried_out_by <notary_basso> ;
    cidoc:P4_has_time-span <dowry002/creation/timespan> ;
    cidoc:P7_took_place_at <genoa> .

<dowry002/creation/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1455-06-20"^^xsd:date .
```

## Implementation Notes

1. **Shared Properties**: Dowry contracts reuse existing properties:
   - `gmn:P70_32_indicates_donor` (shared with donations)
   - `gmn:P70_22_indicates_receiving_party` (shared with cessions, declarations, donations)
   - Price properties `gmn:P70_16` and `gmn:P70_17` can be used to document dowry value

2. **E8_Acquisition Structure**: Like sales and donations, dowry contracts use E8_Acquisition to model the transfer of ownership rights

3. **Multiple Objects**: The `gmn:P70_34_indicates_object_of_dowry` property can be used multiple times when a dowry includes several properties or items

4. **Distinction from Donations**: While structurally similar to donations, dowry contracts are distinguished by:
   - Their specific context (marriage arrangements)
   - Separate class (E31_8 vs E31_7)
   - Specific property for dowry objects (P70_34 vs P70_33)

## Comparison with Similar Contract Types

| Aspect | Sales Contract | Donation Contract | Dowry Contract |
|--------|---------------|-------------------|----------------|
| Central Event | E8_Acquisition | E8_Acquisition | E8_Acquisition |
| Transferring Party | P23 (seller) via P70.1 | P23 (donor) via P70.32 | P23 (donor) via P70.32 |
| Receiving Party | P22 (buyer) via P70.2 | P22 (donee) via P70.22 | P22 (receiving party) via P70.22 |
| Object | P24 (property) via P70.3 | P24 (property) via P70.33 | P24 (dowry object) via P70.34 |
| Context | Commercial sale | Voluntary gift | Marriage arrangement |
| Payment | Required (P70.16-17) | Not expected | Often specified (P70.16-17) |

## Update Required in Main Python Script

Add these transformation functions to the `transform_item()` function:

```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    # ... existing transformations ...
    
    # Dowry contract properties (P70.34)
    item = transform_p70_34_indicates_object_of_dowry(item)
    
    # ... rest of transformations ...
    return item
```

The transformation function for P70.34:

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

Note: The transformations for P70.32 and P70.22 already exist and will automatically handle dowry contracts once the domain is updated in the ontology file.
