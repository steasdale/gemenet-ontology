# P70.3 Documents Transfer Of - Ontology Documentation

## Complete Semantic Documentation

---

## Property Definition

### Turtle Syntax

```turtle
# Property: P70.3 documents transfer of
gmn:P70_3_documents_transfer_of
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.3 documents transfer of"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the physical thing (property, object, or person) being transferred. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The range includes buildings (gmn:E22_1_Building), moveable property (gmn:E22_2_Moveable_Property), and persons (E21_Person, for the historical documentation of enslaved persons or other instances where people were treated as property)."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E18_Physical_Thing ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P24_transferred_title_of .
```

### Metadata

| Field | Value |
|-------|-------|
| **URI** | `http://www.genoesemerchantnetworks.com/ontology#P70_3_documents_transfer_of` |
| **Label** | P70.3 documents transfer of |
| **Property Type** | owl:ObjectProperty, rdf:Property |
| **Superproperty** | cidoc:P70_documents |
| **Domain** | gmn:E31_2_Sales_Contract |
| **Range** | cidoc:E18_Physical_Thing |
| **Created** | 2025-10-17 |
| **Status** | Active |

---

## Semantic Structure

### Full CIDOC-CRM Path

The property represents this complete semantic path:

```
E31_Document (Sales Contract)
  ↓ P70_documents
E8_Acquisition (Transfer Event)
  ↓ P24_transferred_title_of
E18_Physical_Thing (Property Being Transferred)
```

### Visual Representation

```
┌─────────────────────────────┐
│   E31_2_Sales_Contract      │
│   (Contract Document)       │
└──────────────┬──────────────┘
               │ P70_documents
               ↓
┌─────────────────────────────┐
│      E8_Acquisition         │
│   (Transfer Transaction)    │
└──┬────────────┬─────────┬───┘
   │            │         │
   │P23         │P22      │P24_transferred_title_of
   │            │         │
   ↓            ↓         ↓
 Seller      Buyer    E18_Physical_Thing
                      (Building, Goods, etc.)
```

### Component Entities

#### 1. E31_2_Sales_Contract (Domain)
The document that records the transaction. This is the subject of the property - the sales contract itself.

**Characteristics:**
- Physical or conceptual document
- Created by notary
- Contains legal formulas
- Records agreement between parties

#### 2. E8_Acquisition (Intermediate Node)
The event of transferring ownership from one party to another.

**Characteristics:**
- Type: Acquisition of property
- Temporal event
- Involves transfer of title
- Can have multiple participants and objects

#### 3. E18_Physical_Thing (Range)
The actual physical thing (or historically, person) being transferred.

**Characteristics:**
- Can be immovable property (buildings)
- Can be movable property (goods)
- Can have identification (name, description)
- Can have location
- Can have measurements or value

---

## Domain and Range Specifications

### Domain: gmn:E31_2_Sales_Contract

**Definition:** Specialized class describing sales contract documents that record the transfer of ownership of property in exchange for payment.

**Hierarchy:**
```
cidoc:E31_Document
  └─ gmn:E31_1_Contract
      └─ gmn:E31_2_Sales_Contract
```

**Usage:** The property can only be applied to instances of gmn:E31_2_Sales_Contract.

**Example:**
```turtle
<https://example.org/contract/sales_001> a gmn:E31_2_Sales_Contract .
```

### Range: cidoc:E18_Physical_Thing

**Definition:** Physical objects of any kind that are documented as being transferred in the sales contract.

**Hierarchy:**
```
cidoc:E18_Physical_Thing
  ├─ gmn:E22_1_Building (immovable property)
  ├─ gmn:E22_2_Moveable_Property (movable goods)
  ├─ cidoc:E21_Person (historical documentation)
  └─ (other E18 subtypes)
```

**Subclasses in GMN Context:**

#### gmn:E22_1_Building
Immovable property including:
- Houses (domus)
- Shops (apotecha)
- Warehouses (magazenum)
- Land parcels (terra)
- Structures and buildings

**Example:**
```turtle
<https://example.org/building/house_42> a gmn:E22_1_Building ;
    cidoc:P1_is_identified_by [
        a cidoc:E41_Appellation ;
        rdfs:label "House on Via Luccoli"
    ] .
```

