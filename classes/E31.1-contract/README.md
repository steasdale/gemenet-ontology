# General Contract (E31.1) - Ontology Documentation Package

## Overview

This package contains complete documentation and implementation resources for the **gmn:E31_1_Contract** class in the Genoese Merchant Networks ontology. The general contract class serves as the parent class for all specialized contract types and represents notarial contract documents that formalize agreements, transactions, and legal acts between parties.

**Class URI:** `gmn:E31_1_Contract`  
**Parent Class:** `cidoc:E31_Document`  
**Ontology Version:** 1.5  
**Last Updated:** 2025-10-26

## Key Characteristics

- **Purpose**: Parent class for all notarial contract types (sales, donations, dowries, cessions, arbitrations)
- **Scope**: Documents legal agreements and transactions recorded by notaries
- **Semantic Structure**: Represents the document itself; actual transactions are modeled through P70_documents
- **Inheritance**: Specialized contract types inherit from this class and add specific properties

## Quick Start Checklist

### For Understanding the Ontology
- [ ] Read `contract-documentation.md` for complete semantic documentation
- [ ] Review the class hierarchy and inheritance structure
- [ ] Understand the relationship between documents and documented events
- [ ] Examine the transformation examples to see how shortcuts expand to CIDOC-CRM

### For Implementation
- [ ] Read `contract-implementation-guide.md` for step-by-step instructions
- [ ] Review existing ontology structure (already implemented in gmn_ontology.ttl)
- [ ] Understand that E31_1_Contract is already defined as the parent class
- [ ] Note that specialized contract types are subclasses of E31_1_Contract
- [ ] No new TTL additions needed (class already exists)
- [ ] No new Python transformations needed (uses standard document properties)

### For Documentation
- [ ] Review `contract-doc-note.txt` for content to add to project documentation
- [ ] Add examples of general contract usage
- [ ] Document the inheritance hierarchy for all contract types

## Package Contents

### 1. README.md (this file)
Complete overview, quick-start checklist, and package summary.

### 2. contract-implementation-guide.md
Step-by-step implementation guide explaining:
- The role of E31_1_Contract in the ontology
- Inheritance structure and specialized contract types
- How to use general contracts vs. specialized types
- Testing and validation procedures

### 3. contract-documentation.md
Complete semantic documentation including:
- Class definition and purpose
- Inheritance hierarchy
- Applicable properties from cidoc:E31_Document
- Relationship to specialized contract types
- Usage examples and patterns

### 4. contract-ontology.ttl
Ready-to-reference TTL definition showing:
- The existing E31_1_Contract class definition
- Documentation of the class hierarchy
- Reference to all specialized contract subclasses

### 5. contract-transform.py
Python reference documentation showing:
- That E31_1_Contract uses standard document properties
- No specialized transformation functions needed
- How specialized contract types extend the base class

### 6. contract-doc-note.txt
Documentation additions for the main project documentation including:
- Overview of the contract class hierarchy
- Examples of when to use general vs. specialized contracts
- Tables showing all contract types and their specific properties

## Understanding E31.1 Contract

### Conceptual Model

The E31_1_Contract class is fundamentally different from other classes in this ontology because:

1. **It's a Parent Class**: E31_1_Contract serves as the foundation for all specialized contract types. It doesn't typically have instances itself; instead, instances are of its subclasses.

2. **Document vs. Event Separation**: The contract class represents the *document* that records a transaction, not the transaction itself. The actual transaction (acquisition, activity, etc.) is modeled through the P70_documents property.

3. **Inheritance Structure**: All specialized contract types inherit from E31_1_Contract:
   - E31.2 Sales Contract
   - E31.3 Arbitration Agreement
   - E31.4 Cession of Rights Contract
   - E31.7 Donation Contract
   - E31.8 Dowry Contract

### Practical Usage

**When to use E31_1_Contract:**
- When describing a notarial contract that doesn't fit specialized types
- As the parent class in ontology definitions
- For generic contract properties that apply to all contract types

**When to use specialized types:**
- Always prefer specialized types when the contract fits a defined category
- Use E31_2_Sales_Contract for sales transactions
- Use E31_7_Donation_Contract for gifts and donations
- Use E31_8_Dowry_Contract for marriage-related property transfers
- And so on for other specialized types

### Properties Available

E31_1_Contract instances can use all standard document properties:

- **Identification**: P1.1 (name), P102.1 (title)
- **Creation**: P94i.1 (created by), P94i.2 (enactment date), P94i.3 (place of enactment)
- **Context**: P46i.1 (contained in register), P70_documents (documents event)
- **Annotation**: P3.1 (editorial note)

Specialized contract types add additional properties specific to their transaction type.

## Implementation Status

### Already Implemented ✓

The E31_1_Contract class is **already fully implemented** in the current ontology:

- **Class Definition**: Defined in gmn_ontology.ttl (lines 42-49)
- **Subclasses**: All specialized contract types properly inherit from E31_1_Contract
- **Properties**: Uses standard cidoc:E31_Document properties
- **Transformations**: Standard document property transformations apply

### No Changes Needed

Unlike specialized contract types (which add new properties), E31_1_Contract requires:
- ✓ No new class definitions (already exists)
- ✓ No new properties (uses inherited properties)
- ✓ No new transformations (uses standard document transformations)
- ✓ No ontology file additions needed

### Documentation Purpose

This package exists to:
1. **Document the existing class** and its role in the ontology
2. **Explain the inheritance structure** to ontology users
3. **Provide examples** of how general contracts relate to specialized types
4. **Clarify best practices** for when to use general vs. specialized contract classes

## Ontology Structure Overview

