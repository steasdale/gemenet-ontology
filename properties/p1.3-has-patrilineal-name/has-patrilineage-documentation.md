# P1.3 Has Patrilineal Name - Ontology Documentation

## Property Definition

```turtle
# Property: P1.3 has patrilineal name
gmn:P1_3_has_patrilineal_name 
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P1.3 has patrilineal name"@en ;
    rdfs:comment "Simplified property for expressing the patrilineal name of a person, which includes their given name followed by their patronymic ancestry (e.g., 'Giacomo Spinola q. Antonio' meaning 'Giacomo Spinola, son of the late Antonio'). This naming pattern is common in medieval and early modern Italian contexts where 'q.' (quondam) indicates a deceased father or ancestor. Represents the full CIDOC-CRM path: P1_is_identified_by > E41_Appellation > P2_has_type <http://vocab.getty.edu/aat/300404651> > P190_has_symbolic_content. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The appellation type is automatically set to AAT 300404651 (patronymics)."@en ;
    rdfs:subPropertyOf cidoc:P1_is_identified_by ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E62_String ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P1_is_identified_by, cidoc:P190_has_symbolic_content, aat:300404651 ;
    owl:equivalentProperty [
        a owl:Restriction ;
        owl:onProperty cidoc:P1_is_identified_by ;
        owl:allValuesFrom [
            a owl:Restriction ;
            owl:onProperty cidoc:P190_has_symbolic_content ;
            owl:hasValue cidoc:E62_String
        ]
    ] ;
    gmn:hasImplicitType aat:300404651 .
```

## Semantic Structure

### CIDOC-CRM Mapping

The `gmn:P1_3_has_patrilineal_name` property is a shortcut that expands to the following CIDOC-CRM structure:

```
E21_Person (the person being named)
  └─ P1_is_identified_by
      └─ E41_Appellation (the patrilineal name appellation)
          ├─ P2_has_type → AAT:300404651 (patronymic)
          │   └─ E55_Type
          └─ P190_has_symbolic_content → "name string"
```

### Property Hierarchy

```
rdf:Property
  └─ cidoc:P1_is_identified_by
      └─ gmn:P1_3_has_patrilineal_name (shortcut property)
```

## Property Specifications

### Basic Metadata

| Attribute | Value |
|-----------|-------|
| **URI** | `gmn:P1_3_has_patrilineal_name` |
| **Label** | P1.3 has patrilineal name |
| **Property Type** | Data Property (DatatypeProperty) |
| **Super-property** | `cidoc:P1_is_identified_by` |
| **Domain** | `cidoc:E21_Person` |
| **Range** | `cidoc:E62_String` |
| **Functional** | No (multiple values allowed) |
| **Created** | 2025-10-17 |

### Semantic Properties

| Attribute | Value |
|-----------|-------|
| **Implicit Type** | `aat:300404651` (patronymics) |
| **Expansion Target** | `cidoc:P1_is_identified_by` → `cidoc:E41_Appellation` |
| **Type Property** | `cidoc:P2_has_type` |
| **Content Property** | `cidoc:P190_has_symbolic_content` |

### Controlled Vocabulary

**AAT Term**: Patronymics  
**AAT URI**: http://vocab.getty.edu/page/aat/300404651  
**AAT ID**: 300404651

**Definition from AAT**: "Names derived from the name of a father or paternal ancestor, usually by the addition of a suffix or prefix meaning 'son of.'"

**Scope Note**: Used for personal names that incorporate the father's or ancestor's name to indicate lineage. Common in many cultural traditions, including medieval Italian contexts where patronymic chains could extend through several generations.

## Historical Context

### Medieval Italian Naming Conventions

In medieval and early modern Italian documentary sources, particularly notarial acts from Genoa and other Italian city-states, persons were commonly identified by patronymic formulas that included:

1. **Given name** (nome): The person's personal name (e.g., Giacomo, Giovanni)
2. **Family name** (cognome): The surname or clan name (e.g., Spinola, Doria)
3. **Patronymic** (patronimico): The father's name, often with "q." (quondam) if deceased

