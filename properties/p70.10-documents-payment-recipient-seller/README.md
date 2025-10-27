# GMN Ontology: P70.10 Documents Payment Recipient for Seller Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_10_documents_payment_recipient_for_seller` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-payee-for-seller-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-payee-for-seller-documentation.md** - Complete semantic documentation
4. **documents-payee-for-seller-ontology.ttl** - TTL snippets for the ontology file
5. **documents-payee-for-seller-transform.py** - Python code for the transformation script
6. **documents-payee-for-seller-doc-note.txt** - Documentation examples and tables

---

## 🎯 Quick Start Checklist

### Implementation Steps
- [ ] Review semantic documentation in `documents-payee-for-seller-documentation.md`
- [ ] Add TTL definitions from `documents-payee-for-seller-ontology.ttl` to `gmn_ontology.ttl`
- [ ] Add Python transformation function from `documents-payee-for-seller-transform.py` to `gmn_to_cidoc_transform.py`
- [ ] Register transformation in the main `transform_item()` function
- [ ] Add documentation examples from `documents-payee-for-seller-doc-note.txt` to documentation files
- [ ] Test with sample data
- [ ] Validate transformed output

---

## 📋 Property Summary

### Simplified Property
**URI**: `gmn:P70_10_documents_payment_recipient_for_seller`  
**Label**: "P70.10 documents payment recipient for seller"  
**Domain**: `gmn:E31_2_Sales_Contract`  
**Range**: `cidoc:E21_Person`

### Purpose
Associates a sales contract with a third party who receives the payment (funds) on behalf of the seller. Payment recipients are distinct from:
- **Procurators**: Legal representatives who act on behalf of a party
- **Guarantors**: Security providers who promise to fulfill obligations
- **Brokers**: Transaction facilitators who arrange the sale

Payment recipients are third parties who actually receive the funds from the purchase on behalf of the seller, often family members, business partners, or creditors to whom the seller owes money.

### CIDOC-CRM Transformation
The simplified property transforms to:
```
E31_Document 
  → P70_documents 
    → E8_Acquisition 
      → P9_consists_of 
        → E7_Activity [Financial Transaction]
          → P14_carried_out_by → E21_Person (payment recipient)
          → P14.1_in_the_role_of → E55_Type (AAT: payee)
```

The transformation creates an E7_Activity node representing the payment receipt activity, with the payment recipient as the actor carrying out this activity in the role of "payee".

---

## 🔗 Complementary Property

The property works in conjunction with:
- **`gmn:has_payment_received_by`**: Direct relationship from seller (E21_Person) to payment recipient (E21_Person)
  - Domain: `cidoc:E21_Person`
  - Range: `cidoc:E21_Person`
  - Used in Omeka-S annotations to directly link sellers with their payment recipients

---

## 💡 Use Cases

### Typical Scenarios
1. **Family Member Recipients**: Son receives payment on behalf of elderly father selling property
2. **Business Partner Recipients**: Business partner collects payment for seller's share
3. **Creditor Recipients**: Creditor receives payment directly to settle seller's debt
4. **Agent Recipients**: Authorized agent collects funds on seller's behalf

### Example (Simplified Structure)
```turtle
sales_contract:123 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller person:Giovanni ;
    gmn:P70_2_documents_buyer person:Marco ;
    gmn:P70_10_documents_payment_recipient_for_seller person:Antonio .

person:Giovanni gmn:has_payment_received_by person:Antonio .
```

### Example (After Transformation)
```turtle
sales_contract:123 a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents acquisition:123 .

acquisition:123 a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from person:Giovanni ;
    cidoc:P22_transferred_title_to person:Marco ;
    cidoc:P9_consists_of activity:payment_abc123 .

activity:payment_abc123 a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417629> ; # financial transaction
    cidoc:P14_carried_out_by person:Antonio ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/aat/300025555> . # payee
```

---

## 🧪 Testing Checklist

### Validation Tests
- [ ] Property appears in ontology with correct domain/range
- [ ] Property has correct subPropertyOf relationship
- [ ] Transformation creates E7_Activity node
- [ ] Activity has correct type (AAT financial transaction)
- [ ] Activity links to payment recipient via P14_carried_out_by
- [ ] Activity includes P14.1_in_the_role_of with AAT payee concept
- [ ] Activity is properly nested in E8_Acquisition via P9_consists_of
- [ ] Original simplified property is removed after transformation
- [ ] Multiple payment recipients are handled correctly
- [ ] Transformation works with both URI strings and object dictionaries

---

## 📚 Additional Resources

### Related Properties
- `gmn:P70_1_documents_seller` - The seller whose payment is being received
- `gmn:P70_9_documents_payment_provider_for_buyer` - Parallel property for buyer's payment provider
- `gmn:has_payment_received_by` - Direct seller-to-recipient relationship

### AAT Concepts Used
- **Financial Transaction**: http://vocab.getty.edu/aat/300417629
- **Payee**: http://vocab.getty.edu/aat/300025555

### CIDOC-CRM Properties Used
- `cidoc:P70_documents` - Documents an event
- `cidoc:P9_consists_of` - Links acquisition to constituent activities
- `cidoc:P14_carried_out_by` - Links activity to actor
- `cidoc:P14.1_in_the_role_of` - Specifies role of actor
- `cidoc:P2_has_type` - Classifies the activity

---

## 📝 Implementation Notes

### Key Considerations
1. **Role Clarity**: Payment recipients receive funds but are not legal representatives
2. **Activity Modeling**: Each payment recipient creates a separate E7_Activity node
3. **Hash Generation**: Activity URIs use hash of recipient URI + 'payment_recipient' for uniqueness
4. **AAT Integration**: Uses standard AAT concepts for financial transactions and roles
5. **Multiple Recipients**: Supports multiple payment recipients per contract
6. **Data Formats**: Handles both simple URI strings and complex object dictionaries

### Common Patterns
- Payment recipient often appears alongside seller in family relationship
- May be accompanied by notarial attestation of authorization
- Often documented with specific payment amounts or conditions
- May indicate creditor-debtor relationships

---

## 🚀 Getting Started

1. **Read** `documents-payee-for-seller-documentation.md` for complete semantic understanding
2. **Follow** `documents-payee-for-seller-implementation-guide.md` for step-by-step implementation
3. **Copy** code snippets from TTL and Python files
4. **Test** with your sample data
5. **Validate** output against CIDOC-CRM standards

---

## 📅 Version Information

- **Property Created**: 2025-10-17
- **Package Created**: 2025-10-27
- **Deliverables Version**: 1.0

---

## 📧 Support

For questions or issues with implementation:
1. Review the detailed implementation guide
2. Check the semantic documentation for use cases
3. Examine the code comments in the Python transformation function
4. Validate against the test checklist

---

*This package provides everything needed to implement the payment recipient for seller property in your GMN ontology project.*
