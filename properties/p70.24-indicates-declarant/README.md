# GMN Ontology: P70.24 Indicates Declaring Party Property
## Deliverables Package

This package contains all necessary documentation and code for implementing the `gmn:P70_24_indicates_declarant` property in the GMN ontology and transformation pipeline.

---

## 📦 Package Contents

1. **README.md** (this file) - Overview and quick-start guide
2. **indicates-declaring-party-implementation-guide.md** - Step-by-step implementation instructions
3. **indicates-declaring-party-documentation.md** - Complete semantic documentation
4. **indicates-declaring-party-ontology.ttl** - TTL snippets for the ontology
5. **indicates-declaring-party-transform.py** - Python code for transformation
6. **indicates-declaring-party-doc-note.txt** - Documentation examples and tables

---

## 🎯 Property Overview

**Property URI**: `gmn:P70_24_indicates_declarant`

**Label**: "P70.24 indicates declarant"

**Purpose**: Simplified property for associating a declaration document with the person or entity making the declaration (the declarant). The declarant is the party who is formally stating, acknowledging, or asserting something.

**Domain**: `gmn:E31_5_Declaration`

**Range**: `cidoc:E39_Actor`

**CIDOC-CRM Equivalent Path**:
```
E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
```

**Implicit Activity Type**: AAT 300027623 (declaration)

---

## ⚡ Quick Start Checklist

### For Ontology Implementation
- [ ] Add P70.24 property definition to `gmn_ontology.ttl`
- [ ] Verify domain constraint (E31_5_Declaration)
- [ ] Verify range constraint (E39_Actor)
- [ ] Add rdfs:subPropertyOf cidoc:P70_documents
- [ ] Add metadata (dcterms:created, rdfs:seeAlso)

### For Python Transformation
- [ ] Add `transform_p70_24_indicates_declarant()` function to transformation script
- [ ] Add function call to `transform_item()` pipeline
- [ ] Test with simple declaration (single declarant)
- [ ] Test with complex declaration (multiple declarants)
- [ ] Verify activity URI generation
- [ ] Verify E7_Activity typing with AAT 300027623

### For Documentation
- [ ] Add property description to main documentation
- [ ] Include usage examples
- [ ] Add to declaration contract section
- [ ] Update property comparison tables

---

## 📊 Implementation Summary

### What This Property Does

The `gmn:P70_24_indicates_declarant` property provides a simplified way to document who makes a formal declaration. Instead of manually creating the full CIDOC-CRM structure with intermediate activities, you can directly link a declaration document to its declarant.

### Transformation Behavior

**Input (simplified)**:
```turtle
<declaration_001> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <person_giovanni> .
```

**Output (CIDOC-CRM compliant)**:
```turtle
<declaration_001> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <declaration_001/declaration> .

<declaration_001/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <person_giovanni> .
```

### Key Features

- **Automatic Activity Creation**: Creates typed E7_Activity nodes automatically
- **Multiple Declarants**: Supports multiple declarants for joint declarations
- **Activity Reuse**: Reuses existing activity if P70_25 already processed
- **Type Preservation**: Maintains AAT 300027623 (declaration) typing
- **Clean URIs**: Generates consistent URIs as `{document_uri}/declaration`

---

## 🔗 Related Properties

This property works alongside other declaration properties:

- **`gmn:P70_25_indicates_declaration_subject`** - What is being declared
- **`gmn:P70_22_indicates_receiving_party`** - Who receives the declaration (optional)

### Typical Declaration Pattern

```turtle
<declaration> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <declarant> ;      # Who declares
    gmn:P70_25_indicates_declaration_subject <subject> ;  # What is declared
    gmn:P70_22_indicates_receiving_party <recipient> .    # To whom (optional)
```

---

## 🎓 Common Use Cases

1. **Debt Acknowledgment**: Debtor declares debt owed
2. **Property Claim**: Person declares ownership rights
3. **Fact Statement**: Official declares factual information
4. **Obligation Recognition**: Party declares legal obligations
5. **Right Assertion**: Individual declares entitlements

---

## 📝 Example Scenarios

### Simple Declaration
```turtle
<debt_declaration_01> a gmn:E31_5_Declaration ;
    gmn:P1_1_has_name "Declaration of debt by Marco" ;
    gmn:P70_24_indicates_declarant <merchant_marco> ;
    gmn:P70_25_indicates_declaration_subject <debt_500_lire> .
```

### Joint Declaration
```turtle
<joint_declaration_02> a gmn:E31_5_Declaration ;
    gmn:P1_1_has_name "Joint property declaration" ;
    gmn:P70_24_indicates_declarant <brother_antonio> ,
                                   <brother_giovanni> ;
    gmn:P70_25_indicates_declaration_subject <family_vineyard> .
```

---

## ⚠️ Important Notes

1. **Domain Constraint**: Only use with `gmn:E31_5_Declaration` documents
2. **Actor Range**: Declarant must be an E39_Actor (person or group)
3. **Activity Sharing**: P70.24 and P70.25 share the same E7_Activity node
4. **Typing**: Activity is always typed as AAT 300027623 (declaration)
5. **No Recipient Confusion**: P70.24 is declarant (who declares), not recipient

---

## 🔍 Testing Validation

After implementation, verify:
- ✅ Simple declarations transform correctly
- ✅ Multiple declarants create separate P14 links
- ✅ Activity is properly typed with AAT 300027623
- ✅ Activity URI follows pattern: `{document_uri}/declaration`
- ✅ Integration with P70_25 (declaration subject) works
- ✅ No duplicate activities created

---

## 📚 Additional Resources

- **Full Implementation Guide**: `indicates-declaring-party-implementation-guide.md`
- **Semantic Documentation**: `indicates-declaring-party-documentation.md`
- **TTL Snippets**: `indicates-declaring-party-ontology.ttl`
- **Python Code**: `indicates-declaring-party-transform.py`
- **Documentation Examples**: `indicates-declaring-party-doc-note.txt`

---

## 🤝 Need Help?

For questions about:
- **Ontology design**: See the documentation file
- **Implementation**: See the implementation guide
- **Code integration**: See the Python additions file
- **Examples**: See the doc-note file

---

**Version**: 1.0  
**Last Updated**: October 2025  
**Status**: Ready for Implementation
