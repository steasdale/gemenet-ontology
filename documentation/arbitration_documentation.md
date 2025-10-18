# Arbitration Agreement Transformation Documentation

## Overview

The arbitration agreement properties now follow the same semantic pattern as sales contracts, with all parties and subjects linked through a central **E7_Activity** typed as an arbitration agreement. This creates a coherent structure where:

- The document (E31_3_Arbitration_Agreement) **P70_documents** an E7_Activity
- The E7_Activity has **P2_has_type** pointing to AAT 300417271 (arbitration process)
- All participants and subjects are linked to this central activity

## Semantic Structure

```
E31_3_Arbitration_Agreement (the contract document)
  └─ P70_documents
      └─ E7_Activity (the arbitration agreement activity)
          ├─ P2_has_type → AAT 300417271 (arbitration)
          ├─ P14_carried_out_by → E39_Actor (disputing parties)
          ├─ P14_carried_out_by → E39_Actor (arbitrators)
          └─ P16_used_specific_object → E1_CRM_Entity (dispute subject)
```

Note: Both disputing parties and arbitrators use P14_carried_out_by, as they are all active principals in carrying out the arbitration agreement. The disputing parties agree to submit to arbitration and participate actively in the process, while the arbitrators conduct the arbitration itself.

## Property Transformations

### P70.18 documents disputing party

**Input (shortcut):**
```turtle
<contract> gmn:P70_18_documents_disputing_party <person1> .
<contract> gmn:P70_18_documents_disputing_party <person2> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<contract> cidoc:P70_documents <arbitration1> .
<arbitration1> a cidoc:E7_Activity ;
               cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300417271> ;
               cidoc:P14_carried_out_by <person1> , <person2> .
```

**Notes:**
- Disputing parties are active principals who carry out the arbitration agreement via P14_carried_out_by
- Multiple disputing parties can be added to the same activity
- Range is E39_Actor (can be persons or groups)
- Both disputing parties and arbitrators use P14_carried_out_by, as all are active agents in the arbitration process

### P70.19 documents arbitrator

**Input (shortcut):**
```turtle
<contract> gmn:P70_19_documents_arbitrator <arbitrator1> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<contract> cidoc:P70_documents <arbitration1> .
<arbitration1> a cidoc:E7_Activity ;
               cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300417271> ;
               cidoc:P14_carried_out_by <arbitrator1> .
```

**Notes:**
- Arbitrators carry out the arbitration activity via P14_carried_out_by
- Multiple arbitrators can be appointed
- Range is E39_Actor (typically persons, but could be institutional arbitrators)

### P70.20 documents dispute subject

**Input (shortcut):**
```turtle
<contract> gmn:P70_20_documents_dispute_subject <building1> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<contract> cidoc:P70_documents <arbitration1> .
<arbitration1> a cidoc:E7_Activity ;
               cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300417271> ;
               cidoc:P16_used_specific_object <building1> .
```

**Notes:**
- The dispute subject is linked via P16_used_specific_object
- Range is E1_CRM_Entity (can be physical things, legal objects, rights, debts, etc.)
- Multiple subjects can be referenced if the dispute concerns multiple items

## Complete Example

**Input:**
```turtle
<contract123> a gmn:E31_3_Arbitration_Agreement ;
    gmn:P70_18_documents_disputing_party <merchant_a> , <merchant_b> ;
    gmn:P70_19_documents_arbitrator <judge_c> ;
    gmn:P70_20_documents_dispute_subject <debt_xyz> .
```

**Output:**
```turtle
<contract123> a gmn:E31_3_Arbitration_Agreement ;
    cidoc:P70_documents <contract123/arbitration> .

<contract123/arbitration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300417271> ;
    cidoc:P14_carried_out_by <merchant_a> , <merchant_b> , <judge_c> ;
    cidoc:P16_used_specific_object <debt_xyz> .
```

Note: Both disputing parties (merchant_a, merchant_b) and the arbitrator (judge_c) are listed under P14_carried_out_by, as they are all active principals in the arbitration agreement.

## Comparison with Sales Contracts

| Aspect | Sales Contract | Arbitration Agreement |
|--------|---------------|----------------------|
| Central Event | E8_Acquisition | E7_Activity (typed as arbitration) |
| Main Actors | P23 (seller), P22 (buyer) | P14 (disputing parties), P14 (arbitrators) |
| Object | P24 (property transferred) | P16 (dispute subject) |
| Document Link | P70_documents | P70_documents |

Both structures use P70_documents to link the contract to the main event/activity, creating a consistent pattern across different contract types. In arbitration agreements, all active principals (both disputing parties and arbitrators) are linked via P14_carried_out_by, as they jointly carry out the arbitration process.

## Implementation Notes

1. **Shared Activity**: All three properties share the same E7_Activity node. The transformation functions check if an activity already exists before creating a new one.

2. **Activity Type**: The activity is automatically typed as AAT 300417271 (arbitration process) during transformation.

3. **Order Independence**: The properties can be processed in any order - the transformation will always reference or create the same shared activity.

4. **URI Generation**: The activity URI is generated as `{contract_uri}/arbitration` for consistency.

## Update Required in Main Script

Add these three transformation functions to the `transform_item()` function:

```python
def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    # ... existing transformations ...
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
    # ... rest of transformations ...
    return item
```
