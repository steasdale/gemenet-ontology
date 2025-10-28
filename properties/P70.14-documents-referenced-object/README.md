# GMN Ontology: P70.14 Documents Referenced Object Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_14_documents_referenced_object` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-object-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-object-documentation.md** - Complete semantic documentation
4. **documents-object-ontology.ttl** - Ready-to-copy TTL definitions
5. **documents-object-transform.py** - Ready-to-copy Python transformation code
6. **documents-object-doc-note.txt** - Documentation additions for the main docs

---

## 🎯 Quick Start Checklist

### Prerequisites
- [ ] Backup current ontology file (`gmn_ontology.ttl`)
- [ ] Backup transformation script (`gmn_to_cidoc_transform.py`)
- [ ] Backup main documentation file

### Implementation Steps
1. [ ] Add TTL definitions to `gmn_ontology.ttl` (from `documents-object-ontology.ttl`)
2. [ ] Add transformation function to `gmn_to_cidoc_transform.py` (from `documents-object-transform.py`)
3. [ ] Add function call to main transformation pipeline
4. [ ] Update main documentation (from `documents-object-doc-note.txt`)
5. [ ] Run test transformations
6. [ ] Validate output with CIDOC-CRM compliance

### Testing
- [ ] Test with simple object reference (single URI)
- [ ] Test with complex object (nested data)
- [ ] Test with multiple objects (array)
- [ ] Verify P67_refers_to structure
- [ ] Verify E1_CRM_Entity typing

---

## 📋 Implementation Summary

### Property Overview

**Property URI**: `gmn:P70_14_documents_referenced_object`

**Purpose**: Associate sales contracts with any legal or physical objects referenced in the document text.

**Key Features**:
- Captures legal objects (rights, obligations, debts, claims, privileges, servitudes, easements)
- Captures physical objects mentioned in contracts
- Uses direct P67_refers_to relationship
- Flexible E1_CRM_Entity range allows for any type of object

### Transformation Pattern

```
INPUT (GMN simplified):
{
  "@id": "contract:123",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_14_documents_referenced_object": [...]
}

OUTPUT (CIDOC-CRM compliant):
{
  "@id": "contract:123",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "object:uri",
      "@type": "cidoc:E1_CRM_Entity"
    }
  ]
}
```

### CIDOC-CRM Structure

```
E31_Document (Sales Contract)
  └─ P67_refers_to
      └─ E1_CRM_Entity (Referenced Object)
```

---

## 🔍 Common Use Cases

### Legal Objects
- Water rights attached to property
- Easements or servitudes
- Existing debts being settled
- Claims or privileges being transferred
- Rights of way or usage rights

### Physical Objects
- Existing structures mentioned (wells, buildings)
- Moveable property included in the transaction
- Fixtures or attachments
- Objects used to define boundaries

---

## 📚 Related Properties

- **P70.13** (documents_referenced_place) - For places mentioned in the contract
- **P70.11** (documents_referenced_person) - For persons mentioned in the contract
- **P70.3** (documents_transfer_of) - For the primary object being transferred

---

## 🛠️ Integration Points

### In Ontology File
Location: After P70.13 definition, before P70.15

### In Transform Script
- Function: `transform_p70_14_documents_referenced_object()`
- Call location: Main transformation pipeline after P70.13, before P70.15

### In Documentation
Section: P70.14 subsection in property documentation

---

## ⚠️ Important Notes

1. **Range Flexibility**: Uses E1_CRM_Entity as range to accommodate both legal objects (E72_Legal_Object) and physical things (E18_Physical_Thing)

2. **vs. Transfer Object**: P70.3 (documents_transfer_of) is for the primary object being sold, while P70.14 is for additional objects mentioned in the contract

3. **Direct Reference**: Uses P67_refers_to for direct document-to-object relationship, not P70_documents like transactional properties

4. **Type Preservation**: If object data includes specific types (E72_Legal_Object, E18_Physical_Thing), these are preserved in transformation

---

## 📞 Support

For questions or issues:
- Review the Implementation Guide for detailed instructions
- Check the Documentation file for semantic details
- Consult CIDOC-CRM documentation for P67_refers_to usage

---

**Version**: 1.0  
**Date**: 2025-10-27  
**Property Code**: P70.14
