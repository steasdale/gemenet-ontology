# GMN P1.1 has_name Property - Ontology Documentation

**Version:** 1.0  
**Date:** October 26, 2025  
**Status:** Active Property

## Table of Contents

1. [Property Overview](#property-overview)
2. [Semantic Definition](#semantic-definition)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Technical Specifications](#technical-specifications)
5. [Transformation Details](#transformation-details)
6. [Usage Examples](#usage-examples)
7. [Relationship to Other Properties](#relationship-to-other-properties)
8. [AAT Integration](#aat-integration)
9. [Best Practices](#best-practices)
10. [SPARQL Query Examples](#sparql-query-examples)

---

## Property Overview

### Purpose

`gmn:P1_1_has_name` is a simplified datatype property that provides a convenient way to assign names to any entity in the Genoese Merchant Networks (GMN) database. It serves as a shortcut for the more complex CIDOC-CRM naming structure while maintaining full semantic compliance through automatic transformation.

### Key Characteristics

- **Universal Application:** Works with any entity type (persons, places, contracts, buildings, groups, etc.)
- **Simplified Data Entry:** Single property instead of complex property path
- **Automatic Transformation:** Converts to full CIDOC-CRM structure
- **AAT Integration:** Uses Getty AAT concept for "names" (300404650)
- **Semantic Precision:** Maintains CIDOC-CRM compliance while simplifying workflow

### When to Use

Use `gmn:P1_1_has_name` for:
- General names assigned for cataloging or identification purposes
- Modern, scholarly names given to historical entities
- Display names in user interfaces
- Primary identifiers that don't require specialized typing

---

## Semantic Definition

### Formal Definition

The property represents the complete semantic pattern:

```
E1 CRM Entity
  ├─> P1 is identified by
      └─> E41 Appellation
          ├─> P2 has type → E55 Type (AAT 300404650: names)
          └─> P190 has symbolic content → "Name String"
```

### Ontological Commitment

By using `gmn:P1_1_has_name`, you are asserting that:

1. **Identity:** The entity has a name as an identifying characteristic
2. **Type:** The name is of the general type "name" (as opposed to specific name types like patronymics)
3. **Content:** The string value represents the symbolic content of that name
4. **Formalization:** The name follows controlled vocabulary standards (AAT)

### Domain and Range

- **Domain:** `cidoc:E1_CRM_Entity` (any entity in the CIDOC-CRM hierarchy)
- **Range:** `cidoc:E62_String` (string literals)

This broad domain means the property can be applied to:
- E21 Person
- E53 Place
- E22 Human-Made Object (including buildings, artifacts)
- E31 Document (including contracts, letters)
- E74 Group (including social groups, organizations)
- E55 Type (for naming controlled vocabulary terms)
- And any other CIDOC-CRM entity class

---

## CIDOC-CRM Mapping

### Shortcut Property Pattern

`gmn:P1_1_has_name` implements the CIDOC-CRM shortcut pattern, where a simplified property encodes a longer property path:

**Simplified Form (Input):**
```turtle
<entity> gmn:P1_1_has_name "Entity Name" .
```

**Expanded Form (Output):**
```turtle
<entity> cidoc:P1_is_identified_by <entity/appellation/hash> .

<entity/appellation/hash> 
    a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Entity Name" .

<http://vocab.getty.edu/aat/300404650> 
    a cidoc:E55_Type .
```

### CIDOC-CRM Property Chain

The property encodes the following property chain:

1. **P1 is identified by** (E1 → E41)
   - Connects the entity to an appellation
   - Domain: E1 CRM Entity
   - Range: E41 Appellation

2. **P2 has type** (E41 → E55)
   - Types the appellation as a "name"
   - Domain: E41 Appellation
   - Range: E55 Type

3. **P190 has symbolic content** (E41 → String)
   - Provides the actual name string
   - Domain: E90 Symbolic Object (E41 is subclass)
   - Range: E62 String

### Compliance Notes

This transformation ensures full compliance with CIDOC-CRM guidelines:

- ✅ Uses proper entity classes (E41 Appellation)
- ✅ Types appellations with E55 Type
- ✅ Links to controlled vocabularies (AAT)
- ✅ Maintains proper domain/range relationships
- ✅ Creates referenceable appellation resources

---

## Technical Specifications

### RDF/OWL Definition

```turtle
gmn:P1_1_has_name 
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P1.1 has name"@en ;
    rdfs:comment "Simplified property for expressing the name of any entity in the database (persons, places, things, contracts, etc.). Represents the full CIDOC-CRM path: E1_CRM_Entity > P1_is_identified_by > E41_Appellation > P2_has_type <http://vocab.getty.edu/aat/300404650> > P190_has_symbolic_content. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The appellation type is automatically set to AAT 300404650 (names)."@en ;
    rdfs:subPropertyOf cidoc:P1_is_identified_by ;
    rdfs:domain cidoc:E1_CRM_Entity ;
    rdfs:range cidoc:E62_String ;
    dcterms:created "2025-10-16"^^xsd:date ;
    dcterms:modified "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P1_is_identified_by, cidoc:P190_has_symbolic_content, aat:300404650 ;
    owl:equivalentProperty [
        a owl:Restriction ;
        owl:onProperty cidoc:P1_is_identified_by ;
        owl:allValuesFrom [
            a owl:Restriction ;
            owl:onProperty cidoc:P190_has_symbolic_content ;
            owl:hasValue cidoc:E62_String
        ]
    ] ;
    gmn:hasImplicitType aat:300404650 .
```

### Property Attributes

| Attribute | Value |
|-----------|-------|
| **URI** | http://www.genoesemerchantnetworks.com/ontology#P1_1_has_name |
| **Label** | "P1.1 has name"@en |
| **Type** | owl:DatatypeProperty, rdf:Property |
| **SubPropertyOf** | cidoc:P1_is_identified_by |
| **Domain** | cidoc:E1_CRM_Entity |
| **Range** | cidoc:E62_String |
| **Created** | 2025-10-16 |
| **Modified** | 2025-10-17 |
| **Implicit Type** | aat:300404650 |

### Namespace Declarations

Required namespace prefixes:

```turtle
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix aat: <http://vocab.getty.edu/page/aat/> .
```

---

## Transformation Details

### Transformation Algorithm

The transformation process follows these steps:

1. **Detection:** Identify `gmn:P1_1_has_name` in JSON-LD data
2. **Extraction:** Extract name value(s) from property
3. **URI Generation:** Create unique URI for appellation resource
4. **Appellation Creation:** Build E41_Appellation with AAT type
5. **Property Linking:** Connect entity to appellation via P1_is_identified_by
6. **Cleanup:** Remove shortcut property from output

### Python Implementation

```python
def transform_p1_1_has_name(data):
    """Transform gmn:P1_1_has_name to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_1_has_name', AAT_NAME)

def transform_name_property(data, property_name, aat_type_uri):
    """Generic function to transform name shortcut properties."""
    if property_name not in data:
        return data
    
    names = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P1_is_identified_by' not in data:
        data['cidoc:P1_is_identified_by'] = []
    
    for name_obj in names:
        if isinstance(name_obj, dict):
            name_value = name_obj.get('@value', '')
        else:
            name_value = str(name_obj)
        
        if not name_value:
            continue
        
        appellation_uri = generate_appellation_uri(subject_uri, name_value, property_name)
        
        appellation = {
            '@id': appellation_uri,
            '@type': 'cidoc:E41_Appellation',
            'cidoc:P2_has_type': {
                '@id': aat_type_uri,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P190_has_symbolic_content': name_value
        }
        
        data['cidoc:P1_is_identified_by'].append(appellation)
    
    del data[property_name]
    return data
```

### URI Generation Strategy

Appellation URIs are generated using a hash-based approach:

```python
def generate_appellation_uri(subject_uri, name_value, suffix=""):
    """Generate a unique URI for an appellation resource."""
    name_hash = str(hash(name_value + suffix))[-8:]
    return f"{subject_uri}/appellation/{name_hash}"
```

**Pattern:** `{entity_uri}/appellation/{8-digit-hash}`

**Example:** 
- Entity: `http://example.org/persons/p001`
- Name: "Giovanni Spinola"
- Result: `http://example.org/persons/p001/appellation/a1b2c3d4`

### Transformation Guarantees

The transformation ensures:

- ✅ **Uniqueness:** Each name gets a unique appellation URI
- ✅ **Consistency:** Same name on same entity produces same URI
- ✅ **Validity:** All URIs follow URI specification
- ✅ **Completeness:** All required CIDOC-CRM elements present
- ✅ **Type Safety:** Correct data types for all properties

---

## Usage Examples

### Example 1: Person Name

**Input (JSON-LD):**
```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://gmn.org/persons/spinola_giacomo_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [
    {"@value": "Giacomo Spinola"}
  ]
}
```

**Output (Transformed):**
```json
{
  "@id": "http://gmn.org/persons/spinola_giacomo_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://gmn.org/persons/spinola_giacomo_001/appellation/f89a7b3c",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Giacomo Spinola"
    }
  ]
}
```

### Example 2: Place Name

**Input (Turtle):**
```turtle
<http://gmn.org/places/genoa> 
    a cidoc:E53_Place ;
    gmn:P1_1_has_name "Genoa" .
```

**Output (Transformed):**
```turtle
<http://gmn.org/places/genoa> 
    a cidoc:E53_Place ;
    cidoc:P1_is_identified_by <http://gmn.org/places/genoa/appellation/d45e9012> .

<http://gmn.org/places/genoa/appellation/d45e9012>
    a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Genoa" .

<http://vocab.getty.edu/aat/300404650> a cidoc:E55_Type .
```

### Example 3: Contract Name

**Input:**
```json
{
  "@id": "http://gmn.org/contracts/asl1450_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P1_1_has_name": [
    {"@value": "Sale of Building in Via San Lorenzo"}
  ]
}
```

**Output:**
```json
{
  "@id": "http://gmn.org/contracts/asl1450_001",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://gmn.org/contracts/asl1450_001/appellation/c7892de4",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Sale of Building in Via San Lorenzo"
    }
  ]
}
```

### Example 4: Multiple Names

**Input:**
```json
{
  "@id": "http://gmn.org/persons/doria_antonio_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [
    {"@value": "Antonio Doria"},
    {"@value": "Antonius de Auria"}
  ]
}
```

**Output:**
```json
{
  "@id": "http://gmn.org/persons/doria_antonio_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://gmn.org/persons/doria_antonio_001/appellation/b1c2d3e4",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Antonio Doria"
    },
    {
      "@id": "http://gmn.org/persons/doria_antonio_001/appellation/f5g6h7i8",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Antonius de Auria"
    }
  ]
}
```

### Example 5: Building Name

**Input:**
```json
{
  "@id": "http://gmn.org/buildings/palazzo_spinola",
  "@type": "gmn:E22_1_Building",
  "gmn:P1_1_has_name": [
    {"@value": "Palazzo Spinola"}
  ]
}
```

**Output:**
```json
{
  "@id": "http://gmn.org/buildings/palazzo_spinola",
  "@type": "gmn:E22_1_Building",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://gmn.org/buildings/palazzo_spinola/appellation/x9y8z7w6",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Palazzo Spinola"
    }
  ]
}
```

---

## Relationship to Other Properties

### Related Name Properties in GMN Ontology

The GMN ontology includes several name-related properties, each with specific use cases:

| Property | AAT Type | Use Case | Example |
|----------|----------|----------|---------|
| **gmn:P1_1_has_name** | 300404650 (names) | General names | "Giovanni Spinola" |
| **gmn:P1_2_has_name_from_source** | 300456607 (names found in sources) | Historical source names | "Johaninus Spinula" |
| **gmn:P1_3_has_patrilineal_name** | 300404651 (patronymics) | Patronymic names | "Giacomo Spinola q. Antonio" |
| **gmn:P1_4_has_loconym** | Q17143070 (loconym) | Place-based names | "Giacomo of Genoa" |
| **gmn:P102_1_has_title** | - | Document titles | "Instrumentum venditionis" |

### Property Hierarchy

```
cidoc:P1_is_identified_by (superclass)
    ├─> gmn:P1_1_has_name
    ├─> gmn:P1_2_has_name_from_source
    ├─> gmn:P1_3_has_patrilineal_name
    └─> gmn:P1_4_has_loconym

cidoc:P102_has_title (separate hierarchy)
    └─> gmn:P102_1_has_title
```

### Selection Guide

**Use P1_1_has_name when:**
- Providing a general, modern name for cataloging
- Name doesn't fit specialized categories
- Creating a display name for UI
- Name type is simply "name" without further specification

**Use P1_2_has_name_from_source when:**
- Name appears exactly as written in historical source
- Preserving historical spelling variations
- Documenting source-level name data

**Use P1_3_has_patrilineal_name when:**
- Name includes patronymic elements (q., son of, etc.)
- Documenting family lineage in naming
- Medieval/early modern naming patterns

**Use P1_4_has_loconym when:**
- Name indicates geographic origin
- Pattern like "X of Y" or "X from Z"
- Place-based identification is key

**Use P102_1_has_title when:**
- Naming a document or work
- Formal title from the document itself
- Title vs. name distinction matters

### Combining Properties

Multiple name properties can be used together on the same entity:

```json
{
  "@id": "http://gmn.org/persons/spinola_giacomo_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [{"@value": "Giacomo Spinola"}],
  "gmn:P1_2_has_name_from_source": [{"@value": "Jacobus Spinula"}],
  "gmn:P1_3_has_patrilineal_name": [{"@value": "Giacomo Spinola q. Antonio"}]
}
```

This creates three separate appellations with different types, providing multiple perspectives on the person's identification.

---

## AAT Integration

### Getty AAT Concept

The property uses Getty Art & Architecture Thesaurus (AAT) concept:

**AAT 300404650: names**
- **URI:** http://vocab.getty.edu/aat/300404650
- **Preferred Label:** names
- **Definition:** Words or phrases by which an entity is known
- **Broader Concept:** designations (300404639)
- **Hierarchy:** Objects Facet > Information forms > information > information forms > designations > names

### AAT in Transformation

When the property is transformed, the AAT concept becomes the type of the appellation:

```turtle
<appellation_uri> 
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300404650> .

<http://vocab.getty.edu/aat/300404650> 
    a cidoc:E55_Type .
```

### Benefits of AAT Integration

1. **Standardization:** Uses internationally recognized vocabulary
2. **Interoperability:** Enables data exchange with other AAT-using systems
3. **Semantic Clarity:** Clear definition of what constitutes a "name"
4. **Linked Data:** AAT URIs are dereferenceable for more information
5. **Query Support:** Can query by name type using standardized URI

### Alternative AAT Concepts

For reference, related AAT concepts used in other GMN properties:

| AAT URI | Concept | Used In |
|---------|---------|---------|
| 300404650 | names | P1_1_has_name |
| 300456607 | names found in historical sources | P1_2_has_name_from_source |
| 300404651 | patronymics | P1_3_has_patrilineal_name |

---

## Best Practices

### Data Entry

**✅ DO:**
- Use for general, modern names assigned for cataloging
- Keep names consistent within your dataset
- Use simple, clear language
- Include variant forms as separate values if needed
- Document naming conventions in your project guidelines

**❌ DON'T:**
- Use for specialized name types (source names, patronymics, etc.)
- Include extra metadata in the name string (dates, notes, etc.)
- Mix different languages in same name value
- Use abbreviations unless they're part of the standard name
- Include formatting markup or special characters unnecessarily

### Name Formatting

**Recommended Formats:**

**Persons:**
- Given name + Family name: "Giovanni Spinola"
- Family name, Given name: "Spinola, Giovanni"
- Choose one format and be consistent

**Places:**
- Modern standard name: "Genoa"
- Include country if ambiguous: "Genoa, Italy"
- Use English or original language consistently

**Buildings:**
- Include type if relevant: "Palazzo Spinola"
- Location can help: "House on Via San Lorenzo"

**Contracts:**
- Descriptive cataloging name: "Sale of Building in Via San Lorenzo"
- Include key identifying info: "Marriage Contract between Spinola and Doria families, 1450"

### Quality Control

**Validation Checks:**
1. No empty strings
2. No extra whitespace at start/end
3. Consistent capitalization
4. No typos or misspellings
5. Appropriate level of detail

**Example Quality Issues:**

❌ Bad:
```json
"gmn:P1_1_has_name": [{"@value": "  Giovanni  Spinola   "}]  // Extra whitespace
"gmn:P1_1_has_name": [{"@value": ""}]  // Empty value
"gmn:P1_1_has_name": [{"@value": "giovanni spinola"}]  // Inconsistent caps
```

✅ Good:
```json
"gmn:P1_1_has_name": [{"@value": "Giovanni Spinola"}]
```

### Documentation Standards

When documenting use of this property:

1. **Explain Context:** Why this name was chosen
2. **Note Sources:** Where the name comes from (if known)
3. **Flag Uncertainty:** Use editorial notes for doubtful attributions
4. **Link Variants:** Connect to other name forms if available
5. **Cite Authority:** Reference authority files (VIAF, LCNAF, etc.) if applicable

---

## SPARQL Query Examples

### Query 1: Find All Named Entities

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

SELECT ?entity ?name
WHERE {
  ?entity cidoc:P1_is_identified_by ?appellation .
  ?appellation a cidoc:E41_Appellation ;
               cidoc:P2_has_type aat:300404650 ;
               cidoc:P190_has_symbolic_content ?name .
}
```

### Query 2: Find Persons by Name

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

SELECT ?person ?name
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by ?appellation .
  ?appellation cidoc:P2_has_type aat:300404650 ;
               cidoc:P190_has_symbolic_content ?name .
  FILTER(CONTAINS(LCASE(?name), "spinola"))
}
```

### Query 3: Find All Names for a Specific Entity

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

SELECT ?name
WHERE {
  <http://gmn.org/persons/spinola_giacomo_001> 
    cidoc:P1_is_identified_by ?appellation .
  ?appellation cidoc:P2_has_type aat:300404650 ;
               cidoc:P190_has_symbolic_content ?name .
}
```

### Query 4: Count Entities by Name Type

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

SELECT ?type (COUNT(DISTINCT ?entity) AS ?count)
WHERE {
  ?entity a ?type ;
          cidoc:P1_is_identified_by ?appellation .
  ?appellation cidoc:P2_has_type aat:300404650 .
}
GROUP BY ?type
ORDER BY DESC(?count)
```

### Query 5: Find Entities with Multiple Names

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

SELECT ?entity (COUNT(?appellation) AS ?nameCount)
WHERE {
  ?entity cidoc:P1_is_identified_by ?appellation .
  ?appellation cidoc:P2_has_type aat:300404650 .
}
GROUP BY ?entity
HAVING (COUNT(?appellation) > 1)
ORDER BY DESC(?nameCount)
```

### Query 6: Find All Contracts with Names

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

SELECT ?contract ?name ?contractType
WHERE {
  ?contract a ?contractType ;
            cidoc:P1_is_identified_by ?appellation .
  ?appellation cidoc:P2_has_type aat:300404650 ;
               cidoc:P190_has_symbolic_content ?name .
  FILTER(STRSTARTS(STR(?contractType), "http://www.genoesemerchantnetworks.com/ontology#E31"))
}
ORDER BY ?name
```

---

## Validation Rules

### Required Elements

After transformation, each name must have:
- ✅ Valid appellation URI
- ✅ Type declaration (cidoc:E41_Appellation)
- ✅ P2_has_type pointing to AAT 300404650
- ✅ P190_has_symbolic_content with string value
- ✅ Connection from entity via P1_is_identified_by

### Validation SPARQL Query

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

# Find appellations missing required elements
SELECT ?appellation ?issue
WHERE {
  ?entity cidoc:P1_is_identified_by ?appellation .
  ?appellation cidoc:P2_has_type aat:300404650 .
  
  OPTIONAL { ?appellation a ?type }
  OPTIONAL { ?appellation cidoc:P190_has_symbolic_content ?content }
  
  BIND(
    IF(!BOUND(?type), "Missing type declaration",
    IF(!BOUND(?content), "Missing symbolic content",
    "Valid")) AS ?issue
  )
  
  FILTER(?issue != "Valid")
}
```

---

## Error Handling

### Common Transformation Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Property not removed | Function not called | Add to TRANSFORMERS list |
| Invalid URI | Special characters in name | Sanitize input or use hash-only URIs |
| Missing AAT type | Wrong constant used | Verify AAT_NAME value |
| Duplicate appellations | Same name entered twice | Check for duplicates before adding |
| Empty names | Data quality issue | Filter out empty values in transform |

### Defensive Programming

The transformation code includes safeguards:

```python
# Check if property exists before transforming
if property_name not in data:
    return data

# Handle empty name values
if not name_value:
    continue

# Provide fallback URI if @id missing
subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
```

---

## Conclusion

The `gmn:P1_1_has_name` property provides a powerful, flexible, and CIDOC-CRM-compliant way to assign names to any entity in your GMN database. By understanding its semantic basis, transformation process, and relationship to other properties, you can effectively use it to create well-structured, interoperable cultural heritage data.

For implementation details, see `has-name-implementation-guide.md`.  
For code snippets, see `has-name-ontology.ttl` and `has-name-transform.py`.  
For documentation examples, see `has-name-doc-note.txt`.

---

**Version:** 1.0  
**Last Updated:** October 26, 2025  
**Status:** Active and Production-Ready
