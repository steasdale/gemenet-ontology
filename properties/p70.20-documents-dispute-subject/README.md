# GMN Ontology: P70.20 Documents Dispute Subject Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70.20_documents_dispute_subject` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file)
   - Overview of deliverables
   - Quick-start checklist
   - Implementation summary

2. **documents-dispute-object-implementation-guide.md**
   - Step-by-step implementation instructions
   - Code integration procedures
   - Testing and validation steps

3. **documents-dispute-object-documentation.md**
   - Complete semantic documentation
   - Property specifications
   - Usage guidelines and examples

4. **documents-dispute-object-ontology.ttl**
   - Ready-to-copy TTL snippets
   - Property definition for main ontology file

5. **documents-dispute-object-transform.py**
   - Ready-to-copy Python transformation function
   - Integration code for transformation script

6. **documents-dispute-object-doc-note.txt**
   - Examples and tables for main documentation
   - Ready-to-paste content additions

---

## 🎯 Property Overview

**Property:** `gmn:P70_20_documents_dispute_subject`

**Label:** P70.20 documents dispute subject

**Purpose:** Simplified property for associating an arbitration agreement with the subject matter of the dispute being arbitrated.

**Domain:** `gmn:E31_3_Arbitration_Agreement`

**Range:** `cidoc:E1_CRM_Entity`

**CIDOC-CRM Path:**
```
E31_Document 
  → P70_documents 
    → E7_Activity 
      → P16_used_specific_object 
        → E1_CRM_Entity
```

**Key Features:**
- ✅ Links arbitration agreements to the matter in dispute
- ✅ Supports any entity type (property, debt, right, contract, etc.)
- ✅ Multiple subjects can be referenced
- ✅ Transforms to full CIDOC-CRM structure
- ✅ Shares E7_Activity with P70.18 and P70.19 properties

---

## ⚡ Quick-Start Checklist

### 1. Ontology Implementation
- [ ] Open `gmn_ontology.ttl`
- [ ] Locate the arbitration agreement section (search for "P70.20")
- [ ] Verify property definition is present
- [ ] If absent, copy from `documents-dispute-object-ontology.ttl`
- [ ] Save and validate TTL syntax

### 2. Transformation Script Implementation
- [ ] Open `gmn_to_cidoc_transform.py`
- [ ] Locate arbitration transformation section
- [ ] Verify `transform_p70_20_documents_dispute_subject()` function exists
- [ ] If absent, copy from `documents-dispute-object-transform.py`
- [ ] Add function call to transformation pipeline
- [ ] Save and test syntax

### 3. Documentation Update
- [ ] Open main documentation file
- [ ] Locate arbitration agreement section
- [ ] Add property description from `documents-dispute-object-doc-note.txt`
- [ ] Update property tables
- [ ] Add usage examples
- [ ] Save documentation

### 4. Testing
- [ ] Create test arbitration agreement with dispute subject
- [ ] Run transformation script
- [ ] Verify E7_Activity creation
- [ ] Verify P16_used_specific_object is populated
- [ ] Validate output against CIDOC-CRM structure
- [ ] Test with multiple subjects

### 5. Validation
- [ ] Check shared E7_Activity with P70.18 and P70.19
- [ ] Verify arbitration typing (AAT 300417271)
- [ ] Confirm shortcut property removal
- [ ] Validate entity typing
- [ ] Test SPARQL queries

---

## 📋 Implementation Summary

### What This Property Does

The `gmn:P70_20_documents_dispute_subject` property provides a simplified way to link arbitration agreements to the subject matter being arbitrated. It represents the **matter in dispute** - what the conflict is about.

**Common Dispute Subjects:**
- Physical property (buildings, land, ships, goods)
- Legal rights and obligations
- Monetary debts or claims
- Contract disputes
- Services or performances

### How It Works

1. **Input Format** (simplified for data entry):
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/property/building123"},
    {"@id": "http://example.org/debts/debt_xyz"}
  ]
}
```

2. **Transformation Process:**
   - Locates or creates E7_Activity typed as arbitration
   - Adds subjects to activity's P16_used_specific_object
   - Removes shortcut property

3. **Output Format** (CIDOC-CRM compliant):
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {"@id": "http://vocab.getty.edu/page/aat/300417271"},
    "cidoc:P16_used_specific_object": [
      {"@id": "http://example.org/property/building123", "@type": "cidoc:E1_CRM_Entity"},
      {"@id": "http://example.org/debts/debt_xyz", "@type": "cidoc:E1_CRM_Entity"}
    ]
  }]
}
```

### Integration with Related Properties

This property works together with:
- **P70.18** (documents disputing party) - adds parties via P14_carried_out_by
- **P70.19** (documents arbitrator) - adds arbitrators via P14_carried_out_by
- **P70.20** (documents dispute subject) - adds subjects via P16_used_specific_object

All three properties contribute to the **same E7_Activity node**, representing one unified arbitration process.

### Semantic Meaning

The use of `P16_used_specific_object` indicates that the arbitration activity **operates on** or **concerns** the dispute subject. The arbitration process uses knowledge of the subject to render a decision about it.

---

## 🔍 Key Design Decisions

### 1. P16 vs P67 (refers_to)

**Decision:** Use P16_used_specific_object rather than P67_refers_to

**Rationale:**
- P16 indicates the subject is **central to** the activity
- P67 would indicate mere **mention** of the subject
- The dispute subject is what the arbitration operates on, not just mentions
- Aligns with the semantic meaning of arbitration (deciding about the subject)

### 2. Range: E1_CRM_Entity

**Decision:** Use the broadest possible range (E1_CRM_Entity)

**Rationale:**
- Dispute subjects can be any entity type
- Allows maximum flexibility for modeling different disputes
- Physical things, legal objects, documents, activities all supported
- Real-world arbitrations involved diverse subject matters

### 3. Shared Activity Pattern

**Decision:** All three arbitration properties share one E7_Activity

**Rationale:**
- One arbitration agreement = one arbitration activity
- Prevents fragmentation of related information
- Matches sales contract pattern (one acquisition event)
- Easier querying and data integrity

---

## 📚 Additional Resources

### Reference Files
- **Implementation Guide:** `documents-dispute-object-implementation-guide.md`
- **Full Documentation:** `documents-dispute-object-documentation.md`
- **TTL Snippets:** `documents-dispute-object-ontology.ttl`
- **Python Code:** `documents-dispute-object-transform.py`
- **Doc Additions:** `documents-dispute-object-doc-note.txt`

### External References
- CIDOC-CRM P16: http://www.cidoc-crm.org/Property/P16-used-specific-object/version-7.1.1
- CIDOC-CRM E7: http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.1
- AAT Arbitration: http://vocab.getty.edu/page/aat/300417271
- Main Arbitration Documentation: `arbitration-ontology.md`

### Support
For questions or issues with implementation:
1. Review the implementation guide
2. Check the full documentation for usage examples
3. Refer to the main arbitration ontology documentation
4. Test with provided examples

---

## ✅ Validation Checklist

After implementation, verify:
- [ ] Property defined in ontology
- [ ] Transformation function added to script
- [ ] Function called in transformation pipeline
- [ ] Test data transforms correctly
- [ ] E7_Activity properly typed
- [ ] P16_used_specific_object populated
- [ ] Shortcut property removed
- [ ] Integration with P70.18 and P70.19 works
- [ ] Documentation updated
- [ ] SPARQL queries return expected results

---

**Package Version:** 1.0  
**Created:** October 28, 2025  
**Property Status:** Active  
**Last Updated:** October 28, 2025
