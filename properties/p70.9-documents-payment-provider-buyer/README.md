# GMN Ontology: P70.9 Documents Payment Provider for Buyer Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_9_documents_payment_provider_for_buyer` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-payer-for-buyer-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-payer-for-buyer-documentation.md** - Complete semantic documentation
4. **documents-payer-for-buyer-ontology.ttl** - Ready-to-copy TTL snippets
5. **documents-payer-for-buyer-transform.py** - Ready-to-copy Python code
6. **documents-payer-for-buyer-doc-note.txt** - Documentation examples and tables

---

## 🎯 Quick Start Checklist

### Phase 1: Ontology Update
- [ ] Open `gmn_ontology.ttl`
- [ ] Verify `gmn:P70_9_documents_payment_provider_for_buyer` property definition exists
- [ ] Confirm domain is `gmn:E31_2_Sales_Contract`
- [ ] Confirm range is `cidoc:E21_Person`
- [ ] Verify subPropertyOf `cidoc:P70_documents`
- [ ] Check AAT reference for payer role: `http://vocab.getty.edu/page/aat/300386048`

### Phase 2: Transformation Script Update
- [ ] Open `gmn_to_cidoc_transform.py`
- [ ] Add AAT_PAYER constant if not present: `AAT_PAYER = "http://vocab.getty.edu/page/aat/300386048"`
- [ ] Add AAT_FINANCIAL_TRANSACTION constant if not present: `AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/page/aat/300055984"`
- [ ] Locate or add `transform_p70_9_documents_payment_provider_for_buyer()` function
- [ ] Verify function creates E7_Activity with P2_has_type (financial transaction)
- [ ] Verify function adds P14_carried_out_by with P14.1_in_the_role_of (payer)
- [ ] Add function call in `transform_item()` after P70.8 transformation

### Phase 3: Documentation Update
- [ ] Open main documentation file
- [ ] Add P70.9 property to Sales Contract properties table
- [ ] Include transformation pattern and example
- [ ] Update table of contents if applicable

### Phase 4: Testing
- [ ] Create test contract with payment provider
- [ ] Run transformation script
- [ ] Verify E8_Acquisition node created
- [ ] Verify E7_Activity node created with financial transaction type
- [ ] Verify P14_carried_out_by links to payment provider
- [ ] Verify P14.1_in_the_role_of points to AAT payer concept
- [ ] Validate output against CIDOC-CRM specifications

---

## 📋 Property Overview

**Property Name**: `gmn:P70_9_documents_payment_provider_for_buyer`

**Label**: "P70.9 documents payment provider for buyer"

**Purpose**: Associates a sales contract with a third party who provides the payment (funds) on behalf of the buyer.

**Domain**: `gmn:E31_2_Sales_Contract`

**Range**: `cidoc:E21_Person`

**Super-property**: `cidoc:P70_documents`

**Key Distinction**: Unlike procurators (legal representatives), guarantors (security providers), or brokers (facilitators), payment providers are third parties who supply the actual funds for the purchase on behalf of the buyer.

---

## 🔄 Transformation Pattern

```
gmn:P70_9_documents_payment_provider_for_buyer
    ↓ transforms to ↓
cidoc:P70_documents > cidoc:E8_Acquisition > 
    cidoc:P9_consists_of > cidoc:E7_Activity >
        cidoc:P2_has_type > AAT:Financial_Transaction
        cidoc:P14_carried_out_by > cidoc:E21_Person (Payment Provider)
        cidoc:P14.1_in_the_role_of > AAT:Payer
```

---

## 💡 Use Cases

1. **Family Support**: A father provides funds for his son's land purchase
2. **Business Partnerships**: A business partner supplies capital for a colleague's acquisition
3. **Creditor Arrangements**: A creditor provides funds directly to facilitate a transaction
4. **Institutional Financing**: A bank or financial institution provides payment on behalf of a buyer

---

## 🔗 Related Properties

- **P70.1** `documents_seller` - The party transferring ownership
- **P70.2** `documents_buyer` - The party receiving ownership (on whose behalf payment is made)
- **P70.5** `documents_buyers_procurator` - Legal representative (not payment provider)
- **P70.7** `documents_buyers_guarantor` - Security provider (not payment provider)
- **P70.10** `documents_payment_recipient_for_seller` - Receives payment on seller's behalf
- **P70.12** `documents_payment_through_organization` - Organization facilitating payment

---

## ⚠️ Important Notes

- Payment providers supply actual funds, distinguishing them from legal representatives or guarantors
- The transformation creates an E7_Activity typed as a financial transaction
- The payment provider receives the AAT "payer" role designation
- Multiple payment providers can be specified for a single contract
- This property is specific to sales contracts and represents a convenience for data entry

---

## 📚 Additional Resources

- CIDOC-CRM Documentation: http://www.cidoc-crm.org/
- Getty AAT for Payer: http://vocab.getty.edu/page/aat/300386048
- Getty AAT for Financial Transaction: http://vocab.getty.edu/page/aat/300055984

---

## 🆘 Support

For implementation questions or issues:
1. Review the implementation guide (documents-payer-for-buyer-implementation-guide.md)
2. Check the semantic documentation (documents-payer-for-buyer-documentation.md)
3. Examine transformation examples in the documentation

---

**Package Version**: 1.0  
**Created**: October 2025  
**Ontology Version**: GMN 1.0  
**CIDOC-CRM Version**: 7.1.1
