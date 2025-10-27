# GMN P3.1 has editorial note Property - Deliverables Package

**Property:** `gmn:P3_1_has_editorial_note`  
**Version:** 1.0  
**Date:** October 26, 2025  
**Property Type:** Internal Documentation Property (DatatypeProperty)  
**Status:** ✅ ALREADY IMPLEMENTED - No new code needed

---

## Overview

This deliverables package contains all necessary documentation and code for implementing the `gmn:P3_1_has_editorial_note` property in the Genoese Merchant Networks (GMN) ontology. This property provides a simplified way to add editorial notes, comments, and internal documentation to any entity in the database and automatically transforms to full CIDOC-CRM compliant structure.

**Important:** This property is marked as **internal-only** and should typically be **excluded from public data exports**. The transformation script supports an `--include-internal` flag to control whether editorial notes are transformed or removed.

## What's Included

This package contains six essential files:

1. **README.md** (this file) - Overview and quick-start guide
2. **has-editorial-note-implementation-guide.md** - Step-by-step implementation instructions
3. **has-editorial-note-documentation.md** - Complete semantic documentation
4. **has-editorial-note-ontology.ttl** - TTL snippets for the ontology file
5. **has-editorial-note-transform.py** - Python code for the transformation script
6. **has-editorial-note-doc-note.txt** - Documentation additions for the main text file

---

## Quick-Start Checklist

### ✅ Implementation Status

Since this property is **already fully implemented**, use this checklist to verify:

- [x] **Ontology Definition** - Already exists in `gmn_ontology.ttl`
- [x] **Python Transformation** - Already exists in `gmn_to_cidoc_transform.py`
- [ ] **Documentation** - Add usage examples to project documentation (see `has-editorial-note-doc-note.txt`)
- [ ] **Testing** - Test transformation with sample data (see Implementation Guide)
- [ ] **Internal Use Policy** - Establish guidelines for when to use editorial notes

### 📝 Recommended Actions

1. **Review Documentation** - Read through this package to understand the property fully
2. **Test Transformation** - Run transformation tests with both `--include-internal` and without
3. **Update Project Docs** - Add examples from `has-editorial-note-doc-note.txt` to main documentation
4. **Establish Policies** - Create internal guidelines for editorial note usage

---

## Implementation Summary

### Property Specification

**Property URI:** `gmn:P3_1_has_editorial_note`  
**Label:** "P3.1 has editorial note"@en  
**Type:** `owl:DatatypeProperty`  
**Subproperty of:** `cidoc:P3_has_note`  
**Domain:** `cidoc:E1_CRM_Entity` (can be applied to any entity)  
**Range:** `cidoc:E62_String`  
**AAT Type:** `aat:300456627` (editorial notes)  
**Internal Only:** `true` (gmn:isInternalOnly)

### CIDOC-CRM Transformation Pattern

The property transforms from:

```turtle
<entity> gmn:P3_1_has_editorial_note "This person appears in multiple contracts under different spellings." .
```

To the full CIDOC-CRM structure:

```turtle
<entity> cidoc:P67i_is_referred_to_by <entity/note/abc123> .
<entity/note/abc123> a cidoc:E33_Linguistic_Object ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300456627> ;
    cidoc:P190_has_symbolic_content "This person appears in multiple contracts under different spellings." .
```

### Key Features

1. **Universal Application** - Can be applied to any entity (E1_CRM_Entity domain)
2. **Internal Use** - Marked with `gmn:isInternalOnly true`
3. **Optional Inclusion** - Transform script supports `--include-internal` flag
4. **Type Safety** - AAT type (300456627) automatically applied during transformation
5. **Multiple Notes** - Multiple editorial notes can be applied to the same entity

---

## Usage Examples

### Example 1: Person Entity with Editorial Note

```json
{
  "@id": "http://example.org/person/giacomo_spinola_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [
    {"@value": "Giacomo Spinola q. Antonio"}
  ],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Name varies in sources between 'Giacomo' and 'Jacopo'. Identity confirmed through patronymic and property references."}
  ]
}
```

### Example 2: Contract with Editorial Note

```json
{
  "@id": "http://example.org/contract/sales_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P102_1_has_title": [
    {"@value": "Sale of House in Genoa"}
  ],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Partially damaged document. Sale price inferred from context. Requires verification with parallel sources."}
  ]
}
```

