# GMN Ontology: P70.12 Documents Payment Through Organization Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_12_documents_payment_through_organization` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-payment-org-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-payment-org-documentation.md** - Complete semantic documentation
4. **documents-payment-org-ontology.ttl** - TTL snippets for the ontology file
5. **documents-payment-org-transform.py** - Python code for transformation script
6. **documents-payment-org-doc-note.txt** - Examples and tables for documentation

---

## 🎯 Property Overview

### Purpose
The `gmn:P70_12_documents_payment_through_organization` property associates a sales contract with an organization (typically a bank) through which payment for the transaction is made or facilitated. This captures financial institutions that serve as intermediaries in the payment process, such as banks holding deposits, making transfers, or providing credit facilities.

### Key Characteristics
- **Domain:** `gmn:E31_2_Sales_Contract`
- **Range:** `cidoc:E74_Group` (organizations)
- **Superproperty:** `cidoc:P70_documents`
- **Cardinality:** Zero or many (multiple organizations may facilitate payment)

### Transformation Path
The property represents a simplified version of:
```
E31_Document 
  → P70_documents 
    → E8_Acquisition 
      → P9_consists_of 
        → E7_Activity (payment facilitation activity)
          → P14_carried_out_by 
            → E74_Group (financial institution)
```

---

## ⚡ Quick Start Checklist

### Phase 1: Ontology Update
- [ ] Add TTL definition to `gmn_ontology.ttl` (see `documents-payment-org-ontology.ttl`)
- [ ] Validate TTL syntax
- [ ] Commit changes to version control

### Phase 2: Transformation Script Update
- [ ] Add transformation function to `gmn_to_cidoc_transform.py` (see `documents-payment-org-transform.py`)
- [ ] Add function call to `transform_gmn_to_cidoc()` pipeline
- [ ] Test transformation with sample data

### Phase 3: Documentation Update
- [ ] Add property documentation to main text files
- [ ] Include examples from `documents-payment-org-doc-note.txt`
- [ ] Update property index/table of contents

### Phase 4: Testing & Validation
- [ ] Test with organization URI references
- [ ] Test with inline organization data
- [ ] Test with multiple organizations
- [ ] Verify P67_refers_to structure is created correctly
- [ ] Validate output against CIDOC-CRM standards

---

## 📊 Implementation Summary

### What This Property Does
- **Captures** organizations that facilitate payment in sales transactions
- **Represents** financial intermediaries (banks, transfer agencies, credit institutions)
- **Distinguishes** from principal parties (buyer/seller) and individual agents (procurators/guarantors)
- **Transforms** to proper CIDOC-CRM relationship: P67_refers_to > E74_Group

### Design Decisions

#### Why P67_refers_to Instead of P9_consists_of?
The property uses **P67_refers_to** rather than creating payment activities because:
- Organizations are **referenced** in the contract but don't actively participate in the documented transaction
- The contract mentions the bank as a payment mechanism, not as a transaction participant
- This is similar to referenced persons (P70.11) and referenced places (P70.13)
- P67 captures textual presence without implying active participation

#### Relationship to Other Properties
- **P70.9 (payment provider for buyer):** Individual person who provides funds on behalf of buyer
- **P70.10 (payment recipient for seller):** Individual person who receives funds on behalf of seller
- **P70.12 (payment through organization):** Organization (bank) facilitating the payment mechanism
- These are complementary and can co-exist in a single contract

---

## 🔧 Technical Notes

### Data Entry Format
```json
{
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_12_documents_payment_through_organization": [
    {
      "@id": "http://example.org/organization/banco_di_san_giorgio",
      "@type": "cidoc:E74_Group",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Banco di San Giorgio"
      }
    }
  ]
}
```

### After Transformation
```json
{
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "http://example.org/organization/banco_di_san_giorgio",
      "@type": "cidoc:E74_Group",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "cidoc:P190_has_symbolic_content": "Banco di San Giorgio"
      }
    }
  ]
}
```

---

## 📚 Usage Examples

### Example 1: Simple Bank Reference
```turtle
:contract_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_12_documents_payment_through_organization :banco_san_giorgio .

:banco_san_giorgio a cidoc:E74_Group ;
    cidoc:P1_is_identified_by [
        a cidoc:E41_Appellation ;
        cidoc:P190_has_symbolic_content "Banco di San Giorgio"
    ] .
```

### Example 2: Multiple Financial Institutions
```turtle
:contract_002 a gmn:E31_2_Sales_Contract ;
    gmn:P70_12_documents_payment_through_organization :banco_san_giorgio ,
                                                        :casa_credito_genova .
```

### Example 3: With Other Payment Roles
```turtle
:contract_003 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller :giovanni_doria ;
    gmn:P70_2_documents_buyer :pietro_spinola ;
    gmn:P70_9_documents_payment_provider_for_buyer :luca_spinola ;
    gmn:P70_12_documents_payment_through_organization :banco_san_giorgio .
```

---

## 🚨 Common Pitfalls

1. **Don't confuse with individual payment roles**
   - Use P70.12 for **organizations** (banks, financial houses)
   - Use P70.9/P70.10 for **individual persons** providing/receiving payment

2. **Don't create payment activities**
   - This property uses P67_refers_to (reference)
   - It does NOT create P9_consists_of structures
   - The organization is mentioned, not an active participant

3. **Don't mix with guarantors**
   - Guarantors (P70.6/P70.7) provide security for obligations
   - Payment organizations facilitate the transfer mechanism
   - These are distinct roles

---

## 📖 For More Information

- See **documents-payment-org-implementation-guide.md** for detailed implementation steps
- See **documents-payment-org-documentation.md** for complete semantic documentation
- See **documents-payment-org-doc-note.txt** for documentation examples

---

## 📅 Version Information

- **Created:** 2025-10-17
- **Property URI:** `http://www.genoesemerchantnetworks.com/ontology#P70_12_documents_payment_through_organization`
- **Package Version:** 1.0
- **Last Updated:** 2025-10-27
