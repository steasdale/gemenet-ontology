# E31.7 Donation Contract - Ontology Documentation

## Class Definition

```turtle
# Class: E31.7 Donation Contract
gmn:E31_7_Donation_Contract
    a owl:Class ;
    rdfs:subClassOf gmn:E31_1_Contract ;
    rdfs:label "E31.7 Donation Contract"@en ;
    rdfs:comment "Specialized class that describes donation contract documents. This is a specialized type of gmn:E31_1_Contract used to represent legal documents that record the gratuitous transfer of property (both real estate and moveable property) from a donor to a donee (recipient). Unlike sales contracts where transfer occurs in exchange for payment, donation contracts document voluntary transfers without expectation of compensation, though they may include conditions or stipulations. Like all notarial contracts in this ontology, donation contracts model the transfer of rights: the donor agrees or obliges themselves to transfer an object of donation to the person receiving the donation. Donation contracts typically include information about the donor, donee, property being donated, any conditions attached to the donation, date of transaction, and witnessing notaries. Instances of this class represent the physical or conceptual document itself, while the actual transfer of ownership is modeled through E8_Acquisition events that the document documents (via P70_documents)."@en ;
    dcterms:created "2025-10-19"^^xsd:date ;
    rdfs:seeAlso gmn:E31_1_Contract, cidoc:E8_Acquisition, cidoc:P70_documents .
```

## Semantic Structure

```
E31_7_Donation_Contract (the document)
  └─ P70_documents
      └─ E8_Acquisition (the donation transfer)
          ├─ P23_transferred_title_from → E39_Actor (donor)
          ├─ P22_transferred_title_to → E39_Actor (donee via P70.22)
          └─ P24_transferred_title_of → E18_Physical_Thing (donated object)
```

## Properties

### P70.32 indicates donor

```turtle
gmn:P70_32_indicates_donor
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.32 indicates donor"@en ;
    rdfs:comment "Simplified property for associating a donation contract with the person or entity named as the donor. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P23_transferred_title_from > E39_Actor. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The donor is the party voluntarily transferring ownership of the property being donated without expectation of payment."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_7_Donation_Contract ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-19"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P23_transferred_title_from .
```

### P70.22 indicates receiving party (updated)

```turtle
gmn:P70_22_indicates_receiving_party
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.22 indicates receiving party"@en ;
    rdfs:comment "Simplified property for associating a document with the person or entity receiving something in the documented activity. In cession of rights contracts, this is the party receiving the ceded rights. In declarations, this is the party to whom the declaration is addressed or directed. In donation contracts, this is the donee receiving the donated property. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P01_has_domain > E39_Actor (using the inverse P01i_is_domain_of for declarations) OR E31_Document > P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor (for cessions and donations, where the receiving party acquires ownership or rights). The E7_Activity or E8_Acquisition should be typed appropriately (AAT 300417639 for cessions, AAT 300027623 for declarations, or appropriate type for donations). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf (
            gmn:E31_4_Cession_of_Rights_Contract
            gmn:E31_5_Declaration
            gmn:E31_7_Donation_Contract
        )
    ] ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-18"^^xsd:date ;
    dcterms:modified "2025-10-19"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P22_transferred_title_to, cidoc:P01_has_domain .
```

### P70.33 indicates object of donation

```turtle
gmn:P70_33_indicates_object_of_donation
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.33 indicates object of donation"@en ;
    rdfs:comment "Simplified property for associating a donation contract with the physical thing (property or object) being donated. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The range includes buildings (gmn:E22_1_Building) and moveable property (gmn:E22_2_Moveable_Property) that are being transferred as gifts."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_7_Donation_Contract ;
    rdfs:range cidoc:E18_Physical_Thing ;
    dcterms:created "2025-10-19"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P24_transferred_title_of .
```

## Transformation Examples

### Example 1: Simple Donation

**Input (shortcut):**
```turtle
<donation001> a gmn:E31_7_Donation_Contract ;
    gmn:P70_32_indicates_donor <merchant_giovanni> ;
    gmn:P70_22_indicates_receiving_party <monastery_san_lorenzo> ;
    gmn:P70_33_indicates_object_of_donation <palazzo_via_garibaldi> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<donation001> a gmn:E31_7_Donation_Contract ;
    cidoc:P70_documents <donation001/acquisition> .

<donation001/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <merchant_giovanni> ;
    cidoc:P22_transferred_title_to <monastery_san_lorenzo> ;
    cidoc:P24_transferred_title_of <palazzo_via_garibaldi> .
```

### Example 2: Complex Donation with Notary and Date

**Input (shortcut):**
```turtle
<donation002> a gmn:E31_7_Donation_Contract ;
    gmn:P1_1_has_name "Donation of warehouse to hospital" ;
    gmn:P70_32_indicates_donor <widow_maria> ;
    gmn:P70_22_indicates_receiving_party <hospital_pammatone> ;
    gmn:P70_33_indicates_object_of_donation <warehouse_porto> ;
    gmn:P94i_1_was_created_by <notary_antonio> ;
    gmn:P94i_2_has_enactment_date "1445-03-15"^^xsd:date ;
    gmn:P94i_3_has_place_of_enactment <genoa_city> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<donation002> a gmn:E31_7_Donation_Contract ;
    cidoc:P1_is_identified_by <donation002/appellation> ;
    cidoc:P70_documents <donation002/acquisition> ;
    cidoc:P94i_was_created_by <donation002/creation> .

<donation002/appellation> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Donation of warehouse to hospital" .

<donation002/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <widow_maria> ;
    cidoc:P22_transferred_title_to <hospital_pammatone> ;
    cidoc:P24_transferred_title_of <warehouse_porto> .

<donation002/creation> a cidoc:E65_Creation ;
    cidoc:P14_carried_out_by <notary_antonio> ;
    cidoc:P4_has_time-span <donation002/creation/timespan> ;
    cidoc:P7_took_place_at <genoa_city> .

<donation002/creation/timespan> a cidoc:E52_Time-Span ;
    cidoc:P82_at_some_time_within "1445-03-15"^^xsd:date .
```

