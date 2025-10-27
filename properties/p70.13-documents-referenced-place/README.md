# GMN Ontology: P70.13 Documents Referenced Place Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_13_documents_referenced_place` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-place-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-place-documentation.md** - Complete semantic documentation
4. **documents-place-ontology.ttl** - TTL snippets for ontology file
5. **documents-place-transform.py** - Python code for transformation script
6. **documents-place-doc-note.txt** - Documentation examples and tables

---

## 🎯 Property Overview

**Property**: `gmn:P70_13_documents_referenced_place`

**Purpose**: Associates a sales contract with any place referenced or mentioned in the document text (boundary descriptions, landmarks, districts, parishes, etc.)

**Domain**: `gmn:E31_2_Sales_Contract`

**Range**: `cidoc:E53_Place`

**CIDOC-CRM Path**: `E31_Document > P67_refers_to > E53_Place`

**Key Distinction**: Unlike `P94i_3_has_place_of_enactment` (where the contract was created), this property represents places mentioned within the contract content itself.

---

## ⚡ Quick Start Checklist

### For Ontology Maintainers
- [ ] Copy TTL from `documents-place-ontology.ttl`
- [ ] Add to main ontology file under P70 property section
- [ ] Validate TTL syntax
- [ ] Commit changes with descriptive message

### For Developers
- [ ] Copy function from `documents-place-transform.py`
- [ ] Add to transformation script
- [ ] Add function call to main transform pipeline
- [ ] Run test suite
- [ ] Verify CIDOC-CRM output structure

### For Documentation Team
- [ ] Review semantic documentation
- [ ] Copy examples from `documents-place-doc-note.txt`
- [ ] Add to main documentation file
- [ ] Update property index/table

---

## 📊 Implementation Summary

### Transformation Logic
```
INPUT:  gmn:P70_13_documents_referenced_place → E53_Place
OUTPUT: cidoc:P67_refers_to → E53_Place
```

**Transformation Type**: Direct property mapping with type inference

**Complexity**: Low (simple P67 reference)

**Dependencies**: None

---

## 🔍 Use Cases

### Typical Scenarios
1. **Boundary Descriptions**: "bounded on the north by the property of Giovanni..."
2. **Landmark References**: "near the Rialto bridge..."
3. **District/Parish Mentions**: "in the parish of San Polo..."
4. **Geographic Context**: "facing the Grand Canal..."

### Data Entry Examples

**Simple URI Reference**:
```json
{
  "@id": "contract123",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_13_documents_referenced_place": "place:rialto_bridge"
}
```

**Detailed Place Object**:
```json
{
  "@id": "contract123",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_13_documents_referenced_place": [
    {
      "@id": "place:san_polo_parish",
      "@type": "cidoc:E53_Place",
      "rdfs:label": "Parish of San Polo"
    },
    {
      "@id": "place:grand_canal",
      "@type": "cidoc:E53_Place",
      "rdfs:label": "Grand Canal"
    }
  ]
}
```

---

## 🔗 Related Properties

| Property | Purpose | Difference |
|----------|---------|------------|
| `gmn:P94i_3_has_place_of_enactment` | Where contract was created | Contract creation location vs. mentioned places |
| `gmn:P70_3_documents_transfer_of` | Property being transferred | The transaction subject vs. reference points |
| `gmn:P70_11_documents_referenced_person` | Persons mentioned in text | Similar pattern for people instead of places |

---

## 📋 Files Description

### 1. Implementation Guide
- **File**: `documents-place-implementation-guide.md`
- **Audience**: Developers, ontology maintainers
- **Contains**: Step-by-step implementation, code snippets, testing procedures

### 2. Ontology Documentation
- **File**: `documents-place-documentation.md`
- **Audience**: Domain experts, semantic web specialists
- **Contains**: Property definitions, CIDOC-CRM mappings, scope notes

### 3. TTL Additions
- **File**: `documents-place-ontology.ttl`
- **Audience**: Ontology maintainers
- **Contains**: Copy-paste ready Turtle syntax for ontology file

### 4. Python Transform Code
- **File**: `documents-place-transform.py`
- **Audience**: Developers
- **Contains**: Transformation function with error handling

### 5. Documentation Examples
- **File**: `documents-place-doc-note.txt`
- **Audience**: Documentation team
- **Contains**: Usage examples, tables, explanatory text

---

## ⚙️ Technical Notes

### Transformation Behavior
- **Input Validation**: Accepts both URI strings and place objects
- **Type Inference**: Adds `@type: cidoc:E53_Place` if not present
- **Multiple Places**: Supports array of place references
- **Null Safety**: Handles missing property gracefully

### Integration Points
1. **Ontology File**: Add after P70.12 property definition
2. **Transform Script**: Add before P70.14 transformation
3. **Documentation**: Add in "Place Properties" section

---

## 🧪 Testing Recommendations

### Unit Tests
- [ ] Single place URI reference
- [ ] Multiple place references
- [ ] Place object with @type
- [ ] Place object without @type (infers E53_Place)
- [ ] Missing property (no error)
- [ ] Empty array (no error)

### Integration Tests
- [ ] Complete contract with multiple P70 properties
- [ ] Validate CIDOC-CRM compliance
- [ ] Check no duplicate P67_refers_to entries

---

## 📝 Version Information

**Version**: 1.0
**Created**: 2025-10-27
**Status**: Production Ready
**CIDOC-CRM Version**: 7.1
**Ontology Namespace**: `http://www.genoamemerchants.net/ontology#`

---

## 👥 Support

For questions or issues:
- Review semantic documentation in `documents-place-documentation.md`
- Check implementation guide for troubleshooting
- Consult project knowledge base
- Reference CIDOC-CRM documentation: http://www.cidoc-crm.org/

---

## 📜 License & Attribution

Part of the Genoese Merchants Network (GMN) ontology project.
Based on CIDOC-CRM v7.1 standard.

---

**Quick Implementation**: Start with step 1 in `documents-place-implementation-guide.md`
