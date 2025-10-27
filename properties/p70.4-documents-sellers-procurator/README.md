# GMN Ontology: P70.4 Documents Seller's Procurator Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_4_documents_sellers_procurator` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-sellers-procurator-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-sellers-procurator-documentation.md** - Complete semantic documentation
4. **documents-sellers-procurator-ontology.ttl** - TTL snippets for ontology file
5. **documents-sellers-procurator-transform.py** - Python code for transformation script
6. **documents-sellers-procurator-doc-note.txt** - Documentation examples and tables

---

## 🎯 Quick Start

### Prerequisites
- GMN ontology file (`gmn_ontology.ttl`)
- Transformation script (`gmn_to_cidoc_transform.py`)
- Main documentation file

### Implementation Checklist

- [ ] **Step 1**: Add TTL definitions to `gmn_ontology.ttl`
  - Copy content from `documents-sellers-procurator-ontology.ttl`
  - Place after P70.3 documents transfer of property definition
  
- [ ] **Step 2**: Add transformation function to `gmn_to_cidoc_transform.py`
  - Copy content from `documents-sellers-procurator-transform.py`
  - Place in the Sales Contract transformations section (after P70.3)
  - Verify `transform_procurator_property()` helper function exists
  
- [ ] **Step 3**: Update main transformation caller
  - Ensure `transform_p70_4_documents_sellers_procurator(item)` is called in `transform_item()`
  - Should be placed after P70.3 transformation
  
- [ ] **Step 4**: Update documentation
  - Add content from `documents-sellers-procurator-doc-note.txt` to main documentation
  - Include usage examples and transformation patterns
  
- [ ] **Step 5**: Test implementation
  - Create test data with seller's procurator
  - Run transformation script
  - Verify correct CIDOC-CRM output structure

---

## 📋 Property Overview

**Property**: `gmn:P70_4_documents_sellers_procurator`  
**Label**: "P70.4 documents seller's procurator"  
**Domain**: `gmn:E31_2_Sales_Contract`  
**Range**: `cidoc:E21_Person`  
**Date Created**: 2025-10-17

### Purpose

This property simplifies data entry for sales contracts by directly linking a contract to the person who acted as the seller's procurator (legal representative). It represents a complex CIDOC-CRM path as a single, user-friendly property.

### Semantic Path

The property represents:
```
E31_Document → P70_documents → E8_Acquisition → P9_consists_of → E7_Activity
  → P14_carried_out_by → E21_Person (procurator)
  → P17_was_motivated_by → E21_Person (seller)
```

### Key Features

- **Simplified Input**: Single property for procurator relationships
- **Automatic Transformation**: Converts to full CIDOC-CRM structure
- **Role Specification**: Uses AAT term for "agent" role
- **Seller Linkage**: Connects procurator to the seller they represent via P17_was_motivated_by

---

## 🔄 Transformation Example

### Input (GMN Shortcut)
```json
{
  "@id": "contract/001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [{"@id": "person/seller001"}],
  "gmn:P70_4_documents_sellers_procurator": [{"@id": "person/procurator001"}]
}
```

### Output (CIDOC-CRM)
```json
{
  "@id": "contract/001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "contract/001/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P23_transferred_title_from": [{
      "@id": "person/seller001",
      "@type": "cidoc:E21_Person"
    }],
    "cidoc:P9_consists_of": [{
      "@id": "contract/001/activity/procurator_abc12345",
      "@type": "cidoc:E7_Activity",
      "cidoc:P14_carried_out_by": [{
        "@id": "person/procurator001",
        "@type": "cidoc:E21_Person"
      }],
      "cidoc:P14.1_in_the_role_of": {
        "@id": "http://vocab.getty.edu/page/aat/300025972",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P17_was_motivated_by": {
        "@id": "person/seller001",
        "@type": "cidoc:E21_Person"
      }
    }]
  }]
}
```

---

## 🔍 Related Properties

- **gmn:P70_1_documents_seller** - Direct seller identification
- **gmn:P70_5_documents_buyers_procurator** - Buyer's procurator (parallel structure)
- **gmn:P70_6_documents_sellers_guarantor** - Seller's guarantor (similar but different role)
- **gmn:P70_2_documents_buyer** - Direct buyer identification

---

## 📚 Implementation Details

### AAT Role Type
- **URI**: `http://vocab.getty.edu/page/aat/300025972`
- **Term**: "agent"
- **Definition**: Legal representatives acting on behalf of principals

### Dependency Management

This property transformation depends on:
1. The seller being defined via `gmn:P70_1_documents_seller` for proper P17 linkage
2. The generic `transform_procurator_property()` helper function
3. The acquisition structure created by prior transformations

### Multiple Procurators

The property supports multiple procurators for a single seller. Each procurator creates a separate E7_Activity node with its own unique URI.

---

## ⚠️ Important Notes

1. **Order of Operations**: The `transform_p70_1_documents_seller()` must be called before this transformation to ensure the seller URI is available for P17_was_motivated_by linkage.

2. **URI Generation**: Activity URIs are generated using a hash of the procurator URI and property name to ensure uniqueness and reproducibility.

3. **Role Qualification**: The procurator role is explicitly specified using the AAT "agent" concept, distinguishing procurators from other transaction participants.

4. **Missing Seller**: If no seller is defined in the acquisition, the transformation will still create the procurator activity but without the P17_was_motivated_by link.

---

## 🧪 Testing

After implementation, test with:
1. Single procurator for seller
2. Multiple procurators for same seller
3. Procurator without seller defined (edge case)
4. Combined with buyer's procurator (gmn:P70_5)

---

## 📖 Documentation

For complete semantic documentation and detailed examples, see:
- `documents-sellers-procurator-documentation.md`
- `documents-sellers-procurator-implementation-guide.md`

---

## 🤝 Support

For questions or issues with implementation:
1. Review the implementation guide
2. Check the ontology documentation
3. Examine the transformation code comments
4. Test with provided examples

---

**Version**: 1.0  
**Last Updated**: October 2025  
**Property Created**: 2025-10-17
