# GMN Ontology: P70.22 Indicates Receiving Party Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_22_indicates_receiving_party` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **indicates-receiving-party-implementation-guide.md** - Detailed implementation instructions with code snippets
3. **indicates-receiving-party-documentation.md** - Complete semantic documentation and transformation examples
4. **indicates-receiving-party-ontology.ttl** - Ready-to-copy TTL snippets for the main ontology file
5. **indicates-receiving-party-transform.py** - Ready-to-copy Python code for the transformation script
6. **indicates-receiving-party-doc-note.txt** - Examples and tables for documentation text files

---

## 🎯 Property Overview

**Property URI**: `gmn:P70_22_indicates_receiving_party`

**Label**: "P70.22 indicates receiving party" (English)

**Purpose**: Simplified property for associating a document with the person or entity receiving something in the documented activity. This is a multi-purpose property used across four different document types with context-dependent semantics.

**Document Types Supported**:
- **Cession of Rights Contracts** (`gmn:E31_4_Cession_of_Rights_Contract`) - party receiving the ceded rights
- **Declarations** (`gmn:E31_5_Declaration`) - party to whom the declaration is addressed
- **Donation Contracts** (`gmn:E31_7_Donation_Contract`) - donee receiving the donated property
- **Dowry Contracts** (`gmn:E31_8_Dowry_Contract`) - party receiving the dowry property

**CIDOC-CRM Transformation Paths**:
- **For Declarations**: `E31_Document > P70_documents > E7_Activity > P01_has_domain > E39_Actor`
- **For Cessions, Donations, and Dowries**: `E31_Document > P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor`

---

## ✅ Quick-Start Implementation Checklist

### Phase 1: Ontology Update
- [ ] Open `gmn_ontology.ttl`
- [ ] Locate the property definition section for P70.22
- [ ] Replace existing definition with updated version from `indicates-receiving-party-ontology.ttl`
- [ ] Verify TTL syntax with validator
- [ ] Commit changes with message: "Updated P70.22 indicates receiving party property"

### Phase 2: Python Transformation Script Update
- [ ] Open `gmn_to_cidoc_transform.py`
- [ ] Locate the `transform_p70_22_indicates_receiving_party()` function
- [ ] Replace existing function with version from `indicates-receiving-party-transform.py`
- [ ] Update `transform_item()` to ensure function is called
- [ ] Verify imports include `uuid` module

### Phase 3: Testing
- [ ] Create test data for each document type (cession, declaration, donation, dowry)
- [ ] Run transformation script on test data
- [ ] Verify correct CIDOC-CRM paths for each document type
- [ ] Check that E8_Acquisition is used for cessions, donations, and dowries
- [ ] Check that E7_Activity is used for declarations
- [ ] Validate all output URIs are properly generated

### Phase 4: Documentation Updates
- [ ] Review `indicates-receiving-party-doc-note.txt`
- [ ] Add examples to relevant documentation files:
  - Cession of rights documentation
  - Declaration documentation
  - Donation documentation (`donation-documentation.md`)
  - Dowry documentation (`dowry-documentation.md`)
- [ ] Update comparison tables if present
- [ ] Add cross-references between related properties

### Phase 5: Validation and Deployment
- [ ] Run full test suite
- [ ] Validate transformed output against CIDOC-CRM specification
- [ ] Review edge cases (multiple receiving parties, complex document types)
- [ ] Deploy to production environment
- [ ] Update user-facing documentation

---

## 📊 Implementation Summary

### Key Characteristics

1. **Multi-Context Property**: Unlike most GMN shortcut properties that serve a single document type, P70.22 is shared across four different document types with semantically appropriate transformations for each.

2. **Dual Transformation Paths**: 
   - **E8_Acquisition Path** (for ownership/rights transfer): Used for cessions, donations, and dowries where the receiving party acquires ownership or legal rights
   - **E7_Activity Path** (for communication): Used for declarations where the recipient is the target/addressee of the communication

3. **Semantic Precision**: The transformation intelligently determines which CIDOC-CRM path to use based on the document type, ensuring semantic accuracy.

### Integration Points

