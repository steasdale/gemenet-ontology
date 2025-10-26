# E31.5 Declaration - Implementation Guide

## Table of Contents
1. [Pre-Implementation Checklist](#pre-implementation-checklist)
2. [Step 1: Ontology Modifications](#step-1-ontology-modifications)
3. [Step 2: Python Script Modifications](#step-2-python-script-modifications)
4. [Step 3: Testing](#step-3-testing)
5. [Step 4: Validation](#step-4-validation)
6. [Troubleshooting](#troubleshooting)

---

## Pre-Implementation Checklist

Before beginning implementation, ensure you have:

- [ ] Access to `gmn_ontology.ttl` file
- [ ] Access to `gmn_to_cidoc_transform_script.py` file
- [ ] Backup copies of both files
- [ ] RDF validation tool (e.g., rapper, RDFLib)
- [ ] Python 3.7+ environment
- [ ] Understanding of CIDOC-CRM basics
- [ ] Sample declaration data for testing

---

## Step 1: Ontology Modifications

### 1.1 Locate the Document Classes Section

Open `gmn_ontology.ttl` and find the section containing document class definitions (likely near E31_1_Contract, E31_2_Sales_Contract, etc.).

### 1.2 Add E31_5_Declaration Class

Add the following class definition:

```turtle
# Class: E31.5 Declaration
gmn:E31_5_Declaration
    a owl:Class ;
    rdfs:subClassOf cidoc:E31_Document ;
    rdfs:label "E31.5 Declaration"@en ;
    rdfs:comment "Specialized class that describes declaration documents. This is a specialized type of cidoc:E31_Document used to represent legal documents where one party (the declarant) makes a formal statement, acknowledgment, or assertion to another party (the recipient) regarding a specific subject matter. Declarations can be either notarial documents (recorded by a notary) or governmental documents (issued by official authorities without notarial involvement). Common types include declarations of debt, acknowledgments of obligations, statements of fact, official pronouncements, formal notifications, or governmental decrees. Unlike contracts (E31.1) which typically involve bilateral agreements, declarations are unilateral statements, though they have legal effect and may create or acknowledge obligations. Some declarations may be recorded in notarial registers alongside contracts, while others exist as independent governmental or administrative documents. Instances of this class represent the physical or conceptual document itself, while the actual declaration activity and its effects are modeled through E7_Activity that the document documents (via P70_documents)."@en ;
    dcterms:created "2025-10-25"^^xsd:date ;
    rdfs:seeAlso cidoc:E31_Document, cidoc:E7_Activity, cidoc:P70_documents .
```

### 1.3 Add P70_24_indicates_declarant Property

Locate the properties section and add:

```turtle
# Property: P70.24 indicates declarant
gmn:P70_24_indicates_declarant
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.24 indicates declarant"@en ;
    rdfs:comment "Simplified property for associating a declaration document with the person or entity making the declaration. The declarant is the party who is formally stating, acknowledging, or asserting something. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor. The E7_Activity should be typed as a declaration (AAT 300027623). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_5_Declaration ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-25"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

### 1.4 Add P70_25_indicates_declaration_subject Property

Add the following property:

```turtle
# Property: P70.25 indicates declaration subject
gmn:P70_25_indicates_declaration_subject
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.25 indicates declaration subject"@en ;
    rdfs:comment "Simplified property for associating a declaration document with the subject matter being declared, acknowledged, or asserted. This can include debts being acknowledged, facts being stated, obligations being recognized, properties being claimed, rights being asserted, or any other matter that is the content of the declaration. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity. The E7_Activity should be typed as a declaration (AAT 300027623). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_5_Declaration ;
    rdfs:range cidoc:E1_CRM_Entity ;
    dcterms:created "2025-10-25"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P16_used_specific_object .
```

### 1.5 Update P70_22_indicates_receiving_party Property

Find the existing `gmn:P70_22_indicates_receiving_party` property definition and **replace** it with:

```turtle
# Property: P70.22 indicates receiving party (updated)
gmn:P70_22_indicates_receiving_party
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.22 indicates receiving party"@en ;
    rdfs:comment "Simplified property for associating a document with the person or entity receiving something in the documented activity. In cession of rights contracts, this is the party receiving the ceded rights. In declarations, this is the party to whom the declaration is addressed or directed. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P01_has_domain > E39_Actor (using the inverse P01i_is_domain_of for declarations) OR E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor (for cessions, where both parties carry out the activity). The E7_Activity should be typed appropriately (AAT 300417639 for cessions, AAT 300027623 for declarations). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_4_Cession_of_Rights_Contract
            gmn:E31_5_Declaration
        )
    ] ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-25"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P01_has_domain .
```

### 1.6 Validate TTL Syntax

Run a validation tool to ensure no syntax errors:

```bash
rapper -i turtle -o turtle gmn_ontology.ttl > /dev/null
```

If there are errors, review the additions and fix any typos or formatting issues.

---

## Step 2: Python Script Modifications

### 2.1 Add AAT Constant

Open `gmn_to_cidoc_transform_script.py` and locate the constants section at the top of the file (where other AAT URIs are defined). Add:

```python
# Getty AAT URI for declarations
AAT_DECLARATION = "http://vocab.getty.edu/page/aat/300027623"
```

### 2.2 Add transform_p70_24_indicates_declarant Function

Add the following function (recommend placing it after other P70 transformation functions):

```python
def transform_p70_24_indicates_declarant(data):
    """
    Transform gmn:P70_24_indicates_declarant to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_24_indicates_declarant' not in data:
        return data
    
    declarants = data['gmn:P70_24_indicates_declarant']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if declaration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing declaration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new declaration activity
        activity_uri = f"{subject_uri}/declaration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_DECLARATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # Initialize P14 if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_activity:
        existing_activity['cidoc:P14_carried_out_by'] = []
    
    # Add declarants to declaration activity
    for declarant_obj in declarants:
        # Handle both URI references and full objects
        if isinstance(declarant_obj, dict):
            declarant_data = declarant_obj.copy()
            if '@type' not in declarant_data:
                declarant_data['@type'] = 'cidoc:E39_Actor'
        else:
            declarant_uri = str(declarant_obj)
            declarant_data = {
                '@id': declarant_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add to declaration activity
        existing_activity['cidoc:P14_carried_out_by'].append(declarant_data)
    
    # Remove shortcut property
    del data['gmn:P70_24_indicates_declarant']
    
    return data
```

### 2.3 Update transform_p70_22_indicates_receiving_party Function

**Replace** the existing `transform_p70_22_indicates_receiving_party` function with this updated version that handles both cessions and declarations:

```python
def transform_p70_22_indicates_receiving_party(data):
    """
    Transform gmn:P70_22_indicates_receiving_party to full CIDOC-CRM structure.
    
    Handles two different document types:
    - For E31_4_Cession_of_Rights_Contract: P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    - For E31_5_Declaration: P70_documents > E7_Activity > P01_has_domain > E39_Actor
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_22_indicates_receiving_party' not in data:
        return data
    
    receiving_parties = data['gmn:P70_22_indicates_receiving_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Determine document type to decide which property to use
    is_declaration = False
    is_cession = False
    
    if '@type' in data:
        types = data['@type'] if isinstance(data['@type'], list) else [data['@type']]
        is_declaration = 'gmn:E31_5_Declaration' in types
        is_cession = 'gmn:E31_4_Cession_of_Rights_Contract' in types
    
    # Check if activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new activity with appropriate type
        activity_uri = f"{subject_uri}/{'declaration' if is_declaration else 'cession'}"
        activity_type = AAT_DECLARATION if is_declaration else AAT_TRANSFER_OF_RIGHTS
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': activity_type,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # For declarations, use P01_has_domain
    # For cessions, use P14_carried_out_by (both parties actively carry out the cession)
    property_key = 'cidoc:P01_has_domain' if is_declaration else 'cidoc:P14_carried_out_by'
    
    # Initialize property if it doesn't exist
    if property_key not in existing_activity:
        existing_activity[property_key] = []
    
    # Add receiving parties
    for party_obj in receiving_parties:
        # Handle both URI references and full objects
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
        
        # Add to activity
        existing_activity[property_key].append(party_data)
    
    # Remove shortcut property
    del data['gmn:P70_22_indicates_receiving_party']
    
    return data
```

### 2.4 Add transform_p70_25_indicates_declaration_subject Function

Add the following function:

```python
def transform_p70_25_indicates_declaration_subject(data):
    """
    Transform gmn:P70_25_indicates_declaration_subject to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_25_indicates_declaration_subject' not in data:
        return data
    
    subjects = data['gmn:P70_25_indicates_declaration_subject']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if declaration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing declaration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new declaration activity
        activity_uri = f"{subject_uri}/declaration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_DECLARATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # Initialize P16 if it doesn't exist
    if 'cidoc:P16_used_specific_object' not in existing_activity:
        existing_activity['cidoc:P16_used_specific_object'] = []
    
    # Add declaration subjects
    for subject_obj in subjects:
        # Handle both URI references and full objects
        if isinstance(subject_obj, dict):
            subject_data = subject_obj.copy()
            if '@type' not in subject_data:
                subject_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            subj_uri = str(subject_obj)
            subject_data = {
                '@id': subj_uri,
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        # Add to declaration activity
        existing_activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    # Remove shortcut property
    del data['gmn:P70_25_indicates_declaration_subject']
    
    return data
```

### 2.5 Update transform_item Function

Locate the `transform_item()` function and find the section where property transformations are called. **IMPORTANT**: The order matters! Add these lines in the correct position:

```python
def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    """
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    item = transform_p1_3_has_patrilineal_name(item)
    item = transform_p102_1_has_title(item)
    item = transform_p94i_1_was_created_by(item)
    item = transform_p94i_2_has_enactment_date(item)
    item = transform_p94i_3_has_place_of_enactment(item)
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
    item = transform_p70_12_documents_payment_through_organization(item)
    item = transform_p70_13_documents_referenced_place(item)
    item = transform_p70_14_documents_referenced_object(item)
    item = transform_p70_15_documents_witness(item)
    item = transform_p70_16_documents_sale_price_amount(item)
    item = transform_p70_17_documents_sale_price_currency(item)
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
    item = transform_p70_21_indicates_conceding_party(item)
    # NOTE: P70.22 MUST be called AFTER P70.21 (conceding party) and P70.24 (declarant)
    # so that the activity type is already set when determining which property to use
    item = transform_p70_24_indicates_declarant(item)
    item = transform_p70_22_indicates_receiving_party(item)
    item = transform_p70_23_indicates_object_of_cession(item)
    item = transform_p70_25_indicates_declaration_subject(item)
    # Continue with other transformations...
    item = transform_p138i_1_has_representation(item)
    item = transform_p1_4_has_loconym(item)
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)
    item = transform_p11i_3_has_spouse(item)
    item = transform_p22_1_has_owner(item)
    item = transform_p53_1_has_occupant(item)
    item = transform_p96_1_has_mother(item)
    item = transform_p97_1_has_father(item)
    item = transform_p107i_1_has_regional_provenance(item)
    item = transform_p107i_2_has_social_category(item)
    item = transform_p107i_3_has_occupation(item)
    item = transform_p3_1_has_editorial_note(item, include_internal)
    return item
```

### 2.6 Test Python Syntax

Run a basic syntax check:

```bash
python -m py_compile gmn_to_cidoc_transform_script.py
```

---

## Step 3: Testing

### 3.1 Create Test Data

Create a test file `test_declaration.json` with sample declaration data:

```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@graph": [
    {
      "@id": "https://example.org/declaration/001",
      "@type": "gmn:E31_5_Declaration",
      "gmn:P102_1_has_title": "Declaration of Debt by Giovanni Rossi",
      "gmn:P70_24_indicates_declarant": {
        "@id": "https://example.org/person/giovanni_rossi",
        "@type": "cidoc:E21_Person"
      },
      "gmn:P70_22_indicates_receiving_party": {
        "@id": "https://example.org/person/paolo_bianchi",
        "@type": "cidoc:E21_Person"
      },
      "gmn:P70_25_indicates_declaration_subject": {
        "@id": "https://example.org/debt/500_lire",
        "@type": "cidoc:E1_CRM_Entity"
      },
      "gmn:P94i_2_has_enactment_date": "1450-03-15"
    },
    {
      "@id": "https://example.org/declaration/002",
      "@type": "gmn:E31_5_Declaration",
      "gmn:P102_1_has_title": "Governmental Tax Exemption Declaration",
      "gmn:P70_24_indicates_declarant": {
        "@id": "https://example.org/org/doge_office",
        "@type": "cidoc:E74_Group"
      },
      "gmn:P70_22_indicates_receiving_party": {
        "@id": "https://example.org/group/genoa_merchants",
        "@type": "cidoc:E74_Group"
      },
      "gmn:P70_25_indicates_declaration_subject": {
        "@id": "https://example.org/policy/tax_exemption_1450",
        "@type": "cidoc:E73_Information_Object"
      },
      "gmn:P94i_2_has_enactment_date": "1450-06-15",
      "gmn:P94i_3_has_place_of_enactment": {
        "@id": "https://example.org/place/genoa_palace"
      }
    }
  ]
}
```

### 3.2 Run Transformation

Execute the transformation script:

```bash
python gmn_to_cidoc_transform_script.py --input test_declaration.json --output test_declaration_output.json
```

### 3.3 Verify Output Structure

Check that the output contains the expected CIDOC-CRM structure. For the first declaration, you should see:

```json
{
  "@id": "https://example.org/declaration/001",
  "@type": "gmn:E31_5_Declaration",
  "cidoc:P102_has_title": {
    "@value": "Declaration of Debt by Giovanni Rossi"
  },
  "cidoc:P70_documents": [
    {
      "@id": "https://example.org/declaration/001/declaration",
      "@type": "cidoc:E7_Activity",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300027623",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P14_carried_out_by": [
        {
          "@id": "https://example.org/person/giovanni_rossi",
          "@type": "cidoc:E21_Person"
        }
      ],
      "cidoc:P01_has_domain": [
        {
          "@id": "https://example.org/person/paolo_bianchi",
          "@type": "cidoc:E21_Person"
        }
      ],
      "cidoc:P16_used_specific_object": [
        {
          "@id": "https://example.org/debt/500_lire",
          "@type": "cidoc:E1_CRM_Entity"
        }
      ]
    }
  ],
  "cidoc:P94i_was_created_by": {
    "@id": "https://example.org/declaration/001/creation",
    "@type": "cidoc:E65_Creation",
    "cidoc:P4_has_time-span": {
      "@type": "cidoc:E52_Time-Span",
      "cidoc:P82_at_some_time_within": "1450-03-15"
    }
  }
}
```

### 3.4 Verify Key Points

Check that:
- [ ] All three properties (P70.24, P70.22, P70.25) share the same E7_Activity node
- [ ] The activity is typed as AAT 300027623 (declarations)
- [ ] P70.24 transforms to P14_carried_out_by
- [ ] P70.22 transforms to P01_has_domain (not P14_carried_out_by)
- [ ] P70.25 transforms to P16_used_specific_object
- [ ] No gmn:P70_24, gmn:P70_22, or gmn:P70_25 properties remain in output

---

## Step 4: Validation

### 4.1 Validate Against CIDOC-CRM

Verify that the output conforms to CIDOC-CRM patterns:

1. **E7_Activity Structure**: Check that declaration activities have:
   - P2_has_type pointing to AAT concept
   - P14_carried_out_by for declarant
   - P01_has_domain for recipient
   - P16_used_specific_object for subject

2. **Property Domains and Ranges**: Verify that:
   - P14_carried_out_by points to E39_Actor subclasses
   - P01_has_domain points to E39_Actor subclasses
   - P16_used_specific_object points to E1_CRM_Entity

### 4.2 Test with Cession Comparison

Create a test file with both a cession and a declaration to verify P70.22 works differently for each:

```json
{
  "@graph": [
    {
      "@id": "https://example.org/cession/001",
      "@type": "gmn:E31_4_Cession_of_Rights_Contract",
      "gmn:P70_21_indicates_conceding_party": {
        "@id": "https://example.org/person/marco"
      },
      "gmn:P70_22_indicates_receiving_party": {
        "@id": "https://example.org/person/luca"
      }
    },
    {
      "@id": "https://example.org/declaration/001",
      "@type": "gmn:E31_5_Declaration",
      "gmn:P70_24_indicates_declarant": {
        "@id": "https://example.org/person/giovanni"
      },
      "gmn:P70_22_indicates_receiving_party": {
        "@id": "https://example.org/person/paolo"
      }
    }
  ]
}
```

Verify that in the output:
- Cession's P70.22 becomes P14_carried_out_by
- Declaration's P70.22 becomes P01_has_domain

### 4.3 Validate RDF Serialization

If converting to RDF/XML or Turtle, validate with:

```bash
rapper -i json-ld -o turtle test_declaration_output.json > test_declaration.ttl
rapper -c test_declaration.ttl
```

---

## Step 5: Integration Testing

### 5.1 Test with Real Data

Once basic tests pass, test with actual declaration data from your corpus:

1. Select 5-10 declaration documents
2. Create simplified JSON-LD entries
3. Run transformation
4. Review output for accuracy
5. Check for any edge cases or errors

### 5.2 Test Order Dependencies

Verify transformation order by creating test data where:
- P70.22 appears before P70.24 in the JSON
- Both properties reference the same activity
- Output correctly shares activity node

### 5.3 Test Notarial vs. Governmental Declarations

Create examples of both types:

**Notarial Declaration:**
```json
{
  "@id": "https://example.org/declaration/notarial_001",
  "@type": "gmn:E31_5_Declaration",
  "gmn:P94i_1_was_created_by": {
    "@id": "https://example.org/person/notary_antonio"
  },
  "gmn:P70_24_indicates_declarant": {...}
}
```

**Governmental Declaration:**
```json
{
  "@id": "https://example.org/declaration/gov_001",
  "@type": "gmn:E31_5_Declaration",
  "gmn:P70_24_indicates_declarant": {
    "@id": "https://example.org/org/council_of_ancients"
  }
}
```

Verify both transform correctly, with or without notary information.

---

## Troubleshooting

### Issue 1: P70.22 Not Using P01_has_domain for Declarations

**Symptoms**: P70.22 transforms to P14_carried_out_by for declarations instead of P01_has_domain

**Solution**: 
1. Verify P70.24 is called BEFORE P70.22 in transform_item()
2. Check that '@type' contains 'gmn:E31_5_Declaration'
3. Ensure is_declaration check in transform_p70_22 is working

**Debug**:
```python
# Add debug prints in transform_p70_22_indicates_receiving_party
print(f"Document types: {data.get('@type')}")
print(f"Is declaration: {is_declaration}")
print(f"Property key: {property_key}")
```

### Issue 2: Multiple Activity Nodes Created

**Symptoms**: Each property creates its own E7_Activity instead of sharing one

**Solution**:
1. Check that all transformation functions check for existing 'cidoc:P70_documents'
2. Verify activity is being reused when it exists
3. Ensure functions retrieve existing_activity[0] consistently

### Issue 3: AAT Type Not Applied

**Symptoms**: E7_Activity lacks P2_has_type or has wrong type

**Solution**:
1. Verify AAT_DECLARATION constant is defined
2. Check that activity creation includes P2_has_type
3. Ensure existing activities aren't overwriting the type

### Issue 4: Shortcut Properties Remain in Output

**Symptoms**: gmn:P70_24, gmn:P70_22, or gmn:P70_25 appear in final output

**Solution**:
1. Verify `del data['gmn:P70_XX']` statements are executing
2. Check that transformation functions are being called
3. Ensure no errors during transformation that skip deletion

### Issue 5: Transformation Order Errors

**Symptoms**: KeyError or unexpected behavior

**Solution**:
1. Review transform_item() order
2. Ensure P70.24 before P70.22
3. Check that all functions handle missing properties gracefully

### Issue 6: RDF Validation Errors

**Symptoms**: Rapper or other validators reject output

**Solution**:
1. Check JSON-LD context definitions
2. Verify all URIs are properly formatted
3. Ensure namespace prefixes are consistent
4. Validate against JSON-LD specification

---

## Post-Implementation Checklist

After completing implementation and testing:

- [ ] All TTL additions validated
- [ ] All Python functions added and tested
- [ ] transform_item() updated with correct ordering
- [ ] Sample declarations transform correctly
- [ ] Both notarial and governmental declarations work
- [ ] P70.22 behaves correctly for both cessions and declarations
- [ ] RDF output validates
- [ ] Documentation updated
- [ ] Team notified of new class availability
- [ ] Omeka-S templates updated (if applicable)
- [ ] Data entry guidelines updated

---

## Additional Resources

### CIDOC-CRM Documentation
- P01_has_domain: http://www.cidoc-crm.org/Property/P01-has-domain/version-7.1.1
- P14_carried_out_by: http://www.cidoc-crm.org/Property/P14-carried-out-by/version-7.1.1
- P16_used_specific_object: http://www.cidoc-crm.org/Property/P16-used-specific-object/version-7.1.1
- E7_Activity: http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.1

### Getty AAT
- Declarations: http://vocab.getty.edu/page/aat/300027623

### Related GMN Documentation
- Cession of Rights (shares P70.22): See cession documentation
- Sales Contracts: See main ontology documentation
- Arbitration Agreements: See arbitration documentation

---

## Support

For questions or issues during implementation:
1. Review the declaration-documentation.md file for semantic details
2. Check troubleshooting section above
3. Validate syntax with appropriate tools
4. Contact the ontology maintainer if issues persist
