# GMN Ontology: P70.5 Documents Buyer's Procurator Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_5_documents_buyers_procurator` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-buyers-procurator-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-buyers-procurator-documentation.md** - Complete semantic documentation
4. **documents-buyers-procurator-ontology.ttl** - TTL snippets for ontology
5. **documents-buyers-procurator-transform.py** - Python transformation code
6. **documents-buyers-procurator-doc-note.txt** - Documentation additions

---

## 🎯 Property Overview

**Property Name:** `gmn:P70_5_documents_buyers_procurator`  
**Label:** "P70.5 documents buyer's procurator"  
**Purpose:** Simplified property for associating a sales contract with the person named as the procurator (legal representative) for the buyer

### Key Characteristics

- **Domain:** `gmn:E31_2_Sales_Contract`
- **Range:** `cidoc:E21_Person`
- **Superproperty:** `cidoc:P70_documents`
- **Created:** 2025-10-17

### CIDOC-CRM Transformation Path

```
E31_Document 
  → P70_documents → E8_Acquisition 
    → P9_consists_of → E7_Activity 
      → P14_carried_out_by → E21_Person (procurator)
      → P14.1_in_the_role_of → E55_Type (AAT: agent)
      → P17_was_motivated_by → E21_Person (buyer)
```

---

## ✅ Quick-Start Checklist

### For Ontology Implementation
- [ ] Add TTL definition to `gmn_ontology.ttl`
- [ ] Verify property hierarchy and domain/range
- [ ] Check rdfs:seeAlso references
- [ ] Validate with ontology testing tools

### For Transformation Script
- [ ] Add transformation function to `gmn_to_cidoc_transform.py`
- [ ] Update main transformation pipeline
- [ ] Add AAT_AGENT constant (if not present)
- [ ] Test with sample data

### For Documentation
- [ ] Add property description to main documentation
- [ ] Include examples with procurators
- [ ] Document relationship with buyer property (P70.2)
- [ ] Add transformation examples

---

## 📊 Implementation Summary

### What This Property Does

The `gmn:P70_5_documents_buyers_procurator` property enables data entry systems to directly associate a sales contract with the procurator (legal representative) acting on behalf of the buyer. This simplified approach is automatically transformed into the full CIDOC-CRM structure that explicitly models:

1. The **E7_Activity** representing the procurator's participation
2. The **P14_carried_out_by** relationship to the procurator person
3. The **P14.1_in_the_role_of** qualification specifying the agent role
4. The **P17_was_motivated_by** relationship linking the procurator to the buyer they represent

### Why Transformation is Necessary

Historical documents often name procurators (legal representatives) who act on behalf of buyers in property transactions. A procurator might be:
- A family member acting for an absent buyer
- A business partner representing a buyer
- A professional agent authorized to complete the purchase

The simplified property provides convenience for data entry while the transformation ensures CIDOC-CRM compliance by properly modeling:
- The participation of the procurator as an activity within the acquisition
- The relationship between the procurator and the buyer they represent
- The role specification using AAT vocabulary

### Related Properties

This property works in conjunction with:
- **gmn:P70_2_documents_buyer** - Documents the buyer (principal party)
- **gmn:P70_4_documents_sellers_procurator** - Documents the seller's procurator
- **gmn:P70_7_documents_buyers_guarantor** - Documents the buyer's guarantor (security provider)

---

## 🔧 Technical Details

### Transformation Behavior

1. **E8_Acquisition Creation**: If no acquisition exists, creates one
2. **E7_Activity Creation**: Creates unique activity for each procurator
3. **URI Generation**: Uses hash-based URI: `{contract_uri}/activity/procurator_{hash}`
4. **Buyer Linkage**: Automatically links to buyer via P17_was_motivated_by
5. **Role Specification**: Applies AAT_AGENT type to qualify the relationship
6. **Property Removal**: Deletes simplified property after transformation

### Constants Used

```python
AAT_AGENT = "http://vocab.getty.edu/aat/300411835"  # Agents (people in legal context)
```

---

## 📚 Example Usage

### Input (Simplified)

```json
{
  "@id": "https://example.org/contract/1234",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [{
    "@id": "https://example.org/person/buyer_001",
    "@type": "cidoc:E21_Person"
  }],
  "gmn:P70_5_documents_buyers_procurator": [{
    "@id": "https://example.org/person/procurator_001",
    "@type": "cidoc:E21_Person"
  }]
}
```

### Output (Transformed)

```json
{
  "@id": "https://example.org/contract/1234",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [{
    "@id": "https://example.org/contract/1234/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P22_transferred_title_to": [{
      "@id": "https://example.org/person/buyer_001",
      "@type": "cidoc:E21_Person"
    }],
    "cidoc:P9_consists_of": [{
      "@id": "https://example.org/contract/1234/activity/procurator_a1b2c3d4",
      "@type": "cidoc:E7_Activity",
      "cidoc:P14_carried_out_by": [{
        "@id": "https://example.org/person/procurator_001",
        "@type": "cidoc:E21_Person"
      }],
      "cidoc:P14.1_in_the_role_of": {
        "@id": "http://vocab.getty.edu/aat/300411835",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P17_was_motivated_by": {
        "@id": "https://example.org/person/buyer_001",
        "@type": "cidoc:E21_Person"
      }
    }]
  }]
}
```

---

## 🔍 Key Concepts

### Procurator vs. Other Roles

**Procurator (Legal Representative)**
- Acts with legal authority on behalf of the buyer
- Makes binding decisions for the principal party
- Often holds power of attorney

**Guarantor (P70.7)**
- Provides security for the buyer's obligations
- Does not act on behalf of the buyer
- Promises to fulfill obligations if buyer defaults

**Payment Provider (P70.9)**
- Supplies funds for the purchase
- May not have legal authority to act for buyer
- Financial supporter rather than legal representative

### Historical Context

In Genoa and other Mediterranean commercial centers, procurators were essential for:
- Long-distance trade (buyers couldn't always be physically present)
- Family transactions (managing property for relatives)
- Professional representation (merchants employing agents)
- Legal proceedings (representation before notaries and courts)

---

## 📖 Documentation References

For complete implementation details, see:
- **Implementation Guide** - Step-by-step instructions with code
- **Ontology Documentation** - Full semantic specifications
- **TTL Additions** - Ready-to-copy ontology snippets
- **Python Additions** - Ready-to-copy transformation code
- **Doc Additions** - Examples for main documentation

---

## 🚀 Getting Started

1. Read the **Implementation Guide** for step-by-step instructions
2. Copy TTL definition from **TTL Additions** file
3. Copy Python code from **Python Additions** file
4. Test transformation with sample data
5. Add documentation examples from **Doc Additions** file

---

## ⚠️ Important Notes

- Always transform this property before serializing to pure CIDOC-CRM
- Ensure buyer (P70.2) is documented before procurator transformation
- Multiple procurators create multiple E7_Activity instances
- Each activity receives unique URI based on procurator URI hash
- Property is removed from output after transformation

---

## 📞 Support

For questions about this property or the GMN ontology:
- Review the complete documentation in this package
- Check existing examples in the project files
- Consult CIDOC-CRM specifications for underlying semantics
- Review AAT vocabulary for role types

---

**Version:** 1.0  
**Date:** 2025-10-27  
**Property Created:** 2025-10-17
