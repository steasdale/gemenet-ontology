# GMN Ontology: P70.6 Documents Seller's Guarantor Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_6_documents_sellers_guarantor` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-sellers-guarantor-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-sellers-guarantor-documentation.md** - Complete semantic documentation
4. **documents-sellers-guarantor-ontology.ttl** - TTL snippets for the ontology file
5. **documents-sellers-guarantor-transform.py** - Python code for the transformation script
6. **documents-sellers-guarantor-doc-note.txt** - Examples and tables for documentation

---

## 🎯 Property Overview

**Property Name:** `gmn:P70_6_documents_sellers_guarantor`

**Label:** "P70.6 documents seller's guarantor"

**Purpose:** Associates a sales contract with the person who provides security (guarantee) for the seller's obligations in the transaction.

**Domain:** `gmn:E31_2_Sales_Contract`

**Range:** `cidoc:E21_Person`

---

## 🔄 Transformation Pattern

The property transforms from a simplified GMN structure to full CIDOC-CRM compliance:

### Simplified GMN Structure (Input)
```turtle
:contract a gmn:E31_2_Sales_Contract ;
    gmn:P70_6_documents_sellers_guarantor :guarantor_person .
```

### Full CIDOC-CRM Structure (Output)
```turtle
:contract cidoc:P70_documents :acquisition .

:acquisition a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from :seller_person ;
    cidoc:P9_consists_of :guarantor_activity .

:guarantor_activity a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by :guarantor_person ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300379835> ; # guarantor role
    cidoc:P17_was_motivated_by :seller_person .
```

---

## 📋 Quick-Start Checklist

### Phase 1: Ontology Update
- [ ] Open `gmn_ontology.ttl`
- [ ] Add the property definition from `documents-sellers-guarantor-ontology.ttl`
- [ ] Verify syntax with a TTL validator
- [ ] Commit changes with message: "Add P70.6 documents seller's guarantor property"

### Phase 2: Transformation Script Update
- [ ] Open `gmn_to_cidoc_transform.py`
- [ ] Add the AAT_GUARANTOR constant (if not already present)
- [ ] Add the `transform_guarantor_property()` helper function (if not already present)
- [ ] Add the `transform_p70_6_documents_sellers_guarantor()` function
- [ ] Add the function call to the main `transform_item()` pipeline
- [ ] Run unit tests

### Phase 3: Documentation Update
- [ ] Open your main documentation file
- [ ] Add the property description from `documents-sellers-guarantor-doc-note.txt`
- [ ] Include examples and transformation patterns
- [ ] Update any property tables or indexes

### Phase 4: Testing
- [ ] Create test data with seller's guarantor relationships
- [ ] Run transformation script
- [ ] Validate CIDOC-CRM output structure
- [ ] Verify E7_Activity nodes are correctly created
- [ ] Confirm P17_was_motivated_by links guarantor to seller

---

## 🔑 Key Concepts

### What is a Guarantor?
A guarantor is a person who provides security for a transaction by promising to fulfill the obligations of another party (the principal) if they default. In historical contracts:
- Guarantors reduce risk for the other party
- They provide financial or personal security
- Their involvement is formally documented in the contract
- They may be liable if the principal fails to perform

### Seller's Guarantor vs. Other Roles
- **Seller's Guarantor:** Guarantees the seller's obligations (this property)
- **Buyer's Guarantor:** Guarantees the buyer's obligations (P70.7)
- **Seller's Procurator:** Legal representative acting for the seller (P70.4)
- **Broker:** Neutral facilitator of the transaction (P70.8)

### The E7_Activity Pattern
The transformation creates an E7_Activity node to explicitly model:
1. The guarantor's participation (P14_carried_out_by)
2. Their specific role as guarantor (P14.1_in_the_role_of → AAT:300379835)
3. Their motivation/principal (P17_was_motivated_by → seller)

This pattern allows CIDOC-CRM to represent complex relationships while maintaining semantic precision.

---

## 📊 Implementation Summary

### Files to Modify
1. `gmn_ontology.ttl` - Add property definition
2. `gmn_to_cidoc_transform.py` - Add transformation function
3. Main documentation file - Add property documentation

### Dependencies
- The helper function `transform_guarantor_property()` (shared with P70.7)
- AAT concept: 300379835 (guarantor)
- Existing acquisition structure with P23_transferred_title_from (seller)

### Estimated Time
- Ontology update: 5 minutes
- Script update: 10 minutes (if helper function exists), 20 minutes (if creating from scratch)
- Documentation update: 15 minutes
- Testing: 15 minutes
- **Total: ~45-60 minutes**

---

## 🔗 Related Properties

This property is part of a family of sales contract role properties:

| Property | Domain | Range | Role |
|----------|--------|-------|------|
| P70.1 | Sales Contract | Person | Seller |
| P70.2 | Sales Contract | Person | Buyer |
| P70.4 | Sales Contract | Person | Seller's Procurator |
| P70.5 | Sales Contract | Person | Buyer's Procurator |
| **P70.6** | **Sales Contract** | **Person** | **Seller's Guarantor** |
| P70.7 | Sales Contract | Person | Buyer's Guarantor |
| P70.8 | Sales Contract | Person | Broker |

---

## 📚 Additional Resources

- **Implementation Guide:** See `documents-sellers-guarantor-implementation-guide.md` for detailed step-by-step instructions
- **Full Documentation:** See `documents-sellers-guarantor-documentation.md` for complete semantic specifications
- **CIDOC-CRM:** http://www.cidoc-crm.org/
- **Getty AAT:** http://vocab.getty.edu/aat/

---

## ❓ Support

For questions or issues:
1. Review the implementation guide for detailed instructions
2. Check the documentation file for semantic specifications
3. Consult existing guarantor implementations (P70.7 for buyer's guarantor)
4. Review the arbitration ontology documentation for similar role patterns

---

## 📝 Version Information

- **Property Created:** 2025-10-17
- **Documentation Package Created:** 2025-10-27
- **GMN Ontology Version:** 1.0
- **CIDOC-CRM Version:** 7.1.1

---

## ✅ Implementation Status

Track your implementation progress:

- [ ] Ontology definition added
- [ ] Transformation function implemented
- [ ] Unit tests created and passing
- [ ] Documentation updated
- [ ] Integration tested with real data
- [ ] Peer review completed
- [ ] Production deployment approved
