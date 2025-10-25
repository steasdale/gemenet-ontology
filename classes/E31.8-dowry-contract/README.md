# Dowry Contract Ontology - Deliverables Summary

## Overview

This package contains all necessary documentation and code to add the gmn:E31_8_Dowry_Contract class to the Genoese Merchant Networks ontology. The dowry contract models the transfer of property from a donor to a receiving party in the context of marriage arrangements.

## Key Design Features

✓ **Reuses existing P70.32 property** (indicates donor) as requested
✓ **Shares P70.22 property** (indicates receiving party) with other contract types
✓ **Creates new P70.34 property** (indicates object of dowry) for clarity
✓ **Uses E8_Acquisition** like sales and donations for consistency
✓ **Maintains full CIDOC-CRM compliance** in transformation

## Files Included

### 1. dowry_contract_implementation_guide.md
**Purpose**: Complete step-by-step implementation guide
**Contents**:
- Overview of dowry contracts
- Design decisions and rationale
- Detailed implementation steps for:
  - Ontology file updates (4 changes)
  - Transformation script updates (3 changes)
  - Documentation updates
- Testing instructions
- Summary of all changes

**Use this file**: As your primary implementation reference

### 2. dowry_contract_ontology.md
**Purpose**: Complete ontology documentation for dowry contracts
**Contents**:
- Class definition (gmn:E31_8_Dowry_Contract)
- Property definitions (P70.32, P70.22, P70.34)
- Semantic structure diagrams
- Transformation examples (basic and complex)
- Comparison with similar contract types
- Implementation notes

**Use this file**: For reference when working with dowry contracts

### 3. dowry_contract_ontology_additions.ttl
**Purpose**: Ready-to-use TTL snippets for the ontology file
**Contents**:
- New class definition (E31_8)
- Updated P70.32 domain
- Updated P70.22 domain
- New P70.34 property definition

**Use this file**: Copy/paste snippets directly into gmn_ontology.ttl

### 4. dowry_contract_transform_additions.py
**Purpose**: Ready-to-use Python code for the transformation script
**Contents**:
- New transformation function (transform_p70_34_indicates_object_of_dowry)
- Updated transformation function (transform_p70_22_indicates_receiving_party)
- Updated transform_item() function with new call
- Updated main() help text

**Use this file**: Copy/paste functions directly into gmn_to_cidoc_transform.py

### 5. dowry_contract_documentation_additions.txt
**Purpose**: Ready-to-add examples for the main documentation file
**Contents**:
- Transformation examples for all three properties
- Complete dowry contract example
- Updated class hierarchy
- Updated property domain distribution
- Comparison tables

**Use this file**: Copy/paste sections into documentation_note.txt

## Quick Start Implementation Checklist

### Ontology File (gmn_ontology.ttl)
- [ ] Add E31_8_Dowry_Contract class definition
- [ ] Update P70.32 domain (add E31_8 to union)
- [ ] Update P70.32 comment (mention dowries)
- [ ] Update P70.22 domain (add E31_8 to union)
- [ ] Update P70.22 comment (mention dowries)
- [ ] Add P70.34 property definition
- [ ] Update ontology version to 1.5 and modified date

### Transformation Script (gmn_to_cidoc_transform.py)
- [ ] Add transform_p70_34_indicates_object_of_dowry() function
- [ ] Update transform_p70_22_indicates_receiving_party() function
- [ ] Add call to transform_p70_34 in transform_item() function
- [ ] Update module docstring to include E31_8
- [ ] Update main() help text to include E31_8

### Documentation (documentation_note.txt)
- [ ] Add P70.32 transformation example (updated)
- [ ] Add P70.22 transformation example (updated)
- [ ] Add P70.34 transformation example (new)
- [ ] Add complete dowry contract example
- [ ] Update class hierarchy diagram
- [ ] Update property domain distribution table
- [ ] Add contract type comparison table

### Testing
- [ ] Create test JSON with dowry contract
- [ ] Run transformation script
- [ ] Verify output structure
- [ ] Check all properties transform correctly

## Property Usage Summary

