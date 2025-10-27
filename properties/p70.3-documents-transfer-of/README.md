# GMN Ontology: P70.3 Documents Transfer Of Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_3_documents_transfer_of` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **documents-transfer-implementation-guide.md** - Step-by-step implementation instructions
3. **documents-transfer-documentation.md** - Complete semantic documentation
4. **documents-transfer-ontology.ttl** - TTL additions for the main ontology file
5. **documents-transfer-transform.py** - Python code additions for transformation script
6. **documents-transfer-doc-note.txt** - Documentation additions and examples

---

## 🎯 Quick Start

### For Ontology Updates
1. Copy the TTL from `documents-transfer-ontology.ttl`
2. Add to your main `gmn_ontology.ttl` file in the appropriate property section
3. Validate the ontology syntax

### For Transformation Pipeline
1. Copy the function from `documents-transfer-transform.py`
2. Add to your `gmn_to_cidoc_transform.py` file
3. Register the transformation function in the main processing pipeline
4. Run tests to verify correct transformation

### For Documentation
1. Review examples in `documents-transfer-doc-note.txt`
2. Add the property table and examples to your main documentation
3. Update any cross-references

---

## 📋 Property Overview

**Property URI:** `gmn:P70_3_documents_transfer_of`

**Label:** P70.3 documents transfer of

**Purpose:** Simplified property for associating a sales contract with the physical thing (property, object, or person) being transferred.

**Domain:** gmn:E31_2_Sales_Contract

**Range:** cidoc:E18_Physical_Thing (includes gmn:E22_1_Building, gmn:E22_2_Moveable_Property, and E21_Person)

**Full CIDOC-CRM Path:**
```
E31_Document 
  → P70_documents 
    → E8_Acquisition 
      → P24_transferred_title_of 
        → E18_Physical_Thing
```

---

## 🔑 Key Features

- **Simplified Data Entry:** Direct association between sales contract document and physical thing being transferred
- **Automatic Transformation:** Converts to full CIDOC-CRM E8_Acquisition structure
- **Multiple Thing Support:** Handles one or multiple physical things in a single contract
- **Flexible Range:** Supports buildings, moveable property, and (historically) persons
- **Type Preservation:** Maintains specific types (E22_1_Building, E22_2_Moveable_Property) during transformation

---

## 💡 Usage Example

### Input (Simplified GMN)
```json
{
  "@id": "https://example.org/contract/sales_1",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "https://example.org/building/shop_23",
      "@type": "gmn:E22_1_Building",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "@value": "Shop on Soziglia Street"
      }
    }
  ]
}
```

### Output (Full CIDOC-CRM)
```json
{
  "@id": "https://example.org/contract/sales_1",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://example.org/contract/sales_1/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "https://example.org/building/shop_23",
          "@type": "gmn:E22_1_Building",
          "cidoc:P1_is_identified_by": {
            "@type": "cidoc:E41_Appellation",
            "@value": "Shop on Soziglia Street"
          }
        }
      ]
    }
  ]
}
```

---

## ✅ Implementation Checklist

- [ ] Review complete semantic documentation
- [ ] Add TTL definitions to ontology file
- [ ] Add transformation function to Python script
- [ ] Register function in transformation pipeline
- [ ] Create test cases for single thing
- [ ] Create test cases for multiple things
- [ ] Test with building objects
- [ ] Test with moveable property objects
- [ ] Test with mixed types
- [ ] Validate transformation output
- [ ] Update main documentation
- [ ] Add usage examples to documentation

---

## 🔗 Related Properties

This property works in conjunction with other sales contract properties:

- **gmn:P70_1_documents_seller** - Associates contract with seller (P23_transferred_title_from)
- **gmn:P70_2_documents_buyer** - Associates contract with buyer (P22_transferred_title_to)
- **gmn:P70_4_documents_sellers_procurator** - Associates contract with seller's representative
- **gmn:P70_5_documents_buyers_procurator** - Associates contract with buyer's representative

All these properties share the same E8_Acquisition node created by the transformation.

---

## 📚 Documentation Files

### 1. Implementation Guide
**File:** `documents-transfer-implementation-guide.md`

Comprehensive step-by-step instructions including:
- Prerequisites and dependencies
- Ontology updates with validation
- Python transformation implementation
- Testing procedures
- Troubleshooting guide

### 2. Ontology Documentation
**File:** `documents-transfer-documentation.md`

Complete semantic documentation including:
- Property definition and metadata
- CIDOC-CRM path explanation
- Domain and range specifications
- Usage patterns and examples
- Transformation behavior

### 3. TTL Additions
**File:** `documents-transfer-ontology.ttl`

Ready-to-copy Turtle syntax including:
- Property declaration
- Metadata and annotations
- Domain and range specifications
- Cross-references

### 4. Python Additions
**File:** `documents-transfer-transform.py`

Ready-to-copy Python code including:
- Complete transformation function
- Error handling
- Type preservation logic
- Integration instructions

### 5. Documentation Additions
**File:** `documents-transfer-doc-note.txt`

Examples and tables for main documentation including:
- Property specification table
- Usage examples
- Common patterns
- Integration with other properties

---

## 🎓 Semantic Notes

### Why This Property Exists

The `gmn:P70_3_documents_transfer_of` property simplifies the representation of property transfers in sales contracts. The full CIDOC-CRM path requires:
- Creating an E8_Acquisition event
- Linking it via P70_documents
- Associating the transferred thing via P24_transferred_title_of

This property allows direct association and automatic transformation to the full structure.

### Historical Context

In medieval Genoese contracts, property transfers could include:
- **Buildings:** Houses, shops, warehouses (gmn:E22_1_Building)
- **Moveable Property:** Goods, merchandise, equipment (gmn:E22_2_Moveable_Property)  
- **Historical Documentation:** In historical records, this range also includes E21_Person to document instances where enslaved persons or others were treated as transferable property

### Range Flexibility

The property's range is `cidoc:E18_Physical_Thing`, which encompasses:
- Buildings and structures
- Moveable objects and goods
- Historically, persons (for accurate historical documentation)

The transformation preserves specific subtypes when provided in the input data.

---

## ⚠️ Important Notes

1. **Type Preservation:** If input data specifies a subtype (e.g., gmn:E22_1_Building), the transformation preserves it. If no type is specified, it defaults to cidoc:E18_Physical_Thing.

2. **Multiple Things:** The property accepts an array of things, allowing a single contract to document the transfer of multiple items.

3. **Shared Acquisition Node:** The transformation creates or reuses an existing E8_Acquisition node, allowing other sales contract properties (seller, buyer) to reference the same transaction.

4. **Property Deletion:** After transformation, the simplified property is removed from the data structure to avoid duplication.

---

## 📞 Support & Questions

For questions or issues regarding this property:
1. Review the complete implementation guide
2. Check the semantic documentation
3. Examine the test cases in the Python file
4. Consult the main GMN ontology documentation

---

## 📅 Metadata

**Property Created:** 2025-10-17  
**Documentation Version:** 1.0  
**Package Created:** 2025-10-27  
**Compatible With:** GMN Ontology v1.x, CIDOC-CRM v7.x

---

## License

This documentation follows the same license as the GMN Ontology project.
