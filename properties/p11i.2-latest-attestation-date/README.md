# GMN Ontology: P11i.2 Latest Attestation Date Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P11i_2_latest_attestation_date` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **has-latest-attestation-date-implementation-guide.md** - Step-by-step implementation instructions
3. **has-latest-attestation-date-documentation.md** - Complete semantic documentation
4. **has-latest-attestation-date-ontology.ttl** - TTL snippets for main ontology file
5. **has-latest-attestation-date-transform.py** - Python code for transformation script
6. **has-latest-attestation-date-doc-note.txt** - Examples and tables for documentation

---

## 🎯 Property Overview

**Property Name:** `gmn:P11i_2_latest_attestation_date`  
**Label:** "P11i.2 latest attestation date"  
**Property Type:** Datatype Property (owl:DatatypeProperty)  
**Status:** ✅ **ALREADY FULLY IMPLEMENTED**

### Quick Description

This simplified property captures the **latest date** at which a person is documented or attested to have been alive in historical sources. It represents the last known documentary evidence of a person's existence.

### CIDOC-CRM Transformation Path

```
E21_Person 
  → P11i_participated_in 
    → E5_Event 
      → P4_has_time-span 
        → E52_Time-Span 
          → P82b_end_of_the_end: date
```

---

## ✅ Implementation Status Checklist

### Current Status

- [x] **Ontology Definition** - Already exists in `gmn_ontology.ttl` (lines 143-152)
- [x] **Python Transformation** - Already exists in `gmn_to_cidoc_transform.py` (function: `transform_p11i_2_latest_attestation_date`)
- [x] **Integration** - Already called in main transformation pipeline
- [ ] **Documentation** - Add usage examples to project documentation (see file #6)
- [ ] **Testing** - Test transformation with sample data (see Implementation Guide)

### What This Package Provides

Since this property is **already fully implemented**, this package provides:

1. **Documentation** - Complete semantic and technical documentation
2. **Reference Materials** - Current ontology definition and transformation code
3. **Testing Guidance** - Procedures for validating the existing implementation
4. **Usage Examples** - Sample data and expected outputs

---

## 🚀 Quick Start

### For New Users

If you're just learning about this property:

1. Read the **Ontology Documentation** (file #3) to understand the semantic model
2. Review the **Implementation Guide** (file #2) for technical details
3. Check the **Document Additions** (file #6) for usage examples

### For Developers

If you need to work with this property:

1. The ontology definition is in `gmn_ontology.ttl` - see file #4 for the exact snippet
2. The transformation function is in `gmn_to_cidoc_transform.py` - see file #5 for the code
3. Follow the testing procedures in the Implementation Guide (file #2)

### For Documentation Writers

If you're updating project documentation:

1. See file #6 (`has-latest-attestation-date-doc-note.txt`) for ready-to-use examples and tables
2. Copy the relevant sections into your documentation
3. Adjust formatting as needed for your documentation system

---

## 📚 Key Concepts

### What is a "Latest Attestation Date"?

In historical research, an **attestation date** is a date on which a person is documented in a historical source. The **latest attestation date** is:

- The **last known date** when historical records show evidence of a person's existence
- Often used as a proxy for a person's death date when the actual death date is unknown
- Distinct from a death date (which would use different CIDOC-CRM properties)
- Useful for establishing a terminus ante quem (latest possible date) for a person's lifespan

### Example Use Cases

1. **Unknown Death Date**: "Person X last appears in records on 1592-06-15"
2. **Fragmentary Records**: "Person Y witnessed a contract on 1588-12-03, our latest record of them"
3. **Biographical Research**: "Person Z's activities ceased after 1595-08-20 based on available sources"

### Relationship to Other Properties

- **gmn:P11i_1_earliest_attestation_date** - The earliest known date (beginning of documented life)
- **gmn:P11i_2_latest_attestation_date** - The latest known date (end of documented life)
- These two properties bracket the period during which we have documentary evidence of a person

---

## 🔄 How the Transformation Works

### Input (Simplified GMN Format)

```turtle
person:lorenzo_giustiniani a cidoc:E21_Person ;
    gmn:P1_1_has_name "Lorenzo Giustiniani" ;
    gmn:P11i_2_latest_attestation_date "1595-08-20"^^xsd:date .
```

### Output (Full CIDOC-CRM Compliant)

```turtle
person:lorenzo_giustiniani a cidoc:E21_Person ;
    cidoc:P1_is_identified_by [
        a cidoc:E41_Appellation ;
        cidoc:P190_has_symbolic_content "Lorenzo Giustiniani"
    ] ;
    cidoc:P11i_participated_in [
        a cidoc:E5_Event ;
        cidoc:P4_has_time-span [
            a cidoc:E52_Time-Span ;
            cidoc:P82b_end_of_the_end "1595-08-20"^^xsd:date
        ]
    ] .
```

### Why This Transformation?

- **CIDOC-CRM Compliance**: The full structure is semantically richer and interoperable
- **Event-Based Modeling**: Attestations are treated as participation events
- **Temporal Precision**: Uses P82b_end_of_the_end specifically for the latest bound
- **Data Entry Convenience**: The simplified property makes data entry easier while maintaining semantic rigor

---

## 📖 Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| README.md | Overview and quick start | Everyone |
| has-latest-attestation-date-implementation-guide.md | Technical implementation | Developers |
| has-latest-attestation-date-documentation.md | Semantic model documentation | Ontologists, Researchers |
| has-latest-attestation-date-ontology.ttl | TTL code snippets | Ontology Developers |
| has-latest-attestation-date-transform.py | Python transformation code | Software Developers |
| has-latest-attestation-date-doc-note.txt | Examples for project docs | Documentation Writers |

---

## 🧪 Testing Recommendations

1. **Unit Tests**: Test the transformation function with various date formats
2. **Integration Tests**: Verify the property works within complete person records
3. **Edge Cases**: Test with missing dates, multiple dates, invalid formats
4. **Round-Trip**: Ensure data can be transformed and queried correctly

See the Implementation Guide (file #2) for detailed testing procedures.

---

## 📝 Notes

- **Property Status**: This property is already fully implemented and functional
- **No Code Changes Needed**: All code is already in place and working
- **Documentation Focus**: This package focuses on documenting the existing implementation
- **Use Case**: Primarily for historical person records where death dates are unknown

---

## 🔗 Related Properties

- `gmn:P11i_1_earliest_attestation_date` - Earliest attestation date
- `gmn:P11i_3_has_spouse` - Spousal relationships (also uses P11i_participated_in)
- Standard CIDOC-CRM properties: `P11i_participated_in`, `P4_has_time-span`, `P82b_end_of_the_end`

---

## 📞 Support

For questions or issues:
- Review the Implementation Guide for technical details
- Check the Ontology Documentation for semantic clarification
- Consult the CIDOC-CRM specification for standard property definitions

---

**Last Updated**: October 2025  
**Ontology Version**: GMN 1.0  
**CIDOC-CRM Version**: 7.1.x
