# GMN P3.1 has editorial note - Ontology Documentation

**Property URI:** `gmn:P3_1_has_editorial_note`  
**Version:** 1.0  
**Date:** October 26, 2025  
**Status:** Implemented

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Formal Definition](#formal-definition)
3. [CIDOC-CRM Alignment](#cidoc-crm-alignment)
4. [Transformation Pattern](#transformation-pattern)
5. [Semantic Examples](#semantic-examples)
6. [Integration Patterns](#integration-patterns)
7. [Inference Rules](#inference-rules)
8. [Validation Constraints](#validation-constraints)

---

## Property Overview

### Purpose

`gmn:P3_1_has_editorial_note` provides a simplified mechanism for expressing editorial notes, internal comments, and documentation about any entity in the GMN database. It serves as a convenient shorthand for creating CIDOC-CRM-compliant linguistic objects typed as editorial notes.

### Design Philosophy

1. **Internal Documentation** - Designed primarily for internal project use
2. **Privacy Control** - Can be excluded from public exports
3. **Flexibility** - Applicable to any entity (E1_CRM_Entity domain)
4. **Semantic Rigor** - Transforms to full CIDOC-CRM structure when needed
5. **Practical Utility** - Balances formal ontology requirements with research workflow needs

### Key Characteristics

- **Type:** Datatype Property (owl:DatatypeProperty)
- **Simplified Property:** Yes - transforms to full CIDOC-CRM path
- **Internal Only:** Yes - marked with `gmn:isInternalOnly true`
- **Multiple Values:** Supported - can have multiple notes per entity
- **AAT Typed:** Yes - automatically typed as aat:300456627

---

## Formal Definition

### RDF/Turtle Definition

```turtle
# Property: P3.1 has editorial note
gmn:P3_1_has_editorial_note 
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P3.1 has editorial note"@en ;
    rdfs:comment "Simplified property for expressing editorial notes, comments, and internal documentation about an entity. Represents the full CIDOC-CRM path: P67i_is_referred_to_by > E33_Linguistic_Object > P2_has_type <http://vocab.getty.edu/aat/300456627> > P190_has_symbolic_content. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The linguistic object type is automatically set to AAT 300456627. This property is intended for internal project use and may be excluded from public data exports."@en ;
    rdfs:subPropertyOf cidoc:P3_has_note ;
    rdfs:domain cidoc:E1_CRM_Entity ;
    rdfs:range cidoc:E62_String ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P3_has_note, cidoc:P67i_is_referred_to_by, cidoc:P190_has_symbolic_content, aat:300456627 ;
    gmn:hasImplicitType aat:300456627 ;
    gmn:isInternalOnly true .
```

### Property Metadata

| Attribute | Value |
|-----------|-------|
| **URI** | `gmn:P3_1_has_editorial_note` |
| **Label** | "P3.1 has editorial note"@en |
| **Type** | owl:DatatypeProperty, rdf:Property |
| **Subproperty Of** | cidoc:P3_has_note |
| **Domain** | cidoc:E1_CRM_Entity |
| **Range** | cidoc:E62_String |
| **Created** | 2025-10-16 |
| **Implicit Type** | aat:300456627 (editorial notes) |
| **Internal Only** | true |

---

## CIDOC-CRM Alignment

### Parent Property

**cidoc:P3_has_note**
- Domain: E1_CRM_Entity
- Range: E62_String
- Scope note: "This property is a container for all informal descriptions about an object that have not been expressed in terms of CRM constructs."

**Relationship:**  
`gmn:P3_1_has_editorial_note rdfs:subPropertyOf cidoc:P3_has_note`

While `P3_has_note` allows direct string annotation, `gmn:P3_1_has_editorial_note` transforms to a more structured pattern using E33_Linguistic_Object to enable richer semantic relationships.

### Full CIDOC-CRM Path

The property represents this complete semantic path:

```
Subject Entity (E1_CRM_Entity)
    ↓ cidoc:P67i_is_referred_to_by
Editorial Note (E33_Linguistic_Object)
    ↓ cidoc:P2_has_type
Note Type (E55_Type) = aat:300456627
    ↓ (back to E33)
Editorial Note (E33_Linguistic_Object)
    ↓ cidoc:P190_has_symbolic_content
Note Text (E62_String)
```

### CIDOC-CRM Classes Involved

**E1_CRM_Entity**
- Definition: "This class comprises all things in the universe of discourse of the CIDOC Conceptual Reference Model"
- Role: Domain - the entity being annotated

**E33_Linguistic_Object**
- Definition: "This class comprises identifiable expressions in natural language or languages"
- Role: The editorial note itself as a linguistic expression
- Properties:
  - P2_has_type → E55_Type
  - P190_has_symbolic_content → E62_String

**E55_Type**
- Definition: "This class comprises concepts denoted by terms from thesauri and controlled vocabularies"
- Role: Specifies the note is an editorial note (AAT 300456627)

**E62_String**
- Definition: "This class comprises coherent sequences of binary-encoded symbols"
- Role: The actual text content of the note

### CIDOC-CRM Properties Involved

**P67i_is_referred_to_by**
- Domain: E1_CRM_Entity
- Range: E89_Propositional_Object
- Scope: Links entity to textual references about it
- Note: E33_Linguistic_Object is a subclass of E89_Propositional_Object

**P2_has_type**
- Domain: E1_CRM_Entity
- Range: E55_Type
- Scope: Links an entity to its classification

**P190_has_symbolic_content**
- Domain: E90_Symbolic_Object
- Range: E62_String
- Scope: Links a symbolic object to its textual content
- Note: E33_Linguistic_Object is a subclass of E90_Symbolic_Object

---

## Transformation Pattern

### Simplified Form (Input)

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/person/giovanni_001",
  "@type": "cidoc:E21_Person",
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Name spelling varies in sources between 'Giovanni' and 'Iohanes'."}
  ]
}
```

### Full CIDOC-CRM Form (Output with --include-internal)

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "aat": "http://vocab.getty.edu/aat/"
  },
  "@id": "http://example.org/person/giovanni_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P67i_is_referred_to_by": [
    {
      "@id": "http://example.org/person/giovanni_001/note/a1b2c3d4",
      "@type": "cidoc:E33_Linguistic_Object",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300456627",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Name spelling varies in sources between 'Giovanni' and 'Iohanes'."
    }
  ]
}
```

### Removed Form (Output without --include-internal, default)

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/person/giovanni_001",
  "@type": "cidoc:E21_Person"
}
```

The editorial note is completely removed for public export.

---

## Semantic Examples

### Example 1: Person with Uncertain Name

**Scenario:** A person whose name appears differently in various sources

```turtle
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix aat: <http://vocab.getty.edu/aat/> .

<http://example.org/person/giacomo_001> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giacomo Spinola q. Antonio" ;
    gmn:P3_1_has_editorial_note "Name appears as 'Iacopo' in ASG Not. 234, f. 12v. Both spellings refer to same individual based on shared patronymic and property references." .
```

**After Transformation (with --include-internal):**

```turtle
<http://example.org/person/giacomo_001> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <http://example.org/person/giacomo_001/appellation/12345678> ;
    cidoc:P67i_is_referred_to_by <http://example.org/person/giacomo_001/note/87654321> .

<http://example.org/person/giacomo_001/appellation/12345678> a cidoc:E41_Appellation ;
    cidoc:P2_has_type aat:300404650 ;
    cidoc:P190_has_symbolic_content "Giacomo Spinola q. Antonio" .

<http://example.org/person/giacomo_001/note/87654321> a cidoc:E33_Linguistic_Object ;
    cidoc:P2_has_type aat:300456627 ;
    cidoc:P190_has_symbolic_content "Name appears as 'Iacopo' in ASG Not. 234, f. 12v. Both spellings refer to same individual based on shared patronymic and property references." .
```

---

### Example 2: Contract with Source Issues

**Scenario:** A sales contract where the document is partially damaged

```turtle
<http://example.org/contract/sale_045> a gmn:E31_2_Sales_Contract ;
    gmn:P102_1_has_title "Sale of Vineyard" ;
    gmn:P3_1_has_editorial_note "Document partially damaged. Sale price illegible but context suggests 100-150 lire based on comparable properties in same period." .
```

**After Transformation (with --include-internal):**

```turtle
<http://example.org/contract/sale_045> a gmn:E31_2_Sales_Contract ;
    cidoc:P102_has_title <http://example.org/contract/sale_045/title/abc123> ;
    cidoc:P67i_is_referred_to_by <http://example.org/contract/sale_045/note/def456> .

<http://example.org/contract/sale_045/title/abc123> a cidoc:E35_Title ;
    cidoc:P190_has_symbolic_content "Sale of Vineyard" .

<http://example.org/contract/sale_045/note/def456> a cidoc:E33_Linguistic_Object ;
    cidoc:P2_has_type aat:300456627 ;
    cidoc:P190_has_symbolic_content "Document partially damaged. Sale price illegible but context suggests 100-150 lire based on comparable properties in same period." .
```

---

### Example 3: Place with Modern Context

**Scenario:** Historical place mapped to modern location

```turtle
<http://example.org/place/vignolo> a cidoc:E53_Place ;
    gmn:P1_1_has_name "Vignolo" ;
    gmn:P3_1_has_editorial_note "Modern location: frazione of Serra Riccò, province of Genoa. GPS coordinates: 44.4833°N, 8.9167°E. Historical boundaries uncertain but centered on modern village." .
```

---

### Example 4: Multiple Notes on Single Entity

**Scenario:** Multiple editorial observations about the same person

```turtle
<http://example.org/person/bartolomeo_001> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Bartolomeo de Vignolo" ;
    gmn:P3_1_has_editorial_note 
        "Primary attestation: ASG Not. 456, f. 78r, dated 1455-03-12." ,
        "Loconym 'de Vignolo' suggests origin from Vignolo near Serra Riccò." ,
        "Possible relation to Giovanni de Vignolo (ASG Not. 789) - requires investigation." .
```

**After Transformation (with --include-internal):**

Each note becomes a separate E33_Linguistic_Object:

```turtle
<http://example.org/person/bartolomeo_001> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <http://example.org/person/bartolomeo_001/appellation/note1> ;
    cidoc:P67i_is_referred_to_by 
        <http://example.org/person/bartolomeo_001/note/abc123> ,
        <http://example.org/person/bartolomeo_001/note/def456> ,
        <http://example.org/person/bartolomeo_001/note/ghi789> .

<http://example.org/person/bartolomeo_001/note/abc123> a cidoc:E33_Linguistic_Object ;
    cidoc:P2_has_type aat:300456627 ;
    cidoc:P190_has_symbolic_content "Primary attestation: ASG Not. 456, f. 78r, dated 1455-03-12." .

<http://example.org/person/bartolomeo_001/note/def456> a cidoc:E33_Linguistic_Object ;
    cidoc:P2_has_type aat:300456627 ;
    cidoc:P190_has_symbolic_content "Loconym 'de Vignolo' suggests origin from Vignolo near Serra Riccò." .

<http://example.org/person/bartolomeo_001/note/ghi789> a cidoc:E33_Linguistic_Object ;
    cidoc:P2_has_type aat:300456627 ;
    cidoc:P190_has_symbolic_content "Possible relation to Giovanni de Vignolo (ASG Not. 789) - requires investigation." .
```

---

## Integration Patterns

### Pattern 1: Editorial Notes with Name Properties

Editorial notes frequently complement name properties to explain uncertainties:

```json
{
  "@id": "http://example.org/person/giovanni_002",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [
    {"@value": "Giovanni Rossi"}
  ],
  "gmn:P1_2_has_name_from_source": [
    {"@value": "Iohannes Rubeus"}
  ],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Catalog name 'Giovanni Rossi' is normalized form. Original Latin form 'Iohannes Rubeus' appears in all source documents."}
  ]
}
```

---

### Pattern 2: Editorial Notes with Date Properties

Notes can explain date uncertainties or estimation methods:

```json
{
  "@id": "http://example.org/person/maria_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [
    {"@value": "Maria de Genova"}
  ],
  "gmn:P11i_1_earliest_attestation_date": [
    {"@value": "1445-06-15", "@type": "xsd:date"}
  ],
  "gmn:P11i_2_latest_attestation_date": [
    {"@value": "1478-11-22", "@type": "xsd:date"}
  ],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Active period spans 33 years. Latest attestation is sale of property as widow, suggesting death shortly after."}
  ]
}
```

---

### Pattern 3: Editorial Notes with Geographic References

Notes can provide modern context for historical places:

```json
{
  "@id": "http://example.org/place/sampierdarena",
  "@type": "cidoc:E53_Place",
  "gmn:P1_1_has_name": [
    {"@value": "Sampierdarena"}
  ],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Historical: Western suburb of Genoa, independent commune until 1926. Modern: Neighborhood (quartiere) of Genoa. Major port and industrial area in 15th century."}
  ]
}
```

---

### Pattern 4: Editorial Notes with Contract Properties

Notes can document issues with contract records:

```json
{
  "@id": "http://example.org/contract/arbitration_012",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P102_1_has_title": [
    {"@value": "Arbitration - Spinola Property Dispute"}
  ],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/person/party1"},
    {"@id": "http://example.org/person/party2"}
  ],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Arbitration outcome recorded in separate document ASG Not. 567, f. 23r. Parties reached settlement before formal decision."}
  ]
}
```

---

## Inference Rules

### Rule 1: Internal Classification

```sparql
# Any entity with gmn:P3_1_has_editorial_note is marked as having internal documentation
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
    ?entity gmn:hasInternalDocumentation true .
}
WHERE {
    ?entity gmn:P3_1_has_editorial_note ?note .
}
```

---

### Rule 2: Note Type Inference

```sparql
# After transformation, all E33 objects linked via P67i with P2_has_type aat:300456627
# can be inferred to be editorial notes
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