### Example 3: Place with Editorial Note

```json
{
  "@id": "http://example.org/place/vignolo",
  "@type": "cidoc:E53_Place",
  "gmn:P1_1_has_name": [
    {"@value": "Vignolo"}
  ],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Modern location: frazione of Serra Riccò, province of Genoa. Historical boundaries uncertain."}
  ]
}
```

---

## Transformation Behavior

### Public Export (Default)

```bash
python gmn_to_cidoc_transform.py input.json output.json
```

**Result:** Editorial notes are **removed** from the output to protect internal research notes.

### Internal/Full Export

```bash
python gmn_to_cidoc_transform.py input.json output.json --include-internal
```

**Result:** Editorial notes are **transformed** to full CIDOC-CRM structure:

```json
{
  "@id": "http://example.org/person/giacomo_spinola_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P67i_is_referred_to_by": [
    {
      "@id": "http://example.org/person/giacomo_spinola_001/note/12345678",
      "@type": "cidoc:E33_Linguistic_Object",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300456627",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Name varies in sources..."
    }
  ]
}
```

---

## Best Practices

### When to Use Editorial Notes

✅ **Good Uses:**
- Document uncertainties or ambiguities in source material
- Explain editorial decisions or interpretations
- Link to external research or verification sources
- Note discrepancies between multiple sources
- Record temporary working hypotheses
- Flag items requiring further research

❌ **Avoid Using For:**
- Public-facing annotations (use cidoc:P3_has_note directly)
- Bibliographic references (use proper citation properties)
- Content descriptions (use appropriate descriptive properties)
- Permanent scholarly annotations (consider cidoc:P70_documents)

### Editorial Note Guidelines

1. **Be Specific** - Clearly state the issue, uncertainty, or note
2. **Be Concise** - Keep notes brief but informative
3. **Date When Relevant** - Include dates for time-sensitive observations
4. **Use Consistent Language** - Develop standard phrasing for common situations
5. **Distinguish Facts from Interpretation** - Clearly mark interpretations as such

---

## File Descriptions

### 1. README.md (This File)
Complete overview, implementation status, usage examples, and best practices.

### 2. has-editorial-note-implementation-guide.md
Detailed step-by-step instructions for:
- Verifying existing implementation
- Testing the transformation
- Adding new editorial notes
- Troubleshooting common issues

### 3. has-editorial-note-documentation.md
Complete semantic documentation including:
- Formal property definition
- CIDOC-CRM alignment
- Transformation patterns
- Inference rules

### 4. has-editorial-note-ontology.ttl
Ready-to-copy TTL snippets for the main ontology file (already implemented, provided for reference).

### 5. has-editorial-note-transform.py
Ready-to-copy Python code for the transformation script (already implemented, provided for reference).

### 6. has-editorial-note-doc-note.txt
Tables and examples to add to main documentation files.

---

## Related Properties

`gmn:P3_1_has_editorial_note` is designed for internal use. For public annotations, consider:

- **cidoc:P3_has_note** - General notes property (parent property)
- **cidoc:P70_documents** - For documenting formal scholarly statements
- **cidoc:P67i_is_referred_to_by** - For references to external descriptions

---

## Technical Notes

### Dependencies
- **Python 3.6+** for transformation script
- **JSON-LD** support for data export/import
- **CIDOC-CRM** ontology
- **Getty AAT** vocabulary (specifically aat:300456627)

### URI Generation
Editorial note URIs are generated using the pattern:
```
{subject_uri}/note/{hash}
```
Where `{hash}` is the last 8 digits of a hash of the note content.

### Multiple Notes
Multiple editorial notes can be added to the same entity. Each will be transformed to a separate E33_Linguistic_Object.

---

## Support and Questions

For questions about this property or the GMN ontology in general:
- Review the implementation guide for troubleshooting
- Check the documentation file for semantic details
- Consult the main GMN ontology documentation

---

## Version History

**Version 1.0** (October 26, 2025)
- Initial deliverables package release
- Property already implemented in main ontology and transformation script
- Documentation created for reference and training

---

## License and Attribution

This deliverables package is part of the Genoese Merchant Networks (GMN) project.

**Property Definition:** gmn:P3_1_has_editorial_note  
**Created:** 2025-10-16  
**Package Version:** 1.0  
**Package Date:** October 26, 2025
