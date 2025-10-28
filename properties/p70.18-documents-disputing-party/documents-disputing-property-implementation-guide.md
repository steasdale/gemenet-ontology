# Implementation Guide: P70.18 Documents Disputing Party Property

This guide provides complete step-by-step instructions for implementing the `gmn:P70_18_documents_disputing_party` property in the GMN ontology and transformation system.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Overview](#overview)
3. [Phase 1: Ontology Definition](#phase-1-ontology-definition)
4. [Phase 2: Transformation Implementation](#phase-2-transformation-implementation)
5. [Phase 3: Testing](#phase-3-testing)
6. [Phase 4: Documentation](#phase-4-documentation)
7. [Troubleshooting](#troubleshooting)
8. [Validation](#validation)

---

## Prerequisites

### Required Knowledge
- RDF and Turtle syntax
- CIDOC-CRM fundamentals
- Python programming
- JSON-LD format
- Arbitration agreement concepts

### Required Tools
- Text editor or IDE
- RDF validator (e.g., Apache Jena riot)
- Python 3.6+
- JSON validator
- Git (for version control)

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script

### Dependencies
- Python `json` module (standard library)
- Python `uuid` module (standard library)

---

## Overview

### What You're Implementing

The `gmn:P70_18_documents_disputing_party` property is a shortcut that transforms to:

```
E31_3_Arbitration_Agreement
  → cidoc:P70_documents
    → cidoc:E7_Activity
      → cidoc:P14_carried_out_by
        → cidoc:E39_Actor
```

### Implementation Steps Summary

1. Add property definition to ontology (TTL)
2. Implement transformation function (Python)
3. Integrate into transformation pipeline
4. Test with sample data
5. Update documentation

**Estimated Time**: 30-45 minutes

---

## Phase 1: Ontology Definition

### Step 1.1: Open Ontology File

Open `gmn_ontology.ttl` in your text editor.

### Step 1.2: Locate Property Section

Find the section with property definitions. Look for other P70 properties, such as:
- `gmn:P70_5_documents_buyers_procurator`
- `gmn:P70_17_documents_currency`
- `gmn:P70_19_documents_arbitrator`

### Step 1.3: Add Property Definition

Insert the following TTL code in the appropriate location:

```turtle
# Property: P70.18 documents disputing party
gmn:P70_18_documents_disputing_party
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.18 documents disputing party"@en ;
    rdfs:comment "Simplified property for associating an arbitration agreement with a party involved in the dispute. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor. The E7_Activity should be typed as an arbitration agreement (AAT 300417271). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Disputing parties are the active principals who have agreed to submit their dispute to arbitration and are carrying out the arbitration agreement alongside the arbitrator(s)."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-28"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

### Step 1.4: Verify Syntax

Save the file and validate the TTL syntax:

```bash
riot --validate gmn_ontology.ttl
```

If there are errors, check:
- All semicolons and periods are correct
- IRIs are properly formatted
- Date literals have correct type annotations
- Comments are properly quoted

### Step 1.5: Commit Changes

```bash
git add gmn_ontology.ttl
git commit -m "Add P70.18 documents disputing party property"
```

---

## Phase 2: Transformation Implementation

### Step 2.1: Open Transformation Script

Open `gmn_to_cidoc_transform.py` in your text editor.

### Step 2.2: Locate Function Definitions

Find the section with transformation functions. Look for related functions:
- `transform_p70_19_documents_arbitrator()`
- `transform_p70_20_documents_dispute_subject()`

### Step 2.3: Add Transformation Function

Insert the following function (typically after other P70 transformations):

```python
def transform_p70_18_documents_disputing_party(data):
    """
    Transform gmn:P70_18_documents_disputing_party to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    """
    if 'gmn:P70_18_documents_disputing_party' not in data:
        return data
    
    parties = data['gmn:P70_18_documents_disputing_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create or locate activity node
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity'
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    # Initialize P14 array if needed
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    # Add each party
    for party_obj in parties:
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
    
    # Remove shortcut property
    del data['gmn:P70_18_documents_disputing_party']
    return data
```

### Step 2.4: Add to Transformation Pipeline

Find the main transformation function (usually named `transform_item()` or similar).

Locate the section that calls individual transformation functions and add:

```python
# Transform P70.18 - documents disputing party
item = transform_p70_18_documents_disputing_party(item)
```

**Placement**: Add this line alongside other arbitration property transformations (P70.19, P70.20).

### Step 2.5: Verify Syntax

Check Python syntax:

```bash
python3 -m py_compile gmn_to_cidoc_transform.py
```

### Step 2.6: Commit Changes

```bash
git add gmn_to_cidoc_transform.py
git commit -m "Add P70.18 transformation function"
```

---

## Phase 3: Testing

### Step 3.1: Create Test Data File

Create a file `test_p70_18.json`:

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "http://example.org/contracts/test_arbitration_001",
      "@type": "gmn:E31_3_Arbitration_Agreement",
      "gmn:P1_1_has_name": [
        {"@value": "Arbitration Agreement - Spinola v. Doria"}
      ],
      "gmn:P70_18_documents_disputing_party": [
        {"@id": "http://example.org/persons/antonio_spinola"},
        {"@id": "http://example.org/persons/giovanni_doria"}
      ]
    }
  ]
}
```

### Step 3.2: Run Transformation

```bash
python3 gmn_to_cidoc_transform.py test_p70_18.json > output_p70_18.json
```

### Step 3.3: Verify Output

Open `output_p70_18.json` and verify:

1. **Activity Created**: Check for `cidoc:P70_documents` array
2. **Activity URI**: Should be `{document_uri}/arbitration`
3. **Activity Type**: Should be `cidoc:E7_Activity`
4. **Parties Added**: Check `cidoc:P14_carried_out_by` array
5. **Party Types**: Each should have `@type: "cidoc:E39_Actor"`
6. **Property Removed**: `gmn:P70_18_documents_disputing_party` should be gone

Expected output structure:

```json
{
  "@id": "http://example.org/contracts/test_arbitration_001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/test_arbitration_001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P14_carried_out_by": [
      {
        "@id": "http://example.org/persons/antonio_spinola",
        "@type": "cidoc:E39_Actor"
      },
      {
        "@id": "http://example.org/persons/giovanni_doria",
        "@type": "cidoc:E39_Actor"
      }
    ]
  }]
}
```

### Step 3.4: Test Multiple Parties

Create test with 3+ parties:

```json
{
  "@id": "http://example.org/contracts/test_multi",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"},
    {"@id": "http://example.org/persons/party3"}
  ]
}
```

Verify all three parties appear in `P14_carried_out_by`.

### Step 3.5: Test Integration with Other Properties

Create comprehensive test with arbitrator and dispute subject:

```json
{
  "@id": "http://example.org/contracts/test_complete",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/property/building123"}
  ]
}
```

Verify:
- All three properties transform to the same activity
- Activity has both P14 (parties + arbitrator) and P16 (subject)
- All shortcut properties are removed

### Step 3.6: Test Edge Cases

**Empty Array:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": []
}
```
Should not create activity or error.

**Single Party:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"}
  ]
}
```
Should create activity with one party (though semantically unusual).

**Party as String:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    "http://example.org/persons/party1"
  ]
}
```
Should handle string URIs and wrap in proper structure.

### Step 3.7: Validate JSON-LD

Validate output with JSON-LD processor:

```bash
jsonld format output_p70_18.json
```

Or use online validator: https://json-ld.org/playground/

---

## Phase 4: Documentation

### Step 4.1: Update Main Documentation

Add to your main documentation file (e.g., `arbitration-documentation.md`):

```markdown
### gmn:P70_18_documents_disputing_party

**Label:** P70.18 documents disputing party

**Definition:** Simplified property for associating an arbitration agreement with 
the parties involved in the dispute.

**Domain:** gmn:E31_3_Arbitration_Agreement

**Range:** cidoc:E39_Actor

**CIDOC-CRM Path:**
E31_Document → P70_documents → E7_Activity → P14_carried_out_by → E39_Actor

**Usage:** Use to specify the individuals or groups who are parties to the dispute 
being arbitrated. Typically two or more parties. The transformation creates an 
E7_Activity representing the arbitration process and links parties via P14.

**Example:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/merchant1"},
    {"@id": "http://example.org/persons/merchant2"}
  ]
}
```
```

### Step 4.2: Create Usage Examples

Add practical examples to documentation showing:
- Simple two-party arbitration
- Multiple-party arbitration
- Integration with arbitrator property
- SPARQL queries for finding arbitrations by party

### Step 4.3: Document SPARQL Queries

Add query examples:

```sparql
# Find all arbitrations involving a specific person
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement ?date
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by <http://example.org/persons/target_person> .
  
  OPTIONAL {
    ?agreement gmn:P94i_2_has_enactment_date ?date .
  }
}
```

---

## Troubleshooting

### Issue: Property Not Transforming

**Symptoms:** Shortcut property remains in output

**Solutions:**
1. Check function is called in main pipeline
2. Verify property name matches exactly (case-sensitive)
3. Check function order (should be before final output)

### Issue: Activity Not Created

**Symptoms:** `cidoc:P70_documents` is empty or missing

**Solutions:**
1. Verify activity creation logic
2. Check URI generation
3. Ensure document has `@id` property

### Issue: Parties Not Added

**Symptoms:** `P14_carried_out_by` is empty

**Solutions:**
1. Check input data format (array of objects/URIs)
2. Verify loop over parties
3. Check type assignment logic

### Issue: Multiple Activities Created

**Symptoms:** Different P70 properties create separate activities

**Solutions:**
1. Ensure all functions use the same activity URI pattern
2. Check activity reuse logic
3. Verify functions check for existing `cidoc:P70_documents`

### Issue: Type Information Lost

**Symptoms:** Parties missing `@type: "cidoc:E39_Actor"`

**Solutions:**
1. Check type assignment in party loop
2. Verify copy() behavior for dict objects
3. Ensure string URIs get wrapped properly

---

## Validation

### Ontology Validation Checklist

- [ ] TTL syntax is valid
- [ ] Property has correct domain (E31_3_Arbitration_Agreement)
- [ ] Property has correct range (E39_Actor)
- [ ] Superproperty is set (P70_documents)
- [ ] Comments are complete and accurate
- [ ] Date metadata is present

### Transformation Validation Checklist

- [ ] Function exists and is properly named
- [ ] Function is called in main pipeline
- [ ] Activity creation logic is correct
- [ ] Party extraction handles dicts and strings
- [ ] Type assignment works correctly
- [ ] Shortcut property is removed
- [ ] Function doesn't error on missing property

### Output Validation Checklist

- [ ] Activity URI follows pattern: `{document_uri}/arbitration`
- [ ] Activity type is `cidoc:E7_Activity`
- [ ] Each party has `@type: "cidoc:E39_Actor"`
- [ ] All parties appear in P14_carried_out_by
- [ ] Shortcut property is removed from output
- [ ] Output validates as JSON-LD
- [ ] Output follows CIDOC-CRM structure

### Integration Validation Checklist

- [ ] Works with P70.19 (arbitrator)
- [ ] Works with P70.20 (dispute subject)
- [ ] All properties use same activity
- [ ] No duplicate activities created
- [ ] Transformation order doesn't matter

---

## Next Steps

After successful implementation:

1. **Deploy to Production**: Move changes to production environment
2. **Update Training Materials**: Add property to user guides
3. **Bulk Transform**: Transform existing arbitration agreements
4. **Monitor**: Watch for transformation errors in logs
5. **Optimize**: Review performance with large datasets

---

## Additional Resources

### Code References
- Main transformation script: `gmn_to_cidoc_transform.py`
- Ontology file: `gmn_ontology.ttl`
- Related functions: `transform_p70_19_documents_arbitrator()`, `transform_p70_20_documents_dispute_subject()`

### Documentation References
- Arbitration Agreement Documentation: `arbitration-ontology.md`
- CIDOC-CRM Specification: http://www.cidoc-crm.org/
- Getty AAT Arbitration: http://vocab.getty.edu/page/aat/300417271

### Testing Resources
- JSON-LD Playground: https://json-ld.org/playground/
- RDF Validator: Apache Jena riot
- Sample data files: `test_p70_18.json`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-28 | Initial implementation guide |

---

**Implementation complete?** Proceed to the **Testing** phase and then update your documentation!
