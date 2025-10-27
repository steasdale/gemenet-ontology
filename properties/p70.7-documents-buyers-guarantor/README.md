# GMN Ontology: P70.7 Documents Buyer's Guarantor Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_7_documents_buyers_guarantor` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-buyers-guarantor-implementation-guide.md** - Step-by-step implementation instructions with code snippets and testing procedures
3. **documents-buyers-guarantor-documentation.md** - Complete semantic documentation with class definitions, property specifications, and transformation examples
4. **documents-buyers-guarantor-ontology.ttl** - Ready-to-copy TTL snippets for the main ontology file
5. **documents-buyers-guarantor-transform.py** - Ready-to-copy Python code for the transformation script
6. **documents-buyers-guarantor-doc-note.txt** - Examples and tables to add to the main documentation

---

## 🎯 Property Overview

**Property Name:** `gmn:P70_7_documents_buyers_guarantor`

**Label:** "P70.7 documents buyer's guarantor"

**Purpose:** Simplified property for associating a sales contract with the person named as the guarantor for the buyer.

**CIDOC-CRM Path:** E31_Document > P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (guarantor), with P17_was_motivated_by linking to the buyer (E21_Person)

**Role in System:** This property provides a convenient shortcut for data entry that is automatically transformed into the full CIDOC-CRM compliant structure. Guarantors provide security for the transaction by promising to fulfill obligations if the buyer defaults on their commitments.

---

## ⚡ Quick-Start Checklist

### For Ontology Update:
- [ ] Copy TTL snippet from `documents-buyers-guarantor-ontology.ttl`
- [ ] Paste into main ontology file (`gmn_ontology.ttl`) in the P70 properties section
- [ ] Verify proper indentation and syntax
- [ ] Commit changes with message: "Add P70.7 documents buyer's guarantor property"

### For Transformation Script Update:
- [ ] Copy function from `documents-buyers-guarantor-transform.py`
- [ ] Paste into transformation script (`gmn_to_cidoc_transform.py`) after P70.6 guarantor function
- [ ] Add function call to main `transform_item()` in proper sequence
- [ ] Verify AAT_GUARANTOR constant exists
- [ ] Run test cases to verify transformation
- [ ] Commit changes with message: "Add P70.7 buyer's guarantor transformation"

### For Documentation Update:
- [ ] Review examples in `documents-buyers-guarantor-doc-note.txt`
- [ ] Add to main documentation file in P70 properties section
- [ ] Include semantic pattern explanation
- [ ] Add example contracts showing guarantor usage
- [ ] Update property table with P70.7 entry

### For Testing:
- [ ] Create test contract with buyer's guarantor
- [ ] Run transformation script
- [ ] Verify E7_Activity node creation
- [ ] Verify P14_carried_out_by links to guarantor
- [ ] Verify P17_was_motivated_by links to buyer
- [ ] Verify role assignment (AAT_GUARANTOR)
- [ ] Test with multiple guarantors
- [ ] Test with missing buyer (should handle gracefully)

---

## 🔄 Implementation Summary

### Semantic Pattern

The property follows the guarantor pattern established for both buyer and seller guarantors:

```
E31_Document (Sales Contract)
  ├─ P70_documents → E8_Acquisition
      └─ P9_consists_of → E7_Activity (Guaranteeing Activity)
          ├─ P14_carried_out_by → E21_Person (Guarantor)
          │   └─ P14.1_in_the_role_of → E55_Type (AAT: guarantor)
          └─ P17_was_motivated_by → E21_Person (Buyer being guaranteed)
```

### Key Features

- **Shortcut Property**: Provides simple data entry interface
- **Automatic Transformation**: Converts to full CIDOC-CRM structure
- **Role Specification**: Uses Getty AAT term for guarantor (300025614)
- **Buyer Linkage**: Explicitly connects guarantor to the buyer they guarantee
- **Multiple Guarantors**: Supports multiple guarantor persons
- **Activity Pattern**: Uses E7_Activity to represent the guaranteeing action

### Distinction from Other Roles

- **vs. Procurator**: Guarantor provides security/backup, not legal representation
- **vs. Broker**: Guarantor guarantees one party, not facilitates between both
- **vs. Payment Provider**: Guarantor promises future payment if needed, not provides current funds
- **vs. Seller's Guarantor**: This property specifically guarantees the buyer's obligations

---

## 📋 Implementation Files

### 1. Ontology File (`documents-buyers-guarantor-ontology.ttl`)
Contains the complete TTL definition including:
- Property declaration
- Labels and comments
- Domain and range specifications
- Subproperty relationships
- See Also references
- Creation date metadata

### 2. Python Transformation (`documents-buyers-guarantor-transform.py`)
Contains:
- Transform function definition
- Generic guarantor transformation helper (if not present)
- AAT constant verification
- Integration with main transform pipeline

