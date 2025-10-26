# Arbitration Agreement Contract Implementation Package

**Version:** 1.0  
**Date:** October 26, 2025  
**Project:** Genoese Merchant Networks CIDOC-CRM Extension

## Overview

This package contains all files needed to implement the Arbitration Agreement contract subclass in the GMN ontology. Arbitration agreements document the transfer of dispute resolution obligations from disputing parties to appointed arbitrators, following the same semantic pattern as sales contracts.

### What's Included

This deliverables package contains:

1. **README.md** (this file) - Overview and quick-start guide
2. **arbitration-agreement-implementation-guide.md** - Step-by-step implementation instructions
3. **arbitration-agreement-documentation.md** - Complete semantic documentation
4. **arbitration-agreement-ontology.ttl** - TTL snippets for the main ontology
5. **arbitration-agreement-transform.py** - Python code for transformation script
6. **arbitration-agreement-doc-note.txt** - Documentation additions and examples

## Quick Start Checklist

### Phase 1: Ontology Updates
- [ ] Open `gmn_ontology.rdf`
- [ ] Add TTL snippets from `arbitration-agreement-ontology.ttl`
- [ ] Verify the class `gmn:E31_3_Arbitration_Agreement` is added
- [ ] Verify properties P70.18, P70.19, P70.20 are added
- [ ] Save and validate the RDF file

### Phase 2: Transformation Script Updates
- [ ] Open `gmn_to_cidoc_transform_script.py`
- [ ] Add constant from `arbitration-agreement-transform.py` (AAT_ARBITRATION)
- [ ] Add three transformation functions
- [ ] Add function calls to `transform_item()`
- [ ] Save the Python file

### Phase 3: Documentation Updates
- [ ] Open main documentation file
- [ ] Add content from `arbitration-agreement-doc-note.txt`
- [ ] Update class hierarchy documentation
- [ ] Save documentation

### Phase 4: Testing
- [ ] Create test arbitration agreement in Omeka-S
- [ ] Export JSON-LD
- [ ] Run transformation script
- [ ] Verify output structure matches expected format
- [ ] Validate against CIDOC-CRM

## Implementation Summary

### New Ontology Elements

**Class Added:**
- `gmn:E31_3_Arbitration_Agreement` - subclass of `gmn:E31_1_Contract`

**Properties Added:**
- `gmn:P70_18_documents_disputing_party` - links disputing parties via P14_carried_out_by
- `gmn:P70_19_documents_arbitrator` - links arbitrators via P14_carried_out_by  
- `gmn:P70_20_documents_dispute_subject` - links dispute subject via P16_used_specific_object

### Semantic Structure

```
gmn:E31_3_Arbitration_Agreement
  └─ P70_documents → E7_Activity (AAT 300417271: arbitration)
      ├─ P14_carried_out_by → disputing parties (active principals)
      ├─ P14_carried_out_by → arbitrators (active principals)
      └─ P16_used_specific_object → dispute subject
```

### Key Design Decision

**Both disputing parties and arbitrators use P14_carried_out_by** because they are all active principals in the arbitration agreement:
- Disputing parties agree to submit their dispute to arbitration
- Arbitrators agree to conduct the arbitration and render a binding decision
- All parties are carrying out the arbitration agreement together

This differs from P11_had_participant, which would imply passive participation.

## Files Description

### 1. arbitration-agreement-implementation-guide.md
Comprehensive step-by-step instructions for implementing all changes. Includes:
- Detailed procedures for each file
- Code insertion points
- Testing procedures
- Troubleshooting tips

### 2. arbitration-agreement-documentation.md
Complete semantic documentation including:
- Class definitions and rationale
- Property specifications with CIDOC-CRM paths
- Transformation logic explanations
- Complete examples with before/after states

### 3. arbitration-agreement-ontology.ttl
Ready-to-copy Turtle snippets:
- Class definition for E31_3_Arbitration_Agreement
- Three property definitions (P70.18, P70.19, P70.20)
- Complete with comments and AAT references

### 4. arbitration-agreement-transform.py
Python code additions:
- AAT_ARBITRATION constant
- Three transformation functions with full documentation
- Function call additions for transform_item()

### 5. arbitration-agreement-doc-note.txt
Documentation additions:
- Updated class hierarchy table
- Property comparison tables
- Usage examples
- Integration notes for main documentation

## Integration Notes

### Compatibility
- Requires GMN ontology version 1.3 or higher
- Works with existing E31_1_Contract and E31_2_Sales_Contract classes
- Transformation functions follow the same pattern as sales contract transformations

### Dependencies
- Python 3.6+
- No additional Python libraries required beyond standard library
- CIDOC-CRM base ontology
- Getty AAT vocabulary (for type references)

## Support and Questions

For questions about implementation or to report issues:
1. Consult the implementation guide for detailed procedures
2. Review the documentation file for semantic clarifications
3. Check transformation examples in the documentation

## Version History

**v1.0 (2025-10-26)**
- Initial release
- Three arbitration agreement properties
- E31_3_Arbitration_Agreement class
- Complete documentation and implementation guide

## License

This ontology extension follows the same license as the main GMN ontology project.

---

**Next Steps:** Begin with the Implementation Guide (arbitration-agreement-implementation-guide.md) for detailed instructions on integrating these components into your project.
