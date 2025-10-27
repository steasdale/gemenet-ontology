# GMN P70.2 Documents Buyer: Ontology Documentation

## Semantic Overview

### Property Identity

**URI:** `http://example.org/gmn/P70_2_documents_buyer`  
**Prefix Form:** `gmn:P70_2_documents_buyer`  
**Label:** "P70.2 documents buyer"@en  
**Created:** 2025-10-17  
**Version:** 1.0

### Property Classification

```turtle
gmn:P70_2_documents_buyer
    a owl:ObjectProperty ;
    a rdf:Property .
```

This property is defined as both an OWL Object Property (for reasoning) and an RDF Property (for compatibility).

---

## Property Specification

### Domain and Range

**Domain:** `gmn:E31_2_Sales_Contract`  
The property applies to sales contract documents specifically, not to arbitrary documents.

**Range:** `cidoc:E21_Person`  
The property points to persons, representing the individual(s) acquiring ownership through the transaction.

**Cardinality:** Multiple (0..n)  
A sales contract may document:
- Zero buyers (incomplete data)
- One buyer (typical case)
- Multiple buyers (joint purchases)

### Property Hierarchy

```turtle
gmn:P70_2_documents_buyer rdfs:subPropertyOf cidoc:P70_documents .
```

**Parent Property:** `cidoc:P70_documents`  
This relationship indicates that documenting a buyer is a specific way that a document relates to entities in the documented event.

**Semantic Implications:**
- Inherits the meaning that the document provides evidence about the buyer's participation
- Specializes the general documentation relationship to specifically identify the acquiring party
- Maintains CIDOC-CRM compliance through subproperty chain

---

## Formal Definition

### RDF/OWL Declaration

```turtle
# Property: P70.2 documents buyer
gmn:P70_2_documents_buyer
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.2 documents buyer"@en ;
    rdfs:comment "Simplified property for associating a sales contract with the person named as the buyer. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P22_transferred_title_to > E21_Person. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The buyer is the party receiving ownership of the property being sold."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E21_Person ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P22_transferred_title_to .
```

### Property Definition

**Textual Definition:**  
A simplified property for associating a sales contract document with the person or persons named as buyer(s). The buyer is the party receiving ownership rights of the property, object, or (in historical contexts) person being transferred through the documented acquisition event.

**Scope Note:**  
This property provides a convenient shorthand for data entry, abstracting the complex CIDOC-CRM structure of document-event-participation relationships. It should be transformed into the full CIDOC-CRM representation for formal compliance and semantic reasoning.

---

## CIDOC-CRM Mapping

### Transformation Path

The simplified GMN property transforms to the following CIDOC-CRM structure:

```
E31_Document (Sales Contract)
  │
  └─── cidoc:P70_documents
        │
        └─── E8_Acquisition
              │
              └─── cidoc:P22_transferred_title_to
                    │
                    └─── E21_Person (Buyer)
```

### Path Explanation

1. **E31_Document** - The sales contract document
2. **P70_documents** - The document provides evidence about...
3. **E8_Acquisition** - ...an acquisition event (transfer of ownership)
4. **P22_transferred_title_to** - The acquisition transferred title to...
5. **E21_Person** - ...the buyer person(s)

### CIDOC-CRM Properties Used

#### P70 documents (E31 → E8)

**Definition:** This property describes the CRM Entities documented as instances of E31 Document.  
**Domain:** E31_Document  
**Range:** E1_CRM_Entity  
**Inverse:** P70i is documented in

**Application:** Links the sales contract to the acquisition event it evidences.

#### P22 transferred title to (E8 → E21)

**Definition:** This property identifies the E39 Actor or Actors who receive legal ownership through an E8 Acquisition event.  
**Domain:** E8_Acquisition  
**Range:** E39_Actor (specialized to E21_Person in GMN)  
**Inverse:** P22i acquired title through

**Application:** Identifies the person(s) receiving ownership in the transaction.

---

## Semantic Relationships

### Related GMN Properties

#### Complementary Properties (Same Acquisition)

These properties work together to document different aspects of the same transaction:

**gmn:P70_1_documents_seller**  
- Opposite role: transferring party
- CIDOC path: P70 → E8 → P23_transferred_title_from → E21
- Together with P70_2, documents the two principal parties

**gmn:P70_3_documents_transfer_of**  
- Related aspect: object of transaction
- CIDOC path: P70 → E8 → P24_transferred_title_of → E18
- Documents what the buyer acquires

**gmn:P70_16_documents_sale_price_amount**  
- Related aspect: monetary value
- CIDOC path: P70 → E8 → P179_had_sales_price → E97 → P181_has_amount
- Documents what the buyer pays

**gmn:P70_17_documents_sale_price_currency**  
- Related aspect: monetary denomination
- CIDOC path: P70 → E8 → P179_had_sales_price → E97 → P180_has_currency
- Specifies the currency of payment

