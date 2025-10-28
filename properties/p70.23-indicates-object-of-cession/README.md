# GMN Ontology: P70.23 Indicates Object of Cession Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_23_indicates_object_of_cession` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **indicates-cession-object-implementation-guide.md** - Step-by-step implementation instructions
3. **indicates-cession-object-documentation.md** - Complete semantic documentation
4. **indicates-cession-object-ontology.ttl** - TTL snippets for the ontology
5. **indicates-cession-object-transform.py** - Python transformation code
6. **indicates-cession-object-doc-note.txt** - Examples and tables for documentation

---

## 🎯 Quick Start

### Implementation Checklist

- [ ] **Step 1**: Add TTL definition to `gmn_ontology.ttl`
  - Location: After P70.22 (indicates receiving party)
  - File: `indicates-cession-object-ontology.ttl`

- [ ] **Step 2**: Add transformation function to `gmn_to_cidoc_transform.py`
  - Location: After `transform_p70_22_indicates_receiving_party()`
  - File: `indicates-cession-object-transform.py`

- [ ] **Step 3**: Register transformation in main pipeline
  - Location: `transform_item()` function
  - Add: `item = transform_p70_23_indicates_object_of_cession(item)`

- [ ] **Step 4**: Update documentation
  - Add content from `indicates-cession-object-doc-note.txt`
  - Location: Cession of Rights section

- [ ] **Step 5**: Test implementation
  - Run test cases from implementation guide
  - Verify CIDOC-CRM compliance

---

## 📋 Property Overview

### GMN Shortcut Property
**URI**: `gmn:P70_23_indicates_object_of_cession`

**Label**: "P70.23 indicates object of cession"

**Purpose**: Simplified property for associating a cession of rights contract with the legal rights, claims, or obligations being transferred.

### Transformation Target

The property transforms to the full CIDOC-CRM path:

```
E31_Document 
  > P70_documents 
  > E7_Activity (typed as AAT 300417639 - cession/transfer of rights)
  > P16_used_specific_object 
  > E72_Legal_Object
```

---

## 🔑 Key Characteristics

- **Domain**: `gmn:E31_4_Cession_of_Rights_Contract`
- **Range**: `cidoc:E72_Legal_Object`
- **Subproperty of**: `cidoc:P70_documents`
- **Created**: 2025-10-18

### Legal Object Types

The range `E72_Legal_Object` encompasses:
- Rights to collect debts
- Rights to use property (usufruct)
- Rights of ownership
- Claims arising from contracts
- Inheritance rights
- Any other legal interests

---

## 🔄 Transformation Logic

### Input (GMN Shortcut)
```turtle
<cession001> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_23_indicates_object_of_cession <debt_claim_123> .
```

### Output (CIDOC-CRM Compliant)
```turtle
<cession001> a gmn:E31_4_Cession_of_Rights_Contract ;
    cidoc:P70_documents <cession001/cession> .

<cession001/cession> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417639> ;
    cidoc:P16_used_specific_object <debt_claim_123> .

<debt_claim_123> a cidoc:E72_Legal_Object .
```

---

## 🏗️ Integration with Other Properties

The `P70.23_indicates_object_of_cession` property works together with:

1. **P70.21 indicates conceding party** - The party transferring the rights
2. **P70.22 indicates receiving party** - The party receiving the rights
3. **P70.23 indicates object of cession** - The legal object being transferred (this property)

All three properties share the same E7_Activity node, creating a complete representation of the cession transaction.

---

## ⚠️ Important Notes

### Shared Activity Node
- The transformation checks if a cession activity already exists
- Multiple properties can reference the same E7_Activity
- URI pattern: `{contract_uri}/cession`

### Activity Typing
- E7_Activity is typed as AAT 300417639 (cession/transfer of rights)
- Type is added automatically during transformation
- Type distinguishes cessions from other documented activities

### Multiple Objects
- Multiple objects can be ceded in a single contract
- Use P70.23 multiple times for different legal objects
- Each object is added to the activity's P16_used_specific_object

---

## 📚 Documentation References

For complete details, see:
- **Implementation Guide**: `indicates-cession-object-implementation-guide.md`
- **Semantic Documentation**: `indicates-cession-object-documentation.md`

---

## 🧪 Testing

Quick test command:
```python
# Test the transformation
test_data = {
    '@id': 'http://example.org/cession001',
    '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
    'gmn:P70_23_indicates_object_of_cession': {
        '@id': 'http://example.org/debt_claim',
        '@type': 'cidoc:E72_Legal_Object'
    }
}

result = transform_p70_23_indicates_object_of_cession(test_data)
print(json.dumps(result, indent=2))
```

---

## 📞 Support

For questions or issues with this property:
1. Review the implementation guide
2. Check the semantic documentation
3. Verify transformation examples
4. Test with sample data

---

**Created**: 2025-10-28  
**Version**: 1.0  
**Property**: gmn:P70_23_indicates_object_of_cession