#### gmn:E22_2_Moveable_Property
Movable objects including:
- Merchandise (goods for trade)
- Equipment and tools
- Furniture
- Ships or cargo
- Any transportable property

**Example:**
```turtle
<https://example.org/goods/silk_001> a gmn:E22_2_Moveable_Property ;
    cidoc:P2_has_type [
        a cidoc:E55_Type ;
        rdfs:label "silk cloth"
    ] .
```

#### cidoc:E21_Person (Historical Context)
In historical documentation, the range includes E21_Person for accurate recording of historical practices where enslaved persons or others were treated as transferable property.

**Note:** This reflects historical reality in primary sources and is necessary for accurate historical documentation, not endorsement of such practices.

---

## Property Characteristics

### Cardinality
- **Minimum:** 0 (optional - a contract may not explicitly list transferred objects)
- **Maximum:** Unbounded (a contract can transfer multiple things)
- **Typical:** 1-3 items per contract

### Transitivity
- **Not Transitive:** The property does not imply transitive relationships

### Symmetry
- **Not Symmetric:** The relationship is directional (contract → thing)

### Functionality
- **Not Functional:** One contract can document multiple things
- **Not Inverse Functional:** Multiple contracts can reference the same thing (e.g., subsequent sales)

---

## Transformation Specification

### Transformation Rules

1. **Locate or Create E8_Acquisition Node**
   - Check if `cidoc:P70_documents` already exists
   - If not, create new E8_Acquisition with URI pattern: `{contract_uri}/acquisition`
   - If exists, reuse existing acquisition node (for integration with P70.1, P70.2)

2. **Initialize P24 Property**
   - Check if `cidoc:P24_transferred_title_of` exists on acquisition
   - If not, initialize as empty array

3. **Process Each Thing**
   - For dict objects: Copy entire object, preserving all properties
   - For string URIs: Create minimal thing object with @id and default type
   - Preserve specific types (E22_1, E22_2) if provided
   - Default to E18_Physical_Thing if no type specified

4. **Add to Acquisition**
   - Append each processed thing to P24_transferred_title_of array

5. **Clean Up**
   - Delete the simplified `gmn:P70_3_documents_transfer_of` property

### Transformation Algorithm

```python
ALGORITHM transform_p70_3(contract):
    IF contract DOES NOT CONTAIN 'gmn:P70_3_documents_transfer_of':
        RETURN contract
    
    things = contract['gmn:P70_3_documents_transfer_of']
    
    # Step 1: Locate or create acquisition node
    IF contract DOES NOT CONTAIN 'cidoc:P70_documents':
        acquisition_uri = contract['@id'] + "/acquisition"
        acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        contract['cidoc:P70_documents'] = [acquisition]
    ELSE:
        acquisition = contract['cidoc:P70_documents'][0]
    
    # Step 2: Initialize P24 array
    IF acquisition DOES NOT CONTAIN 'cidoc:P24_transferred_title_of':
        acquisition['cidoc:P24_transferred_title_of'] = []
    
    # Step 3-4: Process and add things
    FOR EACH thing IN things:
        IF thing IS dict:
            thing_data = COPY(thing)
            IF thing_data DOES NOT CONTAIN '@type':
                thing_data['@type'] = 'cidoc:E18_Physical_Thing'
        ELSE:
            thing_data = {
                '@id': STRING(thing),
                '@type': 'cidoc:E18_Physical_Thing'
            }
        
        APPEND thing_data TO acquisition['cidoc:P24_transferred_title_of']
    
    # Step 5: Clean up
    DELETE contract['gmn:P70_3_documents_transfer_of']
    
    RETURN contract
```

### Type Preservation Logic

The transformation preserves specific types when provided:

| Input Type | Output Type | Notes |
|------------|-------------|-------|
| gmn:E22_1_Building | gmn:E22_1_Building | Preserved |
| gmn:E22_2_Moveable_Property | gmn:E22_2_Moveable_Property | Preserved |
| cidoc:E21_Person | cidoc:E21_Person | Preserved (historical) |
| (no type specified) | cidoc:E18_Physical_Thing | Default |
| (invalid type) | cidoc:E18_Physical_Thing | Fallback |

