# GMN Ontology: P70.17 Documents Sale Price Currency Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_17_documents_sale_price_currency` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-price-currency-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-price-currency-documentation.md** - Complete semantic documentation
4. **documents-price-currency-ontology.ttl** - TTL snippets for ontology file
5. **documents-price-currency-transform.py** - Python code for transformation script
6. **documents-price-currency-doc-note.txt** - Examples and tables for documentation

---

## 🎯 Quick Overview

**Property:** `gmn:P70_17_documents_sale_price_currency`

**Purpose:** Simplified property for expressing the currency unit of the sale price documented in a sales contract.

**Domain:** `gmn:E31_2_Sales_Contract`

**Range:** `cidoc:E98_Currency`

**CIDOC-CRM Path:**
```
E31_Document 
  > P70_documents 
  > E8_Acquisition 
  > P177_assigned_property_of_type 
  > E97_Monetary_Amount 
  > P180_has_currency 
  > E98_Currency
```

**Companion Property:** Works together with `gmn:P70_16_documents_sale_price_amount` to fully document sale prices.

---

## ✅ Quick-Start Checklist

### For Ontology Implementation:
- [ ] Copy TTL snippets from `documents-price-currency-ontology.ttl`
- [ ] Add to main `gmn_ontology.ttl` file after P70.16 property definition
- [ ] Verify property IRI: `gmn:P70_17_documents_sale_price_currency`
- [ ] Verify domain: `gmn:E31_2_Sales_Contract`
- [ ] Verify range: `cidoc:E98_Currency`
- [ ] Check property relationships with P70_16

### For Transformation Script:
- [ ] Copy function from `documents-price-currency-transform.py`
- [ ] Add to `gmn_to_cidoc_transform.py` after `transform_p70_16_documents_sale_price_amount()`
- [ ] Add function call in `transform_item()` after P70.16 transformation
- [ ] Import required modules (uuid already imported)
- [ ] Verify integration with P70.16 (amount) transformation

### For Documentation:
- [ ] Review complete semantic docs in `documents-price-currency-documentation.md`
- [ ] Copy examples from `documents-price-currency-doc-note.txt`
- [ ] Add to main documentation file in Sales Contract Properties section
- [ ] Include transformation examples and testing scenarios

### For Testing:
- [ ] Create test case with currency only (e.g., lira_genovese)
- [ ] Create test case with both amount and currency
- [ ] Test URI generation for E97_Monetary_Amount
- [ ] Verify P180_has_currency structure
- [ ] Test with multiple currency types (lira, florin, ducat)
- [ ] Verify integration with existing E8_Acquisition nodes

---

## 🔧 Implementation Priority

**High Priority** - This property is essential for:
- Documenting monetary values in sales contracts
- Recording historical currency types (lira genovese, florin, ducat, etc.)
- Working with P70.16 to provide complete price information
- Economic analysis of medieval transactions

---

## 📊 Key Features

1. **Currency Documentation**: Captures historical currency types used in sales
2. **E97_Monetary_Amount Integration**: Creates proper monetary amount structure
3. **Flexible Currency References**: Supports both URI and literal currency values
4. **Acquisition Coordination**: Integrates with existing E8_Acquisition nodes
5. **Amount Pairing**: Works seamlessly with P70.16 for complete price data

---

## 🔗 Related Properties

- **P70.16** (`gmn:P70_16_documents_sale_price_amount`) - Numeric amount companion
- **P177** (`cidoc:P177_assigned_property_of_type`) - Property assignment
- **P180** (`cidoc:P180_has_currency`) - Currency specification
- **P181** (`cidoc:P181_has_amount`) - Amount specification (from P70.16)

---

## 📝 Common Currency Types

Historical currencies commonly found in Genoese records:
- Lira genovese (Genoese pound)
- Florin
- Ducat
- Soldo
- Denaro

---

## 🚀 Getting Started

1. **Read the Implementation Guide** (`documents-price-currency-implementation-guide.md`)
   - Follow step-by-step instructions
   - Review code snippets
   - Understand testing procedures

2. **Review Semantic Documentation** (`documents-price-currency-documentation.md`)
   - Understand CIDOC-CRM mapping
   - Study transformation examples
   - Learn about E97_Monetary_Amount structure

3. **Implement Changes**
   - Add TTL to ontology file
   - Add Python function to transformation script
   - Update main transformation function
   - Run tests

4. **Verify Implementation**
   - Test with sample data
   - Check output structure
   - Verify currency type assignment
   - Confirm integration with P70.16

---

## 💡 Usage Examples

### Simple Usage (Currency Only)
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_17_documents_sale_price_currency <lira_genovese> .
```

### Complete Price (Amount + Currency)
```turtle
<contract002> a gmn:E31_2_Sales_Contract ;
    gmn:P70_16_documents_sale_price_amount "250.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <lira_genovese> .
```

### With Full Contract Details
```turtle
<contract003> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <seller_giovanni> ;
    gmn:P70_2_documents_buyer <buyer_antonio> ;
    gmn:P70_3_documents_transfer_of <house_san_lorenzo> ;
    gmn:P70_16_documents_sale_price_amount "1500.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <florin> .
```

---

## 📚 Additional Resources

- **CIDOC-CRM Documentation**: http://www.cidoc-crm.org/
- **E98_Currency**: http://www.cidoc-crm.org/Entity/e98-currency/
- **E97_Monetary_Amount**: http://www.cidoc-crm.org/Entity/e97-monetary-amount/
- **P180_has_currency**: http://www.cidoc-crm.org/Property/p180-has-currency/

---

## 📞 Support

For questions or issues with implementation:
1. Review the Implementation Guide for detailed instructions
2. Check the semantic documentation for conceptual clarification
3. Examine transformation examples for practical guidance
4. Test with provided sample data

---

## 📅 Version Information

- **Property Created**: 2025-10-17
- **Documentation Version**: 1.0
- **Last Updated**: 2025-10-27

---

## ⚠️ Important Notes

1. **Currency Type Reference**: The range is `cidoc:E98_Currency`, but values can be URIs or structured objects
2. **Works with P70.16**: This property should typically be used alongside P70.16 for complete price data
3. **E97 Monetary Amount**: Both properties contribute to a single E97_Monetary_Amount entity
4. **Acquisition Integration**: The transformation coordinates with existing E8_Acquisition nodes
5. **Historical Accuracy**: Use historically accurate currency types from controlled vocabularies when possible

---

*This deliverables package provides everything needed to implement the documents sale price currency property in the GMN ontology system.*
