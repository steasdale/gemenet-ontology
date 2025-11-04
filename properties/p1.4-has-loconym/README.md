# gmn:P1_4_has_loconym - Deliverables Package

**Property Name:** `gmn:P1_4_has_loconym` (P1.4 has loconym)  
**Property Type:** Object Property (owl:ObjectProperty)  
**Status:** ALREADY IMPLEMENTED - No new code needed

---

##  Quick-Start Checklist

###  Implementation Status

- [x] **Ontology Definition** - Already exists in `gmn_ontology.ttl`
- [x] **Python Transformation** - Already exists in `gmn_to_cidoc_transform.py`
- [ ] **Documentation** - Add usage examples to project documentation (see `has-loconym-doc-note.txt`)
- [ ] **Testing** - Test transformation with sample data (see Implementation Guide)

###  What This Package Provides

Since this property is **already fully implemented**, this package provides:

1. **Documentation** - Complete semantic and technical documentation
2. **Reference Materials** - Current ontology definition and transformation code
3. **Usage Examples** - Practical examples for data entry and transformation
4. **Testing Guide** - Instructions for validating the existing implementation

### ⚠️ Important Note

**No code changes are required.** The `gmn:P1_4_has_loconym` property is already defined in your ontology and the transformation function already exists in your Python script. This package documents the existing implementation and provides usage guidance.

---

## 📦 Package Contents

### 1. README.md (This File)
Complete overview and quick-start guide.

### 2. has-loconym-implementation-guide.md
Step-by-step guide for:
- Understanding the current implementation
- Using the property in data entry
- Testing the transformation
- Troubleshooting common issues

### 3. has-loconym-documentation.md
Complete semantic documentation:
- Property definition and semantics
- CIDOC-CRM path specification
- Transformation examples
- Usage patterns and best practices

### 4. has-loconym-ontology.ttl
Reference copy of the existing TTL definition from `gmn_ontology.ttl` (no additions needed).

### 5. has-loconym-transform.py
Reference copy of the existing Python transformation function from `gmn_to_cidoc_transform.py` (no additions needed).

### 6. has-loconym-doc-note.txt
Documentation additions with examples and tables to add to your project's main documentation file.

---

## 🎯 Purpose and Use Case

### What is a Loconym?

A **loconym** is a place-based name component that indicates that a person or their ancestors originated from a particular place. This toponymic naming pattern was common in medieval Italian contexts.

**Examples:**
- "Giovanni **da Genova**" (Giovanni from Genoa)
- "Bartolomeo **de Vignolo**" (Bartolomeo from Vignolo)
- "Maria **da Venezia**" (Maria from Venice)

The place reference (Genova, Vignolo, Venezia) is the loconym component.

### Why Use This Property?

The `gmn:P1_4_has_loconym` property:

1. **Simplifies Data Entry** - Direct link from person to place (E21_Person → E53_Place)
2. **Captures Geographic Origin** - Documents regional provenance embedded in names
3. **Enables Place-Based Analysis** - Facilitates queries about geographic origins
4. **Maintains Semantic Rigor** - Transforms to full CIDOC-CRM compliant structure

---

## 🔄 Transformation Overview

### Input Format (Simplified)
```turtle
<person_bartolomeo> a cidoc:E21_Person ;
    gmn:P1_4_has_loconym <place_vignolo> .
```

### Output Format (CIDOC-CRM Compliant)
```turtle
<person_bartolomeo> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <person_bartolomeo/appellation/loconym_12345678> .

<person_bartolomeo/appellation/loconym_12345678> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <https://www.wikidata.org/wiki/Q17143070> ;
    cidoc:P67_refers_to <place_vignolo> .

<place_vignolo> a cidoc:E53_Place .
```

### CIDOC-CRM Path
```
E21_Person 
  → P1_is_identified_by 
    → E41_Appellation 
      → P2_has_type → <https://www.wikidata.org/wiki/Q17143070> (loconym)
      → P67_refers_to → E53_Place
```

---

## 🚀 Getting Started

### For New Users

1. **Read the Documentation** - Start with `has-loconym-documentation.md` to understand the property semantics
2. **Review Examples** - See `has-loconym-doc-note.txt` for practical usage patterns
3. **Test Implementation** - Follow testing procedures in `has-loconym-implementation-guide.md`

### For Existing Users

1. **Verify Current Usage** - Check your data for existing uses of `gmn:P1_4_has_loconym`
2. **Add Documentation** - Incorporate examples from `has-loconym-doc-note.txt` into your project docs
3. **Test Transformation** - Validate that transformations work correctly with your data

---

## 📊 Implementation Summary

### Current Status