---

## Usage Examples

### Example 1: Single Building Transfer

**GMN Simplified Input:**
```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "https://genoa.archive/contract/notary_123_doc_45",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "https://genoa.archive/building/soziglia_shop_7",
      "@type": "gmn:E22_1_Building",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "@value": "Shop on Soziglia Street, number 7"
      },
      "cidoc:P53_has_former_or_current_location": {
        "@id": "https://genoa.archive/place/soziglia_street",
        "@type": "cidoc:E53_Place",
        "rdfs:label": "Soziglia Street, Genoa"
      }
    }
  ]
}
```

**CIDOC-CRM Full Output:**
```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/"
  },
  "@id": "https://genoa.archive/contract/notary_123_doc_45",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://genoa.archive/contract/notary_123_doc_45/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "https://genoa.archive/building/soziglia_shop_7",
          "@type": "gmn:E22_1_Building",
          "cidoc:P1_is_identified_by": {
            "@type": "cidoc:E41_Appellation",
            "@value": "Shop on Soziglia Street, number 7"
          },
          "cidoc:P53_has_former_or_current_location": {
            "@id": "https://genoa.archive/place/soziglia_street",
            "@type": "cidoc:E53_Place",
            "rdfs:label": "Soziglia Street, Genoa"
          }
        }
      ]
    }
  ]
}
```

### Example 2: Multiple Items Transfer

**GMN Simplified Input:**
```json
{
  "@id": "https://genoa.archive/contract/notary_88_doc_123",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "https://genoa.archive/building/warehouse_12",
      "@type": "gmn:E22_1_Building",
      "rdfs:label": "Warehouse near the port"
    },
    {
      "@id": "https://genoa.archive/goods/merchandise_234",
      "@type": "gmn:E22_2_Moveable_Property",
      "cidoc:P2_has_type": {
        "@type": "cidoc:E55_Type",
        "@value": "Alum shipment"
      }
    }
  ]
}
```

**CIDOC-CRM Full Output:**
```json
{
  "@id": "https://genoa.archive/contract/notary_88_doc_123",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://genoa.archive/contract/notary_88_doc_123/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "https://genoa.archive/building/warehouse_12",
          "@type": "gmn:E22_1_Building",
          "rdfs:label": "Warehouse near the port"
        },
        {
          "@id": "https://genoa.archive/goods/merchandise_234",
          "@type": "gmn:E22_2_Moveable_Property",
          "cidoc:P2_has_type": {
            "@type": "cidoc:E55_Type",
            "@value": "Alum shipment"
          }
        }
      ]
    }
  ]
}
```

### Example 3: Complete Transaction (with Buyer and Seller)

**GMN Simplified Input:**
```json
{
  "@id": "https://genoa.archive/contract/sale_1447_03_15",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_1_documents_seller": [
    {
      "@id": "https://genoa.archive/person/giovanni_doria",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "@value": "Giovanni Doria"
      }
    }
  ],
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "https://genoa.archive/person/luca_grimaldi",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": {
        "@type": "cidoc:E41_Appellation",
        "@value": "Luca Grimaldi"
      }
    }
  ],
  "gmn:P70_3_documents_transfer_of": [
    {
      "@id": "https://genoa.archive/building/house_vico_dritto_71",
      "@type": "gmn:E22_1_Building",
      "rdfs:label": "House on Vico Dritto di Ponticello"
    }
  ]
}
```

**CIDOC-CRM Full Output:**
```json
{
  "@id": "https://genoa.archive/contract/sale_1447_03_15",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://genoa.archive/contract/sale_1447_03_15/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P23_transferred_title_from": [
        {
          "@id": "https://genoa.archive/person/giovanni_doria",
          "@type": "cidoc:E21_Person",
          "cidoc:P1_is_identified_by": {
            "@type": "cidoc:E41_Appellation",
            "@value": "Giovanni Doria"
          }
        }
      ],
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "https://genoa.archive/person/luca_grimaldi",
          "@type": "cidoc:E21_Person",
          "cidoc:P1_is_identified_by": {
            "@type": "cidoc:E41_Appellation",
            "@value": "Luca Grimaldi"
          }
        }
      ],
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "https://genoa.archive/building/house_vico_dritto_71",
          "@type": "gmn:E22_1_Building",
          "rdfs:label": "House on Vico Dritto di Ponticello"
        }
      ]
    }
  ]
}
```

