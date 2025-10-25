# E31.6 Correspondence Ontology Extension

## Overview

This package contains the complete implementation of the **E31.6 Correspondence** subclass for the Genoese Merchant Networks (GMN) CIDOC-CRM ontology extension. Correspondence documents represent letters and written communication between parties, capturing the sender, recipient, origin and destination locations, and content described within the letter.

## What's Included

This deliverables package contains six files:

1. **README.md** (this file) - Overview and quick-start guide
2. **implementation_guide.md** - Step-by-step implementation instructions
3. **ontology_documentation.md** - Complete semantic documentation
4. **ttl_additions.txt** - TTL code for gmn_ontology.ttl
5. **python_additions.txt** - Python code for gmn_to_cidoc_transform.py
6. **documentation_additions.txt** - Examples for documentation note.txt

## Quick Start Checklist

### Prerequisites
- [ ] Existing GMN ontology infrastructure in place
- [ ] Python transformation script operational
- [ ] Understanding of CIDOC-CRM P70_documents pattern

### Implementation Steps
- [ ] Add TTL definitions to `gmn_ontology.ttl`
- [ ] Add Python transformation functions to `gmn_to_cidoc_transform_script.py`
- [ ] Add transformation calls to main `transform_item()` function
- [ ] Add AAT constant for correspondence
- [ ] Add documentation examples to `documentation note.txt`
- [ ] Test with sample data
- [ ] Validate RDF output

### Expected Timeline
- TTL additions: 15 minutes
- Python additions: 30 minutes
- Testing: 30 minutes
- Documentation: 15 minutes
- **Total: ~90 minutes**

## Properties Summary

| Property | Label | CRM Path | Domain | Range |
|----------|-------|----------|--------|-------|
| P70.26 | indicates sender | P14_carried_out_by | E31_6_Correspondence | E39_Actor |
| P70.27 | has address of origin | P7_took_place_at | E31_6_Correspondence | E53_Place |
| P70.28 | indicates recipient | P01_has_domain | E31_6_Correspondence | E39_Actor |
| P70.29 | indicates holder of item | P16 > E7 > P14 | E31_6_Correspondence | E39_Actor |
| P70.30 | refers to described event | P16_used_specific_object | E31_Document | E5_Event |
| P70.31 | has address of destination | P26_moved_to | E31_6_Correspondence | E53_Place |

## Key Semantic Features

### Correspondence Activity Structure
All correspondence properties link through a central **E7_Activity** typed as AAT 300026877 (correspondence):

```
E31_6_Correspondence
  └─ P70_documents → E7_Activity (correspondence)
      ├─ P14_carried_out_by → sender
      ├─ P7_took_place_at → origin place
      ├─ P26_moved_to → destination place
      ├─ P01_has_domain → recipient
      └─ P16_used_specific_object → described events/items
```

### Shared Activity Pattern
Properties P70.26, P70.27, P70.28, and P70.31 all share the same E7_Activity node, creating a unified model of the correspondence event.

### Spatial Transfer Model
The correspondence models the physical movement of a letter:
- **Origin** (P7_took_place_at): Where the letter was written
- **Destination** (P26_moved_to): Where the letter was sent

### Nested Content
Properties P70.29 and P70.30 create nested structures for content described within the letter, distinct from the letter-writing activity itself.

## AAT Terms Used

- **AAT 300026877** - correspondence (documents)
- **AAT 300077993** - holding (for item holders)

## Related Properties

Correspondence documents can also use existing GMN properties:
- `P70_11_documents_referenced_person` - For persons mentioned in the letter
- `P94i_1_was_created_by` - For the scribe/author
- `P94i_2_has_enactment_date` - For the writing date
- `P102_1_has_title` - For formal letter titles
- `P138i_1_has_representation` - For digital images

## Implementation Notes

### Important Considerations

1. **Order Independence**: Transformation functions can be called in any order
2. **Activity Reuse**: All functions check for existing correspondence activity before creating new ones
3. **P70.30 Domain**: This property has domain E31_Document, making it usable with any document type
4. **Person References**: Use P70_11 for persons mentioned in letter content (including event participants)

### Testing Checklist

After implementation:
- [ ] Test with correspondence containing all properties
- [ ] Test with correspondence containing minimal properties (sender/recipient only)
- [ ] Verify shared activity node creation
- [ ] Validate nested holding activity structure
- [ ] Check event references via P70.30
- [ ] Confirm proper URI generation

## File Organization

```
correspondence_deliverables/
├── README.md (this file)
├── implementation_guide.md
├── ontology_documentation.md
├── ttl_additions.txt
├── python_additions.txt
└── documentation_additions.txt
```

## Support and Questions

For questions about implementation:
1. Review the ontology_documentation.md for semantic details
2. Check implementation_guide.md for step-by-step instructions
3. Examine example transformations in documentation_additions.txt

## Version Information

- **Version**: 1.0
- **Date**: 2025-10-18
- **Compatible with**: GMN Ontology v1.4+
- **CIDOC-CRM Version**: 7.1+

## Change Log

### Version 1.0 (2025-10-18)
- Initial release
- Six correspondence properties (P70.26-P70.31)
- E31.6 Correspondence class definition
- Full transformation support
- Complete documentation

## Next Steps

1. Read `implementation_guide.md` for detailed implementation steps
2. Review `ontology_documentation.md` for semantic understanding
3. Copy code from `ttl_additions.txt` and `python_additions.txt`
4. Test with sample correspondence data
5. Add documentation examples from `documentation_additions.txt`

## License

This ontology extension follows the same license as the main GMN project.
