# Ontology Documentation: P70.22 Indicates Receiving Party
## Complete Semantic Documentation with Transformation Examples

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Formal Definition](#formal-definition)
3. [Semantic Interpretation by Document Type](#semantic-interpretation-by-document-type)
4. [CIDOC-CRM Transformation Paths](#cidoc-crm-transformation-paths)
5. [Property Relationships](#property-relationships)
6. [Comprehensive Examples](#comprehensive-examples)
7. [Comparison with Related Properties](#comparison-with-related-properties)
8. [Implementation Patterns](#implementation-patterns)

---

## Property Overview

### Basic Information

**Property URI**: `gmn:P70_22_indicates_receiving_party`

**Label**: "P70.22 indicates receiving party" (English)

**Property Type**: `owl:ObjectProperty`, `rdf:Property`

**Status**: Active

**Version History**:
- Created: 2025-10-18
- Last Modified: 2025-10-25
- Reason for Modification: Added dowry contract support; refined CIDOC-CRM transformation paths

### Purpose

This property provides a simplified shortcut for associating documents with the person or entity that receives something in the documented activity. It is a multi-purpose property that adapts semantically based on the document type, providing appropriate transformations to full CIDOC-CRM structures.

---

## Formal Definition

### RDF Schema Declaration

```turtle
gmn:P70_22_indicates_receiving_party
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.22 indicates receiving party"@en ;
    rdfs:comment "Simplified property for associating a document with the person or entity receiving something in the documented activity. In cession of rights contracts, this is the party receiving the ceded rights. In declarations, this is the party to whom the declaration is addressed or directed. In donation contracts, this is the donee receiving the donated property. In dowry contracts, this is the party (often the spouse or the couple) receiving the dowry property. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P01_has_domain > E39_Actor (using the inverse P01i_is_domain_of for declarations) OR E31_Document > P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor (for cessions, donations, and dowries, where the receiving party acquires ownership or rights). The E7_Activity or E8_Acquisition should be typed appropriately (AAT 300417639 for cessions, AAT 300027623 for declarations, or appropriate type for donations and dowries). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_4_Cession_of_Rights_Contract
            gmn:E31_5_Declaration
            gmn:E31_7_Donation_Contract
            gmn:E31_8_Dowry_Contract
        )
    ] ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-18"^^xsd:date ;
    dcterms:modified "2025-10-25"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P22_transferred_title_to, cidoc:P01_has_domain .
```

### Domain Specification

The property has a **union domain** comprising four document classes:

1. **`gmn:E31_4_Cession_of_Rights_Contract`**
   - Definition: Documents recording the transfer of legal rights from one party to another
   - Subclass of: `cidoc:E31_Document`

2. **`gmn:E31_5_Declaration`**
   - Definition: Formal statements or pronouncements made by one party
   - Subclass of: `cidoc:E31_Document`

3. **`gmn:E31_7_Donation_Contract`**
   - Definition: Documents recording voluntary transfers of property without payment
   - Subclass of: `cidoc:E31_Document`

4. **`gmn:E31_8_Dowry_Contract`**
   - Definition: Documents recording property transfers as part of marriage arrangements
   - Subclass of: `cidoc:E31_Document`

### Range Specification

**Range**: `cidoc:E39_Actor`

**Definition**: The range encompasses any person, group, or organization that can act as a receiving party. This includes:
- Individual persons (`cidoc:E21_Person`)
- Groups and organizations (`cidoc:E74_Group`)
- Legal persons (corporations, institutions)
- Families and households

### Superproperty

**Superproperty**: `cidoc:P70_documents`

**Meaning**: All instances of `gmn:P70_22_indicates_receiving_party` are also instances of `cidoc:P70_documents`, establishing that the document does document some entity (in this case, indirectly through the documented activity).

### Cardinality

**Quantification**: Many to many (0,n:0,n)

- A document can indicate **zero or multiple** receiving parties
- An actor can be the receiving party in **zero or multiple** documents

---

## Semantic Interpretation by Document Type

### 1. Cession of Rights Contracts

**Context**: Legal transfer of rights, claims, or obligations from one party to another.

**Receiving Party Role**: The party who **acquires** the rights being transferred.

**Semantic Meaning**: The receiving party becomes the new holder of the legal rights, stepping into the position previously held by the conceding party.

**Common Scenarios**:
- Rights to collect debts
- Usufruct rights over property
- Claims arising from other contracts
- Inheritance rights
- Rights of ownership

**Example**:
```
Merchant Marco cedes his right to collect a debt of 100 lire 
from Giovanni to his business partner Pietro. 
Pietro is the receiving party.
```

**CIDOC-CRM Transformation**: Uses `E7_Activity` (cession activity) with `P14_carried_out_by` to link the receiving party as a co-participant alongside the conceding party.

---

### 2. Declarations

**Context**: Formal statements, proclamations, or pronouncements made by a declarant.

**Receiving Party Role**: The party to whom the declaration is **addressed or directed**.

**Semantic Meaning**: The receiving party is the target or addressee of the communication, the party who is meant to receive and acknowledge the declaration.

**Common Scenarios**:
- Debt acknowledgments directed to creditors
- Statements made to magistrates or officials
- Proclamations addressed to specific individuals
- Public notices with specific addressees

**Example**:
```
Merchant Pietro makes a declaration to Magistrate Antonio 
acknowledging a debt to another merchant. 
Antonio is the receiving party.
```

**CIDOC-CRM Transformation**: Uses `E7_Activity` (declaration activity) with `P01_has_domain` to establish the receiving party as the subject/target of the declaration activity.

---

### 3. Donation Contracts

**Context**: Voluntary transfer of property ownership without expectation of payment (gratuitous transfer).

**Receiving Party Role**: The **donee** or beneficiary who receives the gifted property.

**Semantic Meaning**: The receiving party acquires ownership of the donated property as a gift, becoming the new legal owner without providing consideration.

**Common Scenarios**:
- Charitable donations to religious institutions
- Gifts to family members
- Endowments to hospitals or schools
- Transfers to charitable organizations

**Example**:
```
Widow Maria donates a warehouse to Hospital Pammatone 
for care of the poor. 
Hospital Pammatone is the receiving party.
```

**CIDOC-CRM Transformation**: Uses `E8_Acquisition` with `P22_transferred_title_to` to establish the receiving party as the new owner who acquires title.

---

### 4. Dowry Contracts

**Context**: Property transfers as part of marriage arrangements, typically from family to married couple.

**Receiving Party Role**: The **spouse or married couple** who receives the dowry property.

**Semantic Meaning**: The receiving party (often the husband or the couple jointly) acquires ownership of property transferred as part of the marriage arrangement.

**Common Scenarios**:
- Father providing dowry to daughter's husband
- Family endowing a marriage with property
- Transfer of property rights to newly married couple
- Provision of financial support for marriage

**Example**:
```
Father Filippo provides a house as dowry for his daughter's 
marriage to Luca. 
Luca (or the couple) is the receiving party.
```

**CIDOC-CRM Transformation**: Uses `E8_Acquisition` with `P22_transferred_title_to` to establish the receiving party as the new owner who acquires title to the dowry property.

---

## CIDOC-CRM Transformation Paths

### Path 1: E8_Acquisition with P22 (Donations and Dowries)

**Used for**: Donation Contracts, Dowry Contracts

**Full Path**:
```
E31_Document → P70_documents → E8_Acquisition → P22_transferred_title_to → E39_Actor
```

**Graph Structure**:
```
<document> a gmn:E31_7_Donation_Contract ;  # or gmn:E31_8_Dowry_Contract
    cidoc:P70_documents <document/acquisition> .

<document/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P22_transferred_title_to <receiving_party> ;
    cidoc:P23_transferred_title_from <donor> ;
    cidoc:P24_transferred_title_of <property> .

<receiving_party> a cidoc:E39_Actor .
```

**Semantic Justification**:
- Donations and dowries involve actual **transfer of ownership**
- `E8_Acquisition` is the appropriate CIDOC-CRM class for ownership transfer events
- `P22_transferred_title_to` explicitly models the recipient of ownership
- This structure integrates cleanly with P23 (donor) and P24 (property) relationships

**Advantages**:
- Captures the legal nature of ownership transfer
- Supports integration with property descriptions
- Enables querying about title transfers
- Maintains semantic precision about legal rights

---

### Path 2: E7_Activity with P01 (Declarations)

**Used for**: Declarations

**Full Path**:
```
E31_Document → P70_documents → E7_Activity → P01_has_domain → E39_Actor
```

**Inverse Property**: `P01i_is_domain_of` (from Actor to Activity)

**Graph Structure**:
```
<document> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <document/declaration> .

<document/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300027623> ;  # declarations
    cidoc:P14_carried_out_by <declarant> ;
    cidoc:P01_has_domain <receiving_party> .

<receiving_party> a cidoc:E39_Actor .
```

**Semantic Justification**:
- Declarations are **communicative acts**, not ownership transfers
- `E7_Activity` models the declaration action itself
- `P01_has_domain` establishes the receiving party as the "subject" or target of the activity
- This distinguishes the recipient (target) from the declarant (actor)
- Creates an asymmetric relationship appropriate for directed communication

**Advantages**:
- Clearly distinguishes declarant (P14) from recipient (P01)
- Models the communicative nature of declarations
- Supports queries about who was addressed
- Maintains semantic distinction from ownership transfers

**Note on P01**: 
The `P01_has_domain` property is typically used for activities where one party is the "subject" of an action carried out by another. In declarations, the receiving party is the target or addressee - the entity toward whom the declaration is directed. This is semantically distinct from P14 (carried_out_by), which is used for the declarant who performs the act.

---

### Path 3: E7_Activity with P14 (Cessions)

**Used for**: Cession of Rights Contracts

**Full Path**:
```
E31_Document → P70_documents → E7_Activity → P14_carried_out_by → E39_Actor
```

**Graph Structure**:
```
<document> a gmn:E31_4_Cession_of_Rights_Contract ;
    cidoc:P70_documents <document/cession> .

<document/cession> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417639> ;  # transfers of rights
    cidoc:P14_carried_out_by <conceding_party> ;
    cidoc:P14_carried_out_by <receiving_party> ;
    cidoc:P16_used_specific_object <legal_object> .

<receiving_party> a cidoc:E39_Actor .
```

**Semantic Justification**:
- Cessions involve **transfer of legal rights**, not necessarily physical ownership
- Both parties actively **participate** in the cession activity
- `P14_carried_out_by` models both parties as co-participants
- The legal object (rights) is connected via `P16_used_specific_object`
- This models cessions as collaborative legal activities

**Advantages**:
- Models mutual participation in the rights transfer
- Distinguishes rights transfer from ownership transfer
- Supports connection to abstract legal objects (E72_Legal_Object)
- Enables querying about participants in legal activities

**Why Not E8_Acquisition for Cessions?**
While cessions do involve transfer, they typically transfer **legal rights** (E72_Legal_Object) rather than physical property (E18_Physical_Thing). The E7_Activity + P16 structure better captures this abstract legal transfer. However, in cases where cessions specifically involve transfer of ownership rights over physical property, E8_Acquisition could be considered.

---

## Property Relationships

### Complementary Properties (Used Together)

#### With Cession of Rights Contracts:
1. **`gmn:P70_21_indicates_conceding_party`**
   - The party transferring the rights
   - Both parties linked via P14_carried_out_by
   - Create a complete bilateral transfer

2. **`gmn:P70_23_indicates_object_of_cession`**
   - Specifies what legal rights are being transferred
   - Linked via P16_used_specific_object to the cession activity
   - Completes the "who transfers what to whom" structure

#### With Declarations:
1. **`gmn:P70_24_indicates_declarant`**
   - The party making the declaration
   - Linked via P14_carried_out_by
   - Contrasts with receiving party (P01_has_domain)

2. **`gmn:P70_25_indicates_declaration_subject`**
   - Specifies the subject matter of the declaration
   - Linked via P16_used_specific_object
   - Completes the "who declares what to whom" structure

#### With Donation Contracts:
1. **`gmn:P70_32_indicates_donor`**
   - The party giving the property
   - Linked via P23_transferred_title_from
   - Bilateral relationship with receiving party (P22)

2. **`gmn:P70_33_indicates_object_of_donation`**
   - Specifies what property is being donated
   - Linked via P24_transferred_title_of to the acquisition
   - Completes the "who gives what to whom" structure

#### With Dowry Contracts:
1. **`gmn:P70_32_indicates_donor`**
   - The party providing the dowry (often parent or family)
   - Linked via P23_transferred_title_from
   - Bilateral relationship with receiving party (P22)

2. **`gmn:P70_34_indicates_object_of_dowry`**
   - Specifies what property is transferred as dowry
   - Linked via P24_transferred_title_of to the acquisition
   - Completes the "who provides what dowry to whom" structure

### Shared Event Structures

All related properties for a given document type reference the **same intermediate event node**:

**For Donations/Dowries** (shared E8_Acquisition):
```
<document/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <donor> ;           # from P70.32
    cidoc:P22_transferred_title_to <receiving_party> ;   # from P70.22
    cidoc:P24_transferred_title_of <property> .          # from P70.33 or P70.34
```

**For Cessions** (shared E7_Activity):
```
<document/cession> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <conceding_party> ;         # from P70.21
    cidoc:P14_carried_out_by <receiving_party> ;         # from P70.22
    cidoc:P16_used_specific_object <legal_rights> .      # from P70.23
```

**For Declarations** (shared E7_Activity):
```
<document/declaration> a cidoc:E7_Activity ;
    cidoc:P14_carried_out_by <declarant> ;               # from P70.24
    cidoc:P01_has_domain <receiving_party> ;             # from P70.22
    cidoc:P16_used_specific_object <subject_matter> .    # from P70.25
```

---

## Comprehensive Examples

### Example 1: Cession of Rights Contract

**Scenario**: Marco cedes his right to collect a debt from Giovanni to his business partner Pietro.

**Input (Shortcut Form)**:
```turtle
<cession001> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_21_indicates_conceding_party <merchant_marco> ;
    gmn:P70_22_indicates_receiving_party <merchant_pietro> ;
    gmn:P70_23_indicates_object_of_cession <debt_claim_giovanni_100_lire> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<cession001> a gmn:E31_4_Cession_of_Rights_Contract ;
    cidoc:P70_documents <cession001/cession> .

<cession001/cession> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417639> ;  # transfers of rights
    cidoc:P14_carried_out_by <merchant_marco> ;
    cidoc:P14_carried_out_by <merchant_pietro> ;
    cidoc:P16_used_specific_object <debt_claim_giovanni_100_lire> .

<merchant_marco> a cidoc:E39_Actor ;
    rdfs:label "Marco, merchant" .

<merchant_pietro> a cidoc:E39_Actor ;
    rdfs:label "Pietro, merchant" .

<debt_claim_giovanni_100_lire> a cidoc:E72_Legal_Object ;
    rdfs:label "Right to collect debt of 100 lire from Giovanni" .
```

**Explanation**:
- The cession activity links both parties as co-participants (P14)
- The receiving party (Pietro) acquires the right previously held by Marco
- The legal object (debt collection right) is the thing being transferred

---

### Example 2: Declaration Document

**Scenario**: Merchant Pietro declares to Magistrate Antonio that he owes 200 lire to another merchant.

**Input (Shortcut Form)**:
```turtle
<declaration001> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <merchant_pietro> ;
    gmn:P70_22_indicates_receiving_party <magistrate_antonio> ;
    gmn:P70_25_indicates_declaration_subject <debt_acknowledgment_200_lire> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<declaration001> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <declaration001/declaration> .

<declaration001/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300027623> ;  # declarations
    cidoc:P14_carried_out_by <merchant_pietro> ;
    cidoc:P01_has_domain <magistrate_antonio> ;
    cidoc:P16_used_specific_object <debt_acknowledgment_200_lire> .

<merchant_pietro> a cidoc:E39_Actor ;
    rdfs:label "Pietro, merchant" .

<magistrate_antonio> a cidoc:E39_Actor ;
    rdfs:label "Antonio, magistrate" .

<debt_acknowledgment_200_lire> a cidoc:E1_CRM_Entity ;
    rdfs:label "Acknowledgment of debt of 200 lire" .
```

**Explanation**:
- Pietro (declarant) carries out the declaration (P14)
- Antonio (receiving party) is the target/addressee (P01)
- The asymmetric relationship (P14 vs P01) captures the directional nature of communication
- The debt acknowledgment is what the declaration is about (P16)

---

### Example 3: Donation Contract

**Scenario**: Widow Maria donates a warehouse near the port to Hospital Pammatone.

**Input (Shortcut Form)**:
```turtle
<donation001> a gmn:E31_7_Donation_Contract ;
    gmn:P70_32_indicates_donor <widow_maria> ;
    gmn:P70_22_indicates_receiving_party <hospital_pammatone> ;
    gmn:P70_33_indicates_object_of_donation <warehouse_porto> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<donation001> a gmn:E31_7_Donation_Contract ;
    cidoc:P70_documents <donation001/acquisition> .

<donation001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <widow_maria> ;
    cidoc:P22_transferred_title_to <hospital_pammatone> ;
    cidoc:P24_transferred_title_of <warehouse_porto> .

<widow_maria> a cidoc:E39_Actor ;
    rdfs:label "Maria, widow" .

<hospital_pammatone> a cidoc:E39_Actor ;
    rdfs:label "Hospital Pammatone" .

<warehouse_porto> a cidoc:E18_Physical_Thing ;
    a gmn:E22_1_Building ;
    rdfs:label "Warehouse near the port" .
```

**Explanation**:
- The acquisition event models the ownership transfer
- Maria transfers title (P23) to Hospital Pammatone (P22)
- The warehouse is the physical property changing ownership (P24)
- E8_Acquisition is appropriate because actual property ownership is transferred

---

### Example 4: Dowry Contract

**Scenario**: Father Filippo provides a house in the city as dowry for his daughter's marriage to Luca.

**Input (Shortcut Form)**:
```turtle
<dowry001> a gmn:E31_8_Dowry_Contract ;
    gmn:P70_32_indicates_donor <father_filippo> ;
    gmn:P70_22_indicates_receiving_party <husband_luca> ;
    gmn:P70_34_indicates_object_of_dowry <house_city_center> ;
    gmn:P70_16_documents_sale_price "1000" ;
    gmn:P70_17_documents_sale_price_currency <lire_currency> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<dowry001> a gmn:E31_8_Dowry_Contract ;
    cidoc:P70_documents <dowry001/acquisition> .

<dowry001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <father_filippo> ;
    cidoc:P22_transferred_title_to <husband_luca> ;
    cidoc:P24_transferred_title_of <house_city_center> ;
    cidoc:P177_assigned_property_type <price_property> .

<father_filippo> a cidoc:E39_Actor ;
    rdfs:label "Filippo, father" .

<husband_luca> a cidoc:E39_Actor ;
    rdfs:label "Luca, husband" .

<house_city_center> a cidoc:E18_Physical_Thing ;
    a gmn:E22_1_Building ;
    rdfs:label "House in city center" .

<price_property> a cidoc:E54_Dimension ;
    cidoc:P90_has_value "1000"^^xsd:decimal ;
    cidoc:P91_has_unit <lire_currency> .

<lire_currency> a cidoc:E58_Measurement_Unit ;
    rdfs:label "lire" .
```

**Explanation**:
- Like donations, uses E8_Acquisition for ownership transfer
- Father transfers title to the husband (or the couple)
- Dowry value is documented through E54_Dimension
- Distinguished from simple donation by document type and marriage context

---

### Example 5: Multiple Receiving Parties

**Scenario**: A donation is made to three religious institutions jointly.

**Input (Shortcut Form)**:
```turtle
<donation_multi> a gmn:E31_7_Donation_Contract ;
    gmn:P70_32_indicates_donor <wealthy_patron> ;
    gmn:P70_22_indicates_receiving_party <monastery_st_francis> ,
                                          <convent_st_clare> ,
                                          <church_st_john> ;
    gmn:P70_33_indicates_object_of_donation <vineyard_countryside> .
```

**Output (CIDOC-CRM Compliant)**:
```turtle
<donation_multi> a gmn:E31_7_Donation_Contract ;
    cidoc:P70_documents <donation_multi/acquisition> .

<donation_multi/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <wealthy_patron> ;
    cidoc:P22_transferred_title_to <monastery_st_francis> ,
                                    <convent_st_clare> ,
                                    <church_st_john> ;
    cidoc:P24_transferred_title_of <vineyard_countryside> .

<monastery_st_francis> a cidoc:E39_Actor .
<convent_st_clare> a cidoc:E39_Actor .
<church_st_john> a cidoc:E39_Actor .
```

**Explanation**:
- Multiple receiving parties share in the acquisition
- All three institutions jointly receive title
- The transformation handles multiple values correctly

---

## Comparison with Related Properties

### P70.22 vs P70.21 (indicates conceding party)

| Aspect | P70.22 (Receiving Party) | P70.21 (Conceding Party) |
|--------|--------------------------|--------------------------|
| **Used in** | Cessions, Declarations, Donations, Dowries | Cessions only |
| **Semantic Role** | Recipient, acquirer, addressee | Transferor, grantor |
| **CIDOC Path (Cessions)** | P14_carried_out_by (co-participant) | P14_carried_out_by (co-participant) |
| **Direction** | Receives rights/property | Transfers rights/property |
| **Legal Position** | Gains rights | Relinquishes rights |

### P70.22 vs P70.32 (indicates donor)

| Aspect | P70.22 (Receiving Party) | P70.32 (Donor) |
|--------|--------------------------|----------------|
| **Used in** | Donations, Dowries | Donations, Dowries |
| **Semantic Role** | Donee, beneficiary | Donor, benefactor |
| **CIDOC Path** | P22_transferred_title_to | P23_transferred_title_from |
| **Direction** | Receives property | Gives property |
| **Motivation** | Benefits from gift | Provides gift voluntarily |

### P70.22 vs P70.24 (indicates declarant)

| Aspect | P70.22 (Receiving Party) | P70.24 (Declarant) |
|--------|--------------------------|---------------------|
| **Used in** | Declarations | Declarations only |
| **Semantic Role** | Addressee, target | Speaker, maker of statement |
| **CIDOC Path** | P01_has_domain | P14_carried_out_by |
| **Agency** | Passive recipient | Active speaker |
| **Communication** | Receives communication | Initiates communication |

### P70.22 across Document Types

| Document Type | Semantic Role | CIDOC Event | CIDOC Property | Complementary Party Property |
|--------------|---------------|-------------|----------------|------------------------------|
| **Cession** | Rights acquirer | E7_Activity | P14_carried_out_by | P70.21 (conceding party) |
| **Declaration** | Addressee | E7_Activity | P01_has_domain | P70.24 (declarant) |
| **Donation** | Donee | E8_Acquisition | P22_transferred_title_to | P70.32 (donor) |
| **Dowry** | Receiving spouse | E8_Acquisition | P22_transferred_title_to | P70.32 (donor) |

---

## Implementation Patterns

### Pattern 1: Document Type Detection

```python
def get_document_type(data):
    """Determine which type of document we're dealing with."""
    item_type = data.get('@type', '')
    
    # Handle both single type and list of types
    if isinstance(item_type, list):
        if 'gmn:E31_4_Cession_of_Rights_Contract' in item_type:
            return 'cession'
        elif 'gmn:E31_5_Declaration' in item_type:
            return 'declaration'
        elif 'gmn:E31_7_Donation_Contract' in item_type:
            return 'donation'
        elif 'gmn:E31_8_Dowry_Contract' in item_type:
            return 'dowry'
    else:
        if item_type == 'gmn:E31_4_Cession_of_Rights_Contract':
            return 'cession'
        elif item_type == 'gmn:E31_5_Declaration':
            return 'declaration'
        elif item_type == 'gmn:E31_7_Donation_Contract':
            return 'donation'
        elif item_type == 'gmn:E31_8_Dowry_Contract':
            return 'dowry'
    
    return None
```

### Pattern 2: Event Node Creation

```python
def get_or_create_event_node(data, event_type, subject_uri):
    """Get existing event node or create new one."""
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        return data['cidoc:P70_documents'][0]
    
    # Create new event node
    if event_type in ['donation', 'dowry']:
        event_uri = f"{subject_uri}/acquisition"
        event_node = {
            '@id': event_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
    else:
        event_name = 'cession' if event_type == 'cession' else 'declaration'
        event_uri = f"{subject_uri}/{event_name}"
        event_node = {
            '@id': event_uri,
            '@type': 'cidoc:E7_Activity'
        }
        
        # Add activity type
        if event_type == 'cession':
            event_node['cidoc:P2_has_type'] = {
                '@id': 'http://vocab.getty.edu/aat/300417639',
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'transfers of rights'
            }
        elif event_type == 'declaration':
            event_node['cidoc:P2_has_type'] = {
                '@id': 'http://vocab.getty.edu/aat/300027623',
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'declarations'
            }
    
    data['cidoc:P70_documents'] = [event_node]
    return event_node
```

### Pattern 3: Actor Normalization

```python
def normalize_actor(party_obj):
    """Convert party reference to proper actor structure."""
    if isinstance(party_obj, dict):
        party_data = party_obj.copy()
        if '@type' not in party_data:
            party_data['@type'] = 'cidoc:E39_Actor'
    else:
        party_uri = str(party_obj)
        party_data = {
            '@id': party_uri,
            '@type': 'cidoc:E39_Actor'
        }
    return party_data
```

### Pattern 4: Property Assignment by Type

```python
def add_receiving_party_to_event(event_node, party, event_type):
    """Add receiving party to event using appropriate property."""
    party_data = normalize_actor(party)
    
    if event_type in ['donation', 'dowry']:
        # Use P22 for acquisitions
        if 'cidoc:P22_transferred_title_to' not in event_node:
            event_node['cidoc:P22_transferred_title_to'] = []
        event_node['cidoc:P22_transferred_title_to'].append(party_data)
        
    elif event_type == 'declaration':
        # Use P01 for declarations
        if 'cidoc:P01_has_domain' not in event_node:
            event_node['cidoc:P01_has_domain'] = []
        event_node['cidoc:P01_has_domain'].append(party_data)
        
    elif event_type == 'cession':
        # Use P14 for cessions
        if 'cidoc:P14_carried_out_by' not in event_node:
            event_node['cidoc:P14_carried_out_by'] = []
        event_node['cidoc:P14_carried_out_by'].append(party_data)
```

---

## Validation Queries

### SPARQL Query 1: Find All Receiving Parties in Donations

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://genoese-merchants.org/ontology/>

SELECT ?document ?donee ?property
WHERE {
    ?document a gmn:E31_7_Donation_Contract ;
              cidoc:P70_documents ?acquisition .
    
    ?acquisition a cidoc:E8_Acquisition ;
                 cidoc:P22_transferred_title_to ?donee ;
                 cidoc:P24_transferred_title_of ?property .
}
```

### SPARQL Query 2: Compare Declarants and Recipients

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://genoese-merchants.org/ontology/>

SELECT ?document ?declarant ?recipient
WHERE {
    ?document a gmn:E31_5_Declaration ;
              cidoc:P70_documents ?activity .
    
    ?activity a cidoc:E7_Activity ;
              cidoc:P14_carried_out_by ?declarant ;
              cidoc:P01_has_domain ?recipient .
}
```

### SPARQL Query 3: Find Dowry Recipients and Values

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://genoese-merchants.org/ontology/>

SELECT ?document ?donor ?recipient ?property ?value
WHERE {
    ?document a gmn:E31_8_Dowry_Contract ;
              cidoc:P70_documents ?acquisition .
    
    ?acquisition a cidoc:E8_Acquisition ;
                 cidoc:P23_transferred_title_from ?donor ;
                 cidoc:P22_transferred_title_to ?recipient ;
                 cidoc:P24_transferred_title_of ?property .
    
    OPTIONAL {
        ?acquisition cidoc:P177_assigned_property_type ?price .
        ?price cidoc:P90_has_value ?value .
    }
}
```

---

## Additional Semantic Notes

### On the Use of P01_has_domain

The choice of `P01_has_domain` for declarations requires explanation. In CIDOC-CRM, P01 is typically used to model properties where an activity has a "domain" - the entity that the activity is "about" or "concerns" in a particular way. 

For declarations:
- The **declarant** performs the act (P14_carried_out_by)
- The **recipient** is the party to whom it is directed (P01_has_domain)
- This creates an asymmetric, directed relationship

Alternative approaches considered:
- **P01 (chosen)**: Makes recipient the domain/subject of the activity
- **P16** (rejected): Would make recipient an "object used," which is inappropriate for persons
- **Custom property** (rejected): Would diverge from CIDOC-CRM standard

### On Cessions Using P14 for Both Parties

In cession modeling, both the conceding party and receiving party use `P14_carried_out_by`. This models cessions as **bilateral activities** where both parties are active participants in the legal transfer. This is appropriate because:

1. Cessions are **negotiated agreements**, not unilateral acts
2. Both parties must **consent** to the transfer
3. Both have **active roles** in executing the legal transaction
4. This distinguishes cessions from unilateral gifts (donations)

### On Dowries vs Donations

While structurally similar (both use E8_Acquisition), dowries and donations differ in:

**Context**:
- Donations: Voluntary charitable giving
- Dowries: Transfers within marriage arrangements

**Social Function**:
- Donations: Altruistic or religious motivation
- Dowries: Fulfillment of social/family obligations

**Legal Implications**:
- Donations: Unconditional transfer
- Dowries: May have conditions or reversion clauses

The semantic distinction is preserved through:
1. Different document class (E31_7 vs E31_8)
2. Different property names (P70_33 vs P70_34)
3. Contextual metadata in descriptions

---

## Summary

The `gmn:P70_22_indicates_receiving_party` property demonstrates **context-sensitive semantic modeling**:

1. **Single property, multiple meanings**: Adapts role based on document type
2. **Appropriate transformations**: Uses E8 for ownership, E7 for activities
3. **Semantic precision**: Different CIDOC properties (P22, P01, P14) capture nuanced relationships
4. **Integration**: Works seamlessly with complementary properties
5. **Extensibility**: Pattern can extend to additional document types

This approach balances:
- **Simplicity** for data entry (one property name)
- **Precision** in formal semantics (appropriate CRM paths)
- **Consistency** across document types (shared patterns)
- **Compliance** with CIDOC-CRM standards

---

**Version**: 1.0  
**Last Updated**: 2025-10-28  
**Compatibility**: CIDOC-CRM v7.1+, GMN Ontology v1.0+
