# Ontology Documentation: P70.7 Documents Buyer's Guarantor
## Complete Semantic Documentation

This document provides comprehensive semantic documentation for the `gmn:P70_7_documents_buyers_guarantor` property, including its definition, CIDOC-CRM mapping, transformation logic, and usage patterns.

---

## Table of Contents

1. [Property Definition](#property-definition)
2. [CIDOC-CRM Semantic Path](#cidoc-crm-semantic-path)
3. [Property Characteristics](#property-characteristics)
4. [Transformation Logic](#transformation-logic)
5. [Semantic Patterns](#semantic-patterns)
6. [Usage Guidelines](#usage-guidelines)
7. [Examples](#examples)
8. [Comparison with Related Properties](#comparison-with-related-properties)
9. [Edge Cases and Special Considerations](#edge-cases-and-special-considerations)

---

## Property Definition

### Basic Information

**Property URI**: `gmn:P70_7_documents_buyers_guarantor`

**Property Label**: "P70.7 documents buyer's guarantor"@en

**Property Type**: 
- `owl:ObjectProperty`
- `rdf:Property`

**Parent Property**: `cidoc:P70_documents`

**Domain**: `gmn:E31_2_Sales_Contract`

**Range**: `cidoc:E21_Person`

**Creation Date**: 2025-10-17

### Formal Definition

The property `gmn:P70_7_documents_buyers_guarantor` is a simplified shortcut property that associates a sales contract document with one or more persons who serve as guarantors for the buyer in the transaction. A guarantor is an individual who provides security or assurance for the transaction by promising to fulfill the buyer's obligations should the buyer default on their commitments.

This property represents a complex CIDOC-CRM path involving multiple intermediate nodes and relationships. It is designed as a convenience for data entry and must be transformed into the full CIDOC-CRM compliant structure before final export or reasoning.

### Scope and Purpose

**In Scope**:
- Persons explicitly named as guarantors for the buyer
- Individuals providing financial security for buyer's obligations
- Multiple guarantors for a single buyer
- Historical and contemporary guarantee relationships

**Out of Scope**:
- Seller's guarantors (use `gmn:P70_6_documents_sellers_guarantor`)
- Legal representatives/procurators (use `gmn:P70_5_documents_buyers_procurator`)
- Payment providers (use `gmn:P70_9_documents_payment_provider_for_buyer`)
- Transaction facilitators/brokers (use `gmn:P70_8_documents_broker`)
- Witnesses (use `gmn:P70_15_documents_witness`)

---

## CIDOC-CRM Semantic Path

### Full Transformation Path

The shortcut property expands into the following CIDOC-CRM structure:

```
gmn:P70_7_documents_buyers_guarantor
  ↓
E31_Document
  → cidoc:P70_documents → E8_Acquisition
    → cidoc:P9_consists_of → E7_Activity [Guaranteeing Activity]
      ├─ cidoc:P14_carried_out_by → E21_Person [Guarantor]
      │   └─ cidoc:P14.1_in_the_role_of → E55_Type [AAT: Guarantor]
      └─ cidoc:P17_was_motivated_by → E21_Person [Buyer]
```

### Path Components

#### 1. Document to Acquisition
```turtle
ex:Contract_001
  a gmn:E31_2_Sales_Contract ;
  cidoc:P70_documents ex:Acquisition_001 .

ex:Acquisition_001
  a cidoc:E8_Acquisition .
```

**Semantics**: The sales contract documents an acquisition event (the transfer of ownership).

#### 2. Acquisition to Activity
```turtle
ex:Acquisition_001
  cidoc:P9_consists_of ex:GuaranteeActivity_001 .

ex:GuaranteeActivity_001
  a cidoc:E7_Activity .
```

**Semantics**: The acquisition consists of various component activities, including the guaranteeing activity.

#### 3. Activity to Guarantor
```turtle
ex:GuaranteeActivity_001
  cidoc:P14_carried_out_by ex:Person_Guarantor_001 ;
  cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300025614> .

ex:Person_Guarantor_001
  a cidoc:E21_Person .
```

**Semantics**: The guaranteeing activity is carried out by a person acting in the role of guarantor (AAT concept 300025614).

#### 4. Activity to Buyer
```turtle
ex:GuaranteeActivity_001
  cidoc:P17_was_motivated_by ex:Person_Buyer_001 .

ex:Person_Buyer_001
  a cidoc:E21_Person .
```

**Semantics**: The guaranteeing activity is motivated by (done on behalf of) the buyer.

### Why This Structure?

The use of E7_Activity as an intermediate node serves several important purposes:

1. **Role Specification**: Allows clear specification that the person acts as a guarantor via P14.1_in_the_role_of
2. **Relationship Clarity**: P17_was_motivated_by explicitly links the guarantor to the buyer they guarantee
3. **Semantic Precision**: Distinguishes guaranteeing from other forms of participation in the acquisition
4. **Multiple Guarantors**: Each guarantor gets their own activity node, preventing confusion
5. **CIDOC-CRM Compliance**: Follows established patterns for role-based participation

---

## Property Characteristics

### Cardinality

**In GMN Shortcut**: `0..n` (zero or more guarantors per contract)

**In CIDOC-CRM**: Each guarantor creates one E7_Activity node

**Practical Implications**:
- Contracts may have no guarantors (not all transactions required them)
- Contracts may have multiple guarantors (common for high-value transactions)
- Each guarantor is represented independently (enables tracking individual obligations)

### Inverse Property

No explicit inverse property is defined, but the semantic inverse would be:
- "is guarantor for buyer in" (E21_Person → E31_Document)

In CIDOC-CRM structure, traversal would be:
```
E21_Person 
  ← P14_carried_out_by ← E7_Activity 
  ← P9_consists_of ← E8_Acquisition 
  ← P70_documents ← E31_Document
```

### Property Chain

The property represents this chain:
```
P70_documents • P9_consists_of • P14_carried_out_by
```

With qualifications:
- E7_Activity must have `P14.1_in_the_role_of` pointing to AAT_GUARANTOR
- E7_Activity should have `P17_was_motivated_by` pointing to buyer

---

## Transformation Logic

### Algorithm Overview

The transformation follows these steps:

1. **Check for Property**: If `gmn:P70_7_documents_buyers_guarantor` not present, return unchanged
2. **Extract Guarantors**: Get list of guarantor objects/URIs
3. **Ensure Acquisition Node**: Create E8_Acquisition if not present
4. **Find Buyer**: Locate buyer URI from P22_transferred_title_to
5. **For Each Guarantor**:
   - Create unique E7_Activity node
   - Link guarantor via P14_carried_out_by
   - Assign guarantor role via P14.1_in_the_role_of
   - Link to buyer via P17_was_motivated_by (if buyer present)
6. **Remove Shortcut Property**: Delete gmn:P70_7_documents_buyers_guarantor

### Transformation Function

```python
def transform_p70_7_documents_buyers_guarantor(data):
    """Transform gmn:P70_7_documents_buyers_guarantor to full CIDOC-CRM structure."""
    return transform_guarantor_property(data, 'gmn:P70_7_documents_buyers_guarantor', 
                                       'cidoc:P22_transferred_title_to')
```

This function delegates to the generic `transform_guarantor_property` helper, which implements the full algorithm.

### Generic Helper Function

```python
def transform_guarantor_property(data, property_name, motivated_by_property):
    """
    Generic function to transform guarantor properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    
    Args:
        data: Item data dictionary
        property_name: The guarantor property to transform
        motivated_by_property: Property linking to the party being guaranteed
                              (P22 for buyer, P23 for seller)
    
    Returns:
        Transformed data dictionary
    """
    if property_name not in data:
        return data
    
    guarantors = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure E8_Acquisition exists
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Ensure P9_consists_of exists
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Find the party being guaranteed
    motivated_by_uri = None
    if motivated_by_property in acquisition:
        motivated_by_list = acquisition[motivated_by_property]
        if isinstance(motivated_by_list, list) and len(motivated_by_list) > 0:
            if isinstance(motivated_by_list[0], dict):
                motivated_by_uri = motivated_by_list[0].get('@id')
            else:
                motivated_by_uri = str(motivated_by_list[0])
    
    # Create E7_Activity for each guarantor
    for guarantor_obj in guarantors:
        if isinstance(guarantor_obj, dict):
            guarantor_uri = guarantor_obj.get('@id', '')
            guarantor_data = guarantor_obj.copy()
        else:
            guarantor_uri = str(guarantor_obj)
            guarantor_data = {
                '@id': guarantor_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique activity URI
        activity_hash = str(hash(guarantor_uri + property_name))[-8:]
        activity_uri = f"{subject_uri}/activity/guarantor_{activity_hash}"
        
        # Create activity node
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [guarantor_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_GUARANTOR,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add motivation link if party present
        if motivated_by_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': motivated_by_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove shortcut property
    del data[property_name]
    return data
```

### Key Design Decisions

1. **Generic Helper Function**: Both buyer's and seller's guarantor properties use the same transformation logic, differing only in the `motivated_by_property` parameter

2. **Unique Activity URIs**: Hash-based URI generation ensures unique IDs even with multiple guarantors

3. **Graceful Degradation**: If buyer not present, activity still created but without P17 link

4. **Type Coercion**: Handles both URI strings and full object representations of guarantors

5. **AAT Constant**: Uses Getty AAT concept 300025614 for guarantor role

---

## Semantic Patterns

### Pattern 1: Single Guarantor for Buyer

**Scenario**: Giovanni purchases property, Marco guarantees

**Input (GMN)**:
```json
{
  "@id": "ex:Contract_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [
    {"@id": "ex:Giovanni", "@type": "cidoc:E21_Person"}
  ],
  "gmn:P70_7_documents_buyers_guarantor": [
    {"@id": "ex:Marco", "@type": "cidoc:E21_Person"}
  ]
}
```

**Output (CIDOC-CRM)**:
```json
{
  "@id": "ex:Contract_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "ex:Contract_001/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P22_transferred_title_to": [
      {"@id": "ex:Giovanni", "@type": "cidoc:E21_Person"}
    ],
    "cidoc:P9_consists_of": [{
      "@id": "ex:Contract_001/activity/guarantor_XXXXXXXX",
      "@type": "cidoc:E7_Activity",
      "cidoc:P14_carried_out_by": [
        {"@id": "ex:Marco", "@type": "cidoc:E21_Person"}
      ],
      "cidoc:P14.1_in_the_role_of": {
        "@id": "http://vocab.getty.edu/page/aat/300025614",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P17_was_motivated_by": {
        "@id": "ex:Giovanni",
        "@type": "cidoc:E21_Person"
      }
    }]
  }]
}
```

### Pattern 2: Multiple Guarantors

**Scenario**: High-value transaction with multiple guarantors for buyer

**Input (GMN)**:
```json
{
  "@id": "ex:Contract_002",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [
    {"@id": "ex:Francesco"}
  ],
  "gmn:P70_7_documents_buyers_guarantor": [
    {"@id": "ex:Marco"},
    {"@id": "ex:Pietro"},
    {"@id": "ex:Antonio"}
  ]
}
```

**Output (CIDOC-CRM)**:
```json
{
  "cidoc:P70_documents": [{
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P9_consists_of": [
      {
        "@id": "...activity/guarantor_XXXXXXX1",
        "cidoc:P14_carried_out_by": [{"@id": "ex:Marco"}],
        "cidoc:P17_was_motivated_by": {"@id": "ex:Francesco"}
      },
      {
        "@id": "...activity/guarantor_XXXXXXX2",
        "cidoc:P14_carried_out_by": [{"@id": "ex:Pietro"}],
        "cidoc:P17_was_motivated_by": {"@id": "ex:Francesco"}
      },
      {
        "@id": "...activity/guarantor_XXXXXXX3",
        "cidoc:P14_carried_out_by": [{"@id": "ex:Antonio"}],
        "cidoc:P17_was_motivated_by": {"@id": "ex:Francesco"}
      }
    ]
  }]
}
```

### Pattern 3: Buyer and Seller Both Have Guarantors

**Scenario**: Complex transaction with guarantors for both parties

```json
{
  "@id": "ex:Contract_003",
  "gmn:P70_1_documents_seller": [{"@id": "ex:SellerA"}],
  "gmn:P70_2_documents_buyer": [{"@id": "ex:BuyerB"}],
  "gmn:P70_6_documents_sellers_guarantor": [{"@id": "ex:SellerGuarantor"}],
  "gmn:P70_7_documents_buyers_guarantor": [{"@id": "ex:BuyerGuarantor"}]
}
```

Result: Two separate E7_Activity nodes, one linking to seller, one to buyer.

### Pattern 4: Guarantor with Full Person Data

**Input (GMN)**:
```json
{
  "gmn:P70_7_documents_buyers_guarantor": [
    {
      "@id": "ex:Marco",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": [
        {
          "@type": "cidoc:E41_Appellation",
          "cidoc:P190_has_symbolic_content": "Marco di Giovanni Rossi"
        }
      ]
    }
  ]
}
```

**Output**: The full person data is preserved in P14_carried_out_by.

---

## Usage Guidelines

### When to Use This Property

✅ **Use P70.7** when:
- Person explicitly named as guarantor for buyer
- Person provides financial security for buyer's obligations
- Historical document identifies person as "guarantor," "security," "surety" for buyer
- Person promises to fulfill buyer's commitments if buyer defaults

❌ **Do NOT use P70.7** for:
- Legal representatives → use `gmn:P70_5_documents_buyers_procurator`
- Transaction facilitators → use `gmn:P70_8_documents_broker`
- Third-party payers → use `gmn:P70_9_documents_payment_provider_for_buyer`
- Witnesses → use `gmn:P70_15_documents_witness`
- Seller's guarantors → use `gmn:P70_6_documents_sellers_guarantor`

### Data Entry Best Practices

1. **Minimum Required Information**: Guarantor person URI
   ```json
   "gmn:P70_7_documents_buyers_guarantor": ["ex:PersonURI"]
   ```

2. **Recommended Information**: Full person object with identification
   ```json
   "gmn:P70_7_documents_buyers_guarantor": [
     {
       "@id": "ex:PersonURI",
       "@type": "cidoc:E21_Person",
       "cidoc:P1_is_identified_by": [...]
     }
   ]
   ```

3. **Multiple Guarantors**: List all in array
   ```json
   "gmn:P70_7_documents_buyers_guarantor": [
     {"@id": "ex:Guarantor1"},
     {"@id": "ex:Guarantor2"}
   ]
   ```

### Validation Rules

1. **Domain Constraint**: Only use on gmn:E31_2_Sales_Contract
2. **Range Constraint**: Values must be cidoc:E21_Person
3. **Cardinality**: Zero or more values accepted
4. **Uniqueness**: Same person should not appear multiple times as guarantor
5. **Consistency**: If guarantor appears, buyer should also be specified

---

## Examples

### Example 1: 15th Century Venetian Property Sale

**Historical Context**: Property purchase in Venice, 1467. Buyer's brother serves as guarantor.

**GMN Input**:
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/ontology#"
  },
  "@id": "http://example.org/contract/venice_1467_042",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P1_is_identified_by": [
    {
      "@type": "cidoc:E41_Appellation",
      "cidoc:P190_has_symbolic_content": "Venetian Property Sale Contract, 1467"
    }
  ],
  "gmn:P70_1_documents_seller": [
    {
      "@id": "http://example.org/person/lorenzo_contarini",
      "@type": "cidoc:E21_Person"
    }
  ],
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "http://example.org/person/giovanni_mocenigo",
      "@type": "cidoc:E21_Person"
    }
  ],
  "gmn:P70_7_documents_buyers_guarantor": [
    {
      "@id": "http://example.org/person/marco_mocenigo",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": [
        {
          "@type": "cidoc:E41_Appellation",
          "cidoc:P190_has_symbolic_content": "Marco Mocenigo, brother of Giovanni"
        }
      ]
    }
  ],
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "http://example.org/building/venice_cannaregio_house_42",
      "@type": "gmn:E22_1_Building"
    }
  ]
}
```

### Example 2: Commercial Transaction with Multiple Guarantors

**Historical Context**: Large commercial sale, 1502. Multiple family members serve as guarantors for buyer.

**GMN Input**:
```json
{
  "@id": "http://example.org/contract/florence_1502_128",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "http://example.org/person/francesco_medici"
    }
  ],
  "gmn:P70_7_documents_buyers_guarantor": [
    {
      "@id": "http://example.org/person/giovanni_medici",
      "cidoc:P1_is_identified_by": [
        {
          "cidoc:P190_has_symbolic_content": "Giovanni de' Medici, son of Francesco"
        }
      ]
    },
    {
      "@id": "http://example.org/person/lorenzo_medici",
      "cidoc:P1_is_identified_by": [
        {
          "cidoc:P190_has_symbolic_content": "Lorenzo de' Medici, nephew of Francesco"
        }
      ]
    },
    {
      "@id": "http://example.org/person/antonio_medici",
      "cidoc:P1_is_identified_by": [
        {
          "cidoc:P190_has_symbolic_content": "Antonio de' Medici, brother of Francesco"
        }
      ]
    }
  ]
}
```

---

## Comparison with Related Properties

### P70.5: Documents Buyer's Procurator

| Aspect | P70.7 Guarantor | P70.5 Procurator |
|--------|----------------|------------------|
| **Function** | Provides financial security | Acts as legal representative |
| **Authority** | Promise to pay if buyer defaults | Legal authority to act for buyer |
| **Timing** | Contingent (if needed) | Active during transaction |
| **Representation** | E7_Activity with P17 to buyer | E7_Activity with P17 to buyer |
| **Role AAT** | 300025614 (guarantor) | 300025972 (agent) |

### P70.6: Documents Seller's Guarantor

| Aspect | P70.7 Buyer's Guarantor | P70.6 Seller's Guarantor |
|--------|------------------------|--------------------------|
| **Party Guaranteed** | Buyer | Seller |
| **P17 Links To** | P22_transferred_title_to | P23_transferred_title_from |
| **Obligation** | Buyer's payment/performance | Seller's title/delivery |
| **Common In** | Buyer lacking funds/credit | Seller lacking clear title |

### P70.9: Documents Payment Provider for Buyer

| Aspect | P70.7 Guarantor | P70.9 Payment Provider |
|--------|----------------|------------------------|
| **Function** | Promise of contingent payment | Actual current payment |
| **Timing** | If buyer defaults | At time of transaction |
| **Financial Flow** | Conditional | Actual |
| **Role AAT** | 300025614 (guarantor) | 300386048 (payer) |

---

## Edge Cases and Special Considerations

### Edge Case 1: Guarantor Without Buyer

**Situation**: Contract specifies guarantor but buyer not yet determined or recorded.

**Handling**: 
- Transformation still creates E7_Activity
- P17_was_motivated_by omitted (graceful degradation)
- Valid CIDOC-CRM structure maintained

**Example**:
```json
// Input: Only guarantor, no buyer
{
  "gmn:P70_7_documents_buyers_guarantor": [{"@id": "ex:Guarantor"}]
}

