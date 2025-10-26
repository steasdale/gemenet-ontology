# E31.5 Declaration Ontology Addition - Deliverables Summary

## Overview

This package contains all necessary documentation and code to add the **gmn:E31_5_Declaration** class to the Genoese Merchant Networks ontology. The declaration subclass models documents where one party (the declarant) makes a formal statement, acknowledgment, or assertion to another party (the recipient) regarding a specific subject matter. These can be either notarial documents or governmental documents issued without notarial participation.

## What's Included

This deliverables package contains six files:

1. **README.md** (this file) - Overview and quick-start guide
2. **declaration-implementation-guide.md** - Step-by-step implementation instructions
3. **declaration-documentation.md** - Complete semantic documentation
4. **declaration-ontology.ttl** - TTL code for gmn_ontology.ttl
5. **declaration-transform.py** - Python code for transformation script
6. **declaration-doc-note.txt** - Documentation additions for main text file

## Quick Start Checklist

- [ ] Review the implementation guide
- [ ] Add TTL definitions to `gmn_ontology.ttl`
- [ ] Add Python transformation functions to `gmn_to_cidoc_transform_script.py`
- [ ] Update `transform_item()` function with new transformation calls
- [ ] Add AAT constant for declarations
- [ ] Test with sample declaration data
- [ ] Validate RDF output
- [ ] Update main documentation file with examples

## Key Features

### New Class
- **gmn:E31_5_Declaration**: Direct subclass of `cidoc:E31_Document` (not a contract subclass)

### New Properties
- **gmn:P70_24_indicates_declarant**: Links declaration to the party making the statement
- **gmn:P70_25_indicates_declaration_subject**: Links declaration to the subject matter being declared

### Modified Property
- **gmn:P70_22_indicates_receiving_party**: Now has expanded domain to include both cessions and declarations

### Transformation Pattern
All three properties share the same E7_Activity node, automatically typed as AAT 300027623 (declarations).

## Semantic Structure

```
E31_5_Declaration (the declaration document)
  └─ P70_documents
      └─ E7_Activity (the declaration activity)
          ├─ P2_has_type → AAT 300027623 (declarations)
          ├─ P14_carried_out_by → E39_Actor (declarant)
          ├─ P01_has_domain → E39_Actor (recipient)
          └─ P16_used_specific_object → E1_CRM_Entity (declaration subject)
```

## Implementation Summary

### 1. Ontology Changes (gmn_ontology.ttl)
- Add 1 new class definition
- Add 2 new property definitions
- Modify 1 existing property (P70.22) to expand its domain

### 2. Python Script Changes (gmn_to_cidoc_transform_script.py)
- Add 1 new constant: `AAT_DECLARATION`
- Add 2 new transformation functions: `transform_p70_24_indicates_declarant()` and `transform_p70_25_indicates_declaration_subject()`
- Modify 1 existing function: `transform_p70_22_indicates_receiving_party()` to handle both cessions and declarations
- Update `transform_item()` function to call new transformations in correct order

### 3. Documentation Changes
- Add class description and examples
- Add property descriptions
- Update comparison tables to include declarations

## Critical Implementation Notes

### Property Reuse: P70.22
The property `gmn:P70_22_indicates_receiving_party` is shared between:
- **E31_4_Cession_of_Rights_Contract** (transforms to P14_carried_out_by)
- **E31_5_Declaration** (transforms to P01_has_domain)

The transformation function detects document type and uses the appropriate CIDOC-CRM property.

### Transformation Order
**IMPORTANT**: In `transform_item()`, P70.22 must be called **after** P70.21 and P70.24 so the activity type is already set:

```python
item = transform_p70_21_indicates_conceding_party(item)
item = transform_p70_24_indicates_declarant(item)
item = transform_p70_22_indicates_receiving_party(item)  # After P70.21 and P70.24
item = transform_p70_23_indicates_object_of_cession(item)
item = transform_p70_25_indicates_declaration_subject(item)
```

### Difference from Contracts
Unlike E31_1_Contract and its subclasses, E31_5_Declaration is a **direct subclass of E31_Document** because:
- Declarations are not always contracts
- Some are governmental documents without notarial participation
- They represent unilateral statements rather than bilateral agreements

## File Descriptions

