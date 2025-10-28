# GMN Ontology: P70.15 Documents Witness Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_15_documents_witness` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-witness-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-witness-documentation.md** - Complete semantic documentation
4. **documents-witness-ontology.ttl** - Ready-to-copy TTL snippets for the ontology
5. **documents-witness-transform.py** - Ready-to-copy Python transformation code
6. **documents-witness-doc-note.txt** - Examples and tables for documentation

---

## 🎯 Quick Start Checklist

### Implementation Steps

- [ ] **Step 1:** Add the TTL definition from `documents-witness-ontology.ttl` to your main `gmn_ontology.ttl` file
- [ ] **Step 2:** Add the Python transformation function from `documents-witness-transform.py` to your `gmn_to_cidoc_transform.py` script
- [ ] **Step 3:** Add the function call to the main transformation pipeline
- [ ] **Step 4:** Update documentation with content from `documents-witness-doc-note.txt`
- [ ] **Step 5:** Run tests to verify the transformation works correctly

### Testing Steps

- [ ] Test with single witness
- [ ] Test with multiple witnesses
- [ ] Test with complex witness data (names, appellations)
- [ ] Validate output RDF structure
- [ ] Verify role assignment (AAT 300028910)

---

## 📋 Property Summary

**Property URI:** `gmn:P70_15_documents_witness`

**Label:** P70.15 documents witness

**Domain:** `gmn:E31_2_Sales_Contract` (Sales Contract)

**Range:** `cidoc:E21_Person` (Person)

**Purpose:** Associates a sales contract with persons who served as witnesses to the acquisition, providing legal validation of the property transfer event.

**Key Distinction:** Unlike `gmn:P70_11_documents_referenced_person` (which captures persons merely mentioned in the text), witnesses actively participated in the acquisition event by observing and validating the transaction.

---

## 🔄 Transformation Pattern

### Shortcut (GMN):
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_15_documents_witness <witness_antonio>, <witness_paolo> .
```

### Full CIDOC-CRM Structure:
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <contract001/acquisition> .

<contract001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P9_consists_of <contract001/activity/witness_hash1>,
                         <contract001/activity/witness_hash2> .

<contract001/activity/witness_hash1> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <witness_antonio> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .

<contract001/activity/witness_hash2> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <witness_paolo> ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300028910> .

<witness_antonio> a cidoc:E21_Person .
<witness_paolo> a cidoc:E21_Person .
```

---

## 🔑 Key Features

1. **Active Participation:** Witnesses were present at and formally observed the transaction
2. **Legal Validation:** Provided legal validation of the property transfer event
3. **Role Assignment:** Each witness is assigned the AAT role "witness" (300028910)
4. **Activity Modeling:** Creates separate E7_Activity nodes for each witness's participation
5. **Acquisition Context:** Links witnesses to the E8_Acquisition event, not directly to the document

---

## 📚 Related Properties

- **gmn:P70_11_documents_referenced_person** - For persons mentioned but not participating
- **gmn:P70_1_documents_seller** - For the seller in the acquisition
- **gmn:P70_2_documents_buyer** - For the buyer in the acquisition
- **gmn:P70_8_documents_broker** - For transaction facilitators

---

## 🆘 Support

For detailed implementation guidance, see:
- **Implementation Guide:** `documents-witness-implementation-guide.md`
- **Semantic Documentation:** `documents-witness-documentation.md`

For questions about the GMN ontology or CIDOC-CRM mapping, refer to the main project documentation.

---

## 📅 Version Information

- **Created:** 2025-10-17
- **Property Version:** 1.0
- **Package Version:** 1.0
- **CIDOC-CRM Version:** 7.1.1
- **Compatible with:** GMN Ontology v1.0+