### Common Patterns

#### Pattern 1: Simple Patronymic
```
"Giacomo Spinola q. Antonio"
Translation: Giacomo Spinola, son of the late Antonio
```

#### Pattern 2: Extended Patronymic Chain
```
"Giovanni Doria q. Luca q. Branca"
Translation: Giovanni Doria, son of the late Luca, son of the late Branca
```

#### Pattern 3: Multiple Designations
```
"Bartolomeo de Serra q. Nicolò de Serra"
Translation: Bartolomeo de Serra, son of the late Nicolò de Serra
```

### Abbreviations

| Abbreviation | Latin | Meaning | Context |
|--------------|-------|---------|---------|
| q. | quondam | "formerly", "the late" | Indicates deceased father/ancestor |
| fq. | filius quondam | "son of the late" | More explicit form |
| olim | olim | "formerly" | Alternative to quondam |
| f. | filius | "son of" | For living father |

## Usage Guidelines

### When to Use This Property

Use `gmn:P1_3_has_patrilineal_name` when:

1. The source document explicitly includes patronymic information
2. The name includes generational information (father's name, grandfather's name)
3. The name includes "q.", "quondam", or similar indicators
4. You want to preserve the full patronymic formula as written

### When NOT to Use This Property

Do not use for:

1. Simple given names without patronymic → Use `gmn:P1_1_has_name`
2. Names exactly as written in source without interpretation → Use `gmn:P1_2_has_name_from_source`
3. Place-based names (toponyms) → Use `gmn:P1_4_has_loconym`
4. Occupational or descriptive names → Use appropriate alternative property

### Relationship to Other Name Properties

A person can have multiple name properties simultaneously:

```turtle
<person001> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giacomo Spinola" ;
    gmn:P1_2_has_name_from_source "Jac. Sp. q. Ant." ;
    gmn:P1_3_has_patrilineal_name "Giacomo Spinola q. Antonio" ;
    gmn:P1_4_has_loconym <genoa> .
```

Each property serves a different purpose:
- **P1.1**: Standard, normalized name
- **P1.2**: Exact transcription from source
- **P1.3**: Interpreted patronymic form
- **P1.4**: Geographic association

## Transformation Examples

### Example 1: Basic Patronymic

**Input (Shortcut Form)**:
```turtle
@prefix gmn: <https://genoese-merchants.org/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

<https://example.org/person/giacomo_spinola> a cidoc:E21_Person ;
    gmn:P1_3_has_patrilineal_name "Giacomo Spinola q. Antonio" .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
@prefix gmn: <https://genoese-merchants.org/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix aat: <http://vocab.getty.edu/page/aat/> .

<https://example.org/person/giacomo_spinola> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <https://example.org/person/giacomo_spinola/appellation/patrilineal/12345> .

<https://example.org/person/giacomo_spinola/appellation/patrilineal/12345> a cidoc:E41_Appellation ;
    cidoc:P2_has_type aat:300404651 ;
    cidoc:P190_has_symbolic_content "Giacomo Spinola q. Antonio" .

aat:300404651 a cidoc:E55_Type ;
    rdfs:label "patronymics"@en .
```

### Example 2: Multiple Patronymics for One Person

**Input**:
```turtle
<https://example.org/person/giovanni_doria> a cidoc:E21_Person ;
    gmn:P1_3_has_patrilineal_name "Giovanni Doria q. Luca" ;
    gmn:P1_3_has_patrilineal_name "Giovanni Doria q. Luca q. Branca" .
```

