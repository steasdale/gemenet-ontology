# gmn:P1_4_has_loconym - Ontology Documentation

**Property URI:** `http://example.org/gmn/P1_4_has_loconym`  
**Property Label:** P1.4 has loconym  
**Property Type:** Object Property  
**Created:** 2025-10-16

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Semantic Specification](#semantic-specification)
3. [CIDOC-CRM Alignment](#cidoc-crm-alignment)
4. [Transformation Specification](#transformation-specification)
5. [Usage Examples](#usage-examples)
6. [Integration Patterns](#integration-patterns)
7. [Query Examples](#query-examples)
8. [Historical Context](#historical-context)

---

## Property Overview

### Definition

The `gmn:P1_4_has_loconym` property expresses a place referenced in a person's name (a loconym), indicating that the person or their ancestors originated from that place. This property captures toponymic naming patterns common in medieval Italian contexts.

### Purpose

This property serves as a **simplified shortcut** for the full CIDOC-CRM path that represents the semantic relationship between a person and a place referenced in their name. It provides:

1. **Simplified Data Entry** - Direct person-to-place link for easier data modeling
2. **Semantic Clarity** - Explicit representation of toponymic name components
3. **Geographic Analysis** - Enables place-based queries about person origins
4. **CIDOC-CRM Compliance** - Transforms to standard CIDOC-CRM structure

### Key Characteristics

| Characteristic | Value |
|----------------|-------|
| **Property Type** | Object Property (owl:ObjectProperty) |
| **Domain** | cidoc:E21_Person |
| **Range** | cidoc:E53_Place |
| **Cardinality** | 0..* (zero or more) |
| **Supertype** | cidoc:P1_is_identified_by |
| **Implicit Type** | Wikidata Q17143070 (loconym) |

### Scope and Applicability

**In Scope:**
- Place names embedded in person names (da Genova, de Vignolo)
- Toponymic components indicating geographic origin
- Ancestral place references in naming patterns
- Medieval Italian naming conventions

**Out of Scope:**
- Current residence or address (use location properties)
- Places mentioned in documents (use P70.13)
- Document creation locations (use P94i.3)
- Regional group membership (use P107i.1)

---

## Semantic Specification

### RDF/OWL Declaration

```turtle
@prefix gmn: <http://example.org/gmn/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

# Property: P1.4 has loconym
gmn:P1_4_has_loconym
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P1.4 has loconym"@en ;
    rdfs:comment """Simplified property for expressing a place referenced in a 
        person's name (loconym), indicating that the person or their ancestors 
        originated from that place. Represents the full CIDOC-CRM path: 
        P1_is_identified_by > E41_Appellation > P2_has_type 
        <https://www.wikidata.org/wiki/Q17143070> > P67_refers_to > E53_Place. 
        This captures toponymic naming patterns common in medieval Italian 
        contexts (e.g., 'Giovanni da Genova', 'Bartolomeo de Vignolo'). This 
        property is provided as a convenience for data entry and should be 
        transformed to the full CIDOC-CRM structure for formal compliance. The 
        appellation type is automatically set to Wikidata Q17143070 (loconym)."""@en ;
    rdfs:subPropertyOf cidoc:P1_is_identified_by ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E53_Place ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P1_is_identified_by, 
                 cidoc:P67_refers_to, 
                 <https://www.wikidata.org/wiki/Q17143070> ;
    gmn:hasImplicitType <https://www.wikidata.org/wiki/Q17143070> .
```

### Domain: cidoc:E21_Person

The property applies to instances of `cidoc:E21_Person` and its subclasses.

**Valid Subjects:**
```turtle
<person_giovanni> a cidoc:E21_Person .
<person_maria> a cidoc:E21_Person .
<notary_bartolomeo> a cidoc:E21_Person .  # Also valid (subclass)
```

**Invalid Subjects:**
```turtle
<contract_001> a cidoc:E31_Document .     # Wrong class
<building_palazzo> a cidoc:E22_Human-Made_Object .  # Wrong class
```

### Range: cidoc:E53_Place

The property must reference instances of `cidoc:E53_Place` and its subclasses.

**Valid Objects:**
```turtle
<place_genoa> a cidoc:E53_Place ;
    rdfs:label "Genoa"@en .

<place_vignolo> a cidoc:E53_Place ;
    rdfs:label "Vignolo"@it .
```

**Invalid Objects:**
```turtle
"Genoa"  # Literal string, not place resource
<person_antonio>  # Wrong class
```

### Supertype Relationship

`gmn:P1_4_has_loconym` is a subproperty of `cidoc:P1_is_identified_by`:

```turtle
gmn:P1_4_has_loconym rdfs:subPropertyOf cidoc:P1_is_identified_by .
```

This means:
- All loconym relationships are also identification relationships
- Reasoners will infer P1_is_identified_by from P1_4_has_loconym
- The property participates in the CIDOC-CRM identification framework

---

## CIDOC-CRM Alignment

### Full CIDOC-CRM Path

The simplified property represents this complete CIDOC-CRM structure:

```
E21_Person 
  → P1_is_identified_by 
    → E41_Appellation 
      → P2_has_type 
        → E55_Type <https://www.wikidata.org/wiki/Q17143070>
      → P67_refers_to 
        → E53_Place
```

### Path Components

| Component | Class/Property | Description |
|-----------|----------------|-------------|
| **Subject** | E21_Person | The person being identified |
| **P1** | P1_is_identified_by | Links person to appellation |
| **Appellation** | E41_Appellation | The name/appellation resource |
| **P2** | P2_has_type | Specifies appellation type |
| **Type** | E55_Type | Loconym type (Wikidata Q17143070) |
| **P67** | P67_refers_to | Links appellation to place |
| **Place** | E53_Place | The place referenced in the name |

### Comparison with Related Paths

#### Path 1: Standard Name (gmn:P1_1_has_name)
```
E21_Person 
  → P1_is_identified_by 
    → E41_Appellation 
      → P2_has_type → AAT:300404650 (names)
      → P190_has_symbolic_content → Literal string
```

#### Path 2: Loconym (gmn:P1_4_has_loconym)
```
E21_Person 
  → P1_is_identified_by 
    → E41_Appellation 
      → P2_has_type → Wikidata:Q17143070 (loconyms)
      → P67_refers_to → E53_Place
```

**Key Difference:** Loconym appellations use `P67_refers_to` to link to place resources, while standard names use `P190_has_symbolic_content` for string values.

### Wikidata Integration

The property uses **Wikidata Q17143070** as the appellation type:

```turtle
<https://www.wikidata.org/wiki/Q17143070> a cidoc:E55_Type ;
    rdfs:label "loconym"@en ;
    rdfs:comment "a toponymic name component indicating geographic origin"@en .
```

**Why Wikidata Instead of Getty AAT?**
- Getty AAT lacks a specific term for "loconym"
- Wikidata Q17143070 provides precise semantic alignment
- Maintains interoperability with Wikidata knowledge graph
- Supports multilingual labels and descriptions

---

## Transformation Specification

### Transformation Algorithm

```python
def transform_p1_4_has_loconym(data):
    """
    Transform gmn:P1_4_has_loconym to full CIDOC-CRM structure.
    
    Input: Person resource with gmn:P1_4_has_loconym property
    Output: Person resource with cidoc:P1_is_identified_by array
    
    Algorithm:
    1. Check for property existence
    2. Extract place URI(s)
    3. For each place:
       a. Generate unique appellation URI
       b. Create E41_Appellation structure
       c. Set type to Wikidata Q17143070
       d. Add P67_refers_to pointing to place
       e. Append to P1_is_identified_by array
    4. Remove shortcut property
    5. Return modified data
    """
    
    # 1. Check for property
    if 'gmn:P1_4_has_loconym' not in data:
        return data
    
    # 2. Extract places
    places = data['gmn:P1_4_has_loconym']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize array if needed
    if 'cidoc:P1_is_identified_by' not in data:
        data['cidoc:P1_is_identified_by'] = []
    
    # 3. Process each place
    for place_obj in places:
        # Extract place URI (handle both object and string format)
        if isinstance(place_obj, dict):
            place_uri = place_obj.get('@id', '')
        else:
            place_uri = str(place_obj)
        
        # 3a. Generate unique URI
        place_hash = str(hash(place_uri))[-8:]
        appellation_uri = f"{subject_uri}/appellation/loconym_{place_hash}"
        
        # 3b-3d. Create appellation structure
        appellation = {
            '@id': appellation_uri,
            '@type': 'cidoc:E41_Appellation',
            'cidoc:P2_has_type': {
                '@id': 'https://www.wikidata.org/wiki/Q17143070',
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P67_refers_to': {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        }
        
        # 3e. Add to array
        data['cidoc:P1_is_identified_by'].append(appellation)
    
    # 4. Remove shortcut
    del data['gmn:P1_4_has_loconym']
    
    # 5. Return
    return data
```

### URI Generation

Appellation URIs are generated using the hash function:

```python
place_hash = str(hash(place_uri))[-8:]
appellation_uri = f"{subject_uri}/appellation/loconym_{place_hash}"
```

**Example:**
- Person URI: `http://example.org/person/giovanni_001`
- Place URI: `http://example.org/place/genoa`
- Hash of place URI: `-1234567890` → last 8 digits: `67890`
- Appellation URI: `http://example.org/person/giovanni_001/appellation/loconym_67890`

**Properties:**
- Deterministic: Same place always generates same URI
- Unique: Different places generate different URIs
- Namespaced: URI is under person resource
- Readable: Contains "loconym" identifier

### Transformation Guarantees

The transformation function guarantees:

1. **Idempotence** - Running transformation multiple times produces same result
2. **Data Preservation** - All original data preserved, only structure changed
3. **Type Safety** - All generated resources properly typed
4. **URI Uniqueness** - No URI collisions for different places
5. **CIDOC-CRM Compliance** - Output conforms to CIDOC-CRM specification

---

## Usage Examples

### Example 1: Single Loconym

**Input (Simplified):**
```turtle
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix gmn: <http://example.org/gmn/> .

<person_giovanni> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giovanni da Genova" ;
    gmn:P1_4_has_loconym <place_genoa> .

<place_genoa> a cidoc:E53_Place ;
    rdfs:label "Genoa"@en ;
    rdfs:label "Genova"@it .
```

**Output (CIDOC-CRM Compliant):**
```turtle
<person_giovanni> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <person_giovanni/appellation/12345678> ,
                               <person_giovanni/appellation/loconym_87654321> .

<person_giovanni/appellation/12345678> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Giovanni da Genova" .

<person_giovanni/appellation/loconym_87654321> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <https://www.wikidata.org/wiki/Q17143070> ;
    cidoc:P67_refers_to <place_genoa> .

<place_genoa> a cidoc:E53_Place ;
    rdfs:label "Genoa"@en ;
    rdfs:label "Genova"@it .
```

### Example 2: Multiple Loconyms

**Input:**
```turtle
<person_maria> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Maria da Venezia e Genova" ;
    gmn:P1_4_has_loconym <place_venice> , <place_genoa> .
```

**Output:**
```turtle
<person_maria> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <person_maria/appellation/name> ,
                               <person_maria/appellation/loconym_venice_hash> ,
                               <person_maria/appellation/loconym_genoa_hash> .

<person_maria/appellation/name> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Maria da Venezia e Genova" .

<person_maria/appellation/loconym_venice_hash> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <https://www.wikidata.org/wiki/Q17143070> ;
    cidoc:P67_refers_to <place_venice> .

<person_maria/appellation/loconym_genoa_hash> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <https://www.wikidata.org/wiki/Q17143070> ;
    cidoc:P67_refers_to <place_genoa> .
```

### Example 3: Combined with Other Name Properties

**Input:**
```turtle
<person_bartolomeo> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Bartolomeo de Vignolo" ;
    gmn:P1_2_has_name_from_source "Bartholomeus de Vignolo" ;
    gmn:P1_3_has_patrilineal_name "Bartolomeo q. Antonio" ;
    gmn:P1_4_has_loconym <place_vignolo> .
```

**Output:**
```turtle
<person_bartolomeo> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by 
        <person_bartolomeo/appellation/name> ,
        <person_bartolomeo/appellation/source_name> ,
        <person_bartolomeo/appellation/patronymic> ,
        <person_bartolomeo/appellation/loconym> .

<person_bartolomeo/appellation/name> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Bartolomeo de Vignolo" .

<person_bartolomeo/appellation/source_name> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Bartholomeus de Vignolo" .

<person_bartolomeo/appellation/patronymic> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404651> ;
    cidoc:P190_has_symbolic_content "Bartolomeo q. Antonio" .

<person_bartolomeo/appellation/loconym> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <https://www.wikidata.org/wiki/Q17143070> ;
    cidoc:P67_refers_to <place_vignolo> .
```

### Example 4: JSON-LD Format

**Input:**
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/"
  },
  "@id": "http://example.org/person/merchant_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Giacomo da Savona",
  "gmn:P1_4_has_loconym": {
    "@id": "http://example.org/place/savona"
  }
}
```

**Output:**
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/person/merchant_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://example.org/person/merchant_001/appellation/name_hash",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Giacomo da Savona"
    },
    {
      "@id": "http://example.org/person/merchant_001/appellation/loconym_savona_hash",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "https://www.wikidata.org/wiki/Q17143070",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P67_refers_to": {
        "@id": "http://example.org/place/savona",
        "@type": "cidoc:E53_Place"
      }
    }
  ]
}
```

---

## Integration Patterns

### Pattern 1: Person with Complete Biographical Data

```turtle
<person_complete> a cidoc:E21_Person ;
    # Name properties
    gmn:P1_1_has_name "Giovanni da Genova" ;
    gmn:P1_2_has_name_from_source "Iohannes de Ianua" ;
    gmn:P1_4_has_loconym <place_genoa> ;
    
    # Biographical properties
    gmn:P2_1_gender aat:300189559 ;  # male
    gmn:P97_1_has_father <person_antonio> ;
    gmn:P107i_1_has_regional_provenance <group_ligurian> ;
    gmn:P107i_3_has_occupation <group_merchants> ;
    
    # Administrative
    gmn:P3_1_has_editorial_note "Prominent merchant family from Genoa" .
```

### Pattern 2: Place Resource with Geographic Details

```turtle
<place_vignolo> a cidoc:E53_Place ;
    rdfs:label "Vignole Borbera"@it ;
    rdfs:label "Vignolo"@it ;  # Medieval short form
    rdfs:label "Vignole"@en ;
    
    cidoc:P89_falls_within <place_piedmont> ;
    cidoc:P168_place_is_defined_by <coordinates_vignolo> ;
    
    owl:sameAs <http://www.geonames.org/3164092> ;
    owl:sameAs <http://vocab.getty.edu/tgn/7011234> ;
    
    cidoc:P3_has_note """Small town in Piedmont region, part of the 
        Tortona diocese in medieval period. Common origin for merchant 
        families trading in Genoa."""@en .
```

### Pattern 3: Loconym with Regional Provenance

```turtle
<person_merchant> a cidoc:E21_Person ;
    gmn:P1_4_has_loconym <place_genoa> ;
    gmn:P107i_1_has_regional_provenance <group_genoese_merchants> .

<group_genoese_merchants> a gmn:E74_1_Regional_Provenance ;
    cidoc:P2_has_type aat:300055490 ;  # regions (geographic)
    rdfs:label "Genoese Merchants"@en ;
    cidoc:P74_has_current_or_former_residence <place_genoa> .
```

**Distinction:**
- `P1_4_has_loconym`: Place component in the **person's name**
- `P107i_1_has_regional_provenance`: Person's membership in a **regional group**

### Pattern 4: Document Referencing Person with Loconym

```turtle
<contract_001> a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller <person_giovanni_da_genova> ;
    gmn:P94i_3_has_place_of_enactment <place_genoa> .

<person_giovanni_da_genova> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giovanni da Genova" ;
    gmn:P1_4_has_loconym <place_genoa> .
```

**Note:** The loconym (`P1_4`) refers to origin/name, while `P94i_3` refers to document creation place.

---

## Query Examples

### SPARQL Queries

#### Query 1: Find All People from Genoa

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://example.org/gmn/>

SELECT ?person ?name WHERE {
  ?person a cidoc:E21_Person ;
          gmn:P1_4_has_loconym <http://example.org/place/genoa> ;
          gmn:P1_1_has_name ?name .
}
```

#### Query 2: List All Places Referenced in Loconyms

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://example.org/gmn/>

SELECT DISTINCT ?place ?label WHERE {
  ?person gmn:P1_4_has_loconym ?place .
  ?place rdfs:label ?label .
}
ORDER BY ?label
```

#### Query 3: Count People by Origin Place

```sparql
PREFIX gmn: <http://example.org/gmn/>

SELECT ?place (COUNT(?person) as ?count) WHERE {
  ?person gmn:P1_4_has_loconym ?place .
}
GROUP BY ?place
ORDER BY DESC(?count)
```

#### Query 4: Find People with Both Loconym and Regional Group

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://example.org/gmn/>

SELECT ?person ?name ?place ?group WHERE {
  ?person a cidoc:E21_Person ;
          gmn:P1_1_has_name ?name ;
          gmn:P1_4_has_loconym ?place ;
          gmn:P107i_1_has_regional_provenance ?group .
}
```

#### Query 5: Find Transformed Loconym Appellations

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?person ?appellation ?place WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by ?appellation .
  
  ?appellation a cidoc:E41_Appellation ;
               cidoc:P2_has_type <https://www.wikidata.org/wiki/Q17143070> ;
               cidoc:P67_refers_to ?place .
}
```

#### Query 6: Geographic Network Analysis

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://example.org/gmn/>

SELECT ?place1 ?place2 (COUNT(*) as ?connections) WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            gmn:P70_1_documents_seller ?seller ;
            gmn:P70_2_documents_buyer ?buyer .
  
  ?seller gmn:P1_4_has_loconym ?place1 .
  ?buyer gmn:P1_4_has_loconym ?place2 .
  
  FILTER (?place1 != ?place2)
}
GROUP BY ?place1 ?place2
ORDER BY DESC(?connections)
```

---

## Historical Context

### Medieval Italian Naming Conventions

In medieval and Renaissance Italy, particularly in Genoa and surrounding regions, loconyms were a common component of personal names. These toponymic elements served several functions:

1. **Origin Identification** - Distinguished persons from different places
2. **Family Prestige** - Connected individuals to significant locations
3. **Social Networks** - Indicated regional affiliations and trade connections
4. **Legal Documentation** - Provided precise identification in contracts

### Common Patterns

#### Pattern A: "da" + Place Name
```
Giovanni da Genova = Giovanni from Genoa
Antonio da Savona = Antonio from Savona
Maria da Venezia = Maria from Venice
```

#### Pattern B: "de" + Place Name (Latin influenced)
```
Bartholomeus de Vignolo = Bartolomeo from Vignolo
Iacobus de Ianua = Giacomo from Genoa
Francesca de Rapallo = Francesca from Rapallo
```

#### Pattern C: Adjective Form
```
Giovanni Genovese = Giovanni the Genoese
Antonio Savonese = Antonio from Savona
```

### Temporal Considerations

- **12th-14th centuries:** Loconyms increasingly common in notarial records
- **15th century:** Height of usage in Genoa and major trading cities
- **16th century onward:** Gradual stabilization into family surnames

### Geographic Distribution

Primary usage regions:
- **Liguria** (Genoa, Savona, Rapallo)
- **Piedmont** (Vignole, Tortona, Alessandria)
- **Lombardy** (Milan, Pavia)
- **Veneto** (Venice, Padua)

---

## Summary

### Key Points

1. **Purpose:** Links persons to places referenced in their names
2. **Type:** Object property (person → place)
3. **CIDOC-CRM:** Transforms to E41_Appellation with P67_refers_to
4. **Type System:** Uses Wikidata Q17143070 for loconym type
5. **Cardinality:** Zero or more (multiple loconyms possible)

### When to Use

✅ Place name component in person's formal identification  
✅ Toponymic naming patterns (da Genova, de Vignolo)  
✅ Geographic origin indicated in name  
✅ Medieval Italian naming conventions

### When NOT to Use

❌ Current residence or address  
❌ Places mentioned in document content  
❌ Document creation locations  
❌ Regional group membership (not name-based)

### Related Properties

- `gmn:P1_1_has_name` - Display name
- `gmn:P1_2_has_name_from_source` - Historical source name
- `gmn:P1_3_has_patrilineal_name` - Patronymic ancestry
- `gmn:P107i_1_has_regional_provenance` - Regional group
- `gmn:P94i_3_has_place_of_enactment` - Document creation place

---

**End of Documentation**
