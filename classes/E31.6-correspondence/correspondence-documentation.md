# E31.6 Correspondence - Ontology Documentation

## Table of Contents

1. [Class Definition](#class-definition)
2. [Property Specifications](#property-specifications)
3. [Semantic Structure](#semantic-structure)
4. [Transformation Examples](#transformation-examples)
5. [Comparison with Other Document Types](#comparison-with-other-document-types)
6. [Implementation Notes](#implementation-notes)

---

## Class Definition

### gmn:E31_6_Correspondence

**Parent Class**: `cidoc:E31_Document`

**Label**: "E31.6 Correspondence" (English)

**Definition**: A specialized type of E31_Document representing letters and other forms of written correspondence. These are documents written by one party from one location and sent to another party at a different location. Correspondence documents capture communication events between individuals or groups, including the sender, recipient, origin location, destination location, and any events or parties described within the letter's content.

**Scope Note**: This class extends E31_Document to capture the specific structure and participants involved in epistolary communication. Unlike contracts which formalize bilateral agreements, correspondence represents unidirectional or dialogic communication between parties. The class models both the act of writing/sending the letter and the content described within it.

**Examples**:
- A merchant's letter from Venice to Cairo describing cargo shipments
- A diplomatic correspondence between political figures
- Personal letters between family members
- Business correspondence regarding trade negotiations

**Created**: 2025-10-18

---

## Property Specifications

### P70.26 indicates sender

**Property URI**: `gmn:P70_26_indicates_sender`

**Label**: "P70.26 indicates sender" (English)

**Domain**: `gmn:E31_6_Correspondence`

**Range**: `cidoc:E39_Actor`

**Superproperty**: `cidoc:P70_documents`

**Definition**: Simplified property for associating a document with an event described in its content. This captures references within the document to activities, occurrences, or happenings that are narrated or reported.

**CIDOC-CRM Path**:
```
E31_Document > P70_documents > E7_Activity > P16_used_specific_object > E5_Event
```

**Inverse**: N/A

**Quantification**: Many to many (0,n:0,n)

**Scope Note**: The event is part of the document's subject matter, not the document creation activity itself. The documented activity references the described event through P16_used_specific_object. This property has domain E31_Document (not just Correspondence), making it applicable to any document type that describes events - including correspondence, declarations, and contracts. Multiple events can be referenced in a single document.

**Examples**:
- A letter describing a ship's arrival
- A declaration mentioning a previous transaction
- A contract referencing a historical dispute
- Correspondence narrating a political meeting

---

### P70.31 has address of destination

**Property URI**: `gmn:P70_31_has_address_of_destination`

**Label**: "P70.31 has address of destination" (English)

**Domain**: `gmn:E31_6_Correspondence`

**Range**: `cidoc:E53_Place`

**Superproperty**: `cidoc:P70_documents`

**Definition**: Simplified property for associating a correspondence document with the place to which the letter is sent - the destination or location of the recipient.

**CIDOC-CRM Path**:
```
E31_Document > P70_documents > E7_Activity > P26_moved_to > E53_Place
```

**Inverse**: N/A

**Quantification**: Many to one (0,n:0,1)

**Scope Note**: This is distinct from the origin place (P70.27) from which the letter was sent. The use of P26_moved_to models the correspondence as a transfer activity where the letter moves from the origin to the destination. Together, P7_took_place_at (origin) and P26_moved_to (destination) create a complete spatial model of the letter's journey.

**Examples**:
- Cairo - where the recipient will receive the letter
- Constantinople - the destination of diplomatic correspondence
- A rural estate where the addressee resides

---

## Semantic Structure

### Core Correspondence Model

All correspondence properties link through a central **E7_Activity** typed as AAT 300026877 (correspondence):

```
E31_6_Correspondence (the letter document)
  └─ P70_documents
      └─ E7_Activity (the correspondence/letter-writing activity)
          ├─ P2_has_type → http://vocab.getty.edu/aat/300026877
          ├─ P14_carried_out_by → E39_Actor (sender)
          ├─ P7_took_place_at → E53_Place (origin place)
          ├─ P26_moved_to → E53_Place (destination place)
          ├─ P01_has_domain → E39_Actor (recipient)
          └─ P16_used_specific_object → E5_Event | E7_Activity
              └─ [described events and holding activities]
```

### Shared Activity Pattern

Properties P70.26 (sender), P70.27 (origin), P70.28 (recipient), and P70.31 (destination) all share the same E7_Activity node. This creates a unified model of the correspondence event where:

- The **sender** actively carries out the correspondence
- It **takes place** at the origin location
- It **moves to** the destination location
- The **recipient** is the target/domain of the action

### Nested Content Structures

Properties P70.29 (holder) and P70.30 (event) create nested structures via P16_used_specific_object:

**For holders**:
```
E7_Activity (correspondence)
  └─ P16_used_specific_object
      └─ E7_Activity (holding activity)
          ├─ P2_has_type → AAT 300077993 (holding)
          └─ P14_carried_out_by → E39_Actor (holder)
```

**For events**:
```
E7_Activity (correspondence/document activity)
  └─ P16_used_specific_object
      └─ E5_Event (described event)
          └─ [event properties]
```

---

## Transformation Examples

### Example 1: Complete Correspondence

**Input (shortcut properties):**
```turtle
<letter_001> a gmn:E31_6_Correspondence ;
    gmn:P1_1_has_name "Letter from Venice to Cairo" ;
    gmn:P70_26_indicates_sender <person_john_merchant> ;
    gmn:P70_27_has_address_of_origin <place_venice> ;
    gmn:P70_28_indicates_recipient <person_maria_trader> ;
    gmn:P70_31_has_address_of_destination <place_cairo> ;
    gmn:P70_29_indicates_holder_of_item <person_carlo_porter> ;
    gmn:P70_30_refers_to_described_event <event_cargo_arrival> ;
    gmn:P94i_2_has_enactment_date "1450-03-15"^^xsd:date .
```

**Output (CIDOC-CRM compliant):**
```turtle
<letter_001> a gmn:E31_6_Correspondence ;
    cidoc:P1_is_identified_by <letter_001/appellation/12345678> ;
    cidoc:P70_documents <letter_001/correspondence> ;
    cidoc:P94i_was_created_by <letter_001/creation> .

<letter_001/appellation/12345678> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Letter from Venice to Cairo" .

<letter_001/correspondence> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
    cidoc:P14_carried_out_by <person_john_merchant> ;
    cidoc:P7_took_place_at <place_venice> ;
    cidoc:P26_moved_to <place_cairo> ;
    cidoc:P01_has_domain <person_maria_trader> ;
    cidoc:P16_used_specific_object <letter_001/holding_activity_0> ,
                                   <event_cargo_arrival> .

<letter_001/holding_activity_0> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300077993> ;
    cidoc:P14_carried_out_by <person_carlo_porter> .

<letter_001/creation> a cidoc:E65_Creation ;
    cidoc:P4_has_time-span <letter_001/creation/timespan> .

<letter_001/creation/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1450-03-15"^^xsd:date .
```

### Example 2: Minimal Correspondence

**Input:**
```turtle
<letter_002> a gmn:E31_6_Correspondence ;
    gmn:P70_26_indicates_sender <person_antonio> ;
    gmn:P70_28_indicates_recipient <person_lucia> .
```

**Output:**
```turtle
<letter_002> a gmn:E31_6_Correspondence ;
    cidoc:P70_documents <letter_002/correspondence> .

<letter_002/correspondence> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
    cidoc:P14_carried_out_by <person_antonio> ;
    cidoc:P01_has_domain <person_lucia> .
```

**Note**: Even minimal correspondence creates the typed E7_Activity.

### Example 3: Multiple Holders

**Input:**
```turtle
<letter_003> a gmn:E31_6_Correspondence ;
    gmn:P70_26_indicates_sender <person_merchant> ;
    gmn:P70_28_indicates_recipient <person_partner> ;
    gmn:P70_29_indicates_holder_of_item <person_carrier1> ,
                                        <person_carrier2> .
```

**Output:**
```turtle
<letter_003> a gmn:E31_6_Correspondence ;
    cidoc:P70_documents <letter_003/correspondence> .

<letter_003/correspondence> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
    cidoc:P14_carried_out_by <person_merchant> ;
    cidoc:P01_has_domain <person_partner> ;
    cidoc:P16_used_specific_object <letter_003/holding_activity_0> ,
                                   <letter_003/holding_activity_1> .

<letter_003/holding_activity_0> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300077993> ;
    cidoc:P14_carried_out_by <person_carrier1> .

<letter_003/holding_activity_1> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300077993> ;
    cidoc:P14_carried_out_by <person_carrier2> .
```

**Note**: Each holder gets a separate holding activity with unique URI.

### Example 4: P70.30 with Non-Correspondence Document

**Input:**
```turtle
<declaration_004> a gmn:E31_5_Declaration ;
    gmn:P70_24_indicates_declarant <person_official> ;
    gmn:P70_30_refers_to_described_event <event_taxation> .
```

**Output:**
```turtle
<declaration_004> a gmn:E31_5_Declaration ;
    cidoc:P70_documents <declaration_004/declaration> .

<declaration_004/declaration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300027623> ;
    cidoc:P14_carried_out_by <person_official> ;
    cidoc:P16_used_specific_object <event_taxation> .
```

**Note**: P70.30 works with any E31_Document subclass.

---

## Comparison with Other Document Types

### Semantic Comparison Table

| Aspect | Sales Contract | Arbitration | Correspondence |
|--------|---------------|-------------|----------------|
| **Parent Class** | E31_1_Contract | E31_1_Contract | E31_Document |
| **Central Event** | E8_Acquisition | E7_Activity | E7_Activity |
| **Event Type** | (acquisition) | AAT 300417271 | AAT 300026877 |
| **Main Actors** | P23 (seller), P22 (buyer) | P14 (parties & arbitrators) | P14 (sender), P01 (recipient) |
| **Location** | P7 (enactment place) | - | P7 (origin), P26 (destination) |
| **Subject Matter** | P24 (property) | P16 (dispute subject) | P16 (events/items) |
| **Nature** | Bilateral transfer | Multi-party agreement | Unidirectional communication |

### Property Pattern Comparison

**Sales Contract Pattern**:
```
Document → Acquisition → Property/Parties
```

**Arbitration Pattern**:
```
Document → Activity(arbitration) → Parties/Subject
```

**Correspondence Pattern**:
```
Document → Activity(correspondence) → Sender/Recipient/Places
                                   → Described Content
```

### Key Distinguishing Features

**Correspondence Unique Aspects**:
1. **Spatial Transfer Model**: Uses both P7 (origin) and P26 (destination)
2. **Asymmetric Participants**: Sender (P14) vs Recipient (P01)
3. **Nested Content**: Described events and holders via P16
4. **Unidirectional Flow**: From sender to recipient (unlike bilateral contracts)

---

## Implementation Notes

### URI Generation Patterns

**Main Activity**:
```
{document_uri}/correspondence
```

**Holding Activities**:
```
{document_uri}/holding_activity_0
{document_uri}/holding_activity_1
...
```

**Example**:
```
http://example.org/letters/letter123/correspondence
http://example.org/letters/letter123/holding_activity_0
```

### Activity Reuse Logic

All transformation functions check for existing correspondence activity:

```python
existing_activity = None
if 'cidoc:P70_documents' in data:
    for activity in data['cidoc:P70_documents']:
        if activity.get('@id', '').endswith('/correspondence'):
            existing_activity = activity
            break
```

This ensures all properties share the same activity node.

### Order Independence

Properties can be processed in any order. The transformation functions:
1. Check if activity exists
2. Create if needed
3. Add their specific property
4. Return modified data

### Type Inference

The E7_Activity is automatically typed as AAT 300026877 (correspondence) when created by any correspondence property transformation.

### Validation Points

After transformation, verify:
- [ ] Single correspondence activity created
- [ ] Activity has P2_has_type pointing to AAT 300026877
- [ ] Sender linked via P14_carried_out_by
- [ ] Recipient linked via P01_has_domain
- [ ] Places linked via P7 and P26
- [ ] Holders create separate nested E7_Activity instances
- [ ] Events linked via P16_used_specific_object

### Integration with Existing Properties

Correspondence documents can use all standard E31_Document properties:

- **P1_1_has_name**: Modern cataloging name
- **P102_1_has_title**: Original letter title/opening
- **P94i_1_was_created_by**: Scribe/author
- **P94i_2_has_enactment_date**: Date written
- **P94i_3_has_place_of_enactment**: Place of writing (alternative to P70.27)
- **P138i_1_has_representation**: Digital image
- **P46i_1_is_contained_in**: Archival location
- **P70_11_documents_referenced_person**: Persons mentioned in content

### Performance Considerations

- Each correspondence document creates 1 main E7_Activity
- Each holder creates 1 additional nested E7_Activity
- Each event reference adds 1 E5_Event link
- Typical correspondence: 2-5 total nodes created

---

## AAT Terms Reference

### Primary Terms

| AAT ID | Term | Usage |
|--------|------|-------|
| 300026877 | correspondence | Main correspondence activity type |
| 300077993 | holding | Holding activity type |

### Related Terms (for context)

| AAT ID | Term | Usage |
|--------|------|-------|
| 300404650 | names | For P1_1_has_name |
| 300026915 | letters (correspondence) | Alternative term for correspondence |

---

## Best Practices

### When to Use Correspondence

Use E31.6_Correspondence for:
- ✓ Letters between individuals
- ✓ Business correspondence
- ✓ Diplomatic communications
- ✓ Personal epistolary exchanges
- ✓ Official communications sent between parties

Do NOT use for:
- ✗ Contracts (use E31_1_Contract or subclasses)
- ✗ Official declarations not addressed to specific parties (use E31_5_Declaration)
- ✗ Literary letters never sent (use appropriate literary class)

### Property Selection Guidelines

**P70.26 (sender)**: 
- Use for the authorial voice
- If dictated, use sender for dictator, P94i_1 for scribe

**P70.27 vs P94i_3**: 
- P70.27 for correspondence origin
- P94i_3 for document creation place
- Often the same, but can differ

**P70.29 (holder)**:
- Only for holders *mentioned in the letter*
- Not for archival holders (use P46i_1)

**P70.30 (event)**:
- For events described/narrated in content
- Not for the correspondence act itself

### Data Entry Tips

1. **Minimum Required**: Sender and recipient
2. **Highly Recommended**: Origin and destination places, date
3. **Optional but Valuable**: Holders, described events, referenced persons
4. **Always Include**: Modern name (P1_1) for findability

---

## Version History

**Version 1.0** (2025-10-18)
- Initial release
- Six properties defined
- Full transformation support
- Complete documentation

---

## References

- CIDOC-CRM v7.1: http://www.cidoc-crm.org/
- Getty AAT: http://vocab.getty.edu/
- GMN Project Documentation: [internal reference]

---

**Document Status**: Final  
**Last Updated**: 2025-10-18  
**Maintainer**: GMN Ontology Teamating a correspondence document with the party who writes and sends the letter. This is the author and initiator of the communication.

**CIDOC-CRM Path**: 
```
E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
```

**Inverse**: N/A

**Quantification**: Many to many (0,n:0,n)

**Implicit Type**: AAT 300026877 (correspondence)

**Scope Note**: The sender is the active party who carries out the writing and sending activity. This can be an individual person or a group acting as the authorial voice. In cases where a letter is dictated to a scribe, the sender is the person dictating, not the scribe (use P94i_1_was_created_by for the scribe).

**Examples**:
- John the merchant is the sender of a letter about trade goods
- The Doge's office is the sender of an official decree
- A family member writing to relatives abroad

---

### P70.27 has address of origin

**Property URI**: `gmn:P70_27_has_address_of_origin`

**Label**: "P70.27 has address of origin" (English)

**Domain**: `gmn:E31_6_Correspondence`

**Range**: `cidoc:E53_Place`

**Superproperty**: `cidoc:P70_documents`

**Definition**: Simplified property for associating a correspondence document with the place from which the letter originates and is sent.

**CIDOC-CRM Path**:
```
E31_Document > P70_documents > E7_Activity > P7_took_place_at > E53_Place
```

**Inverse**: N/A

**Quantification**: Many to one (0,n:0,1)

**Scope Note**: The correspondence activity (letter writing/sending) took place at this location. This is typically the location of the sender at the time of writing. Together with P70.31 (destination), this models the spatial transfer of the letter.

**Examples**:
- Venice - a merchant writes from Venice
- The Genoese quarter in Pera
- A monastery in the countryside

---

### P70.28 indicates recipient

**Property URI**: `gmn:P70_28_indicates_recipient`

**Label**: "P70.28 indicates recipient" (English)

**Domain**: `gmn:E31_6_Correspondence`

**Range**: `cidoc:E39_Actor`

**Superproperty**: `cidoc:P70_documents`

**Definition**: Simplified property for associating a correspondence document with the intended recipient of the letter. This is the party to whom the letter is addressed and directed.

**CIDOC-CRM Path**:
```
E31_Document > P70_documents > E7_Activity > P01_has_domain > E39_Actor
```

**Inverse**: `cidoc:P01i_is_domain_of`

**Quantification**: Many to many (0,n:0,n)

**Scope Note**: The recipient is the target or addressee of the communication activity. Use of P01_has_domain indicates that the recipient is the "subject" or target of the correspondence action. This is semantically different from P14_carried_out_by (sender), establishing an asymmetric relationship appropriate for directed communication.

**Examples**:
- Maria the trader receiving business correspondence
- A government official receiving a petition
- Multiple family members as co-recipients

---

### P70.29 indicates holder of item

**Property URI**: `gmn:P70_29_indicates_holder_of_item`

**Label**: "P70.29 indicates holder of item" (English)

**Domain**: `gmn:E31_6_Correspondence`

**Range**: `cidoc:E39_Actor`

**Superproperty**: `cidoc:P70_documents`

**Definition**: Simplified property for associating a correspondence document with a party named as holding or carrying an item described in the letter's content.

**CIDOC-CRM Path**:
```
E31_Document > P70_documents > E7_Activity > P16_used_specific_object > E7_Activity > P14_carried_out_by > E39_Actor
```

**Inverse**: N/A

**Quantification**: Many to many (0,n:0,n)

**Implicit Type**: AAT 300077993 (holding)

**Scope Note**: This captures references within the correspondence to individuals or groups who possess, transport, or maintain custody of objects, documents, or goods mentioned in the letter. This is distinct from the letter's sender and recipient - it refers to third parties mentioned in the letter's narrative. The nested E7_Activity represents the holding/carrying activity described in the letter, not the correspondence activity itself.

**Examples**:
- A porter carrying goods mentioned in the letter
- A factor holding documents for safekeeping
- A ship captain transporting cargo described in the correspondence

---

### P70.30 refers to described event

**Property URI**: `gmn:P70_30_refers_to_described_event`

**Label**: "P70.30 refers to described event" (English)

**Domain**: `cidoc:E31_Document`

**Range**: `cidoc:E5_Event`

**Superproperty**: `cidoc:P70_documents`

**Definition**: Simplified property for associ