#### Supporting Role Properties

These properties document individuals who facilitate or support the buyer's role:

**gmn:P70_5_documents_buyers_procurator**  
- Relationship: legal representative
- CIDOC path: P70 → E8 → P9 → E7 → P14 → E21 (with P17 → buyer)
- Person acting with legal authority for the buyer

**gmn:P70_7_documents_buyers_guarantor**  
- Relationship: security provider
- CIDOC path: P70 → E8 → P9 → E7 → P14 → E21 (with P17 → buyer)
- Person guaranteeing buyer's obligations

**gmn:P70_9_documents_payment_provider_for_buyer**  
- Relationship: financial support
- CIDOC path: P70 → E8 → P9 → E7 → P14 → E21 (with P17 → buyer)
- Third party supplying funds on buyer's behalf

### Inverse Relationships

While GMN does not explicitly define inverse properties, the CIDOC-CRM structure implies:

**Buyer's Perspective:**
- `E21_Person` (buyer) `P22i_acquired_title_through` `E8_Acquisition`
- "The buyer acquired title through the documented acquisition"

**Document's Perspective:**
- `E8_Acquisition` `P70i_is_documented_in` `E31_Document`
- "The acquisition is documented in the sales contract"

---

## Usage Patterns

### Pattern 1: Simple Sale

**Scenario:** Single buyer purchasing from single seller

```turtle
:contract_001 a gmn:E31_2_Sales_Contract ;
    gmn:P70_1_documents_seller :seller_giovanni ;
    gmn:P70_2_documents_buyer :buyer_pietro ;
    gmn:P70_3_documents_transfer_of :house_san_marco .
```

**Transforms to:**

```turtle
:contract_001 a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents [
        a cidoc:E8_Acquisition ;
        cidoc:P23_transferred_title_from [
            a cidoc:E21_Person ;
            owl:sameAs :seller_giovanni
        ] ;
        cidoc:P22_transferred_title_to [
            a cidoc:E21_Person ;
            owl:sameAs :buyer_pietro
        ] ;
        cidoc:P24_transferred_title_of [
            a gmn:E22_1_Building ;
            owl:sameAs :house_san_marco
        ]
    ] .
```

### Pattern 2: Joint Purchase

**Scenario:** Multiple buyers acquiring property together

```turtle
:contract_002 a gmn:E31_2_Sales_Contract ;
    gmn:P70_2_documents_buyer 
        :buyer_marco ,
        :buyer_alvise .
```

**Transforms to:**

```turtle
:contract_002 a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents [
        a cidoc:E8_Acquisition ;
        cidoc:P22_transferred_title_to 
            [
                a cidoc:E21_Person ;
                owl:sameAs :buyer_marco
            ] ,
            [
                a cidoc:E21_Person ;
                owl:sameAs :buyer_alvise
            ]
    ] .
```

### Pattern 3: Buyer with Procurator

**Scenario:** Buyer acting through legal representative

```turtle
:contract_003 a gmn:E31_2_Sales_Contract ;
    gmn:P70_2_documents_buyer :buyer_lorenzo ;
    gmn:P70_5_documents_buyers_procurator :procurator_andrea .
```

**Transforms to:**

```turtle
:contract_003 a gmn:E31_2_Sales_Contract ;
    cidoc:P70_documents [
        a cidoc:E8_Acquisition ;
        cidoc:P22_transferred_title_to [
            a cidoc:E21_Person ;
            owl:sameAs :buyer_lorenzo
        ] ;
        cidoc:P9_consists_of [
            a cidoc:E7_Activity ;
            cidoc:P14_carried_out_by [
                a cidoc:E21_Person ;
                owl:sameAs :procurator_andrea
            ] ;
            cidoc:P17_was_motivated_by [
                a cidoc:E21_Person ;
                owl:sameAs :buyer_lorenzo
            ]
        ]
    ] .
```

### Pattern 4: Complex Transaction

**Scenario:** Buyer with guarantor and payment provider

```turtle
:contract_004 a gmn:E31_2_Sales_Contract ;
    gmn:P70_2_documents_buyer :buyer_francesco ;
    gmn:P70_7_documents_buyers_guarantor :guarantor_pietro ;
    gmn:P70_9_documents_payment_provider_for_buyer :payer_giovanni .
```

**Transforms to:** Three E7_Activity nodes within E8_Acquisition, each linked to the buyer via P17_was_motivated_by.

---

## Ontological Distinctions

### Buyer vs. Seller

**gmn:P70_2_documents_buyer**
- Role: Acquiring party
- CIDOC property: P22_transferred_title_to
- Direction: Receives ownership
- Legal status: New owner after transaction

**gmn:P70_1_documents_seller**
- Role: Transferring party
- CIDOC property: P23_transferred_title_from
- Direction: Relinquishes ownership
- Legal status: Former owner after transaction