CONSTRUCT {
    ?note rdf:type gmn:EditorialNote .
}
WHERE {
    ?entity cidoc:P67i_is_referred_to_by ?note .
    ?note a cidoc:E33_Linguistic_Object ;
          cidoc:P2_has_type aat:300456627 .
}
```

---

### Rule 3: Quality Flag Inference

```sparql
# Entities with notes containing quality flag keywords are marked for review
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

CONSTRUCT {
    ?entity gmn:requiresReview true .
}
WHERE {
    ?entity gmn:P3_1_has_editorial_note ?note .
    FILTER(CONTAINS(LCASE(STR(?note)), "needs review") || 
           CONTAINS(LCASE(STR(?note)), "uncertain") ||
           CONTAINS(LCASE(STR(?note)), "requires verification"))
}
```

---

## Validation Constraints

### Constraint 1: Non-Empty Strings

Editorial notes must contain actual content:

```shacl
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .

gmn:EditorialNoteShape
    a sh:NodeShape ;
    sh:targetSubjectsOf gmn:P3_1_has_editorial_note ;
    sh:property [
        sh:path gmn:P3_1_has_editorial_note ;
        sh:minLength 1 ;
        sh:message "Editorial notes must not be empty strings" ;
    ] .
```

---

### Constraint 2: String Datatype

Editorial notes must be strings:

```shacl
gmn:EditorialNoteDatatype shape
    a sh:NodeShape ;
    sh:targetSubjectsOf gmn:P3_1_has_editorial_note ;
    sh:property [
        sh:path gmn:P3_1_has_editorial_note ;
        sh:datatype xsd:string ;
        sh:message "Editorial notes must be string values" ;
    ] .