```
cidoc:E31_Document
  └── gmn:E31_1_Contract (General Contract) ← This class
      ├── gmn:E31_2_Sales_Contract
      ├── gmn:E31_3_Arbitration_Agreement
      ├── gmn:E31_4_Cession_of_Rights_Contract
      ├── gmn:E31_7_Donation_Contract
      └── gmn:E31_8_Dowry_Contract
  └── gmn:E31_5_Declaration (not a contract)
  └── gmn:E31_6_Correspondence (not a contract)
```

## Specialized Contract Types Reference

| Class | Purpose | Specific Properties |
|-------|---------|-------------------|
| E31.1 Contract | Parent class for all contracts | None (uses document properties) |
| E31.2 Sales Contract | Property sales | P70.14 (seller), P70.15 (buyer), P70.16 (price) |
| E31.3 Arbitration | Dispute resolution | P70.18 (disputing party), P70.19 (arbitrator) |
| E31.4 Cession | Rights transfer | P70.21 (conceding party), P70.22 (receiving party) |
| E31.7 Donation | Gift transfer | P70.32 (donor), P70.22 (receiving party) |
| E31.8 Dowry | Marriage property | P70.32 (donor), P70.22 (receiving party) |

## Usage Guidelines

### Best Practices

1. **Prefer Specialized Types**: Always use the most specific contract class available
2. **Understand Inheritance**: Specialized types inherit all properties of E31_1_Contract
3. **Document Separation**: Remember that contracts document events, they don't represent them
4. **Property Domains**: Check which properties apply to which contract types

### Common Patterns

**Pattern 1: Creating a specialized contract**
```turtle
<contract001> a gmn:E31_2_Sales_Contract ;  # Specific type, not E31_1_Contract
    gmn:P1_1_has_name "Sale of House on Via San Lorenzo" ;
    gmn:P94i_1_was_created_by <notary_antonio> ;
    gmn:P94i_2_has_enactment_date "1450-03-15"^^xsd:date ;
    gmn:P70_14_indicates_seller <giovanni_doria> ;
    gmn:P70_15_indicates_buyer <marco_spinola> .
```

**Pattern 2: Querying all contracts**
```sparql
SELECT ?contract WHERE {
    ?contract a/rdfs:subClassOf* gmn:E31_1_Contract .
}
```

## File Descriptions

### contract-implementation-guide.md
Comprehensive guide for developers and ontologists covering:
- Conceptual understanding of general contracts
- Relationship to specialized contract types  
- No implementation steps needed (already exists)
- Best practices for ontology extension

### contract-documentation.md
Formal semantic documentation including:
- Complete class definition with TTL
- CIDOC-CRM compliance explanation
- Inheritance hierarchy visualization
- Property specifications
- Usage examples and patterns

### contract-ontology.ttl
Reference file containing:
- Existing class definition from gmn_ontology.ttl
- Comments explaining the parent class role
- No new definitions to add

### contract-transform.py
Reference documentation showing:
- That E31_1_Contract uses standard transformations
- How specialized types extend with their own transformations
- No new transformation functions needed

### contract-doc-note.txt
Documentation snippets for adding to project docs:
- Overview text explaining the contract hierarchy
- Examples of usage patterns
- Tables of contract types and properties

## Related Documentation

This general contract documentation should be read in conjunction with:

- **Specialized Contract Types**: 
  - Sales Contract documentation (in main ontology)
  - Donation Contract documentation (donation-documentation.md)
  - Dowry Contract documentation (dowry-documentation.md)
  - Arbitration Agreement documentation (arbitration-ontology.md)
  - Cession Contract documentation (in main ontology)

- **Declaration Documents**: See declaration documentation (not contracts)
- **Correspondence Documents**: See correspondence documentation (not contracts)

## Support Information

### Questions and Issues

- **Class Structure Questions**: Refer to contract-documentation.md
- **Implementation Questions**: Refer to contract-implementation-guide.md
- **Property Usage**: Check specialized contract documentation
- **CIDOC-CRM Compliance**: See transformation examples in contract-documentation.md

### Common Misunderstandings

1. **"Do I need to instantiate E31_1_Contract?"**
   - Usually no - use specialized types instead
   - E31_1_Contract is primarily a parent class for inheritance

2. **"What properties does E31_1_Contract have?"**
   - It uses standard cidoc:E31_Document properties
   - Specialized types add their own specific properties

3. **"How do I add a new contract type?"**
   - Create a new subclass of gmn:E31_1_Contract
   - Add specific properties for your contract type
   - Follow the patterns in specialized contract documentation

## Version Information

- **Package Version**: 1.0
- **Ontology Version**: 1.5
- **Class Definition**: Already in gmn_ontology.ttl since v1.0
- **Last Updated**: 2025-10-26
- **Status**: Documentation package (class already implemented)

## Next Steps

After reviewing this package:

1. **For Ontology Understanding**:
   - Read the complete documentation in contract-documentation.md
   - Review specialized contract type documentation
   - Understand the inheritance hierarchy

2. **For Data Entry**:
   - Always use the most specific contract type available
   - Consult specialized contract documentation for properties
   - Use P70_documents to link to the documented event

3. **For Ontology Extension**:
   - Follow the pattern of existing specialized contract types
   - Create subclasses of E31_1_Contract for new contract types
   - Add specific shortcut properties as needed

## Contact

For questions about this documentation package or the E31_1_Contract class:
- Refer to the Genoese Merchant Networks project documentation
- Contact the ontology maintainer
- Review the CIDOC-CRM specification at http://www.cidoc-crm.org/

---

**Note**: This is a documentation package for an already-implemented class. Unlike deliverables for new contract types (such as dowry or donation contracts), this package does not contain new ontology definitions or transformation code to add. Instead, it documents the existing E31_1_Contract class and explains its role as the parent class for all specialized contract types.
