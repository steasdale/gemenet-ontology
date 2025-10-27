# Has Sex/Gender Property (gmn:P2_1_gender) Implementation Package

## 📋 Overview

This deliverables package provides complete implementation documentation for the **gmn:P2_1_gender** property, which records the biological sex characteristics of persons in the Geniza Material Network (GMN) ontology. This property extends CIDOC-CRM's P2_has_type pattern with a controlled vocabulary of three Getty AAT terms.

### Property Summary

- **Property URI**: `gmn:P2_1_gender`
- **Label**: "P2.1 has sex/gender"
- **Domain**: `cidoc:E21_Person`
- **Range**: Controlled vocabulary (AAT terms)
  - `aat:300189559` (male)
  - `aat:300189557` (female)
  - `aat:300417544` (intersex)
- **Superproperty**: `cidoc:P2_has_type`
- **Purpose**: Records biological sex characteristics and physiological traits

---

## 🚀 Quick Start Checklist

### For Implementers

- [ ] **Review** the `has-gender-documentation.md` file for semantic understanding
- [ ] **Add** TTL definitions from `has-gender-ontology.ttl` to your main ontology file
- [ ] **Integrate** Python code from `has-gender-transform.py` into your transformation script
- [ ] **Test** with sample data (examples provided in implementation guide)
- [ ] **Update** project documentation using content from `has-gender-doc-note.txt`
- [ ] **Validate** output against CIDOC-CRM standards

### Estimated Implementation Time
- **Ontology Updates**: 5 minutes
- **Code Integration**: 10-15 minutes
- **Testing**: 15-20 minutes
- **Total**: 30-40 minutes

---

## 📦 Package Contents

### 1. **README.md** (This File)
Complete overview, quick-start checklist, and implementation summary.

### 2. **has-gender-implementation-guide.md**
Step-by-step instructions for implementing all changes, including:
- Ontology modifications
- Transformation script integration
- Code insertion points
- Testing procedures
- Validation examples

### 3. **has-gender-documentation.md**
Complete semantic documentation including:
- Property definition and scope
- CIDOC-CRM alignment
- Controlled vocabulary specifications
- Usage examples and patterns
- Transformation logic explanation

### 4. **has-gender-ontology.ttl**
Ready-to-copy TTL snippets for your main ontology file.
**Note**: The gmn:P2_1_gender property is already defined in the ontology, so this file provides the existing definition for reference.

### 5. **has-gender-transform.py**
Ready-to-copy Python code for the transformation script, including:
- New transformation function
- Integration point in main transform_item function
- Helper utilities

### 6. **has-gender-doc-note.txt**
Examples and documentation text to add to your main project documentation files.

---

## 🎯 Implementation Summary

### What's Already Complete
The **gmn:P2_1_gender** property is already defined in the GMN ontology (gmn_ontology.ttl) with:
- Full OWL/RDFS definition
- Controlled vocabulary restriction (three AAT terms)
- CIDOC-CRM alignment via P2_has_type
- Created date: 2025-10-16

### What Needs to Be Implemented
The transformation logic for this property needs to be added to the Python transformation script. This involves:

1. **Creating a transformation function** (`transform_p2_1_gender`) that converts simplified GMN property to full CIDOC-CRM structure
2. **Integrating the function** into the main `transform_item` function
3. **Testing** with various gender values

### Transformation Pattern

**Input (Simplified GMN)**:
```json
{
  "@id": "person/p123",
  "@type": "cidoc:E21_Person",
  "gmn:P2_1_gender": {
    "@id": "aat:300189559"
  }
}
```

**Output (Full CIDOC-CRM)**:
```json
{
  "@id": "person/p123",
  "@type": "cidoc:E21_Person",
  "cidoc:P2_has_type": {
    "@id": "aat:300189559",
    "@type": "cidoc:E55_Type"
  }
}
```

---

## 🔄 Integration Points

### 1. Ontology (gmn_ontology.ttl)
**Status**: ✅ Already complete
- Property definition exists at line 223
- No changes needed

### 2. Transformation Script (gmn_to_cidoc_transform.py)
**Status**: ⚠️ Needs implementation
- Add `transform_p2_1_gender()` function after line 2486
- Add function call in `transform_item()` after line 2412

### 3. Documentation
**Status**: ⚠️ Needs update
- Add usage examples to project documentation
- Include gender recording best practices

---

## 🧪 Testing Recommendations

### Test Cases to Verify

1. **Male Gender**
   ```json
   "gmn:P2_1_gender": {"@id": "aat:300189559"}
   ```

2. **Female Gender**
   ```json
   "gmn:P2_1_gender": {"@id": "aat:300189557"}
   ```

3. **Intersex**
   ```json
   "gmn:P2_1_gender": {"@id": "aat:300417544"}
   ```

4. **Missing Gender** (property absent)
   - Should process without error
   - No P2_has_type added

### Expected Outcomes

- All gender values correctly transform to `cidoc:P2_has_type`
- Type instances created with `@type: "cidoc:E55_Type"`
- Original `gmn:P2_1_gender` property removed from output
- Items without gender property process normally

---

## 📚 Related Documentation

### GMN Ontology Files
- **Main Ontology**: `gmn_ontology.ttl`
- **Transformation Script**: `gmn_to_cidoc_transform.py`

