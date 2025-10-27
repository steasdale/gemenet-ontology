# Implementation Guide: P70.9 Documents Payment Provider for Buyer

This guide provides step-by-step instructions for implementing the `gmn:P70_9_documents_payment_provider_for_buyer` property in the GMN ontology and transformation pipeline.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Ontology Implementation](#ontology-implementation)
3. [Python Transformation Implementation](#python-transformation-implementation)
4. [Testing Procedures](#testing-procedures)
5. [Validation](#validation)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before implementing this property, ensure you have:

- Access to `gmn_ontology.ttl` file
- Access to `gmn_to_cidoc_transform.py` file
- Python 3.7 or higher installed
- Basic understanding of RDF/OWL and CIDOC-CRM
- Test data in JSON-LD format

---

## Ontology Implementation

### Step 1: Verify Property Definition

Open `gmn_ontology.ttl` and verify the property definition exists:

```turtle
# Property: P70.9 documents payment provider for buyer
gmn:P70_9_documents_payment_provider_for_buyer
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.9 documents payment provider for buyer"@en ;
    rdfs:comment "Simplified property for associating a sales contract with a third party who provides the payment (funds) on behalf of the buyer. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (payment provider), with P17_was_motivated_by linking to the buyer (E21_Person). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Unlike procurators (legal representatives), guarantors (security providers), or brokers (facilitators), payment providers are third parties who supply the actual funds for the purchase on behalf of the buyer, often in situations involving family members, business partners, or creditors."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P17_was_motivated_by .
```

**Verification Checklist**:
- ✓ Property URI: `gmn:P70_9_documents_payment_provider_for_buyer`
- ✓ Label: "P70.9 documents payment provider for buyer"@en
- ✓ Domain: `gmn:E31_2_Sales_Contract`
- ✓ Range: `cidoc:E21_Person`
- ✓ Super-property: `cidoc:P70_documents`
- ✓ Created date: 2025-10-17

### Step 2: Verify Namespace Declarations

Ensure the following namespaces are declared at the top of `gmn_ontology.ttl`:

```turtle
@prefix gmn: <https://w3id.org/geniza/ontology/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

---

## Python Transformation Implementation

### Step 1: Add Required Constants

Open `gmn_to_cidoc_transform.py` and verify these constants are defined near the top of the file (around lines 20-40):

```python
# Getty AAT URI constants
AAT_PAYER = "http://vocab.getty.edu/page/aat/300386048"
AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/page/aat/300055984"
```

If they don't exist, add them after the existing AAT constants.

### Step 2: Add Transformation Function

Locate the section with other P70 transformation functions (around line 690) and verify this function exists:

```python
def transform_p70_9_documents_payment_provider_for_buyer(data):
    """
    Transform gmn:P70_9_documents_payment_provider_for_buyer to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (with role)
    """
    if 'gmn:P70_9_documents_payment_provider_for_buyer' not in data:
        return data
    
    payers = data['gmn:P70_9_documents_payment_provider_for_buyer']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure E8_Acquisition exists
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P9_consists_of if not present
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Process each payment provider
    for payer_obj in payers:
        if isinstance(payer_obj, dict):
            payer_uri = payer_obj.get('@id', '')
            payer_data = payer_obj.copy()
        else:
            payer_uri = str(payer_obj)
            payer_data = {
                '@id': payer_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique activity URI
        activity_hash = str(hash(payer_uri + 'payment_provider'))[-8:]
        activity_uri = f"{subject_uri}/activity/payment_{activity_hash}"
        
        # Create E7_Activity with financial transaction type and payer role
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_FINANCIAL_TRANSACTION,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P14_carried_out_by': [payer_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_PAYER,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove shortcut property
    del data['gmn:P70_9_documents_payment_provider_for_buyer']
    return data
```

**Key Implementation Details**:

1. **Check for property existence**: Function returns early if property not present
2. **Ensure E8_Acquisition exists**: Creates acquisition node if needed
3. **Initialize P9_consists_of**: Ensures the list exists before adding activities
4. **Handle both URI strings and objects**: Supports flexible input formats
5. **Generate unique URIs**: Uses hash of payer URI to create unique activity URIs
6. **Add activity type**: Uses AAT financial transaction concept
7. **Add role designation**: Uses AAT payer concept for P14.1_in_the_role_of
8. **Clean up**: Removes the shortcut property after transformation

### Step 3: Register Function in transform_item()

Find the `transform_item()` function (around line 2400) and add this line in the appropriate location among other P70 transformations:

```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)
    item = transform_p70_7_documents_buyers_guarantor(item)
    item = transform_p70_8_documents_broker(item)
    item = transform_p70_9_documents_payment_provider_for_buyer(item)  # ADD THIS LINE
    item = transform_p70_10_documents_payment_recipient_for_seller(item)
    # ... continue with other transformations ...
```

---

## Testing Procedures

### Test Case 1: Single Payment Provider

Create a test file `test_payment_provider.json`:

```json
{
  "@context": {
    "gmn": "https://w3id.org/geniza/ontology/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "https://example.org/contract/123",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_9_documents_payment_provider_for_buyer": [
    {
      "@id": "https://example.org/person/456",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Expected Output**:

```json
{
  "@context": {
    "gmn": "https://w3id.org/geniza/ontology/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "https://example.org/contract/123",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://example.org/contract/123/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P9_consists_of": [
        {
          "@id": "https://example.org/contract/123/activity/payment_12345678",
          "@type": "cidoc:E7_Activity",
          "cidoc:P2_has_type": {
            "@id": "http://vocab.getty.edu/page/aat/300055984",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P14_carried_out_by": [
            {
              "@id": "https://example.org/person/456",
              "@type": "cidoc:E21_Person"
            }
          ],
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/page/aat/300386048",
            "@type": "cidoc:E55_Type"
          }
        }
      ]
    }
  ]
}
```

### Test Case 2: Multiple Payment Providers

```json
{
  "@id": "https://example.org/contract/789",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_9_documents_payment_provider_for_buyer": [
    {"@id": "https://example.org/person/101"},
    {"@id": "https://example.org/person/102"}
  ]
}
```

**Expected Behavior**: Creates two separate E7_Activity nodes, each with its own payment provider.

### Running Tests

```bash
# Run transformation on test file
python3 gmn_to_cidoc_transform.py test_payment_provider.json output.json

# Verify output structure
python3 -m json.tool output.json
```

---

## Validation

### Validation Checklist

After transformation, verify:

1. **E8_Acquisition Created**:
   - ✓ `cidoc:P70_documents` contains E8_Acquisition
   - ✓ Acquisition has appropriate URI

2. **E7_Activity Created**:
   - ✓ `cidoc:P9_consists_of` contains E7_Activity
   - ✓ Activity has unique URI with hash

3. **Activity Type Set**:
   - ✓ `cidoc:P2_has_type` points to AAT financial transaction
   - ✓ Type is cidoc:E55_Type

4. **Payment Provider Linked**:
   - ✓ `cidoc:P14_carried_out_by` contains payment provider
   - ✓ Provider is cidoc:E21_Person

5. **Role Designated**:
   - ✓ `cidoc:P14.1_in_the_role_of` points to AAT payer
   - ✓ Role is cidoc:E55_Type

6. **Cleanup Complete**:
   - ✓ `gmn:P70_9_documents_payment_provider_for_buyer` removed

### SPARQL Validation Query

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <https://w3id.org/geniza/ontology/>

SELECT ?contract ?acquisition ?activity ?payer ?role
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition .
  ?acquisition a cidoc:E8_Acquisition ;
               cidoc:P9_consists_of ?activity .
  ?activity a cidoc:E7_Activity ;
            cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300055984> ;
            cidoc:P14_carried_out_by ?payer ;
            cidoc:P14.1_in_the_role_of ?role .
  FILTER(?role = <http://vocab.getty.edu/page/aat/300386048>)
}
```

---

## Troubleshooting

### Issue: Function not being called

**Symptom**: Property not transformed after running script

**Solution**:
1. Verify function is added to `transform_item()`
2. Check function is placed in correct order (after P70.8, before P70.10)
3. Ensure no typos in function name

### Issue: E8_Acquisition not created

**Symptom**: Error about missing acquisition node

**Solution**:
1. Verify the acquisition creation code is present
2. Check that `cidoc:P70_documents` is being initialized correctly
3. Ensure acquisition URI generation is working

### Issue: Multiple activities have same URI

**Symptom**: Activities overwriting each other

**Solution**:
1. Verify hash generation includes payment provider URI
2. Check that hash suffix is unique for each provider
3. Ensure the hash is being appended to activity URI

### Issue: AAT constants not found

**Symptom**: NameError for AAT_PAYER or AAT_FINANCIAL_TRANSACTION

**Solution**:
1. Add constants to top of script:
   ```python
   AAT_PAYER = "http://vocab.getty.edu/page/aat/300386048"
   AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/page/aat/300055984"
   ```

### Issue: Role not properly assigned

**Symptom**: P14.1_in_the_role_of missing or incorrect

**Solution**:
1. Verify P14.1 is being added to activity (not to P14_carried_out_by)
2. Check AAT_PAYER constant value is correct
3. Ensure role object has correct structure with @id and @type

---

## Performance Considerations

- **Memory**: Each payment provider creates one E7_Activity node
- **URI Generation**: Hash-based URIs ensure uniqueness without database lookup
- **Scalability**: Function handles multiple payment providers efficiently
- **Processing Time**: Linear with number of payment providers

---

## Best Practices

1. **Always validate input**: Check property exists before transforming
2. **Preserve existing data**: Use `.copy()` when modifying objects
3. **Generate unique URIs**: Use hash-based approach for consistency
4. **Clean up shortcuts**: Remove simplified property after transformation
5. **Document assumptions**: Comment complex logic for future maintainers
6. **Test edge cases**: Single provider, multiple providers, URI vs. object input

---

## Next Steps

After successful implementation:

1. Update documentation with examples
2. Add property to user guides
3. Create training materials for data entry staff
4. Update API documentation if applicable
5. Consider implementing validation rules in data entry interface

---

**Document Version**: 1.0  
**Last Updated**: October 2025
