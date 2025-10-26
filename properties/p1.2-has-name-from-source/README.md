# has_name_from_source Property Implementation Package

**Property**: `gmn:P1_2_has_name_from_source`  
**Version**: 1.0  
**Date**: October 26, 2025  
**Status**: Ready for Implementation

## Overview

This deliverables package provides complete documentation and implementation files for the `gmn:P1_2_has_name_from_source` property in the Genoese Merchant Networks (GMN) ontology. This property serves as a simplified shortcut for expressing names of persons as they appear in historical source documents, automatically transforming to the full CIDOC-CRM compliant structure.

### What is P1_2_has_name_from_source?

`P1_2_has_name_from_source` is a convenience property that simplifies data entry for historical names found in source documents. Rather than requiring users to manually construct the complex CIDOC-CRM path for recording names as documented in sources, this property provides a single, intuitive entry point that automatically transforms to the formal semantic structure.

**Simplified Entry**:
```turtle
<person/123> gmn:P1_2_has_name_from_source "Iohannes de Nigro" .
```

**Transforms To**:
```turtle
<person/123> cidoc:P1_is_identified_by <appellation/456> .
<appellation/456> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Iohannes de Nigro" .
```

## Key Features

- **Simplified Data Entry**: Single property replaces complex CIDOC-CRM structure
- **Automatic Transformation**: Converts to full semantic structure during processing
- **Historical Fidelity**: Preserves names exactly as they appear in source documents
- **AAT Integration**: Automatically applies AAT term 300456607 (names found in historical sources)
- **CIDOC-CRM Compliance**: Output conforms to CIDOC-CRM standards
- **Omeka-S Compatible**: Works seamlessly with Omeka-S data entry forms

## Quick Start Checklist

### For Implementers

- [ ] **Review Ontology Documentation** (`has-name-from-source-documentation.md`)
- [ ] **Copy TTL to Ontology** (from `has-name-from-source-ontology.ttl`)
- [ ] **Add Python Code** (from `has-name-from-source-transform.py`)
- [ ] **Update Documentation** (using `has-name-from-source-doc-note.txt`)
- [ ] **Validate Ontology** (check RDF syntax)
- [ ] **Test Transformation** (run sample data through script)
- [ ] **Deploy to Omeka-S** (update resource templates)

### For Data Entry Users

- [ ] **Understand Property Purpose**: Read semantic documentation
- [ ] **Learn Entry Format**: Review examples in documentation
- [ ] **Practice with Examples**: Test with sample historical names
- [ ] **Check Output**: Verify transformed CIDOC-CRM structure
- [ ] **Report Issues**: Document any edge cases or problems

## Implementation Summary

### Ontology Changes

**Property Added**: `gmn:P1_2_has_name_from_source`
- Type: `owl:DatatypeProperty`
- Domain: `cidoc:E21_Person`
- Range: `cidoc:E62_String`
- Implicit Type: `aat:300456607` (names found in historical sources)

**Semantic Structure**:
```
E21_Person → P1_is_identified_by → E41_Appellation
    → P2_has_type → E55_Type (aat:300456607)
    → P190_has_symbolic_content → E62_String
```

### Transformation Script Changes

**Function Added**: `transform_p1_2_has_name_from_source(data)`
- Utilizes existing `transform_name_property()` helper function
- Applies AAT type 300456607 automatically
- Generates unique URIs for appellations
- Removes shortcut property after transformation

**Integration Point**: Called in main transformation pipeline

### Documentation Updates

**Tables Added**:
- Simplified Properties comparison table
- AAT Type mappings for name properties
- Transformation examples with input/output

**Examples Added**:
- Basic name from source usage
- Multiple names for single person
- Comparison with other name properties
- CIDOC-CRM output structure

## Package Contents

1. **README.md** (this file)
   - Complete overview and quick-start guide
   - Implementation summary and key features

2. **has-name-from-source-implementation-guide.md**
   - Step-by-step implementation instructions
   - Code snippets with line-by-line explanations
   - Testing procedures and validation steps

