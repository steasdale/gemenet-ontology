# GMN Ontology: P11i.3 Has Spouse Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P11i_3_has_spouse` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **has-spouse-implementation-guide.md** - Step-by-step implementation instructions
3. **has-spouse-documentation.md** - Complete semantic documentation
4. **has-spouse-ontology.ttl** - TTL snippets for ontology file
5. **has-spouse-transform.py** - Python code for transformation script
6. **has-spouse-doc-note.txt** - Documentation examples and tables

---

## 🎯 Quick-Start Checklist

### Prerequisites
- [ ] Access to `gmn_ontology.ttl`
- [ ] Access to `gmn_to_cidoc_transform.py`
- [ ] Understanding of CIDOC-CRM event-based modeling
- [ ] Familiarity with JSON-LD transformation patterns

### Implementation Steps
1. [ ] Add TTL definition to ontology file (5 minutes)
2. [ ] Add transformation function to Python script (10 minutes)
3. [ ] Register transformation in main pipeline (2 minutes)
4. [ ] Test with sample data (5 minutes)
5. [ ] Update documentation (optional)

**Total estimated time: ~25 minutes**

---

## 📋 Implementation Summary

### What This Property Does
The `gmn:P11i_3_has_spouse` property is a simplified shorthand for expressing spousal relationships between two persons through marriage events. It abstracts the complex CIDOC-CRM event-based structure into a simple person-to-person relationship.

### Semantic Structure
```
E21_Person (subject)
  └─ P11i_participated_in
      └─ E5_Event (marriage)
          ├─ P2_has_type → AAT:300055475 (marriages)
          └─ P11_had_participant → E21_Person (spouse)
```

### Key Features
- **Domain**: `cidoc:E21_Person`
- **Range**: `cidoc:E21_Person`
- **Auto-typed**: Marriage events automatically typed with AAT 300055475 (marriages)
- **Bidirectional**: Can express spouse relationships in either direction
- **Multi-value**: Supports multiple spouses (sequential or concurrent marriages)

### Files to Modify
1. **gmn_ontology.ttl** - Add property definition
2. **gmn_to_cidoc_transform.py** - Add transformation function and registration

---

## 🚀 Quick Implementation Guide

### 1. Add to Ontology (gmn_ontology.ttl)
Copy the TTL snippet from `has-spouse-ontology.ttl` and paste it into your ontology file in the appropriate section (around line 300-400, near other P11i properties).

### 2. Add to Transformation Script (gmn_to_cidoc_transform.py)
Copy the function from `has-spouse-transform.py` and:
- Paste the function definition after other P11i transformation functions
- Add the function call to the `transform_item()` pipeline

### 3. Test
```python
# Test data
test_person = {
    "@id": "person:123",
    "@type": "cidoc:E21_Person",
    "gmn:P11i_3_has_spouse": [
        {
            "@id": "person:456",
            "@type": "cidoc:E21_Person"
        }
    ]
}

# Expected output includes:
# cidoc:P11i_participated_in → E5_Event → P2_has_type → AAT:300055475
#                            → E5_Event → P11_had_participant → person:456
```

---

## 📚 Documentation Structure

### has-spouse-implementation-guide.md
Detailed step-by-step instructions including:
- Exact file locations and line numbers
- Complete code snippets
- Testing procedures
- Troubleshooting tips

### has-spouse-documentation.md
Complete semantic documentation including:
- Formal property definition
- CIDOC-CRM mapping explanation
- Usage examples
- Design rationale

### has-spouse-doc-note.txt
Ready-to-paste text for main documentation including:
- Property table entry
- Usage examples
- Transformation rules

---

## ⚠️ Important Notes

### Automatic Typing
Marriage events are automatically typed with AAT 300055475 (marriages). No manual type assignment required.

### URI Generation
Event URIs are generated using a hash of the spouse URI + "marriage" to ensure consistency and uniqueness:
```python
event_hash = str(hash(spouse_uri + 'marriage'))[-8:]
event_uri = f"{subject_uri}/event/marriage_{event_hash}"
```

### Multiple Spouses
The property supports multiple values to represent:
- Sequential marriages (remarriage after death or divorce)
- Concurrent marriages (in historical contexts where polygamy occurred)

### Data Quality
- Always use proper URIs for spouse references
- Ensure spouse entities exist in your dataset
- Consider adding inverse relationships for bidirectional modeling

---

## 🔗 Related Properties

This property is part of the GMN simplified property family for person attestations and relationships:

- **gmn:P11i_1_earliest_attestation_date** - Earliest documented existence
- **gmn:P11i_2_latest_attestation_date** - Latest documented existence
- **gmn:P11i_3_has_spouse** - Marriage relationships (this property)
- **gmn:P96_1_has_mother** - Maternal relationship
- **gmn:P97_1_has_father** - Paternal relationship

---

## 📖 Additional Resources

- **CIDOC-CRM**: http://www.cidoc-crm.org/
- **AAT Marriage**: http://vocab.getty.edu/aat/300055475
- **Project Documentation**: See main GMN documentation for complete context

---

## ✅ Validation Checklist

After implementation, verify:
- [ ] TTL validates without syntax errors
- [ ] Transformation function handles all input formats
- [ ] Generated URIs are consistent and unique
- [ ] Marriage events are properly typed
- [ ] Multiple spouses are correctly processed
- [ ] Output JSON-LD is valid and complete

---

## 🆘 Support

For questions or issues:
1. Review the implementation guide for troubleshooting tips
2. Check the documentation for usage examples
3. Verify your input data format matches examples
4. Consult CIDOC-CRM documentation for semantic questions

---

**Version**: 1.0  
**Date**: 2025-10-27  
**Property**: gmn:P11i_3_has_spouse  
**Status**: Ready for implementation
