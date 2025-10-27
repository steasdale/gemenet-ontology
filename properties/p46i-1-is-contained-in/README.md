# GMN Ontology: P46i.1 Is Contained In Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P46i_1_is_contained_in` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **is-contained-in-implementation-guide.md** - Step-by-step implementation instructions
3. **is-contained-in-documentation.md** - Complete semantic documentation
4. **is-contained-in-ontology.ttl** - TTL snippets for ontology file
5. **is-contained-in-transform.py** - Python code for transformation script
6. **is-contained-in-doc-note.txt** - Documentation additions

---

## 🎯 Quick Start

### Implementation Checklist

- [ ] **Review semantic documentation** (`is-contained-in-documentation.md`)
- [ ] **Add TTL definition** to `gmn_ontology.ttl` (already present in current ontology)
- [ ] **Add Python transformation** to `gmn_to_cidoc_transform.py`
- [ ] **Test with sample data**
- [ ] **Update main documentation** with content from `is-contained-in-doc-note.txt`
- [ ] **Validate CIDOC-CRM compliance**

### Estimated Implementation Time
- **Ontology addition**: Already complete ✓
- **Python implementation**: 15-20 minutes
- **Testing**: 10-15 minutes
- **Documentation**: 5-10 minutes
- **Total**: ~30-45 minutes

---

## 📋 Property Overview

### Basic Information

| Attribute | Value |
|-----------|-------|
| **Property URI** | `gmn:P46i_1_is_contained_in` |
| **Label** | "P46i.1 is contained in" |
| **Domain** | `cidoc:E31_Document` |
| **Range** | `cidoc:E78_Curated_Holding` |
| **Superproperty** | `cidoc:P46i_forms_part_of` |
| **Transformation** | Direct property mapping (no intermediate nodes) |

### Purpose

This property provides a simplified way to express that a document forms part of a larger archival unit or collection. It is used to link individual contracts to:
- Registers (E31_Document subtype)
- Filze (bundles of contracts tied with string)
- Folders
- Institutional archives
- Other archival containers

This captures the archival context and provenance of individual documents.

---

## 🔄 Transformation Pattern

### Shortcut (Input)
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    gmn:P46i_1_is_contained_in <register_1450> .
```

### CIDOC-CRM (Output)
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    cidoc:P46i_forms_part_of <register_1450> .
```

**Key Point**: This is a **direct mapping** - the property is simply replaced with its CIDOC-CRM equivalent. No intermediate nodes or additional structures are created.

---

## 🎓 Use Cases

### Common Scenarios

1. **Register Collections**
   - Individual contracts within notarial registers
   - Each document linked to its parent register

2. **Archival Bundles (Filze)**
   - Contracts grouped and tied together
   - Physical organization preservation

3. **Institutional Archives**
   - Documents within organizational collections
   - Provenance tracking

4. **Folder Systems**
   - Modern archival organization
   - Administrative groupings

---

## 📊 Implementation Status

### Current Status
- ✅ **Ontology Definition**: Complete (in gmn_ontology.ttl)
- ⚠️ **Python Transformation**: Needs implementation
- ⚠️ **Documentation**: Needs addition to main docs
- ⚠️ **Testing**: Pending

### Next Steps
1. Review the implementation guide
2. Add transformation function to Python script
3. Test with sample data
4. Update documentation

---

## 🔗 Related Properties

| Property | Relationship |
|----------|-------------|
| `cidoc:P46i_forms_part_of` | Parent property (CIDOC-CRM) |
| `gmn:P94i_3_has_place_of_enactment` | Different: document creation location |
| `cidoc:P55_has_current_location` | Different: current physical location |

---

## 📖 Documentation Structure

### For Implementers
→ Start with **is-contained-in-implementation-guide.md**

### For Ontology Designers
→ Start with **is-contained-in-documentation.md**

### For Developers
→ Use **is-contained-in-transform.py** directly

### For Documentation Writers
→ Use **is-contained-in-doc-note.txt** for copy-paste content

---

## ⚠️ Important Notes

1. **Direct Mapping**: Unlike many GMN shortcut properties, this one does NOT create intermediate nodes. It's a simple 1:1 property replacement.

2. **Range Flexibility**: The range `E78_Curated_Holding` is broad and includes many types of archival units. This allows flexibility in modeling different archival contexts.

3. **Multiple Containment**: A document can theoretically be contained in multiple archival units (many-to-many relationship).

4. **Preservation Context**: This property is crucial for tracking documentary provenance and archival context.

---

## 🤝 Support

For questions or issues with this property implementation, refer to:
- Complete semantic documentation in `is-contained-in-documentation.md`
- Step-by-step guide in `is-contained-in-implementation-guide.md`
- CIDOC-CRM documentation: http://www.cidoc-crm.org/

---

## 📅 Version Information

- **Package Created**: 2025-10-27
- **Ontology Version**: GMN Ontology v1.0
- **CIDOC-CRM Version**: 7.1.x compatible
- **Property Status**: Defined in ontology, transformation pending

---

**Ready to implement?** Start with the implementation guide! 🚀