| Component | Status | Location |
|-----------|--------|----------|
| Ontology Definition | ✅ Implemented | `gmn_ontology.ttl` line 183-196 |
| Transformation Function | ✅ Implemented | `gmn_to_cidoc_transform.py` line 154-186 |
| Documentation | ⚠️ Needs Enhancement | Add from `has-loconym-doc-note.txt` |
| Testing | 📋 To Do | Follow Implementation Guide |

### Property Specification

- **Domain:** `cidoc:E21_Person` - Applied to persons
- **Range:** `cidoc:E53_Place` - References places
- **Type:** Object Property (links to place resources)
- **Implicit Type:** Wikidata Q17143070 (loconym)
- **Created:** 2025-10-16

### Key Features

1. **Wikidata Integration** - Uses Wikidata Q17143070 for loconym type
2. **Place Reference** - Direct semantic link to place entities (P67_refers_to)
3. **Appellation Structure** - Creates proper E41_Appellation intermediary
4. **Automatic Typing** - Transformation automatically sets loconym type

---

## 🔗 Related Properties

### Name Properties (P1.x)
- `gmn:P1_1_has_name` - General cataloging/display name
- `gmn:P1_2_has_name_from_source` - Name as found in historical source
- `gmn:P1_3_has_patrilineal_name` - Patronymic ancestry (e.g., "Giacomo q. Antonio")
- **`gmn:P1_4_has_loconym`** - Place-based name component (this property)

### Provenance Properties
- `gmn:P107i_1_has_regional_provenance` - General regional group membership
- `gmn:P94i_3_has_place_of_enactment` - Document creation place (not person origin)

### Differences

| Property | Purpose | Example |
|----------|---------|---------|
| `P1_4_has_loconym` | Place in person's **name** | "Giovanni **da Genova**" |
| `P107i_1_has_regional_provenance` | Person's **regional group** | Genoese merchants |
| `P94i_3_has_place_of_enactment` | **Document** creation place | Contract signed in Genoa |

---

## ⚙️ Technical Details

### Ontology Declaration
```turtle
gmn:P1_4_has_loconym
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P1.4 has loconym"@en ;
    rdfs:subPropertyOf cidoc:P1_is_identified_by ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E53_Place ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P1_is_identified_by, cidoc:P67_refers_to, 
                 <https://www.wikidata.org/wiki/Q17143070> ;
    gmn:hasImplicitType <https://www.wikidata.org/wiki/Q17143070> .
```

### Python Transformation
```python
def transform_p1_4_has_loconym(data):
    """
    Transform gmn:P1_4_has_loconym to full CIDOC-CRM structure:
    P1_is_identified_by > E41_Appellation > P2_has_type (loconym) > P67_refers_to > E53_Place
    """
    # Function already exists in gmn_to_cidoc_transform.py
    # See has-loconym-transform.py for complete code
```

---

## 📚 Additional Resources

### Internal Documentation
- `gmn_ontology.ttl` - Main ontology file (lines 183-196)
- `gmn_to_cidoc_transform.py` - Transformation script (lines 154-186)
- Project documentation files referenced in package

### External Standards
- [CIDOC-CRM](https://www.cidoc-crm.org/) - Core ontology reference
- [Wikidata Q17143070](https://www.wikidata.org/wiki/Q17143070) - Loconym definition
- [Getty AAT](https://www.getty.edu/research/tools/vocabularies/aat/) - Art & Architecture Thesaurus

### Related Packages
- `has-name-from-source` deliverables - Name from historical sources
- `has-patrilineal-name` deliverables - Patronymic names
- `has-regional-provenance` deliverables - Regional group membership

---

## 🤝 Support and Contact

### Questions About This Property?
- Review the Implementation Guide for step-by-step instructions
- Check the Documentation file for semantic details
- Examine examples in the doc-note file

### Issues or Enhancements?
- Document any issues found during testing
- Suggest improvements based on practical usage
- Share examples of complex naming patterns

---

## 📄 License and Attribution

This deliverables package documents the GMN ontology `has_loconym` property implementation.

**Created:** October 2025  
**Version:** 1.0  
**Status:** Implementation Complete - Documentation Package

---

## 🎓 Learning Path

### Beginner
1. Read "Purpose and Use Case" section above
2. Review simple examples in `has-loconym-doc-note.txt`
3. Understand transformation overview (this file)

### Intermediate
1. Study full documentation in `has-loconym-documentation.md`
2. Examine ontology definition in `has-loconym-ontology.ttl`
3. Review transformation code in `has-loconym-transform.py`

### Advanced
1. Follow implementation guide for testing
2. Explore edge cases and complex scenarios
3. Integrate with related properties (P107i_1, P1_3, etc.)

---

**End of README**
