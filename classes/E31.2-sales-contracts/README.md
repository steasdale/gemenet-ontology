# E31.2 Sales Contract - Deliverables Summary

## Overview

This package contains comprehensive documentation and code for the **gmn:E31_2_Sales_Contract** class in the Genoese Merchant Networks ontology. The sales contract subclass models documents that record the sale and transfer of property (both real estate and moveable property) between parties, including information about buyers, sellers, property transferred, price, and all supporting actors.

## What's Included

This deliverables package contains six files:

1. **README.md** (this file) - Overview and quick-start guide
2. **sales-implementation-guide.md** - Step-by-step implementation instructions
3. **sales-documentation.md** - Complete semantic documentation
4. **sales-ontology.ttl** - TTL code for gmn_ontology.ttl
5. **sales-transform.py** - Python code for transformation script
6. **sales-doc-note.txt** - Documentation additions and examples

## Key Features

The Sales Contract implementation includes:

### 1. Core Transaction Properties
- **P70.1**: documents seller (E21_Person)
- **P70.2**: documents buyer (E21_Person)
- **P70.3**: documents transfer of (E18_Physical_Thing)

### 2. Legal Representatives
- **P70.4**: documents seller's procurator
- **P70.5**: documents buyer's procurator
- **P70.6**: documents seller's guarantor
- **P70.7**: documents buyer's guarantor

### 3. Transaction Facilitators
- **P70.8**: documents broker
- **P70.9**: documents payment provider for buyer
- **P70.10**: documents payment recipient for seller
- **P70.12**: documents payment through organization

### 4. References and Context
- **P70.11**: documents referenced person
- **P70.13**: documents referenced place
- **P70.14**: documents referenced object
- **P70.15**: documents witness

### 5. Monetary Information
- **P70.16**: documents sale price amount (xsd:decimal)
- **P70.17**: documents sale price currency (E98_Currency)

## Quick Start Checklist

### For Ontology Maintainers
- [ ] Review sales-documentation.md for semantic structure
- [ ] Verify TTL definitions in sales-ontology.ttl
- [ ] Check transformation code in sales-transform.py
- [ ] Test with sample data

### For Data Entry Users
- [ ] Understand the 17 sales contract properties
- [ ] Review transformation examples
- [ ] Configure Omeka-S resource templates
- [ ] Begin entering sales contract data

### For Developers
- [ ] Review transformation functions
- [ ] Understand E8_Acquisition structure
- [ ] Test with JSON-LD export
- [ ] Validate CIDOC-CRM output

## Implementation Summary

### Ontology Structure

**Class:**
```
gmn:E31_2_Sales_Contract
  ├── Subclass of: gmn:E31_1_Contract
  └── Documents: cidoc:E8_Acquisition
```

**Semantic Pattern:**
```
E31_2_Sales_Contract (the document)
  └─ P70_documents
      └─ E8_Acquisition (the transfer)
          ├─ P23_transferred_title_from → E21_Person (seller)
          ├─ P22_transferred_title_to → E21_Person (buyer)
          ├─ P24_transferred_title_of → E18_Physical_Thing (property)
          ├─ P177_assigned_property_of_type → E97_Monetary_Amount
          └─ P9_consists_of → E7_Activity (supporting actors)
```

### Transformation Pipeline

The transformation script processes sales contracts through these key functions:

1. **Core Properties** (P70.1-3): Transform to E8_Acquisition with P23/P22/P24
2. **Legal Representatives** (P70.4-7): Create E7_Activity sub-events with P17_was_motivated_by
3. **Transaction Facilitators** (P70.8-10, 12): Add actors to E8_Acquisition or sub-activities
4. **References** (P70.11, 13-14): Use P67_refers_to directly from document
5. **Witnesses** (P70.15): Add to E8_Acquisition with P11_had_participant
6. **Price** (P70.16-17): Create E97_Monetary_Amount with P181_has_amount and P180_has_currency

### File Structure

```
sales-deliverables/
├── README.md (this file)
├── sales-implementation-guide.md
├── sales-documentation.md
├── sales-ontology.ttl
├── sales-transform.py
└── sales-doc-note.txt
```

## Technical Requirements

