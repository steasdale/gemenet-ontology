# E31.5 Declaration - Ontology Documentation

## Table of Contents
1. [Class Definition](#class-definition)
2. [Property Specifications](#property-specifications)
3. [Semantic Structure](#semantic-structure)
4. [Transformation Patterns](#transformation-patterns)
5. [Examples](#examples)
6. [Comparison with Other Document Types](#comparison-with-other-document-types)
7. [AAT References](#aat-references)

---

## Class Definition

### gmn:E31_5_Declaration

**Label**: E31.5 Declaration

**Subclass of**: cidoc:E31_Document

**Definition**: Specialized class that describes declaration documents. This is a specialized type of cidoc:E31_Document used to represent legal documents where one party (the declarant) makes a formal statement, acknowledgment, or assertion to another party (the recipient) regarding a specific subject matter.

**Scope**: Declarations can be either notarial documents (recorded by a notary) or governmental documents (issued by official authorities without notarial involvement). Common types include:
- Declarations of debt
- Acknowledgments of obligations
- Statements of fact
- Official pronouncements
- Formal notifications
- Governmental decrees

**Key Characteristics**:
- **Unilateral**: Unlike contracts involving bilateral agreements, declarations are typically unilateral statements
- **Legal Effect**: Though unilateral, declarations have legal effect and may create or acknowledge obligations
- **Variable Recording**: Some declarations may be recorded in notarial registers alongside contracts, while others exist as independent governmental or administrative documents
- **Document vs. Activity**: Instances of this class represent the physical or conceptual document itself, while the actual declaration activity and its effects are modeled through E7_Activity that the document documents (via P70_documents)

**Distinction from E31_1_Contract**: E31_5_Declaration is a direct subclass of E31_Document rather than E31_1_Contract because:
- Not all declarations are contractual in nature
- Some are governmental documents without notarial participation
- They represent unilateral statements rather than agreements between parties

---

## Property Specifications

### gmn:P70_24_indicates_declarant

**Label**: P70.24 indicates declarant

**Domain**: gmn:E31_5_Declaration

**Range**: cidoc:E39_Actor

**Subproperty of**: cidoc:P70_documents

**Definition**: Simplified property for associating a declaration document with the person or entity making the declaration. The declarant is the party who is formally stating, acknowledging, or asserting something.

**CIDOC-CRM Path**: E31_Document → P70_documents → E7_Activity → P14_carried_out_by → E39_Actor

**Transformation**: The E7_Activity should be typed as a declaration (AAT 300027623).

**Usage**: This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance.

**Examples**:
- A merchant declaring a debt owed
- A government official making a proclamation
- An individual asserting a claim to property
- A notary recording a formal acknowledgment

---

### gmn:P70_22_indicates_receiving_party (updated for declarations)

**Label**: P70.22 indicates receiving party

**Domain**: owl:unionOf (gmn:E31_4_Cession_of_Rights_Contract, gmn:E31_5_Declaration)

**Range**: cidoc:E39_Actor

**Subproperty of**: cidoc:P70_documents

**Definition**: Simplified property for associating a document with the person or entity receiving something in the documented activity. In cession of rights contracts, this is the party receiving the ceded rights. In declarations, this is the party to whom the declaration is addressed or directed.

**CIDOC-CRM Path (for declarations)**: E31_Document → P70_documents → E7_Activity → P01_has_domain → E39_Actor (using the inverse P01i_is_domain_of)

**CIDOC-CRM Path (for cessions)**: E31_Document → P70_documents → E7_Activity → P14_carried_out_by → E39_Actor

**Transformation**: The transformation logic detects the document type:
- For E31_5_Declaration: Uses P01_has_domain (recipient is in the domain of the declaration)
- For E31_4_Cession_of_Rights_Contract: Uses P14_carried_out_by (both parties carry out the cession)

**Usage**: This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance.

**Semantic Rationale**: 
- P01_has_domain is appropriate for declarations because it indicates "the domain of validity" or "who is concerned by" the activity
- The recipient is the person or entity to whom the declaration applies or is directed
- Unlike cessions where both parties actively participate, declarations are directed at the recipient

---

### gmn:P70_25_indicates_declaration_subject

**Label**: P70.25 indicates declaration subject

**Domain**: gmn:E31_5_Declaration

**Range**: cidoc:E1_CRM_Entity

**Subproperty of**: cidoc:P70_documents

**Definition**: Simplified property for associating a declaration document with the subject matter being declared, acknowledged, or asserted. This can include debts being acknowledged, facts being stated, obligations being recognized, properties being claimed, rights being asserted, or any other matter that is the content of the declaration.

**CIDOC-CRM Path**: E31_Document → P70_documents → E7_Activity → P16_used_specific_object → E1_CRM_Entity

**Transformation**: The E7_Activity should be typed as a declaration (AAT 300027623).

**Usage**: This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance.

**Examples of Declaration Subjects**:
- A specific debt (E97_Monetary_Amount or conceptual entity representing the debt)
- A legal right or claim (E72_Legal_Object)
- A fact or circumstance (E73_Information_Object)
- A property or object (E18_Physical_Thing)
- A policy or regulation (E73_Information_Object)
- An obligation or duty (conceptual entity)

---

## Semantic Structure

### Complete Pattern

```
E31_5_Declaration (the declaration document)
  │
  ├─ P70_documents
  │   └─ E7_Activity (the declaration activity)
  │       ├─ P2_has_type → E55_Type (AAT 300027623: declarations)
  │       ├─ P14_carried_out_by → E39_Actor (declarant)
  │       ├─ P01_has_domain → E39_Actor (recipient)
  │       └─ P16_used_specific_object → E1_CRM_Entity (declaration subject)
  │
  └─ P94i_was_created_by (optional, for notarially recorded declarations)
      └─ E65_Creation
          ├─ P4_has_time-span → E52_Time-Span
          ├─ P7_took_place_at → E53_Place
          └─ P14_carried_out_by → E21_Person (notary, if applicable)
```

### Shared Activity Pattern

All three declaration properties (P70.24, P70.22, P70.25) share the same E7_Activity node:
- If an activity already exists when a property is processed, it is reused
- If no activity exists, it is created with proper AAT typing
- This ensures all aspects of the declaration are connected to a single activity

### Activity Typing

The E7_Activity representing the declaration is automatically typed using:
- **Property**: P2_has_type
- **Value**: AAT 300027623 (declarations)
- **Type Class**: E55_Type

---

## Transformation Patterns

### Pattern 1: Simple Debt Declaration

**Input (Simplified Format)**:
```turtle
<declaration001> a gmn:E31_5_Declaration ;
    gmn:P102_1_has_title "Declaration of Debt" ;
    gmn:P70_24_indicates_declarant <merchant_giovanni> ;
    gmn:P70_22_indicates_receiving_party <merchant_paolo> ;
    gmn:P70_25_indicates_declaration_subject <debt_500_lire> ;
    gmn:P94i_2_has_enactment_date "1450-03-15"^^xsd:date ;
    gmn:P94i_1_was_created_by <notary_antonio> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<declaration001> a gmn:E31_5_Declaration ;
    cidoc:P102_has_title "Declaration of Debt" ;
    cidoc:P70_documents <declaration001/declaration> ;
    cidoc:P94i_was_created_by <declaration001/creation> .

<declaration001/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <merchant_giovanni> ;
    cidoc:P01_has_domain <merchant_paolo> ;
    cidoc:P16_used_specific_object <debt_500_lire> .

<declaration001/creation> a cidoc:E65_Creation ;
    cidoc:P4_has_time-span <declaration001/timespan> ;
    cidoc:P14_carried_out_by <notary_antonio> .

<declaration001/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1450-03-15"^^xsd:date .

<http://vocab.getty.edu/page/aat/300027623> a cidoc:E55_Type ;
    rdfs:label "declarations"@en .

<merchant_giovanni> a cidoc:E39_Actor .
<merchant_paolo> a cidoc:E39_Actor .
<debt_500_lire> a cidoc:E1_CRM_Entity .
<notary_antonio> a cidoc:E21_Person .
```

---

### Pattern 2: Governmental Declaration

**Input (Simplified Format)**:
```turtle
<declaration002> a gmn:E31_5_Declaration ;
    gmn:P102_1_has_title "Tax Exemption Decree" ;
    gmn:P70_24_indicates_declarant <doge_office> ;
    gmn:P70_22_indicates_receiving_party <genoa_merchant_guild> ;
    gmn:P70_25_indicates_declaration_subject <tax_exemption_policy> ;
    gmn:P94i_2_has_enactment_date "1450-06-15"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <palazzo_ducale> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<declaration002> a gmn:E31_5_Declaration ;
    cidoc:P102_has_title "Tax Exemption Decree" ;
    cidoc:P70_documents <declaration002/declaration> ;
    cidoc:P94i_was_created_by <declaration002/creation> .

<declaration002/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <doge_office> ;
    cidoc:P01_has_domain <genoa_merchant_guild> ;
    cidoc:P16_used_specific_object <tax_exemption_policy> .

<declaration002/creation> a cidoc:E65_Creation ;
    cidoc:P4_has_time-span <declaration002/timespan> ;
    cidoc:P7_took_place_at <palazzo_ducale> .

<declaration002/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1450-06-15"^^xsd:date .

<doge_office> a cidoc:E74_Group .
<genoa_merchant_guild> a cidoc:E74_Group .
<tax_exemption_policy> a cidoc:E73_Information_Object .
<palazzo_ducale> a cidoc:E53_Place .
```

**Note**: This governmental declaration has no notary (P94i_1_was_created_by property for notary is omitted), demonstrating that declarations can exist without notarial involvement.

---

### Pattern 3: Property Claim Declaration

**Input (Simplified Format)**:
```turtle
<declaration003> a gmn:E31_5_Declaration ;
    gmn:P102_1_has_title "Declaration of Property Ownership" ;
    gmn:P70_24_indicates_declarant <landowner_marco> ;
    gmn:P70_22_indicates_receiving_party <city_council> ;
    gmn:P70_25_indicates_declaration_subject <vineyard_property> ;
    gmn:P94i_2_has_enactment_date "1451-09-20"^^xsd:date .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<declaration003> a gmn:E31_5_Declaration ;
    cidoc:P102_has_title "Declaration of Property Ownership" ;
    cidoc:P70_documents <declaration003/declaration> ;
    cidoc:P94i_was_created_by <declaration003/creation> .

<declaration003/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <landowner_marco> ;
    cidoc:P01_has_domain <city_council> ;
    cidoc:P16_used_specific_object <vineyard_property> .

<declaration003/creation> a cidoc:E65_Creation ;
    cidoc:P4_has_time-span <declaration003/timespan> .

<declaration003/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1451-09-20"^^xsd:date .

<landowner_marco> a cidoc:E21_Person .
<city_council> a cidoc:E74_Group .
<vineyard_property> a cidoc:E18_Physical_Thing .
```

---

## Examples

### Example 1: Merchant's Debt Acknowledgment

**Context**: A merchant formally acknowledges a debt to another merchant in front of a notary.

**Simplified Entry**:
```json
{
  "@id": "https://gmn.org/declaration/debt_1450_03_15",
  "@type": "gmn:E31_5_Declaration",
  "gmn:P102_1_has_title": "Declaration of Debt: Giovanni Rossi to Paolo Bianchi",
  "gmn:P70_24_indicates_declarant": {
    "@id": "https://gmn.org/person/giovanni_rossi",
    "@type": "cidoc:E21_Person"
  },
  "gmn:P70_22_indicates_receiving_party": {
    "@id": "https://gmn.org/person/paolo_bianchi",
    "@type": "cidoc:E21_Person"
  },
  "gmn:P70_25_indicates_declaration_subject": {
    "@id": "https://gmn.org/legal_object/inheritance_estate_visconti",
    "@type": "cidoc:E72_Legal_Object"
  },
  "gmn:P94i_1_was_created_by": {
    "@id": "https://gmn.org/person/notary_francesco"
  },
  "gmn:P94i_2_has_enactment_date": "1451-01-10"
}
```

---

## Comparison with Other Document Types

### Structural Comparison

| Aspect | Sales Contract | Arbitration | Cession | Declaration |
|--------|---------------|-------------|---------|-------------|
| **Central Event** | E8_Acquisition | E7_Activity | E7_Activity | E7_Activity |
| **Event Type** | Purchase/sale | Arbitration (AAT 300054754) | Transfer of rights (AAT 300417639) | Declaration (AAT 300027623) |
| **Main Actors** | P23 (seller) + P22 (buyer) | P14 (all parties + arbitrators) | P14 (both parties) | P14 (declarant) + P01 (recipient) |
| **Receiving Party** | P22_transferred_title_to | N/A | P14_carried_out_by (via P70.22) | P01_has_domain (via P70.22) |
| **Object/Subject** | P24 (property transferred) | P16 (dispute subject) | P16 (legal object/rights) | P16 (declaration subject) |
| **Nature** | Bilateral transfer | Multi-party agreement | Bilateral transfer of rights | Unilateral statement |
| **Subclass of** | E31_1_Contract | E31_1_Contract | E31_1_Contract | E31_Document |
| **Notary Required** | Yes (in GMN corpus) | Yes (in GMN corpus) | Yes (in GMN corpus) | Optional |

### Semantic Differences

**Sales Contract (E31_2)**:
- Models actual transfer of ownership
- Uses E8_Acquisition as central event
- Involves monetary transaction
- Always bilateral with consideration

**Arbitration Agreement (E31_3)**:
- Models resolution of disputes
- Multiple parties can be involved
- Arbitrators are neutral third parties
- Results in binding decision

**Cession of Rights Contract (E31_4)**:
- Models transfer of legal rights (not physical objects)
- Both parties actively participate in cession
- Uses E7_Activity (not E8_Acquisition)
- Bilateral agreement

**Declaration (E31_5)**:
- Models unilateral statements with legal effect
- Recipient is in the domain of the declaration, not an active participant
- Can be notarial or governmental
- Does not necessarily involve transfer or agreement
- Uses E7_Activity with P01_has_domain for recipient

### Property P70.22 Usage Across Document Types

| Document Type | P70.22 Transforms To | Semantic Meaning | Activity Type |
|---------------|---------------------|------------------|---------------|
| E31_4_Cession_of_Rights_Contract | P14_carried_out_by | Both parties actively carry out the cession | Transfer of rights |
| E31_5_Declaration | P01_has_domain | Recipient is in the domain/scope of the declaration | Declaration |

This dual usage is appropriate because:
- **In cessions**: Both parties are active participants in the transfer of rights
- **In declarations**: The recipient is passive - they are the target or addressee of the declaration

---

## AAT References

### Primary Concept

**AAT 300027623: declarations (reports)**
- URI: http://vocab.getty.edu/page/aat/300027623
- Definition: "Formal or explicit statements, proclamations, or announcements"
- Hierarchy: 
  - Objects Facet
  - Visual and Verbal Communication
  - Information Forms
  - reports (documents)
  - declarations

### Related AAT Concepts

**AAT 300027590: proclamations**
- Official public announcements
- Subset of declarations
- Often governmental

**AAT 300026906: acknowledgments**
- Formal recognition or admission
- Type of declaration

**AAT 300027267: statements (documents)**
- Broader term for formal declarations
- Can include various types of assertions

---

## Implementation Notes

### 1. Shared Activity Pattern

All three declaration properties (P70.24, P70.22, P70.25) must share the same E7_Activity node. The transformation functions achieve this by:

```python
# Check if activity already exists
if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
    existing_activity = data['cidoc:P70_documents'][0]
else:
    # Create new activity
    existing_activity = {...}
    data['cidoc:P70_documents'] = [existing_activity]
```

### 2. Activity Typing

The E7_Activity is automatically typed using AAT 300027623:

```python
'cidoc:P2_has_type': {
    '@id': AAT_DECLARATION,
    '@type': 'cidoc:E55_Type'
}
```

### 3. Property Order Dependency

**CRITICAL**: In the transformation script, P70.22 must be called AFTER P70.24 (and P70.21 for cessions) so the activity type is already set when determining which CIDOC-CRM property to use.

Correct order in `transform_item()`:
```python
item = transform_p70_21_indicates_conceding_party(item)  # Cessions
item = transform_p70_24_indicates_declarant(item)        # Declarations
item = transform_p70_22_indicates_receiving_party(item)  # Both - detects type
item = transform_p70_23_indicates_object_of_cession(item)
item = transform_p70_25_indicates_declaration_subject(item)
```

### 4. Document Type Detection

The `transform_p70_22_indicates_receiving_party()` function detects document type:

```python
if '@type' in data:
    types = data['@type'] if isinstance(data['@type'], list) else [data['@type']]
    is_declaration = 'gmn:E31_5_Declaration' in types
    is_cession = 'gmn:E31_4_Cession_of_Rights_Contract' in types

# Use appropriate property based on document type
property_key = 'cidoc:P01_has_domain' if is_declaration else 'cidoc:P14_carried_out_by'
```

### 5. Handling Optional Notary

Unlike other contract types, declarations may or may not have notarial involvement:

**With Notary** (use P94i_1_was_created_by):
```turtle
<declaration001> gmn:P94i_1_was_created_by <notary_antonio> .
```

**Without Notary** (omit P94i_1_was_created_by):
```turtle
<declaration002> gmn:P94i_2_has_enactment_date "1450-06-15"^^xsd:date .
```

Both are valid declaration documents.

### 6. Declaration Subject Types

The subject of a declaration (P70.25) can be any E1_CRM_Entity:

- **E97_Monetary_Amount**: For debt declarations
- **E72_Legal_Object**: For rights or claims
- **E73_Information_Object**: For policies or facts
- **E18_Physical_Thing**: For property claims
- **Custom Conceptual Entities**: For obligations, duties, etc.

Choose the most specific CIDOC-CRM class available for the subject matter.

---

## Use Cases and Examples

### Use Case 1: Debt Acknowledgment

**Scenario**: A merchant acknowledges owing 500 lire to another merchant, recorded by notary.

**Properties Used**:
- P70.24: merchant who owes the debt (declarant)
- P70.22: merchant to whom debt is owed (recipient)
- P70.25: the debt itself (subject)
- P94i_1: notary who recorded the declaration
- P94i_2: date of declaration

**Legal Effect**: Creates evidence of the debt obligation.

---

### Use Case 2: Tax Exemption Decree

**Scenario**: Government issues decree exempting certain merchants from taxes.

**Properties Used**:
- P70.24: government office (declarant)
- P70.22: merchants or guild (recipient)
- P70.25: tax policy or exemption (subject)
- P94i_2: date of decree
- P94i_3: place of issuance

**Legal Effect**: Establishes tax exemption for specified parties.

**Note**: No notary involved (governmental document).

---

### Use Case 3: Property Ownership Claim

**Scenario**: Individual declares ownership of land before authorities.

**Properties Used**:
- P70.24: property claimant (declarant)
- P70.22: city council or court (recipient)
- P70.25: the property claimed (subject)
- P94i_2: date of declaration

**Legal Effect**: Establishes claim to property for legal purposes.

---

### Use Case 4: Official Notification

**Scenario**: One party formally notifies another of a fact or circumstance.

**Properties Used**:
- P70.24: party making notification (declarant)
- P70.22: party being notified (recipient)
- P70.25: fact or circumstance (subject)
- P94i_1: notary (if notarially recorded)

**Legal Effect**: Creates legal record of notification.

---

## Query Examples

### SPARQL Query 1: Find All Declarations by a Person

```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declaration ?title ?date ?recipient ?subject
WHERE {
  ?declaration a gmn:E31_5_Declaration ;
               cidoc:P70_documents ?activity .
  
  ?activity cidoc:P14_carried_out_by <https://gmn.org/person/giovanni_rossi> ;
            cidoc:P01_has_domain ?recipient ;
            cidoc:P16_used_specific_object ?subject .
  
  OPTIONAL { ?declaration cidoc:P102_has_title ?title }
  OPTIONAL { 
    ?declaration cidoc:P94i_was_created_by/cidoc:P4_has_time-span/cidoc:P82_at_some_time_within ?date 
  }
}
```

### SPARQL Query 2: Find Governmental Declarations (No Notary)

```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declaration ?title ?declarant
WHERE {
  ?declaration a gmn:E31_5_Declaration ;
               cidoc:P70_documents ?activity .
  
  ?activity cidoc:P14_carried_out_by ?declarant .
  
  # No notary involvement
  FILTER NOT EXISTS { 
    ?declaration cidoc:P94i_was_created_by ?creation .
    ?creation cidoc:P14_carried_out_by ?notary .
  }
  
  OPTIONAL { ?declaration cidoc:P102_has_title ?title }
}
```

### SPARQL Query 3: Find Declarations About Specific Subject

```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?declaration ?declarant ?recipient ?date
WHERE {
  ?declaration a gmn:E31_5_Declaration ;
               cidoc:P70_documents ?activity .
  
  ?activity cidoc:P14_carried_out_by ?declarant ;
            cidoc:P01_has_domain ?recipient ;
            cidoc:P16_used_specific_object <https://gmn.org/debt/500_lire_1450> .
  
  OPTIONAL { 
    ?declaration cidoc:P94i_was_created_by/cidoc:P4_has_time-span/cidoc:P82_at_some_time_within ?date 
  }
}
```

---

## Validation Checklist

When implementing or reviewing declarations, verify:

- [ ] Class is gmn:E31_5_Declaration (not E31_1_Contract)
- [ ] All three properties share same E7_Activity
- [ ] Activity is typed as AAT 300027623
- [ ] P70.24 (declarant) uses P14_carried_out_by
- [ ] P70.22 (recipient) uses P01_has_domain
- [ ] P70.25 (subject) uses P16_used_specific_object
- [ ] Notary (P94i_1) is optional, not required
- [ ] Date (P94i_2) uses P82_at_some_time_within
- [ ] All actors are E39_Actor subclasses
- [ ] Subject is appropriate E1_CRM_Entity subclass

---

## Related Documentation

- **CIDOC-CRM Specification**: http://www.cidoc-crm.org/
- **Getty AAT**: http://vocab.getty.edu/
- **GMN Ontology Main Documentation**: See gmn_ontology.ttl
- **Cession Documentation**: See documentation for E31_4 (shares P70.22)
- **Sales Contract Documentation**: See documentation for E31_2
- **Transformation Script**: See gmn_to_cidoc_transform_script.py

---

## Version History

- **v1.0** (2025-10-25): Initial creation of E31_5_Declaration class
  - Added P70.24_indicates_declarant
  - Added P70.25_indicates_declaration_subject
  - Updated P70.22_indicates_receiving_party for dual use
  - Created transformation functions for all properties": {
    "@id": "https://gmn.org/debt/500_lire_1450",
    "@type": "cidoc:E97_Monetary_Amount"
  },
  "gmn:P94i_1_was_created_by": {
    "@id": "https://gmn.org/person/notary_antonio"
  },
  "gmn:P94i_2_has_enactment_date": "1450-03-15",
  "gmn:P94i_3_has_place_of_enactment": {
    "@id": "https://gmn.org/place/genoa_notary_office"
  }
}
```

---

### Example 2: Official Proclamation

**Context**: The Doge's office issues an official declaration exempting certain merchants from taxes.

**Simplified Entry**:
```json
{
  "@id": "https://gmn.org/declaration/tax_exemption_1450_06_15",
  "@type": "gmn:E31_5_Declaration",
  "gmn:P102_1_has_title": "Declaration of Tax Exemption for Silk Merchants",
  "gmn:P70_24_indicates_declarant": {
    "@id": "https://gmn.org/org/doge_office",
    "@type": "cidoc:E74_Group"
  },
  "gmn:P70_22_indicates_receiving_party": {
    "@id": "https://gmn.org/group/silk_merchant_guild",
    "@type": "cidoc:E74_Group"
  },
  "gmn:P70_25_indicates_declaration_subject": {
    "@id": "https://gmn.org/policy/silk_tax_exemption_1450",
    "@type": "cidoc:E73_Information_Object"
  },
  "gmn:P94i_2_has_enactment_date": "1450-06-15",
  "gmn:P94i_3_has_place_of_enactment": {
    "@id": "https://gmn.org/place/palazzo_ducale"
  }
}
```

---

### Example 3: Right to Inheritance Declaration

**Context**: An individual declares their right to an inheritance before city authorities.

**Simplified Entry**:
```json
{
  "@id": "https://gmn.org/declaration/inheritance_claim_1451_01_10",
  "@type": "gmn:E31_5_Declaration",
  "gmn:P102_1_has_title": "Declaration of Inheritance Rights",
  "gmn:P70_24_indicates_declarant": {
    "@id": "https://gmn.org/person/maria_visconti",
    "@type": "cidoc:E21_Person"
  },
  "gmn:P70_22_indicates_receiving_party": {
    "@id": "https://gmn.org/org/genoa_magistracy",
    "@type": "cidoc:E74_Group"
  },
  "gmn:P70_25_indicates_declaration_subject