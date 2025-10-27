# GMN Ontology: P53.1 Has Occupant Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P53_1_has_occupant` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **has-occupant-implementation-guide.md** - Step-by-step implementation instructions
3. **has-occupant-documentation.md** - Complete semantic documentation
4. **has-occupant-ontology.ttl** - TTL snippets for the ontology file
5. **has-occupant-transform.py** - Python code for the transformation script
6. **has-occupant-doc-note.txt** - Examples and tables for documentation

---

## 🎯 Quick Start Checklist

### Phase 1: Ontology Definition
- [ ] Add TTL definition to `gmn_ontology.ttl`
- [ ] Verify domain (gmn:E22_1_Building) and range (cidoc:E21_Person)
- [ ] Confirm subproperty relationship to `cidoc:P53i_is_former_or_current_location_of`

### Phase 2: Transformation Script
- [ ] Add `transform_p53_1_has_occupant()` function to transformation script
- [ ] Add function call in `transform_item()` pipeline
- [ ] Test with sample data

### Phase 3: Documentation
- [ ] Add property description to main documentation
- [ ] Include usage examples
- [ ] Document transformation pattern

### Phase 4: Testing & Validation
- [ ] Test with single occupant
- [ ] Test with multiple occupants
- [ ] Validate CIDOC-CRM compliance
- [ ] Verify JSON-LD output structure

---

## 📋 Implementation Summary

### Property Overview
**Name:** `gmn:P53_1_has_occupant`  
**Label:** "P53.1 has occupant"  
**Purpose:** Simplified property for expressing occupation/residence in a building by a person who is not the owner

### Semantic Path
The property represents a simplified CIDOC-CRM relationship:
- **Shortcut:** Building → has occupant → Person
- **Full Path:** Building → P53_has_former_or_current_location → Person

**Note:** The ontology comment describes a more detailed path through E9_Move events, but the current implementation uses the simplified direct relationship for practical data entry purposes.

### Domain and Range
- **Domain:** `gmn:E22_1_Building` (buildings and built structures)
- **Range:** `cidoc:E21_Person` (occupant persons)

### Key Distinctions
- **Occupancy vs. Ownership:** This property captures residence/occupation, distinct from ownership (use `gmn:P22_1_has_owner` for ownership)
- **Multiple Occupants:** Buildings can have multiple occupants over time or simultaneously
- **Non-owner Residence:** Specifically for residents who are not the property owners

---

## 🔄 Transformation Pattern

### Input (GMN Shortcut)
```json
{
  "@id": "building123",
  "@type": "gmn:E22_1_Building",
  "gmn:P53_1_has_occupant": [
    {"@id": "person456", "@type": "cidoc:E21_Person"}
  ]
}
```

### Output (CIDOC-CRM Compliant)
```json
{
  "@id": "building123",
  "@type": "gmn:E22_1_Building",
  "cidoc:P53_has_former_or_current_location": [
    {"@id": "person456", "@type": "cidoc:E21_Person"}
  ]
}
```

---

## 📚 Related Properties

- **gmn:P22_1_has_owner** - For property ownership relationships
- **cidoc:P53i_is_former_or_current_location_of** - Parent property
- **cidoc:P74_has_current_or_former_residence** - Alternative person-centric property

---

## 🚀 Quick Implementation

1. **Copy TTL definition** from `has-occupant-ontology.ttl` to your ontology file
2. **Copy Python function** from `has-occupant-transform.py` to your transformation script
3. **Add function call** to the transformation pipeline
4. **Test** with sample building data
5. **Document** in your project documentation using examples from `has-occupant-doc-note.txt`

---

## ⚠️ Important Notes

- This is a **simplified property** for data entry convenience
- The property is **automatically transformed** to full CIDOC-CRM structure
- **Distinct from ownership** - use separate properties for ownership vs. occupation
- Supports **multiple occupants** (array/list format)
- The transformation maintains **CIDOC-CRM semantic compliance**

---

## 📖 Additional Resources

For detailed implementation instructions, see **has-occupant-implementation-guide.md**  
For complete semantic documentation, see **has-occupant-documentation.md**

---

**Created:** 2025-10-27  
**Property ID:** gmn:P53_1_has_occupant  
**CIDOC-CRM Version:** 7.1.1
