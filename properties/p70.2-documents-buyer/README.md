# GMN Ontology: P70.2 Documents Buyer Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_2_documents_buyer` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-buyer-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-buyer-documentation.md** - Complete semantic documentation
4. **documents-buyer-ontology.ttl** - TTL snippets for the ontology file
5. **documents-buyer-transform.py** - Python code for the transformation script
6. **documents-buyer-doc-note.txt** - Examples and tables for documentation

---

## 🎯 Quick Start Checklist

### Phase 1: Ontology Definition (5 minutes)
- [ ] Copy TTL from `documents-buyer-ontology.ttl`
- [ ] Paste into `gmn_ontology.ttl` in the P70 properties section
- [ ] Verify correct formatting and indentation
- [ ] Validate TTL syntax

### Phase 2: Transformation Implementation (10 minutes)
- [ ] Copy Python code from `documents-buyer-transform.py`
- [ ] Paste into `gmn_to_cidoc_transform.py`
- [ ] Add function call to `transform_item()` pipeline
- [ ] Import necessary modules (uuid4)

### Phase 3: Documentation Update (10 minutes)
- [ ] Review examples in `documents-buyer-doc-note.txt`
- [ ] Add property description to main documentation
- [ ] Include transformation examples
- [ ] Add to property reference table

### Phase 4: Testing & Validation (15 minutes)
- [ ] Create test data with P70_2 property
- [ ] Run transformation script
- [ ] Verify E8_Acquisition node creation
- [ ] Validate P22_transferred_title_to structure
- [ ] Check buyer E21_Person representation
- [ ] Test with multiple buyers

---

## 📋 Implementation Summary

### Property Overview
**GMN Property:** `gmn:P70_2_documents_buyer`  
**Label:** "P70.2 documents buyer"  
**Purpose:** Simplified property for associating a sales contract with the person named as the buyer

### CIDOC-CRM Path
```
E31_Document (Sales Contract)
  └─ P70_documents
      └─ E8_Acquisition
          └─ P22_transferred_title_to
              └─ E21_Person (Buyer)
```

### Key Features
- **Simplification**: Direct relationship between contract and buyer
- **Domain**: `gmn:E31_2_Sales_Contract`
- **Range**: `cidoc:E21_Person`
- **Parent Property**: `cidoc:P70_documents`
- **Multiple Values**: Supports multiple buyers in a single transaction
- **Automatic URI Generation**: Creates acquisition nodes when needed

### Transformation Behavior
1. Checks for existing E8_Acquisition node
2. Creates acquisition node if not present
3. Adds buyer to P22_transferred_title_to array
4. Handles both URI references and inline person objects
5. Preserves existing buyer data structure
6. Removes original GMN property after transformation

### Integration Points
- **Works with**: P70_1 (seller), P70_3 (transfer of), P70_5 (buyer's procurator)
- **Creates**: E8_Acquisition nodes shared by all P70 properties
- **Complements**: Other sales contract participant properties

---

## 🔍 Use Cases

### 1. Single Buyer Transaction
Most common case: one buyer purchasing property from one seller.

### 2. Multiple Buyers (Joint Purchase)
Multiple individuals purchasing property together (e.g., siblings, business partners).

### 3. Buyer with Representative
Used alongside P70_5 (buyer's procurator) when legal representative acts for buyer.

### 4. Complex Transactions
Combined with guarantors (P70_7) and payment providers (P70_9) for full transaction context.

---

## 📚 Related Properties

- **gmn:P70_1_documents_seller** - Identifies the seller (P23_transferred_title_from)
- **gmn:P70_3_documents_transfer_of** - Identifies property transferred (P24_transferred_title_of)
- **gmn:P70_5_documents_buyers_procurator** - Legal representative for buyer
- **gmn:P70_7_documents_buyers_guarantor** - Security provider for buyer
- **gmn:P70_9_documents_payment_provider_for_buyer** - Third party providing payment

---

## ⚠️ Important Notes

1. **E8_Acquisition Node Sharing**: All P70 properties that document the acquisition (seller, buyer, transfer of, price) share the same E8_Acquisition node
2. **Multiple Buyers**: The property accepts arrays and properly handles multiple buyers
3. **Type Safety**: Automatically assigns `cidoc:E21_Person` type if not specified
4. **URI Handling**: Supports both string URIs and full object structures
5. **Data Preservation**: Copies and preserves all existing buyer properties during transformation

---

## 🔗 External References

- CIDOC-CRM P22: http://www.cidoc-crm.org/Property/P22-transferred-title-to/version-7.1.3
- CIDOC-CRM P70: http://www.cidoc-crm.org/Property/P70-documents/version-7.1.3
- CIDOC-CRM E8: http://www.cidoc-crm.org/Entity/E8-Acquisition/version-7.1.3
- CIDOC-CRM E21: http://www.cidoc-crm.org/Entity/E21-Person/version-7.1.3

---

## 📖 Documentation Files

For complete implementation details, consult:
- **Implementation Guide**: Step-by-step instructions with code examples
- **Ontology Documentation**: Complete semantic specification
- **Transform Code**: Ready-to-use Python implementation
- **Doc Notes**: Examples and reference materials

---

**Version:** 1.0  
**Created:** 2025-10-27  
**Property Creation Date:** 2025-10-17