```

---

### Constraint 3: Domain Validation

Editorial notes can only be applied to E1_CRM_Entity instances:

```shacl
gmn:EditorialNoteDomainShape
    a sh:NodeShape ;
    sh:targetSubjectsOf gmn:P3_1_has_editorial_note ;
    sh:class cidoc:E1_CRM_Entity ;
    sh:message "Editorial notes can only be applied to CRM entities" .
```

---

## Getty AAT Concept

### AAT 300456627: editorial notes

**Preferred Term:** editorial notes  
**Alternate Terms:** editor's notes, editorial annotations  
**Hierarchy:**
- Associated Concepts Facet (300264088)
  - Associated Concepts (300054557)
    - document genres (300027253)
      - editorial notes (300456627)

**Scope Note:** "Notes written by editors that provide context, explanation, or clarification of the content of a document or publication."

**Use in GMN:**  
This AAT concept is used to type all E33_Linguistic_Object instances created by transforming `gmn:P3_1_has_editorial_note` properties.

---

## Comparison with Related Properties

### vs. cidoc:P3_has_note

| Aspect | gmn:P3_1_has_editorial_note | cidoc:P3_has_note |
|--------|----------------------------|-------------------|
| **Structure** | Transforms to E33 + type | Direct string annotation |
| **Typing** | Automatically typed (aat:300456627) | Not typed |
| **Internal Use** | Yes (gmn:isInternalOnly) | No |
| **Public Export** | Optional | Always included |
| **Domain** | E1_CRM_Entity | E1_CRM_Entity |
| **Semantic Richness** | Higher (allows relationships) | Lower (simple annotation) |

**When to use which:**
- Use `gmn:P3_1_has_editorial_note` for internal research notes that may be excluded from public exports
- Use `cidoc:P3_has_note` for public-facing general notes that don't need structured representation

---

### vs. cidoc:P70_documents

| Aspect | gmn:P3_1_has_editorial_note | cidoc:P70_documents |
|--------|----------------------------|---------------------|
| **Purpose** | Editorial commentary | Formal documentation |
| **Direction** | Subject has note | Document about subject |
| **Formality** | Informal, internal | Formal, scholarly |
| **Range** | String | E1_CRM_Entity |
| **Use Case** | Working notes | Published scholarship |

---

## SPARQL Query Patterns

### Pattern 1: Find All Entities with Editorial Notes

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

SELECT ?entity ?note
WHERE {
    ?entity gmn:P3_1_has_editorial_note ?note .
}
ORDER BY ?entity
```