### External Standards
- **CIDOC-CRM**: [P2_has_type](http://www.cidoc-crm.org/Property/P2-has-type/version-7.1.3)
- **Getty AAT**: 
  - [male (300189559)](http://vocab.getty.edu/page/aat/300189559)
  - [female (300189557)](http://vocab.getty.edu/page/aat/300189557)
  - [intersex (300417544)](http://vocab.getty.edu/page/aat/300417544)

### Project Documentation
- `correspondence-documentation.md`
- `donation-documentation.md`
- `dowry-documentation.md`
- `arbitration-ontology.md`

---

## 💡 Key Concepts

### Why Use a Simplified Property?

The **gmn:P2_1_gender** property simplifies data entry by:
1. Providing a clear, domain-specific property name
2. Restricting values to a controlled vocabulary
3. Avoiding complex type assignment during data entry
4. Enabling validation at the ontology level

The transformation script then converts this simplified property to the full CIDOC-CRM structure for semantic compliance.

### Controlled Vocabulary Benefits

Using Getty AAT terms provides:
- **Standardization**: Globally recognized identifiers
- **Interoperability**: Compatible with other heritage databases
- **Semantic richness**: Full AAT term definitions and relationships
- **Authority control**: Maintained by Getty Research Institute

---

## ⚠️ Important Notes

### Data Entry Guidelines

1. **Always use AAT URIs**: Use the full Getty AAT URI, not labels
2. **Validation**: The ontology restricts values to the three specified AAT terms
3. **Optional property**: Not all persons require gender information
4. **Privacy considerations**: Record only when historically documented

### Transformation Behavior

1. **Automatic conversion**: The transformation script automatically converts gmn:P2_1_gender to cidoc:P2_has_type
2. **Type creation**: Creates proper E55_Type instances
3. **Property removal**: Removes the simplified property from output
4. **Graceful handling**: Processes items without gender information normally

---

## 🔗 Cross-References

This property works alongside other person properties:
- **gmn:P1_1_has_name**: Person's name
- **gmn:P1_2_has_name_from_source**: Name as recorded in source
- **gmn:P1_3_has_patrilineal_name**: Patronymic/family name
- **gmn:P11i_1_earliest_attestation_date**: First historical appearance
- **gmn:P11i_2_latest_attestation_date**: Last historical appearance
- **gmn:P11i_3_has_spouse**: Marital relationships
- **gmn:P96_1_has_mother**: Maternal relationship
- **gmn:P97_1_has_father**: Paternal relationship

---

## 📞 Support and Questions

For questions about this implementation:
1. Review the detailed `has-gender-implementation-guide.md`
2. Check the semantic documentation in `has-gender-documentation.md`
3. Examine the code examples in `has-gender-transform.py`
4. Refer to CIDOC-CRM documentation for P2_has_type

---

## 📜 Version Information

- **Package Version**: 1.0
- **Property Created**: 2025-10-16
- **Documentation Updated**: 2025-10-26
- **CIDOC-CRM Version**: 7.1.3
- **Getty AAT Version**: Current (2025)

---

## ✅ Implementation Checklist

Use this checklist to track your implementation progress:

### Pre-Implementation
- [ ] Read this README completely
- [ ] Review `has-gender-documentation.md`
- [ ] Understand CIDOC-CRM P2_has_type pattern
- [ ] Verify ontology contains gmn:P2_1_gender definition

### Ontology Phase
- [ ] Confirm property definition in gmn_ontology.ttl (line 223)
- [ ] Verify controlled vocabulary constraints
- [ ] Check AAT term URIs are correct

### Code Implementation Phase
- [ ] Create `transform_p2_1_gender()` function
- [ ] Add function call to `transform_item()`
- [ ] Verify placement in transformation sequence
- [ ] Review error handling

### Testing Phase
- [ ] Test with male gender value
- [ ] Test with female gender value
- [ ] Test with intersex gender value
- [ ] Test with missing gender property
- [ ] Verify CIDOC-CRM compliance of output

### Documentation Phase
- [ ] Update project documentation with examples
- [ ] Add usage guidelines
- [ ] Document data entry best practices
- [ ] Include gender recording policies

### Validation Phase
- [ ] Run transformation on real data
- [ ] Validate JSON-LD output
- [ ] Check for transformation errors
- [ ] Verify semantic correctness

### Deployment
- [ ] Commit changes to version control
- [ ] Update deployment documentation
- [ ] Notify team of new property availability
- [ ] Train data entry staff on usage

---

## 🎓 Learning Resources

### Understanding Gender in Historical Records

Gender recording in historical documents presents unique challenges:
- **Historical terminology**: Terms vary across time periods and cultures
- **Document limitations**: Not all documents record gender explicitly
- **Inference caution**: Avoid inferring gender from names or roles alone
- **Cultural sensitivity**: Respect historical and cultural contexts

### CIDOC-CRM Type Pattern

The P2_has_type pattern is widely used in CIDOC-CRM for classification:
- **Flexible typing**: Allows multiple types per entity
- **Controlled vocabularies**: Encourages use of standard terms
- **Semantic clarity**: Makes classification explicit and queryable
- **Extensibility**: New types can be added as needed

---

## 🔍 Troubleshooting

### Common Issues and Solutions

**Issue**: Property not transforming
- **Solution**: Verify function is called in `transform_item()`

**Issue**: Invalid gender value
- **Solution**: Check that AAT URI matches controlled vocabulary

**Issue**: Missing @type in output
- **Solution**: Ensure E55_Type is added in transformation

**Issue**: Property remains in output
- **Solution**: Verify `del data['gmn:P2_1_gender']` executes

---

## 📈 Future Enhancements

Potential future improvements:
1. **Extended vocabulary**: Consider adding more nuanced gender terms
2. **Temporal gender**: Record gender changes over time
3. **Source attribution**: Link gender information to specific documents
4. **Confidence levels**: Indicate certainty of gender attribution

---

*This implementation package follows GMN ontology standards and CIDOC-CRM best practices. For the most current information, refer to the official GMN ontology repository and CIDOC-CRM documentation.*