**Related Properties**:
- `gmn:P70_21_indicates_conceding_party` - Complementary property for cessions (the party transferring rights)
- `gmn:P70_32_indicates_donor` - Complementary property for donations and dowries (the party giving property)
- `gmn:P70_23_indicates_object_of_cession` - Specifies what rights are being transferred in cessions
- `gmn:P70_33_indicates_object_of_donation` - Specifies what property is being donated
- `gmn:P70_34_indicates_object_of_dowry` - Specifies what property is being transferred as dowry

**Shared E8_Acquisition Node**:
For donations and dowries, the transformation creates or references a shared E8_Acquisition node that connects:
- P23 (donor) via `P70_32_indicates_donor`
- P22 (receiving party) via `P70_22_indicates_receiving_party`
- P24 (object) via `P70_33_indicates_object_of_donation` or `P70_34_indicates_object_of_dowry`

### Common Use Cases

1. **Cession Contract**: Recording the party acquiring rights in a rights transfer agreement
2. **Declaration Document**: Identifying the addressee or target of a formal declaration
3. **Donation Contract**: Documenting the donee (recipient) of gifted property
4. **Dowry Contract**: Identifying the spouse or couple receiving dowry property in a marriage arrangement

---

## 🔍 Property Semantics by Document Type

### In Cession of Rights Contracts
The receiving party is the actor who **acquires legal rights** being transferred. This could be:
- Rights to collect debts
- Usufruct rights
- Ownership rights
- Contractual claims
- Any other legal interests

### In Declarations
The receiving party is the **addressee or target** of the declaration. This is:
- The party to whom the statement is directed
- Often the party affected by the declaration
- Distinct from the declarant (who makes the declaration)

### In Donation Contracts
The receiving party is the **donee** - the beneficiary who receives donated property without payment. This could be:
- Religious institutions
- Family members
- Charitable organizations
- Any party receiving a voluntary gift

### In Dowry Contracts
The receiving party is the **spouse or couple** who receives dowry property as part of a marriage arrangement. This is:
- Often the husband or the married couple jointly
- Distinguished from the donor (often a parent or family member)
- Part of a specific marriage context

---

## 🚀 Quick Implementation Example

### Input (Shortcut Form)
```turtle
<donation001> a gmn:E31_7_Donation_Contract ;
    gmn:P70_32_indicates_donor <widow_maria> ;
    gmn:P70_22_indicates_receiving_party <hospital_pammatone> ;
    gmn:P70_33_indicates_object_of_donation <building_chapel> .
```

### Output (CIDOC-CRM Compliant)
```turtle
<donation001> a gmn:E31_7_Donation_Contract ;
    cidoc:P70_documents <donation001/acquisition> .

<donation001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <widow_maria> ;
    cidoc:P22_transferred_title_to <hospital_pammatone> ;
    cidoc:P24_transferred_title_of <building_chapel> .
```

---

## 📚 Additional Resources

- **CIDOC-CRM Documentation**: http://www.cidoc-crm.org/
- **P22 transferred title to**: Used in acquisition transformations
- **P01 has domain**: Used in declaration transformations
- **GMN Ontology Documentation**: See project documentation files
- **Related Document Types**: See `donation-documentation.md`, `dowry-documentation.md`

---

## 🆘 Support and Troubleshooting

### Common Issues

1. **Wrong transformation path**: Ensure document type is correctly specified with proper class URI
2. **Missing E8_Acquisition**: Check that acquisition node is created before adding P22 relationships
3. **Type conflicts**: Verify that only one document type is assigned to each document instance

### Validation Checklist

✓ Property definition includes all four document types in domain union  
✓ Transformation function checks document type before selecting path  
✓ E8_Acquisition nodes are properly shared across related properties  
✓ Actor instances have proper E39_Actor typing  
✓ URIs are consistently generated using document base URI  

---

## 📝 Version Information

**Property Created**: 2025-10-18  
**Last Modified**: 2025-10-25  
**Deliverables Package Created**: 2025-10-28  
**Compatible with**: GMN Ontology v1.0+, CIDOC-CRM v7.1+

---

## 📄 License and Attribution

This deliverables package is part of the GMN (Genoese Merchants Network) Ontology project.

For questions or clarifications, please refer to the complete documentation files included in this package.
