# E31.1 General Contract - Ontology Documentation

## Overview

This document provides complete semantic documentation for the **gmn:E31_1_Contract** class in the Genoese Merchant Networks CIDOC-CRM extension ontology. This class serves as the parent class for all specialized contract types and represents notarial contract documents that formalize agreements, transactions, and legal acts between parties in medieval and early modern Genoa.

**Namespace**: `http://www.genoesemerchantnetworks.com/ontology#`  
**Prefix**: `gmn:`  
**Class URI**: `gmn:E31_1_Contract`  
**Ontology Version**: 1.5  
**Last Updated**: 2025-10-26

## Class Definition

### TTL Definition

```turtle
# Class: E31.1 Contract
gmn:E31_1_Contract
    a owl:Class ;
    rdfs:subClassOf cidoc:E31_Document ;
    rdfs:label "E31.1 Contract"@en ;
    rdfs:comment "General class that describes notarial contract documents. This is a specialized type of E31_Document used to represent legal documents recorded by notaries that formalize agreements, transactions, and legal acts between parties. Contracts are the primary documentary evidence for social, economic, and legal relationships in medieval and early modern societies. Instances of this class represent the physical or conceptual document itself, while the actual events documented (acquisitions, agreements, etc.) are modeled through appropriate event classes that the document documents (via P70_documents). This serves as a parent class for more specific contract types."@en ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:E31_Document, cidoc:P70_documents .
```

### Semantic Description

**gmn:E31_1_Contract** represents notarial contract documents in the Genoese context. This class:

1. **Extends CIDOC-CRM**: Specializes `cidoc:E31_Document` to represent contract documents specifically
2. **Parent Class Role**: Serves as the base class for all specialized contract types
3. **Document Focus**: Models the contract document itself, not the transaction it records
4. **Historical Context**: Captures notarial records that were central to medieval commercial and social life

### Key Characteristics

- **Type**: OWL Class
- **Subclass of**: cidoc:E31_Document
- **Instantiation**: Typically instantiated through specialized subclasses
- **Purpose**: Parent class providing common structure for all contract types
- **Scope**: Notarial contracts from medieval and early modern Genoa

## Inheritance Hierarchy

### Complete Class Tree

```
owl:Thing
  │
  └── cidoc:E1_CRM_Entity
      │
      └── cidoc:E71_Human-Made_Thing  
          │
          └── cidoc:E31_Document (CIDOC-CRM)
              │
              ├── gmn:E31_1_Contract ← This class
              │   │
              │   ├── gmn:E31_2_Sales_Contract
              │   │   (Property sales and purchases)
              │   │
              │   ├── gmn:E31_3_Arbitration_Agreement
              │   │   (Dispute resolution agreements)
              │   │
              │   ├── gmn:E31_4_Cession_of_Rights_Contract
              │   │   (Transfer of legal rights and claims)
              │   │
              │   ├── gmn:E31_7_Donation_Contract
              │   │   (Gratuitous property transfers)
              │   │
              │   └── gmn:E31_8_Dowry_Contract
              │       (Marriage-related property transfers)
              │
              ├── gmn:E31_5_Declaration
              │   (Not a contract - unilateral statements)
              │
              └── gmn:E31_6_Correspondence
                  (Not a contract - letters)
```

### Specialized Contract Types

| Class | Label | Transaction Type | Specific Properties |
|-------|-------|------------------|---------------------|
| E31.2 | Sales Contract | E8_Acquisition | P70.14 (seller), P70.15 (buyer), P70.16 (price) |
| E31.3 | Arbitration Agreement | E7_Activity | P70.18 (disputing party), P70.19 (arbitrator) |
| E31.4 | Cession Contract | E7_Activity | P70.21 (conceding party), P70.22 (receiving party) |
| E31.7 | Donation Contract | E8_Acquisition | P70.32 (donor), P70.22 (receiving party) |
| E31.8 | Dowry Contract | E8_Acquisition | P70.32 (donor), P70.22 (receiving party) |

## Semantic Structure

### Document-Transaction Separation

A fundamental principle in this ontology:

```
┌─────────────────────────┐
│   E31_1_Contract        │  (The document)
│   (Document entity)     │
└───────────┬─────────────┘
            │
            │ cidoc:P70_documents
            │
            ▼
┌─────────────────────────┐
│   E8_Acquisition or     │  (The transaction)
│   E7_Activity           │
│   (Event entity)        │
└─────────────────────────┘
```

**Contract (E31_1_Contract)**:
- The physical document or notarial record
- The written evidence of the transaction
- Stored in notarial registers
- Has creation date, creator (notary), location

