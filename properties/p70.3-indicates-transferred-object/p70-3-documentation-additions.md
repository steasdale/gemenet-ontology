# P70.3 Indicates Transferred Object - Documentation Additions

## Purpose

This document provides additional notes, updates, and integration guidance for the `gmn:P70_3_indicates_transferred_object` property that should be incorporated into existing project documentation.

## Updates to Main GMN Ontology Documentation

### Property List Addition

Add to the main properties list in `gmn_ontology.ttl` documentation:

```
P70.3 indicates transferred object
- Domain: E31.2 Sales Contract, E31.6 Lease Contract, E31.7 Donation Contract, E31.8 Dowry Contract
- Range: E18_Physical_Thing, E21_Person, E22.1_Building, E22.2_Moveable_Property, E24_Physical_Human-Made_Thing, E53_Place
- Pattern: E13 Attribute Assignment
- Status: Active
- Version: 1.0 (added 2025-10-28)
```

### Supporting Properties Addition

Add these supporting properties to the documentation:

```
P2.1 has type (object classification)
P54.1 has count (quantity)
P43.1 has dimension (measurements)
P56.1 has color
P27.1 has origin (provenance)
has_monetary_value_lire (L.S.D format)
has_monetary_value_soldi (L.S.D format)
has_monetary_value_denari (L.S.D format)
has_monetary_value_currency
has_monetary_value_provenance
```

## Updates to Contract Type Documentation

### Sales Contract (E31.2) Updates

Add to `E31_2_Sales_Contract` documentation:

**New Property**: `gmn:P70_3_indicates_transferred_object`

This property provides an alternative to the simple P24 reference for objects being sold, enabling rich semantic modeling of transferred items including type, quantity, measurements, value, and provenance.

**When to Use**:
- Use P70.3 when objects need detailed properties
- Use simple P70.3 references for well-documented commodities
- Combine with P70.16-17 for overall transaction pricing

**Example**:
```turtle
<sales_contract_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_indicates_seller <merchant_001> ;
    gmn:P70_2_indicates_buyer <merchant_002> ;
    gmn:P70_3_indicates_transferred_object <object_salt_001> ;
    gmn:P70_16_documents_sale_price_amount "450.00"^^xsd:decimal .
```

### Lease Contract (E31.6) Updates

Add to `E31_6_Lease_Contract` documentation:

**New Property**: `gmn:P70_3_indicates_transferred_object`

For lease contracts, this property documents objects transferred under custody (P30) rather than ownership (P24). The transformation automatically uses E10_Transfer_of_Custody instead of E8_Acquisition.

**Key Difference**: Lease contracts transfer temporary custody, not permanent ownership. The E13 Attribute Assignment uses P30_transferred_custody_of instead of P24_transferred_title_of.

### Donation Contract (E31.7) Updates

Add to `E31_7_Donation_Contract` documentation:

**Alternative Property**: `gmn:P70_3_indicates_transferred_object`

Can be used instead of `gmn:P70_33_indicates_object_of_donation` when objects require detailed property modeling.

**Comparison**:
- **P70.33**: Simpler, direct link to object
- **P70.3**: Richer, includes E13 pattern with object properties

Both are valid; choose based on data granularity needs.

### Dowry Contract (E31.8) Updates

Add to `E31_8_Dowry_Contract` documentation:

**Alternative Property**: `gmn:P70_3_indicates_transferred_object`

Can be used instead of `gmn:P70_34_indicates_object_of_dowry` when objects require detailed property modeling.

**Use Case**: Particularly useful for dowries involving multiple items with varying values, measurements, or conditions.

## Integration with Transformation Script

### Main Script Updates (gmn_to_cidoc_transform.py)

Add the following sections:

**1. Import Section** (after existing imports):
```python
# P70.3 Transformation Functions
from p70_3_transformation import (
    transform_p70_3_indicates_transferred_object,
    transform_object_properties,
    get_or_create_activity
)
```

