# GMN Ontology: Marriage Enumeration Supplement
## P11i.3 Has Spouse - Enumeration Support (Option 2: E13_Attribute_Assignment)

This supplement extends the base `gmn:P11i_3_has_spouse` property implementation with support for marriage enumeration using the E13_Attribute_Assignment approach.

---

## 📦 Supplement Contents

1. **README.md** (this file) - Supplement overview
2. **enumeration-implementation-guide.md** - Step-by-step implementation
3. **enumeration-documentation.md** - Complete semantic documentation
4. **enumeration-ontology.ttl** - New TTL property definitions
5. **enumeration-transform.py** - Enhanced transformation function
6. **enumeration-doc-note.txt** - Documentation additions

---

## 🎯 What This Supplement Adds

### Base Package (Required)
The base has-spouse deliverables package provides:
- `gmn:P11i_3_has_spouse` - Simple spouse relationship
- Transformation to E5_Event with AAT marriage type
- Basic marriage event structure

### This Supplement (Optional Enhancement)
This supplement adds:
- **Marriage enumeration for each person** (1st, 2nd, 3rd marriage, etc.)
- **E13_Attribute_Assignment** modeling approach
- **Person-specific ordinal numbers** in the same marriage event
- **Enhanced queryability** for marriage order

---

## 📋 Quick-Start Checklist

### Prerequisites
- [ ] Base has-spouse package already implemented
- [ ] Understanding of E13_Attribute_Assignment class
- [ ] Familiarity with P140/P141 properties

### Implementation Steps
1. [ ] Add new simplified properties to ontology (5 minutes)
2. [ ] Replace transformation function with enhanced version (15 minutes)
3. [ ] Test with enumerated marriage data (10 minutes)
4. [ ] Update documentation (optional)

**Total estimated time**: ~30 minutes (plus base package time if not already implemented)

---

## 🔄 Usage Comparison

### WITHOUT Enumeration (Base Package)
```json
{
  "@id": "person:giovanni",
  "gmn:P11i_3_has_spouse": [
    {"@id": "person:maria"}
  ]
}
```
**Result**: Simple marriage event with both participants

### WITH Enumeration (This Supplement)
```json
{
  "@id": "person:giovanni",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:maria",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 1
    }
  ]
}
```
**Result**: Marriage event with E13_Attribute_Assignment nodes indicating this is Giovanni's 2nd marriage and Maria's 1st

---

## 🏗️ Semantic Structure

### Enhanced Structure with Enumeration

```
E21_Person (Giovanni)
  └─ P11i_participated_in
      └─ E5_Event (marriage)
          ├─ P2_has_type → AAT:300055475 (marriages)
          ├─ P11_had_participant → Giovanni
          ├─ P11_had_participant → Maria
          ├─ P140i_was_attributed_by
          │   └─ E13_Attribute_Assignment (Giovanni's enumeration)
          │       ├─ P140_assigned_attribute_to → Giovanni
          │       ├─ P141_assigned → "2"^^xsd:integer
          │       └─ P177_assigned_property_of_type → P11_had_participant
          └─ P140i_was_attributed_by
              └─ E13_Attribute_Assignment (Maria's enumeration)
                  ├─ P140_assigned_attribute_to → Maria
                  ├─ P141_assigned → "1"^^xsd:integer
                  └─ P177_assigned_property_of_type → P11_had_participant
```

---

## 🆕 New Simplified Properties

### gmn:marriage_number_for_subject
- **Purpose**: Indicates the marriage ordinal number for the person who has this spouse property
- **Type**: xsd:integer (1, 2, 3, etc.)
- **Example**: 2 = second marriage for the subject person

### gmn:marriage_number_for_spouse
- **Purpose**: Indicates the marriage ordinal number for the spouse being referenced
- **Type**: xsd:integer (1, 2, 3, etc.)
- **Example**: 1 = first marriage for the spouse

---

## 💡 Use Cases

### Use Case 1: Different Marriage Numbers
```json
{
  "@id": "person:widower",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:second_wife",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 1
    }
  ]
}
```
A widower remarries; it's his second marriage but her first.

### Use Case 2: Both Second Marriages
```json
{
  "@id": "person:widow",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:widower",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 2
    }
  ]
}
```
Two people who have both been widowed marry each other.

### Use Case 3: Multiple Marriages with Enumeration
```json
{
  "@id": "person:historical_figure",
  "gmn:P11i_3_has_spouse": [
    {
      "@id": "person:first_spouse",
      "gmn:marriage_number_for_subject": 1,
      "gmn:marriage_number_for_spouse": 1
    },
    {
      "@id": "person:second_spouse",
      "gmn:marriage_number_for_subject": 2,
      "gmn:marriage_number_for_spouse": 1
    }
  ]
}
```
Complete marriage history with enumeration.

