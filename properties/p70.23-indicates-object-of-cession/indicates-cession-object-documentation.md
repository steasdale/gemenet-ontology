# Ontology Documentation: P70.23 Indicates Object of Cession

Complete semantic documentation for the `gmn:P70_23_indicates_object_of_cession` property in the GMN ontology.

---

## Table of Contents

1. [Property Definition](#property-definition)
2. [Semantic Structure](#semantic-structure)
3. [Domain and Range](#domain-and-range)
4. [CIDOC-CRM Mapping](#cidoc-crm-mapping)
5. [Legal Object Types](#legal-object-types)
6. [Transformation Examples](#transformation-examples)
7. [Integration with Related Properties](#integration-with-related-properties)
8. [Comparison with Other Contracts](#comparison-with-other-contracts)
9. [Use Cases](#use-cases)

---

## Property Definition

### Basic Information

**URI**: `gmn:P70_23_indicates_object_of_cession`

**Label**: "P70.23 indicates object of cession" (English)

**Definition**: Simplified property for associating a cession of rights contract with the legal rights, claims, or obligations being transferred. This can include rights to collect debts, rights to use property (usufruct), rights of ownership over some object, claims arising from other contracts, inheritance rights, or any other legal interests.

**Type**: 
- `owl:ObjectProperty`
- `rdf:Property`

**Subproperty of**: `cidoc:P70_documents`

**Created**: 2025-10-18

**See Also**: 
- `cidoc:P70_documents`
- `cidoc:P16_used_specific_object`

---

## Semantic Structure

### Purpose

This property serves as a convenience shortcut for data entry, allowing users to directly associate a cession contract document with the legal object being transferred without manually creating the intermediate E7_Activity structure required by CIDOC-CRM.

### Design Rationale

1. **Simplification**: Reduces data entry complexity by eliminating multiple intermediate nodes
2. **Clarity**: Makes the relationship between document and legal object explicit
3. **Consistency**: Follows the same pattern as other GMN convenience properties
4. **Reversibility**: Transforms cleanly to full CIDOC-CRM structure

### Transformation Philosophy

The property is designed for **convenience during data entry** but must be **transformed to full CIDOC-CRM structure** for formal compliance and interoperability. The transformation is automatic and lossless.

---

## Domain and Range

### Domain

**Class**: `gmn:E31_4_Cession_of_Rights_Contract`

**Description**: Legal documents that record the transfer of rights, claims, or obligations from one party to another.

**Characteristics**:
- Subclass of `cidoc:E31_Document`
- Specific to rights transfers (not physical property)
- May or may not involve payment
- Common in historical Genoese notarial records

### Range

**Class**: `cidoc:E72_Legal_Object`

**Description**: Represents legal rights, claims, obligations, or any other legal interests that can be possessed, transferred, or enforced.

**CIDOC-CRM Definition**: "This class comprises those material or immaterial items to which instances of E30 Right, such as the right of ownership or use, can be applied."

**Includes**:
- Rights to collect debts (creditor rights)
- Usufruct rights (rights to use property)
- Ownership rights over objects
- Contract claims
- Inheritance rights
- Lease rights
- Water rights
- Mining rights
- Any other transferable legal interest

**Excludes**:
- Physical objects themselves (use E18_Physical_Thing)
- The rights holders (use E39_Actor)
- The activities of exercising rights (use E7_Activity)

---

## CIDOC-CRM Mapping

### Full Path

```
E31_Document (Cession Contract)
  |
  | cidoc:P70_documents
  |
  v
E7_Activity (Cession/Transfer Activity)
  |
  | cidoc:P2_has_type
  |
  v
E55_Type (AAT 300417639: "transfer of rights")
  
E7_Activity (same as above)
  |
  | cidoc:P16_used_specific_object
  |
  v
E72_Legal_Object (The rights/claims being transferred)
```

### Visual Diagram

```
┌─────────────────────────────────────┐
│  E31_4_Cession_of_Rights_Contract  │
│         <cession_doc>               │
└──────────────┬──────────────────────┘
               │ P70_documents
               v
┌─────────────────────────────────────┐
│         E7_Activity                 │
│      <cession_doc/cession>          │
│                                     │
│  P2_has_type: AAT 300417639        │
│  (transfer of rights)               │
└──────────────┬──────────────────────┘
               │ P16_used_specific_object
               v
┌─────────────────────────────────────┐
│       E72_Legal_Object              │
│    <debt_claim> or <right>          │
└─────────────────────────────────────┘
```

### Property Mappings

| GMN Shortcut | CIDOC-CRM Path | Direction |
|--------------|----------------|-----------|
| P70.23 | P70_documents > P16_used_specific_object | Outgoing from document |

### Activity Typing

The E7_Activity node is typed using the Getty AAT:
- **URI**: `http://vocab.getty.edu/aat/300417639`
- **Label**: "transfer of rights" / "cession"
- **Description**: The act of transferring legal rights or claims from one party to another

---

## Legal Object Types

### Common Categories

#### 1. Debt Collection Rights

**Description**: Rights to collect money owed by a third party

**Example**:
```turtle
<debt_claim_001> a cidoc:E72_Legal_Object ;
    rdfs:label "Right to collect 500 lire from Pietro" ;
    cidoc:P2_has_type <concept_debt_claim> .
```

**Use Case**: Giovanni owes Marco 500 lire. Marco transfers his right to collect this debt to Lucia.

#### 2. Usufruct Rights

**Description**: Rights to use and benefit from property owned by another

**Example**:
```turtle
<usufruct_warehouse> a cidoc:E72_Legal_Object ;
    rdfs:label "Usufruct right over warehouse in Porto" ;
    cidoc:P2_has_type <concept_usufruct> ;
    cidoc:P67_refers_to <warehouse_porto> .
```

**Use Case**: Antonio has usufruct rights over a warehouse and transfers these rights to Maria.

#### 3. Ownership Rights

**Description**: Rights of ownership or partial ownership over property

**Example**:
```turtle
<ownership_share> a cidoc:E72_Legal_Object ;
    rdfs:label "One-third ownership share in vineyard" ;
    cidoc:P2_has_type <concept_ownership_right> ;
    cidoc:P67_refers_to <vineyard_chiavari> .
```

**Use Case**: Stefano owns 1/3 of a vineyard and transfers this ownership share to his nephew.

#### 4. Contract Claims

**Description**: Rights arising from other contracts (future payments, delivery rights, etc.)

**Example**:
```turtle
<contract_claim> a cidoc:E72_Legal_Object ;
    rdfs:label "Claim to future wheat deliveries from 1445 lease" ;
    cidoc:P2_has_type <concept_contract_claim> ;
    cidoc:P67_refers_to <lease_contract_1445> .
```

**Use Case**: A lease contract entitles the holder to receive wheat payments; this entitlement is transferred.

#### 5. Inheritance Rights

**Description**: Rights to inherit property or assets

**Example**:
```turtle
<inheritance_right> a cidoc:E72_Legal_Object ;
    rdfs:label "Right to inherit father's estate" ;
    cidoc:P2_has_type <concept_inheritance_right> .
```

**Use Case**: A son transfers his right to inherit from his father to his brother.

### Distinguishing Legal Objects from Physical Objects

| Aspect | Legal Object (E72) | Physical Object (E18) |
|--------|-------------------|----------------------|
| Nature | Intangible right or claim | Tangible physical thing |
| Examples | Right to collect debt, usufruct right | House, vineyard, coins |
| Transfer | Cession of rights | Transfer of title/ownership |
| Property | P70.23 (indicates object of cession) | P70.3 (documents transfer of) |
| Activity | E7_Activity | E8_Acquisition |

---

## Transformation Examples

### Example 1: Simple Debt Right Cession

**Input (GMN Shortcut):**
```turtle
<cession001> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_23_indicates_object_of_cession <debt_claim_123> .

<debt_claim_123> a cidoc:E72_Legal_Object ;
    rdfs:label "Right to collect 200 lire from Matteo" .
```

**Output (CIDOC-CRM Compliant):**
```turtle
<cession001> a gmn:E31_4_Cession_of_Rights_Contract ;
    cidoc:P70_documents <cession001/cession> .

<cession001/cession> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417639> ;
    cidoc:P16_used_specific_object <debt_claim_123> .

<debt_claim_123> a cidoc:E72_Legal_Object ;
    rdfs:label "Right to collect 200 lire from Matteo" .
```

### Example 2: Usufruct Right Cession

**Input (GMN Shortcut):**
```turtle
<cession002> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_23_indicates_object_of_cession <usufruct_house> .

<usufruct_house> a cidoc:E72_Legal_Object ;
    rdfs:label "Usufruct of house in Genoa city center" ;
    cidoc:P67_refers_to <house_piazza_banchi> .
```

**Output (CIDOC-CRM Compliant):**
```turtle
<cession002> a gmn:E31_4_Cession_of_Rights_Contract ;
    cidoc:P70_documents <cession002/cession> .

<cession002/cession> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417639> ;
    cidoc:P16_used_specific_object <usufruct_house> .

<usufruct_house> a cidoc:E72_Legal_Object ;
    rdfs:label "Usufruct of house in Genoa city center" ;
    cidoc:P67_refers_to <house_piazza_banchi> .
```

### Example 3: Multiple Legal Objects

**Input (GMN Shortcut):**
```turtle
<cession003> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_23_indicates_object_of_cession <debt_claim_1> , <debt_claim_2> .
```

**Output (CIDOC-CRM Compliant):**
```turtle
<cession003> a gmn:E31_4_Cession_of_Rights_Contract ;
    cidoc:P70_documents <cession003/cession> .

<cession003/cession> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417639> ;
    cidoc:P16_used_specific_object <debt_claim_1> , <debt_claim_2> .
```

### Example 4: Complete Cession with All Properties

**Input (GMN Shortcut):**
```turtle
<cession004> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_21_indicates_conceding_party <giovanni_merchant> ;
    gmn:P70_22_indicates_receiving_party <marco_banker> ;
    gmn:P70_23_indicates_object_of_cession <debt_claim_pietro> .

<giovanni_merchant> a cidoc:E21_Person ;
    rdfs:label "Giovanni, merchant" .

<marco_banker> a cidoc:E21_Person ;
    rdfs:label "Marco, banker" .

<debt_claim_pietro> a cidoc:E72_Legal_Object ;
    rdfs:label "Right to collect 500 lire from Pietro" .
```

**Output (CIDOC-CRM Compliant):**
```turtle
<cession004> a gmn:E31_4_Cession_of_Rights_Contract ;
    cidoc:P70_documents <cession004/cession> .

<cession004/cession> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/aat/300417639> ;
    cidoc:P14_carried_out_by <giovanni_merchant> , <marco_banker> ;
    cidoc:P16_used_specific_object <debt_claim_pietro> .

<giovanni_merchant> a cidoc:E21_Person ;
    rdfs:label "Giovanni, merchant" .

<marco_banker> a cidoc:E21_Person ;
    rdfs:label "Marco, banker" .

<debt_claim_pietro> a cidoc:E72_Legal_Object ;
    rdfs:label "Right to collect 500 lire from Pietro" .
```

**Note**: All three properties (P70.21, P70.22, P70.23) share the same E7_Activity node.

---

## Integration with Related Properties

### Cession Property Trio

The object of cession property works in concert with two other cession properties:

#### P70.21: Indicates Conceding Party

**Path**: E31 > P70 > E7 > P14 > E39 (conceding party)

**Role**: The party transferring/ceding the rights

#### P70.22: Indicates Receiving Party  

**Path**: E31 > P70 > E7 > P14 > E39 (receiving party)

**Role**: The party receiving the rights (for cessions)

#### P70.23: Indicates Object of Cession

**Path**: E31 > P70 > E7 > P16 > E72 (legal object)

**Role**: The rights/claims being transferred

### Shared Activity Node

All three properties reference the **same E7_Activity** node:

```turtle
<cession_doc> a gmn:E31_4_Cession_of_Rights_Contract ;
    cidoc:P70_documents <cession_doc/cession> .

<cession_doc/cession> a cidoc:E7_Activity ;
    cidoc:P2_has_type <AAT_300417639> ;
    cidoc:P14_carried_out_by <conceding_party> ;    # From P70.21
    cidoc:P14_carried_out_by <receiving_party> ;    # From P70.22
    cidoc:P16_used_specific_object <legal_object> . # From P70.23
```

### Transformation Order

The transformation functions check for an existing activity before creating a new one, ensuring all properties share the same node regardless of processing order.

---

## Comparison with Other Contracts

### Cession vs. Sales Contract

| Aspect | Cession Contract | Sales Contract |
|--------|-----------------|----------------|
| Central Event | E7_Activity (cession) | E8_Acquisition (sale) |
| Object Type | E72_Legal_Object (rights) | E18_Physical_Thing (property) |
| Object Property | P16_used_specific_object | P24_transferred_title_of |
| Nature | Transfer of rights/claims | Transfer of physical property |
| Payment | Variable (may or may not) | Typically involves payment |

**Example Comparison:**

*Cession*: Giovanni transfers his *right to collect a debt* from Pietro to Marco.

*Sale*: Giovanni transfers *ownership of a house* from himself to Marco.

### Cession vs. Donation Contract

| Aspect | Cession Contract | Donation Contract |
|--------|-----------------|-------------------|
| Central Event | E7_Activity | E8_Acquisition |
| Object Type | E72_Legal_Object | E18_Physical_Thing |
| Object Property | P70.23 | P70.33 |
| Nature | Rights transfer | Gift of property |
| Payment | Variable | None (gratuitous) |

### Cession vs. Dowry Contract

| Aspect | Cession Contract | Dowry Contract |
|--------|-----------------|----------------|
| Central Event | E7_Activity | E8_Acquisition |
| Object Type | E72_Legal_Object | E18_Physical_Thing |
| Object Property | P70.23 | P70.34 |
| Context | General rights transfer | Marriage-related transfer |

---

## Use Cases

### Use Case 1: Debt Assignment

**Scenario**: A merchant needs liquidity and sells his right to collect a future debt to a banker.

**Parties**:
- **Conceding Party**: Marco (merchant creditor)
- **Receiving Party**: Antonio (banker)
- **Object**: Right to collect 1000 lire from Pietro (due in 6 months)

**Modeling**:
```turtle
<cession_debt_001> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_21_indicates_conceding_party <marco_merchant> ;
    gmn:P70_22_indicates_receiving_party <antonio_banker> ;
    gmn:P70_23_indicates_object_of_cession <debt_right_pietro> .

<debt_right_pietro> a cidoc:E72_Legal_Object ;
    rdfs:label "Right to collect 1000 lire from Pietro due 1445-12-25" ;
    cidoc:P2_has_type <concept_debt_collection_right> .
```

### Use Case 2: Usufruct Transfer

**Scenario**: A widow holds usufruct rights over her deceased husband's property and transfers these rights to her son.

**Parties**:
- **Conceding Party**: Maria (widow)
- **Receiving Party**: Giovanni (son)
- **Object**: Usufruct of farmland in Chiavari

**Modeling**:
```turtle
<cession_usufruct_001> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_21_indicates_conceding_party <maria_widow> ;
    gmn:P70_22_indicates_receiving_party <giovanni_son> ;
    gmn:P70_23_indicates_object_of_cession <usufruct_farmland> .

<usufruct_farmland> a cidoc:E72_Legal_Object ;
    rdfs:label "Usufruct of farmland in Chiavari" ;
    cidoc:P2_has_type <concept_usufruct> ;
    cidoc:P67_refers_to <farmland_chiavari> .

<farmland_chiavari> a gmn:E22_3_Land_Parcel ;
    rdfs:label "Farmland in Chiavari, 5 hectares" .
```

### Use Case 3: Inheritance Right Transfer

**Scenario**: A brother renounces his inheritance rights in favor of his sister.

**Parties**:
- **Conceding Party**: Pietro (brother)
- **Receiving Party**: Caterina (sister)
- **Object**: Right to inherit from their father's estate

**Modeling**:
```turtle
<cession_inheritance_001> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_21_indicates_conceding_party <pietro_brother> ;
    gmn:P70_22_indicates_receiving_party <caterina_sister> ;
    gmn:P70_23_indicates_object_of_cession <inheritance_right_father> .

<inheritance_right_father> a cidoc:E72_Legal_Object ;
    rdfs:label "Pietro's right to inherit from father Antonio's estate" ;
    cidoc:P2_has_type <concept_inheritance_right> .
```

### Use Case 4: Contract Claim Transfer

**Scenario**: A landlord transfers his right to receive rent payments from a lease contract to a creditor as debt repayment.

**Parties**:
- **Conceding Party**: Stefano (landlord)
- **Receiving Party**: Lorenzo (creditor)
- **Object**: Right to receive 50 lire annual rent from tenant

**Modeling**:
```turtle
<cession_lease_claim> a gmn:E31_4_Cession_of_Rights_Contract ;
    gmn:P70_21_indicates_conceding_party <stefano_landlord> ;
    gmn:P70_22_indicates_receiving_party <lorenzo_creditor> ;
    gmn:P70_23_indicates_object_of_cession <rent_claim> .

<rent_claim> a cidoc:E72_Legal_Object ;
    rdfs:label "Right to receive 50 lire annual rent from lease contract" ;
    cidoc:P2_has_type <concept_contract_claim> ;
    cidoc:P67_refers_to <lease_contract_1444> .

<lease_contract_1444> a cidoc:E31_Document ;
    rdfs:label "Lease contract of 1444 with tenant Marco" .
```

---

## Implementation Notes

### Activity Node Creation

The transformation function follows this logic:

1. **Check for existing activity**: If `cidoc:P70_documents` already contains an activity, reuse it
2. **Create new activity if needed**: Generate URI as `{contract_uri}/cession`
3. **Add type**: Always add `cidoc:P2_has_type` with AAT 300417639
4. **Add object**: Add legal object to `cidoc:P16_used_specific_object`

### URI Patterns

**Cession Activity**: `{contract_uri}/cession`

**Example**:
- Contract: `http://example.org/notarial_act_1445_03_15`
- Activity: `http://example.org/notarial_act_1445_03_15/cession`

### Multiple Objects Handling

When multiple legal objects are ceded:
```turtle
gmn:P70_23_indicates_object_of_cession <obj1> , <obj2> , <obj3> .
```

Transforms to:
```turtle
cidoc:P16_used_specific_object <obj1> , <obj2> , <obj3> .
```

### Type Inference

If a legal object doesn't have an explicit type, the transformation adds:
```turtle
'@type': 'cidoc:E72_Legal_Object'
```

---

## Best Practices

### DO:
✓ Use for rights, claims, and legal interests  
✓ Ensure the legal object is properly typed as E72_Legal_Object  
✓ Use P67_refers_to to link legal objects to physical things when relevant  
✓ Combine with P70.21 and P70.22 for complete cession modeling  

### DON'T:
✗ Use for physical property (use P70.3 for sales contracts instead)  
✗ Use for donations of physical objects (use P70.33 instead)  
✗ Create multiple activities for the same contract  
✗ Forget to type the legal object  

---

## References

### CIDOC-CRM
- E7_Activity: http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.3
- E72_Legal_Object: http://www.cidoc-crm.org/Entity/E72-Legal-Object/version-7.1.3
- P16_used_specific_object: http://www.cidoc-crm.org/Property/P16-used-specific-object/version-7.1.3

### Getty AAT
- Transfer of rights (300417639): http://vocab.getty.edu/aat/300417639

### Related Documentation
- Cession of Rights Contracts Documentation
- GMN Property Transformation Guide
- CIDOC-CRM Implementation Guidelines

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-28  
**Status**: Approved for Implementation