**2. AAT Constants Section** (add to existing constants):
```python
# Object property types
AAT_WEIGHT = "http://vocab.getty.edu/page/aat/300056240"
AAT_VOLUME = "http://vocab.getty.edu/page/aat/300055624"
AAT_LENGTH = "http://vocab.getty.edu/page/aat/300055645"
AAT_MONETARY_VALUE = "http://vocab.getty.edu/page/aat/300055997"
AAT_COLOR = "http://vocab.getty.edu/page/aat/300056130"
```

**3. Transform Item Function** (add to transform_item):
```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    
    # ... existing transformations (P1_1, P1_2, etc.) ...
    
    # P70 series for contracts
    item = transform_p70_1_indicates_seller(item)
    item = transform_p70_2_indicates_buyer(item)
    
    # P70.3 Transferred Object (E13 pattern) - ADD THIS
    item = transform_p70_3_indicates_transferred_object(item)
    
    item = transform_p70_16_documents_sale_price(item)
    # ... rest of P70 transformations ...
    
    # Object property transformations - ADD THIS
    item_types = item.get('@type', [])
    if not isinstance(item_types, list):
        item_types = [item_types]
    
    is_object = any(
        'E18_Physical_Thing' in str(t) or
        'E24_Physical_Human-Made_Thing' in str(t) or
        'E22_' in str(t)
        for t in item_types
    )
    
    if is_object:
        item = transform_object_properties(item)
    
    # ... rest of transformations ...
    
    return item
```

## Comparison with Existing Properties

### P70.3 vs P70.33 (Object of Donation)

| Feature | P70.3 | P70.33 |
|---------|-------|--------|
| **Complexity** | High (E13 pattern) | Low (direct link) |
| **Object Properties** | Full support | Limited |
| **Use Cases** | Detailed documentation | Simple references |
| **Transformation** | Complex | Simple |
| **Reusability** | High (separate resources) | Medium |
| **Data Entry** | More steps | Fewer steps |
| **Semantic Richness** | Maximum | Basic |

**Recommendation**: Use P70.3 for research-focused projects requiring detailed object analysis. Use P70.33 for projects prioritizing data entry speed over granularity.

### P70.3 vs P70.34 (Object of Dowry)

Similar comparison to P70.33. The key decision factor is whether you need:
- **Detailed object properties**: Use P70.3
- **Simple object references**: Use P70.34

Both can coexist in the same ontology for different use cases.

### P70.3 vs Direct P24 on E8

Some implementations might use direct P24_transferred_title_of on the E8_Acquisition. P70.3's E13 pattern offers advantages:

1. **Attribution Context**: Explicitly documents that the property assignment comes from the contract
2. **Type Specification**: Can specify object type at attribution level
3. **Property Disambiguation**: Clear distinction between P24 (title) and P30 (custody)
4. **Source Tracking**: Better provenance for property assertions

## Vocabulary Management

### Recommended Controlled Vocabularies

