# Implementation Guide: P70.22 Indicates Receiving Party
## Step-by-Step Instructions for Full Implementation

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Ontology File Updates](#phase-1-ontology-file-updates)
3. [Phase 2: Python Transformation Script Updates](#phase-2-python-transformation-script-updates)
4. [Phase 3: Testing Procedures](#phase-3-testing-procedures)
5. [Phase 4: Documentation Updates](#phase-4-documentation-updates)
6. [Phase 5: Deployment](#phase-5-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script
- Documentation files: `donation-documentation.md`, `dowry-documentation.md`

### Required Tools
- Text editor with Turtle syntax support
- Python 3.7+ environment
- TTL validator (e.g., rapper, riot)
- RDF visualization tool (optional, for validation)

### Required Knowledge
- Basic understanding of RDF/Turtle syntax
- Familiarity with CIDOC-CRM structure
- Python programming basics
- Understanding of the GMN ontology structure

---

## Phase 1: Ontology File Updates

### Step 1.1: Locate the Property Definition

Open `gmn_ontology.ttl` and search for:
```turtle
gmn:P70_22_indicates_receiving_party
```

You should find an existing property definition. This needs to be replaced with the updated version.

### Step 1.2: Backup Current Definition

Before making changes, copy the current definition to a backup file or comment it out:

```turtle
# BACKUP - Original definition before update (2025-10-28)
# gmn:P70_22_indicates_receiving_party
#     a owl:ObjectProperty ;
#     ... [rest of old definition]
```

### Step 1.3: Replace with Updated Definition

Delete or comment out the old definition and insert the new one from the `indicates-receiving-party-ontology.ttl` file:

```turtle
# Property: P70.22 indicates receiving party
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

### Step 1.4: Validate TTL Syntax

Validate the file using a TTL validator:

```bash
# Using rapper
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Using riot (from Apache Jena)
riot --validate gmn_ontology.ttl
```

If validation errors occur, check:
- All angle brackets are properly closed
- All strings are properly quoted
- No duplicate property definitions exist
- Prefix declarations are present at the top of file

### Step 1.5: Commit Changes

```bash
git add gmn_ontology.ttl
git commit -m "Updated P70.22 indicates receiving party property - added dowry support and refined CIDOC-CRM paths"
```

---

## Phase 2: Python Transformation Script Updates

### Step 2.1: Locate the Transformation Function

Open `gmn_to_cidoc_transform.py` and search for:
```python
def transform_p70_22_indicates_receiving_party(data):
```

### Step 2.2: Check Required Imports

At the top of the file, ensure these imports are present:

```python
from uuid import uuid4
import json
```

If missing, add them to the import section.

### Step 2.3: Replace the Transformation Function

Delete the existing `transform_p70_22_indicates_receiving_party()` function and replace it with the updated version from `indicates-receiving-party-transform.py`:

```python
def transform_p70_22_indicates_receiving_party(data):
    """
    Transform gmn:P70_22_indicates_receiving_party to full CIDOC-CRM structure.
    
    Handles multiple document types with different transformation paths:
    - Cessions: P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    - Declarations: P70_documents > E7_Activity > P01_has_domain > E39_Actor
    - Donations: P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
    - Dowries: P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
    
    UPDATED VERSION - replaces existing function in gmn_to_cidoc_transform.py
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
    is_dowry = 'gmn:E31_8_Dowry_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_8_Dowry_Contract'
    
    if is_donation or is_dowry:
        # For donations and dowries, use E8_Acquisition
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
        # For declarations, use E7_Activity with P01_has_domain
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            activity_uri = f"{subject_uri}/declaration"
            data['cidoc:P70_documents'] = [{
                '@id': activity_uri,
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': 'http://vocab.getty.edu/aat/300027623',
                    '@type': 'cidoc:E55_Type',
                    'rdfs:label': 'declarations'
                }
            }]
        
        activity = data['cidoc:P70_documents'][0]
        
        if 'cidoc:P01_has_domain' not in activity:
            activity['cidoc:P01_has_domain'] = []
        
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
            
            activity['cidoc:P01_has_domain'].append(party_data)
    
    elif is_cession:
        # For cessions, use E7_Activity with P14_carried_out_by
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            activity_uri = f"{subject_uri}/cession"
            data['cidoc:P70_documents'] = [{
                '@id': activity_uri,
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': 'http://vocab.getty.edu/aat/300417639',
                    '@type': 'cidoc:E55_Type',
                    'rdfs:label': 'transfers of rights'
                }
            }]
        
        activity = data['cidoc:P70_documents'][0]
        
        if 'cidoc:P14_carried_out_by' not in activity:
            activity['cidoc:P14_carried_out_by'] = []
        
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
            
            activity['cidoc:P14_carried_out_by'].append(party_data)
    
    # Remove the simplified property after transformation
    del data['gmn:P70_22_indicates_receiving_party']
    return data
```

### Step 2.4: Update transform_item() Function

Locate the `transform_item()` function and ensure it calls the receiving party transformation:

```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    # ... existing transformations ...
    
    # Add or verify this line is present:
    item = transform_p70_22_indicates_receiving_party(item)
    
    # ... remaining transformations ...
    return item
```

### Step 2.5: Test Function in Isolation

Create a test script to verify the function works:

```python
# test_p70_22.py
from gmn_to_cidoc_transform import transform_p70_22_indicates_receiving_party

# Test case 1: Donation
test_donation = {
    '@id': 'http://example.org/donation001',
    '@type': 'gmn:E31_7_Donation_Contract',
    'gmn:P70_22_indicates_receiving_party': [
        {'@id': 'http://example.org/person/maria'}
    ]
}

result = transform_p70_22_indicates_receiving_party(test_donation.copy())
print("Donation test result:")
print(json.dumps(result, indent=2))

# Test case 2: Declaration
test_declaration = {
    '@id': 'http://example.org/declaration001',
    '@type': 'gmn:E31_5_Declaration',
    'gmn:P70_22_indicates_receiving_party': [
        {'@id': 'http://example.org/person/giovanni'}
    ]
}

result = transform_p70_22_indicates_receiving_party(test_declaration.copy())
print("\nDeclaration test result:")
print(json.dumps(result, indent=2))
```

Run the test:
```bash
python test_p70_22.py
```

### Step 2.6: Commit Changes

```bash
git add gmn_to_cidoc_transform.py
git commit -m "Updated transform_p70_22_indicates_receiving_party function - added dowry support and improved type detection"
```

---

## Phase 3: Testing Procedures

### Step 3.1: Prepare Test Data

Create a test file `test_p70_22_data.json` with samples of each document type:

```json
{
  "@graph": [
    {
      "@id": "http://gmn.org/test/cession001",
      "@type": "gmn:E31_4_Cession_of_Rights_Contract",
      "gmn:P70_21_indicates_conceding_party": [
        {"@id": "http://gmn.org/actor/creditor_marco"}
      ],
      "gmn:P70_22_indicates_receiving_party": [
        {"@id": "http://gmn.org/actor/debtor_giovanni"}
      ],
      "gmn:P70_23_indicates_object_of_cession": [
        {"@id": "http://gmn.org/legal/debt_claim_001"}
      ]
    },
    {
      "@id": "http://gmn.org/test/declaration001",
      "@type": "gmn:E31_5_Declaration",
      "gmn:P70_24_indicates_declarant": [
        {"@id": "http://gmn.org/actor/merchant_pietro"}
      ],
      "gmn:P70_22_indicates_receiving_party": [
        {"@id": "http://gmn.org/actor/magistrate_antonio"}
      ],
      "gmn:P70_25_indicates_declaration_subject": [
        {"@id": "http://gmn.org/legal/debt_acknowledgment_001"}
      ]
    },
    {
      "@id": "http://gmn.org/test/donation001",
      "@type": "gmn:E31_7_Donation_Contract",
      "gmn:P70_32_indicates_donor": [
        {"@id": "http://gmn.org/actor/widow_maria"}
      ],
      "gmn:P70_22_indicates_receiving_party": [
        {"@id": "http://gmn.org/actor/hospital_pammatone"}
      ],
      "gmn:P70_33_indicates_object_of_donation": [
        {"@id": "http://gmn.org/property/warehouse_001"}
      ]
    },
    {
      "@id": "http://gmn.org/test/dowry001",
      "@type": "gmn:E31_8_Dowry_Contract",
      "gmn:P70_32_indicates_donor": [
        {"@id": "http://gmn.org/actor/father_filippo"}
      ],
      "gmn:P70_22_indicates_receiving_party": [
        {"@id": "http://gmn.org/actor/husband_luca"}
      ],
      "gmn:P70_34_indicates_object_of_dowry": [
        {"@id": "http://gmn.org/property/dowry_house_001"}
      ]
    }
  ]
}
```

### Step 3.2: Run Transformation on Test Data

```bash
python gmn_to_cidoc_transform.py test_p70_22_data.json output_p70_22.json
```

### Step 3.3: Validate Transformation Results

For each document type, verify the correct structure:

#### Cession Validation Checklist:
```
✓ P70_documents points to E7_Activity
✓ E7_Activity has P2_has_type = AAT 300417639
✓ E7_Activity has P14_carried_out_by with receiving party
✓ P14_carried_out_by also includes conceding party
✓ Original gmn:P70_22 property is removed
```

#### Declaration Validation Checklist:
```
✓ P70_documents points to E7_Activity
✓ E7_Activity has P2_has_type = AAT 300027623
✓ E7_Activity has P01_has_domain with receiving party
✓ E7_Activity has P14_carried_out_by with declarant
✓ Original gmn:P70_22 property is removed
```

#### Donation Validation Checklist:
```
✓ P70_documents points to E8_Acquisition
✓ E8_Acquisition has P22_transferred_title_to with receiving party
✓ E8_Acquisition has P23_transferred_title_from with donor
✓ E8_Acquisition has P24_transferred_title_of with donated object
✓ Original gmn:P70_22 property is removed
```

#### Dowry Validation Checklist:
```
✓ P70_documents points to E8_Acquisition
✓ E8_Acquisition has P22_transferred_title_to with receiving party
✓ E8_Acquisition has P23_transferred_title_from with donor
✓ E8_Acquisition has P24_transferred_title_of with dowry object
✓ Original gmn:P70_22 property is removed
```

### Step 3.4: Test Edge Cases

Create additional test cases for:

1. **Multiple receiving parties**:
```json
{
  "@id": "http://gmn.org/test/donation_multi",
  "@type": "gmn:E31_7_Donation_Contract",
  "gmn:P70_32_indicates_donor": [
    {"@id": "http://gmn.org/actor/benefactor"}
  ],
  "gmn:P70_22_indicates_receiving_party": [
    {"@id": "http://gmn.org/actor/recipient1"},
    {"@id": "http://gmn.org/actor/recipient2"}
  ]
}
```

2. **Mixed document types**:
```json
{
  "@id": "http://gmn.org/test/complex_doc",
  "@type": ["gmn:E31_7_Donation_Contract", "gmn:E31_1_Notarial_Document"],
  "gmn:P70_22_indicates_receiving_party": [
    {"@id": "http://gmn.org/actor/recipient"}
  ]
}
```

3. **Minimal data (only receiving party, no other properties)**:
```json
{
  "@id": "http://gmn.org/test/minimal",
  "@type": "gmn:E31_8_Dowry_Contract",
  "gmn:P70_22_indicates_receiving_party": [
    {"@id": "http://gmn.org/actor/spouse"}
  ]
}
```

### Step 3.5: Automated Test Suite

Create an automated test script `test_suite_p70_22.py`:

```python
import unittest
import json
from gmn_to_cidoc_transform import transform_p70_22_indicates_receiving_party

class TestP7022Transformation(unittest.TestCase):
    
    def test_donation_transformation(self):
        """Test that donations use E8_Acquisition with P22"""
        data = {
            '@id': 'http://test/doc1',
            '@type': 'gmn:E31_7_Donation_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor1'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        self.assertIn('cidoc:P70_documents', result)
        acquisition = result['cidoc:P70_documents'][0]
        self.assertEqual(acquisition['@type'], 'cidoc:E8_Acquisition')
        self.assertIn('cidoc:P22_transferred_title_to', acquisition)
        self.assertNotIn('gmn:P70_22_indicates_receiving_party', result)
    
    def test_declaration_transformation(self):
        """Test that declarations use E7_Activity with P01"""
        data = {
            '@id': 'http://test/doc2',
            '@type': 'gmn:E31_5_Declaration',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor2'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        self.assertIn('cidoc:P70_documents', result)
        activity = result['cidoc:P70_documents'][0]
        self.assertEqual(activity['@type'], 'cidoc:E7_Activity')
        self.assertIn('cidoc:P01_has_domain', activity)
        self.assertNotIn('gmn:P70_22_indicates_receiving_party', result)
    
    def test_cession_transformation(self):
        """Test that cessions use E7_Activity with P14"""
        data = {
            '@id': 'http://test/doc3',
            '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor3'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        self.assertIn('cidoc:P70_documents', result)
        activity = result['cidoc:P70_documents'][0]
        self.assertEqual(activity['@type'], 'cidoc:E7_Activity')
        self.assertIn('cidoc:P14_carried_out_by', activity)
        self.assertNotIn('gmn:P70_22_indicates_receiving_party', result)
    
    def test_dowry_transformation(self):
        """Test that dowries use E8_Acquisition with P22"""
        data = {
            '@id': 'http://test/doc4',
            '@type': 'gmn:E31_8_Dowry_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor4'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        self.assertIn('cidoc:P70_documents', result)
        acquisition = result['cidoc:P70_documents'][0]
        self.assertEqual(acquisition['@type'], 'cidoc:E8_Acquisition')
        self.assertIn('cidoc:P22_transferred_title_to', acquisition)
        self.assertNotIn('gmn:P70_22_indicates_receiving_party', result)
    
    def test_multiple_receiving_parties(self):
        """Test handling of multiple receiving parties"""
        data = {
            '@id': 'http://test/doc5',
            '@type': 'gmn:E31_7_Donation_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor5a'},
                {'@id': 'http://test/actor5b'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        acquisition = result['cidoc:P70_documents'][0]
        self.assertEqual(len(acquisition['cidoc:P22_transferred_title_to']), 2)
    
    def test_no_receiving_party(self):
        """Test that transformation is skipped when property is absent"""
        data = {
            '@id': 'http://test/doc6',
            '@type': 'gmn:E31_7_Donation_Contract'
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        # Should return unchanged
        self.assertEqual(data, result)

if __name__ == '__main__':
    unittest.main()
```

Run the test suite:
```bash
python test_suite_p70_22.py
```

Expected output:
```
......
----------------------------------------------------------------------
Ran 6 tests in 0.012s

OK
```

---

## Phase 4: Documentation Updates

### Step 4.1: Update Donation Documentation

Open `donation-documentation.md` and add P70.22 examples. Insert the content from `indicates-receiving-party-doc-note.txt` in the appropriate section.

### Step 4.2: Update Dowry Documentation

Open `dowry-documentation.md` and add P70.22 examples. Ensure cross-references to donation documentation are included.

### Step 4.3: Update Property Comparison Tables

If comparison tables exist, update them to include P70.22:

```markdown
| Property | Cession | Declaration | Donation | Dowry |
|----------|---------|-------------|----------|-------|
| P70.22 (receiving party) | Acquires rights | Addressee | Donee | Receiving spouse |
| CIDOC Path | P14 (E7) | P01 (E7) | P22 (E8) | P22 (E8) |
| Semantic Role | Co-participant | Target | Beneficiary | Beneficiary |
```

### Step 4.4: Add Cross-References

Ensure these cross-references are present:
- From P70.21 (conceding party) to P70.22 (complementary in cessions)
- From P70.32 (donor) to P70.22 (complementary in donations and dowries)
- Between P70.22 sections in different document type files

---

## Phase 5: Deployment

### Step 5.1: Final Validation

Run complete validation suite:

```bash
# Validate ontology syntax
rapper -i turtle -o ntriples gmn_ontology.ttl > /dev/null

# Run transformation on full dataset
python gmn_to_cidoc_transform.py full_dataset.json transformed_output.json

# Run unit tests
python test_suite_p70_22.py

# Validate output RDF
rapper -i jsonld -o ntriples transformed_output.json > /dev/null
```

### Step 5.2: Create Release Branch

```bash
git checkout -b release/p70-22-update
git push origin release/p70-22-update
```

### Step 5.3: Merge to Main

After review and approval:

```bash
git checkout main
git merge release/p70-22-update
git push origin main
```

### Step 5.4: Tag Release

```bash
git tag -a v1.2.0 -m "Added P70.22 indicates receiving party with dowry support"
git push origin v1.2.0
```

### Step 5.5: Update Production

Deploy the updated files to production environment according to your deployment procedures.

---

## Troubleshooting

### Issue 1: TTL Validation Fails

**Symptom**: Rapper or riot reports syntax errors

**Solution**:
- Check that all IRIs are properly formatted in angle brackets
- Verify that the `owl:unionOf` list is properly closed
- Ensure no duplicate property definitions exist
- Check that all required prefixes are declared

### Issue 2: Wrong Transformation Path Selected

**Symptom**: Donation uses P01 instead of P22, or declaration uses P22 instead of P01

**Solution**:
- Verify that document type is correctly specified in `@type`
- Check that type detection logic uses `isinstance()` for list types
- Ensure no conflicting document types are assigned
- Add debug logging to see which branch is being executed

### Issue 3: E8_Acquisition Not Shared Properly

**Symptom**: Multiple E8_Acquisition nodes created instead of one shared node

**Solution**:
- Ensure all related properties check for existing acquisition before creating
- Verify acquisition URI generation is consistent (`{subject_uri}/acquisition`)
- Check transformation order in `transform_item()` function

### Issue 4: Actor Type Not Added

**Symptom**: Receiving party objects don't have `cidoc:E39_Actor` type

**Solution**:
- Verify that the type-adding logic is present in transformation function
- Check that both dict and URI-only forms are handled
- Ensure type is only added when not already present

### Issue 5: Property Not Removed After Transformation

**Symptom**: Both `gmn:P70_22` and CIDOC-CRM properties exist in output

**Solution**:
- Verify that `del data['gmn:P70_22_indicates_receiving_party']` is executed
- Check that transformation function returns modified data
- Ensure no exceptions are silently caught before deletion

### Issue 6: Multiple Receiving Parties Not Handled

**Symptom**: Only first receiving party is transformed

**Solution**:
- Verify that transformation iterates over all items in receiving_parties list
- Check that each party is appended to the target property array
- Ensure array is initialized before appending

---

## Performance Considerations

### Optimization Tips

1. **Batch Processing**: Process documents in batches rather than one at a time
2. **Type Caching**: Cache document type detection results if processing multiple properties
3. **URI Validation**: Pre-validate URIs before transformation to avoid repeated checks
4. **Parallel Processing**: Consider using multiprocessing for large datasets

### Benchmarking

To measure transformation performance:

```python
import time

start_time = time.time()
result = transform_p70_22_indicates_receiving_party(large_dataset)
end_time = time.time()

print(f"Transformation took {end_time - start_time:.2f} seconds")
print(f"Processed {len(large_dataset)} items")
print(f"Average: {(end_time - start_time) / len(large_dataset):.4f} seconds per item")
```

---

## Rollback Procedures

If issues arise after deployment:

### Step 1: Revert Ontology Changes

```bash
git checkout HEAD~1 gmn_ontology.ttl
```

### Step 2: Revert Python Changes

```bash
git checkout HEAD~1 gmn_to_cidoc_transform.py
```

### Step 3: Validate Rollback

```bash
python test_suite_p70_22.py
```

### Step 4: Notify Stakeholders

Send notification about rollback with details of issues encountered.

---

## Additional Resources

- **CIDOC-CRM Official Documentation**: http://www.cidoc-crm.org/
- **RDF 1.1 Turtle Specification**: https://www.w3.org/TR/turtle/
- **Getty AAT Vocabulary**: http://vocab.getty.edu/aat/
- **JSON-LD Specification**: https://www.w3.org/TR/json-ld11/

---

## Support

For questions or issues during implementation:
1. Review this guide and the semantic documentation
2. Check the troubleshooting section
3. Consult project documentation files
4. Contact the ontology maintainer

---

**Last Updated**: 2025-10-28  
**Version**: 1.0  
**Compatibility**: GMN Ontology v1.0+, CIDOC-CRM v7.1+
