# GMN P70.24 Indicates Declaring Party - Ontology Documentation

This document provides complete semantic documentation for the `gmn:P70_24_indicates_declarant` property, including its role in the GMN ontology, relationship to CIDOC-CRM, and usage patterns.

---

## Table of Contents

1. [Property Specification](#property-specification)
2. [Semantic Description](#semantic-description)
3. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
4. [Domain and Range](#domain-and-range)
5. [Relationship to Other Properties](#relationship-to-other-properties)
6. [Transformation Patterns](#transformation-patterns)
7. [Usage Examples](#usage-examples)
8. [Comparison with Similar Properties](#comparison-with-similar-properties)
9. [Implementation Notes](#implementation-notes)

---

## Property Specification

### Basic Information

**Property URI**: `gmn:P70_24_indicates_declarant`

**Property ID**: P70.24

**Label**: "P70.24 indicates declarant" (English)

**Alternative Labels**: 
- "indicates party issuing declaration"
- "has declarant"
- "documents declarant"

**Definition**: Simplified property for associating a declaration document with the person or entity making the declaration. The declarant is the party who is formally stating, acknowledging, or asserting something.

**Scope Note**: This property provides a shortcut for data entry when documenting declaration documents. It represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor. The E7_Activity should be typed as a declaration (AAT 300027623). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance.

---

## Semantic Description

### Purpose

The `gmn:P70_24_indicates_declarant` property serves to identify who is making a formal declaration, acknowledgment, or assertion documented in a legal instrument. It captures the active party responsible for the declaration act itself.

### Conceptual Model

```
Declaration Document  →  Declaration Activity  →  Declarant (Actor)
     (E31_5)              (E7, typed as AAT 300027623)    (E39)
```

The declarant is the person or organization who:
- Makes formal statements of fact
- Acknowledges debts or obligations
- Asserts rights or claims
- Recognizes legal relationships
- States intentions or positions

### Distinction from Related Roles

- **Declarant (P70.24)**: The party making the declaration (active role)
- **Receiving Party (P70.22)**: The party to whom the declaration is directed (passive role)
- **Declaration Subject (P70.25)**: What is being declared (object of the declaration)
- **Notary (P94i_1)**: The party creating the document (not necessarily the declarant)

---

## CIDOC-CRM Mapping

### Full Path Representation

**Shortcut Form**:
```turtle
<declaration> gmn:P70_24_indicates_declarant <person> .
```

**Expanded CIDOC-CRM Form**:
```turtle
<declaration> cidoc:P70_documents <declaration/activity> .

<declaration/activity> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <person> .

<person> a cidoc:E39_Actor .
```

### Path Components

1. **E31_Document** (Declaration): The document recording the declaration
2. **P70_documents**: Connects document to the activity it records
3. **E7_Activity** (Declaration): The act of making the declaration
4. **P2_has_type**: Types the activity as "declaration" (AAT 300027623)
5. **P14_carried_out_by**: Links activity to the actor performing it
6. **E39_Actor** (Declarant): The person or group making the declaration

### AAT Typing

**Activity Type**: AAT 300027623 - "declaration"

**AAT Definition**: "Written or oral statements made, as under oath before a notary public, by one who has knowledge of facts"

**URI**: `http://vocab.getty.edu/page/aat/300027623`

---

## Domain and Range

### Domain

**Class**: `gmn:E31_5_Declaration`

**Description**: Legal documents that contain formal statements, acknowledgments, or assertions made by one or more parties.

**Examples of E31_5 Documents**:
- Debt acknowledgments (confessio debiti)
- Property declarations
- Statements of fact
- Recognitions of obligations
- Assertions of rights

**Domain Constraint**: This property can ONLY be used with declaration documents. Using it with other document types (sales contracts, correspondence, etc.) violates the ontology constraints.

### Range

**Class**: `cidoc:E39_Actor`

**Description**: Persons or groups capable of deliberate action

**Includes**:
- `cidoc:E21_Person` - Individual human beings
- `cidoc:E74_Group` - Organizations, families, companies, etc.

**Range Constraint**: The declarant must be an actor capable of making intentional statements. Objects, places, or abstract concepts cannot be declarants.

### Cardinality

**Quantification**: Many to many (0,n:0,n)

- **Zero or more declarants per declaration**: A declaration may have no explicitly stated declarant (though unusual), one declarant, or multiple declarants (joint declarations)
- **Zero or more declarations per actor**: An actor can be the declarant in zero, one, or multiple declarations across different documents

---

## Relationship to Other Properties

### Declaration Document Properties

The complete set of properties for E31_5_Declaration:

| Property | Purpose | Range |
|----------|---------|-------|
| **P70.24 indicates declarant** | Who makes the declaration | E39_Actor |
| **P70.25 indicates declaration subject** | What is being declared | E1_CRM_Entity |
| **P70.22 indicates receiving party** | To whom it is directed (optional) | E39_Actor |

### Typical Usage Pattern

```turtle
<declaration> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <actor> ;       # Required: who declares
    gmn:P70_25_indicates_declaration_subject <object> ;  # Required: what is declared
    gmn:P70_22_indicates_receiving_party <recipient> .   # Optional: to whom
```

### Shared Activity Node

**Critical Implementation Detail**: P70.24 and P70.25 share the same E7_Activity node in the transformed output. The transformation functions must check for and reuse existing activities.

```turtle
# Both properties reference the same activity
<declaration> cidoc:P70_documents <declaration/activity> .

<declaration/activity> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <declarant> ;         # From P70.24
    cidoc:P16_used_specific_object <subject> .     # From P70.25
```

### Comparison with P14_carried_out_by

While P70.24 ultimately maps to P14_carried_out_by, there are important differences:

| Aspect | P70.24 | P14_carried_out_by |
|--------|--------|-------------------|
| **Application** | Document level (shortcut) | Activity level (canonical) |
| **Domain** | E31_5_Declaration | E7_Activity |
| **Implicit typing** | Creates typed E7_Activity | No implicit typing |
| **Convenience** | Simplified data entry | Full CRM compliance |
| **Transformation** | Removed during processing | Present in final output |

---

## Transformation Patterns

### Pattern 1: Single Declarant

**Input**:
```turtle
<declaration001> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <person_marco> .
```

**Output**:
```turtle
<declaration001> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <declaration001/declaration> .

<declaration001/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <person_marco> .
```

**JSON-LD Input**:
```json
{
    "@id": "http://example.org/declaration001",
    "@type": "gmn:E31_5_Declaration",
    "gmn:P70_24_indicates_declarant": ["http://example.org/person_marco"]
}
```

**JSON-LD Output**:
```json
{
    "@id": "http://example.org/declaration001",
    "@type": "gmn:E31_5_Declaration",
    "cidoc:P70_documents": [
        {
            "@id": "http://example.org/declaration001/declaration",
            "@type": "cidoc:E7_Activity",
            "cidoc:P2_has_type": {
                "@id": "http://vocab.getty.edu/page/aat/300027623",
                "@type": "cidoc:E55_Type"
            },
            "cidoc:P14_carried_out_by": [
                {
                    "@id": "http://example.org/person_marco",
                    "@type": "cidoc:E39_Actor"
                }
            ]
        }
    ]
}
```

### Pattern 2: Multiple Declarants (Joint Declaration)

**Input**:
```turtle
<declaration002> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <brother_antonio> ,
                                   <brother_giovanni> ,
                                   <brother_francesco> .
```

**Output**:
```turtle
<declaration002> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <declaration002/declaration> .

<declaration002/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <brother_antonio> ,
                             <brother_giovanni> ,
                             <brother_francesco> .
```

**Notes**: 
- All declarants are added to the same activity
- Each gets a separate P14_carried_out_by statement
- Order is preserved from input

### Pattern 3: Integration with Declaration Subject

**Input**:
```turtle
<declaration003> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <debtor_lucia> ;
    gmn:P70_25_indicates_declaration_subject <debt_300_lire> .
```

**Output**:
```turtle
<declaration003> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <declaration003/declaration> .

<declaration003/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <debtor_lucia> ;
    cidoc:P16_used_specific_object <debt_300_lire> .
```

**Critical**: Both properties contribute to the SAME activity node.

### Pattern 4: Complete Declaration with Metadata

**Input**:
```turtle
<declaration004> a gmn:E31_5_Declaration ;
    gmn:P1_1_has_name "Declaration of inheritance rights" ;
    gmn:P70_24_indicates_declarant <heir_margherita> ;
    gmn:P70_25_indicates_declaration_subject <estate_vineyard> ;
    gmn:P70_22_indicates_receiving_party <court_official> ;
    gmn:P94i_1_was_created_by <notary_domenico> ;
    gmn:P94i_2_has_enactment_date "1448-09-12"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <genoa_city> .
```

**Output**:
```turtle
<declaration004> a gmn:E31_5_Declaration ;
    cidoc:P1_is_identified_by <declaration004/appellation> ;
    cidoc:P70_documents <declaration004/declaration> ;
    cidoc:P94i_was_created_by <declaration004/creation> .

<declaration004/appellation> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Declaration of inheritance rights" .

<declaration004/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <heir_margherita> ;
    cidoc:P16_used_specific_object <estate_vineyard> ;
    cidoc:P01_has_domain <court_official> .

<declaration004/creation> a cidoc:E65_Creation ;
    cidoc:P14_carried_out_by <notary_domenico> ;
    cidoc:P4_has_time-span <declaration004/creation/timespan> ;
    cidoc:P7_took_place_at <genoa_city> .

<declaration004/creation/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1448-09-12"^^xsd:date .
```

**Notes**:
- Declaration activity is separate from creation activity
- Declarant (P70.24 → P14) ≠ Notary (P94i_1 → P14 on different activity)
- Declaration activity documents the substance; creation documents the document-making

---

## Usage Examples

### Example 1: Simple Debt Acknowledgment

**Scenario**: A merchant acknowledges a debt owed to another merchant.

**Input**:
```turtle
<debt_decl_01> a gmn:E31_5_Declaration ;
    gmn:P1_1_has_name "Marco's acknowledgment of debt to Giovanni" ;
    gmn:P70_24_indicates_declarant <merchant_marco> ;
    gmn:P70_25_indicates_declaration_subject <debt_500_lire_to_giovanni> ;
    gmn:P94i_2_has_enactment_date "1445-03-20"^^xsd:date .
```

**Context**: Marco is publicly acknowledging he owes Giovanni 500 lire, creating a formal record of the debt.

### Example 2: Property Rights Declaration

**Scenario**: A widow declares her ownership of a property inherited from her late husband.

**Input**:
```turtle
<property_decl_02> a gmn:E31_5_Declaration ;
    gmn:P1_1_has_name "Lucia's declaration of property rights" ;
    gmn:P70_24_indicates_declarant <widow_lucia> ;
    gmn:P70_25_indicates_declaration_subject <house_via_tommaso> ;
    gmn:P70_22_indicates_receiving_party <city_magistrate> .
```

**Context**: Lucia is formally stating her ownership claim to the authorities.

### Example 3: Joint Declaration by Business Partners

**Scenario**: Three business partners jointly declare their shares in a commercial venture.

**Input**:
```turtle
<business_decl_03> a gmn:E31_5_Declaration ;
    gmn:P1_1_has_name "Partnership declaration for spice trade" ;
    gmn:P70_24_indicates_declarant <partner_antonio> ,
                                   <partner_battista> ,
                                   <partner_carlo> ;
    gmn:P70_25_indicates_declaration_subject <partnership_shares> .
```

**Context**: All three partners are making a joint statement about their business arrangement.

### Example 4: Obligation Recognition

**Scenario**: An heir declares acceptance of obligations attached to an inheritance.

**Input**:
```turtle
<obligation_decl_04> a gmn:E31_5_Declaration ;
    gmn:P1_1_has_name "Francesco's acceptance of estate obligations" ;
    gmn:P70_24_indicates_declarant <heir_francesco> ;
    gmn:P70_25_indicates_declaration_subject <estate_debts_and_duties> ;
    gmn:P94i_1_was_created_by <notary_pietro> ;
    gmn:P94i_3_has_place_of_enactment <genoa_palazzo_san_giorgio> .
```

**Context**: Francesco is formally accepting the liabilities that come with his inheritance.

### Example 5: Declaration with Rich Actor Data

**Scenario**: A declaration where the declarant has detailed biographical information.

**Input**:
```turtle
<detailed_decl_05> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <person_margherita_001> ;
    gmn:P70_25_indicates_declaration_subject <vineyard_levanto> .

<person_margherita_001> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <margherita_name> ;
    gmn:P1_1_has_name "Margherita" ;
    gmn:P1_3_has_patrilineal_name "Spinola" .
```

**Output** (declarant detail preserved):
```turtle
<detailed_decl_05> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <detailed_decl_05/declaration> .

<detailed_decl_05/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <person_margherita_001> ;
    cidoc:P16_used_specific_object <vineyard_levanto> .

<person_margherita_001> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <margherita_name> ;
    # ... other properties preserved
```

---

## Comparison with Similar Properties

### Across Document Types

Different document types use different properties for similar roles:

| Document Type | Property for "Active Party" | CIDOC Path |
|--------------|----------------------------|------------|
| Sales Contract | P70.1 documents seller | E8 > P23 transferred_title_from |
| Declaration | **P70.24 indicates declarant** | **E7 > P14 carried_out_by** |
| Cession | P70.21 indicates conceding party | E7 > P14 carried_out_by |
| Donation | P70.32 indicates donor | E8 > P23 transferred_title_from |
| Correspondence | P70.26 indicates sender | E7 > P14 carried_out_by |
| Arbitration | P70.18 documents disputing party | E7 > P14 carried_out_by |

### Why Different Properties?

Each document type has semantically distinct roles:
- **Declarant**: Makes a formal statement (unilateral action)
- **Seller/Buyer**: Transfer property (bilateral transaction)
- **Sender/Recipient**: Communicate (directed exchange)
- **Disputing parties**: Disagree (conflictual relationship)

While they may map to the same CIDOC-CRM properties (P14, P23, etc.), the distinct GMN properties capture the specific semantic context of each document type.

### Activity Type Comparison

| Document Type | Activity Type | AAT URI |
|--------------|---------------|---------|
| Declaration | declaration | 300027623 |
| Sales | acquisition | (default E8) |
| Correspondence | correspondence | 300026877 |
| Arbitration | arbitration agreement | 300417271 |
| Cession | transfer of rights | 300417639 |

---

## Implementation Notes

### 1. Activity URI Generation

The activity URI follows the pattern:
```
{document_uri}/declaration
```

Example:
- Document: `http://example.org/doc123`
- Activity: `http://example.org/doc123/declaration`

This pattern:
- Ensures uniqueness
- Makes the relationship clear
- Follows GMN conventions
- Enables easy querying

### 2. Activity Reuse Logic

The transformation function checks for existing activities:

```python
if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
    # Create new activity
    data['cidoc:P70_documents'] = [{ ... }]
else:
    # Reuse existing activity
    activity = data['cidoc:P70_documents'][0]
```

This ensures that P70.24 and P70.25 share the same activity node.

### 3. List Handling

Declarants are always processed as a list, even if only one:

```python
declarants = data['gmn:P70_24_indicates_declarant']  # Always a list
for declarant_obj in declarants:
    # Process each declarant
```

### 4. Type Assignment

Each declarant is explicitly typed as E39_Actor if not already typed:

```python
if '@type' not in declarant_data:
    declarant_data['@type'] = 'cidoc:E39_Actor'
```

### 5. Order Independence

The transformation is order-independent:
- P70.24 can be processed before or after P70.25
- Both will correctly reference/create the same activity
- The activity will have both P14 and P16 properties

### 6. Shortcut Removal

The shortcut property is always removed after transformation:

```python
del data['gmn:P70_24_indicates_declarant']
```

This ensures the output contains only CIDOC-CRM compliant structures.

### 7. Error Handling

The function gracefully handles edge cases:
- Missing property: Returns data unchanged
- Empty list: Creates activity but no P14 statements
- Malformed data: Attempts to process, may require validation

### 8. Integration Points

This property integrates with:
- **P70.25** (declaration subject): Shares activity
- **P70.22** (receiving party): Can co-occur, uses P01_has_domain
- **P94i_1** (notary): Different activity (creation vs. declaration)
- **P1** (naming): Can name both document and actors

---

## Validation Rules

### Ontology-Level Validation

1. **Domain constraint**: Property can only be used with E31_5_Declaration
2. **Range constraint**: Value must be E39_Actor or subclass
3. **Cardinality**: 0 to n (optional, but can have multiple)

### Transformation Validation

1. **Activity creation**: Must create E7_Activity with correct URI
2. **Activity typing**: Activity must have type AAT 300027623
3. **Actor linking**: Each declarant must be linked via P14
4. **Shortcut removal**: gmn:P70_24 must not appear in output
5. **Activity sharing**: Must reuse existing activity if present

### Data Quality Checks

1. **Non-empty declarants**: Warning if declarant list is empty
2. **Valid actor URIs**: Declarant URIs should resolve to actors
3. **Consistent types**: If typed, should be E39_Actor or subclass
4. **No duplicates**: Same actor shouldn't appear multiple times (warning)

---

## SPARQL Queries

### Query 1: Find all declarations and their declarants

```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declaration ?declarant ?name
WHERE {
    ?declaration a gmn:E31_5_Declaration ;
                 cidoc:P70_documents ?activity .
    ?activity cidoc:P14_carried_out_by ?declarant .
    
    OPTIONAL {
        ?declarant cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
    }
}
```

### Query 2: Find joint declarations (multiple declarants)

```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declaration (COUNT(DISTINCT ?declarant) as ?declarant_count)
WHERE {
    ?declaration a gmn:E31_5_Declaration ;
                 cidoc:P70_documents ?activity .
    ?activity cidoc:P14_carried_out_by ?declarant .
}
GROUP BY ?declaration
HAVING (COUNT(DISTINCT ?declarant) > 1)
```

### Query 3: Find declarations by a specific person

```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declaration ?subject
WHERE {
    ?declaration a gmn:E31_5_Declaration ;
                 cidoc:P70_documents ?activity .
    ?activity cidoc:P14_carried_out_by <http://example.org/person_marco> ;
              cidoc:P16_used_specific_object ?subject .
}
```

### Query 4: Find most active declarants

```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declarant (COUNT(?declaration) as ?count)
WHERE {
    ?declaration a gmn:E31_5_Declaration ;
                 cidoc:P70_documents ?activity .
    ?activity cidoc:P14_carried_out_by ?declarant .
}
GROUP BY ?declarant
ORDER BY DESC(?count)
LIMIT 10
```

---

## Conclusion

The `gmn:P70_24_indicates_declarant` property provides an essential shortcut for documenting declaration documents in the GMN ontology. By clearly identifying who makes formal statements, acknowledgments, or assertions, it enables rich modeling of legal declarations while maintaining compatibility with CIDOC-CRM through systematic transformation.

Key takeaways:
- **Semantic clarity**: Distinct from other document roles
- **CIDOC-CRM compliance**: Maps to standard P14_carried_out_by
- **Activity sharing**: Integrates with P70.25 on same activity
- **Flexible cardinality**: Supports both individual and joint declarations
- **Systematic transformation**: Automated conversion to CRM structures

---

**Documentation Version**: 1.0  
**Last Updated**: October 2025  
**Ontology Version**: GMN 2.0  
**CIDOC-CRM Version**: 7.1.1