**Transaction (E8 or E7)**:
- The actual transfer of property or rights
- The legal event or activity
- Has participants, transferred objects, conditions
- May have occurred at different time/place than document creation

### CIDOC-CRM Compliance

The connection follows standard CIDOC-CRM patterns:

```turtle
<contract_doc> a gmn:E31_1_Contract ;
    cidoc:P70_documents <transaction_event> .

<transaction_event> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <party1> ;
    cidoc:P22_transferred_title_to <party2> ;
    cidoc:P24_transferred_title_of <object> .
```

This separation allows:
- Modeling document creation separately from transaction occurrence
- Recording notary information (document creator) vs. transaction participants
- Capturing when contracts document past or future transactions
- Maintaining clear semantic boundaries

## Property Specifications

### Properties Inherited from cidoc:E31_Document

E31_1_Contract instances inherit all properties from cidoc:E31_Document and can use GMN shortcut properties:

#### Identification Properties

**gmn:P1_1_has_name**
```turtle
gmn:P1_1_has_name 
    a owl:DatatypeProperty ;
    rdfs:label "P1.1 has name"@en ;
    rdfs:domain cidoc:E1_CRM_Entity ;  # Includes E31_1_Contract
    rdfs:range cidoc:E62_String .
```

- **Purpose**: Provides a readable name for the contract
- **Transforms to**: `cidoc:P1_is_identified_by > E41_Appellation > P190_has_symbolic_content`
- **Example**: "Sale of house on Via San Lorenzo"

**gmn:P102_1_has_title**
```turtle
gmn:P102_1_has_title
    a owl:DatatypeProperty ;
    rdfs:label "P102.1 has title"@en ;
    rdfs:domain cidoc:E71_Human-Made_Thing ;  # Includes E31_1_Contract
    rdfs:range cidoc:E62_String .
```

- **Purpose**: Formal title, often in Latin
- **Transforms to**: `cidoc:P102_has_title > E35_Title > P190_has_symbolic_content`
- **Example**: "Contractus venditionis domus in civitate Janue"

#### Creation Properties

**gmn:P94i_1_was_created_by**
```turtle
gmn:P94i_1_was_created_by
    a owl:ObjectProperty ;
    rdfs:label "P94i.1 was created by"@en ;
    rdfs:domain cidoc:E31_Document ;  # E31_1_Contract inherits
    rdfs:range cidoc:E21_Person .
```

- **Purpose**: Links to the notary who recorded the contract
- **Transforms to**: `cidoc:P94i_was_created_by > E65_Creation > P14_carried_out_by > E21_Person`
- **Example**: Link to notary resource

**gmn:P94i_2_has_enactment_date**
```turtle
gmn:P94i_2_has_enactment_date
    a owl:DatatypeProperty ;
    rdfs:label "P94i.2 has enactment date"@en ;
    rdfs:domain cidoc:E31_Document ;
    rdfs:range xsd:date .
```

- **Purpose**: Date when the contract was enacted/recorded
- **Transforms to**: `cidoc:P94i_was_created_by > E65_Creation > P4_has_time-span > E52_Time-Span > P82_at_some_time_within`
- **Example**: "1450-03-15"^^xsd:date

**gmn:P94i_3_has_place_of_enactment**
```turtle
gmn:P94i_3_has_place_of_enactment
    a owl:ObjectProperty ;
    rdfs:label "P94i.3 has place of enactment"@en ;
    rdfs:domain cidoc:E31_Document ;
    rdfs:range cidoc:E53_Place .
```

