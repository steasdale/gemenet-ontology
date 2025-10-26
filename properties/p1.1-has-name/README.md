# GMN P1.1 has_name Property - Deliverables Package

**Property:** `gmn:P1_1_has_name`  
**Version:** 1.0  
**Date:** October 26, 2025  
**Property Type:** Simplified Datatype Property  
**Status:** Ready for Implementation

## Overview

This deliverables package contains all necessary documentation and code for implementing the `gmn:P1_1_has_name` property in the Genoese Merchant Networks (GMN) ontology. This property provides a simplified way to express names for any entity in the database and automatically transforms to full CIDOC-CRM compliant structure.

## What's Included

This package contains six essential files:

1. **README.md** (this file) - Overview and quick-start guide
2. **has-name-implementation-guide.md** - Step-by-step implementation instructions
3. **has-name-documentation.md** - Complete semantic documentation
4. **has-name-ontology.ttl** - Ready-to-copy TTL additions
5. **has-name-transform.py** - Ready-to-copy Python transformation code
6. **has-name-doc-note.txt** - Documentation examples and tables

## Quick Start Checklist

### Phase 1: Review Documentation (15 minutes)
- [ ] Read this README completely
- [ ] Review the implementation guide (has-name-implementation-guide.md)
- [ ] Review the semantic documentation (has-name-documentation.md)
- [ ] Understand the transformation pattern

### Phase 2: Backup Current System (10 minutes)
- [ ] Backup gmn_ontology.ttl
- [ ] Backup gmn_to_cidoc_transform.py
- [ ] Backup main documentation files
- [ ] Document current system state

### Phase 3: Update Ontology (10 minutes)
- [ ] Open gmn_ontology.ttl
- [ ] Locate the P1.1 has_name property definition (around line 280)
- [ ] Verify property is already present (created 2025-10-16, modified 2025-10-17)
- [ ] No changes needed unless updating version or comments
- [ ] Validate TTL syntax

### Phase 4: Verify Transformation Code (15 minutes)
- [ ] Open gmn_to_cidoc_transform.py
- [ ] Locate transform_p1_1_has_name function (around line 49)
- [ ] Verify AAT_NAME constant is defined (line 23)
- [ ] Verify function is in TRANSFORMERS list
- [ ] Code is already implemented - no changes needed
- [ ] Run syntax validation

### Phase 5: Test Implementation (30 minutes)
- [ ] Create test JSON-LD with gmn:P1_1_has_name
- [ ] Run transformation script
- [ ] Verify output structure
- [ ] Check appellation URI generation
- [ ] Validate AAT type assignment
- [ ] Test with multiple names

### Phase 6: Update Documentation (20 minutes)
- [ ] Add examples to main documentation
- [ ] Update property reference tables
- [ ] Document usage guidelines
- [ ] Add to training materials

### Phase 7: Deployment (varies)
- [ ] Deploy updated files to production
- [ ] Update Omeka-S resource templates
- [ ] Test in Omeka-S environment
- [ ] Train data entry staff
- [ ] Monitor for issues

## Key Features

### Universal Application
- **Domain:** `cidoc:E1_CRM_Entity` - Works with ANY entity type
- **Use Cases:** Persons, places, things, contracts, groups, concepts
- **Flexibility:** Single property for all naming needs

### Automatic Transformation
The property automatically transforms from:
```turtle
<entity> gmn:P1_1_has_name "Name String" .
```

To full CIDOC-CRM structure:
```turtle
<entity> cidoc:P1_is_identified_by <entity/appellation/12345678> .
<entity/appellation/12345678> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Name String" .
```

### AAT Integration
- Uses Getty AAT 300404650 (names) as the appellation type
- Ensures semantic consistency
- Enables vocabulary-based queries

## Implementation Summary

### Files to Update

1. **gmn_ontology.ttl** - Already contains the property definition (no changes needed)
2. **gmn_to_cidoc_transform.py** - Already contains transformation function (no changes needed)
3. **Documentation files** - May need examples and usage guidelines added

### Changes Required

**IMPORTANT:** The property and transformation code are ALREADY IMPLEMENTED in the current system. This deliverables package provides:
- Complete documentation for the existing property
- Usage examples and guidelines
- Testing procedures
- Training materials

### Testing Checklist

- [ ] Verify property definition in ontology
- [ ] Test transformation with sample data
- [ ] Validate output against CIDOC-CRM
- [ ] Test with multiple entity types (Person, Place, Contract, etc.)
- [ ] Check URI generation for uniqueness
- [ ] Verify AAT type assignment

## Property Specifications