**Key Observation:** All three P70.x properties add their information to the same E8_Acquisition node, creating a complete representation of the transaction.

### Example 4: URI String Reference (Minimal)

**GMN Simplified Input:**
```json
{
  "@id": "https://genoa.archive/contract/simple_sale",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_3_documents_transfer_of": [
    "https://genoa.archive/building/unknown_building_42"
  ]
}
```

**CIDOC-CRM Full Output:**
```json
{
  "@id": "https://genoa.archive/contract/simple_sale",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "https://genoa.archive/contract/simple_sale/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P24_transferred_title_of": [
        {
          "@id": "https://genoa.archive/building/unknown_building_42",
          "@type": "cidoc:E18_Physical_Thing"
        }
      ]
    }
  ]
}
```

**Note:** When only a URI string is provided without additional properties, the transformation creates a minimal object with default type.

---

## Integration with Related Properties

The P70.3 property is designed to work seamlessly with other sales contract properties:

### Related Property Overview

| Property | Label | CIDOC-CRM Target | Description |
|----------|-------|------------------|-------------|
| gmn:P70_1 | documents seller | P23_transferred_title_from | Person selling the property |
| gmn:P70_2 | documents buyer | P22_transferred_title_to | Person buying the property |
| **gmn:P70_3** | **documents transfer of** | **P24_transferred_title_of** | **Thing being transferred** |
| gmn:P70_4 | documents seller's procurator | P14_carried_out_by (seller's agent) | Seller's representative |
| gmn:P70_5 | documents buyer's procurator | P14_carried_out_by (buyer's agent) | Buyer's representative |

### Shared E8_Acquisition Node

All these properties contribute to the same E8_Acquisition event:

```
E8_Acquisition
├─ P23_transferred_title_from (from P70.1)
├─ P22_transferred_title_to (from P70.2)
├─ P24_transferred_title_of (from P70.3) ← This property
├─ P9_consists_of
│   ├─ E7_Activity (seller's representation)
│   │   └─ P14_carried_out_by (from P70.4)
│   └─ E7_Activity (buyer's representation)
│       └─ P14_carried_out_by (from P70.5)
└─ (other properties...)
```

### Transformation Order

