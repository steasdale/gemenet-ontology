# GMN Ontology: P70.11 Documents Referenced Person Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_11_documents_referenced_person` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-referenced-person-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-referenced-person-documentation.md** - Complete semantic documentation
4. **documents-referenced-person-ontology.ttl** - Ready-to-copy TTL snippets
5. **documents-referenced-person-transform.py** - Ready-to-copy Python code
6. **documents-referenced-person-doc-note.txt** - Documentation additions with examples

---

## 🎯 Quick Start Checklist

### For Ontology File (`gmn_ontology.ttl`)
- [ ] Copy TTL definition from `documents-referenced-person-ontology.ttl`
- [ ] Paste after P70.10 definition (around line 1100)
- [ ] Verify proper indentation and syntax
- [ ] Check that property URI is `gmn:P70_11_documents_referenced_person`

### For Transformation Script (`gmn_to_cidoc_transform.py`)
- [ ] Copy function from `documents-referenced-person-transform.py`
- [ ] Paste after `transform_p70_10_documents_payment_recipient_for_seller()` (around line 803)
- [ ] Add function call to `transform_item()` around line 2350
- [ ] Place after `transform_p70_10_documents_payment_recipient_for_seller(item)`
- [ ] Run unit tests to verify transformation

### For Documentation File
- [ ] Add content from `documents-referenced-person-doc-note.txt`
- [ ] Insert in appropriate section for P70 properties
- [ ] Add examples to examples section
- [ ] Update table of contents if needed

---

## 📋 Property Overview

### Purpose
The `gmn:P70_11_documents_referenced_person` property captures persons who are mentioned in a document but do not have a specified transactional role. This includes witnesses, deceased persons mentioned in context, neighbors referenced in property descriptions, previous owners, and any other individuals named in the document text who are not direct participants in the documented activity.

### Key Characteristics
- **Simplified Property**: Yes (transforms to CIDOC-CRM P67_refers_to)
- **Domain**: `cidoc:E31_Document`
- **Range**: `cidoc:E21_Person`
- **Subproperty Of**: `cidoc:P67_refers_to`
- **Creation Date**: 2025-10-17

### Distinction from Other Properties
Unlike properties that document participation in the E8_Acquisition event (seller, buyer, procurator, etc.), this property represents a direct relationship between the document and the person: **E31_Document > P67_refers_to > E21_Person**. This acknowledges that the person is textually present without implying their participation in the transaction.

---

## 🔄 Transformation Pattern

### Input (GMN Simplified)
```turtle
:contract_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_11_documents_referenced_person :giovanni_deceased ,
                                           :marco_neighbor .

:giovanni_deceased a cidoc:E21_Person ;
    rdfs:label "Giovanni (deceased father)" .

:marco_neighbor a cidoc:E21_Person ;
    rdfs:label "Marco (adjacent property owner)" .
```

### Output (CIDOC-CRM Compliant)
```turtle
:contract_001 a gmn:E31_2_Sales_Contract ;
    cidoc:P67_refers_to :giovanni_deceased ,
                        :marco_neighbor .

:giovanni_deceased a cidoc:E21_Person ;
    rdfs:label "Giovanni (deceased father)" .

:marco_neighbor a cidoc:E21_Person ;
    rdfs:label "Marco (adjacent property owner)" .
```

---

## 💡 Common Use Cases

### 1. Deceased Persons in Context
**Scenario**: "Giovanni, son of the late Marco"
```turtle
:contract_123 gmn:P70_11_documents_referenced_person :marco_deceased .
:marco_deceased rdfs:label "Marco (deceased father of seller)" .
```

### 2. Neighbors in Property Descriptions
**Scenario**: Property boundaries reference adjacent owners
```turtle
:contract_456 gmn:P70_11_documents_referenced_person :pietro_neighbor .
:pietro_neighbor rdfs:label "Pietro (owner of adjacent vineyard)" .
```

### 3. Previous Owners in Provenance
**Scenario**: "Previously owned by Antonio da Firenze"
```turtle
:contract_789 gmn:P70_11_documents_referenced_person :antonio_previous .
:antonio_previous rdfs:label "Antonio da Firenze (previous owner)" .
```