### Example 3: Donation with Multiple Objects

**Input (shortcut):**
```turtle
<donation003> a gmn:E31_7_Donation_Contract ;
    gmn:P70_32_indicates_donor <nobleman_filippo> ;
    gmn:P70_22_indicates_receiving_party <church_santo_stefano> ;
    gmn:P70_33_indicates_object_of_donation <building_chapel> , <land_parcel_12> .
```

**Output (CIDOC-CRM compliant):**
```turtle
<donation003> a gmn:E31_7_Donation_Contract ;
    cidoc:P70_documents <donation003/acquisition> .

<donation003/acquisition> a cidoc:E8_Acquisition ;
    cidoc:P23_transferred_title_from <nobleman_filippo> ;
    cidoc:P22_transferred_title_to <church_santo_stefano> ;
    cidoc:P24_transferred_title_of <building_chapel> , <land_parcel_12> .
```

## Comparison with Other Contract Types

| Aspect | Sales Contract | Donation Contract | Cession | Declaration |
|--------|---------------|-------------------|---------|-------------|
| Central Event | E8_Acquisition | E8_Acquisition | E7_Activity (cession) | E7_Activity (declaration) |
| Transferring Party | P23 (seller) | P23 (donor) | P14 (conceding party) | P14 (declarant) |
| Receiving Party | P22 (buyer) | P22 (donee) | P14 (receiving party) | P01 (recipient) |
| Object | P24 (property) | P24 (donated property) | P16 (rights/legal object) | P16 (declaration subject) |
| Payment | Required | Not expected | Variable | N/A |
| Nature | Commercial transfer | Gratuitous transfer | Rights transfer | Unilateral statement |

## Implementation Notes

1. **Shared Acquisition**: All three properties (P70.32, P70.22, P70.33) share the same E8_Acquisition node. The transformation functions check if an acquisition already exists before creating a new one.

2. **E8_Acquisition Type**: Unlike sales contracts which may have explicit typing, donation acquisitions use the default E8_Acquisition without additional type specification. The donation nature is implicit in the contract type.

3. **Order Independence**: The properties can be processed in any order - the transformation will always reference or create the same shared acquisition.

4. **URI Generation**: The acquisition URI is generated as `{contract_uri}/acquisition` for consistency.

5. **Multiple Objects**: Multiple objects can be donated in a single contract by using P70.33 multiple times. Each object is added to the acquisition's P24_transferred_title_of property.

6. **Donor Types**: The donor (P70.32) can be any E39_Actor - either a person (E21_Person) or a group (E74_Group), allowing for donations from families, guilds, or other organizations.

7. **Receiving Party Types**: Similarly, the receiving party (P70.22) can be any E39_Actor, commonly religious institutions, hospitals, or individuals.

## Additional Notes

- All donation contracts should be classified as both `cidoc:E31_Document` and `gmn:E31_7_Donation_Contract`
- The transformation automatically creates URIs for intermediate entities (acquisitions, appellations, etc.)
- Price properties (P70.16-17) are typically not used for donations, as they are gratuitous transfers
- Conditions attached to donations should be documented using appropriate properties or notes
- Multiple objects can be associated with a single donation using P70.33 multiple times
- The donor in P70.32 can be any E39_Actor (person or group)

## Related Contract Types

Donation contracts share semantic patterns with:
- **Sales Contracts (E31_2)**: Both use E8_Acquisition for property transfer
- **Cession Contracts (E31_4)**: Both share P70.22 for receiving party
- **Dowry Contracts (E31_8)**: Similar gratuitous transfer context (if implemented)

## Use Cases

Common scenarios for donation contracts include:
- Religious donations (property to churches, monasteries)
- Charitable donations (property to hospitals, orphanages)
- Testamentary donations (bequests in wills)
- Family donations (inter vivos gifts between family members)
- Pious donations (donations for masses, prayers, charitable works)

## AAT References

Relevant Getty AAT terms that may be used with donation contracts:
- **AAT 300417639**: transfer of rights (general concept)
- **AAT 300055475**: gifts (concept of donation)
- **AAT 300404650**: names (for identifying donations)

## Best Practices

1. **Always specify the donor**: Use P70.32 to link to the donor
2. **Always specify the receiving party**: Use P70.22 to link to the donee
3. **Always specify the object**: Use P70.33 to link to donated property
4. **Document conditions**: Use editorial notes for any conditions or stipulations
5. **Record dates**: Use P94i_2 for the date of donation
6. **Identify notary**: Use P94i_1 for the notary who recorded the donation
7. **Note context**: Use descriptive names (P1_1) to clarify the donation purpose