| Attribute | Value |
|-----------|-------|
| **Property URI** | `gmn:P1_1_has_name` |
| **Label** | "P1.1 has name" |
| **Type** | owl:DatatypeProperty |
| **Domain** | cidoc:E1_CRM_Entity |
| **Range** | cidoc:E62_String |
| **Created** | 2025-10-16 |
| **Modified** | 2025-10-17 |
| **AAT Type** | 300404650 (names) |
| **Status** | Active |

## Usage Guidelines

### When to Use P1.1 has_name

✅ **Use for:**
- General, common names for any entity
- Modern cataloging names
- Display names for database records
- Primary identifiers for entities
- Names without specific type requirements

### When NOT to Use P1.1 has_name

❌ **Don't use for:**
- Names from historical sources (use `gmn:P1_2_has_name_from_source`)
- Patrilineal names with patronymic (use `gmn:P1_3_has_patrilineal_name`)
- Place-based names/loconyms (use `gmn:P1_4_has_loconym`)
- Formal document titles (use `gmn:P102_1_has_title`)
- Editorial notes (use `gmn:P3_1_has_editorial_note`)

### Property Relationships

**Specialized Name Properties:**
- `gmn:P1_2_has_name_from_source` - Historical source names (AAT 300456607)
- `gmn:P1_3_has_patrilineal_name` - Patronymic names (AAT 300404651)
- `gmn:P1_4_has_loconym` - Place-based names (Wikidata Q17143070)

**Related Properties:**
- `gmn:P102_1_has_title` - For formal document titles
- `cidoc:P1_is_identified_by` - Direct CIDOC-CRM identification property

## Common Use Cases

### 1. Person Names
```json
{
  "@id": "http://example.org/persons/p001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [{"@value": "Giacomo Spinola"}]
}
```

### 2. Place Names
```json
{
  "@id": "http://example.org/places/genoa",
  "@type": "cidoc:E53_Place",
  "gmn:P1_1_has_name": [{"@value": "Genoa"}]
}
```

### 3. Contract Names
```json
{
  "@id": "http://example.org/contracts/c001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P1_1_has_name": [{"@value": "Sale of Property in Via San Lorenzo"}]
}
```

### 4. Building Names
```json
{
  "@id": "http://example.org/buildings/b001",
  "@type": "gmn:E22_1_Building",
  "gmn:P1_1_has_name": [{"@value": "Palazzo Spinola"}]
}
```

## Technical Details

### Transformation Process

1. **Input Detection:** Script identifies `gmn:P1_1_has_name` in JSON-LD
2. **URI Generation:** Creates unique appellation URI based on subject + name hash
3. **Appellation Creation:** Builds E41_Appellation with AAT type and symbolic content
4. **Property Removal:** Removes shortcut property from output
5. **CIDOC-CRM Output:** Produces compliant P1_is_identified_by structure

### URI Pattern

Appellation URIs follow the pattern:
```
{subject_uri}/appellation/{hash}
```

Where `{hash}` is the last 8 digits of the hash of the name value and property name.

## Support and Troubleshooting

### Common Issues

**Issue:** Property not transforming  
**Solution:** Verify property name is exactly `gmn:P1_1_has_name` (case-sensitive)

**Issue:** Invalid URIs generated  
**Solution:** Check that subject entity has valid `@id` field

**Issue:** AAT type not appearing  
**Solution:** Verify AAT_NAME constant is set to "http://vocab.getty.edu/page/aat/300404650"

**Issue:** Duplicate appellations  
**Solution:** URI generation uses hash to prevent duplicates; check for data inconsistencies

### Testing Recommendations

1. Start with simple test cases (single entity, single name)
2. Progress to complex cases (multiple names, multiple entities)
3. Test with all entity types in your domain
4. Validate all output against CIDOC-CRM specification
5. Check for performance with large datasets

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-26 | Initial deliverables package created |
| - | 2025-10-17 | Property modified in ontology |
| - | 2025-10-16 | Property created in ontology |

## Related Documentation

- **Implementation Guide:** has-name-implementation-guide.md
- **Ontology Documentation:** has-name-documentation.md
- **Main Ontology:** gmn_ontology.ttl
- **Transformation Script:** gmn_to_cidoc_transform.py

## Contact

For questions about this implementation:
- Review the detailed documentation in this package
- Check the main GMN ontology documentation
- Consult the CIDOC-CRM specification
- Contact the ontology maintainer

## License and Attribution

This deliverables package is part of the Genoese Merchant Networks project ontology documentation.

---

**Note:** The `gmn:P1_1_has_name` property is already implemented in the current GMN ontology. This package provides comprehensive documentation, usage guidelines, and testing procedures for the existing implementation.