| Property | Domain | Used For | Transformation |
|----------|--------|----------|----------------|
| P70.32 | E31_7, E31_8 | Donor of donation/dowry | P23_transferred_title_from |
| P70.22 | E31_4, E31_5, E31_7, E31_8 | Receiving party | P22_transferred_title_to (for E31_7, E31_8) |
| P70.34 | E31_8 | Object of dowry | P24_transferred_title_of |
| P70.16 | E31_2 (primarily) | Price/value amount | P181_has_amount |
| P70.17 | E31_2 (primarily) | Price/value currency | P180_has_currency |

## Transformation Flow

```
Dowry Contract (gmn:E31_8_Dowry_Contract)
    |
    ├─ P70.32 → E8_Acquisition → P23_transferred_title_from → Donor
    ├─ P70.22 → E8_Acquisition → P22_transferred_title_to → Receiving Party
    ├─ P70.34 → E8_Acquisition → P24_transferred_title_of → Dowry Object(s)
    ├─ P70.16 → E8_Acquisition → P177 → E97_Monetary_Amount → P181 → Amount
    └─ P70.17 → E8_Acquisition → P177 → E97_Monetary_Amount → P180 → Currency
```

## Example Usage in Omeka-S

When creating a dowry contract in Omeka-S:

1. Select resource type: `gmn:E31_8_Dowry_Contract`
2. Add name: `gmn:P1_1_has_name` (e.g., "Dowry of Maria Spinola")
3. Add donor: `gmn:P70_32_indicates_donor` (link to person resource)
4. Add receiving party: `gmn:P70_22_indicates_receiving_party` (link to person resource)
5. Add dowry object(s): `gmn:P70_34_indicates_object_of_dowry` (link to building/property)
6. Optionally add value: `gmn:P70_16_documents_sale_price_amount` and `gmn:P70_17_documents_sale_price_currency`
7. Add notary: `gmn:P94i_1_was_created_by` (link to notary)
8. Add date: `gmn:P94i_2_has_enactment_date`
9. Add place: `gmn:P94i_3_has_place_of_enactment`

## Design Rationale

### Why E31_8 instead of E31_9?
The numbering follows the existing sequence in the ontology. E31_7 is Donation Contract, so E31_8 is the logical next number.

### Why not create P70.35 for donor?
The semantic meaning of "donor" is identical in both donations and dowries - someone transferring property. The context (gift vs. marriage) is captured by the document type, not by different property names.

### Why create P70.34 instead of reusing P70.33?
While the transformation is identical, having separate properties:
- Makes data entry clearer and more explicit
- Allows for future distinctions if needed
- Maintains semantic precision at the source level
- Improves data model documentation

## Support Information

If you encounter issues during implementation:

1. **Ontology validation**: Use an RDF validator to check syntax
2. **Transformation testing**: Test with small sample files first
3. **CIDOC-CRM compliance**: Verify output against CIDOC-CRM specification
4. **Property domains**: Ensure all property domains are correctly updated

## Version Information

- **Ontology Version**: 1.5
- **Creation Date**: 2025-10-25
- **Classes Added**: 1 (E31_8_Dowry_Contract)
- **Properties Added**: 1 (P70.34)
- **Properties Modified**: 2 (P70.32, P70.22)
- **Transformation Functions Added**: 1
- **Transformation Functions Modified**: 1

## Related Documentation

This dowry contract addition follows the same pattern as:
- Sales Contracts (E31_2) - documented in main ontology
- Donation Contracts (E31_7) - documented in main ontology
- Cession Contracts (E31_4) - documented in main ontology
- Declarations (E31_5) - documented in declaration_ontology.md
- Arbitration Agreements (E31_3) - documented in arbitration_documentation.md

## Next Steps

After implementation:
1. Test with sample data
2. Update any documentation or training materials
3. Notify Omeka-S administrators to add the new class to resource templates
4. Create example records in Omeka-S for reference
5. Update any data entry guidelines for users

## Contact

For questions about this implementation, refer to the Genoese Merchant Networks project documentation or contact the ontology maintainer.