### Buyer vs. Buyer's Procurator

**gmn:P70_2_documents_buyer**
- Role: Principal party
- Legal capacity: Acts in own interest
- Ownership: Receives title directly
- CIDOC structure: Direct P22 relationship

**gmn:P70_5_documents_buyers_procurator**
- Role: Representative
- Legal capacity: Acts for another
- Ownership: Does not receive title
- CIDOC structure: E7_Activity with P17 linking to buyer

### Buyer vs. Buyer's Guarantor

**gmn:P70_2_documents_buyer**
- Financial obligation: Primary debtor
- Transaction role: Principal party
- Benefit: Receives property
- Risk: Primary responsibility for payment

**gmn:P70_7_documents_buyers_guarantor**
- Financial obligation: Secondary/contingent
- Transaction role: Security provider
- Benefit: None (unless default occurs)
- Risk: Contingent liability if buyer defaults

### Buyer vs. Payment Provider

**gmn:P70_2_documents_buyer**
- Legal role: Acquirer of property
- Financial aspect: Obligation to pay
- Property: Receives ownership
- May or may not provide funds directly

**gmn:P70_9_documents_payment_provider_for_buyer**
- Legal role: Financial supporter
- Financial aspect: Supplies funds
- Property: Does not receive ownership
- Third party providing payment on buyer's behalf

---

## Data Entry Guidelines

### Required Information

**Minimum:**
- Person identifier (URI or ID)
- Or person name (for URI generation)

**Recommended:**
- Full person object with:
  - Name (`gmn:P1_1_has_name`)
  - Patrilineal name (`gmn:P1_3_has_patrilineal_name`)
  - Any other identifying properties

### Data Quality Principles

1. **Completeness:** Document all buyers mentioned in the contract
2. **Accuracy:** Use exact names as they appear in document
3. **Consistency:** Use same person URI across multiple documents
4. **Disambiguation:** Distinguish persons with identical names
5. **Context:** Link to related roles (procurators, guarantors)

### Common Patterns in Historical Documents

**Single Buyer:**
```json
"gmn:P70_2_documents_buyer": [
  {
    "@id": "person_123",
    "gmn:P1_1_has_name": "Giovanni Marcello"
  }
]
```

**Multiple Buyers (Siblings):**
```json
"gmn:P70_2_documents_buyer": [
  {
    "@id": "person_124",
    "gmn:P1_1_has_name": "Marco Contarini",
    "gmn:P1_3_has_patrilineal_name": "Contarini"
  },
  {
    "@id": "person_125",
    "gmn:P1_1_has_name": "Alvise Contarini",
    "gmn:P1_3_has_patrilineal_name": "Contarini"
  }
]
```

**Buyer with Title:**
```json
"gmn:P70_2_documents_buyer": [
  {
    "@id": "person_126",
    "gmn:P1_1_has_name": "Pietro Grimani",
    "gmn:P102_1_has_title": "Procurator of San Marco"
  }
]
```

---

## Validation Rules

### Structural Validation

1. **Property must be array:** Even single buyers should be in array
2. **Array elements must be objects or strings:** No other data types
3. **Objects must have @id:** Either explicit or generatable
4. **Domain constraint:** Only on E31_2_Sales_Contract instances

### Semantic Validation

1. **Buyer should be person:** Range should be E21_Person
2. **No empty values:** Array should not contain null/undefined
3. **Unique buyers:** Same person should not appear multiple times
4. **Consistency check:** Buyer should not also be seller (in most cases)

### SPARQL Validation Queries

**Check for empty buyer arrays:**
```sparql
SELECT ?contract
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            gmn:P70_2_documents_buyer ?buyers .
  FILTER(NOT EXISTS {
    ?contract gmn:P70_2_documents_buyer ?buyer .
    FILTER(isIRI(?buyer) || isBlank(?buyer))
  })
}
```

**Check for buyer-seller overlap:**
```sparql
SELECT ?contract ?person
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            gmn:P70_1_documents_seller ?person ;
            gmn:P70_2_documents_buyer ?person .
}
```

---

## Transformation Specification

### Input Format (GMN)

```json
{
  "@id": "contract_uri",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P70_2_documents_buyer": [
    {
      "@id": "buyer_uri",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": "Buyer Name",
      "...": "other properties"
    }
  ]
}
```

### Output Format (CIDOC-CRM)

```json
{
  "@id": "contract_uri",
  "@type": "gmn:E31_2_Sales_Contract",
  "cidoc:P70_documents": [
    {
      "@id": "contract_uri/acquisition",
      "@type": "cidoc:E8_Acquisition",
      "cidoc:P22_transferred_title_to": [
        {
          "@id": "buyer_uri",
          "@type": "cidoc:E21_Person",
          "gmn:P1_1_has_name": "Buyer Name",
          "...": "other properties"
        }
      ]
    }
  ]
}
```