**Output**:
```turtle
<https://example.org/person/giovanni_doria> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <https://example.org/person/giovanni_doria/appellation/patrilineal/12346> ;
    cidoc:P1_is_identified_by <https://example.org/person/giovanni_doria/appellation/patrilineal/12347> .

<https://example.org/person/giovanni_doria/appellation/patrilineal/12346> a cidoc:E41_Appellation ;
    cidoc:P2_has_type aat:300404651 ;
    cidoc:P190_has_symbolic_content "Giovanni Doria q. Luca" .

<https://example.org/person/giovanni_doria/appellation/patrilineal/12347> a cidoc:E41_Appellation ;
    cidoc:P2_has_type aat:300404651 ;
    cidoc:P190_has_symbolic_content "Giovanni Doria q. Luca q. Branca" .
```

**Note**: Multiple patronymic forms for the same person are valid - different documents may use different levels of genealogical detail.

### Example 3: Combined with Other Name Properties

**Input**:
```turtle
<https://example.org/person/bartolomeo> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Bartolomeo de Serra" ;
    gmn:P1_2_has_name_from_source "Bart. de Serra q. Nic." ;
    gmn:P1_3_has_patrilineal_name "Bartolomeo de Serra q. Nicolò de Serra" ;
    gmn:P1_4_has_loconym <https://example.org/place/serra> .
```

**Output**:
```turtle
<https://example.org/person/bartolomeo> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <https://example.org/person/bartolomeo/appellation/name/12348> ;
    cidoc:P1_is_identified_by <https://example.org/person/bartolomeo/appellation/source/12349> ;
    cidoc:P1_is_identified_by <https://example.org/person/bartolomeo/appellation/patrilineal/12350> ;
    cidoc:P1_is_identified_by <https://example.org/person/bartolomeo/appellation/loconym/12351> .

<https://example.org/person/bartolomeo/appellation/name/12348> a cidoc:E41_Appellation ;
    cidoc:P2_has_type aat:300404688 ;  # "names"
    cidoc:P190_has_symbolic_content "Bartolomeo de Serra" .

<https://example.org/person/bartolomeo/appellation/source/12349> a cidoc:E41_Appellation ;
    cidoc:P2_has_type aat:300456607 ;  # "names from source"
    cidoc:P190_has_symbolic_content "Bart. de Serra q. Nic." .

<https://example.org/person/bartolomeo/appellation/patrilineal/12350> a cidoc:E41_Appellation ;
    cidoc:P2_has_type aat:300404651 ;  # "patronymics"
    cidoc:P190_has_symbolic_content "Bartolomeo de Serra q. Nicolò de Serra" .

<https://example.org/person/bartolomeo/appellation/loconym/12351> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <https://www.wikidata.org/wiki/Q17143070> ;  # "loconym"
    cidoc:P67_refers_to <https://example.org/place/serra> .
```

### Example 4: JSON-LD Format

**Input**:
```json
{
  "@context": {
    "gmn": "https://genoese-merchants.org/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "https://example.org/person/giacomo",
  "@type": "cidoc:E21_Person",
  "gmn:P1_3_has_patrilineal_name": [
    {
      "@value": "Giacomo Spinola q. Antonio"
    }
  ]
}
```