For correct integration, transformations should be applied in this order:
1. P70.1 (seller) - Creates acquisition node
2. P70.2 (buyer) - Adds to existing acquisition node
3. **P70.3 (transfer of)** - Adds to existing acquisition node
4. P70.4 (seller's procurator) - Adds activities to acquisition
5. P70.5 (buyer's procurator) - Adds activities to acquisition

---

## Historical Context

### Medieval Genoese Practice

In medieval Genoa (particularly 1154-1164, the period of the Genoese Merchant Networks project), property transfers were meticulously documented by notaries.

**Typical Contract Components:**
1. **Parties:** Seller (venditor) and buyer (emptor)
2. **Object:** Property being sold (res vendita)
3. **Price:** Amount paid (pretium)
4. **Location:** Where property is situated
5. **Boundaries:** Adjacent properties (confines)
6. **Date and place** of contract execution
7. **Witnesses** to the transaction

**Property Types Commonly Transferred:**
- **Domus:** Houses, residences
- **Apotecha:** Shops, commercial spaces
- **Terra:** Land parcels
- **Magazenum:** Warehouses
- **Casale:** Rural properties
- Various moveable goods and merchandise

### Legal Significance

The notarial document served multiple functions:
1. **Legal Proof:** Evidence of ownership transfer
2. **Title Chain:** Part of property's ownership history
3. **Tax Record:** Basis for property taxation
4. **Dispute Resolution:** Reference in legal conflicts

---

## CIDOC-CRM Alignment

### E8 Acquisition Definition

From CIDOC-CRM specification:

> "This class comprises transfers of legal ownership from one or more instances of E39 Actor to one or more other instances of E39 Actor. The class also applies to the establishment or loss of ownership of instances of E18 Physical Thing."

### P24 transferred_title_of Definition

From CIDOC-CRM specification:

> "This property identifies the instance(s) of E18 Physical Thing involved in an instance of E8 Acquisition. In reality, an acquisition must refer to at least one transferred item."

### Semantic Equivalence

```
gmn:P70_3_documents_transfer_of → EQUIVALENT TO → 
    cidoc:P70_documents / cidoc:P24_transferred_title_of
```

This property chain means:
- "The contract documents a transfer of X"
- Is semantically equivalent to:
- "The contract documents an acquisition that transferred title of X"

---

## Data Quality Considerations

### Required Information

**Minimum Required:**
- Contract URI (@id)
- Contract type (gmn:E31_2_Sales_Contract)
- At least one thing being transferred

**Recommended Additional:**
- Thing type (Building vs Moveable Property)
- Thing identifier (name, description)
- Thing location (for buildings)

### Validation Rules

1. **Domain Validation:**
   - Subject must be gmn:E31_2_Sales_Contract
   - Warn if applied to other document types

2. **Range Validation:**
   - Objects should be E18_Physical_Thing or subtypes
   - Warn if unrecognized types are used

3. **Completeness Validation:**
   - Check if both P70.1 (seller) and P70.2 (buyer) are present
   - Contract without parties is incomplete

4. **Cardinality Validation:**
   - At least one thing should be specified
   - Multiple things are valid

### Common Data Issues

**Issue 1: Missing Type Information**
```json
// Problematic
{"@id": "thing_uri"}

// Better
{"@id": "thing_uri", "@type": "gmn:E22_1_Building"}
```

**Issue 2: Incomplete Thing Description**
```json
// Minimal (valid but limited)
{"@id": "building_42", "@type": "gmn:E22_1_Building"}

// Rich (preferred)
{
  "@id": "building_42",
  "@type": "gmn:E22_1_Building",
  "cidoc:P1_is_identified_by": {"@value": "Shop on Main Street"},
  "cidoc:P53_has_former_or_current_location": {"@id": "main_street"}
}
```

---

## Query Examples

### SPARQL Query 1: Find All Things Transferred in Sales Contracts

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?thing ?thingType
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition .
  ?acquisition a cidoc:E8_Acquisition ;
               cidoc:P24_transferred_title_of ?thing .
  ?thing a ?thingType .
}
```

### SPARQL Query 2: Find Buildings Sold in Specific Period

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?building ?date
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition ;
            cidoc:P94i_was_created_by ?creation .
  
  ?acquisition cidoc:P24_transferred_title_of ?building .
  ?building a gmn:E22_1_Building .
  
  ?creation cidoc:P4_has_time-span ?timespan .
  ?timespan cidoc:P82_at_some_time_within ?date .
  
  FILTER(?date >= "1154-01-01" && ?date <= "1164-12-31")
}
ORDER BY ?date
```

### SPARQL Query 3: Find Complete Transactions (Seller, Buyer, Thing)

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?seller ?buyer ?thing
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            cidoc:P70_documents ?acquisition .
  
  ?acquisition cidoc:P23_transferred_title_from ?seller ;
               cidoc:P22_transferred_title_to ?buyer ;
               cidoc:P24_transferred_title_of ?thing .
}
```

---

## Summary

The `gmn:P70_3_documents_transfer_of` property:

1. ✅ **Simplifies** data entry for sales contracts
2. ✅ **Transforms** to full CIDOC-CRM structure automatically
3. ✅ **Integrates** with related P70.x properties
4. ✅ **Preserves** type information for transferred things
5. ✅ **Supports** multiple items in single contract
6. ✅ **Aligns** with CIDOC-CRM E8 Acquisition semantics
7. ✅ **Reflects** medieval Genoese notarial practice

---

**Documentation Version:** 1.0  
**Property Version:** As of ontology creation date 2025-10-17  
**Last Updated:** 2025-10-27  
**CIDOC-CRM Version:** 7.x compatibility
