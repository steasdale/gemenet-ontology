# GMN P70.11 Documents Referenced Person - Ontology Documentation

## Table of Contents
1. [Property Overview](#property-overview)
2. [Semantic Foundations](#semantic-foundations)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Usage Patterns](#usage-patterns)
5. [Distinction from Related Properties](#distinction-from-related-properties)
6. [Examples and Use Cases](#examples-and-use-cases)
7. [Technical Specifications](#technical-specifications)
8. [Best Practices](#best-practices)

---

## Property Overview

### Basic Information

| Attribute | Value |
|-----------|-------|
| **Property URI** | `gmn:P70_11_documents_referenced_person` |
| **Label** | "P70.11 documents referenced person" |
| **Property Type** | `owl:ObjectProperty`, `rdf:Property` |
| **Subproperty Of** | `cidoc:P67_refers_to` |
| **Domain** | `cidoc:E31_Document` |
| **Range** | `cidoc:E21_Person` |
| **Creation Date** | 2025-10-17 |
| **Status** | Active |

### Purpose Statement

The `gmn:P70_11_documents_referenced_person` property associates a document with any person who is mentioned in the document text but does not have a specified transactional or participatory role. This property captures the textual presence of individuals in the documentary record without implying their active participation in the documented events.

### Scope

**Includes**:
- Deceased persons mentioned for identification or context
- Neighbors referenced in property boundary descriptions
- Previous owners mentioned in provenance statements
- Family members referenced but not participating
- Absent parties whose rights or claims are acknowledged
- Any individuals named in the document without a specific functional role

**Excludes** (use other properties instead):
- Active witnesses (use `P70_15_documents_witness`)
- Transaction parties: sellers, buyers, procurators, guarantors, brokers
- Persons with defined roles in the documented event

---

## Semantic Foundations

### Conceptual Model

Unlike most P70 subproperties which model participation in an E8_Acquisition event, P70.11 represents a **direct documentary reference**:

```
E31_Document --P67_refers_to--> E21_Person
```

This acknowledges textual presence without implying participation in the transaction.

### Relationship to CIDOC-CRM Entities

#### E31_Document
The document is the subject that refers to the person. This can be:
- E31_1_Contract and its subclasses (E31_2_Sales_Contract, etc.)
- E31_5_Declaration
- E31_6_Correspondence
- Any document type that might reference persons

#### E21_Person
The person being referenced. Characteristics:
- May be living or deceased at time of document creation
- May have any relationship to the document's subject matter
- May appear once or multiple times in different contexts
- Need not be identified beyond their mention in the text

### Theoretical Justification

#### Why P67_refers_to?
P67_refers_to is the appropriate CIDOC-CRM property because:
1. It models **aboutness** rather than participation
2. It applies to any CRM entity as range (we narrow to E21_Person)
3. It makes no claims about the nature of the relationship
4. It's neutral about the referenced entity's role or status

#### Why Not P11_had_participant?
P11_had_participant would be incorrect because:
- It implies active participation in an event
- Referenced persons may be deceased or absent
- References may be incidental (e.g., boundary markers)
- Participation requires involvement in the documented activity

#### Why Not P14_carried_out_by?
P14_carried_out_by would be incorrect because:
- It implies agency and action
- Referenced persons may not have performed any action
- It requires an E7_Activity context
- References are often passive mentions

---

## CIDOC-CRM Mapping

### Transformation Pattern

#### Input Format (GMN Simplified)
```turtle
@prefix gmn: <http://example.org/gmn/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

:contract_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_11_documents_referenced_person :person_001 ,
                                           :person_002 .

:person_001 a cidoc:E21_Person ;
    rdfs:label "Giovanni (deceased father of seller)" .

:person_002 a cidoc:E21_Person ;
    rdfs:label "Marco (owner of adjacent property)" .
```

#### Output Format (CIDOC-CRM Compliant)
```turtle
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .

:contract_001 a gmn:E31_2_Sales_Contract ;
    cidoc:P67_refers_to :person_001 ,
                        :person_002 .

:person_001 a cidoc:E21_Person ;
    rdfs:label "Giovanni (deceased father of seller)" .

:person_002 a cidoc:E21_Person ;
    rdfs:label "Marco (owner of adjacent property)" .
```

### Transformation Algorithm

1. **Identify**: Check if `gmn:P70_11_documents_referenced_person` exists in document
2. **Initialize**: Create `cidoc:P67_refers_to` array if it doesn't exist
3. **Transform**: For each referenced person:
   - If person is object with properties: copy entire object
   - If person is URI string: create minimal person object
   - Ensure `@type` is `cidoc:E21_Person`
   - Add to `cidoc:P67_refers_to` array
4. **Cleanup**: Remove original `gmn:P70_11_documents_referenced_person` property

### Compatibility with Other Properties

P70.11 plays well with other properties that use P67_refers_to:
- `gmn:P70_13_documents_referenced_place` (also uses P67, but range is E53_Place)
- `gmn:P70_14_documents_referenced_object` (also uses P67, range is E1_CRM_Entity)

All three can coexist in the same P67_refers_to array, distinguished by their `@type`.

---

## Usage Patterns

### Pattern 1: Deceased Person in Patronymic

**Scenario**: Document identifies a party as "Giovanni, son of the late Marco"

```turtle
:contract_123 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller :giovanni ;
    gmn:P70_11_documents_referenced_person :marco_deceased .

:giovanni a cidoc:E21_Person ;
    rdfs:label "Giovanni di Marco" ;
    gmn:P1_1_has_name "Giovanni di Marco" .

:marco_deceased a cidoc:E21_Person ;
    rdfs:label "Marco (deceased father of Giovanni)" ;
    gmn:P1_1_has_name "Marco" .
```

**After Transformation**:
```turtle
:contract_123 a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents :acquisition_123 ;
    cidoc:P67_refers_to :marco_deceased .

:acquisition_123 a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_from :giovanni .

:marco_deceased a cidoc:E21_Person ;
    rdfs:label "Marco (deceased father of Giovanni)" .
```

### Pattern 2: Multiple Neighbors in Boundary Description

**Scenario**: Property boundaries reference multiple adjacent landowners

```turtle
:contract_456 a gmn:E31_2_Sales_Contract ;
    gmn:P70_3_documents_transfer_of :property_456 ;
    gmn:P70_11_documents_referenced_person :pietro_north ,
                                           :antonio_south ,
                                           :leonardo_east .

:pietro_north a cidoc:E21_Person ;
    rdfs:label "Pietro (owner of northern boundary)" .

:antonio_south a cidoc:E21_Person ;
    rdfs:label "Antonio (owner of southern boundary)" .

:leonardo_east a cidoc:E21_Person ;
    rdfs:label "Leonardo (owner of eastern boundary)" .
```

**Usage Note**: These persons are not parties to the transaction—they're landmarks in the property description.

### Pattern 3: Previous Owner in Provenance Chain

**Scenario**: Document mentions previous ownership

```turtle
:contract_789 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller :seller_current ;
    gmn:P70_11_documents_referenced_person :owner_previous .

:owner_previous a cidoc:E21_Person ;
    rdfs:label "Francesco da Prato (previous owner, sold 1445)" ;
    rdfs:comment "Mentioned in provenance statement" .
```

### Pattern 4: Minimal Reference (URI Only)

**Scenario**: Person identified but no additional data available

```turtle
:contract_012 a gmn:E31_2_Sales_Contract ;
    gmn:P70_11_documents_referenced_person <http://example.org/person/unknown_123> .
```

**After Transformation**:
```turtle
:contract_012 a gmn:E31_2_Sales_Contract ;
    cidoc:P67_refers_to <http://example.org/person/unknown_123> .

<http://example.org/person/unknown_123> a cidoc:E21_Person .
```

### Pattern 5: Mixed Notation (Some with Data, Some URIs Only)

**Scenario**: Varying levels of information about referenced persons

```turtle
:contract_345 a gmn:E31_2_Sales_Contract ;
    gmn:P70_11_documents_referenced_person 
        :person_detailed ,
        <http://example.org/person/minimal> ,
        :person_another .

:person_detailed a cidoc:E21_Person ;
    rdfs:label "Detailed Person" ;
    gmn:P1_1_has_name "Lorenzo Medici" .

:person_another a cidoc:E21_Person ;
    rdfs:label "Another Person" .
```

---

## Distinction from Related Properties

### P70.11 vs. P70.15 (documents witness)

| Aspect | P70.11 Referenced Person | P70.15 Witness |
|--------|-------------------------|----------------|
| **Participation** | Not present at event | Present at event |
| **Role** | Mentioned in text | Active observer |
| **Legal Function** | Contextual reference | Legal validation |
| **CIDOC Path** | E31 > P67 > E21 | E31 > P70 > E8 > P11 > E21 |
| **Example** | Deceased parent in patronymic | Person who signed as witness |

### P70.11 vs. Other P70 Properties

| Property | Relationship to Event | Example Context |
|----------|----------------------|-----------------|
| **P70.1** (seller) | Direct participant | Party selling property |
| **P70.2** (buyer) | Direct participant | Party buying property |
| **P70.4/5** (procurator) | Legal representative | Acting on behalf of party |
| **P70.6/7** (guarantor) | Security provider | Guaranteeing payment |
| **P70.8** (broker) | Transaction facilitator | Arranged the sale |
| **P70.11** (referenced) | **No event role** | **Mentioned in narrative** |

### When to Use P70.11 Instead of Other Properties

Use P70.11 when:
✅ Person is mentioned but has no transactional function
✅ Person provides context (e.g., deceased relative)
✅ Person is geographic reference (neighbor)
✅ Person is historical reference (previous owner)
✅ Person's relationship to transaction is unclear or absent

Do NOT use P70.11 when:
❌ Person has a defined role (use specific P70 property)
❌ Person witnessed the event (use P70.15)
❌ Person's participation is documented (use appropriate P11, P14, etc.)

---

## Examples and Use Cases

### Example 1: Family Identification

**Historical Context**: Medieval contracts often identified parties through family relationships

```turtle
# Document Text: 
# "Venduto per Giovanni di Marco del fu Tommaso..."
# (Sold by Giovanni son of Marco son of the late Tommaso...)

:contract_medieval_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller :giovanni ;
    gmn:P70_11_documents_referenced_person :marco_father ,
                                           :tommaso_grandfather .

:giovanni a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giovanni di Marco" .

:marco_father a cidoc:E21_Person ;
    gmn:P1_1_has_name "Marco" ;
    rdfs:comment "Father of Giovanni, mentioned for identification" .

:tommaso_grandfather a cidoc:E21_Person ;
    gmn:P1_1_has_name "Tommaso" ;
    rdfs:comment "Deceased grandfather of Giovanni" .
```

### Example 2: Property Boundaries

**Historical Context**: Properties defined by neighboring landowners

```turtle
# Document Text:
# "A parcel bounded on the north by the property of Pietro Rossi,
#  on the south by lands of the heirs of Giovanni Bianchi..."

:contract_boundary_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_3_documents_transfer_of :property_vineyard_001 ;
    gmn:P70_11_documents_referenced_person :pietro_neighbor ,
                                           :giovanni_deceased_heirs .

:pietro_neighbor a cidoc:E21_Person ;
    gmn:P1_1_has_name "Pietro Rossi" ;
    rdfs:comment "Owner of northern boundary property" .

:giovanni_deceased_heirs a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giovanni Bianchi" ;
    rdfs:comment "Deceased, heirs own southern boundary" .
```

### Example 3: Consent and Permissions

**Historical Context**: Wife's consent required for husband's transactions

```turtle
# Document Text:
# "With the consent and approval of his wife Lucia..."

:contract_consent_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller :husband ;
    gmn:P70_11_documents_referenced_person :lucia_wife .

:husband a cidoc:E21_Person ;
    gmn:P1_1_has_name "Antonio Ferrara" .

:lucia_wife a cidoc:E21_Person ;
    gmn:P1_1_has_name "Lucia" ;
    rdfs:comment "Wife giving consent, mentioned but not signatory" .
```

**Note**: If Lucia actively participated (e.g., co-signed), she would be a seller (P70.1), not a referenced person.

### Example 4: Previous Transactions

**Historical Context**: Establishing provenance chain

```turtle
# Document Text:
# "This property was previously purchased from Matteo Verdi 
#  on 15 March 1450..."

:contract_provenance_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller :current_seller ;
    gmn:P70_11_documents_referenced_person :matteo_previous_seller .

:matteo_previous_seller a cidoc:E21_Person ;
    gmn:P1_1_has_name "Matteo Verdi" ;
    rdfs:comment "Sold property to current seller in 1450" .
```

### Example 5: Rights and Claims

**Historical Context**: Acknowledging but not transferring rights

```turtle
# Document Text:
# "Sold with the understanding that Lorenzo Medici retains
#  water rights to the western spring..."

:contract_rights_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_3_documents_transfer_of :property_farmland_001 ;
    gmn:P70_11_documents_referenced_person :lorenzo_rights_holder .

:lorenzo_rights_holder a cidoc:E21_Person ;
    gmn:P1_1_has_name "Lorenzo Medici" ;
    rdfs:comment "Retains water rights, mentioned but not party to sale" .
```

### Example 6: Multiple Documents, Same Person

**Pattern**: Person referenced in multiple contracts

```turtle
:contract_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_11_documents_referenced_person :marco_neighbor .

:contract_002 a gmn:E31_2_Sales_Contract ;
    gmn:P70_11_documents_referenced_person :marco_neighbor .

:contract_003 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller :marco_neighbor .

:marco_neighbor a cidoc:E21_Person ;
    gmn:P1_1_has_name "Marco Santini" ;
    rdfs:comment "Referenced as neighbor in contracts 001 and 002, seller in contract 003" .
```

**Research Value**: Tracking an individual's progression from peripheral mention to active participant.

---

## Technical Specifications

### RDF/OWL Characteristics

```turtle
gmn:P70_11_documents_referenced_person
    a owl:ObjectProperty ;           # Object property (relates instances)
    a rdf:Property ;                 # Also an RDF property
    rdfs:subPropertyOf cidoc:P67_refers_to ;  # Inherits semantics
    rdfs:domain cidoc:E31_Document ; # Applies to documents
    rdfs:range cidoc:E21_Person ;    # References persons
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P67_refers_to .
```

### Cardinality

- **Minimum**: 0 (optional—not all documents reference persons)
- **Maximum**: Unbounded (can reference any number of persons)

### Constraints

#### Domain Constraint
Must be used with E31_Document or its subclasses:
- ✅ E31_1_Contract
- ✅ E31_2_Sales_Contract
- ✅ E31_5_Declaration
- ✅ E31_6_Correspondence
- ❌ E21_Person (wrong class)
- ❌ E53_Place (wrong class)

#### Range Constraint
Must point to E21_Person:
- ✅ Individual persons
- ❌ E74_Group (use different property)
- ❌ E39_Actor (too general, use E21_Person)

### Data Types

#### Accepted Input Formats

**Format 1: URI String**
```json
"gmn:P70_11_documents_referenced_person": ["person:123"]
```

**Format 2: Object with Type**
```json
"gmn:P70_11_documents_referenced_person": [
    {
        "@id": "person:123",
        "@type": "cidoc:E21_Person"
    }
]
```

**Format 3: Object with Properties**
```json
"gmn:P70_11_documents_referenced_person": [
    {
        "@id": "person:123",
        "@type": "cidoc:E21_Person",
        "rdfs:label": "Marco (neighbor)",
        "gmn:P1_1_has_name": "Marco Santini"
    }
]
```

**Format 4: Mixed Array**
```json
"gmn:P70_11_documents_referenced_person": [
    "person:123",
    {
        "@id": "person:456",
        "@type": "cidoc:E21_Person",
        "rdfs:label": "Giovanni"
    }
]
```

### Output Guarantee

After transformation, all persons will be objects with at minimum:
```json
{
    "@id": "person:123",
    "@type": "cidoc:E21_Person"
}
```

---

## Best Practices

### Data Entry Guidelines

#### 1. Identify Referenced Persons Consistently
```turtle
# Good: Clear identification of reference context
:person_marco a cidoc:E21_Person ;
    gmn:P1_1_has_name "Marco Santini" ;
    rdfs:label "Marco Santini (owner of adjacent property)" .

# Acceptable: Basic identification
:person_marco a cidoc:E21_Person ;
    gmn:P1_1_has_name "Marco Santini" .

# Poor: No context for why person is referenced
:person_marco a cidoc:E21_Person .
```

#### 2. Distinguish Status When Relevant
```turtle
# Good: Status indicated
:person_giovanni a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giovanni Rossi" ;
    rdfs:label "Giovanni Rossi (deceased father of seller)" .

# Also good: Date of death if known
:person_giovanni a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giovanni Rossi" ;
    rdfs:comment "Died before 1455, father of seller" .
```

#### 3. Create Unique Person Records
```turtle
# Good: One person record used consistently
:person_marco a cidoc:E21_Person ;
    gmn:P1_1_has_name "Marco Santini" .

:contract_001 gmn:P70_11_documents_referenced_person :person_marco .
:contract_002 gmn:P70_11_documents_referenced_person :person_marco .

# Poor: Duplicate records for same person
:contract_001 gmn:P70_11_documents_referenced_person :person_marco_1 .
:contract_002 gmn:P70_11_documents_referenced_person :person_marco_2 .
```

#### 4. Document the Reference Context
Use rdfs:comment to explain why the person is mentioned:

```turtle
:person_lorenzo a cidoc:E21_Person ;
    gmn:P1_1_has_name "Lorenzo Medici" ;
    rdfs:comment "Referenced as holder of water rights that are excepted from sale" .
```

### Query Patterns

#### Find All Persons Referenced in Documents
```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?document ?person ?name WHERE {
    ?document gmn:P70_11_documents_referenced_person ?person .
    OPTIONAL { ?person gmn:P1_1_has_name ?name . }
}
```

#### Find Documents Referencing Deceased Persons
```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?document ?person ?label WHERE {
    ?document gmn:P70_11_documents_referenced_person ?person .
    ?person rdfs:label ?label .
    FILTER(CONTAINS(LCASE(?label), "deceased") || CONTAINS(LCASE(?label), "late"))
}
```

#### Find Most Frequently Referenced Persons
```sparql
PREFIX gmn: <http://example.org/gmn/>

SELECT ?person (COUNT(?document) as ?ref_count) WHERE {
    ?document gmn:P70_11_documents_referenced_person ?person .
}
GROUP BY ?person
ORDER BY DESC(?ref_count)
```

### Validation Rules

#### Rule 1: Domain Check
```sparql
# Find invalid domain usage
SELECT ?subject WHERE {
    ?subject gmn:P70_11_documents_referenced_person ?person .
    FILTER NOT EXISTS { ?subject a cidoc:E31_Document }
}
```

#### Rule 2: Range Check
```sparql
# Find invalid range usage
SELECT ?person WHERE {
    ?doc gmn:P70_11_documents_referenced_person ?person .
    FILTER NOT EXISTS { ?person a cidoc:E21_Person }
}
```

#### Rule 3: Witness Misclassification
```sparql
# Find persons who might be misclassified as referenced when they're actually witnesses
SELECT ?doc ?person WHERE {
    ?doc gmn:P70_11_documents_referenced_person ?person .
    ?person rdfs:label ?label .
    FILTER(CONTAINS(LCASE(?label), "witness") || CONTAINS(LCASE(?label), "testified"))
}
```

### Performance Considerations

- Property transformation is O(n) where n = number of referenced persons
- No recursive processing required
- Minimal memory overhead
- Suitable for batch processing large datasets

### Interoperability

This property and its transformation are compatible with:
- ✅ Standard CIDOC-CRM queries
- ✅ SPARQL 1.1 endpoints
- ✅ RDF/XML serialization
- ✅ JSON-LD contexts
- ✅ Linked Open Data best practices

---

## Appendix: Full Property Definition

```turtle
@prefix gmn: <http://example.org/gmn/> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Property: P70.11 documents referenced person
gmn:P70_11_documents_referenced_person
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.11 documents referenced person"@en ;
    rdfs:comment """Simplified property for associating a sales contract with any person referenced or mentioned in the document text who does not have one of the specified transactional roles. This captures persons who appear in the contract narrative but are not parties to the acquisition: witnesses present at the signing, absent parties whose rights or claims are acknowledged, deceased persons whose estates or relationships are mentioned for context (e.g., 'Giovanni, son of the late Marco'), neighbors or adjacent property owners referenced in property descriptions, previous owners mentioned in provenance statements, or any other individuals named in the contract text. Unlike the other P70 properties which document participation in the E8_Acquisition event, this property represents a direct relationship between the document and the person: E31_Document > P67_refers_to > E21_Person. This acknowledges that the person is textually present in the document without implying their participation in the transaction itself."""@en ;
    rdfs:subPropertyOf cidoc:P67_refers_to ;
    rdfs:domain cidoc:E31_Document ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P67_refers_to .
```

---

**Document Version**: 1.0  
**Date**: October 2025  
**Authors**: GMN Ontology Development Team  
**Property**: gmn:P70_11_documents_referenced_person  
**Status**: Final