3. **has-name-from-source-documentation.md**
   - Complete semantic documentation
   - Class and property specifications
   - Use cases and transformation examples
   - Relationship to CIDOC-CRM

4. **has-name-from-source-ontology.ttl**
   - Ready-to-copy TTL snippet
   - Complete property definition
   - Annotations and metadata

5. **has-name-from-source-transform.py**
   - Ready-to-copy Python code
   - Transformation function
   - Integration instructions

6. **has-name-from-source-doc-note.txt**
   - Documentation additions
   - Tables and examples
   - Formatting for existing documentation

## Use Cases

### Primary Use Case: Recording Historical Names

When transcribing historical documents, record names exactly as they appear in the source:

```turtle
# Name as found in notarial contract dated 1350
<person/spinola_antonio> gmn:P1_2_has_name_from_source "Antonius Spinula" .

# Name as found in commercial letter dated 1360
<person/spinola_antonio> gmn:P1_2_has_name_from_source "Antonio de Spinola" .
```

### Use Case: Variant Name Forms

Track different spellings and forms found across multiple documents:

```turtle
<person/doria_branca> gmn:P1_2_has_name_from_source "Branca de Auria" .
<person/doria_branca> gmn:P1_2_has_name_from_source "Blancha Doria" .
<person/doria_branca> gmn:P1_2_has_name_from_source "Branca Aurie" .
```

### Use Case: Distinguishing from Normalized Names

Use alongside `gmn:P1_1_has_name` for normalized forms:

```turtle
<person/grimaldi_oberto>
    gmn:P1_1_has_name "Oberto Grimaldi" ;  # Normalized modern form
    gmn:P1_2_has_name_from_source "Obertus de Grimaldis" ;  # As in 1345 contract
    gmn:P1_2_has_name_from_source "Oberti Grimaldi" ;  # As in 1352 will
    gmn:P1_2_has_name_from_source "Obertus Grimaldus" .  # As in 1347 letter
```

## Technical Details

### AAT Term Information

**AAT ID**: 300456607  
**Preferred Label**: "names found in historical sources"  
**Scope Note**: Names for people, places, and entities documented in historical records, manuscripts, and archival materials, particularly when those names differ from modern standardized forms.

### CIDOC-CRM Alignment

The property transforms to CIDOC-CRM structure compliant with:
- **E21_Person**: The entity being named
- **P1_is_identified_by**: Links person to appellation
- **E41_Appellation**: The name construct
- **P2_has_type**: Classifies the appellation type
- **E55_Type**: The AAT concept
- **P190_has_symbolic_content**: The actual name string

### Relationship to Other Name Properties

| Property | AAT Type | Purpose |
|----------|----------|---------|
| `P1_1_has_name` | 300404650 (names) | Normalized modern name form |
| `P1_2_has_name_from_source` | 300456607 (names from sources) | Name as documented in historical source |
| `P1_3_has_patrilineal_name` | 300404651 (patronymics) | Patrilineal name with ancestry |
| `P1_4_has_loconym` | 300404651 (loconyms) | Place-based identifier |

## Benefits

### For Data Entry

- **Simplified Input**: Enter names with single property rather than complex structure
- **Historical Accuracy**: Preserve exact forms from source documents
- **Clear Semantics**: Explicit designation that this is a source-documented name
- **Reduced Errors**: Less complex structure means fewer data entry mistakes

### For Data Analysis

- **Source Tracking**: Easily identify which names come directly from historical sources
- **Variant Analysis**: Compare source forms to normalized forms
- **Spelling Patterns**: Study historical orthographic variations
- **Document Dating**: Use name forms as evidence for document dating

### For System Integration

- **Automatic Transformation**: No manual CIDOC-CRM structure creation needed
- **Consistent Output**: Standardized transformation ensures data quality
- **AAT Integration**: Proper terminology classification maintained
- **Interoperability**: CIDOC-CRM output works with other systems

## Implementation Timeline

**Estimated Time**: 2-3 hours

1. **Ontology Update** (30 minutes)
   - Add TTL to ontology file
   - Validate syntax
   - Commit changes