// Output: Activity without P17
{
  "cidoc:P70_documents": [{
    "cidoc:P9_consists_of": [{
      "cidoc:P14_carried_out_by": [{"@id": "ex:Guarantor"}],
      "cidoc:P14.1_in_the_role_of": {...}
      // No P17_was_motivated_by
    }]
  }]
}
```

### Edge Case 2: Same Person as Buyer and Guarantor

**Situation**: Person listed as both buyer and guarantor (unusual but possible in complex arrangements).

**Handling**: 
- Valid in data model (though semantically unusual)
- Results in E7_Activity where P14 and P17 point to same person
- May warrant data quality check

### Edge Case 3: Guarantor Also Has Other Roles

**Situation**: Same person serves as both guarantor and witness, or guarantor and broker.

**Handling**:
- Each role gets separate representation
- Person appears in multiple P14_carried_out_by statements with different roles
- E7_Activity nodes keep roles distinct

**Example**:
```json
{
  "gmn:P70_7_documents_buyers_guarantor": [{"@id": "ex:Marco"}],
  "gmn:P70_15_documents_witness": [{"@id": "ex:Marco"}]
}
// Results in two E7_Activity nodes for Marco
```

### Edge Case 4: URI-Only vs. Full Object

**Situation**: Guarantor specified as bare URI string vs. full object.

**Handling**: Transformation normalizes both formats to full object with @id and @type.

### Edge Case 5: Multiple Contracts, Same Guarantor

**Situation**: Same person serves as guarantor in multiple contracts.

**Handling**:
- Each contract creates independent E7_Activity
- Person URI reused but activities unique
- Enables tracking of guarantor's participation across transactions

---

## Summary

The `gmn:P70_7_documents_buyers_guarantor` property provides a convenient shortcut for documenting buyer's guarantors in sales contracts while maintaining full CIDOC-CRM semantic precision through automatic transformation. The property:

- **Simplifies data entry** with intuitive shortcut syntax
- **Maintains semantic rigor** through proper CIDOC-CRM transformation
- **Supports complex scenarios** including multiple guarantors
- **Integrates seamlessly** with other P70 properties
- **Enables rich querying** via transformed E7_Activity structure
- **Preserves role semantics** using Getty AAT vocabulary

---

**Documentation Version**: 1.0  
**Last Updated**: 2025-10-27  
**Property**: gmn:P70_7_documents_buyers_guarantor  
**Namespace**: http://example.org/gmn/ontology#
