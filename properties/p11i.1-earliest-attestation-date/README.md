# GMN Ontology: P11i.1 Earliest Attestation Date Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P11i_1_earliest_attestation_date` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **has-earliest-attestation-date-implementation-guide.md** - Step-by-step implementation instructions
3. **has-earliest-attestation-date-documentation.md** - Complete semantic documentation
4. **has-earliest-attestation-date-ontology.ttl** - Ready-to-copy TTL snippets
5. **has-earliest-attestation-date-transform.py** - Ready-to-copy Python transformation code
6. **has-earliest-attestation-date-doc-note.txt** - Documentation examples and tables

---

## 🎯 Quick Start Checklist

### For Ontology Updates
- [ ] Open `gmn_ontology.ttl`
- [ ] Copy content from `has-earliest-attestation-date-ontology.ttl`
- [ ] Paste into the appropriate section (around line 200-300, with other P11i properties)
- [ ] Verify TTL syntax with a validator
- [ ] Commit changes with message: "Add P11i.1 earliest attestation date property"

### For Transformation Script Updates
- [ ] Open `gmn_to_cidoc_transform.py`
- [ ] Copy the function from `has-earliest-attestation-date-transform.py`
- [ ] Paste after other P11i transformation functions (around line 1500)
- [ ] Add function call to `transform_item()` in the Person attestation section
- [ ] Run unit tests to verify transformation
- [ ] Commit changes with message: "Add P11i.1 earliest attestation date transformation"

### For Documentation Updates
- [ ] Open your main documentation file
- [ ] Copy content from `has-earliest-attestation-date-doc-note.txt`
- [ ] Add to the "Person Properties" or "Attestation Properties" section
- [ ] Update table of contents if needed
- [ ] Review formatting and cross-references
- [ ] Commit changes

---

## 📋 Property Summary

**Property Name:** `gmn:P11i_1_earliest_attestation_date`  
**Label:** "P11i.1 earliest attestation date"  
**Domain:** `cidoc:E21_Person`  
**Range:** `xsd:date`  
**Purpose:** Captures the earliest date at which a person is documented or attested to have been alive in historical sources

### CIDOC-CRM Mapping
```
E21_Person 
  → P11i_participated_in 
    → E5_Event 
      → P4_has_time-span 
        → E52_Time-Span 
          → P82a_begin_of_the_begin [xsd:date]
```

---

## 💡 Use Cases

1. **Biographical Research**: Record the first known historical reference to a person
2. **Chronological Analysis**: Establish terminus post quem for person's existence
3. **Source Documentation**: Link attestation dates to specific archival documents
4. **Prosopographical Studies**: Build timelines of historical figures' documented presence

---

## 📖 Example Usage

### Input (GMN Shortcut)
```turtle
<person/giovanni_rossi> a cidoc:E21_Person ;
    gmn:P11i_1_earliest_attestation_date "1450-03-15"^^xsd:date .
```

### Output (Full CIDOC-CRM)
```turtle
<person/giovanni_rossi> a cidoc:E21_Person ;
    cidoc:P11i_participated_in <person/giovanni_rossi/event/earliest_a1b2c3d4> .

<person/giovanni_rossi/event/earliest_a1b2c3d4> a cidoc:E5_Event ;
    cidoc:P4_has_time-span <person/giovanni_rossi/event/earliest_a1b2c3d4/timespan> .

<person/giovanni_rossi/event/earliest_a1b2c3d4/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82a_begin_of_the_begin "1450-03-15"^^xsd:date .
```

---

## 🔧 Implementation Notes

### Key Design Decisions

1. **Event-based Model**: Uses CIDOC-CRM's event-based approach to model attestation
2. **URI Generation**: Creates stable URIs using hash-based identifiers
3. **Date Format**: Accepts ISO 8601 date format (YYYY-MM-DD)
4. **Multiple Dates**: Supports multiple attestation dates per person

### Dependencies

- **Python packages**: None (uses standard library only)
- **Ontology imports**: CIDOC-CRM, XSD datatypes
- **Related properties**: Works with `gmn:P11i_2_latest_attestation_date`

### Testing Recommendations

1. Test with single date value
2. Test with multiple date values
3. Test with existing P11i_participated_in property
4. Test date format validation
5. Verify URI generation stability

---

## 📚 Related Properties

- **gmn:P11i_2_latest_attestation_date** - Latest attestation date for a person
- **gmn:P11i_3_has_spouse** - Spousal relationships (also uses P11i_participated_in)
- **gmn:P98i_1_has_birth_date** - Birth date (uses P98i_was_born pathway)
- **gmn:P100i_1_has_death_date** - Death date (uses P100i_died_in pathway)

---

## 🔗 Documentation References

- **CIDOC-CRM Specification**: [P11i participated in (participated in)](https://cidoc-crm.org/Property/P11i-participated-in/version-7.1.2)
- **CIDOC-CRM P4**: [P4 has time-span (is time-span of)](https://cidoc-crm.org/Property/P4-has-time-span/version-7.1.2)
- **CIDOC-CRM P82a**: [P82a begin of the begin](https://cidoc-crm.org/Property/P82a-begin-of-the-begin/version-7.1.2)

---

## 📞 Support

For questions or issues with this implementation:
1. Review the Implementation Guide for detailed instructions
2. Check the Documentation file for semantic clarifications
3. Consult the CIDOC-CRM specification for property definitions
4. Review test cases in the transformation script

---

## 📝 Version History

- **v1.0** (2025-10-26) - Initial deliverables package created
  - Ontology definition
  - Transformation function
  - Documentation and examples

---

## ✅ Validation Checklist

Before deploying to production:
- [ ] TTL syntax validated
- [ ] Python code passes unit tests
- [ ] Transformation produces valid CIDOC-CRM output
- [ ] Documentation is accurate and complete
- [ ] Examples match actual implementation
- [ ] Related properties tested for compatibility

---

*This deliverables package is part of the GMN (Genoa Medieval Notarial) ontology project, implementing CIDOC-CRM compliant shortcuts for historical data modeling.*
