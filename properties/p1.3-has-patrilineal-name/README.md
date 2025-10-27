# P1.3 Has Patrilineal Name - Implementation Package

## Overview

This package contains all necessary documentation and code to implement the `gmn:P1_3_has_patrilineal_name` property in the Genoese Merchant Networks (GMN) ontology and transformation system. This property provides a simplified way to capture patrilineal names (patronymic ancestry) for persons in medieval and early modern Italian contexts.

**Property URI:** `gmn:P1_3_has_patrilineal_name`  
**Version:** 1.0  
**Created:** 2025-10-17  
**Last Updated:** 2025-10-26

## What This Property Does

The `P1_3_has_patrilineal_name` property captures the full patronymic naming pattern common in medieval Italian sources, where a person's name includes their given name followed by their patronymic ancestry. Examples include:

- "Giacomo Spinola q. Antonio" (Giacomo Spinola, son of the late Antonio)
- "Giovanni Doria q. Luca" (Giovanni Doria, son of the late Luca)
- "Bartolomeo de Serra q. Nicolò" (Bartolomeo de Serra, son of the late Nicolò)

The abbreviation "q." (quondam) indicates a deceased father or ancestor.

## Semantic Representation

This property is a **shortcut property** that simplifies data entry. Behind the scenes, it transforms to the full CIDOC-CRM structure:

```
E21_Person
  └─ P1_is_identified_by
      └─ E41_Appellation
          ├─ P2_has_type → AAT:300404651 (patronymic)
          └─ P190_has_symbolic_content → "name string"
```

## Quick-Start Checklist

Follow these steps to implement the has patrilineal property:

- [ ] **Step 1**: Review the ontology documentation (`has-patrilineage-documentation.md`)
- [ ] **Step 2**: Add TTL definitions to `gmn_ontology.ttl` (from `has-patrilineage-ontology.ttl`)
- [ ] **Step 3**: Add Python transformation code to `gmn_to_cidoc_transform.py` (from `has-patrilineage-transform.py`)
- [ ] **Step 4**: Test the implementation with sample data
- [ ] **Step 5**: Validate RDF output
- [ ] **Step 6**: Update Omeka-S resource templates
- [ ] **Step 7**: Add documentation examples (from `has-patrilineage-doc-note.txt`)

## Package Contents

### 1. README.md (this file)
Complete overview, quick-start checklist, and implementation summary.

### 2. has-patrilineage-implementation-guide.md
Step-by-step instructions for implementing all changes, including:
- Detailed implementation procedures
- Code integration instructions
- Testing and validation steps
- Troubleshooting guidelines

### 3. has-patrilineage-documentation.md
Complete semantic documentation including:
- Property definition and specification
- CIDOC-CRM mapping details
- Transformation examples
- Use cases and patterns

### 4. has-patrilineage-ontology.ttl
Ready-to-copy TTL snippets for the main ontology file, including:
- Property definition
- OWL restrictions
- Metadata annotations

### 5. has-patrilineage-transform.py
Ready-to-copy Python code for the transformation script, including:
- Transformation function
- Helper functions
- Integration points

### 6. has-patrilineage-doc-note.txt
Examples and tables to add to the main documentation, including:
- Usage examples
- Common patterns
- Best practices

## Key Features

### Simplified Data Entry
Instead of creating complex CIDOC-CRM structures manually, data entry personnel can use the simple shortcut:

```turtle
<person001> a cidoc:E21_Person ;
    gmn:P1_3_has_patrilineal_name "Giacomo Spinola q. Antonio" .
```

### Automatic Transformation
The transformation script automatically expands this to full CIDOC-CRM compliance:

```turtle
<person001> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <person001_appellation_patrilineal> .

<person001_appellation_patrilineal> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404651> ;
    cidoc:P190_has_symbolic_content "Giacomo Spinola q. Antonio" .

<http://vocab.getty.edu/page/aat/300404651> a cidoc:E55_Type .
```

### Standards Compliance
- Full CIDOC-CRM compatibility
- Uses Getty AAT controlled vocabulary (AAT:300404651 for patronymics)
- Follows GMN ontology patterns and conventions

## Implementation Context

This property is part of a family of name properties in the GMN ontology:

- **P1.1** has name (general names)
- **P1.2** has name from source (names exactly as written in source)
- **P1.3** has patrilineal name ← THIS PROPERTY
- **P1.4** has loconym (place-based names)

All use the same transformation pattern but with different AAT type identifiers.

## Technical Details

### Property Type
- **OWL Type**: `owl:DatatypeProperty`
- **RDF Type**: `rdf:Property`
- **Super-property**: `cidoc:P1_is_identified_by`
- **Domain**: `cidoc:E21_Person`
- **Range**: `cidoc:E62_String`

### AAT Type
- **URI**: `http://vocab.getty.edu/page/aat/300404651`
- **Label**: "patronymics"
- **Scope**: Names derived from father's or ancestor's name

### Implementation Status

✅ **Ontology Definition**: Complete (added 2025-10-17)  
✅ **Transformation Code**: Complete (added 2025-10-17)  
⚠️ **Documentation**: Needs expansion  
⚠️ **Testing**: Requires validation with production data  
❌ **Omeka-S Templates**: Not yet configured

## Support and Resources

### Related Documentation
- Main GMN Ontology: `/mnt/project/gmn_ontology.ttl`
- Transformation Script: `/mnt/project/gmn_to_cidoc_transform.py`
- CIDOC-CRM Specification: http://www.cidoc-crm.org/
- Getty AAT: http://www.getty.edu/research/tools/vocabularies/aat/

### Common Issues

**Issue**: Property not transforming correctly  
**Solution**: Verify that the property name matches exactly: `gmn:P1_3_has_patrilineal_name`

**Issue**: AAT type not resolving  
**Solution**: Ensure AAT constant is defined: `AAT_PATRONYMIC = "http://vocab.getty.edu/page/aat/300404651"`

**Issue**: Multiple appellations per person  
**Solution**: This is expected - a person can have multiple types of appellations (name, patronymic, loconym)

## Next Steps After Implementation

1. **Test with Sample Data**: Use historical records from Genoese notarial documents
2. **Validate Transformations**: Ensure output matches CIDOC-CRM specifications
3. **Update User Training**: Document the new property for data entry personnel
4. **Configure Omeka-S**: Add the property to relevant resource templates
5. **Create Examples**: Build a reference collection of correctly formatted entries

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-17 | Initial property creation in ontology and transform script |
| 1.1 | 2025-10-26 | Documentation package created |

## Contact

For questions about this implementation:
- Ontology issues: Review CIDOC-CRM documentation
- Transformation issues: Check Python transformation script
- Data entry questions: Refer to implementation guide

---

**Package Created**: 2025-10-26  
**For**: Genoese Merchant Networks Project  
**Property**: gmn:P1_3_has_patrilineal_name
