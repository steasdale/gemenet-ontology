# E31.2 Sales Contract Implementation Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Implementation Steps](#implementation-steps)
4. [Testing Procedures](#testing-procedures)
5. [Troubleshooting](#troubleshooting)

## Overview

This guide provides step-by-step instructions for implementing E31_2_Sales_Contract in the Genoese Merchant Networks ontology. The sales contract class models documents recording the transfer of property between parties through purchase.

**Status**: All code is already implemented in the ontology and transformation script. This guide documents the existing implementation.

## Prerequisites

### Required Files
- `gmn_ontology.ttl` (main ontology file)
- `gmn_to_cidoc_transform.py` (transformation script)

### Required Knowledge
- Basic understanding of CIDOC-CRM concepts
- Familiarity with RDF/Turtle syntax
- Python 3.6+ for transformation testing
- Understanding of sales transaction structure

### Software Requirements
- RDF validator (e.g., Raptor, rapper)
- Python 3.6 or higher
- JSON processing capabilities
- Omeka-S 3.0+ (for data entry)

## Implementation Steps

### Step 1: Verify Class Definition

The E31_2_Sales_Contract class is already defined in `gmn_ontology.ttl`. Verify its presence:

```bash
grep -A 8 "Class: E31.2 Sales Contract" gmn_ontology.ttl
```

**Expected output**:
```turtle
# Class: E31.2 Sales Contract
gmn:E31_2_Sales_Contract
    a owl:Class ;
    rdfs:subClassOf gmn:E31_1_Contract ;
    rdfs:label "E31.2 Sales Contract"@en ;
    rdfs:comment "Specialized class that describes sales contract documents..." ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso gmn:E31_1_Contract, cidoc:E8_Acquisition, cidoc:P70_documents .
```

✓ **No action needed** - class already exists

### Step 2: Verify Properties (P70.1 through P70.17)

Check that all 17 sales contract properties are defined:

```bash
grep "gmn:P70_[1-9]_documents\|gmn:P70_1[0-7]_documents" gmn_ontology.ttl | grep "a owl"
```

The following properties should be present:

#### Core Transaction Properties
- **P70.1**: documents_seller
- **P70.2**: documents_buyer  
- **P70.3**: documents_transfer_of

#### Legal Representatives
- **P70.4**: documents_sellers_procurator
- **P70.5**: documents_buyers_procurator
- **P70.6**: documents_sellers_guarantor
- **P70.7**: documents_buyers_guarantor

#### Transaction Facilitators
- **P70.8**: documents_broker
- **P70.9**: documents_payment_provider_for_buyer
- **P70.10**: documents_payment_recipient_for_seller
- **P70.12**: documents_payment_through_organization

#### References and Context
- **P70.11**: documents_referenced_person
- **P70.13**: documents_referenced_place
- **P70.14**: documents_referenced_object
- **P70.15**: documents_witness

#### Monetary Information
- **P70.16**: documents_sale_price_amount
- **P70.17**: documents_sale_price_currency

✓ **No action needed** - all properties already exist

### Step 3: Verify Transformation Functions

Check that transformation functions exist in `gmn_to_cidoc_transform.py`:

```bash
grep "def transform_p70_[1-9]\|def transform_p70_1[0-7]" gmn_to_cidoc_transform.py
```

**Expected functions** (17 total):
- `transform_p70_1_documents_seller`
- `transform_p70_2_documents_buyer`
- `transform_p70_3_documents_transfer_of`
- `transform_p70_4_documents_sellers_procurator`
- `transform_p70_5_documents_buyers_procurator`
- `transform_p70_6_documents_sellers_guarantor`
- `transform_p70_7_documents_buyers_guarantor`
- `transform_p70_8_documents_broker`
- `transform_p70_9_documents_payment_provider_for_buyer`
- `transform_p70_10_documents_payment_recipient_for_seller`
- `transform_p70_11_documents_referenced_person`
- `transform_p70_12_documents_payment_through_organization`
- `transform_p70_13_documents_referenced_place`
- `transform_p70_14_documents_referenced_object`
- `transform_p70_15_documents_witness`
- `transform_p70_16_documents_sale_price_amount`
- `transform_p70_17_documents_sale_price_currency`

✓ **No action needed** - all functions already exist

### Step 4: Verify Transform Item Function

Check that sales contract properties are called in the main `transform_item()` function:

```bash
grep -A 200 "def transform_item" gmn_to_cidoc_transform.py | grep "transform_p70_[1-9]\|transform_p70_1[0-7]"
```

The function should call transformations in this order:
1. Core properties (P70.1-3)
2. Legal representatives (P70.4-7)
3. Transaction facilitators (P70.8-10, 12)
4. References (P70.11, 13-15)
5. Price (P70.16-17)

✓ **No action needed** - transform order already correct

### Step 5: Configure Omeka-S Resource Templates

Create a resource template for Sales Contracts in Omeka-S:

1. **Navigate** to Omeka-S Admin → Resource Templates
2. **Create** new template named "Sales Contract"
3. **Set base resource** to `gmn:E31_2_Sales_Contract`
4. **Add properties** in this recommended order:

```
BASIC INFORMATION:
- dcterms:title (document title/identifier)
- dcterms:date (date of contract)
- dcterms:description (summary of transaction)

CORE TRANSACTION:
- gmn:P70_1_documents_seller
- gmn:P70_2_documents_buyer
- gmn:P70_3_documents_transfer_of

PRICE INFORMATION:
- gmn:P70_16_documents_sale_price_amount
- gmn:P70_17_documents_sale_price_currency

LEGAL REPRESENTATIVES (optional):
- gmn:P70_4_documents_sellers_procurator
- gmn:P70_5_documents_buyers_procurator
- gmn:P70_6_documents_sellers_guarantor
- gmn:P70_7_documents_buyers_guarantor

FACILITATORS (optional):
- gmn:P70_8_documents_broker
- gmn:P70_9_documents_payment_provider_for_buyer
- gmn:P70_10_documents_payment_recipient_for_seller
- gmn:P70_12_documents_payment_through_organization

REFERENCES (optional):
- gmn:P70_11_documents_referenced_person
- gmn:P70_13_documents_referenced_place
- gmn:P70_14_documents_referenced_object
- gmn:P70_15_documents_witness
```

5. **Save** the template

✓ **Action required** - configure Omeka-S

### Step 6: Test Data Entry

Create a test sales contract in Omeka-S:

1. **Create new item** using Sales Contract template
2. **Add basic information**:
   - Title: "Sale of palazzo on Via Garibaldi"
   - Date: "1450-05-15"
3. **Add core data**:
   - Seller: Link to person resource
   - Buyer: Link to person resource
   - Transfer of: Link to building resource
4. **Add price**:
   - Amount: 500
   - Currency: Link to "Genoese lira" resource
5. **Save** the item

✓ **Action required** - test in Omeka-S

### Step 7: Export and Transform Test Data

Export the test item and run transformation:

```bash
# Export from Omeka-S as JSON-LD
# Save as test_sales_contract.json

# Run transformation
python3 gmn_to_cidoc_transform.py test_sales_contract.json > test_sales_output.json

# Verify output contains E8_Acquisition
grep "E8_Acquisition" test_sales_output.json
```

**Expected output structure**:
```json
{
  "@id": "http://example.com/items/123",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "http://example.com/items/123/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P23_transferred_title_from": [...],
    "cidoc:P22_transferred_title_to": [...],
    "cidoc:P24_transferred_title_of": [...],
    "cidoc:P177_assigned_property_of_type": {
      "@type": "cidoc:E97_Monetary_Amount",
      "cidoc:P180_has_currency_amount": "500",
      "cidoc:P180_has_currency": {...}
    }
  }]
}
```

✓ **Action required** - test transformation

## Testing Procedures

### Test 1: Simple Sales Contract

**Purpose**: Verify basic seller→buyer→property transformation

**Input**:
```turtle
<sale001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <giovanni> ;
    gmn:P70_2_documents_buyer <marco> ;
    gmn:P70_3_documents_transfer_of <palazzo001> .
```

**Expected Output**:
```turtle
<sale001> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <sale001/acquisition> .

<sale001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <giovanni> ;
    cidoc:P22_transferred_title_to <marco> ;
    cidoc:P24_transferred_title_of <palazzo001> .
```

**Validation**:
- ✓ E8_Acquisition created
- ✓ Seller mapped to P23_transferred_title_from
- ✓ Buyer mapped to P22_transferred_title_to
- ✓ Property mapped to P24_transferred_title_of

### Test 2: Sales Contract with Price

**Purpose**: Verify price transformation

**Input**:
```turtle
<sale002> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <anna> ;
    gmn:P70_2_documents_buyer <paolo> ;
    gmn:P70_3_documents_transfer_of <ship001> ;
    gmn:P70_16_documents_sale_price_amount "1000"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <genoese_lira> .
```

**Expected Output**:
```turtle
<sale002/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <anna> ;
    cidoc:P22_transferred_title_to <paolo> ;
    cidoc:P24_transferred_title_of <ship001> ;
    cidoc:P177_assigned_property_of_type <sale002/acquisition/monetary_amount> .

<sale002/acquisition/monetary_amount> a cidoc:E97_Monetary_Amount ;
    cidoc:P180_has_currency_amount "1000" ;
    cidoc:P180_has_currency <genoese_lira> .
```

**Validation**:
- ✓ E97_Monetary_Amount created
- ✓ Amount mapped to P180_has_currency_amount
- ✓ Currency mapped to P180_has_currency
- ✓ Monetary amount linked via P177

### Test 3: Sales Contract with Procurator

**Purpose**: Verify legal representative transformation

**Input**:
```turtle
<sale003> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <seller_pietro> ;
    gmn:P70_2_documents_buyer <buyer_luca> ;
    gmn:P70_4_documents_sellers_procurator <procurator_antonio> ;
    gmn:P70_3_documents_transfer_of <warehouse001> .
```

**Expected Output**:
```turtle
<sale003/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <seller_pietro> ;
    cidoc:P22_transferred_title_to <buyer_luca> ;
    cidoc:P24_transferred_title_of <warehouse001> ;
    cidoc:P9_consists_of <sale003/activity/procurator_XXXXXXXX> .

<sale003/activity/procurator_XXXXXXXX> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <procurator_antonio> ;
    cidoc:P14.1_in_the_role_of <AAT:300025972> ;
    cidoc:P17_was_motivated_by <seller_pietro> .
```

**Validation**:
- ✓ E7_Activity created for procurator
- ✓ Procurator linked via P14_carried_out_by
- ✓ Role typed with AAT agent concept
- ✓ Seller linked via P17_was_motivated_by

### Test 4: Complex Sales Contract

**Purpose**: Verify all property types together

**Input**: Sales contract with:
- Seller and buyer
- Procurators for both
- Guarantors for both
- Broker
- Payment provider and recipient
- Witnesses
- Referenced persons and places
- Price information

**Validation**:
- ✓ Single E8_Acquisition created
- ✓ All actors properly mapped
- ✓ E7_Activity sub-events created appropriately
- ✓ References use P67_refers_to
- ✓ No orphaned nodes

### Test 5: Multiple Values

**Purpose**: Verify handling of multiple actors

**Input**:
```turtle
<sale005> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <seller1>, <seller2> ;
    gmn:P70_2_documents_buyer <buyer1> ;
    gmn:P70_15_documents_witness <witness1>, <witness2>, <witness3> .
```

**Expected Output**:
- Multiple sellers in P23_transferred_title_from array
- Multiple witnesses each with own E7_Activity

**Validation**:
- ✓ Arrays handle multiple values
- ✓ Each witness gets separate activity
- ✓ No data loss

## Troubleshooting

### Issue 1: Transformation Produces No Output

**Symptoms**:
- Script runs but produces empty output
- No E8_Acquisition created

**Possible Causes**:
1. Input JSON-LD not properly formatted
2. Missing @id or @type in input
3. Property names don't match exactly

**Solutions**:
```bash
# Validate input JSON
python3 -m json.tool test_input.json

# Check for required fields
grep '@type.*E31_2_Sales_Contract' test_input.json

# Verify property names
grep 'gmn:P70_' test_input.json
```

### Issue 2: Missing E7_Activity Nodes

**Symptoms**:
- Procurators, guarantors, or witnesses not transformed
- Missing P9_consists_of relationships

**Possible Causes**:
1. Seller/buyer not present in acquisition
2. Function not called in transform_item()

**Solutions**:
```bash
# Verify seller/buyer present first
grep "P23_transferred_title_from\|P22_transferred_title_to" test_output.json

# Check function call order
grep "transform_p70_4\|transform_p70_5" gmn_to_cidoc_transform.py
```

### Issue 3: Price Not Appearing

**Symptoms**:
- No E97_Monetary_Amount created
- Missing P177_assigned_property_of_type

**Possible Causes**:
1. Amount and currency not both present
2. Wrong data type for amount

**Solutions**:
```bash
# Verify both properties present
grep "P70_16\|P70_17" test_input.json

# Check amount is numeric
grep 'P70_16.*value' test_input.json
```

### Issue 4: Referenced Items Not Linked

**Symptoms**:
- P67_refers_to not appearing
- Referenced persons/places/objects missing

**Possible Causes**:
1. Using wrong properties (P70.11, 13, 14)
2. Items not typed correctly

**Solutions**:
```bash
# Verify reference properties
grep "P70_11\|P70_13\|P70_14" test_input.json

# Check P67_refers_to in output
grep "P67_refers_to" test_output.json
```

### Issue 5: Duplicate Acquisition Nodes

**Symptoms**:
- Multiple E8_Acquisition instances
- Broken relationships

**Possible Causes**:
1. Transformation functions called multiple times
2. Acquisition not reused properly

**Solutions**:
- Review transform_item() function
- Ensure single acquisition per document
- Check for idempotency

## Validation Checklist

Before deploying to production:

### Ontology Validation
- [ ] TTL validates with RDF validator
- [ ] All properties have correct domains
- [ ] All properties have correct ranges
- [ ] Comments are clear and accurate
- [ ] Creation dates are present

### Transformation Validation  
- [ ] All 17 functions present
- [ ] Functions called in correct order
- [ ] Test files transform correctly
- [ ] No errors in Python code
- [ ] Output validates against CIDOC-CRM

### Data Entry Validation
- [ ] Omeka-S template configured
- [ ] All properties accessible
- [ ] Test items created successfully
- [ ] Export produces valid JSON-LD
- [ ] Transformation works end-to-end

### Documentation Validation
- [ ] All examples work correctly
- [ ] Code snippets are accurate
- [ ] No broken references
- [ ] Version information current

## Next Steps

After successful implementation:

1. **Train staff** on sales contract data entry
2. **Create documentation** for end users
3. **Establish workflows** for quality control
4. **Monitor** initial data entry
5. **Gather feedback** and refine process
6. **Scale up** to production volume

## Support

For issues not covered in this guide:
- Review `sales-documentation.md` for semantic details
- Examine `sales-transform.py` for code examples
- Check `sales-doc-note.txt` for additional examples
- Contact ontology maintainer

---

**Guide Version**: 1.0  
**Last Updated**: 2025-10-26  
**Status**: Complete