**Output**:
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "aat": "http://vocab.getty.edu/page/aat/"
  },
  "@id": "https://example.org/person/giacomo",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "https://example.org/person/giacomo/appellation/patrilineal/12352",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Giacomo Spinola q. Antonio"
    }
  ]
}
```

## Data Quality Considerations

### Standardization

While the property accepts free-text input, consider these guidelines:

1. **Consistent Abbreviations**: Use standardized forms (e.g., "q." rather than "qd.", "quond.")
2. **Spacing**: Maintain consistent spacing around abbreviations
3. **Capitalization**: Follow source document conventions for proper names
4. **Diacritics**: Preserve original diacritical marks when present

### Validation Rules

Implement these validation checks in data entry systems:

1. **Required Format**: Should include at least one genealogical indicator (q., f., etc.)
2. **Person Name**: Should begin with a proper name
3. **Length**: Typically 10-100 characters
4. **Characters**: Allow letters, spaces, periods, apostrophes, and hyphens

### Common Data Entry Errors

| Error | Example | Correction |
|-------|---------|------------|
| Missing space after abbreviation | "Giacomo q.Antonio" | "Giacomo q. Antonio" |
| Inconsistent abbreviation | "Giacomo qd Antonio" | "Giacomo q. Antonio" |
| Missing family name | "Giacomo q. Antonio" (if Spinola is family name) | "Giacomo Spinola q. Antonio" |
| Mixing name types | Using patronymic for place names | Use separate properties |

## Querying Patterns

### SPARQL Examples

**Query 1: Find all persons with patronymic names**
```sparql
PREFIX gmn: <https://genoese-merchants.org/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?patronymic
WHERE {
  ?person a cidoc:E21_Person ;
          gmn:P1_3_has_patrilineal_name ?patronymic .
}
```

**Query 2: Find persons whose father was named "Antonio"**
```sparql
PREFIX gmn: <https://genoese-merchants.org/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?patronymic
WHERE {
  ?person a cidoc:E21_Person ;
          gmn:P1_3_has_patrilineal_name ?patronymic .
  FILTER(CONTAINS(LCASE(?patronymic), "q. antonio"))
}
```

**Query 3: Find all patronymic appellations (expanded form)**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/page/aat/>

SELECT ?person ?patronymic
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by ?appellation .
  ?appellation a cidoc:E41_Appellation ;
               cidoc:P2_has_type aat:300404651 ;
               cidoc:P190_has_symbolic_content ?patronymic .
}
```

## Related Properties

### Name Property Family (P1.x)

| Property | Purpose | Example |
|----------|---------|---------|
| **P1.1** has name | General normalized name | "Giacomo Spinola" |
| **P1.2** has name from source | Exact transcription | "Jac. Sp. q. Ant." |
| **P1.3** has patrilineal name | Patronymic with lineage | "Giacomo Spinola q. Antonio" |
| **P1.4** has loconym | Place-based name | Reference to Genoa |

### CIDOC-CRM Base Properties

| Property | Description |
|----------|-------------|
| `cidoc:P1_is_identified_by` | Links person to appellation |
| `cidoc:P2_has_type` | Links appellation to type concept |
| `cidoc:P190_has_symbolic_content` | Contains the actual name string |

## Integration with External Resources

### Getty AAT Integration

The property automatically assigns the AAT term for "patronymics" (300404651) to all transformed appellations. This enables:

1. **Interoperability**: Linking with other systems using AAT
2. **Semantic Precision**: Clear type identification
3. **Controlled Vocabulary**: Consistent terminology across datasets

### Future Enhancements

Potential future developments:

1. **Parsing**: Automatic extraction of father's name from patronymic
2. **Relationship Inference**: Creating explicit P_was_father_of relationships
3. **Genealogical Networks**: Building family trees from patronymic data
4. **Variant Detection**: Identifying the same person with different patronymic levels

## Comparison with Other Standards

### Comparison with Schema.org

Schema.org uses `givenName` and `familyName` but doesn't have a specific property for patronymics. The GMN approach provides:

- More specificity for historical naming conventions
- Explicit type assignment (via AAT)
- Full CIDOC-CRM compatibility

### Comparison with FOAF

FOAF uses `foaf:name` as a simple string property. The GMN approach provides:

- Semantic typing of name components
- Historical context preservation
- Cultural and temporal specificity

## Best Practices Summary

1. **Use for patronymic patterns**: Only use when source includes genealogical information
2. **Preserve original form**: Keep the name as close to the source as possible
3. **Combine with other properties**: Use alongside P1.1, P1.2, P1.4 as appropriate
4. **Consistent formatting**: Follow project guidelines for abbreviations
5. **Document sources**: Link to the document where the name appears
6. **Validate data**: Check for proper format and required elements

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-17 | Initial property creation in ontology |
| 1.1 | 2025-10-26 | Documentation package created |

---

**Documentation Version**: 1.0  
**Last Updated**: 2025-10-26  
**Property**: gmn:P1_3_has_patrilineal_name  
**Status**: Implemented and Operational