2. **Script Update** (30 minutes)
   - Add transformation code
   - Verify constant definitions
   - Run syntax checks

3. **Testing** (60 minutes)
   - Create test data samples
   - Run transformation script
   - Validate output structure
   - Check AAT type assignment

4. **Documentation** (30 minutes)
   - Add tables and examples
   - Update user guides
   - Create reference materials

## Testing Strategy

### Unit Testing

Test the transformation function with various inputs:

```python
# Test single name
test_data_1 = {
    '@id': 'person/test1',
    '@type': 'cidoc:E21_Person',
    'gmn:P1_2_has_name_from_source': [{'@value': 'Iohannes Spinula'}]
}

# Test multiple names
test_data_2 = {
    '@id': 'person/test2',
    '@type': 'cidoc:E21_Person',
    'gmn:P1_2_has_name_from_source': [
        {'@value': 'Antonius de Auria'},
        {'@value': 'Antonio Doria'}
    ]
}

# Test with special characters
test_data_3 = {
    '@id': 'person/test3',
    '@type': 'cidoc:E21_Person',
    'gmn:P1_2_has_name_from_source': [{'@value': 'Iohannes q. Petri de Nigro'}]
}
```

### Integration Testing

1. Load sample Omeka-S data with `gmn:P1_2_has_name_from_source`
2. Run full transformation pipeline
3. Validate output contains proper E41_Appellation structures
4. Verify AAT type 300456607 is applied correctly
5. Check that original property is removed from output

### Validation Testing

1. **RDF Syntax**: Validate TTL with RDF parser
2. **CIDOC-CRM Compliance**: Check output against CIDOC-CRM specification
3. **AAT Terms**: Verify AAT URIs resolve correctly
4. **URI Generation**: Ensure unique, valid URIs for appellations

## Common Issues and Solutions

### Issue: Names Not Transforming

**Symptom**: `gmn:P1_2_has_name_from_source` appears in output unchanged

**Solutions**:
- Verify transformation function is being called in pipeline
- Check that function name matches in main transformation flow
- Ensure AAT_NAME_FROM_SOURCE constant is defined
- Validate JSON-LD input structure

### Issue: Invalid URIs Generated

**Symptom**: Appellation URIs cause RDF validation errors

**Solutions**:
- Check `generate_appellation_uri()` function
- Verify URI encoding for special characters
- Ensure base URI is properly configured
- Test with various character sets

### Issue: Missing AAT Type

**Symptom**: E41_Appellation lacks P2_has_type link

**Solutions**:
- Verify AAT_NAME_FROM_SOURCE constant value
- Check network access to AAT vocabulary
- Ensure transformation includes type assignment
- Validate AAT URI format

## Support and Resources

### Documentation Files

- **Implementation Guide**: Detailed step-by-step instructions
- **Ontology Documentation**: Complete semantic specifications
- **Code Examples**: Working Python and TTL samples

### External Resources

- **CIDOC-CRM**: http://www.cidoc-crm.org/
- **Getty AAT**: http://www.getty.edu/research/tools/vocabularies/aat/
- **Omeka-S Documentation**: https://omeka.org/s/docs/

### Contact

For questions or issues:
1. Review the implementation guide and documentation
2. Check the testing section for common problems
3. Consult the Genoese Merchant Networks project documentation
4. Contact the ontology maintainer

## Version History

- **1.0** (2025-10-26): Initial release
  - Property definition created
  - Transformation function implemented
  - Documentation completed

## Next Steps

After implementing this property:

1. **Train Users**: Provide documentation to data entry personnel
2. **Update Templates**: Add property to Omeka-S resource templates
3. **Create Examples**: Generate sample records for reference
4. **Monitor Usage**: Track how the property is being used
5. **Collect Feedback**: Gather user experiences and issues
6. **Iterate**: Make improvements based on real-world usage

## License and Attribution

This implementation follows the standards and practices of the Genoese Merchant Networks project and adheres to CIDOC-CRM and Getty AAT usage guidelines.

---

**Ready to implement?** Start with the Implementation Guide (`has-name-from-source-implementation-guide.md`) for detailed step-by-step instructions.