### 1. declaration-implementation-guide.md
Step-by-step instructions for implementing all changes:
- Pre-implementation checklist
- Detailed ontology modifications
- Python script modifications with code snippets
- Testing procedures
- Validation steps
- Troubleshooting guide

### 2. declaration-documentation.md
Complete semantic documentation:
- Class definition and scope notes
- Property specifications with semantic paths
- Full CIDOC-CRM transformation patterns
- Multiple transformation examples
- Comparison with other document types
- AAT references

### 3. declaration-ontology.ttl
Ready-to-copy TTL code including:
- Class definition for E31_5_Declaration
- Property definition for P70_24_indicates_declarant
- Property definition for P70_25_indicates_declaration_subject
- Updated property definition for P70_22_indicates_receiving_party

### 4. declaration-transform.py
Ready-to-copy Python code including:
- AAT constant definition
- `transform_p70_24_indicates_declarant()` function
- Updated `transform_p70_22_indicates_receiving_party()` function
- `transform_p70_25_indicates_declaration_subject()` function
- Updated `transform_item()` function with correct ordering

### 5. declaration-doc-note.txt
Documentation additions including:
- Declaration examples for main documentation
- Comparison tables
- Use case descriptions
- Property usage examples

## Use Cases

Declarations model various types of formal statements:

1. **Debt Acknowledgments**: Merchant declares owing money to another party
2. **Property Claims**: Individual declares ownership or rights to property
3. **Official Pronouncements**: Government declares policies, exemptions, or decrees
4. **Formal Notifications**: Party notifies another of facts or circumstances
5. **Legal Acknowledgments**: Recognition of obligations or legal status

## Testing Recommendations

1. Create sample declaration data in simplified format
2. Run transformation script
3. Validate output against CIDOC-CRM
4. Verify all three properties share the same activity node
5. Check that P70.22 uses P01_has_domain for declarations
6. Verify AAT typing is correct (300027623)
7. Test with both notarial and governmental declaration examples

## Comparison with Other Document Types

| Aspect | Sales Contract | Cession | Declaration |
|--------|---------------|---------|-------------|
| Central Event | E8_Acquisition | E7_Activity (cession) | E7_Activity (declaration) |
| Main Actors | P23/P22 (seller/buyer) | P14 (both parties) | P14 (declarant) + P01 (recipient) |
| Receiving Party Property | P22_transferred_title_to | P14_carried_out_by (via P70.22) | P01_has_domain (via P70.22) |
| Object | P24 (property transferred) | P16 (legal object/rights) | P16 (declaration subject) |
| Nature | Bilateral transfer | Bilateral transfer of rights | Unilateral statement |
| Subclass of | E31_1_Contract | E31_1_Contract | E31_Document (not contract) |

## Version Information

- **Ontology Version**: 1.5
- **Creation Date**: 2025-10-25
- **Classes Added**: 1 (E31_5_Declaration)
- **Properties Added**: 2 (P70_24, P70_25)
- **Properties Modified**: 1 (P70_22)
- **Transformation Functions Added**: 2
- **Transformation Functions Modified**: 1

## Related Documentation

This declaration addition complements other document types:
- Sales Contracts (E31_2) - documented in main ontology
- Arbitration Agreements (E31_3) - documented in main ontology
- Cession Contracts (E31_4) - documented in main ontology
- Donation Contracts (E31_7) - if implemented
- Dowry Contracts (E31_8) - if implemented

## Support Information

If you encounter issues during implementation:

1. **Ontology validation**: Use an RDF validator to check TTL syntax
2. **Transformation testing**: Test with small sample files first
3. **CIDOC-CRM compliance**: Verify output against CIDOC-CRM specification
4. **Property domains**: Ensure P70.22 domain includes both E31_4 and E31_5
5. **Transformation order**: Verify P70.22 is called after P70.24 in transform_item()

## Next Steps

After implementation:
1. Test with sample declaration data
2. Validate transformed output
3. Update any documentation or training materials
4. Notify Omeka-S administrators to add new class to resource templates
5. Create example records in Omeka-S for reference
6. Update data entry guidelines for users

## Contact

For questions about this implementation, refer to the Genoese Merchant Networks project documentation or contact the ontology maintainer.