---

### Pattern 2: Find Notes by Keyword

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

SELECT ?entity ?note
WHERE {
    ?entity gmn:P3_1_has_editorial_note ?note .
    FILTER(CONTAINS(LCASE(STR(?note)), "uncertain"))
}
```

---

### Pattern 3: Count Notes per Entity Type

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?type (COUNT(?note) AS ?noteCount)
WHERE {
    ?entity rdf:type ?type ;
            gmn:P3_1_has_editorial_note ?note .
}
GROUP BY ?type
ORDER BY DESC(?noteCount)
```

---

### Pattern 4: Find Transformed Editorial Notes (After --include-internal)

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

SELECT ?entity ?noteURI ?noteText
WHERE {
    ?entity cidoc:P67i_is_referred_to_by ?noteURI .
    ?noteURI a cidoc:E33_Linguistic_Object ;
             cidoc:P2_has_type aat:300456627 ;
             cidoc:P190_has_symbolic_content ?noteText .
}
```

---

## Summary

`gmn:P3_1_has_editorial_note` is a specialized property for internal project documentation that:

1. **Extends CIDOC-CRM** with editorial note functionality
2. **Provides flexibility** through optional transformation
3. **Maintains privacy** for internal research notes
4. **Ensures semantic rigor** through AAT typing
5. **Supports research workflow** with practical convenience

The property balances the needs of formal ontological modeling with the practical requirements of collaborative historical research projects.

---

**Document Version:** 1.0  
**Date:** October 26, 2025  
**Property:** gmn:P3_1_has_editorial_note  
**Ontology:** Genoese Merchant Networks (GMN)
