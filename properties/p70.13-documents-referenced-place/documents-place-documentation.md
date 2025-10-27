# Ontology Documentation: P70.13 Documents Referenced Place
## Semantic Specification and CIDOC-CRM Mapping

---

## Property Overview

### Basic Information

**Property URI**: `gmn:P70_13_documents_referenced_place`

**Label**: "P70.13 documents referenced place" (English)

**Created**: 2025-10-27

**Status**: Active

**Version**: 1.0

---

## Formal Definition

### Domain and Range

**Domain**: `gmn:E31_2_Sales_Contract`
- The property applies to sales contract documents
- Sales contracts are a subclass of E31_Document in the GMN ontology
- This specificity ensures the property is used in appropriate context

**Range**: `cidoc:E53_Place`
- The property points to places (geographic locations)
- Places can be natural or human-made locations
- Follows CIDOC-CRM's place entity definition

### Superproperty

**rdfs:subPropertyOf**: `cidoc:P67_refers_to`

This property is a specialization of CIDOC-CRM's P67 "refers to" property, which establishes a general reference relationship between a document and an entity mentioned in its content.

**P67 Definition** (from CIDOC-CRM):
> "This property documents that an instance of E89 Propositional Object makes a statement about an instance of E1 CRM Entity. P67 refers to (is referred to by) has the P67.1 has type link to an instance of E55 Type. This is intended to allow a more detailed description of the type of reference. This differs from P129 is about (is subject of), which describes the primary subject or subjects of the E89 Propositional Object."

### Quantification