**Object Types** (P2.1):
1. **Primary**: Getty AAT (http://vocab.getty.edu/aat/)
2. **Fallback**: Project-specific commodity list
3. **Custom**: Local terminology with AAT mappings

**Colors** (P56.1):
Create custom vocabulary with both English and Latin terms:
- white / albus
- black / niger  
- red / ruber
- blue / caeruleus
- green / viridis
- yellow / flavus
- brown / brunneus
- gray / griseus

**Medieval Units** (dimension P91):
Document regional variations:

*Genoese System*:
- Rubbio (weight, ~8-9 kg)
- Cantaro (weight, ~47 kg)
- Mina (weight)
- Congio (volume)

*Venetian System*:
- Libra (weight)
- Barile (volume)
- Miglio (length)

*Florentine System*:
- Libra (weight)
- Braccio (length)
- Staio (volume)

### Creating Vocabularies in Omeka-S

**Step 1**: Install Custom Vocab module

**Step 2**: Create vocabularies:
1. Navigate to Modules → Custom Vocab
2. Click "Add Vocabulary"
3. Name: "Object Types (Commodities)"
4. Add terms (one per line):
   ```
   Salt (sale) | http://vocab.getty.edu/page/aat/300010967
   Wool (lana) | http://vocab.getty.edu/page/aat/300243430
   Cloth (pannos) | http://vocab.getty.edu/page/aat/300014063
   Wine (vinum) | http://vocab.getty.edu/page/aat/300379690
   Wheat (granum) | http://vocab.getty.edu/page/aat/300387009
   [continue for all commodity types...]
   ```

**Step 3**: Link vocabularies to properties in resource templates

## Data Entry Guidelines

### Standard Operating Procedure for Object Entry

**Phase 1: Object Resource Creation**
1. Create new item with "Transferred Object" template
2. Enter descriptive title
3. Set resource class (E24_Physical_Human-Made_Thing)
4. Complete required fields (minimum: type)

**Phase 2: Basic Properties**
5. Add name (P1_1) if mentioned in source
6. Select type (P2_1) from vocabulary
7. Enter count/quantity (P54_1) if specified
8. Note any uncertainty in editorial notes

**Phase 3: Physical Properties** (if documented)
9. Create dimension resource for measurements
10. Add color if specified
11. Link to origin place if known

**Phase 4: Monetary Value** (if documented)
12. Enter lire value
13. Add soldi/denari if specified
14. Link to currency type
15. **CRITICAL**: Document provenance (folio, line, method)

**Phase 5: Link to Contract**
16. Save object resource
17. Open contract resource
18. Add P70.3 property
19. Link to object resource
20. Save contract

### Quality Control Checklist

Before marking object complete:
- [ ] Type is specified (required)
- [ ] Count is entered if document specifies
- [ ] At least one measurement if document specifies
- [ ] Color noted if document specifies
- [ ] Monetary value has provenance citation
- [ ] Object is linked to at least one contract
- [ ] Uncertain information is noted
- [ ] Controlled vocabulary terms are used
- [ ] Units are specified for all measurements

## Query Examples for Analysis

### Find All Objects of a Type

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?object ?name ?count ?contract
WHERE {
  ?contract gmn:P70_3_indicates_transferred_object ?object .
  ?object cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300010967> . # salt
  OPTIONAL { ?object gmn:P54_1_has_count ?count }
  OPTIONAL { ?object gmn:P1_1_has_name ?name }
}
```

### Find Objects by Origin

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?object ?type ?origin
WHERE {
  ?contract gmn:P70_3_indicates_transferred_object ?object .
  ?object cidoc:P2_has_type ?type .
  ?object cidoc:P27_moved_from ?origin .
  FILTER (?origin = <place_ibiza>)
}
```

### Calculate Total Value by Commodity

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?type (SUM(?value) as ?total_value)
WHERE {
  ?object cidoc:P2_has_type ?type .
  ?object gmn:has_monetary_value_lire ?value .
}
GROUP BY ?type
ORDER BY DESC(?total_value)
```

### Find Contracts with Multiple Objects

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

SELECT ?contract (COUNT(?object) as ?object_count)
WHERE {
  ?contract gmn:P70_3_indicates_transferred_object ?object .
}
GROUP BY ?contract
HAVING (COUNT(?object) > 1)
ORDER BY DESC(?object_count)
```

## Migration Strategies

### From Simple References to P70.3

**Scenario**: You have contracts with text descriptions of objects

**Strategy**:
1. Export existing contracts
2. Parse object descriptions
3. Create object resources with extracted properties
4. Replace text with P70.3 links
5. Validate completeness

**Example**:
```
Before:
<contract001> gmn:object_description "100 rubbi of white salt from Ibiza" .

After:
<contract001> gmn:P70_3_indicates_transferred_object <object_salt_001> .
<object_salt_001> gmn:P2_1_has_type <aat:300010967> ;
                  gmn:P54_1_has_count "100"^^xsd:integer ;
                  gmn:P56_1_has_color "white" ;
                  gmn:P27_1_has_origin <place_ibiza> .
```

### From P70.33/34 to P70.3

**Scenario**: You want richer semantics for some donation/dowry objects

**Strategy**:
1. Identify objects needing detailed properties
2. Create enhanced object resources
3. Add P70.3 alongside or instead of P70.33/34
4. Document decision rationale
5. Maintain consistency within contract types

**Both properties can coexist**:
```turtle
<donation001> 
    gmn:P70_33_indicates_object_of_donation <simple_house_001> ;
    gmn:P70_3_indicates_transferred_object <detailed_cargo_001> .
```

## Performance Considerations

### Database Impact

Adding E13 Attribute Assignment pattern increases triple count:

**Before (simple reference)**:
- 1 triple: Contract → Object

**After (E13 pattern)**:
- 5-10 triples: Contract → Activity → E13 → Object + properties

**Recommendation**: 
- Acceptable for <10,000 objects
- Consider optimization for larger datasets
- Index key properties (type, value, origin)

### Query Optimization

For large datasets:
1. Index frequently queried properties
2. Cache common aggregations
3. Use materialized views for complex patterns
4. Consider SPARQL query optimization
5. Monitor query performance

### Data Entry Efficiency

To speed up entry:
1. Create templates for common object types
2. Batch create objects of same type
3. Use import tools for bulk data
4. Provide autocomplete for vocabularies
5. Train team on efficient workflows

## Future Extensions

### Possible Enhancements

**1. Object Condition**
Add property for documenting object condition:
```turtle
gmn:has_condition
    rdfs:domain cidoc:E18_Physical_Thing ;
    rdfs:range xsd:string .
```

**2. Quality Indicators**
Add quality/grade specifications:
```turtle
gmn:has_quality_grade
    rdfs:domain cidoc:E18_Physical_Thing ;
    rdfs:range cidoc:E55_Type .
```

**3. Packaging**
Document how objects were packaged:
```turtle
gmn:has_packaging
    rdfs:domain cidoc:E18_Physical_Thing ;
    rdfs:range xsd:string .
```

**4. Insurance Value**
Separate insurance from sale value:
```turtle
gmn:has_insurance_value
    rdfs:domain cidoc:E18_Physical_Thing ;
    rdfs:range cidoc:E54_Dimension .
```

### Expansion to Other Contract Types

Consider adding P70.3 support for:
- Partnership contracts (societas)
- Exchange contracts (cambium)
- Loan contracts (mutuum)
- Insurance contracts (securitas)

## Training Materials

### For Data Entry Team

**Topics to Cover**:
1. Understanding object resources
2. Using controlled vocabularies
3. Entering measurements properly
4. Documenting monetary values with provenance
5. Linking objects to contracts
6. Quality control procedures

**Hands-on Exercises**:
- Create sample objects from transcriptions
- Practice linking to contracts
- Work through ambiguous cases
- Validate transformations

### For Researchers

**Topics to Cover**:
1. Querying object data
2. Understanding E13 pattern
3. Analyzing transformed data
4. Interpreting CIDOC-CRM output
5. Citing object provenance

## Troubleshooting Common Issues

### Issue: Object Not Appearing in Contract Link

**Cause**: Resource class mismatch or visibility settings

**Solution**:
1. Verify object has compatible resource class
2. Check object is public/published
3. Clear Omeka-S cache
4. Verify property configuration in template

### Issue: Monetary Values Not Transforming

**Cause**: Missing currency or improper data type

**Solution**:
1. Ensure currency is specified
2. Verify numeric data type for lire
3. Check transformation script handles missing values
4. Add default currency if needed

### Issue: Measurements Missing Units

**Cause**: Dimension resource incomplete

**Solution**:
1. Always create complete dimension resources
2. Require unit selection in templates
3. Validate before saving
4. Use controlled vocabulary for units

### Issue: E13 Nodes Not Creating

**Cause**: Transformation script not called or activity missing

**Solution**:
1. Verify transform function is called
2. Check activity creation logic
3. Validate contract type detection
4. Review transformation logs

## Contact and Support

For questions about P70.3 implementation:
1. Review the comprehensive documentation files
2. Check the transformation code comments
3. Consult the ontology definitions
4. Contact the project team

## Conclusion

The P70.3 property represents a significant enhancement to the GMN ontology, enabling rich semantic modeling of transferred objects with full CIDOC-CRM compliance. While more complex than simpler shortcut properties, it provides the granularity needed for serious historical research and analysis.

Key success factors:
- Proper vocabulary management
- Consistent data entry procedures
- Regular quality control
- Team training and support
- Careful transformation testing

---

**Document Version**: 1.0  
**Last Updated**: October 28, 2025  
**Author**: Genoese Merchant Networks Project