### 4. Family Members Mentioned
**Scenario**: "With consent of his brother Lorenzo"
```turtle
:contract_012 gmn:P70_11_documents_referenced_person :lorenzo_brother .
:lorenzo_brother rdfs:label "Lorenzo (brother of seller)" .
```

---

## ⚠️ Important Notes

### When to Use This Property
✅ Use `P70_11_documents_referenced_person` for:
- Persons mentioned in narrative context
- Deceased individuals referenced for identification
- Neighbors named in boundary descriptions
- Previous owners in provenance statements
- Family members mentioned but not participating
- Any person named without a specific transactional role

### When NOT to Use This Property
❌ Do NOT use for:
- **Witnesses** → Use `P70_15_documents_witness` (they participated in the event)
- **Sellers** → Use `P70_1_documents_seller`
- **Buyers** → Use `P70_2_documents_buyer`
- **Procurators** → Use `P70_4` or `P70_5`
- **Guarantors** → Use `P70_6` or `P70_7`
- **Brokers** → Use `P70_8_documents_broker`
- Any person with a defined role in the transaction

### Data Quality Considerations
- Be consistent in how you describe the person's relationship (use rdfs:label or notes)
- Consider creating separate person records for better linkage
- Document the context of the reference in notes
- Distinguish living references from deceased persons

---

## 🔗 Related Properties

| Property | Purpose | Relationship |
|----------|---------|--------------|
| `P70_15_documents_witness` | Active witnesses | Use for participatory roles, not mere mentions |
| `P67_refers_to` | General reference | P70.11 is subproperty of this |
| `P70_13_documents_referenced_place` | Referenced places | Similar pattern for geographic references |
| `P70_14_documents_referenced_object` | Referenced objects | Similar pattern for object references |

---

## 📚 Additional Resources

### Documentation Files in This Package
1. **Implementation Guide** - Detailed step-by-step installation and testing procedures
2. **Ontology Documentation** - Complete semantic analysis and usage patterns
3. **TTL Additions** - Ready-to-paste ontology definitions
4. **Python Additions** - Complete transformation function with comments
5. **Doc Note** - Examples and tables for main documentation

### External References
- CIDOC-CRM P67_refers_to: https://cidoc-crm.org/Property/P67-refers-to/version-7.1.3
- CIDOC-CRM E21_Person: https://cidoc-crm.org/Entity/E21-Person/version-7.1.3

---

## 🚀 Implementation Summary

### Complexity Level
**Low** - Simple transformation pattern with direct P67_refers_to mapping

### Estimated Implementation Time
- Ontology addition: 5 minutes
- Python transformation: 10 minutes
- Testing: 15 minutes
- Documentation: 10 minutes
**Total: ~40 minutes**

### Dependencies
- No special dependencies
- Works with any document type (E31_Document or subclasses)
- No interaction with other transformation functions
- Can handle multiple referenced persons per document

### Testing Requirements
1. Single person reference
2. Multiple person references
3. Person with URI only
4. Person with full data object
5. Document with no referenced persons (should pass through unchanged)

---

## 📞 Support

For questions or issues with this property implementation:
1. Review the detailed documentation in `documents-referenced-person-documentation.md`
2. Check the implementation guide for step-by-step instructions
3. Verify TTL syntax using a Turtle validator
4. Test transformation with provided examples

---

## ✅ Validation Checklist

After implementation, verify:
- [ ] Property appears in ontology with correct URI
- [ ] Property has correct domain (E31_Document)
- [ ] Property has correct range (E21_Person)
- [ ] Transformation function processes single persons correctly
- [ ] Transformation function processes multiple persons correctly
- [ ] Transformation handles both URI and object formats
- [ ] Output uses P67_refers_to correctly
- [ ] E21_Person type is preserved or added
- [ ] Original property is removed from output
- [ ] Function is called in transform_item() pipeline

---

**Version**: 1.0  
**Date**: October 2025  
**Property**: gmn:P70_11_documents_referenced_person  
**Status**: Ready for Implementation
