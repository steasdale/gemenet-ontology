# Implementation Guide: P70.10 Documents Payment Recipient for Seller

This guide provides step-by-step instructions for implementing the `gmn:P70_10_documents_payment_recipient_for_seller` property in your GMN ontology project.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Add Ontology Definitions](#step-1-add-ontology-definitions)
4. [Step 2: Add Transformation Function](#step-2-add-transformation-function)
5. [Step 3: Register Transformation](#step-3-register-transformation)
6. [Step 4: Add Supporting Property](#step-4-add-supporting-property)
7. [Step 5: Test Implementation](#step-5-test-implementation)
8. [Step 6: Validate Output](#step-6-validate-output)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The `gmn:P70_10_documents_payment_recipient_for_seller` property enables you to document third parties who receive payment on behalf of sellers in sales contracts. This is distinct from procurators (legal representatives), guarantors (security providers), or brokers (transaction facilitators).

**Implementation Time**: Approximately 30-45 minutes

---

## Prerequisites

Before beginning implementation, ensure you have:

- [x] Access to `gmn_ontology.ttl` file
- [x] Access to `gmn_to_cidoc_transform.py` file
- [x] Understanding of your ontology's namespace structure
- [x] Python environment for testing transformations
- [x] Sample data with payment recipient information

---

## Step 1: Add Ontology Definitions

### 1.1 Locate the Sales Contract Properties Section

Open `gmn_ontology.ttl` and find the section containing other P70 properties (around lines 800-1200, depending on your file structure).

### 1.2 Add the P70.10 Property Definition

Insert the following TTL after the P70.9 property definition:

```turtle
# Property: P70.10 documents payment recipient for seller
gmn:P70_10_documents_payment_recipient_for_seller
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.10 documents payment recipient for seller"@en ;
    rdfs:comment "Simplified property for associating a sales contract with a third party who receives the payment (funds) on behalf of the seller. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (payment recipient), with P17_was_motivated_by linking to the seller (E21_Person). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Unlike procurators (legal representatives), guarantors (security providers), or brokers (facilitators), payment recipients are third parties who receive the actual funds from the purchase on behalf of the seller, often in situations involving family members, business partners, or creditors to whom the seller owes money."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P17_was_motivated_by .
```

### 1.3 Verify Property Structure

Ensure your addition includes:
- Property URI (`gmn:P70_10_documents_payment_recipient_for_seller`)
- Type declarations (`owl:ObjectProperty`, `rdf:Property`)
- English label
- Comprehensive comment explaining usage and distinction from other roles
- Correct domain (`gmn:E31_2_Sales_Contract`)
- Correct range (`cidoc:E21_Person`)
- SubProperty relationship (`cidoc:P70_documents`)
- Creation date
- See also references

---

## Step 2: Add Transformation Function

### 2.1 Locate the Transformation Functions Section

Open `gmn_to_cidoc_transform.py` and find the section with other P70 transformation functions (search for `def transform_p70_`).

### 2.2 Insert the P70.10 Transformation Function

Add the following function after the `transform_p70_9_documents_payment_provider_for_buyer` function:

```python
def transform_p70_10_documents_payment_recipient_for_seller(data):
    """
    Transform gmn:P70_10_documents_payment_recipient_for_seller to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (with role)
    
    Creates an E7_Activity node for each payment recipient, representing the payment receipt
    activity. The activity is typed as a financial transaction and links the recipient
    as the actor carrying out the activity in the role of "payee".
    
    Args:
        data: Dictionary containing the GMN item data
        
    Returns:
        Transformed data dictionary with P70.10 converted to full CIDOC-CRM structure
        
    Example Input:
        {
            '@id': 'contract:123',
            'gmn:P70_10_documents_payment_recipient_for_seller': [
                {'@id': 'person:Antonio', '@type': 'cidoc:E21_Person'}
            ]
        }
        
    Example Output:
        {
            '@id': 'contract:123',
            'cidoc:P70_documents': [{
                '@id': 'contract:123/acquisition',
                '@type': 'cidoc:E8_Acquisition',
                'cidoc:P9_consists_of': [{
                    '@id': 'contract:123/activity/payment_abc123',
                    '@type': 'cidoc:E7_Activity',
                    'cidoc:P2_has_type': {
                        '@id': 'http://vocab.getty.edu/aat/300417629',
                        '@type': 'cidoc:E55_Type'
                    },
                    'cidoc:P14_carried_out_by': [
                        {'@id': 'person:Antonio', '@type': 'cidoc:E21_Person'}
                    ],
                    'cidoc:P14.1_in_the_role_of': {
                        '@id': 'http://vocab.getty.edu/aat/300025555',
                        '@type': 'cidoc:E55_Type'
                    }
                }]
            }]
        }
    """
    if 'gmn:P70_10_documents_payment_recipient_for_seller' not in data:
        return data
    
    payees = data['gmn:P70_10_documents_payment_recipient_for_seller']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure acquisition exists
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
    
    # Create an activity for each payment recipient
    for payee_obj in payees:
        # Handle both URI strings and object dictionaries
        if isinstance(payee_obj, dict):
            payee_uri = payee_obj.get('@id', '')
            payee_data = payee_obj.copy()
        else:
            payee_uri = str(payee_obj)
            payee_data = {
                '@id': payee_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique activity URI using hash
        activity_hash = str(hash(payee_uri + 'payment_recipient'))[-8:]
        activity_uri = f"{subject_uri}/activity/payment_{activity_hash}"
        
        # Create the payment receipt activity
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_FINANCIAL_TRANSACTION,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P14_carried_out_by': [payee_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_PAYEE,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add activity to acquisition
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove the simplified property
    del data['gmn:P70_10_documents_payment_recipient_for_seller']
    return data
```

### 2.3 Verify AAT Constants

Ensure these AAT constants are defined at the top of your transformation file:

```python
# AAT Concept URIs
AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/aat/300417629"
AAT_PAYEE = "http://vocab.getty.edu/aat/300025555"
```

If they're not already present, add them to the constants section.

---

## Step 3: Register Transformation

### 3.1 Locate the Main Transform Function

Find the `transform_item()` function (usually around line 1500-1800).

### 3.2 Add Function Call

In the "Sales contract properties (P70.1-P70.17)" section, add the function call after P70.9:

```python
# Sales contract properties (P70.1-P70.17)
item = transform_p70_1_documents_seller(item)
item = transform_p70_2_documents_buyer(item)
item = transform_p70_3_documents_transfer_of(item)
item = transform_p70_4_documents_sellers_procurator(item)
item = transform_p70_5_documents_buyers_procurator(item)
item = transform_p70_6_documents_sellers_guarantor(item)
item = transform_p70_7_documents_buyers_guarantor(item)
item = transform_p70_8_documents_broker(item)
item = transform_p70_9_documents_payment_provider_for_buyer(item)
item = transform_p70_10_documents_payment_recipient_for_seller(item)  # ADD THIS LINE
item = transform_p70_11_documents_referenced_person(item)
# ... rest of the function
```

### 3.3 Verify Placement

Ensure the function is called:
- After P70.9 transformation
- Before P70.11 transformation
- Within the sales contract properties section

---

## Step 4: Add Supporting Property

### 4.1 Locate the Direct Relationship Properties Section

In `gmn_ontology.ttl`, find the section with direct relationship properties like `has_payment_provided_by` and `is_represented_by`.

### 4.2 Add the has_payment_received_by Property

Insert this definition:

```turtle
# Property: has payment received by
gmn:has_payment_received_by
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "has payment received by"@en ;
    rdfs:comment "Direct relationship linking a person (seller) to another person (payment recipient) who receives the funds from their sale. This property provides a simple semantic link between sellers and those who collect payment on their behalf. When used in the context of sales contracts, this relationship is documented within the contract and elaborated through E7_Activity nodes in the acquisition event structure. This property enables Omeka-S annotations to directly connect sellers with their payment recipients."@en ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date .
```

### 4.3 Purpose of Supporting Property

This property enables direct linking in Omeka-S annotations and provides a simplified view of the seller-recipient relationship.

---

## Step 5: Test Implementation

### 5.1 Create Test Data

Create a test file `test_p70_10.json`:

```json
{
    "@context": {
        "gmn": "http://example.org/gmn/",
        "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
    },
    "@id": "contract:test_123",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_1_documents_seller": [
        {
            "@id": "person:Giovanni_Rossi",
            "@type": "cidoc:E21_Person"
        }
    ],
    "gmn:P70_2_documents_buyer": [
        {
            "@id": "person:Marco_Bianchi",
            "@type": "cidoc:E21_Person"
        }
    ],
    "gmn:P70_10_documents_payment_recipient_for_seller": [
        {
            "@id": "person:Antonio_Rossi",
            "@type": "cidoc:E21_Person"
        }
    ]
}
```

### 5.2 Run Transformation

```python
import json
from gmn_to_cidoc_transform import transform_item

# Load test data
with open('test_p70_10.json', 'r') as f:
    test_data = json.load(f)

# Transform
result = transform_item(test_data)

# Print result
print(json.dumps(result, indent=2))
```

### 5.3 Verify Output Structure

Expected output structure:

```json
{
    "@id": "contract:test_123",
    "@type": "gmn:E31_2_Sales_Contract",
    "cidoc:P70_documents": [
        {
            "@id": "contract:test_123/acquisition",
            "@type": "cidoc:E8_Acquisition",
            "cidoc:P23_transferred_title_from": [...],
            "cidoc:P22_transferred_title_to": [...],
            "cidoc:P9_consists_of": [
                {
                    "@id": "contract:test_123/activity/payment_abc123",
                    "@type": "cidoc:E7_Activity",
                    "cidoc:P2_has_type": {
                        "@id": "http://vocab.getty.edu/aat/300417629",
                        "@type": "cidoc:E55_Type"
                    },
                    "cidoc:P14_carried_out_by": [
                        {
                            "@id": "person:Antonio_Rossi",
                            "@type": "cidoc:E21_Person"
                        }
                    ],
                    "cidoc:P14.1_in_the_role_of": {
                        "@id": "http://vocab.getty.edu/aat/300025555",
                        "@type": "cidoc:E55_Type"
                    }
                }
            ]
        }
    ]
}
```

### 5.4 Test Multiple Recipients

Test with multiple payment recipients:

```json
{
    "@id": "contract:test_124",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_10_documents_payment_recipient_for_seller": [
        {"@id": "person:Antonio", "@type": "cidoc:E21_Person"},
        {"@id": "person:Luigi", "@type": "cidoc:E21_Person"}
    ]
}
```

Verify that each recipient gets their own E7_Activity node.

---

## Step 6: Validate Output

### 6.1 Structural Validation

Verify the transformed data contains:

- [ ] `cidoc:P70_documents` property linking to E8_Acquisition
- [ ] E8_Acquisition contains `cidoc:P9_consists_of` array
- [ ] Each payment recipient has an E7_Activity node
- [ ] Each activity has `@type`: "cidoc:E7_Activity"
- [ ] Each activity has `cidoc:P2_has_type` pointing to AAT financial transaction
- [ ] Each activity has `cidoc:P14_carried_out_by` linking to the recipient
- [ ] Each activity has `cidoc:P14.1_in_the_role_of` pointing to AAT payee
- [ ] Original `gmn:P70_10_documents_payment_recipient_for_seller` is removed

### 6.2 Semantic Validation

Verify the transformation preserves semantic meaning:

- [ ] Payment recipient is correctly modeled as actor of payment receipt activity
- [ ] Activity is properly nested within E8_Acquisition
- [ ] Role specification (payee) is present
- [ ] Activity type (financial transaction) is correct
- [ ] Person entities maintain their identity and type

### 6.3 Integration Validation

Test with full sales contract data:

```python
# Test with complete contract including seller, buyer, and payment recipient
test_full_contract = {
    "@id": "contract:complete",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_1_documents_seller": [{"@id": "person:Seller"}],
    "gmn:P70_2_documents_buyer": [{"@id": "person:Buyer"}],
    "gmn:P70_10_documents_payment_recipient_for_seller": [{"@id": "person:Recipient"}]
}

result = transform_item(test_full_contract)

# Verify all components are present and properly linked
assert 'cidoc:P70_documents' in result
acquisition = result['cidoc:P70_documents'][0]
assert 'cidoc:P23_transferred_title_from' in acquisition
assert 'cidoc:P22_transferred_title_to' in acquisition
assert 'cidoc:P9_consists_of' in acquisition
assert len(acquisition['cidoc:P9_consists_of']) > 0
```

---

## Step 7: Update Documentation

### 7.1 Add Property to Documentation

Add the following section to your main documentation file (after P70.9):

```markdown
### P70.10 documents payment recipient for seller

**Property URI**: `gmn:P70_10_documents_payment_recipient_for_seller`

Associates a sales contract with a third party who receives the payment (funds) on behalf of the seller.

**Domain**: `gmn:E31_2_Sales_Contract`  
**Range**: `cidoc:E21_Person`

**Purpose**: Documents third parties who actually receive funds from purchases on behalf of sellers, distinct from procurators (legal representatives), guarantors (security providers), or brokers (transaction facilitators).

**Common scenarios**:
- Family member receiving payment for elderly relative
- Business partner collecting payment for joint venture
- Creditor receiving direct payment to settle debt
- Authorized agent collecting funds on seller's behalf

**CIDOC-CRM Transformation**:
```
E31_Document 
  → P70_documents 
    → E8_Acquisition 
      → P9_consists_of 
        → E7_Activity [Financial Transaction]
          → P14_carried_out_by → E21_Person (payment recipient)
          → P14.1_in_the_role_of → E55_Type (AAT: payee)
```

**Example**:
```turtle
contract:456 gmn:P70_10_documents_payment_recipient_for_seller person:Antonio .
person:Giovanni gmn:has_payment_received_by person:Antonio .
```

Transforms to:

```turtle
contract:456 cidoc:P70_documents acquisition:456 .
acquisition:456 cidoc:P9_consists_of activity:payment_xyz .
activity:payment_xyz a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by person:Antonio ;
    cidoc:P14.1_in_the_role_of <AAT:payee> .
```
```

---

## Troubleshooting

### Issue: Property Not Found in Transformation

**Symptom**: `gmn:P70_10_documents_payment_recipient_for_seller` remains in output

**Solutions**:
1. Verify function is added to `gmn_to_cidoc_transform.py`
2. Check function is called in `transform_item()`
3. Ensure function name matches exactly
4. Verify property key matches exactly (check underscores)

### Issue: Activity Not Created

**Symptom**: No E7_Activity appears in output

**Solutions**:
1. Verify `cidoc:P9_consists_of` is initialized
2. Check loop over payees executes
3. Verify activity dictionary is appended to list
4. Check for exceptions in transformation function

### Issue: AAT Concepts Not Resolving

**Symptom**: AAT URIs are incorrect or missing

**Solutions**:
1. Verify AAT constants are defined:
   ```python
   AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/aat/300417629"
   AAT_PAYEE = "http://vocab.getty.edu/aat/300025555"
   ```
2. Check constant names match usage in function
3. Verify AAT URIs are correct (check Getty AAT)

### Issue: Multiple Recipients Not Handled

**Symptom**: Only first recipient is transformed

**Solutions**:
1. Verify payees is treated as list
2. Check loop iterates over all items
3. Ensure activity appending is inside loop
4. Verify hash generation creates unique URIs

### Issue: Acquisition Already Exists

**Symptom**: Multiple acquisition nodes created

**Solutions**:
1. Check if `cidoc:P70_documents` already exists before creating
2. Verify you're getting the first acquisition: `acquisition = data['cidoc:P70_documents'][0]`
3. Ensure other P70 transformations also use same acquisition

---

## Next Steps

After successful implementation:

1. **Document Examples**: Add real-world examples to documentation
2. **Integration Testing**: Test with production data pipeline
3. **User Training**: Update data entry guidelines
4. **Quality Assurance**: Review transformed contracts in repository
5. **Monitor Usage**: Track how often property is used

---

## Additional Resources

### Related Properties
- `gmn:P70_1_documents_seller` - The seller whose payment is being received
- `gmn:P70_9_documents_payment_provider_for_buyer` - Parallel property for buyer
- `gmn:has_payment_received_by` - Direct seller-to-recipient link

### CIDOC-CRM Documentation
- [P70 documents](http://www.cidoc-crm.org/Property/P70-documents/version-7.1.3)
- [P9 consists of](http://www.cidoc-crm.org/Property/P9-consists-of/version-7.1.3)
- [P14 carried out by](http://www.cidoc-crm.org/Property/P14-carried-out-by/version-7.1.3)
- [E7 Activity](http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.3)

### Getty AAT
- [Financial Transactions](http://vocab.getty.edu/aat/300417629)
- [Payee](http://vocab.getty.edu/aat/300025555)

---

**Implementation Complete!** You have successfully implemented the payment recipient for seller property.