**Cardinality**: Many to many (0,n:0,n)
- One contract can reference zero or more places
- One place can be referenced by zero or more contracts
- Optional property (contracts don't require referenced places)

---

## Semantic Intent

### Purpose Statement

This property captures places that are **mentioned in the text** of a sales contract. These are places that appear in the narrative or descriptive portions of the contract, particularly:

1. **Boundary Descriptions**: Adjacent properties or landmarks used to describe property boundaries
2. **Locational Context**: Districts, parishes, neighborhoods, or geographic features providing context
3. **Reference Points**: Landmarks or known locations used to orient the reader
4. **Comparative Locations**: Other properties or places mentioned for comparison

### Critical Distinction

**This property is NOT for**:
- ❌ The place where the contract was created/enacted → Use `gmn:P94i_3_has_place_of_enactment`
- ❌ The location of property being sold → Described within the property object (P70.3)
- ❌ Places where parties resided → Use person-level place properties

**This property IS for**:
- ✅ Places mentioned in boundary descriptions
- ✅ Landmarks referenced in contract text
- ✅ Districts/parishes named in the document
- ✅ Geographic features mentioned for context

### Textual vs. Transactional

The key semantic distinction is between:
- **Textual presence**: The place is written in the document text → **P70.13**
- **Transactional role**: The place is where something happened → **Other properties**

This property acknowledges textual presence without claiming participation in the documented event.

---

## CIDOC-CRM Mapping

### Simplified Form (GMN)

```turtle
contract:123 gmn:P70_13_documents_referenced_place place:rialto .
```

### Expanded Form (CIDOC-CRM)

```turtle
contract:123 cidoc:P67_refers_to place:rialto .

place:rialto a cidoc:E53_Place .
```

### Path Representation

```
E31_Document --P67_refers_to--> E53_Place
```

This is one of the simplest property patterns in the GMN ontology - a direct reference relationship with no intermediate nodes.

### Transformation Logic

**Input** (JSON-LD with GMN property):
```json
{
  "@id": "contract:456",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_13_documents_referenced_place": [
    "place:san_polo",
    "place:grand_canal"
  ]
}
```

**Output** (JSON-LD with CIDOC-CRM):
```json
{
  "@id": "contract:456",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "place:san_polo",
      "@type": "cidoc:E53_Place"
    },
    {
      "@id": "place:grand_canal",
      "@type": "cidoc:E53_Place"
    }
  ]
}
```

**Transformation Steps**:
1. Extract place reference(s) from GMN property
2. Create P67_refers_to array if not present
3. For each place:
   - If URI string → wrap in object with @id and @type
   - If object → ensure @type is E53_Place
4. Add to P67_refers_to array
5. Remove GMN property

---

## Usage Patterns

### Pattern 1: Single Referenced Place

**Scenario**: Contract mentions one boundary landmark

**GMN Input**:
```json
{
  "@id": "contract:1458-03-15-001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_13_documents_referenced_place": "place:church_san_giacomo"
}
```

**CIDOC-CRM Output**:
```json
{
  "@id": "contract:1458-03-15-001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "place:church_san_giacomo",
      "@type": "cidoc:E53_Place"
    }
  ]
}
```

### Pattern 2: Multiple Referenced Places

**Scenario**: Contract describes property with several boundary markers

**GMN Input**:
```json
{
  "@id": "contract:1459-07-22-003",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_13_documents_referenced_place": [
    "place:property_giovanni_corner",
    "place:canal_de_rio",
    "place:calle_lunga",
    "place:campo_santa_maria"
  ]
}
```

**CIDOC-CRM Output**:
```json
{
  "@id": "contract:1459-07-22-003",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "place:property_giovanni_corner",
      "@type": "cidoc:E53_Place"
    },
    {
      "@id": "place:canal_de_rio",
      "@type": "cidoc:E53_Place"
    },
    {
      "@id": "place:calle_lunga",
      "@type": "cidoc:E53_Place"
    },
    {
      "@id": "place:campo_santa_maria",
      "@type": "cidoc:E53_Place"
    }
  ]
}
```

### Pattern 3: Detailed Place Objects

**Scenario**: Places with additional metadata

**GMN Input**:
```json
{
  "@id": "contract:1460-11-08-007",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_13_documents_referenced_place": [
    {
      "@id": "place:rialto_bridge",
      "@type": "cidoc:E53_Place",
      "rdfs:label": "Ponte di Rialto",
      "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300008193",
      "cidoc:P89_falls_within": "place:venice"
    }
  ]
}
```

**CIDOC-CRM Output**:
```json
{
  "@id": "contract:1460-11-08-007",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "place:rialto_bridge",
      "@type": "cidoc:E53_Place",
      "rdfs:label": "Ponte di Rialto",
      "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300008193",
      "cidoc:P89_falls_within": "place:venice"
    }
  ]
}
```

**Note**: All place metadata is preserved during transformation.

---

## Relationship to Other Properties

### Comparison with Similar Properties

#### P70.13 vs P94i.3 (Place of Enactment)

| Aspect | P70.13 Referenced Place | P94i.3 Place of Enactment |
|--------|------------------------|---------------------------|
| **Semantic** | Place mentioned in text | Place where contract created |
| **CIDOC Path** | P67_refers_to | P94i > E65_Creation > P7_took_place_at |
| **Typical Value** | Landmarks, boundaries | Notary office, public building |
| **Multiplicity** | Often multiple | Usually single |
| **Example** | "near the Rialto" | "in the notary office of San Marco" |

**Usage Decision**:
- Use P70.13 for places that appear as references in the contract narrative
- Use P94i.3 for the physical location where the contract document was created

#### P70.13 vs P70.3 (Documents Transfer Of)

| Aspect | P70.13 Referenced Place | P70.3 Documents Transfer Of |
|--------|------------------------|----------------------------|
| **Semantic** | Supporting geographic context | The property being sold |
| **Type** | Any place | Physical property (land, building) |
| **Role** | Reference/landmark | Transaction subject |
| **Integration** | May overlap (property boundaries) | Separate property entity |

**Usage Decision**:
- Use P70.13 for neighboring properties or landmarks mentioned
- Use P70.3 for the actual property being transferred
- The sold property itself has its own location (within P70.3 object)

#### P70.13 vs P70.11 (Referenced Person)

| Aspect | P70.13 Referenced Place | P70.11 Referenced Person |
|--------|------------------------|--------------------------|
| **Semantic** | Place mentioned in text | Person mentioned in text |
| **Range** | E53_Place | E21_Person |
| **Path** | P67_refers_to | P67_refers_to |
| **Pattern** | Same reference pattern | Same reference pattern |

**Parallel Structure**: These properties follow the same semantic pattern for different entity types.

### Property Clustering

P70.13 belongs to the **"Referenced Entities"** cluster:
- **P70.11**: Referenced Person
- **P70.13**: Referenced Place ← This property
- **P70.14**: Referenced Object

All use P67_refers_to and represent textual mentions without implying participation in the transaction.

---

## Examples from Historical Contracts

### Example 1: Venetian House Sale with Boundary Description

**Contract**: Sale of house in San Polo parish, 1458

**Original Latin Text** (abbreviated):
> "...domus sita in confinio Sancti Pauli, cui coherent: ab uno latere domus Johannis de Corner, ab alio via publica, a tertio canale de Rio, a quarto campus Sancte Marie..."

**Translation**:
> "...house situated in the parish of San Polo, bounded by: on one side the house of Giovanni de Corner, on another the public street, on the third the Rio canal, on the fourth the campo of Santa Maria..."

**GMN Encoding**:
```json
{
  "@id": "contract:ASV-001-1458",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P1_1_has_name": "Sale of house in San Polo, 1458",
  "gmn:P70_13_documents_referenced_place": [
    {
      "@id": "place:parish_san_polo",
      "rdfs:label": "Parish of San Polo"
    },
    {
      "@id": "place:property_giovanni_corner",
      "rdfs:label": "House of Giovanni de Corner",
      "rdfs:comment": "Adjacent property, eastern boundary"
    },
    {
      "@id": "place:rio_canal",
      "rdfs:label": "Rio Canal",
      "rdfs:comment": "Western boundary"
    },
    {
      "@id": "place:campo_santa_maria",
      "rdfs:label": "Campo of Santa Maria",
      "rdfs:comment": "Southern boundary"
    }
  ]
}
```

### Example 2: Commercial Property Near Rialto

**Contract**: Sale of warehouse near Rialto market, 1460

**Original Text**:
> "...magazzino prope pontem Realti, in regione Sancti Johannis Crisostomi..."

**Translation**:
> "...warehouse near the Rialto bridge, in the district of San Giovanni Grisostomo..."

**GMN Encoding**:
```json
{
  "@id": "contract:ASV-002-1460",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P1_1_has_name": "Sale of warehouse near Rialto, 1460",
  "gmn:P70_13_documents_referenced_place": [
    {
      "@id": "place:rialto_bridge",
      "rdfs:label": "Rialto Bridge",
      "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300008193"
    },
    {
      "@id": "place:district_san_giovanni_grisostomo",
      "rdfs:label": "District of San Giovanni Grisostomo",
      "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300000745"
    }
  ]
}
```

### Example 3: Rural Property with Multiple Landmarks

**Contract**: Sale of agricultural land outside Venice, 1462

**Original Text**:
> "...terreno situm in villa Mestre, iuxta ecclesiam Sancti Laurentii, prope viam ducalem, non longe ab hostaria del Leone..."

**Translation**:
> "...land situated in the village of Mestre, next to the church of San Lorenzo, near the ducal road, not far from the Leone inn..."

**GMN Encoding**:
```json
{
  "@id": "contract:ASV-003-1462",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P1_1_has_name": "Sale of agricultural land in Mestre, 1462",
  "gmn:P70_13_documents_referenced_place": [
    {
      "@id": "place:village_mestre",
      "rdfs:label": "Village of Mestre",
      "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300008375"
    },
    {
      "@id": "place:church_san_lorenzo",
      "rdfs:label": "Church of San Lorenzo",
      "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300007466"
    },
    {
      "@id": "place:ducal_road",
      "rdfs:label": "Ducal Road",
      "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300008217"
    },
    {
      "@id": "place:inn_leone",
      "rdfs:label": "Leone Inn",
      "cidoc:P2_has_type": "http://vocab.getty.edu/aat/300007166"
    }
  ]
}
```

---

## Scope Notes

### When to Use This Property

**Use P70.13 when**:
- ✅ A place name appears in the contract text
- ✅ The place provides geographic context or orientation
- ✅ The place is used in boundary descriptions
- ✅ The place is a landmark mentioned for reference
- ✅ The place is a district, parish, or administrative division mentioned

**Do NOT use P70.13 when**:
- ❌ The place is where the contract was created → P94i.3
- ❌ The place is the location of the property being sold → encode within property object
- ❌ The place is where a party resides → person-level property
- ❌ The place is implied but not explicitly mentioned in text

### Interpretation Guidelines

**Explicit vs. Implicit**:
- Record only places **explicitly named** in the contract text
- Do not infer places from context unless clearly indicated
- When uncertain, err on the side of explicit mention

**Level of Specificity**:
- Record places at the specificity level used in the contract
- If contract says "San Polo," record "San Polo" (not just "Venice")
- Create place hierarchy separately, don't collapse into single reference

**Multiple Mentions**:
- Each distinct place gets one reference (no duplication)
- Same place mentioned multiple times → single reference
- Different aspects of same place → still single reference

---

## Technical Specifications

### RDF Serialization

**Turtle Syntax**:
```turtle
@prefix gmn: <http://www.genoamemerchants.net/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

gmn:P70_13_documents_referenced_place
    a owl:ObjectProperty ;
    rdfs:label "P70.13 documents referenced place"@en ;
    rdfs:comment "Simplified property for associating a sales contract with any place referenced or mentioned in the document text."@en ;
    rdfs:subPropertyOf cidoc:P67_refers_to ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E53_Place .
```

**JSON-LD Context**:
```json
{
  "@context": {
    "gmn": "http://www.genoamemerchants.net/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "documents_referenced_place": {
      "@id": "gmn:P70_13_documents_referenced_place",
      "@type": "@id"
    }
  }
}
```

### Data Validation

**SHACL Shape** (example):
```turtle
gmn:P70_13Shape
    a sh:PropertyShape ;
    sh:path gmn:P70_13_documents_referenced_place ;
    sh:class cidoc:E53_Place ;
    sh:nodeKind sh:IRI ;
    sh:severity sh:Warning ;
    sh:message "P70.13 should point to E53_Place instances" .
```

### SPARQL Queries

**Query 1: Find all contracts referencing a specific place**:
```sparql
PREFIX gmn: <http://www.genoamemerchants.net/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?contractName
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            gmn:P70_13_documents_referenced_place <place:rialto_bridge> ;
            gmn:P1_1_has_name ?contractName .
}
```

**Query 2: Count referenced places per contract**:
```sparql
PREFIX gmn: <http://www.genoamemerchants.net/ontology#>

SELECT ?contract (COUNT(?place) AS ?placeCount)
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            gmn:P70_13_documents_referenced_place ?place .
}
GROUP BY ?contract
ORDER BY DESC(?placeCount)
```

**Query 3: Find contracts with no referenced places**:
```sparql
PREFIX gmn: <http://www.genoamemerchants.net/ontology#>

SELECT ?contract
WHERE {
  ?contract a gmn:E31_2_Sales_Contract .
  FILTER NOT EXISTS {
    ?contract gmn:P70_13_documents_referenced_place ?place .
  }
}
```

---

## Implementation Considerations

### Performance

**Index Recommendations**:
- Index on subject (contract URI)
- Index on object (place URI)
- Consider full-text index on place labels for search

**Query Optimization**:
- Cache frequently referenced places
- Use property path queries for place hierarchies
- Batch process transformations for large datasets

### Data Quality

**Validation Checks**:
- ✅ Place URI resolves to valid E53_Place
- ✅ No duplicate place references per contract
- ✅ Place has human-readable label
- ✅ Place type (P2_has_type) is appropriate

**Quality Metrics**:
- Percentage of contracts with referenced places
- Average number of places per contract
- Place reference distribution (most/least common)

### Interoperability

**Linked Data**:
- Use Getty TGN URIs when possible for well-known places
- Link to Wikidata for modern place equivalents
- Provide owl:sameAs links to external place authorities

**Example**:
```turtle
place:rialto_bridge
    a cidoc:E53_Place ;
    rdfs:label "Rialto Bridge"@en ;
    owl:sameAs <http://vocab.getty.edu/tgn/7011751> ;
    owl:sameAs <http://www.wikidata.org/entity/Q1227334> .
```

---

## Versioning and Evolution

### Current Version: 1.0

**Status**: Stable
**Date**: 2025-10-27

### Change Log

**Version 1.0** (2025-10-27):
- Initial property definition
- Documentation created
- Transformation logic implemented
- Examples documented

### Future Considerations

**Potential Enhancements**:
1. Add property for relationship type (boundary, landmark, context)
2. Consider temporal aspects (historical vs. contemporary place names)
3. Evaluate need for place role typing
4. Assess integration with spatial querying

**Backward Compatibility**:
- Changes will maintain backward compatibility
- Deprecation warnings will precede breaking changes
- Migration paths will be documented

---

## References

### CIDOC-CRM Documentation

- **P67 refers to**: http://www.cidoc-crm.org/Property/p67-refers-to/version-7.1
- **E53 Place**: http://www.cidoc-crm.org/Entity/e53-place/version-7.1
- **E31 Document**: http://www.cidoc-crm.org/Entity/e31-document/version-7.1

### Getty Vocabularies

**Place Types (AAT)**:
- Churches: http://vocab.getty.edu/aat/300007466
- Bridges: http://vocab.getty.edu/aat/300008193
- Districts: http://vocab.getty.edu/aat/300000745
- Villages: http://vocab.getty.edu/aat/300008375
- Roads: http://vocab.getty.edu/aat/300008217

**Place Names (TGN)**:
- Venice: http://vocab.getty.edu/tgn/7018159
- Rialto: http://vocab.getty.edu/tgn/7011751

### Project Documentation

- GMN Ontology Specification
- CIDOC-CRM Transformation Guide
- Data Entry Manual
- Property Index

---

## Appendices

### Appendix A: Property Hierarchy

```
cidoc:P67_refers_to
  └── gmn:P70_13_documents_referenced_place
```

### Appendix B: Full Transformation Example

**Before Transformation** (GMN simplified):
```json
{
  "@context": {
    "gmn": "http://www.genoamemerchants.net/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contract/1458-001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P1_1_has_name": "House sale in San Polo",
  "gmn:P70_13_documents_referenced_place": [
    "http://example.org/place/san_polo",
    "http://example.org/place/rialto"
  ]
}
```

**After Transformation** (CIDOC-CRM compliant):
```json
{
  "@context": {
    "gmn": "http://www.genoamemerchants.net/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contract/1458-001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P1_is_identified_by": {
    "@type": "cidoc:E33_E41_Linguistic_Appellation",
    "cidoc:P190_has_symbolic_content": "House sale in San Polo"
  },
  "cidoc:P67_refers_to": [
    {
      "@id": "http://example.org/place/san_polo",
      "@type": "cidoc:E53_Place"
    },
    {
      "@id": "http://example.org/place/rialto",
      "@type": "cidoc:E53_Place"
    }
  ]
}
```

### Appendix C: AAT Terms for Place Types

| AAT ID | Term | Definition | Usage in GMN |
|--------|------|------------|--------------|
| 300000745 | districts | Administrative divisions of cities | Parish, sestiere references |
| 300007466 | churches | Buildings for Christian worship | Boundary landmarks |
| 300008193 | bridges | Structures spanning obstacles | Geographic references |
| 300008217 | roads | Linear transportation routes | Boundary markers |
| 300008375 | villages | Small settlements | Contract location context |

---

**Document Status**: Final  
**Version**: 1.0  
**Last Updated**: 2025-10-27  
**Maintained By**: GMN Ontology Team  
**License**: CC BY 4.0
