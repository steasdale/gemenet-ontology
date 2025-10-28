# GMN Ontology: P70.19 Documents Arbitrator Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_19_documents_arbitrator` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file)
   - Overview and quick-start guide
   - Implementation checklist
   - Package summary

2. **documents-arbitrator-implementation-guide.md**
   - Step-by-step implementation instructions
   - Code integration procedures
   - Testing and validation procedures

3. **documents-arbitrator-documentation.md**
   - Complete semantic documentation
   - Class and property specifications
   - Transformation examples
   - SPARQL query examples

4. **documents-arbitrator-ontology.ttl**
   - Ready-to-copy TTL snippets
   - Property definition in Turtle format
   - For addition to main ontology file

5. **documents-arbitrator-transform.py**
   - Ready-to-copy Python code
   - Transformation function
   - For addition to transformation script

6. **documents-arbitrator-doc-note.txt**
   - Examples and usage notes
   - Tables and reference materials
   - For addition to main documentation

---

## 🎯 Property Overview

**Property URI:** `gmn:P70_19_documents_arbitrator`

**Label:** P70.19 documents arbitrator

**Purpose:** Simplified property for associating an arbitration agreement with the person or persons appointed to resolve the dispute.

**Domain:** `gmn:E31_3_Arbitration_Agreement`

**Range:** `cidoc:E39_Actor`

**CIDOC-CRM Path:**
```
E31_Document 
  → P70_documents 
    → E7_Activity 
      → P14_carried_out_by 
        → E39_Actor
```

---

## ⚡ Quick Start Checklist

### Prerequisites
- [ ] GMN ontology file (`gmn_ontology.ttl`) accessible
- [ ] Transformation script (`gmn_to_cidoc_transform.py`) accessible
- [ ] Understanding of arbitration agreement context
- [ ] Familiarity with CIDOC-CRM P70_documents pattern

### Implementation Steps

#### 1. Ontology Update
- [ ] Open `gmn_ontology.ttl`
- [ ] Locate the arbitration properties section (around line with P70.18/P70.19)
- [ ] Verify `gmn:P70_19_documents_arbitrator` definition exists
- [ ] If missing, copy from `documents-arbitrator-ontology.ttl`
- [ ] Validate TTL syntax

#### 2. Transformation Script Update
- [ ] Open `gmn_to_cidoc_transform.py`
- [ ] Locate arbitration transformation functions
- [ ] Verify `transform_p70_19_documents_arbitrator()` function exists
- [ ] If missing, copy from `documents-arbitrator-transform.py`
- [ ] Add function call to transformation pipeline
- [ ] Verify shared activity pattern with P70.18 and P70.20

#### 3. Documentation Update
- [ ] Review `documents-arbitrator-documentation.md` for semantic details
- [ ] Add usage examples from `documents-arbitrator-doc-note.txt` to main docs
- [ ] Update property index/table of contents
- [ ] Add cross-references to related properties

#### 4. Testing
- [ ] Create test arbitration agreement with arbitrator(s)
- [ ] Run transformation script
- [ ] Verify E7_Activity creation
- [ ] Confirm P14_carried_out_by relationship
- [ ] Validate AAT typing (300417271)
- [ ] Test with multiple arbitrators
- [ ] Test integration with P70.18 (disputing parties)

#### 5. Validation
- [ ] Run SPARQL queries from documentation
- [ ] Verify query results match expectations
- [ ] Check for duplicate activities
- [ ] Validate all arbitrators appear in P14_carried_out_by

---

## 📋 Implementation Summary

### What This Property Does

The `gmn:P70_19_documents_arbitrator` property creates a simplified way to associate arbitration agreements with the arbitrators appointed to resolve disputes. It's a shortcut that expands into a full CIDOC-CRM compliant structure during transformation.

### Key Characteristics

1. **Shared Activity Pattern**
   - Uses the same E7_Activity as P70.18 (disputing parties) and P70.20 (dispute subject)
   - All three properties contribute to one arbitration activity
   - Ensures semantic unity of the arbitration agreement

2. **Active Principal Role**
   - Arbitrators are modeled as active principals (P14_carried_out_by)
   - They carry out the arbitration process
   - Not passive observers but decision-makers

3. **Multiple Arbitrators**
   - Supports single arbitrator or arbitration panels
   - Each arbitrator added individually to P14_carried_out_by
   - No limit on number of arbitrators

4. **Activity Typing**
   - E7_Activity typed with AAT 300417271 (arbitration)
   - Distinguishes arbitration from other activities
   - Enables precise querying

### Integration Points

**Works Together With:**
- `gmn:P70_18_documents_disputing_party` - parties to the dispute
- `gmn:P70_20_documents_dispute_subject` - subject matter of dispute
- `gmn:E31_3_Arbitration_Agreement` - document class
- Standard document properties (dates, places, creators)

**Activity Coordination:**
All three arbitration properties (P70.18, P70.19, P70.20) share a single E7_Activity instance. The transformation functions coordinate to:
1. Detect existing activity
2. Reuse or create as needed
3. Add appropriate relationships
4. Maintain semantic coherence

### Transformation Behavior

**Input (GMN):**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator_1"}
  ]
}
```

**Output (CIDOC-CRM):**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271",
      "@type": "cidoc:E55_Type"
    },
    "cidoc:P14_carried_out_by": [
      {"@id": "http://example.org/persons/arbitrator_1", "@type": "cidoc:E39_Actor"}
    ]
  }]
}
```

---

## 🔗 Related Properties

| Property | Purpose | Relationship |
|----------|---------|--------------|
| `gmn:P70_18_documents_disputing_party` | Links disputing parties | Shares same E7_Activity |
| `gmn:P70_20_documents_dispute_subject` | Links dispute subject | Shares same E7_Activity |
| `gmn:E31_3_Arbitration_Agreement` | Document class | Domain for this property |
| `cidoc:P14_carried_out_by` | Actor relationship | Target of transformation |

---

## 📚 Additional Resources

- **Arbitration Ontology Documentation:** `/mnt/project/arbitration-ontology.md`
- **GMN Main Ontology:** `/mnt/project/gmn_ontology.ttl`
- **Transformation Script:** `/mnt/project/gmn_to_cidoc_transform.py`
- **CIDOC-CRM Documentation:** http://www.cidoc-crm.org/
- **Getty AAT (Arbitration):** http://vocab.getty.edu/page/aat/300417271

---

## 🚀 Getting Started

1. **Review** this README to understand the property
2. **Read** `documents-arbitrator-documentation.md` for complete semantic details
3. **Follow** `documents-arbitrator-implementation-guide.md` for step-by-step instructions
4. **Copy** code from `.ttl` and `.py` files as needed
5. **Test** using examples from documentation
6. **Validate** using SPARQL queries

---

## ❓ Questions & Support

If you encounter issues:
1. Verify all prerequisites are met
2. Check the implementation guide for troubleshooting
3. Review the semantic documentation for clarification
4. Examine test examples for correct usage patterns

---

## 📝 Version Information

- **Package Version:** 1.0
- **Property Created:** 2025-10-17
- **Last Modified:** 2025-10-18
- **Compatibility:** GMN Ontology v1.0+

---

## ✅ Success Criteria

Implementation is successful when:
- [ ] Arbitration agreements can link to arbitrators
- [ ] Transformation creates proper E7_Activity structure
- [ ] Multiple arbitrators supported
- [ ] Integration with P70.18 and P70.20 works correctly
- [ ] SPARQL queries return expected results
- [ ] No duplicate activities created

---

*This deliverables package provides everything needed to implement the documents arbitrator property in the GMN ontology.*
