# Correspondence Document Transformation Documentation

## Overview

The Correspondence class (`gmn:E31_6_Correspondence`) follows the same semantic pattern as other GMN document types, with all participants and subjects linked through a central **E7_Activity** typed as correspondence/letter writing. This creates a coherent structure where:

- The document (E31_6_Correspondence) **P70_documents** an E7_Activity
- The E7_Activity has **P2_has_type** pointing to AAT 300026877 (correspondence)
- Sender, origin place, and recipient are linked to the main correspondence activity
- Items held, events described, and event participants are linked through P16_used_specific_object to nested activities/events

## Semantic Structure

```
E31_6_Correspondence (the letter document)
  └─ P70_documents
      └─ E7_Activity (the correspondence/letter-writing activity)
          ├─ P2_has_type → AAT 300026877 (correspondence)
          ├─ P14_carried_out_by → E39_Actor (sender)
          ├─ P7_took_place_at → E53_Place (origin place)
          ├─ P26_moved_to → E53_Place (destination place)
          ├─ P01_has_domain → E39_Actor (recipient)
          └─ P16_used_specific_object → E5_Event (described events)
```

## Property Transformations

### P70.26 indicates sender

**Input (shortcut):**
```turtle
<letter1> gmn:P70_26_indicates_sender <person_john> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<letter1> cidoc:P70_documents <letter1/correspondence> .
<letter1/correspondence> a cidoc:E7_Activity ;
                        cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
                        cidoc:P14_carried_out_by <person_john> .
```

**Notes:**
- The sender is the active agent who carries out the correspondence activity via P14_carried_out_by
- Range is E39_Actor (can be persons or groups)
- AAT 300026877 = correspondence (documents)

---

### P70.27 has address of origin

**Input (shortcut):**
```turtle
<letter1> gmn:P70_27_has_address_of_origin <venice> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<letter1> cidoc:P70_documents <letter1/correspondence> .
<letter1/correspondence> a cidoc:E7_Activity ;
                        cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
                        cidoc:P7_took_place_at <venice> .
```

**Notes:**
- The origin place is where the correspondence activity took place via P7_took_place_at
- Range is E53_Place
- This is the location from which the letter was written and sent

---

### P70.28 indicates recipient

**Input (shortcut):**
```turtle
<letter1> gmn:P70_28_indicates_recipient <person_maria> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<letter1> cidoc:P70_documents <letter1/correspondence> .
<letter1/correspondence> a cidoc:E7_Activity ;
                        cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
                        cidoc:P01_has_domain <person_maria> .
```

**Notes:**
- The recipient is the addressee/target of the communication via P01_has_domain
- Range is E39_Actor (can be persons or groups)
- P01_has_domain (inverse: P01i_is_domain_of) represents the target or subject of an action

---

### P70.29 indicates holder of item

**Input (shortcut):**
```turtle
<letter1> gmn:P70_29_indicates_holder_of_item <person_carlo> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<letter1> cidoc:P70_documents <letter1/correspondence> .
<letter1/correspondence> a cidoc:E7_Activity ;
                        cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
                        cidoc:P16_used_specific_object <letter1/holding_activity> .

<letter1/holding_activity> a cidoc:E7_Activity ;
                          cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300077993> ;
                          cidoc:P14_carried_out_by <person_carlo> .
```

**Notes:**
- The holder is linked through a nested E7_Activity representing the holding/carrying
- The correspondence activity P16_used_specific_object points to the holding activity
- The holder carries out the holding activity via P14_carried_out_by
- AAT 300077993 = holding (grasping, retaining possession)
- This captures third parties mentioned in the letter as possessing items

---

### P70.30 refers to described event

**Input (shortcut):**
```turtle
<letter1> gmn:P70_30_refers_to_described_event <shipment_arrival> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<letter1> cidoc:P70_documents <letter1/correspondence> .
<letter1/correspondence> a cidoc:E7_Activity ;
                        cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
                        cidoc:P16_used_specific_object <shipment_arrival> .

<shipment_arrival> a cidoc:E5_Event .
```

**Notes:**
- Events described in the letter are linked via P16_used_specific_object
- Range is E5_Event (or any of its subclasses like E7_Activity)
- Multiple events can be referenced in a single letter
- The letter documents or narrates these events

---

### P70.31 indicates event participant

**Input (shortcut):**
```turtle
<letter1> gmn:P70_31_indicates_event_participant <merchant_giuseppe> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<letter1> cidoc:P70_documents <letter1/correspondence> .
<letter1/correspondence> a cidoc:E7_Activity ;
                        cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
                        cidoc:P16_used_specific_object <letter1/described_event> .

<letter1/described_event> a cidoc:E5_Event ;
                         cidoc:P11_had_participant <merchant_giuseppe> .
```

**Notes:**
- Event participants are linked through a described event
- The correspondence P16_used_specific_object points to an event
- That event P11_had_participant includes the named party
- If P70.30 was already used to create a specific event, that same event should be reused
---

### P70.31 has address of destination

