# Ontology Documentation: gmn:P70_1_indicates_seller

Complete semantic documentation for the `gmn:P70_1_indicates_seller` property, including the E13 Attribute Assignment pattern, CIDOC-CRM alignment, and transformation examples.

---

## Table of Contents

1. [Property Overview](#property-overview)
2. [Formal Specification](#formal-specification)
3. [CIDOC-CRM Alignment](#cidoc-crm-alignment)
4. [E13 Attribute Assignment Pattern](#e13-attribute-assignment-pattern)
5. [Semantic Model](#semantic-model)
6. [Usage Guidelines](#usage-guidelines)
7. [Transformation Examples](#transformation-examples)
8. [Relationship to Other Properties](#relationship-to-other-properties)

---

## Property Overview

### Purpose

The `gmn:P70_1_indicates_seller` property provides a simplified mechanism for associating sales contract documents with the persons who act as sellers in the sale event. It serves as a convenience property for data entry, abstracting the complexity of the full CIDOC-CRM E13 Attribute Assignment pattern.

### Conceptual Foundation

In this implementation, the transfer of ownership is modeled as an **E7 Activity** (typed as "sale") rather than an E8_Acquisition. The participants' roles (seller, buyer) are assigned using the **E13_Attribute_Assignment** pattern, which provides:

1. **Formal role attribution**: Explicitly documents the assignment of roles
2. **Property type specification**: Identifies the relationship type (P14 carried out by)
3. **Role typing**: Specifies the role (seller, buyer, etc.)
4. **Provenance**: Provides traceability for the attribution

### Historical Context

In medieval and early modern notarial records, the seller is a fundamental party to sales contracts. The E13 pattern allows us to formally document:
- Who the seller is (E21_Person)
- What their role is ("seller")
- What property type connects them to the sale ("P14 carried out by")

---

## Formal Specification

### RDF/OWL Definition

```turtle
gmn:P70_1_indicates_seller
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.1 indicates seller"@en ;
    rdfs:comment "Simplified property for associating a sales contract document with the person who acts as the seller in the sale event. Represents the full CIDOC-CRM path: E70_Document > P70_documents > E7_Activity (typed as 'sale') > P140i_was_attributed_by > E13_Attribute_Assignment > P141_assigned > E21_Person, with P177_assigned_property_of_type indicating 'P14 carried out by' and P14.1_in_the_role_of indicating 'seller'. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The seller is the party transferring ownership of the property being sold."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain cidoc:E70_Document ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P140i_was_attributed_by, cidoc:E13_Attribute_Assignment, cidoc:P141_assigned .
```

### Property Characteristics

| Characteristic | Value |
|----------------|-------|
| **Type** | owl:ObjectProperty |
| **Domain** | cidoc:E70_Document |
| **Range** | cidoc:E21_Person |
| **Cardinality** | 0..* (zero or more) |
| **Functional** | No (multiple sellers allowed) |
| **Inverse Functional** | No |
| **Transitive** | No |
| **Symmetric** | No |

### Constraints

1. **Domain Constraint**: Subject must be a Document (cidoc:E70_Document), typically typed as "sales contract" via P2
2. **Range Constraint**: Object must be a Person (cidoc:E21_Person)
3. **Transformation Required**: Property must be transformed to full CIDOC-CRM with E13 pattern before publishing
4. **Semantic Validity**: Each seller must have legal capacity to transfer title

---

## CIDOC-CRM Alignment

### Full CIDOC-CRM Path

The simplified property represents this complete path:

```
E70_Document (sales contract)
    ↓ P2_has_type → E55_Type ("sales contract")
    ↓ P70_documents
E7_Activity (sale event)
    ↓ P2_has_type → E55_Type ("sale")
    ↓ P140i_was_attributed_by
E13_Attribute_Assignment
    ↓ P141_assigned → E21_Person (seller)
    ↓ P177_assigned_property_of_type → E55_Type ("P14 carried out by")
    ↓ P14.1_in_the_role_of → E55_Type ("seller")
```

### CIDOC-CRM Classes and Properties Used

#### E70_Document
- **Definition**: "Information as a unit, in physical or digital form"
- **GMN Usage**: Base class for sales contract documents
- **Typed via**: P2_has_type with value "sales contract"

#### E7_Activity
- **Definition**: "Intentional human actions and sets of coherent actions"
- **GMN Usage**: Models the sale as an intentional activity
- **Typed via**: P2_has_type with AAT term for "sale" (300054751)

#### E13_Attribute_Assignment
- **Definition**: "The action of associating specific information to objects and concepts"
- **GMN Usage**: Assigns the "carried out by" attribute to the sale, specifying the seller
- **Scope**: Documents the formal attribution of participant roles

#### P70_documents (E70_Document → E7_Activity)
- **Definition**: "This property links a document to the activity it documents"
- **Scope Note**: "Documents may be expressions of activities themselves or may describe activities"
- **GMN Usage**: Links the sales contract to the sale event

#### P140i_was_attributed_by (E7_Activity → E13_Attribute_Assignment)
- **Definition**: Inverse of P140_assigned_attribute_to
- **Scope Note**: Links an entity to the attribute assignment that characterized it
- **GMN Usage**: Links the sale event to its seller attribution

#### P141_assigned (E13_Attribute_Assignment → E21_Person)
- **Definition**: "This property indicates the object that was assigned in an Attribute Assignment"
- **GMN Usage**: Identifies the seller person being assigned to the sale

#### P177_assigned_property_of_type (E13_Attribute_Assignment → E55_Type)
- **Definition**: "This property specifies the type of property that was assigned"
- **GMN Usage**: Specifies that "P14 carried out by" is the property type being assigned

#### P14.1_in_the_role_of (E13_Attribute_Assignment → E55_Type)
- **Definition**: "Qualifier for P14 to specify the role"
- **GMN Usage**: Specifies "seller" as the role

---

## E13 Attribute Assignment Pattern

### Pattern Explanation

The E13_Attribute_Assignment class is used in CIDOC-CRM to document the formal assignment of attributes or properties to entities. This pattern is particularly useful when you need to:

1. **Document provenance** of attribute assignments
2. **Specify the type** of property being assigned
3. **Qualify relationships** with roles or contexts
4. **Support multiple** assignments of the same property type

### Why Use E13 for Seller Attribution?

Traditional approaches might directly link person to activity via P14_carried_out_by. The E13 pattern adds an intermediate attribution node that:

1. **Makes the relationship explicit**: Documents that we are assigning the "carried out by" property
2. **Enables role specification**: Via P14.1, we can specify "seller" vs "buyer" vs other roles
3. **Provides attribution context**: E13 itself can have temporal, spatial, or agent properties
4. **Supports complex scenarios**: Multiple people with different roles

### E13 Structure

```
E7_Activity (the sale event)
  |
  └─ P140i_was_attributed_by
      |
      └─ E13_Attribute_Assignment (the attribution)
          |
          ├─ P141_assigned 
          |   └─ E21_Person (Giovanni Rossi - the seller)
          |
          ├─ P177_assigned_property_of_type
          |   └─ E55_Type ("P14 carried out by")
          |
          └─ P14.1_in_the_role_of
              └─ E55_Type ("seller")
```

This structure reads as:
> "The sale event was attributed by an assignment which assigned Giovanni Rossi as the value of the property 'P14 carried out by' in the role of 'seller'."

### AAT Terms Integration

The pattern uses Getty AAT controlled vocabulary:

1. **Sale Event Type**: `http://vocab.getty.edu/aat/300054751`
   - Label: "sale (event)"
   - Definition: Activities involving the exchange of goods for money

2. **Seller Role**: `http://vocab.getty.edu/aat/300410369`
   - Label: "sellers (people)"
   - Definition: People who sell goods or services

3. **P14 Property**: `http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by`
   - This is the CIDOC-CRM property URI itself used as a type

---

## Semantic Model

### Conceptual Diagram

```
┌─────────────────────────────────┐
│ E70_Document                    │
│ (Sales Contract)                │
│ contract_001                    │
│   P2 → "sales contract"         │
└────────────┬────────────────────┘
             │ P70_documents
             ↓
┌─────────────────────────────────┐
│ E7_Activity                     │
│ (Sale Event)                    │
│ contract_001/sale               │
│   P2 → "sale" (AAT:300054751)   │
└────────────┬────────────────────┘
             │ P140i_was_attributed_by
             ↓
┌─────────────────────────────────┐
│ E13_Attribute_Assignment        │
│ (Seller Attribution)            │
│ contract_001/attribution/...    │
├─────────────────────────────────┤
│ P141_assigned → Person          │
│ P177 → "P14 carried out by"     │
│ P14.1 → "seller" (AAT:300410369)│
└────────────┬────────────────────┘
             │ P141_assigned
             ↓
┌─────────────────────────────────┐
│ E21_Person                      │
│ (Seller)                        │
│ giovanni_rossi                  │
└─────────────────────────────────┘
```

### Simplified vs. Full Model

**Simplified GMN Model**:
```
E70_Document --P70_1_indicates_seller--> E21_Person
```

**Full CIDOC-CRM Model**:
```
E70_Document 
  --P70_documents--> E7_Activity 
    --P140i_was_attributed_by--> E13_Attribute_Assignment
      --P141_assigned--> E21_Person
      --P177_assigned_property_of_type--> E55_Type ("P14")
      --P14.1_in_the_role_of--> E55_Type ("seller")
```

### Multiple Sellers

When multiple persons jointly sell property, each gets a separate E13_Attribute_Assignment:

```
                    ┌──> E13 (Seller 1) ──> Person 1
                    │     ├─ P177 → "P14"
                    │     └─ P14.1 → "seller"
                    │
E7_Activity ────────┼──> E13 (Seller 2) ──> Person 2
  (sale)            │     ├─ P177 → "P14"
                    │     └─ P14.1 → "seller"
                    │
                    └──> E13 (Seller 3) ──> Person 3
                          ├─ P177 → "P14"
                          └─ P14.1 → "seller"
```

All sellers are linked to the same E7_Activity via separate E13_Attribute_Assignment instances, each specifying the "seller" role.

---

## Usage Guidelines

### When to Use This Property

✅ **Use P70_1_indicates_seller when**:
- Recording the primary seller in a sales contract
- The seller is an individual person (not a group/organization)
- Documenting actual ownership transfer
- During initial data entry phase
- You want clear role specification via E13

❌ **Do not use P70_1_indicates_seller for**:
- Procurators/legal representatives (use P70_4_indicates_sellers_procurator)
- Guarantors (use P70_6_indicates_sellers_guarantor)
- Organizations (consider using E74_Group with custom property)
- Witnesses (use P70_15_indicates_witness)
- Referenced persons not involved in transaction (use P70_11_documents_referenced_person)

### Best Practices

1. **Complete Person Data**: Include as much person information as available
   ```json
   {
     "@id": "person_001",
     "@type": "cidoc:E21_Person",
     "cidoc:P1_is_identified_by": [...]
   }
   ```

2. **URI Consistency**: Use consistent URI patterns for persons across contracts

3. **Multiple Sellers**: List all co-sellers using array syntax:
   ```json
   "gmn:P70_1_indicates_seller": [
     {"@id": "person_001"},
     {"@id": "person_002"}
   ]
   ```

4. **Document Typing**: Always include P2_has_type on the E70_Document:
   ```json
   {
     "@type": "cidoc:E70_Document",
     "cidoc:P2_has_type": {
       "@type": "cidoc:E55_Type",
       "rdfs:label": "sales contract"
     }
   }
   ```

5. **Complement with Buyer**: Always pair with P70_2_indicates_buyer for complete transaction

### Data Quality Considerations

- **Verification**: Ensure person is actually the seller (not their representative)
- **Completeness**: Include person identification data when available
- **Consistency**: Use same person URI across related contracts
- **Context**: Consider documenting seller's role if unusual (e.g., executor of estate)

---

## Transformation Examples

### Example 1: Simple Single Seller

**Input (Simplified GMN)**:
```json
{
  "@context": {
    "gmn": "http://example.org/gmn/",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contract/sale_1435_03_15",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "http://example.org/type/sales_contract",
    "@type": "cidoc:E55_Type",
    "rdfs:label": "sales contract"
  },
  "gmn:P70_1_indicates_seller": [
    {
      "@id": "http://example.org/person/giovanni_rossi",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": [
        {
          "@type": "cidoc:E41_Appellation",
          "cidoc:P190_has_symbolic_content": "Giovanni Rossi"
        }
      ]
    }
  ]
}
```

**Output (Full CIDOC-CRM with E13)**:
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "http://example.org/contract/sale_1435_03_15",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "http://example.org/type/sales_contract",
    "@type": "cidoc:E55_Type",
    "rdfs:label": "sales contract"
  },
  "cidoc:P70_documents": [
    {
      "@id": "http://example.org/contract/sale_1435_03_15/sale",
      "@type": "cidoc:E7_Activity",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300054751",
        "@type": "cidoc:E55_Type",
        "rdfs:label": "sale"
      },
      "cidoc:P140i_was_attributed_by": [
        {
          "@id": "http://example.org/contract/sale_1435_03_15/attribution/seller_abc12345",
          "@type": "cidoc:E13_Attribute_Assignment",
          "cidoc:P141_assigned": {
            "@id": "http://example.org/person/giovanni_rossi",
            "@type": "cidoc:E21_Person",
            "cidoc:P1_is_identified_by": [
              {
                "@type": "cidoc:E41_Appellation",
                "cidoc:P190_has_symbolic_content": "Giovanni Rossi"
              }
            ]
          },
          "cidoc:P177_assigned_property_of_type": {
            "@id": "http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "P14 carried out by"
          },
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/aat/300410369",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "seller"
          }
        }
      ]
    }
  ]
}
```

### Example 2: Multiple Co-Sellers

**Input**:
```json
{
  "@id": "http://example.org/contract/sale_1435_04_20",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type"
  },
  "gmn:P70_1_indicates_seller": [
    {
      "@id": "http://example.org/person/marco_bianchi",
      "@type": "cidoc:E21_Person"
    },
    {
      "@id": "http://example.org/person/paolo_verdi",
      "@type": "cidoc:E21_Person"
    }
  ]
}
```

**Output (showing multiple E13 attributions)**:
```json
{
  "@id": "http://example.org/contract/sale_1435_04_20",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type"
  },
  "cidoc:P70_documents": [
    {
      "@id": "http://example.org/contract/sale_1435_04_20/sale",
      "@type": "cidoc:E7_Activity",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300054751",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P140i_was_attributed_by": [
        {
          "@id": "http://example.org/contract/sale_1435_04_20/attribution/seller_xyz11111",
          "@type": "cidoc:E13_Attribute_Assignment",
          "cidoc:P141_assigned": {
            "@id": "http://example.org/person/marco_bianchi",
            "@type": "cidoc:E21_Person"
          },
          "cidoc:P177_assigned_property_of_type": {
            "@id": "http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/aat/300410369",
            "@type": "cidoc:E55_Type"
          }
        },
        {
          "@id": "http://example.org/contract/sale_1435_04_20/attribution/seller_xyz22222",
          "@type": "cidoc:E13_Attribute_Assignment",
          "cidoc:P141_assigned": {
            "@id": "http://example.org/person/paolo_verdi",
            "@type": "cidoc:E21_Person"
          },
          "cidoc:P177_assigned_property_of_type": {
            "@id": "http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/aat/300410369",
            "@type": "cidoc:E55_Type"
          }
        }
      ]
    }
  ]
}
```

### Example 3: Complete Sales Transaction (Seller + Buyer + Object)

**Input**:
```json
{
  "@id": "http://example.org/contract/sale_1435_05_10",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type"
  },
  "gmn:P70_1_indicates_seller": [
    {
      "@id": "http://example.org/person/antonio_ferrari",
      "@type": "cidoc:E21_Person"
    }
  ],
  "gmn:P70_2_indicates_buyer": [
    {
      "@id": "http://example.org/person/francesco_lombardi",
      "@type": "cidoc:E21_Person"
    }
  ],
  "gmn:P70_3_indicates_transfer_of": [
    {
      "@id": "http://example.org/building/casa_via_garibaldi_42",
      "@type": "gmn:E22_1_Building"
    }
  ]
}
```

**Output (showing seller and buyer E13 attributions)**:
```json
{
  "@id": "http://example.org/contract/sale_1435_05_10",
  "@type": "cidoc:E70_Document",
  "cidoc:P2_has_type": {
    "@id": "sales_contract_type",
    "@type": "cidoc:E55_Type"
  },
  "cidoc:P70_documents": [
    {
      "@id": "http://example.org/contract/sale_1435_05_10/sale",
      "@type": "cidoc:E7_Activity",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300054751",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P140i_was_attributed_by": [
        {
          "@id": "http://example.org/contract/sale_1435_05_10/attribution/seller_...",
          "@type": "cidoc:E13_Attribute_Assignment",
          "cidoc:P141_assigned": {
            "@id": "http://example.org/person/antonio_ferrari",
            "@type": "cidoc:E21_Person"
          },
          "cidoc:P177_assigned_property_of_type": {
            "@id": "http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/aat/300410369",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "seller"
          }
        },
        {
          "@id": "http://example.org/contract/sale_1435_05_10/attribution/buyer_...",
          "@type": "cidoc:E13_Attribute_Assignment",
          "cidoc:P141_assigned": {
            "@id": "http://example.org/person/francesco_lombardi",
            "@type": "cidoc:E21_Person"
          },
          "cidoc:P177_assigned_property_of_type": {
            "@id": "http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P14.1_in_the_role_of": {
            "@id": "http://vocab.getty.edu/aat/300239436",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "buyer"
          }
        }
      ],
      "cidoc:P16_used_specific_object": [
        {
          "@id": "http://example.org/building/casa_via_garibaldi_42",
          "@type": "gmn:E22_1_Building"
        }
      ]
    }
  ]
}
```

---

## Relationship to Other Properties

### Complementary Properties

#### gmn:P70_2_indicates_buyer
- **Relationship**: Complementary opposite role
- **Path**: E70 > P70 > E7 > P140i > E13 (with P14.1 role "buyer")
- **Usage**: Always use together to document both parties

#### gmn:P70_3_indicates_transfer_of
- **Relationship**: Complementary object
- **Path**: E70 > P70 > E7 > P16_used_specific_object > E18_Physical_Thing
- **Usage**: Documents what is being transferred in the sale

### Related Agent Properties

#### gmn:P70_4_indicates_sellers_procurator
- **Relationship**: Seller's representative
- **Distinction**: Procurator acts *for* seller; not the actual owner
- **E13 Role**: Would use different role type ("procurator" not "seller")

#### gmn:P70_6_indicates_sellers_guarantor
- **Relationship**: Seller's guarantor
- **Distinction**: Guarantor provides security *for* seller; doesn't own property
- **E13 Role**: Would use role type "guarantor"

### Comparison Table

| Property | Role | E13 Role Type | AAT Term |
|----------|------|---------------|----------|
| **P70.1 Seller** | Principal party | seller | 300410369 |
| P70.2 Buyer | Principal party | buyer | 300239436 |
| P70.4 Procurator | Legal representative | procurator | (custom) |
| P70.6 Guarantor | Security provider | guarantor | 300025245 |

---

## Advanced Topics

### Comparing E13 vs. Direct P14 Approaches

**Direct P14 (not used in GMN)**:
```
E7_Activity --P14_carried_out_by--> E21_Person
```

**E13 Attribution (GMN approach)**:
```
E7_Activity --P140i_was_attributed_by--> E13 --P141--> E21_Person
                                          ├─P177--> "P14"
                                          └─P14.1--> "seller"
```

**Advantages of E13 pattern**:
1. Explicit role specification via P14.1
2. Property type documentation via P177
3. Ability to add attribution metadata (time, place, agent)
4. Clear separation of different participant roles
5. Supports complex scenarios (multiple people, changing roles)

### Extension Possibilities

The E13 pattern supports future extensions such as:

```json
{
  "@type": "cidoc:E13_Attribute_Assignment",
  "cidoc:P141_assigned": { /* seller */ },
  "cidoc:P177_assigned_property_of_type": { /* P14 */ },
  "cidoc:P14.1_in_the_role_of": { /* seller */ },
  "cidoc:P4_has_time-span": { /* when attribution was made */ },
  "cidoc:P14_carried_out_by": { /* who made the attribution */ }
}
```

---

## References

### CIDOC-CRM Documentation
- [E7 Activity](http://www.cidoc-crm.org/Entity/e7-activity/version-7.1.1)
- [E13 Attribute Assignment](http://www.cidoc-crm.org/Entity/e13-attribute-assignment/version-7.1.1)
- [P140i was attributed by](http://www.cidoc-crm.org/Property/p140-assigned-attribute-to/version-7.1.1)
- [P141 assigned](http://www.cidoc-crm.org/Property/p141-assigned/version-7.1.1)
- [P177 assigned property of type](http://www.cidoc-crm.org/Property/p177-assigned-property-of-type/version-7.1.1)

### Getty AAT
- [Sale (event) - 300054751](http://vocab.getty.edu/aat/300054751)
- [Sellers (people) - 300410369](http://vocab.getty.edu/aat/300410369)

### Related GMN Documentation
- E70 Document usage in GMN
- Property transformation documentation
- Data entry guidelines

---

*This documentation should be read in conjunction with the implementation guide and transformation code examples.*
