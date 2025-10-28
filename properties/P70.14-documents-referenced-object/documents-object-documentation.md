# Ontology Documentation: P70.14 Documents Referenced Object
## GMN Ontology Property Specification

**Property URI**: `gmn:P70_14_documents_referenced_object`  
**Version**: 1.0  
**Status**: Active  
**Date Created**: 2025-10-27

---

## Table of Contents

1. [Property Definition](#property-definition)
2. [Semantic Structure](#semantic-structure)
3. [Domain and Range](#domain-and-range)
4. [Relationship to CIDOC-CRM](#relationship-to-cidoc-crm)
5. [Usage Guidelines](#usage-guidelines)
6. [Examples](#examples)
7. [Transformation Specification](#transformation-specification)
8. [Related Properties](#related-properties)

---

## Property Definition

### Basic Information

**Property URI**: `gmn:P70_14_documents_referenced_object`

**Label**: "P70.14 documents referenced object" (English)

**Property Type**: `owl:ObjectProperty`, `rdf:Property`

**Superproperty**: `cidoc:P67_refers_to`

**Domain**: `gmn:E31_2_Sales_Contract`

**Range**: `cidoc:E1_CRM_Entity`

**Created**: 2025-10-27

**Inverse**: None (P67_refers_to has inverse P67i_is_referred_to_by)

### Definition

Simplified property for associating a sales contract with any object (legal or physical) referenced or mentioned in the document. This includes legal objects (rights, obligations, debts, claims, privileges, servitudes, easements) and physical objects mentioned in the contract.

### Scope Note

This property captures objects of various types that are mentioned within a sales contract, even if they are not the primary object of the transaction. For example, a contract selling a house might reference existing water rights attached to the property, mention outstanding debts that are being settled as part of the sale, or describe easements that affect the property.

The property acknowledges that these objects are textually present in the document, whether as context, as part of the transaction conditions, or as related obligations. The use of E1_CRM_Entity as the range provides maximum flexibility to accommodate both:
- **Legal Objects** (E72_Legal_Object): rights, obligations, privileges, debts, claims
- **Physical Things** (E18_Physical_Thing): tangible objects, structures, fixtures

This is distinct from:
- **P70.3 (documents_transfer_of)**: which represents the primary object being transferred in the sale
- **P67_refers_to (direct)**: which is the underlying CIDOC-CRM property that this simplifies

---

## Semantic Structure

### CIDOC-CRM Pattern

The property represents the direct CIDOC-CRM relationship:

```
E31_Document (Sales Contract)
  └─ P67_refers_to
      └─ E1_CRM_Entity (Referenced Object)
```

### RDF/TTL Structure

```turtle
gmn:P70_14_documents_referenced_object
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.14 documents referenced object"@en ;
    rdfs:comment "[definition text]"@en ;
    rdfs:subPropertyOf cidoc:P67_refers_to ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E1_CRM_Entity ;
    dcterms:created "2025-10-27"^^xsd:date ;
    rdfs:seeAlso cidoc:P67_refers_to .
```

### Property Chain

This property does NOT use a property chain (unlike many other P70.x properties). It is a direct reference property:

```
Subject: E31_2_Sales_Contract
Predicate: P67_refers_to
Object: E1_CRM_Entity
```

---

## Domain and Range

### Domain: gmn:E31_2_Sales_Contract

The property's domain is restricted to sales contracts because:
1. This is where object references typically appear in transactional documents
2. Sales contracts often reference ancillary objects related to the transaction
3. The property fits the P70.x naming convention for sales contract-specific properties

**Note**: While P67_refers_to has domain E31_Document (broader), this simplified property is specialized for sales contracts.

### Range: cidoc:E1_CRM_Entity

The range is the broadest possible entity type in CIDOC-CRM because:

1. **Flexibility**: Allows for any type of referenced object
2. **Legal Objects**: Accommodates E72_Legal_Object and its subclasses
3. **Physical Things**: Accommodates E18_Physical_Thing and its subclasses
4. **Other Entities**: Can handle concepts, events, or other CRM entities if needed

**Common Subtypes**:
- `cidoc:E72_Legal_Object` - Rights, obligations, debts, claims, privileges
- `cidoc:E18_Physical_Thing` - Physical objects, structures, fixtures
- `cidoc:E22_Human-Made_Object` - Specific artifacts or constructed items
- `cidoc:E73_Information_Object` - Documents or abstract information objects

---

## Relationship to CIDOC-CRM

### Base Property: P67 refers to

**CIDOC-CRM Definition**: "This property documents that a E89 Propositional Object makes a statement about an instance or instances of E1 CRM Entity."

**GMN Usage**: We use P67_refers_to to indicate that a sales contract document mentions or refers to various objects, whether in passing, as conditions, or as context for the transaction.

### Why Not P70_documents?

Unlike most P70.x properties in GMN, P70.14 does NOT use P70_documents because:

1. **Not About the Transaction Event**: Referenced objects are mentioned in the text but aren't necessarily part of the acquisition event itself
2. **Direct Reference**: The relationship is between the document and the object, not between the acquisition event and the object
3. **Semantic Clarity**: P67_refers_to more accurately captures "mentioned in the text" vs. P70_documents which means "documents an event involving"

### Comparison with P67-based Properties

GMN has several properties based on P67_refers_to:
- **P70.11** (documents_referenced_person) - Persons mentioned in text
- **P70.13** (documents_referenced_place) - Places mentioned in text
- **P70.14** (documents_referenced_object) - Objects mentioned in text

All three use P67_refers_to because they represent textual mentions rather than event participation.

---

## Usage Guidelines

### When to Use This Property

Use `P70_14_documents_referenced_object` when:

1. **Legal Objects**:
   - Water rights attached to property
   - Easements or servitudes affecting the property
   - Existing debts being settled as part of the transaction
   - Claims or privileges being transferred
   - Obligations that continue with the property
   - Rights of way or usage rights

2. **Physical Objects**:
   - Existing wells, cisterns, or water infrastructure
   - Structures mentioned but not the primary sale object
   - Fixtures or attachments referenced
   - Objects used to define boundaries (trees, stones, walls)
   - Moveable property included in transaction

3. **Contextual References**:
   - Objects mentioned for clarification
   - Items referenced in property descriptions
   - Related objects that affect the transaction

### When NOT to Use This Property

Do NOT use this property for:

1. **Primary Transaction Object**: Use P70.3 (documents_transfer_of) instead
2. **Persons**: Use P70.11 (documents_referenced_person) instead
3. **Places**: Use P70.13 (documents_referenced_place) instead
4. **Event Participants**: Use appropriate P70.1-P70.10 properties

### Multiple Objects

A single contract may reference multiple objects:

```json
{
  "@id": "contract:123",
  "gmn:P70_14_documents_referenced_object": [
    "object:water_right_1",
    "object:easement_1",
    "object:debt_to_creditor",
    "object:well_1"
  ]
}
```

### Type Specificity

When you know the specific type, include it in the object data:

```json
{
  "@id": "contract:123",
  "gmn:P70_14_documents_referenced_object": [
    {
      "@id": "object:water_right_1",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Water rights to spring on north boundary"
    }
  ]
}
```

---

## Examples

### Example 1: Water Rights Reference

**Scenario**: A house sale contract mentions water rights attached to the property.

**GMN Input**:
```json
{
  "@id": "contract:venice_1450_01_15",
  "@type": "gmn:E31_2_Sales_Contract",
  "rdfs:label": "Sale of house with water rights",
  "gmn:P70_1_documents_seller": ["person:giovanni_merchant"],
  "gmn:P70_2_documents_buyer": ["person:marco_artisan"],
  "gmn:P70_3_documents_transfer_of": ["property:house_san_marco_district"],
  "gmn:P70_14_documents_referenced_object": [
    {
      "@id": "object:water_right_spring_north",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Water rights to spring on north boundary"
    }
  ]
}
```

**CIDOC-CRM Output**:
```json
{
  "@id": "contract:venice_1450_01_15",
  "@type": "gmn:E31_2_Sales_Contract",
  "rdfs:label": "Sale of house with water rights",
  "cidoc:P70_documents": [{
    "@id": "contract:venice_1450_01_15/acquisition",
    "@type": "cidoc:E8_Acquisition",
    "cidoc:P22_transferred_title_to": ["person:marco_artisan"],
    "cidoc:P23_transferred_title_from": ["person:giovanni_merchant"],
    "cidoc:P24_transferred_title_of": ["property:house_san_marco_district"]
  }],
  "cidoc:P67_refers_to": [
    {
      "@id": "object:water_right_spring_north",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Water rights to spring on north boundary"
    }
  ]
}
```

**Explanation**: The water rights are mentioned in the contract as part of the property description, but they are not the primary object being transferred (that's the house). They are referenced using P67_refers_to.

---

### Example 2: Debt Settlement Reference

**Scenario**: A contract mentions settling an existing debt as part of the transaction.

**GMN Input**:
```json
{
  "@id": "contract:genoa_1455_03_20",
  "@type": "gmn:E31_2_Sales_Contract",
  "rdfs:label": "Land sale with debt settlement",
  "gmn:P70_1_documents_seller": ["person:antonio_landowner"],
  "gmn:P70_2_documents_buyer": ["person:francesco_merchant"],
  "gmn:P70_3_documents_transfer_of": ["property:vineyard_portofino"],
  "gmn:P70_14_documents_referenced_object": [
    {
      "@id": "object:debt_to_creditor_paolo",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Outstanding debt of 50 ducats to Paolo",
      "gmn:relates_to_person": "person:paolo_creditor"
    }
  ]
}
```

**CIDOC-CRM Output**:
```json
{
  "@id": "contract:genoa_1455_03_20",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "object:debt_to_creditor_paolo",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Outstanding debt of 50 ducats to Paolo",
      "gmn:relates_to_person": "person:paolo_creditor"
    }
  ]
}
```

---

### Example 3: Multiple Objects

**Scenario**: A complex property transaction referencing multiple objects.

**GMN Input**:
```json
{
  "@id": "contract:florence_1460_07_10",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_14_documents_referenced_object": [
    {
      "@id": "object:well_in_courtyard",
      "@type": "cidoc:E22_Human-Made_Object",
      "rdfs:label": "Stone well in central courtyard"
    },
    {
      "@id": "object:easement_neighbor_access",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Easement for neighbor access to road"
    },
    {
      "@id": "object:servitude_water_passage",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Servitude allowing water passage to adjacent property"
    }
  ]
}
```

**CIDOC-CRM Output**:
```json
{
  "@id": "contract:florence_1460_07_10",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "object:well_in_courtyard",
      "@type": "cidoc:E22_Human-Made_Object",
      "rdfs:label": "Stone well in central courtyard"
    },
    {
      "@id": "object:easement_neighbor_access",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Easement for neighbor access to road"
    },
    {
      "@id": "object:servitude_water_passage",
      "@type": "cidoc:E72_Legal_Object",
      "rdfs:label": "Servitude allowing water passage to adjacent property"
    }
  ]
}
```

---

### Example 4: Simple URI References

**Scenario**: Basic references without detailed object data.

**GMN Input**:
```json
{
  "@id": "contract:pisa_1465_11_05",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_14_documents_referenced_object": [
    "object:privilege_tax_exemption",
    "object:right_market_stall",
    "object:claim_inheritance"
  ]
}
```

**CIDOC-CRM Output**:
```json
{
  "@id": "contract:pisa_1465_11_05",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P67_refers_to": [
    {
      "@id": "object:privilege_tax_exemption",
      "@type": "cidoc:E1_CRM_Entity"
    },
    {
      "@id": "object:right_market_stall",
      "@type": "cidoc:E1_CRM_Entity"
    },
    {
      "@id": "object:claim_inheritance",
      "@type": "cidoc:E1_CRM_Entity"
    }
  ]
}
```

---

## Transformation Specification

### Transformation Function

**Function Name**: `transform_p70_14_documents_referenced_object(data)`

**Input**: Document data dictionary with GMN properties

**Output**: Document data dictionary with CIDOC-CRM properties

### Transformation Algorithm

```
1. Check if 'gmn:P70_14_documents_referenced_object' exists in data
   - If not, return data unchanged

2. Get list of referenced objects from the property

3. Initialize 'cidoc:P67_refers_to' array if it doesn't exist
   - Preserve any existing P67_refers_to data

4. For each object in the list:
   a. If object is a dictionary:
      - Copy the object data
      - Add '@type': 'cidoc:E1_CRM_Entity' if @type is missing
   b. If object is a URI string:
      - Create dictionary with '@id' and '@type': 'cidoc:E1_CRM_Entity'
   
5. Append processed object to 'cidoc:P67_refers_to' array

6. Delete 'gmn:P70_14_documents_referenced_object' property

7. Return transformed data
```

### Type Handling

The transformation preserves specific types when present:

**Input with Specific Type**:
```json
{
  "@id": "object:123",
  "@type": "cidoc:E72_Legal_Object"
}
```

**Output**: Type preserved as E72_Legal_Object

**Input without Type**:
```json
"object:123"
```

**Output**: Default type E1_CRM_Entity added

### Array Handling

The function handles both single objects and arrays:

**Single Object**:
```json
"gmn:P70_14_documents_referenced_object": ["object:123"]
```

**Multiple Objects**:
```json
"gmn:P70_14_documents_referenced_object": [
  "object:123",
  "object:456",
  "object:789"
]
```

### Existing P67_refers_to

If `cidoc:P67_refers_to` already exists (e.g., from P70.11 or P70.13), the function appends to it rather than overwriting:

**Before**:
```json
{
  "cidoc:P67_refers_to": [
    {"@id": "person:123", "@type": "cidoc:E21_Person"}
  ],
  "gmn:P70_14_documents_referenced_object": ["object:456"]
}
```

**After**:
```json
{
  "cidoc:P67_refers_to": [
    {"@id": "person:123", "@type": "cidoc:E21_Person"},
    {"@id": "object:456", "@type": "cidoc:E1_CRM_Entity"}
  ]
}
```

---

## Related Properties

### Within GMN Ontology

**P70.3 - documents_transfer_of**
- Purpose: Primary object being transferred in the sale
- Difference: P70.3 is for the main transaction object, P70.14 is for additional referenced objects
- Relationship: Complementary - a contract may have both

**P70.11 - documents_referenced_person**
- Purpose: Persons mentioned in the contract text
- Similarity: Both use P67_refers_to for textual mentions
- Difference: P70.11 is for persons, P70.14 is for objects

**P70.13 - documents_referenced_place**
- Purpose: Places mentioned in the contract text
- Similarity: Both use P67_refers_to for textual mentions
- Difference: P70.13 is for places, P70.14 is for objects

### In CIDOC-CRM

**P67_refers_to**
- The base property that P70.14 simplifies
- Domain: E89_Propositional_Object (broader than E31_Document)
- Range: E1_CRM_Entity
- Usage: Direct reference from document to entity

**P70_documents**
- Not used by P70.14 (unlike most P70.x properties)
- Represents: Document → Event relationship
- Difference: P70.14 represents Document → Entity, not Document → Event

**P16_used_specific_object**
- Alternative: Could be used if objects are involved in events
- P70.14 Choice: Uses P67_refers_to for simpler "mentioned in text" semantics

---

## Ontological Considerations

### Entity Types

The broad E1_CRM_Entity range accommodates various entity types:

**Legal Objects (E72)**:
- Rights: Water rights, mineral rights, usage rights
- Obligations: Service obligations, maintenance duties
- Privileges: Tax exemptions, market privileges
- Debts: Outstanding debts, credits
- Claims: Inheritance claims, ownership claims
- Easements: Right of way, access rights
- Servitudes: Burdens or restrictions on property

**Physical Things (E18)**:
- Structures: Wells, cisterns, walls, buildings
- Features: Trees, boundary markers, fountains
- Infrastructure: Irrigation systems, drainage
- Moveable Objects: Tools, furniture, equipment

**Other Entities**:
- Information Objects (E73): Referenced documents, deeds
- Conceptual Objects (E28): Abstract rights or concepts
- Events (E5): Historical events referenced in context

### Semantic Precision

Using P67_refers_to instead of P70_documents provides semantic clarity:

**P67_refers_to semantics**: "The document mentions or refers to this entity"
- Lighter commitment - just textual presence
- Appropriate for contextual mentions
- No implication of event participation

**P70_documents semantics**: "The document records an event involving this entity"
- Stronger commitment - event participation
- Appropriate for transaction participants
- Implies role in documented event

---

## Version History

**Version 1.0** (2025-10-27)
- Initial property definition
- Added to GMN ontology
- Transformation function implemented
- Documentation completed

---

## References

- CIDOC-CRM Version 7.1.3: http://www.cidoc-crm.org/
- P67 refers to: http://www.cidoc-crm.org/Property/P67-refers-to/version-7.1.3
- E1 CRM Entity: http://www.cidoc-crm.org/Entity/E1-CRM-Entity/version-7.1.3
- E72 Legal Object: http://www.cidoc-crm.org/Entity/E72-Legal-Object/version-7.1.3
- E18 Physical Thing: http://www.cidoc-crm.org/Entity/E18-Physical-Thing/version-7.1.3

---

**Document Status**: Complete  
**Last Updated**: 2025-10-27  
**Maintained By**: GMN Ontology Team
