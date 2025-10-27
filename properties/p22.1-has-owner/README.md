# GMN Ontology: P22.1 Has Owner Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P22_1_has_owner` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **has-owner-implementation-guide.md** - Step-by-step implementation instructions
3. **has-owner-documentation.md** - Complete semantic documentation
4. **has-owner-ontology.ttl** - TTL snippets for main ontology file
5. **has-owner-transform.py** - Python code for transformation script
6. **has-owner-doc-note.txt** - Examples and tables for documentation

---

## 🎯 Quick Start

### What is P22.1?

`gmn:P22_1_has_owner` is a simplified property for expressing ownership of buildings or moveable property by a person. It represents the full CIDOC-CRM path:

```
E22_Human-Made_Object 
  → P24i_changed_ownership_through 
    → E8_Acquisition 
      → P22_transferred_title_to 
        → E21_Person
```

### Key Features

- **Domain**: `cidoc:E22_Human-Made_Object` (buildings and moveable property)
- **Range**: `cidoc:E21_Person`
- **Subproperty of**: `cidoc:P24i_changed_ownership_through`
- **Creates**: E8_Acquisition event for each ownership relationship
- **Applies to**: Both `gmn:E22_1_Building` and `gmn:E22_2_Moveable_Property`

---

## ✅ Implementation Checklist

### Phase 1: Ontology Update
- [ ] Add P22.1 property definition to `gmn_ontology.ttl`
- [ ] Verify property label and comment
- [ ] Check domain and range restrictions
- [ ] Confirm subproperty relationship
- [ ] Validate with Protégé or other RDF validator

### Phase 2: Transformation Script
- [ ] Add `transform_p22_1_has_owner()` function to `gmn_to_cidoc_transform.py`
- [ ] Add function call to `transform_item()` pipeline
- [ ] Test with sample data
- [ ] Verify URI generation logic
- [ ] Confirm acquisition event structure

### Phase 3: Documentation
- [ ] Add property description to main documentation
- [ ] Include usage examples
- [ ] Add transformation examples
- [ ] Update property reference table
- [ ] Document relationship to related properties

### Phase 4: Testing
- [ ] Test with single owner
- [ ] Test with multiple owners
- [ ] Test with building ownership
- [ ] Test with moveable property ownership
- [ ] Verify URI uniqueness across multiple owners
- [ ] Check roundtrip conversion

---

## 📊 Quick Reference

### Input Format (Shortcut)
```turtle
<building001> a gmn:E22_1_Building ;
    gmn:P22_1_has_owner <person_giovanni> , <person_francesco> .
```

### Output Format (CIDOC-CRM)
```turtle
<building001> a gmn:E22_1_Building ;
    cidoc:P24i_changed_ownership_through 
        <building001/acquisition/ownership_a1b2c3d4> ,
        <building001/acquisition/ownership_e5f6g7h8> .

<building001/acquisition/ownership_a1b2c3d4> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to <person_giovanni> .

<building001/acquisition/ownership_e5f6g7h8> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to <person_francesco> .
```

---

## 🔍 Common Use Cases

1. **Building Ownership**: Documenting owners of houses, shops, warehouses, etc.
2. **Property Records**: Linking property ownership to specific persons
3. **Multiple Owners**: Expressing joint or co-ownership scenarios
4. **Historical Reconstruction**: Building ownership networks and patterns

---

## 🔗 Related Properties

- **P53.1 Has Occupant** (`gmn:P53_1_has_occupant`) - For residence/occupation (not ownership)
- **P70.1 Documents Seller** (`gmn:P70_1_documents_seller`) - For sellers in sales contracts
- **P70.2 Documents Buyer** (`gmn:P70_2_documents_buyer`) - For buyers in sales contracts
- **P70.3 Documents Transfer Of** (`gmn:P70_3_documents_transfer_of`) - For property being transferred

---

## 📝 Property Specification

| Aspect | Value |
|--------|-------|
| **Property IRI** | `gmn:P22_1_has_owner` |
| **Label** | "P22.1 has owner"@en |
| **Subproperty of** | `cidoc:P24i_changed_ownership_through` |
| **Domain** | `cidoc:E22_Human-Made_Object` |
| **Range** | `cidoc:E21_Person` |
| **Created** | 2025-10-16 |
| **Type** | ObjectProperty |

---

## 🎓 Understanding the Transformation

### Why Use E8_Acquisition?

The transformation creates an E8_Acquisition event to properly model ownership in CIDOC-CRM:

1. **Event-Based Modeling**: CIDOC-CRM models relationships through events
2. **Temporal Context**: Acquisitions can have time-spans (when ownership was acquired)
3. **Rich Context**: Can be expanded with location, witnesses, payment details, etc.
4. **Standards Compliance**: Follows CIDOC-CRM best practices for ownership modeling

### URI Generation Strategy

Each ownership relationship gets a unique acquisition URI:
- Base: Object URI + `/acquisition/ownership_`
- Hash: Last 8 characters of hash(owner_uri + 'ownership')
- Example: `<building001/acquisition/ownership_a1b2c3d4>`

This ensures:
- Unique URIs for each owner-object pair
- Consistent URIs across transformations
- Collision resistance for multiple owners

---

## ⚠️ Important Notes

### Distinction from Occupation

- **P22.1 (Has Owner)**: Legal ownership of property
- **P53.1 (Has Occupant)**: Physical residence/occupation without ownership
- These are **different relationships** and should not be confused

### Applies to Human-Made Objects Only

This property is specifically for:
- Buildings (`gmn:E22_1_Building`)
- Moveable property (`gmn:E22_2_Moveable_Property`)

Do not use for:
- Land parcels (use appropriate land ownership properties)
- Natural features
- Abstract concepts

### Multiple Owners

When multiple owners are specified, each gets their own E8_Acquisition event. This allows for:
- Different acquisition dates per owner (if data available)
- Different ownership contexts
- Independent modeling of each ownership relationship

---

## 📚 Additional Resources

For complete implementation details, see:
- **has-owner-implementation-guide.md** - Full step-by-step instructions
- **has-owner-documentation.md** - Complete semantic documentation
- **has-owner-ontology.ttl** - Ready-to-copy TTL snippets
- **has-owner-transform.py** - Ready-to-copy Python code
- **has-owner-doc-note.txt** - Documentation additions

---

## 🤝 Support

For questions or issues:
1. Consult the detailed implementation guide
2. Review the semantic documentation
3. Check the transformation examples
4. Verify against test cases in the guide

---

## 📄 License

This documentation is part of the GMN Ontology project.

---

**Last Updated**: October 2025  
**Version**: 1.0  
**Property**: gmn:P22_1_has_owner
