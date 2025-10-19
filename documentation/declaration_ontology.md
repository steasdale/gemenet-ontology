# E31.5 Declaration - Ontology Addition

## Class Definition

```turtle
# Class: E31.5 Declaration
gmn:E31_5_Declaration
    a owl:Class ;
    rdfs:subClassOf cidoc:E31_Document ;
    rdfs:label "E31.5 Declaration"@en ;
    rdfs:comment "Specialized class that describes declaration documents. This is a specialized type of cidoc:E31_Document used to represent legal documents where one party (the declarant) makes a formal statement, acknowledgment, or assertion to another party (the recipient) regarding a specific subject matter. Declarations can be either notarial documents (recorded by a notary) or governmental documents (issued by official authorities without notarial involvement). Common types include declarations of debt, acknowledgments of obligations, statements of fact, official pronouncements, formal notifications, or governmental decrees. Unlike contracts (E31.1) which typically involve bilateral agreements, declarations are unilateral statements, though they have legal effect and may create or acknowledge obligations. Some declarations may be recorded in notarial registers alongside contracts, while others exist as independent governmental or administrative documents. Instances of this class represent the physical or conceptual document itself, while the actual declaration activity and its effects are modeled through E7_Activity that the document documents (via P70_documents)."@en ;
    dcterms:created "2025-10-18"^^xsd:date ;
    rdfs:seeAlso cidoc:E31_Document, cidoc:E7_Activity, cidoc:P70_documents .
```

## Semantic Structure

```
E31_5_Declaration (the declaration document)
  └─ P70_documents
      └─ E7_Activity (the declaration activity)
          ├─ P2_has_type → AAT 300027623 (declarations)
          ├─ P14_carried_out_by → E39_Actor (declarant)
          ├─ P01_has_domain → E39_Actor (recipient) [using P01i_is_domain_of inverse]
          └─ P16_used_specific_object → E1_CRM_Entity (declaration subject)
```

## Properties

### P70.24 indicates declarant

```turtle
gmn:P70_24_indicates_declarant
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.24 indicates declarant"@en ;
    rdfs:comment "Simplified property for associating a declaration document with the person or entity making the declaration. The declarant is the party who is formally stating, acknowledging, or asserting something. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor. The E7_Activity should be typed as a declaration (AAT 300027623). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_5_Declaration ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-18"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

### P70.22 indicates receiving party (updated)

```turtle
gmn:P70_22_indicates_receiving_party
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.22 indicates receiving party"@en ;
    rdfs:comment "Simplified property for associating a document with the person or entity receiving something in the documented activity. In cession of rights contracts, this is the party receiving the ceded rights. In declarations, this is the party to whom the declaration is addressed or directed. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P01_has_domain > E39_Actor (using the inverse P01i_is_domain_of for declarations) OR E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor (for cessions, where both parties carry out the activity). The E7_Activity should be typed appropriately (AAT 300417639 for cessions, AAT 300027623 for declarations). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_4_Cession_of_Rights_Contract
            gmn:E31_5_Declaration
        )
    ] ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-18"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by, cidoc:P01_has_domain .
```

### P70.25 indicates declaration subject

```turtle
gmn:P70_25_indicates_declaration_subject
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.25 indicates declaration subject"@en ;
    rdfs:comment "Simplified property for associating a declaration document with the subject matter being declared, acknowledged, or asserted. This can include debts being acknowledged, facts being stated, obligations being recognized, properties being claimed, rights being asserted, or any other matter that is the content of the declaration. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity. The E7_Activity should be typed as a declaration (AAT 300027623). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_5_Declaration ;
    rdfs:range cidoc:E1_CRM_Entity ;
    dcterms:created "2025-10-18"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P16_used_specific_object .
```

## Transformation Examples

### Example 1: Declaration of Debt

**Input (shortcut):**
```turtle
<declaration001> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <merchant_giovanni> ;
    gmn:P70_22_indicates_receiving_party <merchant_paolo> ;
    gmn:P70_25_indicates_declaration_subject <debt_500_lire> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<declaration001> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <declaration001/activity> .

<declaration001/activity> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <merchant_giovanni> ;
    cidoc:P01_has_domain <merchant_paolo> ;
    cidoc:P16_used_specific_object <debt_500_lire> .
```

### Example 2: Governmental Declaration

**Input (shortcut):**
```turtle
<declaration002> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <doge_office> ;
    gmn:P70_22_indicates_receiving_party <citizens_genoa> ;
    gmn:P70_25_indicates_declaration_subject <tax_exemption_1450> ;
    gmn:P94i_2_has_enactment_date "1450-06-15"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <genoa_palace> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<declaration002> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <declaration002/activity> ;
    cidoc:P94i_was_created_by <declaration002/creation> .

<declaration002/activity> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <doge_office> ;
    cidoc:P01_has_domain <citizens_genoa> ;
    cidoc:P16_used_specific_object <tax_exemption_1450> .

<declaration002/creation> a cidoc:E65_Creation ;
    cidoc:P4_has_time-span <declaration002/timespan> ;
    cidoc:P7_took_place_at <genoa_palace> .

<declaration002/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1450-06-15"^^xsd:date .
```

## AAT Reference

- **AAT 300027623**: declarations (reports)
  - "Formal or explicit statements, proclamations, or announcements"

## Implementation Notes

1. **Shared Activity**: All three properties (P70.24, P70.25, P70.26) share the same E7_Activity node
2. **Activity Type**: Automatically typed as AAT 300027623 (declarations)
3. **Flexibility**: Works for both notarial and governmental declarations
4. **Optional Notary**: Unlike sales contracts, the P94i_1_was_created_by property is optional, since governmental declarations may not involve a notary
5. **Unilateral Nature**: The structure reflects that declarations are typically unilateral acts by the declarant, though they may create obligations or have legal effects on the recipient

## Comparison with Other Contract Types

| Aspect | Sales Contract | Arbitration | Cession | Declaration |
|--------|---------------|-------------|---------|-------------|
| Central Event | E8_Acquisition | E7_Activity (arbitration) | E7_Activity (cession) | E7_Activity (declaration) |
| Main Actors | P23/P22 (seller/buyer) | P14 (all parties & arbitrators) | P14 (both parties) | P14 (declarant) + P01 (recipient) |
| Receiving Party | P22 (buyer) | N/A | P14 (receiving party) | P01 (recipient) |
| Object | P24 (property) | P16 (dispute subject) | P16 (rights/legal object) | P16 (declaration subject) |
| Nature | Bilateral transfer | Multi-party agreement | Bilateral transfer of rights | Unilateral statement |