- **Ontology Version**: 1.5+
- **CIDOC-CRM**: Compatible with CIDOC-CRM 7.1+
- **Python**: 3.6+ for transformation script
- **Dependencies**: JSON library for transformation
- **Platform**: Omeka-S 3.0+ for data entry

## Usage Scenarios

### Scenario 1: Simple Property Sale
Document a straightforward sale of a building from one person to another with price.

**Properties used**: P70.1, P70.2, P70.3, P70.16, P70.17

### Scenario 2: Sale with Legal Representatives
Document a sale where procurators represent both buyer and seller.

**Properties used**: P70.1, P70.2, P70.3, P70.4, P70.5, P70.16, P70.17

### Scenario 3: Complex Transaction
Document a sale with multiple supporting actors including guarantors, brokers, and payment intermediaries.

**Properties used**: All core + P70.6, P70.7, P70.8, P70.9, P70.10, P70.12

### Scenario 4: Sale with References
Document a sale referencing neighboring properties, previous owners, and related obligations.

**Properties used**: Core + P70.11, P70.13, P70.14, P70.15

## Relationship to Other Classes

Sales contracts interact with other GMN classes:

- **E22.1_Building**: Property being transferred (via P70.3)
- **E22.2_Moveable_Property**: Goods being transferred (via P70.3)
- **E31.1_Contract**: Parent class (generic contract)
- **E31.4_Cession_of_Rights_Contract**: Related transfer of rights
- **E31.7_Donation_Contract**: Similar to sale but gratuitous
- **E31.8_Dowry_Contract**: Similar to sale but marriage-related

## CIDOC-CRM Compliance

All shortcut properties transform to standard CIDOC-CRM:

- ✓ Uses E8_Acquisition for ownership transfer
- ✓ Uses E7_Activity for supporting actor activities
- ✓ Uses P67_refers_to for textual references
- ✓ Uses P177_assigned_property_of_type for price
- ✓ Uses E97_Monetary_Amount with P181/P180 for amounts
- ✓ Maintains proper entity typing throughout

## Validation and Testing

### Validation Checklist
- [ ] All TTL validates with RDF validators
- [ ] Python transformation code runs without errors
- [ ] Output validates against CIDOC-CRM ontology
- [ ] Test data transforms correctly
- [ ] No orphaned entities in output
- [ ] All URIs are properly formed

### Test Data Recommendations
1. Create simple sales contract with just buyer/seller/property
2. Add price information
3. Test with procurators and guarantors
4. Test with brokers and payment intermediaries
5. Test with referenced persons, places, and objects
6. Validate full transformation pipeline

## Support Information

If you encounter issues:

1. **Ontology questions**: Review sales-documentation.md for semantic details
2. **Implementation questions**: See sales-implementation-guide.md
3. **Transformation errors**: Check sales-transform.py code
4. **Data entry questions**: Refer to sales-doc-note.txt examples

## Version Information

- **Ontology Version**: 1.5
- **Creation Date**: 2025-10-17
- **Last Modified**: 2025-10-17
- **Classes Included**: 1 (E31_2_Sales_Contract)
- **Properties Included**: 17 (P70.1 through P70.17)
- **Transformation Functions**: 17 functions
- **Status**: Production-ready

## Related Documentation

This sales contract documentation is part of the broader GMN ontology that includes:
- General Contracts (E31.1) - parent class
- Arbitration Agreements (E31.3) - documented in arbitration_documentation.md
- Cession Contracts (E31.4) - documented in main ontology
- Declarations (E31.5) - documented in main ontology
- Correspondence (E31.6) - documented in correspondence_documentation.md
- Donation Contracts (E31.7) - documented in donation_documentation.md
- Dowry Contracts (E31.8) - documented in dowry_documentation.md

## Next Steps

After reviewing this package:

1. **Study the semantic documentation** in sales-documentation.md
2. **Follow the implementation guide** in sales-implementation-guide.md
3. **Review TTL definitions** in sales-ontology.ttl
4. **Examine transformation code** in sales-transform.py
5. **Check example documentation** in sales-doc-note.txt
6. **Test with sample data** before production use
7. **Configure Omeka-S templates** for data entry
8. **Train data entry staff** on property usage

## Contact

For questions about this implementation, refer to the Genoese Merchant Networks project documentation or contact the ontology maintainer.

---

**Document Status**: Complete  
**Package Version**: 1.0  
**Date**: 2025-10-26
