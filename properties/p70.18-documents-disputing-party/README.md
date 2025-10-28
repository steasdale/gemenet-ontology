# GMN Ontology: P70.18 Documents Disputing Party Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_18_documents_disputing_party` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-disputing-property-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-disputing-property-documentation.md** - Complete semantic documentation
4. **documents-disputing-property-ontology.ttl** - TTL snippets for ontology file
5. **documents-disputing-property-transform.py** - Python code for transformation script
6. **documents-disputing-property-doc-note.txt** - Documentation additions for text files

---

## 🎯 Quick Start

### For Implementation

1. Read the **Implementation Guide** for step-by-step instructions
2. Copy TTL snippets from **documents-disputing-property-ontology.ttl** to `gmn_ontology.ttl`
3. Copy Python code from **documents-disputing-property-transform.py** to `gmn_to_cidoc_transform.py`
4. Follow testing procedures in the Implementation Guide
5. Add documentation from **documents-disputing-property-doc-note.txt** to your text files

### For Understanding

1. Read the **Ontology Documentation** for semantic details
2. Review property specifications and CIDOC-CRM mappings
3. Examine transformation examples

---

## 📋 Implementation Checklist

### Phase 1: Ontology Definition
- [ ] Add property definition to `gmn_ontology.ttl`
- [ ] Verify TTL syntax with RDF validator
- [ ] Document property in ontology comments

### Phase 2: Transformation Script
- [ ] Add `transform_p70_18_documents_disputing_party()` function
- [ ] Update main transformation pipeline
- [ ] Add function to transformation list

### Phase 3: Testing
- [ ] Test with sample arbitration agreement data
- [ ] Verify CIDOC-CRM structure is correct
- [ ] Test with multiple disputing parties
- [ ] Validate JSON-LD output

### Phase 4: Documentation
- [ ] Add property to main documentation
- [ ] Create usage examples
- [ ] Document SPARQL query patterns

---

## 🔑 Key Concepts

### Property Overview

**gmn:P70_18_documents_disputing_party** is a simplified property for associating an arbitration agreement with the parties involved in the dispute.

**Semantic Path:**
```
E31_3_Arbitration_Agreement 
  → P70_documents 
    → E7_Activity 
      → P14_carried_out_by 
        → E39_Actor
```

### Core Features

1. **Shortcut Property**: Simplifies CIDOC-CRM structure for data entry
2. **Multiple Parties**: Supports two or more disputing parties
3. **Active Principals**: Uses P14_carried_out_by (not passive P11_had_participant)
4. **Shared Activity**: Links to same E7_Activity as arbitrators

### Transformation Behavior

The transformation:
- Creates or locates an E7_Activity node (arbitration process)
- Types the activity as arbitration (AAT 300417271)
- Adds each party to P14_carried_out_by
- Removes the shortcut property from output

---

## 📊 Property Summary

| Aspect | Value |
|--------|-------|
| **URI** | `http://www.genoesemerchantnetworks.com/ontology#P70_18_documents_disputing_party` |
| **Label** | P70.18 documents disputing party |
| **Domain** | gmn:E31_3_Arbitration_Agreement |
| **Range** | cidoc:E39_Actor |
| **Superproperty** | cidoc:P70_documents |
| **Cardinality** | One or many (typically two or more) |
| **Status** | Active |

---

## 🔗 Related Properties

This property is part of the arbitration agreement property set:

- **gmn:P70_18_documents_disputing_party** - Parties to the dispute (this property)
- **gmn:P70_19_documents_arbitrator** - Arbitrators appointed to resolve dispute
- **gmn:P70_20_documents_dispute_subject** - Subject matter of the dispute

All three properties contribute to the same E7_Activity node.

---

## 💡 Usage Examples

### Simple Example (Two Parties)

**Input:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/merchant1"},
    {"@id": "http://example.org/persons/merchant2"}
  ]
}
```

**Output:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contracts/arb001/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P14_carried_out_by": [
      {"@id": "http://example.org/persons/merchant1", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/merchant2", "@type": "cidoc:E39_Actor"}
    ]
  }]
}
```

### Complex Example (With Arbitrator and Subject)

**Input:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/property/building123"}
  ]
}
```

**Output:**
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
      {"@id": "http://example.org/persons/party1", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/party2", "@type": "cidoc:E39_Actor"},
      {"@id": "http://example.org/persons/arbitrator", "@type": "cidoc:E39_Actor"}
    ],
    "cidoc:P16_used_specific_object": [
      {"@id": "http://example.org/property/building123", "@type": "cidoc:E1_CRM_Entity"}
    ]
  }]
}
```

---

## 📚 Documentation Files

### Implementation Guide
Complete step-by-step instructions for adding this property to your system, including:
- Prerequisites and dependencies
- Code integration steps
- Testing procedures
- Troubleshooting tips

### Ontology Documentation
Semantic documentation including:
- Detailed property specifications
- CIDOC-CRM path mappings
- Design rationale
- Usage guidelines
- SPARQL query examples

### Code Files
Ready-to-copy code snippets:
- **TTL**: Ontology definition
- **Python**: Transformation function
- **Documentation**: Example text and tables

---

## 🔍 Testing Guidelines

### Unit Tests

Test the transformation with:
1. Single arbitration agreement with two disputing parties
2. Multiple disputing parties (3+)
3. Combination with arbitrator property
4. Combination with all arbitration properties
5. Missing or empty property values

### Integration Tests

Verify:
1. Activity URI generation is consistent
2. Activity is shared across all arbitration properties
3. Existing activity is reused when present
4. Property is removed after transformation
5. Output validates against CIDOC-CRM

### Sample Test Data

```json
{
  "@id": "http://example.org/contracts/test001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [{"@value": "Test Arbitration Agreement"}],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"}
  ]
}
```

---

## 🚀 Version Information

- **Package Version**: 1.0
- **Property Version**: 1.0
- **Created**: October 2025
- **Last Updated**: October 2025
- **GMN Ontology Version**: 1.0+
- **CIDOC-CRM Version**: 7.1.1

---

## 📖 Additional Resources

### Internal Documentation
- Arbitration Agreement Ontology Documentation
- GMN Ontology Main Documentation
- Correspondence Documentation
- Donation Documentation
- Dowry Documentation

### External References
- CIDOC-CRM Official Documentation: http://www.cidoc-crm.org/
- Getty AAT (Arbitration): http://vocab.getty.edu/page/aat/300417271
- Getty AAT (E7 Activity): http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.1

---

## 🆘 Support

For questions or issues:
1. Review the Implementation Guide
2. Check the Ontology Documentation
3. Examine test cases and examples
4. Consult the main GMN documentation

---

## ✅ Implementation Status

Once you've completed the implementation, use this checklist:

- [ ] Ontology definition added
- [ ] Transformation function implemented
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] SPARQL queries tested
- [ ] Production deployment ready

---

**Ready to implement?** Start with the **Implementation Guide** for step-by-step instructions!