**Input (shortcut):**
```turtle
<letter1> gmn:P70_31_has_address_of_destination <cairo> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<letter1> cidoc:P70_documents <letter1/correspondence> .
<letter1/correspondence> a cidoc:E7_Activity ;
                        cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
                        cidoc:P26_moved_to <cairo> .
```

**Notes:**
- The destination place is where the letter is sent to via P26_moved_to
- Range is E53_Place
- This is distinct from the origin place (P70.27) and represents the receiving location
- Models the correspondence as a transfer/movement activity from origin to destination
- Event participants mentioned in the letter can be captured using P70_11_documents_referenced_person

---

## Complete Example

**Input (using shortcut properties):**
```turtle
<letter_abc123> a gmn:E31_6_Correspondence ;
    gmn:P70_26_indicates_sender <john_merchant> ;
    gmn:P70_27_has_address_of_origin <venice> ;
    gmn:P70_28_indicates_recipient <maria_trader> ;
    gmn:P70_31_has_address_of_destination <cairo> ;
    gmn:P70_29_indicates_holder_of_item <carlo_porter> ;
    gmn:P70_30_refers_to_described_event <cargo_arrival> ;
    gmn:P70_11_documents_referenced_person <port_official> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<letter_abc123> a gmn:E31_6_Correspondence ;
    cidoc:P70_documents <letter_abc123/correspondence> ;
    cidoc:P67_refers_to <port_official> .

<letter_abc123/correspondence> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300026877> ;
    cidoc:P14_carried_out_by <john_merchant> ;
    cidoc:P7_took_place_at <venice> ;
    cidoc:P26_moved_to <cairo> ;
    cidoc:P01_has_domain <maria_trader> ;
    cidoc:P16_used_specific_object <letter_abc123/holding_activity> ,
                                   <cargo_arrival> .

<letter_abc123/holding_activity> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300077993> ;
    cidoc:P14_carried_out_by <carlo_porter> .

<cargo_arrival> a cidoc:E5_Event .
```doc:P01_has_domain <maria_trader> ;
    cidoc:P16_used_specific_object <letter_abc123/holding_activity> ,
                                   <cargo_arrival> .

<letter_abc123/holding_activity> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300077993> ;
    cidoc:P14_carried_out_by <carlo_porter> .

<cargo_arrival> a cidoc:E5_Event ;
    cidoc:P11_had_participant <port_official> .
```

---

## Comparison with Other GMN Document Types

| Aspect | Sales Contract | Arbitration Agreement | Correspondence |
|--------|---------------|----------------------|----------------|
| Central Event | E8_Acquisition | E7_Activity (arbitration) | E7_Activity (correspondence) |
| Main Actors | P23 (seller), P22 (buyer) | P14 (parties), P14 (arbitrators) | P14 (sender), P01 (recipient) |
| Location | P7 (place of enactment) | - | P7 (origin), P26 (destination) |
| Subject Matter | P24 (property transferred) | P16 (dispute subject) | P16 (described events/items) |
| Document Link | P70_documents | P70_documents | P70_documents |

All document structures use **P70_documents** to link the document to its main activity/event, creating a consistent pattern across different document types.

---

## Key Semantic Distinctions

### Sender vs. Recipient
- **Sender** (P14_carried_out_by): The active agent who writes and sends the letter
- **Recipient** (P01_has_domain): The intended target/addressee of the communication
- This asymmetric relationship captures the directed nature of correspondence

### Main Activity vs. Described Content
- The **correspondence activity** itself (writing and sending the letter)
- **Described events** (P16_used_specific_object): Events narrated within the letter's content
- This distinction separates the act of writing from the content being described

### Direct Participants vs. Mentioned Parties
- **Sender and recipient**: Direct participants in the correspondence activity
- **Holders, event participants**: Third parties mentioned in the letter's narrative
- This captures both the communication structure and its content

---

## Implementation Notes

1. **Shared Activity**: All properties P70.26-P70.28 and P70.31 share the same E7_Activity node representing the main correspondence activity. The transformation should check if this activity already exists before creating a new one.

2. **Activity Type**: The correspondence activity is automatically typed as AAT 300026877 (correspondence) during transformation.

3. **Nested Structures**: Properties P70.29-P70.30 create nested structures to represent content described within the letter, distinct from the letter-writing activity itself.

4. **Referenced Persons**: Use the existing P70_11_documents_referenced_person property to capture any persons mentioned in the letter who are not the sender or recipient, including event participants.

5. **URI Generation**: 
   - Main activity: `{letter_uri}/correspondence`
   - Holding activity: `{letter_uri}/holding_activity`
   - Described events: Either use existing event URIs or generate as `{letter_uri}/described_event`

6. **Order Independence**: The properties can be processed in any order - the transformation will reference or create the shared correspondence activity as needed.

7. **Origin and Destination**: The correspondence models spatial transfer using P7_took_place_at (origin) and P26_moved_to (destination), capturing the movement of the letter from sender location to recipient location.