---

## 🔍 Queryability Benefits

### SPARQL: Find All Second Marriages
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?marriage ?spouse
WHERE {
  ?marriage cidoc:P11_had_participant ?person .
  ?marriage cidoc:P140i_was_attributed_by ?attr .
  ?attr cidoc:P140_assigned_attribute_to ?person .
  ?attr cidoc:P141_assigned "2"^^xsd:integer .
  ?marriage cidoc:P11_had_participant ?spouse .
  FILTER(?person != ?spouse)
}
```

### SPARQL: Find Marriage Number Mismatches
```sparql
# Find marriages where ordinal numbers differ significantly
SELECT ?person1 ?num1 ?person2 ?num2
WHERE {
  ?marriage cidoc:P11_had_participant ?person1, ?person2 .
  
  ?marriage cidoc:P140i_was_attributed_by ?attr1 .
  ?attr1 cidoc:P140_assigned_attribute_to ?person1 .
  ?attr1 cidoc:P141_assigned ?num1 .
  
  ?marriage cidoc:P140i_was_attributed_by ?attr2 .
  ?attr2 cidoc:P140_assigned_attribute_to ?person2 .
  ?attr2 cidoc:P141_assigned ?num2 .
  
  FILTER(?person1 != ?person2)
  FILTER(ABS(?num1 - ?num2) > 1)
}
```

---

## ⚠️ Important Notes

### Backward Compatibility
- This supplement **replaces** the base transformation function
- Marriages without enumeration still work (properties are optional)
- Enhanced function handles both enumerated and non-enumerated marriages

### Data Entry
- Both enumeration properties are optional
- Can specify one, both, or neither
- Zero or missing values are treated as "unspecified"

### URI Generation
- Attribution URIs include both event and person identifiers
- Format: `{event_uri}/attribution_{person_hash}`
- Ensures unique URIs even with multiple attributions per event

---

## 📊 Implementation Impact

### Additional Nodes per Marriage
- **Without enumeration**: 1 event node
- **With full enumeration**: 1 event + 2 attribution nodes = 3 nodes total

### Storage Considerations
- Each E13_Attribute_Assignment adds ~150-200 bytes to JSON-LD
- For 1000 marriages with full enumeration: ~400KB additional storage

### Query Performance
- Attribution nodes increase query complexity
- Use indexed SPARQL queries for large datasets
- Consider materialized views for frequent marriage number queries

---

## 🔗 Related Enhancements

This enumeration approach can be extended to other relationship types:

- **Parent enumeration**: "Second child of father"
- **Occupation enumeration**: "Third career/occupation"
- **Property ownership enumeration**: "Second property owned"

The same E13_Attribute_Assignment pattern applies.

---

## 📚 Documentation References

### CIDOC-CRM Classes
- **E13_Attribute_Assignment**: http://www.cidoc-crm.org/Entity/e13-attribute-assignment/version-7.1.3
- **E5_Event**: http://www.cidoc-crm.org/Entity/e5-event/version-7.1.3

### CIDOC-CRM Properties
- **P140_assigned_attribute_to**: http://www.cidoc-crm.org/Property/p140-assigned-attribute-to/version-7.1.3
- **P141_assigned**: http://www.cidoc-crm.org/Property/p141-assigned/version-7.1.3
- **P177_assigned_property_of_type**: http://www.cidoc-crm.org/Property/p177-assigned-property-of-type/version-7.1.3

---

## ✅ Validation Checklist

After implementing this supplement:

- [ ] TTL validates with new properties
- [ ] Transformation handles missing enumeration gracefully
- [ ] Attribution URIs are unique
- [ ] SPARQL queries retrieve enumerations correctly
- [ ] Backward compatible with non-enumerated marriages
- [ ] Documentation updated with examples

---

## 🆘 Support

### Common Questions

**Q: Do I need to specify both subject and spouse numbers?**
A: No, both are optional. Specify what you know.

**Q: Can I use this with the base package?**
A: This supplement replaces the base transformation function but remains backward compatible.

**Q: What if I don't know the marriage number?**
A: Omit the properties. The transformation will work without them.

**Q: How do I query just marriages with enumeration?**
A: Filter for existence of P140i_was_attributed_by in your SPARQL queries.

---

## 📦 Installation Summary

1. Install base has-spouse package (if not already done)
2. Add new properties from `enumeration-ontology.ttl`
3. Replace transformation function with version from `enumeration-transform.py`
4. Test with enumerated marriage data
5. Update documentation from `enumeration-doc-note.txt`

---

**Supplement Version**: 1.0  
**Base Package**: gmn:P11i_3_has_spouse v1.0  
**Date**: 2025-10-27  
**Approach**: E13_Attribute_Assignment (Option 2)  
**Status**: Ready for implementation
