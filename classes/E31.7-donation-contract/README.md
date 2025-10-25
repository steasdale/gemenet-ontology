# Donation Contract Ontology - Deliverables Summary

## 📦 Complete Package Contents

This package contains everything needed to implement the gmn:E31_7_Donation_Contract class in the Genoese Merchant Networks ontology.

### 📄 Included Files

1. **README.md** (this file)
   - Overview and quick-start guide
   - Summary of all deliverables
   - Implementation checklist

2. **donation_contract_implementation_guide.md**
   - Complete step-by-step instructions
   - Design decisions and rationale
   - Testing procedures
   - Code snippets for all changes

3. **donation_contract_ontology.md**
   - Full ontology documentation
   - Class and property definitions
   - Transformation examples
   - Comparison tables
   - Best practices

4. **donation_contract_ontology_additions.ttl**
   - Ready-to-copy TTL snippets
   - 1 class definition
   - 2 new properties
   - 1 updated property

5. **donation_contract_transform_additions.py**
   - Ready-to-copy Python code
   - 2 new transformation functions
   - 2 function updates
   - Help text update

6. **donation_contract_documentation_additions.txt**
   - Examples for documentation
   - Updated tables and hierarchies
   - Usage notes

## Overview

This package contains all necessary documentation and code to add the gmn:E31_7_Donation_Contract class to the Genoese Merchant Networks ontology. The donation contract models the gratuitous transfer of property from a donor to a donee (recipient) without expectation of payment.

## Key Design Features

✓ **Creates new P70.32 property** (indicates donor) for donors
✓ **Reuses existing P70.22 property** (indicates receiving party) as requested
✓ **Creates new P70.33 property** (indicates object of donation) for donated property
✓ **Uses E8_Acquisition** like sales for consistency in property transfers
✓ **Maintains full CIDOC-CRM compliance** in transformation

## 🎯 Quick Start Checklist

- [ ] Read donation_contract_implementation_guide.md
- [ ] Add class and properties to gmn_ontology.ttl (4 changes)
- [ ] Add transformation functions to gmn_to_cidoc_transform.py (5 changes)
- [ ] Add examples to documentation_note.txt (6 sections)
- [ ] Test with sample data
- [ ] Validate RDF syntax
- [ ] Update Omeka-S templates

## 📊 Implementation Summary

### Files to Modify
1. **gmn_ontology.ttl**: Add 1 class, add 2 properties, update 1 property
2. **gmn_to_cidoc_transform.py**: Add 2 functions, update 2 functions, update help text
3. **documentation_note.txt**: Add 6 sections with examples and tables

### Changes at a Glance
- **Classes Added**: 1 (E31_7_Donation_Contract)
- **Properties Added**: 2 (P70.32, P70.33)
- **Properties Modified**: 1 (P70.22)
- **Transformation Functions Added**: 2
- **Transformation Functions Modified**: 2
- **Lines of Code Added**: ~150

## 🔧 Support Information

If you encounter issues during implementation:

1. **Ontology validation**: Use an RDF validator to check syntax
2. **Transformation testing**: Test with small sample files first
3. **CIDOC-CRM compliance**: Verify output against CIDOC-CRM specification
4. **Property domains**: Ensure all property domains are correctly updated

## 📅 Version Information

- **Ontology Version**: 1.4
- **Creation Date**: 2025-10-19
- **Classes Added**: 1 (E31_7_Donation_Contract)
- **Properties Added**: 2 (P70.32, P70.33)
- **Properties Modified**: 1 (P70.22)
- **Transformation Functions Added**: 2
- **Transformation Functions Modified**: 2

## 📚 Related Documentation

This donation contract addition follows the same pattern as:
- Sales Contracts (E31_2) - documented in main ontology
- Cession Contracts (E31_4) - documented in main ontology
- Declarations (E31_5) - documented in declaration_ontology.md
- Arbitration Agreements (E31_3) - documented in arbitration_documentation.md
- Correspondence (E31_6) - documented in main ontology

## 🚀 Next Steps

After implementation:
1. Test with sample data
2. Update any documentation or training materials
3. Notify Omeka-S administrators to add the new class to resource templates
4. Create example records in Omeka-S for reference
5. Update any data entry guidelines for users

## 📧 Contact

For questions about this implementation, refer to the Genoese Merchant Networks project documentation or contact the ontology maintainer.

---

## Semantic Structure Overview

```
E31_7_Donation_Contract (document)
  └─ P70_documents
      └─ E8_Acquisition (transfer event)
          ├─ P23_transferred_title_from → E39_Actor (donor via P70.32)
          ├─ P22_transferred_title_to → E39_Actor (donee via P70.22)
          └─ P24_transferred_title_of → E18_Physical_Thing (property via P70.33)
```

## Property Summary

| Property | Label | Transformation | Domain |
|----------|-------|----------------|--------|
| P70.32 | indicates donor | P70 > E8 > P23 | E31_7_Donation_Contract |
| P70.22 | indicates receiving party | P70 > E8 > P22 | E31_4, E31_5, E31_7 |
| P70.33 | indicates object of donation | P70 > E8 > P24 | E31_7_Donation_Contract |
