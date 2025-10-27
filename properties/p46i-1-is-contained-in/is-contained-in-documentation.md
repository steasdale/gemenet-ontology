# P46i.1 Is Contained In: Ontology Documentation
## Complete Semantic Documentation for GMN Ontology

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Semantic Specification](#semantic-specification)
3. [CIDOC-CRM Alignment](#cidoc-crm-alignment)
4. [Usage Guidelines](#usage-guidelines)
5. [Transformation Patterns](#transformation-patterns)
6. [Examples](#examples)
7. [Integration with Other Properties](#integration-with-other-properties)
8. [Best Practices](#best-practices)
9. [SPARQL Query Patterns](#sparql-query-patterns)

---

## Property Overview

### Basic Information

| Attribute | Value |
|-----------|-------|
| **URI** | `gmn:P46i_1_is_contained_in` |
| **Label** | "P46i.1 is contained in" (English) |
| **Domain** | `cidoc:E31_Document` |
| **Range** | `cidoc:E78_Curated_Holding` |
| **Superproperty** | `cidoc:P46i_forms_part_of` |
| **Inverse Property** | `cidoc:P46_is_composed_of` |
| **Quantification** | Many to many (0,n:0,n) |
| **Created** | 2025-10-17 |

### Definition

**Simplified property for expressing that a document forms part of a larger archival unit or collection.** Use this to link individual contracts to the registers, filze (bundles of contracts tied with string), folders, or other archival containers in which they are physically housed. This represents the direct CIDOC-CRM property `P46i_forms_part_of`. The range can be any archival unit or collection, including registers (E31_Document subtype), filze, folders, or institutional archives. This captures the archival context and provenance of individual documents.

### Purpose in GMN Ontology

This property serves to:

1. **Preserve Archival Context**: Maintain the relationship between documents and their archival containers
2. **Support Provenance Research**: Enable tracking of documentary origins and organizational structures
3. **Facilitate Collection Navigation**: Allow users to understand document organization
4. **Enable Hierarchical Queries**: Support queries traversing archival hierarchies

---

## Semantic Specification

### RDF/OWL Definition

```turtle
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

gmn:P46i_1_is_contained_in
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P46i.1 is contained in"@en ;
    rdfs:comment "Simplified property for expressing that a document forms part of a larger archival unit or collection. Use this to link individual contracts to the registers, filze (bundles of contracts tied with string), folders, or other archival containers in which they are physically housed. This represents the direct CIDOC-CRM property P46i_forms_part_of. The range can be any archival unit or collection, including registers (E31_Document subtype), filze, folders, or institutional archives. This captures the archival context and provenance of individual documents."@en ;
    rdfs:subPropertyOf cidoc:P46i_forms_part_of ;
    rdfs:domain cidoc:E31_Document ;
    rdfs:range cidoc:E78_Curated_Holding ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P46i_forms_part_of .
```

### Domain and Range Analysis

#### Domain: `cidoc:E31_Document`

Documents that can use this property include:
- **Sales Contracts** (`gmn:E31_2_Sales_Contract`)
- **Correspondence** (`gmn:E31_6_Correspondence`)
- **Dowry Contracts** (`gmn:E31_8_Dowry_Contract`)
- **Arbitration Agreements** (`gmn:E31_3_Arbitration_Agreement`)
- **Donation Contracts** (`gmn:E31_7_Donation_Contract`)
- **Generic Documents** (`cidoc:E31_Document`)

Any subclass of E31_Document can use this property.

#### Range: `cidoc:E78_Curated_Holding`

Valid containers include:

- **Notarial Registers**: Books containing multiple contracts
  - Type: `cidoc:E31_Document` + `cidoc:E78_Curated_Holding`
  
- **Filze**: Bundles of contracts tied with string
  - Type: `cidoc:E78_Curated_Holding`
  
- **Folders**: Modern archival folders
  - Type: `cidoc:E78_Curated_Holding`
  
- **Institutional Archives**: Larger archival collections
  - Type: `cidoc:E78_Curated_Holding` or subclass

- **Buste**: Archival boxes or bundles
  - Type: `cidoc:E78_Curated_Holding`

---

## CIDOC-CRM Alignment

### Direct Mapping

This property is a **direct subproperty** of `cidoc:P46i_forms_part_of`. Unlike many GMN shortcut properties, this one does NOT require transformation through intermediate nodes. The transformation is a simple property substitution.

### CIDOC-CRM P46i_forms_part_of

**Definition**: "This property associates an instance of E18 Physical Thing with another instance of E18 Physical Thing that forms part of it."

**Key Points**:
- Both domain and range are E18_Physical_Thing in strict CIDOC-CRM
- E31_Document is a subclass of E18_Physical_Thing
- E78_Curated_Holding is a subclass of E18_Physical_Thing
- The property is transitive (if A is part of B, and B is part of C, then A is part of C)

### Inverse Relationship

The inverse property `cidoc:P46_is_composed_of` can be inferred:

```turtle
<register_1450> cidoc:P46_is_composed_of <contract_001> .
```

This is automatically derivable from:
```turtle
<contract_001> cidoc:P46i_forms_part_of <register_1450> .
```

### Transitivity

The property supports transitive queries:

```turtle
# Contract is part of filza
<contract_001> cidoc:P46i_forms_part_of <filza_23> .

# Filza is part of busta
<filza_23> cidoc:P46i_forms_part_of <busta_5> .

# Therefore, contract is (transitively) part of busta
# Can be inferred: <contract_001> cidoc:P46i_forms_part_of <busta_5> .
```

---

## Usage Guidelines

### When to Use This Property

✅ **USE** `gmn:P46i_1_is_contained_in` when:

1. **Physical Containment**: Document is physically housed within an archival unit
2. **Archival Organization**: Expressing the original archival structure
3. **Provenance Tracking**: Recording where documents come from
4. **Collection Context**: Linking documents to their parent collections

### When NOT to Use This Property

❌ **DO NOT USE** for:

1. **Current Physical Location**: Use `cidoc:P55_has_current_location` instead
   ```turtle
   <contract> cidoc:P55_has_current_location <archive_building> .
   ```

2. **Document Creation Location**: Use `gmn:P94i_3_has_place_of_enactment` instead
   ```turtle
   <contract> gmn:P94i_3_has_place_of_enactment <genoa> .
   ```

3. **Referenced Locations**: Use `cidoc:P67_refers_to` instead
   ```turtle
   <contract> cidoc:P67_refers_to <property_location> .
   ```

4. **Conceptual Relationships**: Use appropriate semantic properties
   ```turtle
   <contract> cidoc:P70_documents <acquisition> .
   ```

### Common Scenarios

#### Scenario 1: Contract in Register
```turtle
<contract_genoa_1450_123> 
    a gmn:E31_2_Sales_Contract ;
    gmn:P46i_1_is_contained_in <notarial_register_antonio_1450> .

<notarial_register_antonio_1450>
    a cidoc:E31_Document ;
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Notarial Register of Antonio Foglietta, 1450"@en .
```

#### Scenario 2: Multiple Containment Levels
```turtle
<contract_001> 
    gmn:P46i_1_is_contained_in <filza_23> .

<filza_23> 
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Filza 23"@it ;
    gmn:P46i_1_is_contained_in <busta_5> .

<busta_5>
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Busta 5, Archivio di Stato di Genova"@it ;
    cidoc:P55_has_current_location <archivio_stato_genova> .
```

#### Scenario 3: Letter in Letterbook
```turtle
<letter_1453_05_12_maria_to_giovanni>
    a gmn:E31_6_Correspondence ;
    gmn:P46i_1_is_contained_in <letterbook_maria_1453> .

<letterbook_maria_1453>
    a cidoc:E31_Document ;
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Letterbook of Maria Spinola, 1453"@en .
```

---

## Transformation Patterns

### Pattern: Direct Property Substitution

This property transformation is one of the simplest in the GMN ontology.

#### Input (GMN Shortcut)
```turtle
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .

<contract_001> a gmn:E31_2_Sales_Contract ;
    gmn:P46i_1_is_contained_in <register_1450> .
```

#### Output (CIDOC-CRM Compliant)
```turtle
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

<contract_001> a gmn:E31_2_Sales_Contract ;
    cidoc:P46i_forms_part_of <register_1450> .
```

#### Transformation Diagram

```
┌─────────────────────────────────────────────┐
│          GMN Shortcut Input                  │
├─────────────────────────────────────────────┤
│                                              │
│  <contract_001>                              │
│      gmn:P46i_1_is_contained_in              │
│          <register_1450>                     │
│                                              │
└─────────────────────────────────────────────┘
                    ↓
         [Direct Property Mapping]
                    ↓
┌─────────────────────────────────────────────┐
│       CIDOC-CRM Compliant Output             │
├─────────────────────────────────────────────┤
│                                              │
│  <contract_001>                              │
│      cidoc:P46i_forms_part_of                │
│          <register_1450>                     │
│                                              │
└─────────────────────────────────────────────┘
```

**No intermediate nodes created!** This is a simple property replacement.

### Comparison with Complex Properties

For context, here's how this differs from more complex GMN properties:

#### Complex Property Example (P94i.1)
```turtle
# Input
<contract> gmn:P94i_1_was_created_by <notary> .

# Output (creates intermediate E65_Creation)
<contract> cidoc:P94i_was_created_by <contract/creation> .
<contract/creation> a cidoc:E65_Creation ;
    cidoc:P14_carried_out_by <notary> .
```

#### Simple Property (P46i.1)
```turtle
# Input
<contract> gmn:P46i_1_is_contained_in <register> .

# Output (direct substitution only)
<contract> cidoc:P46i_forms_part_of <register> .
```

---

## Examples

### Example 1: Single Document in Register

**Scenario**: A sales contract housed in a notarial register.

**Input Data**:
```turtle
@prefix ex: <http://example.org/> .
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .

ex:contract_genoa_1450_07_15_house_sale
    a gmn:E31_2_Sales_Contract ;
    gmn:P1_1_has_name "House Sale Contract, July 15, 1450"@en ;
    gmn:P94i_2_has_enactment_date "1450-07-15"^^xsd:date ;
    gmn:P46i_1_is_contained_in ex:register_foglietta_1450 .

ex:register_foglietta_1450
    a cidoc:E31_Document ;
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Notarial Register of Antonio Foglietta, 1450"@en ;
    gmn:P94i_1_was_created_by ex:notary_antonio_foglietta .
```

**Transformed Output**:
```turtle
ex:contract_genoa_1450_07_15_house_sale
    a gmn:E31_2_Sales_Contract ;
    cidoc:P1_is_identified_by ex:contract_genoa_1450_07_15_house_sale/appellation/1 ;
    cidoc:P94i_was_created_by ex:contract_genoa_1450_07_15_house_sale/creation ;
    cidoc:P46i_forms_part_of ex:register_foglietta_1450 .  # TRANSFORMED

ex:register_foglietta_1450
    a cidoc:E31_Document ;
    a cidoc:E78_Curated_Holding ;
    cidoc:P1_is_identified_by ex:register_foglietta_1450/appellation/1 ;
    cidoc:P94i_was_created_by ex:register_foglietta_1450/creation .
```

### Example 2: Hierarchical Archival Structure

**Scenario**: A contract within a filza, which is within a busta, which is in an archive.

**Input Data**:
```turtle
ex:contract_001
    a gmn:E31_2_Sales_Contract ;
    gmn:P1_1_has_name "Contract 001"@en ;
    gmn:P46i_1_is_contained_in ex:filza_23 .

ex:filza_23
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Filza 23"@it ;
    gmn:P46i_1_is_contained_in ex:busta_5 .

ex:busta_5
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Busta 5"@it ;
    gmn:P46i_1_is_contained_in ex:archivio_stato_genova .

ex:archivio_stato_genova
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Archivio di Stato di Genova"@it ;
    cidoc:P55_has_current_location ex:genoa_city .
```

**Transformed Output**:
```turtle
ex:contract_001
    cidoc:P46i_forms_part_of ex:filza_23 .

ex:filza_23
    cidoc:P46i_forms_part_of ex:busta_5 .

ex:busta_5
    cidoc:P46i_forms_part_of ex:archivio_stato_genova .

# Transitive inference possible:
# ex:contract_001 cidoc:P46i_forms_part_of ex:archivio_stato_genova .
```

### Example 3: Multiple Documents in Same Container

**Scenario**: Multiple contracts in the same register.

**Input Data**:
```turtle
ex:contract_001 gmn:P46i_1_is_contained_in ex:register_1450 .
ex:contract_002 gmn:P46i_1_is_contained_in ex:register_1450 .
ex:contract_003 gmn:P46i_1_is_contained_in ex:register_1450 .
ex:contract_004 gmn:P46i_1_is_contained_in ex:register_1450 .
```

**Transformed Output**:
```turtle
ex:contract_001 cidoc:P46i_forms_part_of ex:register_1450 .
ex:contract_002 cidoc:P46i_forms_part_of ex:register_1450 .
ex:contract_003 cidoc:P46i_forms_part_of ex:register_1450 .
ex:contract_004 cidoc:P46i_forms_part_of ex:register_1450 .

# Inverse inferences:
ex:register_1450 cidoc:P46_is_composed_of ex:contract_001 ,
                                          ex:contract_002 ,
                                          ex:contract_003 ,
                                          ex:contract_004 .
```

### Example 4: Mixed Document Types in Collection

**Scenario**: Letters and contracts in the same archival box.

**Input Data**:
```turtle
ex:letter_1453_01_10
    a gmn:E31_6_Correspondence ;
    gmn:P46i_1_is_contained_in ex:box_correspondence_1453 .

ex:contract_1453_02_15
    a gmn:E31_2_Sales_Contract ;
    gmn:P46i_1_is_contained_in ex:box_correspondence_1453 .

ex:letter_1453_03_22
    a gmn:E31_6_Correspondence ;
    gmn:P46i_1_is_contained_in ex:box_correspondence_1453 .

ex:box_correspondence_1453
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Correspondence and Contracts, 1453"@en .
```

**Transformed Output**:
```turtle
ex:letter_1453_01_10 cidoc:P46i_forms_part_of ex:box_correspondence_1453 .
ex:contract_1453_02_15 cidoc:P46i_forms_part_of ex:box_correspondence_1453 .
ex:letter_1453_03_22 cidoc:P46i_forms_part_of ex:box_correspondence_1453 .
```

---

## Integration with Other Properties

### Complementary Properties

#### Document Creation Properties
```turtle
<contract>
    gmn:P94i_1_was_created_by <notary> ;      # Who created the document
    gmn:P94i_2_has_enactment_date "1450-03-15"^^xsd:date ;  # When
    gmn:P94i_3_has_place_of_enactment <genoa> ;  # Where created
    gmn:P46i_1_is_contained_in <register> .   # Where stored
```

These properties work together to provide complete document context.

#### Physical Location Properties
```turtle
<register>
    a cidoc:E78_Curated_Holding ;
    cidoc:P46_is_composed_of <contract> ;       # Contains documents
    cidoc:P55_has_current_location <archive> .  # Current physical location
```

#### Digital Representation
```turtle
<contract>
    gmn:P46i_1_is_contained_in <register> ;  # Physical container
    gmn:P138i_1_has_representation <scan_001.jpg> .  # Digital scan
```

### Property Chain Examples

#### Chain 1: Document → Container → Location
```turtle
# Find where a document is physically located
<contract> cidoc:P46i_forms_part_of <register> .
<register> cidoc:P55_has_current_location <archive> .
<archive> cidoc:P87_is_identified_by "Archivio di Stato di Genova"@it .
```

#### Chain 2: Document → Multiple Containment Levels
```turtle
<contract> cidoc:P46i_forms_part_of <filza> .
<filza> cidoc:P46i_forms_part_of <busta> .
<busta> cidoc:P46i_forms_part_of <fondo> .
<fondo> cidoc:P46i_forms_part_of <archivio> .
```

---

## Best Practices

### Data Entry Guidelines

1. **Always Link to Container**: If you know the archival container, use this property
   ```turtle
   <contract> gmn:P46i_1_is_contained_in <register> .
   ```

2. **Type Containers Properly**: Ensure containers have appropriate types
   ```turtle
   <register> a cidoc:E31_Document ;
              a cidoc:E78_Curated_Holding .
   ```

3. **Maintain Hierarchy**: Use multiple levels when applicable
   ```turtle
   <contract> gmn:P46i_1_is_contained_in <filza> .
   <filza> gmn:P46i_1_is_contained_in <busta> .
   ```

4. **Don't Confuse with Location**: Use correct property for current location
   ```turtle
   # Correct:
   <contract> gmn:P46i_1_is_contained_in <register> .
   <register> cidoc:P55_has_current_location <archive> .
   
   # Incorrect:
   <contract> gmn:P46i_1_is_contained_in <archive> .  # Unless archive is direct container
   ```

### Modeling Recommendations

#### Container Naming
Use consistent, informative names for containers:
```turtle
<register_foglietta_1450_1451>
    gmn:P1_1_has_name "Notarial Register of Antonio Foglietta, 1450-1451"@en ;
    gmn:P1_1_has_name "Registro notarile di Antonio Foglietta, 1450-1451"@it .
```

#### Container Typing
Always provide sufficient type information:
```turtle
<filza_23>
    a cidoc:E78_Curated_Holding ;  # Required
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300026392> ;  # "filze" in AAT
    gmn:P1_1_has_name "Filza 23"@it .
```

#### Multiple Containment
A document can be in multiple containers (e.g., original + copy):
```turtle
<contract_original> gmn:P46i_1_is_contained_in <register_original> .
<contract_copy> gmn:P46i_1_is_contained_in <register_copy> .
```

### Query Optimization

For large datasets, index on `P46i_forms_part_of`:
```sql
-- If using a triple store with SQL backend
CREATE INDEX idx_forms_part_of ON triples(predicate, object) 
WHERE predicate = 'http://www.cidoc-crm.org/cidoc-crm/P46i_forms_part_of';
```

---

## SPARQL Query Patterns

### Query 1: Find All Documents in a Container

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

SELECT ?document ?name
WHERE {
    ?document cidoc:P46i_forms_part_of <http://example.org/register_1450> ;
              cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
}
ORDER BY ?name
```

### Query 2: Find Container of a Document

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?container ?containerName
WHERE {
    <http://example.org/contract_001> cidoc:P46i_forms_part_of ?container .
    ?container cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?containerName .
}
```

### Query 3: Traverse Archival Hierarchy

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?level1 ?level2 ?level3 ?level4
WHERE {
    <http://example.org/contract_001> cidoc:P46i_forms_part_of ?level1 .
    OPTIONAL { ?level1 cidoc:P46i_forms_part_of ?level2 . }
    OPTIONAL { ?level2 cidoc:P46i_forms_part_of ?level3 . }
    OPTIONAL { ?level3 cidoc:P46i_forms_part_of ?level4 . }
}
```

### Query 4: Find All Documents at Any Level in Archive

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?document
WHERE {
    ?document cidoc:P46i_forms_part_of+ <http://example.org/archivio_stato_genova> .
}
```
*(Uses property path `+` for one or more levels)*

### Query 5: Count Documents per Container

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?container (COUNT(?document) AS ?documentCount)
WHERE {
    ?document cidoc:P46i_forms_part_of ?container .
}
GROUP BY ?container
ORDER BY DESC(?documentCount)
```

### Query 6: Find Documents Without Container Information

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

SELECT ?document
WHERE {
    ?document a ?docType .
    FILTER(STRSTARTS(STR(?docType), "http://www.genoesemerchantnetworks.com/ontology#E31_"))
    FILTER NOT EXISTS { ?document cidoc:P46i_forms_part_of ?container . }
}
```

### Query 7: Find Physical Location of Document via Container

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?document ?container ?location ?locationName
WHERE {
    ?document cidoc:P46i_forms_part_of ?container .
    ?container cidoc:P55_has_current_location ?location .
    ?location cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?locationName .
}
```

---

## Validation Rules

### Rule 1: Domain Validation
All subjects must be E31_Document or subclass:
```sparql
ASK {
    ?doc gmn:P46i_1_is_contained_in ?container .
    FILTER NOT EXISTS { ?doc a ?type . ?type rdfs:subClassOf* cidoc:E31_Document . }
}
# Should return FALSE
```

### Rule 2: Range Validation
All objects must be E78_Curated_Holding or subclass:
```sparql
ASK {
    ?doc gmn:P46i_1_is_contained_in ?container .
    FILTER NOT EXISTS { ?container a ?type . ?type rdfs:subClassOf* cidoc:E78_Curated_Holding . }
}
# Should return FALSE
```

### Rule 3: Circular Reference Check
Detect circular containment:
```sparql
ASK {
    ?doc cidoc:P46i_forms_part_of+ ?doc .
}
# Should return FALSE
```

---

## Archival Standards Alignment

### ISAD(G) Alignment

This property aligns with ISAD(G) element 3.1.4 "Immediate source of acquisition or transfer":

| ISAD(G) Element | GMN Property |
|----------------|--------------|
| 3.1.4 Immediate source | `P46i_1_is_contained_in` links to source container |
| 3.1.3 Extent | Can be inferred by counting contained documents |
| 3.1.1 Reference code | Stored as `P1_is_identified_by` on container |

### EAD Alignment

Maps to EAD elements:
```xml
<archdesc>
    <dsc>
        <c01> <!-- Container -->
            <did>
                <unitid>register_1450</unitid>
            </did>
            <c02> <!-- Contained document -->
                <did>
                    <unitid>contract_001</unitid>
                </did>
            </c02>
        </c01>
    </dsc>
</archdesc>
```

---

## Conclusion

The `gmn:P46i_1_is_contained_in` property provides a straightforward, CIDOC-CRM-compliant way to express archival containment relationships. Its direct mapping transformation makes it efficient to implement while maintaining full semantic clarity. Use this property consistently to preserve archival context and enable powerful hierarchical queries across your documentary collections.

**Key Takeaways**:
- ✅ Direct property mapping (no intermediate nodes)
- ✅ Preserves archival context and provenance
- ✅ Supports hierarchical and transitive queries
- ✅ Fully CIDOC-CRM compliant
- ✅ Simple to implement and maintain