- **Purpose**: Location where contract was drawn up
- **Transforms to**: `cidoc:P94i_was_created_by > E65_Creation > P7_took_place_at > E53_Place`
- **Example**: Link to place resource (notary's office, public building)

#### Context Properties

**gmn:P46i_1_is_contained_in**
```turtle
gmn:P46i_1_is_contained_in
    a owl:ObjectProperty ;
    rdfs:label "P46i.1 is contained in"@en ;
    rdfs:domain cidoc:E18_Physical_Thing ;  # Documents are physical things
    rdfs:range cidoc:E31_Document .  # Register is also a document
```

- **Purpose**: Links contract to its containing register
- **Transforms to**: `cidoc:P46i_forms_part_of > E31_Document` (register)
- **Example**: Link to notarial register resource

**cidoc:P70_documents**
```turtle
# This is a standard CIDOC-CRM property
cidoc:P70_documents
    rdfs:domain cidoc:E31_Document ;
    rdfs:range cidoc:E1_CRM_Entity .  # Usually E7_Activity or E8_Acquisition
```

- **Purpose**: Links contract document to the transaction it documents
- **Critical property**: This is the key connection between document and transaction
- **Example**: Link to E8_Acquisition or E7_Activity resource

#### Annotation Properties

**gmn:P3_1_has_editorial_note**
```turtle
gmn:P3_1_has_editorial_note 
    a owl:DatatypeProperty ;
    rdfs:label "P3.1 has editorial note"@en ;
    rdfs:domain cidoc:E1_CRM_Entity ;
    rdfs:range cidoc:E62_String .
```

- **Purpose**: Internal notes for project documentation
- **Transforms to**: `cidoc:P67i_is_referred_to_by > E33_Linguistic_Object > P190_has_symbolic_content`
- **Example**: "Contract text partially damaged; interpretation uncertain"
- **Note**: Internal use; may be excluded from public exports

### Properties NOT on E31_1_Contract

The following properties exist in the ontology but apply only to specialized contract types:

#### Sales Contract Properties (E31.2)

- `gmn:P70_14_indicates_seller` - Domain: E31_2_Sales_Contract
- `gmn:P70_15_indicates_buyer` - Domain: E31_2_Sales_Contract
- `gmn:P70_16_documents_sale_price_amount` - Domain: E31_2_Sales_Contract
- `gmn:P70_17_documents_sale_price_currency` - Domain: E31_2_Sales_Contract

#### Arbitration Properties (E31.3)

- `gmn:P70_18_documents_disputing_party` - Domain: E31_3_Arbitration_Agreement
- `gmn:P70_19_documents_arbitrator` - Domain: E31_3_Arbitration_Agreement
- `gmn:P70_20_documents_dispute_subject` - Domain: E31_3_Arbitration_Agreement

#### Cession Properties (E31.4)

- `gmn:P70_21_indicates_conceding_party` - Domain: E31_4_Cession_of_Rights_Contract
- `gmn:P70_22_indicates_receiving_party` - Domain: E31_4_Cession_of_Rights_Contract (also others)
- `gmn:P70_23_indicates_object_of_cession` - Domain: E31_4_Cession_of_Rights_Contract

#### Donation/Dowry Properties (E31.7, E31.8)

- `gmn:P70_32_indicates_donor` - Domain: Union of E31_7 and E31_8
- `gmn:P70_33_indicates_object_of_donation` - Domain: E31_7_Donation_Contract
- `gmn:P70_34_indicates_object_of_dowry` - Domain: E31_8_Dowry_Contract

**These properties should not be used with E31_1_Contract directly.** Use the appropriate specialized contract type instead.

## Usage Examples

### Example 1: Basic General Contract (Rare Usage)

When a contract doesn't fit specialized types:

**Input (shortcut):**
```turtle
<contract_misc_001> a gmn:E31_1_Contract ;
    gmn:P1_1_has_name "Unclassified contract from Notary Basso, 1455" ;
    gmn:P94i_1_was_created_by <notary_antonio_basso> ;
    gmn:P94i_2_has_enactment_date "1455-08-12"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <genoa_piazza_banchi> ;
    gmn:P46i_1_is_contained_in <register_basso_1455> ;
    gmn:P3_1_has_editorial_note "Contract type unclear; appears to be a complex arrangement not fitting standard categories. Requires expert analysis." .
```

**Output (CIDOC-CRM compliant):**
```turtle
<contract_misc_001> a gmn:E31_1_Contract ;
    cidoc:P1_is_identified_by <contract_misc_001/appellation/1> ;
    cidoc:P94i_was_created_by <contract_misc_001/creation> ;
    cidoc:P46i_forms_part_of <register_basso_1455> ;
    cidoc:P67i_is_referred_to_by <contract_misc_001/note/1> .

<contract_misc_001/appellation/1> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Unclassified contract from Notary Basso, 1455" .

<contract_misc_001/creation> a cidoc:E65_Creation ;
    cidoc:P14_carried_out_by <notary_antonio_basso> ;
    cidoc:P4_has_time-span <contract_misc_001/creation/timespan> ;
    cidoc:P7_took_place_at <genoa_piazza_banchi> .

<contract_misc_001/creation/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1455-08-12"^^xsd:date .

<contract_misc_001/note/1> a cidoc:E33_Linguistic_Object ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456627> ;
    cidoc:P190_has_symbolic_content "Contract type unclear..." .
```

### Example 2: Proper Use of Specialized Type (Common Usage)

Most contracts should use specialized types:

**Input (shortcut):**
```turtle
<contract_sale_001> a gmn:E31_2_Sales_Contract ;  # Specific type
    gmn:P1_1_has_name "Sale of house in Genoa" ;
    gmn:P102_1_has_title "Contractus venditionis domus"@la ;
    gmn:P70_14_indicates_seller <maria_doria> ;
    gmn:P70_15_indicates_buyer <giovanni_spinola> ;
    gmn:P70_16_documents_sale_price_amount "500.00"^^xsd:decimal ;
    gmn:P70_17_documents_sale_price_currency <lira_genovese> ;
    gmn:P94i_1_was_created_by <notary_basso> ;
    gmn:P94i_2_has_enactment_date "1455-08-12"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <genoa> ;
    gmn:P46i_1_is_contained_in <register_basso_1455> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<contract_sale_001> a gmn:E31_2_Sales_Contract ;
    cidoc:P1_is_identified_by <contract_sale_001/appellation/1> ;
    cidoc:P102_has_title <contract_sale_001/title/1> ;
    cidoc:P70_documents <contract_sale_001/acquisition> ;
    cidoc:P94i_was_created_by <contract_sale_001/creation> ;
    cidoc:P46i_forms_part_of <register_basso_1455> .

<contract_sale_001/appellation/1> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Sale of house in Genoa" .

<contract_sale_001/title/1> a cidoc:E35_Title ;
    cidoc:P190_has_symbolic_content "Contractus venditionis domus"@la .

<contract_sale_001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <maria_doria> ;
    cidoc:P22_transferred_title_to <giovanni_spinola> ;
    cidoc:P24_transferred_title_of <house_001> ;
    cidoc:P177_assigned_property_of_type [
        a cidoc:E97_Monetary_Amount ;
        cidoc:P180_has_currency <lira_genovese> ;
        cidoc:P181_has_amount "500.00"^^xsd:decimal
    ] .

<contract_sale_001/creation> a cidoc:E65_Creation ;
    cidoc:P14_carried_out_by <notary_basso> ;
    cidoc:P4_has_time-span <contract_sale_001/creation/timespan> ;
    cidoc:P7_took_place_at <genoa> .

<contract_sale_001/creation/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1455-08-12"^^xsd:date .
```

### Example 3: Querying Contract Hierarchy

**SPARQL: Find all contracts regardless of type**
```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?type ?name WHERE {
    ?contract a ?type .
    ?type rdfs:subClassOf* gmn:E31_1_Contract .
    
    OPTIONAL {
        ?contract cidoc:P1_is_identified_by ?appellation .
        ?appellation cidoc:P190_has_symbolic_content ?name .
    }
}
ORDER BY ?type
```

**SPARQL: Count contracts by type**
```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

SELECT ?type ?label (COUNT(?contract) as ?count) WHERE {
    ?contract a ?type .
    ?type rdfs:subClassOf+ gmn:E31_1_Contract .
    ?type rdfs:label ?label .
}
GROUP BY ?type ?label
ORDER BY DESC(?count)
```

**SPARQL: Find contracts by notary**
```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?notary ?date WHERE {
    ?contract a/rdfs:subClassOf* gmn:E31_1_Contract .
    ?contract cidoc:P94i_was_created_by ?creation .
    ?creation cidoc:P14_carried_out_by ?notary .
    ?creation cidoc:P4_has_time-span/cidoc:P82_at_some_time_within ?date .
}
ORDER BY ?date
```

## Transformation Patterns

### General Contract Transformations

E31_1_Contract uses standard document property transformations. There are no contract-specific transformation functions because:

1. **Standard Properties**: E31_1_Contract only uses inherited document properties
2. **No Transaction-Specific Properties**: Transaction-specific properties belong to specialized types
3. **Reusable Transformations**: All transformation functions are defined for the general properties

### Standard Property Transformations Used

The following transformation functions apply to E31_1_Contract:

- `transform_p1_1_has_name()` - For contract names
- `transform_p102_1_has_title()` - For formal titles
- `transform_p94i_1_was_created_by()` - For notary information
- `transform_p94i_2_has_enactment_date()` - For enactment dates
- `transform_p94i_3_has_place_of_enactment()` - For enactment locations
- `transform_p46i_1_is_contained_in()` - For register containment
- `transform_p3_1_has_editorial_note()` - For editorial annotations

These functions are defined in `gmn_to_cidoc_transform.py` and apply to all document types, including contracts.

### Specialized Type Transformations

Specialized contract types add their own transformation functions:

**Sales Contracts (E31.2)**:
- `transform_p70_14_indicates_seller()`
- `transform_p70_15_indicates_buyer()`
- `transform_p70_16_documents_sale_price()`

**Donation Contracts (E31.7)**:
- `transform_p70_32_indicates_donor()`
- `transform_p70_33_indicates_object_of_donation()`

**Dowry Contracts (E31.8)**:
- `transform_p70_32_indicates_donor()` (shared with donations)
- `transform_p70_34_indicates_object_of_dowry()`

See specialized contract documentation for details on these transformations.

## Best Practices

### 1. Use Specialized Types When Possible

✅ **Preferred**:
```turtle
<contract001> a gmn:E31_2_Sales_Contract .
```

❌ **Avoid**:
```turtle
<contract001> a gmn:E31_1_Contract .  # Too general when specific type exists
```

### 2. Understand Document vs. Transaction

✅ **Correct separation**:
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents <acquisition001> .

<acquisition001> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <seller> ;
    cidoc:P22_transferred_title_to <buyer> .
```

❌ **Incorrect conflation**:
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;
    cidoc:P23_transferred_title_from <seller> .  # Wrong: this belongs on E8_Acquisition
```

### 3. Document Uncertain Classifications

✅ **Use editorial notes**:
```turtle
<contract001> a gmn:E31_1_Contract ;
    gmn:P3_1_has_editorial_note "Contract type unclear; requires expert analysis" .
```

### 4. Leverage Inheritance in Queries

✅ **Query all contracts**:
```sparql
?x a/rdfs:subClassOf* gmn:E31_1_Contract .
```

### 5. Follow Naming Conventions

✅ **Clear names**:
```turtle
gmn:P1_1_has_name "Sale of house by Giovanni to Marco, 1455"@en .
```

❌ **Cryptic names**:
```turtle
gmn:P1_1_has_name "G->M 1455"@en .
```

## CIDOC-CRM Compliance

### Alignment with CIDOC-CRM

E31_1_Contract fully complies with CIDOC-CRM by:

1. **Proper Subclassing**: Extends cidoc:E31_Document
2. **P70_documents Usage**: Links documents to documented entities correctly
3. **Event Separation**: Distinguishes document creation (E65_Creation) from documented transactions
4. **Standard Properties**: Uses CIDOC-CRM properties (P1, P70, P94i, etc.) correctly

### CIDOC-CRM Path Equivalencies

The shortcut properties expand to standard CIDOC-CRM paths:

| Shortcut Property | CIDOC-CRM Path |
|------------------|----------------|
| P1.1 has name | P1_is_identified_by > E41_Appellation > P190_has_symbolic_content |
| P94i.1 was created by | P94i_was_created_by > E65_Creation > P14_carried_out_by |
| P94i.2 has enactment date | P94i_was_created_by > E65_Creation > P4_has_time-span > P82_at_some_time_within |
| P94i.3 has place of enactment | P94i_was_created_by > E65_Creation > P7_took_place_at |
| P46i.1 is contained in | P46i_forms_part_of |
| P3.1 has editorial note | P67i_is_referred_to_by > E33_Linguistic_Object > P190_has_symbolic_content |

### Validation Against CIDOC-CRM

To validate compliance:

1. **Class Hierarchy**: Verify E31_1_Contract is properly subclassed from cidoc:E31_Document
2. **Property Domains**: Ensure properties have correct domain restrictions
3. **Property Ranges**: Ensure properties have correct range restrictions
4. **Path Correctness**: Verify transformation outputs match CIDOC-CRM specifications

## Related Documentation

### Specialized Contract Types

- **Sales Contracts (E31.2)**: See main ontology documentation
- **Donation Contracts (E31.7)**: See `donation-documentation.md`
- **Dowry Contracts (E31.8)**: See `dowry-documentation.md`
- **Arbitration Agreements (E31.3)**: See `arbitration-ontology.md`
- **Cession Contracts (E31.4)**: See main ontology documentation

### Related Document Types

- **Declarations (E31.5)**: See declaration documentation (not a contract)
- **Correspondence (E31.6)**: See correspondence documentation (not a contract)

### Implementation Resources

- **Implementation Guide**: `contract-implementation-guide.md`
- **TTL Reference**: `contract-ontology.ttl`
- **Transformation Reference**: `contract-transform.py`
- **Documentation Additions**: `contract-doc-note.txt`

## Conclusion

The E31_1_Contract class is a foundational element that:

- Provides a common base for all contract types through inheritance
- Maintains separation between documents and transactions
- Ensures CIDOC-CRM compliance through proper subclassing
- Enables flexible ontology extension for new contract types

For specific contract types, always consult their specialized documentation. The general contract class serves primarily as a parent class and should be used directly only when a contract doesn't fit existing specialized types.
