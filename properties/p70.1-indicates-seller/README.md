# GMN Ontology: P70.1 Indicates Seller Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_1_indicates_seller` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-seller-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-seller-documentation.md** - Complete semantic documentation
4. **documents-seller-ontology.ttl** - Ready-to-copy TTL snippets for ontology
5. **documents-seller-transform.py** - Ready-to-copy Python transformation code
6. **documents-seller-doc-note.txt** - Examples and tables for main documentation

---

## 🎯 Quick Overview

**Property**: `gmn:P70_1_indicates_seller`

**Purpose**: Simplified property for associating a sales contract document with the person who acts as the seller in the sale event.

**Represents**: The full CIDOC-CRM path using E13 Attribute Assignment:
```
E70_Document (typed as "sales contract")
  > P70_documents 
  > E7_Activity (typed as "sale")
  > P140i_was_attributed_by 
  > E13_Attribute_Assignment
    > P141_assigned > E21_Person (seller)
    > P177_assigned_property_of_type > E55_Type ("P14 carried out by")
    > P14.1_in_the_role_of > E55_Type ("seller")
```

**Domain**: `cidoc:E70_Document` (with P2 type "sales contract")

**Range**: `cidoc:E21_Person`

---

## ✅ Quick-Start Checklist

### For Ontology Implementation:
- [ ] Copy TTL snippet from `documents-seller-ontology.ttl` 
- [ ] Add to main `gmn_ontology.ttl` file
- [ ] Verify property declaration and metadata
- [ ] Check rdfs:subPropertyOf relationship to cidoc:P70_documents
- [ ] Validate domain and range restrictions

### For Transformation Script:
- [ ] Copy function from `documents-seller-transform.py`
- [ ] Add to `gmn_to_cidoc_transform.py` file
- [ ] Add function call to `transform_item()` function
- [ ] Ensure AAT constants are defined for role types
- [ ] Test with sample data

### For Documentation:
- [ ] Review semantic documentation in `documents-seller-documentation.md`
- [ ] Copy relevant examples from `documents-seller-doc-note.txt`
- [ ] Add to main documentation file
- [ ] Verify E13 attribution pattern is clear
- [ ] Check cross-references to related properties

---

## 📋 Implementation Summary

### What This Property Does

The `gmn:P70_1_indicates_seller` property creates a simplified way to link sales contract documents to sellers. Instead of manually creating the full CIDOC-CRM structure with E7 activities and E13 attribute assignments, users can use this shorthand property during data entry.

### Architectural Approach

**E13 Attribute Assignment Pattern**: This implementation uses CIDOC-CRM's E13_Attribute_Assignment class to formally assign the "carried out by" attribute to the sale event, specifying the seller's role. This pattern provides:
- Explicit attribution of the seller role
- Formal typing of the relationship (P14 carried out by)
- Clear role specification ("seller")
- Provenance for the attribution

### Transformation Process

**Input (Simplified GMN)**:
```json
{
  "@id": "contract_001",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type",
    "rdfs:label": "sales contract"
  },
  "gmn:P70_1_indicates_seller": [
    {
      "@id": "person_001",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Output (Full CIDOC-CRM)**:
```json
{
  "@id": "contract_001",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type",
    "rdfs:label": "sales contract"
  },
  "cidoc:P70_documents": [
    {
      "@id": "contract_001/sale",
      "@type": "cidoc:E7_Activity",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300054751",
        "@type": "cidoc:E55_Type",
        "rdfs:label": "sale"
      },
      "cidoc:P140i_was_attributed_by": [
        {
          "@id": "contract_001/attribution/seller_person_001",
          "@type": "cidoc:E13_Attribute_Assignment",
          "cidoc:P141_assigned": {
            "@id": "person_001",
            "@type": "cidoc:E21_Person"
          },
          "cidoc:P177_assigned_property_of_type": {
            "@id": "http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "P14 carried out by"
          },
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/aat/300410369",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "seller"
          }
        }
      ]
    }
  ]
}
```

### Key Features

1. **E70 Document Base**: Uses standard E70_Document with P2 type, not a custom subclass
2. **E7 Activity**: Models the sale as an E7_Activity (typed as "sale"), not E8_Acquisition
3. **E13 Attribution**: Uses E13_Attribute_Assignment for formal role attribution
4. **Explicit Role Typing**: Links to AAT terms for "seller" role and "P14 carried out by" property
5. **Multiple Sellers**: Supports multiple sellers via multiple E13 attributions
6. **Provenance**: E13 pattern provides clear provenance for the seller attribution

### Related Properties

- **gmn:P70_2_indicates_buyer** - Complementary property for buyers (similar E13 pattern)
- **gmn:P70_3_indicates_transfer_of** - Links to object being transferred
- **gmn:P70_4_indicates_sellers_procurator** - Legal representative for seller
- **gmn:P70_6_indicates_sellers_guarantor** - Guarantor for seller

---

## 🔗 Integration Notes

### AAT Terms Required

The transformation uses Getty AAT terms:
- **Sale Event**: `http://vocab.getty.edu/aat/300054751` (sale, event)
- **Seller Role**: `http://vocab.getty.edu/aat/300410369` (sellers, people)
- **P14 Property**: `http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by`

### Sequence in Transform Pipeline

The `transform_p70_1_indicates_seller()` function should be called:
1. After document creation properties (P94i series)
2. As part of the sales contract properties group (P70.1-P70.17)
3. Before transformation functions that depend on the E7_Activity structure

### Dependencies

- Requires `uuid` module for generating URIs
- Requires AAT constants defined (AAT_SALE_EVENT, AAT_SELLER_ROLE)
- Works with existing E7_Activity if present, creates new one if not
- Complements P70_2 (buyer) and P70_3 (transfer of) properties

---

## 📚 Additional Resources

For complete implementation details, see:
- **Implementation Guide**: `documents-seller-implementation-guide.md`
- **Full Documentation**: `documents-seller-documentation.md`

For code snippets, see:
- **Ontology Code**: `documents-seller-ontology.ttl`
- **Python Code**: `documents-seller-transform.py`

For documentation examples, see:
- **Doc Additions**: `documents-seller-doc-note.txt`

---

## 🏷️ Metadata

- **Property ID**: gmn:P70_1_indicates_seller
- **Created**: 2025-10-17
- **Version**: 2.0 (E13 Attribution Pattern)
- **Status**: Production-ready
- **Compatibility**: CIDOC-CRM compliant

---

## ⚠️ Important Notes

1. **E13 Pattern**: Uses attribute assignment for formal role specification
2. **Document Type**: Sales contracts use E70_Document with P2 type, not E31.2 subclass
3. **Activity Type**: Uses E7_Activity (type "sale"), not E8_Acquisition
4. **AAT Integration**: Requires AAT terms for sale, seller role, and P14 property
5. **Seller vs. Procurator**: Use P70.1 for actual sellers, P70.4 for their legal representatives
6. **Person Only**: Range is restricted to E21_Person (not groups/organizations)
7. **Deletion**: The simplified property is removed after transformation
8. **URI Generation**: Function generates stable URIs using document ID as base
9. **Multiple Sellers**: Property supports arrays, each creates separate E13 attribution

---

*For questions or issues, refer to the complete implementation guide and documentation files included in this package.*
