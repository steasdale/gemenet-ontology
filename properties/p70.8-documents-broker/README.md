# GMN Ontology: P70.8 Documents Broker Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_8_documents_broker` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-broker-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-broker-documentation.md** - Complete semantic documentation
4. **documents-broker-ontology.ttl** - Ready-to-copy TTL snippets
5. **documents-broker-transform.py** - Ready-to-copy Python code
6. **documents-broker-doc-note.txt** - Documentation additions

---

## 🎯 Quick Start Checklist

### For Ontology Maintainers
- [ ] Review the property definition in `documents-broker-documentation.md`
- [ ] Copy TTL from `documents-broker-ontology.ttl` to main ontology file
- [ ] Validate ontology syntax
- [ ] Update ontology version/date metadata

### For Developers
- [ ] Read implementation guide in `documents-broker-implementation-guide.md`
- [ ] Copy Python code from `documents-broker-transform.py` to transformation script
- [ ] Add function call to main transformation pipeline
- [ ] Test with sample data
- [ ] Validate output against CIDOC-CRM

### For Documentation Teams
- [ ] Review content in `documents-broker-doc-note.txt`
- [ ] Add examples to main documentation
- [ ] Update property tables
- [ ] Add usage examples

---

## 📋 Property Overview

**Property Name**: `gmn:P70_8_documents_broker`

**Purpose**: Simplified property for associating a sales contract with the person named as the broker who facilitated the transaction.

**Domain**: `gmn:E31_2_Sales_Contract`

**Range**: `cidoc:E21_Person`

**Role**: Brokers facilitate transactions between both buyer and seller, arranging the sale and often receiving a commission. Unlike procurators who represent one party, or guarantors who provide security, brokers are neutral facilitators.

---

## 🔄 Transformation Pattern

The simplified property:
```turtle
<contract> gmn:P70_8_documents_broker <broker_person> .
```

Transforms to:
```turtle
<contract> cidoc:P70_documents <acquisition> .
<acquisition> a cidoc:E8_Acquisition ;
    cidoc:P14_carried_out_by <broker_person> .
<broker_person> a cidoc:E21_Person ;
    cidoc:P14.1_in_the_role_of <http://vocab.getty.edu/page/aat/300025234> .
```

The AAT URI `300025234` represents "brokers (people)".

---

## 💡 Key Features

1. **Simple Data Entry**: Use one property to connect contract to broker
2. **CIDOC-CRM Compliance**: Automatically expands to proper E8_Acquisition structure
3. **Role Specification**: Automatically assigns broker role from Getty AAT
4. **Multiple Brokers**: Supports contracts with multiple brokers
5. **Neutral Facilitator**: Models broker as neutral party (unlike procurators/guarantors)

---

## 📖 Usage Examples

### Simple Broker Assignment
```turtle
<sales_contract_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_8_documents_broker <person_giovanni_broker> .
```

### Multiple Brokers
```turtle
<sales_contract_002> a gmn:E31_2_Sales_Contract ;
    gmn:P70_8_documents_broker <person_giovanni_broker> ,
                                <person_marco_broker> .
```

---

## 🔗 Related Properties

- **gmn:P70_1_documents_seller** - The party selling the property
- **gmn:P70_2_documents_buyer** - The party buying the property
- **gmn:P70_4_documents_sellers_procurator** - Legal representative for seller
- **gmn:P70_5_documents_buyers_procurator** - Legal representative for buyer
- **gmn:P70_6_documents_sellers_guarantor** - Guarantor for seller
- **gmn:P70_7_documents_buyers_guarantor** - Guarantor for buyer

---

## ⚠️ Important Notes

1. **Broker vs Procurator**: Brokers facilitate transactions for both parties; procurators legally represent one party
2. **Broker vs Guarantor**: Brokers arrange transactions; guarantors provide security
3. **Neutral Role**: Brokers are neutral facilitators, not advocates for either party
4. **Commission**: Brokers typically receive commission from one or both parties
5. **Medieval Context**: In Genoa, brokers (sensali) were often officially licensed

---

## 📚 Historical Context

In medieval Genoese contracts, brokers (Italian: *sensali*) were professional intermediaries who:
- Facilitated negotiations between buyers and sellers
- Helped establish fair market prices
- Often worked as licensed professionals
- Received commissions for their services
- Were distinct from legal representatives (procurators)
- Could work on behalf of both parties simultaneously

---

## 🛠️ Implementation Status

- [x] Ontology definition complete
- [x] Transformation code complete
- [x] Documentation complete
- [ ] Integrated into main ontology
- [ ] Integrated into transformation pipeline
- [ ] Tested with production data

---

## 📞 Support

For questions or issues:
1. Review the detailed implementation guide
2. Check the semantic documentation
3. Consult the transformation code comments
4. Review CIDOC-CRM P14 and P70 documentation

---

## 📄 License & Attribution

Part of the GMN (Genoese Maritime Network) Ontology
Created: 2025-10-17
Last Updated: 2025-10-27

---

## ✅ Validation Checklist

Before deploying to production:
- [ ] TTL syntax validated
- [ ] Python code tested with unit tests
- [ ] Transformation output validated against CIDOC-CRM
- [ ] Sample data transformed successfully
- [ ] Documentation reviewed and approved
- [ ] AAT URI validated (300025234 = brokers)
- [ ] Integration tests passed