### 3. Documentation (`documents-buyers-guarantor-documentation.md`)
Comprehensive semantic documentation including:
- Detailed property definition
- CIDOC-CRM path explanation
- Use cases and examples
- Transformation logic description
- Testing guidelines
- Common patterns and edge cases

### 4. Implementation Guide (`documents-buyers-guarantor-implementation-guide.md`)
Step-by-step instructions for:
- Adding property to ontology
- Implementing transformation function
- Testing the implementation
- Troubleshooting common issues
- Integration with existing codebase

### 5. Documentation Note (`documents-buyers-guarantor-doc-note.txt`)
Ready-to-insert content for main documentation:
- Property table entry
- Usage examples
- Historical context
- Sample contracts

---

## 🔍 Key Concepts

### What is a Guarantor?

A guarantor is a person who provides security for a transaction by promising to fulfill the obligations of one of the principal parties (in this case, the buyer) if that party defaults. This was common in historical contracts where the buyer's financial reliability needed additional assurance.

### Guarantor vs. Other Roles

| Role | Function | Representation in CIDOC-CRM |
|------|----------|----------------------------|
| **Guarantor** | Provides security/backup for buyer | E7_Activity with P17 to buyer |
| **Procurator** | Acts as legal representative for buyer | E7_Activity with P17 to buyer |
| **Broker** | Facilitates transaction between parties | Direct P14 on E8_Acquisition |
| **Payment Provider** | Provides funds for buyer | E7_Activity with P17 to buyer |

### Why Use E7_Activity?

The E7_Activity node represents the "act of guaranteeing" and allows us to:
1. Link the guarantor (who performs the activity) via P14_carried_out_by
2. Link to the buyer being guaranteed via P17_was_motivated_by
3. Specify the role using P14.1_in_the_role_of
4. Keep the guaranteeing activity separate from the main acquisition

---

## 🧪 Testing Checklist

### Basic Functionality
- [ ] Property transforms correctly for single guarantor
- [ ] Property transforms correctly for multiple guarantors
- [ ] E7_Activity node is created with unique URI
- [ ] P14_carried_out_by links to guarantor correctly
- [ ] P17_was_motivated_by links to buyer correctly
- [ ] Role specification uses correct AAT URI

### Edge Cases
- [ ] Missing buyer (P22_transferred_title_to not present)
- [ ] Guarantor with minimal data (URI only)
- [ ] Guarantor with full person data
- [ ] Multiple guarantors for same buyer
- [ ] Empty guarantor list

### Integration
- [ ] Works alongside P70.6 (seller's guarantor)
- [ ] Works with other P70 properties
- [ ] Doesn't interfere with existing transformations
- [ ] Properly removes shortcut property after transformation

---

## 📚 Related Properties

- `gmn:P70_6_documents_sellers_guarantor` - Guarantor for seller
- `gmn:P70_5_documents_buyers_procurator` - Procurator for buyer
- `gmn:P70_4_documents_sellers_procurator` - Procurator for seller
- `gmn:P70_2_documents_buyer` - The buyer being guaranteed
- `gmn:P70_9_documents_payment_provider_for_buyer` - Payment provider for buyer

---

## 🔗 External References

- **CIDOC-CRM Documentation**: http://www.cidoc-crm.org/
- **Getty AAT - Guarantor**: http://vocab.getty.edu/page/aat/300025614
- **Getty AAT - Agent**: http://vocab.getty.edu/page/aat/300025972

---

## 📝 Version Information

- **Created**: 2025-10-17
- **Property ID**: P70.7
- **Parent Property**: cidoc:P70_documents
- **Domain**: gmn:E31_2_Sales_Contract
- **Range**: cidoc:E21_Person

---

## ⚠️ Important Notes

1. **Transformation Required**: This shortcut property MUST be transformed to full CIDOC-CRM structure before final export
2. **Role Assignment**: Always uses AAT_GUARANTOR constant (300025614)
3. **Buyer Dependency**: The transformation works best when P22_transferred_title_to (buyer) is present
4. **Multiple Guarantors**: Each guarantor gets their own E7_Activity node
5. **Activity URI**: Generated using hash of guarantor URI and property name for uniqueness

---

## 🚀 Getting Started

1. Read the **Implementation Guide** for detailed step-by-step instructions
2. Review the **Documentation** for semantic understanding
3. Copy code from **ontology.ttl** and **transform.py** files
4. Run test cases to verify implementation
5. Update main documentation using **doc-note.txt**

---

## 📞 Support

For questions or issues:
- Review the comprehensive documentation in this package
- Check existing implementations of P70.6 (seller's guarantor) as reference
- Consult CIDOC-CRM documentation for semantic questions
- Test thoroughly before deploying to production

---

**Package Version**: 1.0  
**Generated**: 2025-10-27  
**Property**: gmn:P70_7_documents_buyers_guarantor