### Transformation Rules

1. **Check for property:** If `gmn:P70_2_documents_buyer` not present, skip
2. **Check for acquisition:** If `cidoc:P70_documents` exists, use it; otherwise create
3. **Create P22 array:** Initialize if not present
4. **Process each buyer:**
   - If object: copy all properties
   - If string: create minimal object with @id and @type
   - Add @type if missing
5. **Remove GMN property:** Delete `gmn:P70_2_documents_buyer`

### Transformation Algorithm (Pseudocode)

```
function transform_p70_2_documents_buyer(data):
    if 'gmn:P70_2_documents_buyer' not in data:
        return data
    
    buyers = data['gmn:P70_2_documents_buyer']
    subject_uri = data.get('@id', generate_uuid())
    
    # Get or create E8_Acquisition
    if 'cidoc:P70_documents' not in data or empty:
        acquisition_uri = subject_uri + '/acquisition'
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P22 array
    if 'cidoc:P22_transferred_title_to' not in acquisition:
        acquisition['cidoc:P22_transferred_title_to'] = []
    
    # Process each buyer
    for buyer in buyers:
        if is_object(buyer):
            buyer_data = copy(buyer)
            if '@type' not in buyer_data:
                buyer_data['@type'] = 'cidoc:E21_Person'
        else:  # is string URI
            buyer_data = {
                '@id': buyer,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P22_transferred_title_to'].append(buyer_data)
    
    # Remove GMN property
    delete data['gmn:P70_2_documents_buyer']
    
    return data
```

---

## Query Examples

### SPARQL Queries

**Find all buyers in sales contracts:**
```sparql
PREFIX gmn: <http://example.org/gmn/>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?contract ?buyer ?name
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            gmn:P70_2_documents_buyer ?buyer .
  OPTIONAL { ?buyer gmn:P1_1_has_name ?name }
}
```

**Find joint purchases (multiple buyers):**
```sparql
PREFIX gmn: <http://example.org/gmn/>

SELECT ?contract (COUNT(?buyer) as ?num_buyers)
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            gmn:P70_2_documents_buyer ?buyer .
}
GROUP BY ?contract
HAVING (COUNT(?buyer) > 1)
```

**Find contracts where person is buyer:**
```sparql
PREFIX gmn: <http://example.org/gmn/>

SELECT ?contract ?date
WHERE {
  ?contract a gmn:E31_2_Sales_Contract ;
            gmn:P70_2_documents_buyer <person_uri> ;
            gmn:P94i_2_has_enactment_date ?date .
}
ORDER BY ?date
```

**Find buyers with same patrilineal name (families):**
```sparql
PREFIX gmn: <http://example.org/gmn/>

SELECT ?patrilineal_name (COUNT(DISTINCT ?buyer) as ?count)
WHERE {
  ?contract gmn:P70_2_documents_buyer ?buyer .
  ?buyer gmn:P1_3_has_patrilineal_name ?patrilineal_name .
}
GROUP BY ?patrilineal_name
HAVING (COUNT(DISTINCT ?buyer) > 1)
ORDER BY DESC(?count)
```

---

## Implementation Notes

### Performance Considerations

- **Indexing:** Index on buyer URIs for fast lookup
- **Caching:** Cache acquisition node lookups
- **Batch Processing:** Process multiple contracts in single transaction
- **Memory:** Buyer objects can be large with full person data

### Edge Cases

1. **No buyers documented:** Valid for incomplete records
2. **Same person multiple times:** Possible data error, should validate
3. **Anonymous buyers:** Use blank nodes with descriptive properties
4. **Buyer is also seller:** Rare but possible in complex transactions

### Best Practices

1. **Validate before transformation:** Check data quality first
2. **Log transformations:** Record what changed
3. **Preserve original:** Keep GMN version in separate graph if needed
4. **Test thoroughly:** Use diverse historical examples
5. **Document assumptions:** Note any interpretations made

---

## External References

### CIDOC-CRM Resources

- **P22 Documentation:** http://www.cidoc-crm.org/Property/P22-transferred-title-to/version-7.1.3
- **E8 Documentation:** http://www.cidoc-crm.org/Entity/E8-Acquisition/version-7.1.3
- **E21 Documentation:** http://www.cidoc-crm.org/Entity/E21-Person/version-7.1.3
- **P70 Documentation:** http://www.cidoc-crm.org/Property/P70-documents/version-7.1.3

### Related Standards

- **FOAF Person:** http://xmlns.com/foaf/spec/#term_Person
- **Schema.org Person:** https://schema.org/Person
- **RDF/OWL Specifications:** https://www.w3.org/TR/owl2-overview/

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-27  
**Maintainer:** GMN Project Team  
**Status:** Active
