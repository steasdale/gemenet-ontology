# GMN Property P70.3: Indicates Transferred Object - Deliverables Package

## Overview

This deliverables package provides complete documentation and implementation code for the GMN ontology property `gmn:P70_3_indicates_transferred_object`, which models transferred objects in historical contracts (sales, leases, donations, dowries) using the CIDOC-CRM E13 Attribute Assignment pattern.

**Property Name:** `gmn:P70_3_indicates_transferred_object`

**Purpose:** To model transferred objects with rich semantic properties including type, quantity, value, measurements, color, and provenance.

**Scope:** Sales contracts, lease contracts, donation contracts, and dowry contracts.

## What's Included

This package contains six comprehensive files:

1. **README.md** (this file) - Overview and quick start guide
2. **Implementation_Guide.md** - Detailed Omeka-S implementation instructions
3. **Ontology_Documentation.md** - Complete semantic and ontological documentation
4. **P70_3_TTL_Additions.ttl** - Turtle format ontology definitions
5. **P70_3_Transformation.py** - Python transformation code for CIDOC-CRM compliance
6. **Documentation_Additions.md** - Additional notes and integration guidance

## Key Features

### Semantic Structure

The property implements the E13 Attribute Assignment pattern:

```
E31_Document (contract)
  └─ P67_refers_to
      └─ E7/E8/E10_Activity (transfer event)
          └─ P140i_was_assigned_by
              └─ E13_Attribute_Assignment (object attribution)
                  ├─ P177_assigned_property_of_type (P24 or P30)
                  ├─ P141_assigned → Object Resource
                  └─ P2_has_type → Object Category
```

### Object Properties Modeled

Each transferred object can have:

- **Type/Commodity**: Controlled vocabulary (salt, wool, boards, cloth, etc.)
- **Number/Count**: Integer quantity
- **Monetary Value**: Lire.Soldi.Denari (L.S.D) format with provenance
- **Measurement**: Weight/volume with number + unit
- **Color**: Controlled vocabulary
- **Provenance**: Place of origin (E53_Place)

### Implementation Approach

- **Omeka-S Resource Items**: Each object is a separate resource item
- **Linked via Property**: Objects are linked to contracts via `gmn:P70_3_indicates_transferred_object`
- **Full Semantic Structure**: Maintains complete CIDOC-CRM compliance
- **E13 Pattern**: Uses Attribute Assignment for object properties

## Quick Start

### For Ontology Developers

1. Review the semantic documentation in `Ontology_Documentation.md`
2. Add the TTL definitions from `P70_3_TTL_Additions.ttl` to your GMN ontology file
3. Update the version number and modification date in your ontology

### For Implementation Teams

1. Read the `Implementation_Guide.md` for step-by-step Omeka-S setup
2. Create the necessary resource templates for objects
3. Configure vocabularies for controlled terms
4. Test with sample data

### For Data Transformation

1. Add the transformation functions from `P70_3_Transformation.py` to your transformation script
2. Update the `transform_item()` function to call the new transformers
3. Test transformation with sample JSON-LD exports
4. Validate output against CIDOC-CRM schema

## Technical Requirements

- **GMN Ontology Version:** 1.5 or higher
- **CIDOC-CRM Version:** 7.x compatible
- **Omeka-S Version:** 4.x recommended
- **Python Version:** 3.7+ (for transformation script)
- **Dependencies:** Standard library only (json, uuid, sys)

## Contract Types Supported

The property works with these contract types:

- **E31.2 Sales Contract** (`gmn:E31_2_Sales_Contract`)
- **E31.6 Lease Contract** (`gmn:E31_6_Lease_Contract`) 
- **E31.7 Donation Contract** (`gmn:E31_7_Donation_Contract`)
- **E31.8 Dowry Contract** (`gmn:E31_8_Dowry_Contract`)

## Key Design Decisions

1. **Separate Resource Items**: Each object is modeled as its own resource item in Omeka-S, allowing for reuse and detailed attribution
2. **E13 Attribute Assignment**: Uses the formal CIDOC-CRM pattern for assigning properties to objects within activities
3. **Flexible Property Types**: Supports both P24 (transferred_title_of) and P30 (custody_transferred_of) for ownership vs. custody
4. **Controlled Vocabularies**: Recommends Getty AAT and custom project vocabularies for consistency
5. **L.S.D. Monetary Values**: Supports period-appropriate Lire.Soldi.Denari format with provenance tracking

## Integration with Existing GMN Properties

This property complements existing GMN properties:

- **P70.1** (indicates seller) - Person transferring object
- **P70.2** (indicates buyer) - Person receiving object
- **P70.3** (indicates transferred object) - **THIS PROPERTY** - Object being transferred
- **P70.16-17** (sale price) - Overall transaction price
- **P70.32** (indicates donor) - For donation contracts
- **P70.34** (indicates object of dowry) - For dowry contracts

## Usage Example

**Simple Sales Contract:**

```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_indicates_seller <merchant_giovanni> ;
    gmn:P70_2_indicates_buyer <merchant_paolo> ;
    gmn:P70_3_indicates_transferred_object <object_salt_001> .

<object_salt_001> a gmn:E24_Physical_Human-Made_Thing ;
    gmn:P1_1_has_name "White salt from Ibiza" ;
    gmn:P2_1_has_type <aat:300010967> ; # salt
    gmn:P54_1_has_count "100"^^xsd:integer ;
    gmn:P43_1_has_dimension <dimension_weight_001> .
```

## Validation Checklist

Before deploying, ensure:

- [ ] TTL definitions added to ontology file
- [ ] Omeka-S resource templates created
- [ ] Controlled vocabularies configured
- [ ] Transformation code integrated and tested
- [ ] Sample data transforms correctly
- [ ] Output validates against CIDOC-CRM
- [ ] Documentation reviewed by team
- [ ] Integration tested with existing properties

## Support and Documentation

For questions or issues:

1. Review the detailed `Ontology_Documentation.md`
2. Check the `Implementation_Guide.md` for Omeka-S specifics
3. Examine transformation examples in `P70_3_Transformation.py`
4. Refer to project documentation at `/mnt/project/`

## Version Information

- **Package Version:** 1.0
- **Created:** October 28, 2025
- **GMN Ontology Compatibility:** 1.5+
- **CIDOC-CRM Version:** 7.x
- **Author:** Genoese Merchant Networks Project

## License

This ontology extension follows the same license as the GMN ontology.

## Next Steps

1. Review all documentation files in this package
2. Plan implementation timeline with your team
3. Set up development/testing environment
4. Begin with small dataset for validation
5. Iterate based on testing results
6. Deploy to production when validated

---

**Important Note:** This property uses the E13 Attribute Assignment pattern, which is more complex than simple shortcut properties. Please read the full documentation before implementation to understand the semantic structure and transformation requirements.
